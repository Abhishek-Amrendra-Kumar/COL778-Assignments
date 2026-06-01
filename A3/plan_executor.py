import os
import pickle
import numpy as np
import matplotlib.pyplot as plt
import pdb 
from ai2thor.controller import Controller
import os
import pdb
import argparse
import imageio
from PIL import Image 
from task_context import get_task_context


class PlanExecutor:

    def __init__(self, task_context, debug = True, log = True) -> None:
        self.task_context = task_context
        self.debug = debug
        self.log = log
        self.init_env()
        self.ego_frames = []
        self.third_party_frames = []
        self.log_lines = []
        self.action_no = 0
        self.action_metadata_keys = ["lastAction", "lastActionSuccess", "errorMessage", "actionReturn"]
        
    
    def init_env(self):
        self.controller = Controller()
        self.controller.reset(
            scene=self.task_context["scene"],
            visibilityDistance=1.5,
            gridSize=0.01,
            fieldOfView=120,
            width=500,
            height=500,
            renderDepthImage=False,
            renderNormalsImage=False,
            renderInstanceSegmentation=False,
            renderSemanticSegmentation=False,
        )
        object_poses = [
            {
                "objectName": obj["objectName"],
                "position": obj["position"],
                "rotation": obj["rotation"],
            }
            for obj in self.task_context["objects_init_state"]
        ]
        self.controller.step(action="SetObjectPoses", objectPoses=object_poses)
        self.controller.step(action="Done")
        self.controller.step(
            action="Teleport",
            position=self.task_context["robot_init_state"]["position"],
            rotation=self.task_context["robot_init_state"]["rotation"],
            horizon=self.task_context["robot_init_state"]["horizon"],
            standing=True,
        )
        self.controller.step(action="Done")
        self.controller.step(
            action="AddThirdPartyCamera",
            position=dict(x=1.5, y=3.0, z=1.5),
            rotation=dict(x=90, y=0, z=0),
            fieldOfView=120
        )
    def agent_state(self):
        """Return the current agent metadata with an extra 'isHolding' field."""
        event = self.controller.last_event
        agent = event.metadata["agent"]
        agent["isHolding"] = None
        # Determine which object (if any) is currently picked up
        all_objects = self.controller.last_event.metadata["objects"]
        for obj in all_objects:
            if obj.get("pickupable") and obj.get("isPickedUp"):
                agent["isHolding"] = obj
                break
        return agent
    
    def getObjectByType(self, object_type):
        all_objects = self.controller.last_event.metadata["objects"]
        objects = [o for o in all_objects if o["objectType"].lower() == object_type.lower()]
        return objects
        
    def getObjectByName(self, object_name):
        if(object_name == 'bread'):
            #first see if sliced bread is ther
            object_type = 'breadsliced'
            objects = self.getObjectByType(object_type)
            if(len(objects) == 0):
                object_type = 'bread'
                objects = self.getObjectByType(object_type)
            return objects[0]['objectId']
        if(object_name == 'egg'):
            #first see if sliced bread is ther
            object_type = 'eggcracked'
            objects = self.getObjectByType(object_type)
            if(len(objects) == 0):
                object_type = 'egg'
                objects = self.getObjectByType(object_type)
            return objects[0]['objectId']
        elif('counter' in object_name):
            object_type = 'countertop'
            objects = self.getObjectByType(object_type)
            if('counter_1' == object_name):
                return objects[1]['objectId']
            elif('counter_2' == object_name or 'counter_3' == object_name):
                return objects[0]['objectId']
            else:
                raise ValueError(f'Unknown object name {object_name}')
        else:
            if('dining_table' == object_name ):
                object_type = 'diningtable'
            else:
                object_type = object_name
            objects = self.getObjectByType(object_type)
            if(len(objects) == 0):
                raise ValueError(f'Unknown object name {object_name}')
            return objects[0]['objectId']

    def getLocationByName(self, location_name):
        if(location_name not in self.task_context['locations']):
            raise ValueError(f'Unknown location name {location_name}')
        location = self.task_context['locations'][location_name]
        return location['position'], location['rotation']


    def pick(self, objectName, containerName, location):
        objectId = self.getObjectByName(objectName)
        event = self.controller.step(
            action="PickupObject",
            objectId=objectId,
            forceAction=False,
            manualInteract=False)
        return event

    def put(self, objectName, containerName, location):
        containerId = self.getObjectByName(containerName)
        event = self.controller.step(
            action="PutObject",
            objectId=containerId,
            forceAction=False,
            placeStationary=True)
        return event

    def move(self, location_1, location_2):
        position, rotation = self.getLocationByName(location_2)
        event = self.controller.step(
            action="Teleport",
            position=position,
            rotation=rotation,
            horizon=10,
            standing=True,
        )
        return event

    def open(self, objectName, location):
        objectId = self.getObjectByName(objectName)
        event = self.controller.step(
            action='OpenObject', 
            objectId=objectId)
        return event

    def slice(self, objectName, location):
        #TODO should have knife in the hand 
        
        agent = self.agent_state()
        if(agent['isHolding']['objectType'].lower() == 'knife'):
            objectId = self.getObjectByName(objectName)
            event = self.controller.step(
                action="SliceObject",
                objectId=objectId,
                forceAction=False)
        else:
            raise ValueError("Agent should hold knife for slice")
        return event
    
    def turn_on(self, deviceName, location):
        deviceId = self.getObjectByName(deviceName)
        if(deviceName == 'toaster' or deviceName == 'coffeemachine'):
            event = self.controller.step(
                action="ToggleObjectOn",
                objectId=deviceId)
        elif(deviceName == 'stoveburner'):
            stoveknobs = self.getObjectByType('StoveKnob')
            for sk in stoveknobs:
                stove_id = sk['objectId']
                event = self.controller.step(action="ToggleObjectOn",objectId=stove_id)
        return event

    def turn_off(self, deviceName, location):
        deviceId = self.getObjectByName(deviceName)
        event = self.controller.step(
            action="ToggleObjectOff",
            objectId=deviceId)
        return event
    
    def execute_single_action(self,  action):
        action = action.strip()[1:-1].split(' ')
        command = action[0]
        args = action[1:]
        if(command not in self.__dir__()):
            raise ValueError(f'Unknown action {command}')
        command_function = self.__getattribute__(command)
        return command_function(*args)

    def execute_plan_from_file(self, file_name, save_dir = None):
        #log the first stage
        if(self.log):
            self.log_event(self.controller.last_event, first = True)
        file = open(file_name, "r")
        lines = file.readlines()
        if('cost' in lines[-1]):
            lines = lines[:-1]
        for action in lines:
            self.action_no += 1
            event = self.execute_single_action(action)
            if(self.debug):
                print(f'Executing command {action}')
                self.print_action_event(event.metadata)
            if(self.log):
                self.log_event(event)

    def print_action_event(self, metdata):
        for k in self.action_metadata_keys:
            if(k in metdata):
                print(k, ':', metdata[k])
        print("#---------#")

    def log_event(self, event, first = False):
        ego_frame = np.asarray(event.frame)
        ego_frame = Image.fromarray(ego_frame)
        self.ego_frames.append(ego_frame)

        third_party_frame = np.array(event.third_party_camera_frames[0])
        third_party_frame = Image.fromarray(third_party_frame)
        self.third_party_frames.append(third_party_frame)

        if(not first):
            self.log_lines.append(f'Action No. {self.action_no}')
            for k in self.action_metadata_keys:
                if(k in event.metadata):
                    self.log_lines.append(f'{k}: {event.metadata[k]}')
            self.log_lines.append("#---------#")
    
    def save_log(self, out_path, fps = 1/2):
        os.makedirs(out_path, exist_ok=True)

        ego_video_name = os.path.join(out_path, 'ego.mp4')
        writer = imageio.get_writer(ego_video_name, fps=fps)
        for img in self.ego_frames:
            writer.append_data(np.array(img))

        tp_video_name = os.path.join(out_path, 'third_party.mp4')
        writer = imageio.get_writer(tp_video_name, fps=fps)
        for img in self.third_party_frames:
            writer.append_data(np.array(img))

        log_file_name = os.path.join(out_path, 'log.txt')
        log_file = open(log_file_name, 'w')
        for l in self.log_lines:
            log_file.write(l + "\n")

    def close(self):
        self.controller.stop()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="PDDL plan executor")

    parser.add_argument("--task_name", help="Name of the task", default="")
    parser.add_argument("--plan_file", help="Path to the plan file", default="")
    parser.add_argument("--output_path", help="Path where results will be saved", default="")

    args = parser.parse_args()
    task_context = get_task_context(args.task_name)
    plan_executer = PlanExecutor(task_context)
    plan_executer.execute_plan_from_file(args.plan_file)
    plan_executer.save_log(args.output_path)
    plan_executer.close()
