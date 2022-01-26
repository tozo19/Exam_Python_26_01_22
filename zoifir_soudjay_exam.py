import datetime
import time
import threading


stop_thread = False
gbal_fifo= []

################################################################################
#   Handle all connections and rights for the server
################################################################################
class my_task():

	name = None
	priority = -1
	period = -1
	execution_time = -1
	next_ready_time = -1
	state = "SLEEPING"


    	############################################################################
	def __init__(self, name, priority, period, execution_time,  fifo_write = False):

		self.name = name
		self.priority = priority
		self.period = period
		self.execution_time = execution_time
		self.next_ready_time = datetime.datetime.now()
		self.state = "READY"
		self.fifo_write = fifo_write
		
		threading.Thread.__init__(self)


    	############################################################################
	def update_state(self):
		
		if self.next_ready_time < datetime.datetime.now() :
			
			current_task.state = "READY"
	
		print("\t" + self.name + " : " + self.state + "\t(Deadline = " + self.next_ready_time.strftime("%H:%M:%S") + ", Priority = " + str(self.priority) + ")")


    	############################################################################
	def run(self):

		# Update execution_time
		self.next_ready_time  += datetime.timedelta(seconds=self.period)

		# Start task
					
		if (self.fifo_write == True) :
			
			global_fifo.append(self.name + " : reading message : " + datetime.datetime.now().strftime("%H:%M:%S"))
			
		else :
			while (len(global_fifo) > 0):
				print(self.name + " : " + global_fifo[0])
				del global_fifo[0]	



		# Stop task
		print("\t" + self.name + " : Ending (" + datetime.datetime.now().strftime("%H:%M:%S") + ")")
		
		self.state = "SLEEPING"


####################################################################################################
#
#
#
####################################################################################################
if __name__ == '__main__':


	# Instanciation of task objects
	task_list = []
	task_list.append(my_task(name="pump_1", priority = 2, period = 5, execution_time = 2, fifo_write=True))
	task_list.append(my_task(name="pump_2", priority = 2, period = 15, execution_time = 3,  fifo_write=True))
	task_list.append(my_task(name="machine_1", priority = 1, period = 5, execution_time = 5, fifo_write=True))
	task_list.append(my_task(name="machine_2", priority = 1, period = 5, execution_time = 3, fifo_write=True))        
	
	while(1):

		time_now = datetime.datetime.now()
		
		print("\nScheduler : " + time_now.strftime("%H:%M:%S"))


		# Update task state : SLEEPING => READY
		for current_task in task_list:
				
			current_task.update_state()



		# Search for task with higher priority
		task_to_run = None
		task_higher_priority = 0

		for current_task in task_list:
		
			if (current_task.state == "READY") & (current_task.priority > task_higher_priority) :
			
				task_higher_priority = current_task.priority
				task_to_run = current_task

		
		# Start task
		if task_to_run == None :
			time.sleep(5)
			
		else :
			task_to_run.run()


