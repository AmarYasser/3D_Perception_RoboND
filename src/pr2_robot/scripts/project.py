#!/usr/bin/env python

# Import modules
import numpy as np
import sklearn
from sklearn.preprocessing import LabelEncoder
import pickle
from sensor_stick.srv import GetNormals
from sensor_stick.features import compute_color_histograms
from sensor_stick.features import compute_normal_histograms
from visualization_msgs.msg import Marker
from sensor_stick.marker_tools import *
from sensor_stick.msg import DetectedObjectsArray
from sensor_stick.msg import DetectedObject
from sensor_stick.pcl_helper import *

import rospy
import tf
from geometry_msgs.msg import Pose
from std_msgs.msg import Float64
from std_msgs.msg import Int32
from std_msgs.msg import String
from pr2_robot.srv import *
from rospy_message_converter import message_converter
import yaml


# Helper function to get surface normals
def get_normals(cloud):
    get_normals_prox = rospy.ServiceProxy('/feature_extractor/get_normals', GetNormals)
    return get_normals_prox(cloud).cluster

# Helper function to create a yaml friendly dictionary from ROS messages
def make_yaml_dict(test_scene_num, arm_name, object_name, pick_pose, place_pose):
    yaml_dict = {}
    yaml_dict["test_scene_num"] = test_scene_num.data
    yaml_dict["arm_name"]  = arm_name.data
    yaml_dict["object_name"] = object_name.data
    yaml_dict["pick_pose"] = message_converter.convert_ros_message_to_dictionary(pick_pose)
    yaml_dict["place_pose"] = message_converter.convert_ros_message_to_dictionary(place_pose)
    return yaml_dict

# Helper function to output to yaml file
def send_to_yaml(yaml_filename, dict_list):
    data_dict = {"object_list": dict_list}
    with open(yaml_filename, 'w') as outfile:
        yaml.dump(data_dict, outfile, default_flow_style=False)

# Callback function for your Point Cloud Subscriber
def pcl_callback(pcl_msg):

# Exercise-2 TODOs:

    # TODO: Convert ROS msg to PCL data
    cloud_filtered = ros_to_pcl(pcl_msg)
    # TODO: Statistical Outlier Filtering
    # Much like the previous filters, we start by creating a filter object: 
    outlier_filter = cloud_filtered.make_statistical_outlier_filter()

    # Set the number of neighboring points to analyze for any given point
    outlier_filter.set_mean_k(50)

    # Set threshold scale factor
    x = 0.0001

    # Any point with a mean distance larger than global (mean distance+x*std_dev) will be considered outlier
    outlier_filter.set_std_dev_mul_thresh(x)

    # Finally call the filter function for magic
    cloud_filtered = outlier_filter.filter()
      
    # TODO: Voxel Grid Downsampling
    vox = cloud_filtered.make_voxel_grid_filter()
    LEAF_SIZE = 0.01
    # Set the voxel (or leaf) size  
    vox.set_leaf_size(LEAF_SIZE, LEAF_SIZE, LEAF_SIZE)

    # Call the filter function to obtain the resultant downsampled point cloud
    cloud_filtered = vox.filter()
    #filename = 'voxel_downsampled.pcd'
    #pcl.save(cloud_filtered, filename)
    # TODO: PassThrough Filter
    # TODO: RANSAC Plane Segmentation
    # TODO: Extract inliers and outliers
# PassThrough filter
# Create a PassThrough filter object.
    passthrough_z = cloud_filtered.make_passthrough_filter()

# Assign axis and range to the passthrough filter object.
    filter_axis = 'z'
    passthrough_z.set_filter_field_name(filter_axis)
    axis_min = 0.6
    axis_max = 1.1
    passthrough_z.set_filter_limits(axis_min, axis_max)
    cloud_filtered = passthrough_z.filter()
   ##################
    passthrough_y = cloud_filtered.make_passthrough_filter()
    filter_axis = 'y'
    passthrough_y.set_filter_field_name(filter_axis)
    axis_min = -0.5
    axis_max = 0.5
    passthrough_y.set_filter_limits(axis_min, axis_max)
    cloud_filtered = passthrough_y.filter()
# Finally use the filter function to obtain the resultant point cloud. 
    #cloud_filtered = passthrough.filter()
    #filename = 'pass_through_filtered.pcd'
    #pcl.save(cloud_filtered, filename)


# RANSAC plane segmentation
# Create the segmentation object
    seg = cloud_filtered.make_segmenter()

# Set the model you wish to fit 
    seg.set_model_type(pcl.SACMODEL_PLANE)
    seg.set_method_type(pcl.SAC_RANSAC)

# Max distance for a point to be considered fitting the model
# Experiment with different values for max_distance 
# for segmenting the table
    max_distance = 0.01
    seg.set_distance_threshold(max_distance)

