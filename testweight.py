import time
import sys
import serial
import RPi.GPIO as GPIO
#from scale import HX711 

referenceUnit = 1
#load cell setup
#hx = HX711(5, 6)
#hx.set_reading_format("LSB", "MSB")
#hx.set_reference_unit(referenceUnit)

#arduino setup
uno1 = serial.Serial("/dev/ttyACM1", baudrate = 9600)


#def Tare():
    #hx.reset()
    #hx.tare()
    #print("Tare done!")

#def getweight():
    #val = hx.read_average(5)
    #val = round((val)/736,1)
    #hx.power_down()
    #hx.power_up()
    #time.sleep(0.1)
    #return val

def dispense(motorSelection, target):
    proceed = False
    #turns = int(100)
    inpt = str(motorSelection) + "," + str(target) + "/n"

    if motorSelection == 1 or motorSelection == 2:
        uno1.write(inpt.encode())
        while proceed == False:
            if uno1.in_waiting > 0:
                answer = uno1.readline().decode('utf-8').rstrip()
                if answer == "complete":
                        proceed = True
    
    #currentWeight = getweight()
    #amtdispensed = currentWeight - ini
    #diff = target - amtdispensed
    #print(round(diff,1))
    #if diff > 0.5:
    #    dispense(motorSelection, diff, ini)
    #else:
    #    hx.power_down()
    return

#Tare()
dispense(1, 100)
#count = 0
#while True:
    #cur = hx.get_weight()
    #print(count, cur)
    #count += 1
    #time.sleep(1)
