import streamlit as st
import time
from convert import *
import requests

class objectview(object):
    def __init__(self, d):
        self.__dict__ = d

class SpaceVehicle():
    Velocity = float()
    Height = float()
    Mass = int()
    CurrentTemperature = float()
    Radius = float()
    AngleOfAttack = float()

def rnd(object):
    return str(round(object,2))

def convert(obj):
    df = {}
    arrDict = {}
    df["time"] = list()
    for key in obj[0]["vehicleState"]:
        arrDict[key] = list()
    for tf in obj:
        df["time"].append(tf["TimeElapsed"])
        for key in tf:
            arrDict[key].append(tf[key])


    # Acceleraion df
    df["acc"] = DataFrame({
        "absAcc":arrDict["AbsoluteAcceleration"],
        "dccLoad":arrDict["DecelerationLoad"]
    })

    # Angle df
    df["angle"] = DataFrame({
        "angBelowHor":arrDict["AngleBelowHorizontal"],
        "angAttack":arrDict["AngleOfAttack"],
    })

    # Temperature df
    df["temp"] = DataFrame({
        "curTemp":arrDict["CurrentTemperature"],
        "maxTemp":arrDict["MaxTemperature"],
    })

    # Displacement df
    df["disp"] = DataFrame({
        "disp":arrDict["Displacement"],
        "dispEarth":arrDict["DisplacementAroundEarth"],
    })

    # Drag df
    df["drag"] = DataFrame({
        "dragCoeff":arrDict["DragCoeff"],
        "liftToDrag":arrDict["LiftToGrag"]
    })

    # Height df
    df["hgt"] = DataFrame({
        "height":arrDict["Height"]
    })

    # Velocity df
    df["vec"] = DataFrame({
        "velocity":arrDict["Velocity"]
    })

    return objectview(df)

def sideBarInput():
    preset = st.sidebar.selectbox("Select you preset here", ("Rocket", "SpaceCraft"))
    shuttle = SpaceVehicle()
    shuttle.Velocity = st.sidebar.slider("InitialVelocity", 0.0, 3000.0, 500.0)
    shuttle.AngleOfAttack = st.sidebar.slider("InitialAngle(Vertical)", 0.0, 90.0, 45.0)
    shuttle.Height = st.sidebar.slider("StartingAlitude", 0.0, 100000.0, 50000.0)
    shuttle.CurrentTemperature = st.sidebar.slider("Temperature",0.0,3000.0,200.0)
    shuttle.Mass = st.sidebar.slider("Mass",500,10000,2000)
    shuttle.Radius = st.sidebar.slider("Radius",1.0,10.0,2.0)
    return shuttle

def autoSimulation(o):
    SimulationSpeed = st.slider("Select Simulation Speed", 1, 10, 1)
    # Reserve Space for automated tf incrementation
    spTimePmt = st.empty()
    spTfPmt = st.empty()

    spSpdPmt = st.empty()
    spSpeed = st.empty()
    spAccPmt = st.empty()
    spAccRefPmt = st.empty
    spAcc = st.empty()
    spAltPmt = st.empty()
    spAlt = st.empty()
    spDispPmt = st.empty()
    spDispEarthPmt = st.empty()
    spDisp = st.empty()
    spTmpPmt = st.empty()
    spGtmpPmt = st.empty()
    spTmp = st.empty()
    spDragPmt = st.empty()
    spDragLiftPmt = st.empty()
    spDrag = st.empty()
    for i in range(0, len(o.time)):
        spTimePmt.markdown("Current Time Elapsed **" + rnd(o.time[i]))
        spTfPmt.markdown("Curent TimeFrame **" + str(i) + "**")

        spSpdPmt.markdown("The current velocity is **" + rnd(o.vec["velocity"][i]))
        # spSpdPmt.markdown("The current velocity is **"+str(round(g["spd"]["Speed"][tf],4))+" H="+str(round(g["spd"]["HSpeed"][tf],4))+" V="+str(round(g["spd"]["VSpeed"][tf],4))+"**")
        spSpeed.line_chart(o.vec[0:i], height=100)

        spAccPmt.markdown("Current Absolute Acceleration **" + rnd(o.acc["absAcc"][i]) + "**")
        spAccRefPmt.markdown("The orange line indicates the theoretical maximum acceleration human can withstand")
        spAcc.line_chart(o.acc[0:i], height=100)

        spAltPmt.markdown("Current Height **" + rnd(o.hgt["Height"][i]) + "**")
        spAlt.area_chart(o.hgt[0:i], height=100)

        spDispPmt.markdown("Current Displacement is **" + rnd(o.disp["disp"][i]) + "**")
        spDispEarthPmt.markdown("Current Displacement around Earth **" + rnd(o.disp["dispEarth"][i]) + "**")
        spDisp.area_chart(o.disp[0:i], height=100)

        spTmpPmt.markdown("The current temp is **" + rnd(o.temp["curTemp"][i]) + "**")
        spGtmpPmt.markdown("The maximum temp is **" + rnd(o.temp["maxtemp"][i]) + "**")
        spTmp.area_chart(o.temp[0:i], height=100)

        spDragPmt.markdown("Current Drag Coefficient **" + rnd(o.drag["dragCoeff"][i]) + "**")
        spDragLiftPmt.markdown("Current Lift to Drag **" + rnd(o.drag["liftToDrag"][i]) + "**")
        spDrag.line_chart(o.drag[0:i], height=100)
        time.sleep(1.0 / SimulationSpeed)

