#!/usr/bin/python3

import math

def go_to_goal(goal,pose,vmax,Kw,Ka):
    dp = [goal[0]-pose[0],goal[1]-pose[1]]
    e = math.atan2(dp[1],dp[0])-pose[2]
    w = Kw*math.atan2(math.sin(e),math.cos(e))
    v = vmax*(1-math.exp(-(dp[0]**2+dp[1]**2)/Ka))
    return v,w
            