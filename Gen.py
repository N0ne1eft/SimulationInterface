import math
from random import *

def gen(n,initialVelocity,initialAngle,startingAlt,groundTemp):
    initvspeed = initialVelocity*math.sin(initialAngle*math.pi/180)
    if initvspeed<0:
        initvspeed*=-1
    inithspeed = initialVelocity*math.cos(initialAngle*math.pi/180)
    if inithspeed<0:
        inithspeed*=-1
    initalt = startingAlt
    inittemp = 100
    initgtemp = groundTemp
    accMaxRef = 12.0
    dv = 0.0
    dh = 0.0
    acc = []
    accRef = []
    vspeed = []
    hspeed = []
    speed = []
    alt = []
    temp = []
    gtemp = []

    for i in range(n+1):
        dv = uniform(-2.0,0)
        initvspeed += dv
        vspeed.append(initvspeed)
        dh = uniform(-3.0,0)
        inithspeed += dh
        hspeed.append(inithspeed)
        speed.append(math.sqrt(initvspeed**2+inithspeed**2))
        acc.append(math.sqrt(dv**2+dh**2))
        accRef.append(accMaxRef)
        initalt -= uniform(0, int(30000 / n))
        alt.append(initalt)
        inittemp += randint(0, 5)
        temp.append(inittemp)
        initgtemp += uniform(-1,1)
        gtemp.append(initgtemp)
    return (
        {
            "acc":acc,
            "hspeed":hspeed,
            "vspeed":vspeed,
            "speed":speed,
            "alt":alt,
            "temp":temp,
            "gtemp":gtemp,
            "accRef":accRef
        }
    )