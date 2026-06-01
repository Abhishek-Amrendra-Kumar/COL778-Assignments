import numpy as np
from base import PandaArm
import time


class Manipulator(PandaArm):
    def __init__(self, p, pandaId):
        super().__init__(p, pandaId)

    def is_moving(self,):
        '''
        checks if the manipulator is steady or still in motion
        returns
            moving : bool - ?(manipulator_moving)
        '''
        joint_states = self.pybullet_client.getJointStates(self.pandaId, self.REVOLUTE_JOINTS)
        velocities = [abs(state[1]) for state in joint_states]
        return any(v > 1e-4 for v in velocities)

    def move_joints(self, target_joints:list):
        '''
        moves manipulator joints to target joint poses
        args
            target_joints : 7D list of target joint angles
        '''
        self.pybullet_client.setJointMotorControlArray(
            self.pandaId, self.REVOLUTE_JOINTS, 
            controlMode=self.pybullet_client.POSITION_CONTROL, 
            targetPositions=target_joints,
            positionGains=[0.03]*len(self.REVOLUTE_JOINTS))
        # for i, j in enumerate(self.REVOLUTE_JOINTS):
        #     self.pybullet_client.setJointMotorControl2(bodyIndex=self.pandaId, jointIndex=j, controlMode=self.pybullet_client.POSITION_CONTROL, targetPosition=target_joints[i], maxVelocity=.3)
        iters = 0
        while self.is_moving() and iters < 500:
            self.pybullet_client.stepSimulation()
            time.sleep(1/240)
            iters+=1
        time.sleep(.5)
        return True

    def move_home(self,):
        '''
        moves robot to home position
        '''
        self.move_joints(self.PANDA_HOME_POSITION)

    def move_in_task_space(self, target_position, target_orientation):
        '''
        moves robot end effector to target pose
        args
            target_position : 3D spatial location
            target_orientation : 3D orientation
        '''
        joint_poses = self.pybullet_client.calculateInverseKinematics(
            self.pandaId, 11, targetPosition=target_position, 
            targetOrientation=target_orientation,
            lowerLimits=self.JOINT_LOWER_LIMITS,
            upperLimits=self.JOINT_UPPER_LIMITS,
            restPoses=self.PANDA_HOME_POSITION,
            maxNumIterations=10000,
            residualThreshold=1e-4)
            
        self.move_joints(list(joint_poses[:7]))
    
    def command_gripper(self, open:bool):
        '''
        args
            open: do we want the robot to open its fingers, otherwise close them
        returns
            bool (success/failure)

        This function will simply close or open robots gripper, so to grasp or release the object
        '''
        target_pos = self.PANDA_FINGER_OPEN if open else self.PANDA_FINGER_CLOSED
        self.pybullet_client.setJointMotorControlArray(
            self.pandaId, self.PANDA_PRISMATIC_JOINTS,
            controlMode=self.pybullet_client.POSITION_CONTROL, 
            targetPositions=[target_pos, target_pos], forces=[800]*2, velocityGains=[0.5,0.5]
        )
        for _ in range(50):
            self.pybullet_client.stepSimulation()
            time.sleep(1/240)
        time.sleep(.5)
        return True

    # def plot_waypoints(self, start_pos, waypoints, color=[1, 0, 0]):
    #     '''
    #     plots the waypoints using pybullet debug lines
    #     '''
    #     return
    #     pts = [start_pos] + waypoints
    #     for i in range(len(pts)-1):
    #         self.pybullet_client.addUserDebugLine(pts[i], pts[i+1], lineColorRGB=color, lineWidth=2, lifeTime=0)
    #     for pt in pts:
    #         # draw a small cross at each point
    #         d = 0.02
    #         self.pybullet_client.addUserDebugLine([pt[0]-d, pt[1], pt[2]], [pt[0]+d, pt[1], pt[2]], lineColorRGB=[0,0,1], lineWidth=2, lifeTime=0)
    #         self.pybullet_client.addUserDebugLine([pt[0], pt[1]-d, pt[2]], [pt[0], pt[1]+d, pt[2]], lineColorRGB=[0,0,1], lineWidth=2, lifeTime=0)
    #         self.pybullet_client.addUserDebugLine([pt[0], pt[1], pt[2]-d], [pt[0], pt[1], pt[2]+d], lineColorRGB=[0,0,1], lineWidth=2, lifeTime=0)

    def pick_object_from(self, obj_location:list, obj_orientation:list, z=0.041):
        '''
        perform pick operation for object placed at obj_location, obj_orientation
        args
            obj_location : object location
            obj_orientation : object orienation in euler notation
        '''
        self.command_gripper(open=True)
        
        start_state = self.pybullet_client.getLinkState(self.pandaId, 11)
        start_pos = start_state[0]
        
        hover_location = list(obj_location)
        hover_location[2] += 0.25 
        
        waypoint_location = list(obj_location)
        waypoint_location[2] += 0.1
        waypoint_location[0] += 0.01

        
        descend_location = list(obj_location)
        descend_location[2] -= z
        # print(descend_location)
        # self.plot_waypoints(start_pos, [hover_location, descend_location, hover_location], color=[1, 0, 0])
        
        self.move_in_task_space(hover_location, obj_orientation)
        # time.sleep(10)

        # self.move_in_task_space(waypoint_location, obj_orientation)  
        # time.sleep(10)

        
        self.move_in_task_space(descend_location, obj_orientation)
            
        # time.sleep(1)
        self.command_gripper(open=False)
        # time.sleep(1)
        
        self.move_in_task_space(hover_location, obj_orientation)

        self.move_home()

    def place_object_at(self, target_location:list, target_orientation:list):
        '''
        places the grasped object at target location in target orientation
        '''
        start_state = self.pybullet_client.getLinkState(self.pandaId, 11)
        start_pos = start_state[0]
        
        hover_location = list(target_location)
        hover_location[2] += 0.3
        
        waypoint_location = list(target_location)
        waypoint_location[2] += 0.15
        
        descend_location = list(target_location)
        descend_location[2] += 0.05
        
        # self.plot_waypoints(start_pos, [hover_location, waypoint_location, descend_location, hover_location], color=[0, 1, 0])
        
        self.move_in_task_space(hover_location, target_orientation)
        
        self.move_in_task_space(waypoint_location, target_orientation)
            
        descend_location = list(target_location)
        descend_location[2] += 0.05
        
        self.move_in_task_space(descend_location, target_orientation)
        # time.sleep(1)
        self.command_gripper(open=True)
        # time.sleep(1)
        
        self.move_in_task_space(hover_location, target_orientation)

    def execute_task_plan(self, plan:list):
        '''
        executes a task plan generated by the planner
        args
            plan : list of manipulator executable action steps
        '''
        for action in plan:
            action()