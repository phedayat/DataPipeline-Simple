import queue
import threading
import json

class Pipeline:
	def __init__(self, num_workers=3):
		self.queues = dict()
		self.tasks = dict()
		self.num_workers = num_workers
		self.create_queues()

		# Would need if we had separate processes
		# self.workers = dict()

	# Expecting messages to be List[Dict[str, Any]]
	def start(self, messages):
		messages = list(map(json.loads, messages))
		batches = self.create_batches(messages)
		self.distributor(batches)

	def create_batches(self, messages, batch_size=10):
		batches = []
		while batch := messages[:batch_size]:
			batches.append(batch)
			messages = messages[batch_size:]
		return batches

	def create_queues(self):
		self.queues["OUTPUT"] = queue.Queue()
		for i in range(self.num_workers):
			self.queues[i+1] = queue.Queue()

	def distributor(self, batches):
		output_process = threading.Thread(target=self.output_worker, name="worker_output", daemon=True)
		self.tasks[output_process.name] = output_process

		while len(batches) > 0:
			batch = batches[:self.num_workers]
			batches = batches[self.num_workers:]

			for i in range(len(batch)):
				self.queues[i+1].put(batch[i])
				process = threading.Thread(target=self.worker, args=(i+1,), name=f"worker_{i}")
				self.tasks[process.name] = process
				self.tasks[process.name].start()
		self.tasks[output_process.name].start()
		self.tasks[output_process.name].join()

	def worker(self, queue_key):
		# Getting lists from the queues

		while not self.queues[queue_key].empty():
			messages = self.queues[queue_key].get()
			print(f"We have a message for queue {queue_key}!")
			for msg in messages:
				msg["special"] = "Message processed by a worker"
			self.queues["OUTPUT"].put(messages)
			self.queues[queue_key].task_done()

	def output_worker(self):
		with open("output.txt", "a") as f:
			while not self.queues["OUTPUT"].empty():
				messages = self.queues["OUTPUT"].get()
				for message in messages:
					f.write(f"{json.dumps(message, indent=4)}\n")
				print("OUTPUT")
				self.queues["OUTPUT"].task_done()

if __name__=="__main__":
	with open("../DataReader/data_reader_input.txt") as f:
		M = [i.strip() for i in f.readlines()]
		P = Pipeline(num_workers=2)
		P.start(M)