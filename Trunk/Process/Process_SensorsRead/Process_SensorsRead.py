# To add a new process, follow instructions :
# Copy/Paste/rename Process_template folder
# Go to Trunk/Core/Queue_Global.py and follow instructions
# Go to Trunk/main.py and follow instructions
# Rename Process name in StartThread function


from Queue import Queue
from threading import Thread

import Core.Queue_Global as Queue_Global
from Core.QueueItem import QueueItem
import Core.database as database
from Core.sensor import *

def process(Queue):

	while True:
		Item = Queue.get()
		state = Item.state
		data = Item.data
		if state == "Init":
			
			poolThermocoupleConfig = database.databaseSensorsRead.getHardwareConfigurationByName("Pool Temperature Sensor")			
			pumpAmpereMeterConfig = database.databaseSensorsRead.getHardwareConfigurationByName("Pump Ampere Meter")
			poolPhConfig = database.databaseSensorsRead.getHardwareConfigurationByName("Pool Ph Meter")			
			poolThermocouple = Thermocouple(poolThermocoupleConfig[0],poolThermocoupleConfig[2], 4.14)
			pumpAmpereMeter = AmpereMeter(pumpAmpereMeterConfig[0],pumpAmpereMeterConfig[2], 4.14)
			poolPhMeter = PhMeter(poolPhConfig[0],poolPhConfig[2], 4.14)


		elif state == "Start":
			print("Start State")	

		elif state == "Process":
			thermocoupleValue = poolThermocouple.get_value()
			ampereMeterValue = pumpAmpereMeter.get_value()
			poolPhMeterValue = poolPhMeter.get_value()
			#print(ampereMeterValue)		
			#database.databaseSensorsRead.insertMeasure(1, thermocoupleValue)
			Queue.enqueueIfEmpty(state, data, 1000)
			
		elif state == "Stop":
			print("Stop State")		

		elif state == "Exit":
			del poolThermocouple
			del pumpAmpereMeter
			del poolPhMeter
			del database.databaseSensorsRead
			break
		else:
			print("Programmation error : This state is not implemented : "+state)

		Queue.task_done() # Indicate that a formerly enqueued task is complete


def StartThread():
	ThreadProcess = Thread(target=process, args=(Queue_Global.process_SensorsRead,))
	ThreadProcess.setDaemon(False)
	ThreadProcess.start()