import streamlit as st
import requests
from random import *
import pandas as pd
import math
import time
from Gen import *

st.markdown("# Spacecraft Landing Simulator UI")
st.markdown("**THIS IS A WIP (WORK IN PROGRESS) DEMO INTENDED FOR TESTING, ALL THE DATA ARE RANDOMLY GENERATED**")
preset = st.sidebar.selectbox("Select you preset here",("Rocket","SpaceCraft"))

initialVelocity = st.sidebar.slider("InitialVelocity",0.0,3000.0,500.0)
initialAngle = st.sidebar.slider("InitialAngle(Vertical)",0.0,90.0,45.0)
startingAlt = st.sidebar.slider("StartingAlitude",0.0,100000.0,50000.0)

custom = st.sidebar.checkbox("I want to customize advanced varibles")
#### Default
groundTemp = 20.0
if custom:
    groundTemp = st.sidebar.slider("GroundTemperature",-30,40,20)
    BallisticCoefficient = st.sidebar.slider("Ballistic Coefficient",1.0,2.0,1.5)
    noseRad = st.sidebar.slider("NoseConeRadius",0.1,10.0,5.0)

n = st.sidebar.slider("TFCount",1,100,100)

@st.cache(persist=True)
def fetchRandom():
    g=gen(n,initialVelocity,initialAngle,startingAlt,groundTemp)
    return {
        "tmp": pd.DataFrame({"temp":g["temp"],"gtemp":g["gtemp"]}),
        "spd": pd.DataFrame({"Speed":g["speed"],"VSpeed":g["vspeed"],"HSpeed":g["hspeed"]}),
        "acc": pd.DataFrame({"Acc":g["acc"],"AccRef":g["accRef"]}),
        "alt": g["alt"]
    }
g = fetchRandom()

tf=0

aniType = st.selectbox("Select Simulation Type",("Select a method to begin","Automated","Manual"))

if aniType=="Automated":
    SimulationSpeed = st.slider("Select Simulation Speed",1,10,1)
    # Reserve Space for automated tf incrementation
    spTfPmt = st.empty()
    spSpdPmt = st.empty()
    spSpeed = st.empty()
    spAccPmt = st.empty()
    spAccRefPmt = st.empty()
    spAcc = st.empty()
    spAltPmt = st.empty()
    spAlt = st.empty()
    spTmpPmt = st.empty()
    spGtmpPmt = st.empty()
    spTmp = st.empty()

    for i in range(0,n):
        tf+=1
        spTfPmt.markdown("Curent TimeFrame **"+str(tf)+"**")
        #spSpdPmt.markdown("The current speed is **"+str(round(speed[tf],4))+" H="+str(round(spd["HSpeed"][tf],4))+" V="+str(round(spd["VSpeed"][tf],4))+"**")
        spSpeed.line_chart(g["spd"][0:tf], height=100)

        #spAccPmt.markdown("Current Acceleration **"+str(round(g["acc"][tf],4))+"**")
        #spAccRefPmt.markdown("The orange line indicates the theoretical maximum acceleration human can withstand")
        spAcc.line_chart(g["acc"][0:tf],height=100)

        #spAltPmt.markdown("The current alt is **"+str(round(alt[tf],4))+"**")
        spAlt.area_chart(g["alt"][0:tf],height=100)

        #spTmpPmt.markdown("The current temp is **"+str(temp[tf])+"**")
        #spGtmpPmt.markdown("The current ground temp is **"+str(round(gtemp[tf],3))+"**")
        spTmp.area_chart(g["alt"][0:tf],height=100)
        time.sleep(1.0/SimulationSpeed)

# if aniType=="Manual":
#     tf = st.slider("Current TimeStamp",0,n)
#     st.write("Current TimeFrame ",tf)
#     st.write("Current Speed ",round(speed[tf],4))
#     st.line_chart(spd[0:tf], height=100)
#
#     st.write("Current Acceleration ",round(g["acc"][tf],4))
#     st.line_chart(acc[0:tf],height=100)
#
#     st.write("Current Alt ",round(alt[tf],4))
#     st.area_chart(alt[0:tf],height=100)
#
#     st.write("Current Temp ",temp[tf])
#     st.write("Current Ground Temp ",round(gtemp[tf],3))
#     st.area_chart(df[0:tf],height=100)

st.write("https://github.com/N0ne1eft")