# Call the segment function to obtain set of inlier indices and model coefficients
    inliers, coefficients = seg.segment()


# Extract inliers
    cloud_objects = cloud_filtered.extract(inliers , negative = True)
    #filename = 'cloud_objects.pcd'
    #pcl.save(extracted_inliers,filename)

# Save pcd for table
# pcl.save(cloud, filename)


# Extract outliers

    cloud_table = cloud_filtered.extract(inliers , negative = False)
    #filename = 'cloud_table.pcd'
    #pcl.save(extracted_outliners,filename)

    # TODO: Euclidean Clustering
    white_cloud=XYZRGB_to_XYZ(cloud_objects)
    tree = white_cloud.make_kdtree()
    # TODO: Create Cluster-Mask Point Cloud to visualize each cluster separately
    ec = white_cloud.make_EuclideanClusterExtraction()
    ec.set_ClusterTolerance(0.05)
    ec.set_MinClusterSize(20)
    ec.set_MaxClusterSize(6000)
    # Search the k-d tree for clusters
    ec.set_SearchMethod(tree)
    # Extract indices for each of the discovered clusters
    cluster_indices = ec.Extract()
    cluster_color = get_color_list(len(cluster_indices))

    color_cluster_point_list = []

    for j, indices in enumerate(cluster_indices):
        for i, indice in enumerate(indices):
            color_cluster_point_list.append([white_cloud[indice][0],
                                        white_cloud[indice][1],
                                        white_cloud[indice][2],
                                         rgb_to_float(cluster_color[j])])
    
    #Create new cloud containing all clusters, each with unique color
    cluster_cloud = pcl.PointCloud_PointXYZRGB()
    cluster_cloud.from_list(color_cluster_point_list)


    
    # TODO: Convert PCL data to ROS message
    ros_cluster_cloud = pcl_to_ros(cluster_cloud)
    ros_cloud_objects=pcl_to_ros(cloud_objects)
    ros_cloud_table=pcl_to_ros(cloud_table)

    # TODO: Publish ROS messages
    pcl_cluster_pub.publish(ros_cluster_cloud)
    pcl_objects_pub.publish(ros_cloud_objects)
    pcl_table_pub.publish(ros_cloud_table)

# Exercise-3 TODOs: 

    # Classify the clusters! (loop through each detected cluster one at a time)
    detected_objects_labels = []
    detected_objects = []
    for index,pts_list in enumerate (cluster_indices):
    # Grab the points for the cluster
        pcl_cluster = cloud_objects.extract(pts_list)
        # Convert the cluster from pcl to ROS using helper function
        ros_cluster = pcl_to_ros(pcl_cluster)       
        # Compute the associated feature vector
        color_hists = compute_color_histograms(ros_cluster, using_hsv=True)
        normals=get_normals(ros_cluster)
        normal_hists = compute_normal_histograms(normals)
        feature = np.concatenate((color_hists, normal_hists))
        # Make the prediction, retrieve the label for the result
        # and add it to detected_objects_labels list
        prediction = clf.predict(scaler.transform(feature.reshape(1,-1)))
        label = encoder.inverse_transform(prediction)[0]
        detected_objects_labels.append(label)

        # Publish a label into RViz
        label_pos = list(white_cloud[pts_list[0]])
        label_pos[2] += .1
        object_markers_pub.publish(make_label(label,label_pos, index))

        # Add the detected object to the list of detected objects.
        do = DetectedObject()
        do.label = label
        do.cloud = ros_cluster
        detected_objects.append(do)

    rospy.loginfo('Detected {} objects: {}'.format(len(detected_objects_labels), detected_objects_labels))

    # Publish the list of detected objects
    # This is the output you'll need to complete the upcoming project!
    detected_objects_pub.publish(detected_objects)

    # Suggested location for where to invoke your pr2_mover() function within pcl_callback()
    # Could add some logic to determine whether or not your object detections are robust
    # before calling pr2_mover()
    if len(detected_objects)>0:
        try:
            pr2_mover(detected_objects)
        except rospy.ROSInterruptException:
            pass
    else:
        rospy.loginfo('-----There is no object detected-----')

