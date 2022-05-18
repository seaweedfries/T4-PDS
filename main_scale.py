import time
import sys
import serial
import RPi.GPIO as GPIO
import streamlit as st 
from scale import HX711
from PIL import Image

st.set_page_config(layout='wide')
hide_streamlit_style = """
<style>
.css-vl8cle e8zbici2 {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""

#GPIO.setmode(GPIO.BCM)

#interface setup
st.image(image1)
st.image(image2)
notify = st.empty()
col1, col2 = st.columns(2)

col3, col4 = st.columns(2)


#button setup
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


#setup linear regression model for number of turns
import numpy as np
import pandas as pd
from sklearn import linear_model

df = pd.read_csv("CoffeeGrounds.csv")
x = df[["turn"]]
y = df[["weight"]]
regr = linear_model.LinearRegression()
regr.fit(y.values, x.values)

#load cell setup
referenceUnit = 737
hx = HX711(5,6)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(referenceUnit)

#arduino setup
uno1 = serial.Serial("/dev/ttyACM1", baudrate = 9600)
uno2 = serial.Serial("/dev/ttyACM1", baudrate = 9600)



#load cell functions
def Tare():
    hx.reset()
    hx.tare()
    print("Tare done!")

def getweight():
    val = hx.read_average(5)
    val = round((val)/736,1)
    hx.power_down()
    hx.power_up()
    time.sleep(0.1)
    return val

#arduino functions
def dispense(motorSelection, target, ini):
    proceed = False
    turns = int(regr.predict(np.array([[target]])))
    print('turns',turns)
    #turns = int(100)
    inpt = str(motorSelection) + "," + str(turns) + "/n"

    if motorSelection == 1 or motorSelection == 2:
        uno1.write(inpt.encode())
        while proceed == False:
            if uno1.in_waiting > 0:
                answer = uno1.readline().decode('utf-8').rstrip()
                if answer == "complete":
                        proceed = True
    if motorSelection == 3 or motorSelection == 4:
        uno2.write(inpt.encode())
        while proceed == False:
            if uno2.in_waiting > 0:
                answer = uno2.readline().decode('utf-8').rstrip()
                if answer == "complete":
                    proceed = True
    
    currentWeight = getweight()
    amtdispensed = currentWeight - ini
    diff = target - amtdispensed
    #print(round(diff,1))
    if diff > 0.5:
        dispense(motorSelection, diff, ini)
    else:
        return

#notification function
def msg(motors, motorvalues):
    with notify.empty():
        with st.spinner("Dispensing..."):
            for i in range(len(motors)):
                ini = getweight()
                dispense(motors[i], motorvalues[i], ini)
        st.success("Dispensing complete.")
        time.sleep(0.8)
    notify.empty()
    return

#speeddial buttons
def button_callback1(channel):
    ini = getweight()
    dispense(1, 2, ini)

def button_callback2(channel):
    ini = getweight()
    dispense(3, 2, ini)

def button_callback3(channel):
    ini = getweight()
    dispense(1, 2, ini)
    ini = getweight()
    dispense(3, 1, ini)

def button_callback4(channel):
    ini = getweight()
    dispense(3, 1, ini)
    ini = getweight()
    dispense(1, 1, ini)

with col1:
    st.subheader("Slim Spell")
    st.info('2g Cassia Seeds, 3g Roselle Flowers, 6g Hawthorn Fruit')
    if st.button('Dispense1'):
        msg([1], [2])

with col2:
    st.subheader("Murrier Murrier")
    st.info('1g Cassia Seeds, 2g Roselle Flowers, 3g Hawthorn Fruit')
    if st.button('Dispense2'):
        msg([3], [2])
        
with col3:
    st.subheader("Sleeping Beauty")
    st.info('4g Cassia Seeds, 3g Roselle Flowers, 1g Hawthorn Fruit')
    if st.button('Dispense3'):
        msg([1,3], [3,2])

with col4:
    st.subheader("Fair Lady")
    st.info('1g Cassia Seeds, 2g Roselle Flowers, 6g Hawthorn Fruit')
    if st.button('Dispense4'):
        msg([3,1], [2,1])    
    
with st.expander("Custom Recipe"):
    with st.form('custom'):
        motorselect = st.selectbox('Select motor', ([1,2,3,4]))
        weightval = st.slider('Target Weight', 0, 20, 1)

        submit = st.form_submit_button('Submit')
        if submit:
            st.write('Motor Selected:', motorselect, 'Weight Selected', weightval)
            msg([motorselect], [weightval])

placeholder = st.empty()
if placeholder.button('hide'):
    GPIO.add_event_detect(18, GPIO.RISING, callback=button_callback1, bouncetime = 1000)
    GPIO.add_event_detect(22, GPIO.RISING, callback=button_callback2, bouncetime = 1000)
    GPIO.add_event_detect(27, GPIO.RISING, callback=button_callback3, bouncetime = 1000)
    GPIO.add_event_detect(17, GPIO.RISING, callback=button_callback4, bouncetime = 1000)
    Tare()
    placeholder.empty()