def manualSimulation(o):
    i = st.slider("Current TimeFrame",0,len(o.time))
    st.markdown("Current Time Elapsed **" + rnd(o.time[i]))
    st.markdown("Curent TimeFrame **" + str(i) + "**")

    st.markdown("The current velocity is **" + rnd(o.vec["velocity"][i]))
    # spSpdPmt.markdown("The current velocity is **"+str(round(g["spd"]["Speed"][tf],4))+" H="+str(round(g["spd"]["HSpeed"][tf],4))+" V="+str(round(g["spd"]["VSpeed"][tf],4))+"**")
    st.line_chart(o.vec[0:i], height=100)

    st.markdown("Current Absolute Acceleration **" + rnd(o.acc["absAcc"][i]) + "**")
    st.markdown("The orange line indicates the theoretical maximum acceleration human can withstand")
    st.line_chart(o.acc[0:i], height=100)

    st.markdown("Current Height **" + rnd(o.hgt["Height"][i]) + "**")
    st.area_chart(o.hgt[0:i], height=100)

    st.markdown("Current Displacement is **" + rnd(o.disp["disp"][i]) + "**")
    st.markdown("Current Displacement around Earth **" + rnd(o.disp["dispEarth"][i]) + "**")
    st.area_chart(o.disp[0:i], height=100)

    st.markdown("The current temp is **" + rnd(o.temp["curTemp"][i]) + "**")
    st.markdown("The maximum temp is **" + rnd(o.temp["maxtemp"][i]) + "**")
    st.area_chart(o.temp[0:i], height=100)

    st.markdown("Current Drag Coefficient **" + rnd(o.drag["dragCoeff"][i]) + "**")
    st.markdown("Current Lift to Drag **" + rnd(o.drag["liftToDrag"][i]) + "**")
    st.line_chart(o.drag[0:i], height=100)

@st.cache
def fetch(shuttle):
    url = "http://localhost:6000"
    res = None
    with st.spinner("Performing Calculations   Please Wait"):
        res = requests.post(url,data=dict(shuttle))
    return res

def mainView():
    shuttle = sideBarInput()
    st.markdown("# Spacecraft Landing Simulator UI")
    st.markdown("**THIS IS A WIP (WORK IN PROGRESS) DEMO INTENDED FOR TESTING, ALL THE DATA ARE RANDOMLY GENERATED**")
    aniType = st.selectbox("Select Simulation Type", ("Select a method to begin", "Automated", "Manual"))
    if aniType == "Automated":
        autoSimulation(convert(fetch(shuttle)))
    elif aniType == "Manual":
        fetch(shuttle)
        manualSimulation(convert(fetch(shuttle)))
        pass

    st.markdown("---")
    st.markdown("### GitHub Repositories")
    st.markdown("[This Web Interface](https://github.com/N0ne1eft/SimulationInterface) **(WIP Random Data)**")
    st.markdown("[Backend Repo](https://github.com/SkymanOne/SpaceShuttleSimulator) **(WIP not intergrated yet)**")

mainView()