# function to load parameters and request PickPlace service
def pr2_mover(object_list):

    # TODO: Initialize variables
    test_scene_num = Int32()
    test_scene_num.data = 2 # changed with scene
    outputfile = "output_2.yaml" # changed with scene

    object_name = String()
    #object_group =String()
    arm_name = String()

    dropbox_name = []
    dropbox_group = []
    dropbox_position = []

    # TODO: Get/Read parameters
    object_list_param = rospy.get_param('/object_list')
    dropbox_list_param = rospy.get_param('/dropbox')

    # TODO: Parse parameters into individual variables
    for i in range(0, len(dropbox_list_param)):
        dropbox_name.append(dropbox_list_param[i]['name'])         # 0 : Left --- 1 : Right
        dropbox_group.append(dropbox_list_param[i]['group'])       # 0 : red --- 1 : green
        dropbox_position.append(dropbox_list_param[i]['position']) # 0 : Left --- 1 : Right

    # TODO: Rotate PR2 in place to capture side tables for the collision map
    # TODO: Loop through the pick list
    dict_list = []
    for i in range(0, len(object_list)):

        # TODO: Get the PointCloud for a given object and obtain it's centroid
        labels = []
        centroids = [] # to be list of tuples (x, y, z)
	for object in object_list:
            labels.append(object.label)
            points_arr = ros_to_pcl(object.cloud).to_array()
            centroids.append(np.mean(points_arr, axis=0)[:3])
        
        # populate to object data
        object_name.data = object_list_param[i]['name']
        object_group = object_list_param[i]['group']

        # TODO: Create 'place_pose' for the object
        pick_pose= Pose()
        place_pose= Pose()
	# Assgin the dropboxes based on the object_group
        #place_pose
        if object_group == dropbox_group[0]: # red 
            arm_name.data = dropbox_name[0]  # Left
            place_pose.position.x = dropbox_position[0][0]
            place_pose.position.y = dropbox_position[0][1]
            place_pose.position.z = dropbox_position[0][2]
            print (" ------ Place_Pose () is Assigned ------")

        elif object_group == dropbox_group[1]: # Green
            arm_name.data = dropbox_name[1]    # Right
            place_pose.position.x = dropbox_position[1][0]
            place_pose.position.y = dropbox_position[1][1]
            place_pose.position.z = dropbox_position[1][2]
            print (" ------ Place_Pose () is Assigned ------\n")
        else:
	    print ("Error while assigning the Place_Pose()")
   
        print ("**Picking: "+object_name.data)
        print ("**object will be dropped to the : "+arm_name.data+" dropbox")
        # TODO: Assign the arm to be used for pick_place
        #pickk_pose
        # Assignt the pick position (centroids) based on labels
        object_index = labels.index(object_name.data)
        #print ("**Picking: "+object_name.data)
        pick_pose.position.x = np.asscalar(centroids[object_index][0]) # Using np.asscalar to adjust the centroids formats
        pick_pose.position.y = np.asscalar(centroids[object_index][1])
        pick_pose.position.z = np.asscalar(centroids[object_index][2])
        print ("\n ------ Pick_Pose () is Assigned ------ \n")
        
        # TODO: Create a list of dictionaries (made with make_yaml_dict()) for later output to yaml format
        yaml_dict = make_yaml_dict(test_scene_num, arm_name, object_name, pick_pose, place_pose)
        dict_list.append(yaml_dict)
        # TODO: Output your request parameters into output yaml file
        send_to_yaml(outputfile, dict_list) 
	print ("\n ------ output yaml file is created ------ ") 
        # Wait for 'pick_place_routine' service to come up
        #rospy.wait_for_service('pick_place_routine')

        #try:
        #    pick_place_routine = rospy.ServiceProxy('pick_place_routine', PickPlace)

            # TODO: Insert your message variables to be sent as a service request
        #    resp = pick_place_routine(test_scene_num, object_name, arm_name, pick_pose, place_pose)
        #    print (" -------- pick_place_routine is done -------\n")
        #    print ("Response: ",resp.success)
            
        #except rospy.ServiceException, e:
        #    print "Service call failed: %s"%e

    # TODO: Output your request parameters into output yaml file
    #send_to_yaml(outputfile, dict_list)
    



if __name__ == '__main__':
    # TODO: ROS node initialization
    rospy.init_node('clustering',anonymous=True)

    # TODO: Create Subscribers
    pcl_sub = rospy.Subscriber("/pr2/world/points",pc2.PointCloud2, pcl_callback ,queue_size=1)

    # TODO: Create Publishers
    pcl_objects_pub = rospy.Publisher("/pcl_objects", PointCloud2, queue_size=1)
    pcl_table_pub = rospy.Publisher("/pcl_table", PointCloud2, queue_size=1)
    pcl_cluster_pub = rospy.Publisher("/pcl_cluster", PointCloud2, queue_size=1)
    object_markers_pub = rospy.Publisher("/object_markers", Marker, queue_size=1)
    detected_objects_pub = rospy.Publisher("/detected_objects",DetectedObjectsArray, queue_size=1)
    pr2_base_mover_pub   = rospy.Publisher("/pr2/world_joint_controller/command", Float64, queue_size=10)
    

    # TODO: Load Model From disk
    model = pickle.load(open('model_w2.sav', 'rb'))
    clf = model['classifier']
    encoder = LabelEncoder()
    encoder.classes_ = model['classes']
    scaler = model['scaler']

    # Initialize color_list
    get_color_list.color_list = []

    # TODO: Spin while node is not shutdown
    while not rospy.is_shutdown():
     rospy.spin()
