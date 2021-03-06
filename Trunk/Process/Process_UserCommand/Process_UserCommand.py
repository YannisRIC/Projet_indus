# To add a new process, follow instructions :
# Copy/Paste/rename Process_template folder
# rename Process_Template.py
# Go to Trunk/Core/Queue_Global.py and follow instructions
# Go to Trunk/main.py and follow instructions
# Rename Process name in StartThread function (Queue_Global.YOUR_NEW_PROCESS)


from Queue import Queue
from threading import Thread

import Core.Queue_Global as Queue_Global
from Core.QueueItem import QueueItem

import Core.database as database

def process(Queue):

	while True:
		Item = Queue.get()
		state = Item.state
		data = Item.data
		if state == "Init":
			print("Init State")

		elif state == "Start":
			print("Start State")	

		elif state == "Process":
			userCommand = database.databaseUserCommand.getUserCommand()

			for row in userCommand :

				command(row[1], row[2], row[3])
				database.databaseUserCommand.userCommandDone(row[0])

			Queue.enqueueIfEmpty(state, data, 1000)

		elif state == "Stop":
			print("Stop State")		

		elif state == "Exit":
			del database.databaseUserCommand
			break
		else:
			print("Programmation error : This state is not implemented : "+state)

		Queue.task_done() # Indicate that a formerly enqueued task is complete


def StartThread():
	ThreadProcess = Thread(target=process, args=(Queue_Global.process_UserCommand,))
	ThreadProcess.setDaemon(False)
	ThreadProcess.start()

def command(command, targetName, value):
	if(command == 'Set'):
		#print command + " " + targetName + " " + value
		Queue_Global.process_Actuators.enqueue(targetName, value)
	elif(command == 'Update'):
		print command + " " + targetName + " " + value
	else:
		print('Database Error')
