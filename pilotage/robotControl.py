#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
script de controle du robot:
commande proportionnelle par rapport à l'erreur sur l'angle et la distance
"""
# from std_msgs.msg import Int64
# import rospy

# def callback(msg):
#   """
#   renvoie la commande en accélération du robot
#   """
#   value = msg.data
#   print(value)
#   return None

# rospy.init_node("")
# sub = rospy.Subscriber("/topic", Int64, callback)
# pub = rospy.Publisher("/topic", Int64)
# pub.publish(Int64(data=10))





# license removed for brevity
import rospy
from std_msgs.msg import String, Float64, Float64MultiArray
from math import atan2,pi





def orientation_roue_gauche(angle):
    pub = rospy.Publisher('/desherbor_ensta/joint_left_top_wheel/command', Float64, queue_size = 2)
    # rate = rospy.Rate(10)
    if not rospy.is_shutdown():
        rospy.sleep(0.1)
        pub.publish(Float64(data = angle))
        rospy.sleep(0.1)

def orientation_roue_droite(angle):
    pub = rospy.Publisher('/desherbor_ensta/joint_right_top_wheel/command', Float64, queue_size = 2)
    # rate = rospy.Rate(10)
    if not rospy.is_shutdown():
        rospy.sleep(0.1)
        pub.publish(Float64(data = angle))
        rospy.sleep(0.1)

def orientation_roues(angle):
    orientation_roue_gauche(angle)
    orientation_roue_droite(angle)


def change_wheel_speed(value):
    pub1 = rospy.Publisher('/desherbor_ensta/joint_left_bottom_wheel/command', Float64, queue_size = 1)
    pub2 = rospy.Publisher('/desherbor_ensta/joint_right_bottom_wheel/command', Float64, queue_size = 1)
    # rospy.init_node('commande')
    # rate = rospy.Rate(10)
    if not rospy.is_shutdown():
        rospy.sleep(0.1)
        pub1.publish(Float64(data = value))
        pub2.publish(Float64(data = value))


def movement_policy(position,destination):
    """
    publish l'angle et la vitesse pour aller de position vers destination
    """
    x,y = position
    u1,u2 = destination
    eps = 1 # seuil de tolérance en distance

    theta_hat_hat = get_angle(position,destination)
    orientation_roues(theta_hat)
    if (x-u1)**2 + (y-u2)**2 > eps: # si on est trop loin de l'herbe on avance
        change_wheel_speed(1)
    else:
        change_wheel_speed(0)


def commander_vitesse_roues(message, publishers):
    pub1, pub2 = publishers[0],publishers[1]
    r = message.data
    vitesse = 0.5*r + 0.3
    print(r)
    if r > 0.167:
        pub1.publish(Float64(data = 2*vitesse))
        pub2.publish(Float64(data = 2*vitesse))
    else:
        pub1.publish(Float64(data = 0))
        pub2.publish(Float64(data = 0))


def commander_angle_roues(message, publishers):
    pub1, pub2 = publishers[0],publishers[1]
    theta = -message.data/180*pi
    # theta = 0.2
    # print(theta)
    pub1.publish(Float64(data = theta))
    pub2.publish(Float64(data = theta))



if __name__ == '__main__':
    rospy.init_node('commande')
    pub_left_speed = rospy.Publisher('/desherbor_ensta/joint_left_bottom_wheel/command', Float64, queue_size = 1)
    pub_right_speed = rospy.Publisher('/desherbor_ensta/joint_right_bottom_wheel/command', Float64, queue_size = 1)
    pub_left_angle = rospy.Publisher('/desherbor_ensta/joint_left_top_wheel/command', Float64, queue_size = 1)
    pub_right_angle = rospy.Publisher('/desherbor_ensta/joint_right_top_wheel/command', Float64, queue_size = 1)
    rospy.Subscriber("/DISTANCE", Float64, commander_vitesse_roues, callback_args = [pub_left_speed,pub_right_speed])
    rospy.Subscriber("/ORIENTATION", Float64, commander_angle_roues, callback_args = [pub_left_angle,pub_right_angle])
    rospy.spin()


    # while(1):
    #     roulement_roue_gauche()
    #     avancer()
    # try:
    # except rospy.ROSInterruptException:
    #     pass


