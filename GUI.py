import streamlit as st
import time
import requests
import json
from pandas import *
class objectview(object):
    def __init__(self, d):
        self.__dict__ = d

class SpaceVehicle():
    Mass = int()
    AngleBelowHorizontal = float()
    AngleOfAttack = float()
    Height = int()
    Radius = float()
    Velocity = float()
    TimeFrame = int()
    VehicleType = int()
    def __iter__(self):
        yield 'Mass', self.Mass
        yield 'AngleBelowHorizontal', self.AngleBelowHorizontal
        yield 'AngleOfAttack', self.AngleOfAttack
        yield 'Height', self.Height
        yield 'Radius', self.Radius
        yield 'Velocity', self.Velocity
        yield 'TimeFrame', self.TimeFrame
        yield 'VehicleType', self.VehicleType

def rnd(object):
    return str(round(object,2))

def convert(obj):
    arrDict = {}
    timeList = list()
    for key in obj[0]["vehicleState"]:
        arrDict[key] = list()
    for tf in obj:
        timeList.append(tf["timeElapsed"])
        for key in tf["vehicleState"]:
            arrDict[key].append(tf["vehicleState"][key])
    df = dict()
    df["time"] = timeList
    # Acceleraion df
    df["acc"] = DataFrame({
        "absAcc":arrDict["absoluteAcceleration"],
        "dccLoad":arrDict["decelerationLoad"]
    })

    # Angle df
    df["angle"] = DataFrame({
        "angBelowHor":arrDict["angleBelowHorizontal"],
        "angAttack":arrDict["angleOfAttack"],
    })

    # Temperature df
    df["temp"] = DataFrame({
        "curTemp":arrDict["currentTemperature"],
        "maxTemp":arrDict["maxTemperature"],
    })

    # Displacement df
    df["disp"] = DataFrame({
        "disp":arrDict["displacement"],
        "dispEarth":arrDict["displacementAroundEarth"],
    })

    # Drag df
    df["drag"] = DataFrame({
        "dragCoeff":arrDict["dragCoeff"],
        "liftToDrag":arrDict["liftToDrag"]
    })

    # Height df
    df["hgt"] = DataFrame({
        "height":arrDict["height"]
    })

    # Velocity df
    df["vec"] = DataFrame({
        "velocity":arrDict["velocity"]
    })
    df["nerdView"] = DataFrame({
        "time": timeList,
        "absAcc": arrDict["absoluteAcceleration"],
        "dccLoad": arrDict["decelerationLoad"],
        "angBelowHor": arrDict["angleBelowHorizontal"],
        "angAttack": arrDict["angleOfAttack"],
        "curTemp": arrDict["currentTemperature"],
        "maxTemp": arrDict["maxTemperature"],
        "disp": arrDict["displacement"],
        "dispEarth": arrDict["displacementAroundEarth"],
        "dragCoeff": arrDict["dragCoeff"],
        "liftToDrag": arrDict["liftToDrag"],
        "height": arrDict["height"],
        "velocity": arrDict["velocity"]
    })
    #st.write(df)
    detail = st.checkbox("Reload Details for Nerds")
    if detail:
        st.write(df["nerdView"])
    return objectview(df)

def sideBarInput():
    preset = st.sidebar.selectbox("Select you vehicle here", ("SpaceShuttle", "SpaceCraft"))
    shuttle = SpaceVehicle()
    shuttle.Velocity = st.sidebar.slider("InitialVelocity", 5000.0, 20000.0, 10000.0)
    shuttle.AngleOfAttack = st.sidebar.slider("AttackAngle", 0.0, 90.0, 40.0)
    shuttle.Height = st.sidebar.slider("StartingAlitude", 10000, 100000, 80000)
    shuttle.AngleBelowHorizontal = st.sidebar.slider("AngleBelowHorizontal",0.0,90.0,6.0)
    shuttle.Mass = st.sidebar.slider("Mass",50000,100000,78000)
    shuttle.Radius = st.sidebar.slider("Radius",5.0,10.0,6.0)
    shuttle.TimeFrame = st.sidebar.slider("TimeInterval",1,5,1)
    if preset == "SpaceShuttle": shuttle.VehicleType = 0
    else: shuttle.VehicleType = 1
    return shuttle

