from base import RGBDSensor
from control import Manipulator

from ultralytics import YOLO
import open3d as o3d
import numpy as np
import cv2
import math
import time
# from tqdm import tqdm


class ObjectDetector:
    def __init__(self,):
        self.detector = YOLO("./weights/best.pt")

    def detect_objects(self, rgbImage):
        '''
        returns obj_labels and 2D bounding box the objects in the rgb image
        args
            rgbImage : RGB image containing object to be identified

        please note that due to openCV default BGR convention, you will need to 
        first convert the image to BGR before feeding to the detector
        '''
        bgr = cv2.cvtColor(rgbImage, cv2.COLOR_RGB2BGR)
        results = self.detector(bgr, verbose=False)
        
        detections = []
        if len(results) > 0:
            result = results[0]
            for box in result.boxes:
                label = result.names[int(box.cls[0])]
                bbox = box.xyxy[0].cpu().numpy()
                detections.append((label, bbox))
                
        return detections


class Perception:
    def __init__(self, manipulator:Manipulator):
        self.sensor = RGBDSensor()
        self.obj_detector = ObjectDetector()
        self.manipulator = manipulator
        self.depth_processor = DepthProcessor()

    def generate_exploration_poses(self,):
        '''
        returns list of 7D joint poses to explore the scene
        '''
        home = self.manipulator.PANDA_HOME_POSITION
        yaws = np.linspace(-math.pi/2, math.pi/2, 5).tolist()
        pitches = [-0.9, -0.6, -0.3]
        
        exploration_poses = []
        for i, pitch in enumerate(pitches):
            current_yaws = yaws if i % 2 == 0 else yaws[::-1]
            for yaw in current_yaws:
                pose = list(home)
                pose[0] = yaw
                pose[1] = pitch
                exploration_poses.append(pose)
        return exploration_poses

    # def plot_bounding_boxes(self, clusters):
    #     client = self.manipulator.pybullet_client
    #     for cluster in clusters:
    #         bbox = cluster.get_axis_aligned_bounding_box()
    #         min_b = bbox.get_min_bound()
    #         max_b = bbox.get_max_bound()
            
    #         xmin, ymin, zmin = min_b
    #         xmax, ymax, zmax = max_b
            
    #         pts = [
    #             [xmin, ymin, zmin], [xmax, ymin, zmin],
    #             [xmin, ymax, zmin], [xmax, ymax, zmin],
    #             [xmin, ymin, zmax], [xmax, ymin, zmax],
    #             [xmin, ymax, zmax], [xmax, ymax, zmax]
    #         ]
            
    #         lines = [
    #             (0,1), (0,2), (1,3), (2,3),
    #             (4,5), (4,6), (5,7), (6,7),
    #             (0,4), (1,5), (2,6), (3,7)
    #         ]
            
    #         for i, j in lines:
    #             client.addUserDebugLine(pts[i], pts[j], lineColorRGB=[1, 1, 0], lineWidth=2, lifeTime=0)

    def identify_objects(self, pointcloud_clusters, x=-.1, y=-.1):
        '''
        assigns labels to all object clusters in the pointcloud_clusters
        args
            pointcloud_clusters : clustered pointclouds
        returns
            objs : dictionary containing labels and spatial information of all the objects in the scene
                    {obj_label: obj_pointcloud}
        '''
        objs = {}
        client = self.manipulator.pybullet_client
        pandaId = self.manipulator.pandaId
        
        # self.plot_bounding_boxes(pointcloud_clusters)
        
        for cluster in pointcloud_clusters:
            self.manipulator.move_home()
                
            center = self.depth_processor.get_cluster_top_position(cluster)
            if np.linalg.norm(center) < 0.15:
                continue
            top_pos = np.array(center) + np.array([x, y, 0.42])
            hand_state = client.getLinkState(pandaId, 11)
            home_orientation = hand_state[1] 
            self.manipulator.move_in_task_space(list(top_pos), list(home_orientation))
            top_pos = np.array(center) + np.array([x, y, 0.38])
            time.sleep(0.5)
            self.manipulator.move_in_task_space(list(top_pos), list(home_orientation))

            time.sleep(0.5)
            
            rgb, depth, T_cb, intrinsics = self.sensor.get_observation(client, pandaId)
            detections = self.obj_detector.detect_objects(rgb)
            u, v = self.depth_processor.project_world_to_image(center, intrinsics, T_cb)
            
            matched_label = None
            best_dist = float('inf')
            
            if u != -1 and v != -1:
                for label, bbox in detections:
                    xmin, ymin, xmax, ymax = bbox
                    if xmin <= u <= xmax and ymin <= v <= ymax:
                        bcx, bcy = (xmin+xmax)/2, (ymin+ymax)/2
                        dist = (bcx - u)**2 + (bcy - v)**2
                        if dist < best_dist:
                            best_dist = dist
                            matched_label = label
            if not matched_label:
                matched_label = "plateId"
            objs[matched_label] = cluster
                
            self.manipulator.move_home()
                
        return objs

    def get_object_pick_pose(self, obj_label:str, objs:dict):
        '''
        returns 6D pose of the queried object: obj_label
        args
            obj_label : query object label
            objs : dictionary containing labels and spatial information of all the objects in the scene
        '''
        cluster = objs[obj_label]
        center = self.depth_processor.get_cluster_top_position(cluster)
        center[2] = cluster.get_axis_aligned_bounding_box().get_max_bound()[2]
        pick_pose = [np.float64(center[0]), np.float64(center[1]), np.float64(center[2]), math.pi, 0.0, 0]
        return pick_pose


    def get_obj_place_pose(self, obj_label:str, target_obj_label:str, objs:dict):
        '''
        returns 6D target pose for object to be placed at target object location
        args
            obj_label : to be placed object label
            target_obj_label : label of the object on which object is to be placed
            objs : dictionary containing labels and spatial information of all the objects in the scene
        '''
        target_cluster = objs[target_obj_label]
        target_bbox = target_cluster.get_axis_aligned_bounding_box()
        max_bound = target_bbox.get_max_bound()
        target_center = target_bbox.get_center()
        # import random
        place_pose = [np.float64(target_center[0]), np.float64(target_center[1]), np.float64(max_bound[2])+0.05, math.pi, 0.0, 0]
        return place_pose
    
    def exlpore_scene(self, exlporation_poses:list[list]):
        '''
        explore the scene using generated exploration poses and return collected pointclouds
        args
            exploration_poses : list with set of proposed 7D joint positions fullfilling environment/scene exploration
        returns
            pointclouds : list of collected pointclouds from the exploration
        '''
        self.manipulator.move_home()
        pointclouds = []
        p = self.manipulator.pybullet_client
        pandaId = self.manipulator.pandaId
        width = self.sensor.IMG_WIDTH
        height = self.sensor.IMG_HEIGHT

        for pose in exlporation_poses:
            self.manipulator.move_joints(pose)
            # time.sleep(0.2)
            
            rgb, depth, T_cb, intrinsics = self.sensor.get_observation(p, pandaId)
            pcd = self.depth_processor.rgbd_to_pointcloud(rgb, depth, intrinsics, width, height)
            pcd_base = self.depth_processor.transform_pointcloud(pcd, T_cb)
            pointclouds.append(pcd_base)
        self.manipulator.move_home()
        
        return pointclouds


