# To add a new process, follow instructions :
# Copy/Paste/rename Process_template folder
# Go to Trunk/Core/Queue_Global.py and follow instructions
# Go to Trunk/main.py and follow instructions
# Rename Process name in StartThread function


from Queue import Queue
from threading import Thread
import time
import Core.Queue_Global as Queue_Global
from Core.QueueItem import QueueItem
from Core.actuator import *
import Core.database as database



def process(Queue):

	#poolLightConfig = database.databaseActuators.getHardwareConfigurationByName("Pool Light")
	#poolPumpConfig = database.databaseActuators.getHardwareConfigurationByName("Pool Pump")
	poolHeaterConfig = database.databaseActuators.getHardwareConfigurationByName("Pool Heater")

	#light = Light(poolLightConfig[0],poolLightConfig[2])
	#pump = Pump(poolPumpConfig[0],poolPumpConfig[2])
	light = Light(1,1)
	pump = Pump(5,2)
	heater = Heater(poolHeaterConfig[0],poolHeaterConfig[2])
	while True:
		Item = Queue.get()
		state = Item.state
		data = Item.data
		if state == "Init":
			print("Init State")


		elif state == "Start":
			print("Start State")	

		elif state == "Process":
			print("Process State")		
			Queue.enqueueIfEmpty(state, data, 1000)
			
		elif state == "Stop":
			print("Stop State")		

		elif state == "light":
			print("Light")
			if(data == "on"):
				light.set_value(True)		
			else:
				light.set_value(False)

		elif state == "pump":
			print("pump")
			if(data == "on"):
				pump.set_value(True)		
			else:
				pump.set_value(False)

		elif state == "heater":
			print("heater")
			if(data == "on"):
				heater.set_value(True)		
			else:
				heater.set_value(False)

		elif state == "Exit":
			del database.databaseActuators
			break
		else:
			print("Programmation error : This state is not implemented : "+state)

		Queue.task_done() # Indicate that a formerly enqueued task is complete


def StartThread():
	ThreadProcess = Thread(target=process, args=(Queue_Global.process_Actuators,))
	ThreadProcess.setDaemon(False)
	ThreadProcess.start()