def autoSimulation(o):
    SimulationSpeed = st.slider("Select Simulation Speed", 1, 10, 1)
    spTimePmt = st.empty()
    spTfPmt = st.empty()
    spSpdPmt = st.empty()
    spSpeed = st.empty()
    spAccPmt = st.empty()
    spAccRefPmt = st.empty()
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
        spTimePmt.markdown("Current Time Elapsed **" + rnd(o.time[i])+"**")
        spTfPmt.markdown("Curent TimeFrame **" + str(i) + "**")

        spSpdPmt.markdown("The current velocity is **" + rnd(o.vec["velocity"][i])+"**")
        spSpeed.line_chart(o.vec[0:i], height=100)

        spAccPmt.markdown("Current Absolute Acceleration **" + rnd(o.acc["absAcc"][i]) + "**")
        spAcc.line_chart(o.acc[0:i], height=100)

        spAltPmt.markdown("Current Height **" + rnd(o.hgt["height"][i]) + "**")
        spAlt.area_chart(o.hgt[0:i], height=100)

        spDispPmt.markdown("Current Displacement is **" + rnd(o.disp["disp"][i]) + "**")
        spDispEarthPmt.markdown("Current Displacement around Earth **" + rnd(o.disp["dispEarth"][i]) + "**")
        spDisp.area_chart(o.disp[0:i], height=100)

        spTmpPmt.markdown("The current temp is **" + rnd(o.temp["curTemp"][i]) + "**")
        spGtmpPmt.markdown("The maximum temp is **" + rnd(o.temp["maxTemp"][i]) + "**")
        spTmp.area_chart(o.temp[0:i], height=100)

        spDragPmt.markdown("Current Drag Coefficient **" + rnd(o.drag["dragCoeff"][i]) + "**")
        spDragLiftPmt.markdown("Current Lift to Drag **" + rnd(o.drag["liftToDrag"][i]) + "**")
        spDrag.line_chart(o.drag[0:i], height=100)
        time.sleep(1.0 / SimulationSpeed)

def manualSimulation(o):
    i = st.slider("Current TimeFrame",0,len(o.time))
    st.markdown("**Please drag TimeFrame slider slowly**")
    st.markdown("Current Time Elapsed **" + rnd(o.time[i]) + "**")
    st.markdown("Curent TimeFrame **" + str(i) + "**")

    st.markdown("The current velocity is **" + rnd(o.vec["velocity"][i]) + "**")
    st.line_chart(o.vec[0:i], height=100)

    st.markdown("Current Absolute Acceleration **" + rnd(o.acc["absAcc"][i]) + "**")
    st.line_chart(o.acc[0:i], height=100)

    st.markdown("Current Height **" + rnd(o.hgt["height"][i]) + "**")
    st.area_chart(o.hgt[0:i], height=100)

    st.markdown("Current Displacement is **" + rnd(o.disp["disp"][i]) + "**")
    st.markdown("Current Displacement around Earth **" + rnd(o.disp["dispEarth"][i]) + "**")
    st.area_chart(o.disp[0:i], height=100)

    st.markdown("The current temp is **" + rnd(o.temp["curTemp"][i]) + "**")
    st.markdown("The maximum temp is **" + rnd(o.temp["maxTemp"][i]) + "**")
    st.area_chart(o.temp[0:i], height=100)

    st.markdown("Current Drag Coefficient **" + rnd(o.drag["dragCoeff"][i]) + "**")
    st.markdown("Current Lift to Drag **" + rnd(o.drag["liftToDrag"][i]) + "**")
    st.line_chart(o.drag[0:i], height=100)

@st.cache
def fetch(shuttle):
    url = "http://localhost:5000/run"
    res = None
    #with st.spinner("Performing Calculations   Please Wait"):
    print(json.dumps(dict(shuttle)))
    res = requests.post(url,json=dict(shuttle))
    return res.json()

def startApp():
    st.markdown("# Spacecraft Landing Simulator UI")
    aniType = st.sidebar.selectbox("Select Simulation Type", ("Select a method to begin", "Manual","Automated"))
    shuttle = sideBarInput()
    if aniType == "Select a method to begin":
        st.empty()
        st.markdown("""
        ## Instructions:
        Adjust the parameters of the simulation from the side bar \n
        Select the Simulation Type \n
        **Automated**:The simulation data will be updated real-time \n
        **Manual**: Manually adjust the current time \n 
        ---
        ## Development Team
        Follow the link below for Public Github Repositories\n
        German Nikolishin - [BackEnd Simulation API](https://github.com/SkymanOne/SpaceShuttleSimulator)\n
        Tony Zhang - [Frontend User Interface](https://github.com/N0ne1eft/SimulationInterface)\n
        Will Cliffe - Trojectory Research\n
        Mattie Lousada Blaazer - Ballisitic Coefficient Research
        """)
    elif aniType == "Automated":
        autoSimulation(convert(fetch(shuttle)))
    elif aniType == "Manual":
        manualSimulation(convert(fetch(shuttle)))

if __name__ == '__main__':
    startApp()