class DepthProcessor:
    def __init__(self,):
        pass

    def rgbd_to_pointcloud(self, rgb, depth, intrinsics, width, height):
        '''
        returns a colored pointcloud in the camera frame
        args
            rgb : RGB image
            depth : depth image
            intrinsics : list - [fx, fy, cx, cy] : intrinsic parameters from k matrix
        '''
        fx, fy, cx, cy = intrinsics
        u, v = np.meshgrid(np.arange(width), np.arange(height))
        
        Z = depth
        X = (u-cx)*Z/fx
        Y = (v-cy)*Z/fy
        
        points = np.stack((X, Y, Z), axis=-1).reshape(-1, 3)
        colors = rgb.reshape(-1, 3) / 255.0
        valid_idx = Z.reshape(-1) > 0
        pcd = o3d.geometry.PointCloud()
        if np.any(valid_idx):
            pcd.points = o3d.utility.Vector3dVector(points[valid_idx])
            pcd.colors = o3d.utility.Vector3dVector(colors[valid_idx])
            
        return pcd

    def transform_pointcloud(self, pointcloud:o3d.geometry.PointCloud, transform):
        '''
        returns a pointcloud transformed in the target transform frame
        args
            pointcloud : 
            transform : 
        returns
            pointcloud_base : pointcloud transformed in the robot base frame
        '''
        import copy
        pointcloud_base = copy.deepcopy(pointcloud)
        pointcloud_base.transform(transform)
        return pointcloud_base

    def register_pointclouds(self, pcds:list):
        '''
        returns a poincloud aligned in a single frame
        args
            pcds : list of pointclouds
        returns
            scene_pointcloud : combined and aligned pointcloud in a single frame from pcds
        '''
        if not pcds:
            return o3d.geometry.PointCloud()
            
        scene_pointcloud = pcds[0]
        for i in range(1, len(pcds)):
            source = pcds[i]
            init_transform = np.eye(4)
            threshold = 0.02
            reg_p2p = o3d.pipelines.registration.registration_icp(
                source, scene_pointcloud, threshold, init_transform,
                o3d.pipelines.registration.TransformationEstimationPointToPoint()
            )
            source.transform(reg_p2p.transformation)
            scene_pointcloud += source
        return scene_pointcloud

    def visualize_pointcloud(self, pcds:list[o3d.geometry.PointCloud]):
        '''
        this function will visualize the pointcloud(s) present in the list `pcds`
        args
            pcds: list of pointclouds to be visualized (could be single/multiple pointclouds)
        '''
        o3d.visualization.draw_geometries(pcds)

    def remove_plane(self, scene_pcd):
        '''
        this function removes a plane that maximally fits a plane equation (criterion)
        args
            scene_pcd : pointcloud of a scene
        '''
        scene_pcd = scene_pcd.voxel_down_sample(voxel_size=0.005)
        distance_threshold = 0.015
        ransac_n = 3
        num_iterations = 1000
        plane_model, inliers = scene_pcd.segment_plane(distance_threshold=distance_threshold,
                                                       ransac_n=ransac_n,
                                                       num_iterations=num_iterations)
        extracted_objects = scene_pcd.select_by_index(inliers, invert=True)
        return extracted_objects

    def remove_planes(self, scene_pcd):
        '''
        this function iteratively removes multiple planes from the scene_pcd
        '''
        extracted_objects = self.remove_plane(self.remove_plane(scene_pcd))
        return extracted_objects

    def cluster_objects(self, scene_pcd):
        '''
        this function clusters the pointcloud
        args
            scene_pcd : merged pointcloud of the scene
        '''
        eps = (0.03125+0.0390625)/2
        # print(eps)
        min_points = 5
        
        labels = np.array(scene_pcd.cluster_dbscan(eps=eps, min_points=min_points, print_progress=False))
        
        clusters = []
        if len(labels) == 0:
            return clusters
            
        max_label = labels.max()
        for i in range(max_label + 1):
            indices = np.where(labels == i)[0]
            if len(indices) >= 200:
                cluster_pcd = scene_pcd.select_by_index(indices)
                clusters.append(cluster_pcd)
                
        return clusters

    def get_cluster_top_position(self, cluster):
        '''
        args
            cluster : a cluster from the clustered pointcloud which manipulator aims to understand
        '''
        return cluster.get_axis_aligned_bounding_box().get_center()
    
    def project_world_to_image(self, point_world, intrinsics, T_cb):
        """
        args:
            point_world : (x,y,z) in robot base (world) frame
            intrinsics : list [fx, fy, cx, cy] - camera intrinsic parameters
            T_cb: (4x4) transform of camera frame wrt robot base frame
        returns:
            (u, v): pixel coordinates
        """
        fx, fy, cx, cy = intrinsics
        p_w_h = np.array([point_world[0], point_world[1], point_world[2], 1.0])
        T_bc = np.linalg.inv(T_cb)
        p_c = T_bc @ p_w_h
        X_c, Y_c, Z_c = p_c[:3]
        
        if Z_c <= 1e-5:
            return (-1, -1)
            
        u = int((X_c * fx / Z_c) + cx)
        v = int((Y_c * fy / Z_c) + cy)
        
        return (u, v)
