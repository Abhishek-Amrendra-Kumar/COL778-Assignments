
from perception import Perception
import numpy as np




class Planner:
    def __init__(self, manipulator):
        self.perceptor = Perception(manipulator)

    def get_clear_task_plan(self, objs, z=0.041):
        '''
        returns a sequential action plan executable by manipulator to place all the objects in the plate
        you can write the plans for specific objects such that plan steps are manipulator function calls, and robust to object location randomization
        '''
        plan = []
        plate_key = None
        for key in objs.keys():
            if 'plateId' in key:
                plate_key = key
                break
                
        if not plate_key and len(objs) > 0:
            plate_key = list(objs.keys())[0]
            
        for obj_key in objs.keys():
            if obj_key != plate_key:
                a = objs[obj_key].get_axis_aligned_bounding_box()
                b = a.get_max_bound()- a.get_min_bound()
                if np.abs(b).min() < 0.1:
                    plan.extend(self.pick_place_object_plan(obj_key, plate_key, objs, z))
                
        return plan

    def pick_place_object_plan(self, obj_label, place_location_label, objs, z=0.041):
        '''
        returns a sequential action plan executable by manipulator to pick a object and place it at a specified location
        args
            obj_label : label of object to pick
            place_location label : label of object on which the object is to be placed
        '''
        import pybullet as p
        
        def plan_step():
            pick_pose = self.perceptor.get_object_pick_pose(obj_label, objs)
            place_pose = self.perceptor.get_obj_place_pose(obj_label, place_location_label, objs)
        
            pick_pos = list(pick_pose[:3])
            pick_orn = p.getQuaternionFromEuler(list(pick_pose[3:6]))
            
            place_pos = list(place_pose[:3])
            place_orn = p.getQuaternionFromEuler(list(place_pose[3:6]))
            
            self.perceptor.manipulator.pick_object_from(pick_pos, list(pick_orn), z)
            self.perceptor.manipulator.place_object_at(place_pos, list(place_orn))
            
            self.perceptor.manipulator.move_home()
                
        return [plan_step]