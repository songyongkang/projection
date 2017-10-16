#!/usr/bin/env python
import cv2
import rospy
import message_filters
from sensor_msgs.msg import Image
from geometry_msgs.msg import QuaternionStamped
from vision_msgs.msg import Detection2DArray
from std_msgs.msg import Float32
from std_msgs.msg import Int32
import sys

class validate:

    def __init__(self):
        print("init_node")
        # subscriber to subscribe gazebo camera image
        self.image_gazebo_sub = message_filters.Subscriber("/ShowBoundingBox/filtered/image", Image)
        # subscriber to subcribe pixel values of the 2d bbox from the gazebo plugin
        self.bbox_gazbeo_sub = message_filters.Subscriber("/ShowBoundingBox/filtered/pixels", QuaternionStamped)
        # subscriber to subscribe debug image from the object detector
        self.image_detector_sub = message_filters.Subscriber("/debug_image", Image)
        # subscriber to subcribe pixel values of the 2d bbox from the object detector
        self.bbox_detector_sub = message_filters.Subscriber("/objects", Detection2DArray)

        self.overlap_pub = rospy.Publisher("/validate/overlap_area", Float32, queue_size = 1)
        self.object_id_pub = rospy.Publisher("/validate/object_id", Int32, queue_size = 1)
        self.ts = message_filters.TimeSynchronizer([ self.bbox_gazbeo_sub, self.bbox_detector_sub],100)

        self.ts.registerCallback(self.callback)

    # def callback(self, gz_image, gz_box, dt_image, dt_box):
    def callback(self,gz_box, dt_box):

        # gazebo box max and min corners in 2d
        minx_gz = int(gz_box.quaternion.x)
        maxx_gz = int(gz_box.quaternion.y)
        miny_gz = int(gz_box.quaternion.z)
        maxy_gz = int(gz_box.quaternion.w)
        area_inter = 0
        area_dt = 0
        # detector stuff taking only single result
        # center x
        if len(dt_box.detections) !=0 :
            object_id = dt_box.detections[0].results[0].id
            score = dt_box.detections[0].results[0].score
                # if (object_id == 1):
            center_x_detector = dt_box.detections[0].bbox.center.x
            # center y
            center_y_detector = dt_box.detections[0].bbox.center.y
            # size x
            size_x_detector = dt_box.detections[0].bbox.size_x

            size_y_detector = dt_box.detections[0].bbox.size_y

            minx_dt = int(center_x_detector - size_x_detector/2)
            maxx_dt = int(center_x_detector + size_x_detector/2)
            miny_dt = int(center_y_detector - size_y_detector/2)
            maxy_dt = int(center_y_detector + size_y_detector/2)
            area_inter = float(max(0,(min(maxx_gz,maxx_dt)-max(minx_gz,minx_dt)))*max(0,(min(maxy_gz,maxy_dt)-max(miny_gz,miny_dt))))
            area_dt = float(size_y_detector*size_x_detector)
            print(minx_gz)
            print(minx_dt)
            print(miny_gz)
            print(miny_dt)
            print(maxx_gz)
            print(maxx_dt)
            print(maxy_gz)
            print(maxy_dt)

        else:
            overlap = -1
            object_id = -1
        area_gz = float((maxx_gz-minx_gz)*(maxy_gz-miny_gz))
        overlap = float(area_inter/area_gz)
        self.overlap_pub.publish(overlap)
        self.object_id_pub.publish(object_id)
        if ( object_id ==1):
            print("start")

            print("Common area:")
            print(area_inter)
            print("Area Gazebo:")
            print(area_gz)
            print("Area Detector:")
            print(area_dt)
            print("overlap:")
            print(overlap)
            print("end")
        else:
            print("#########fail#########")
            print(object_id)
            # else:
            #     print("##########################fail#####################################")


def main(args):

    rospy.init_node('validate', anonymous = True)
    val = validate()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting Down")

if __name__ == '__main__':
    main(sys.argv)
