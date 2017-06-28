from kafka import KafkaClient,KafkaProducer
import threading
import pandas as pd
import datetime
import numpy as np
import csv
import random
import time
import calendar
import sys

class myThread (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
   def run(self):
      print "Starting " + self.name
      print_message(self.name, self.counter)
      print "Exiting " + self.name

def print_message(Stock,price):
	#print("sending messages")
	x = float(price)
	a = datetime.datetime(2016,1,1,00,00,00)
	y = np.arange(1000000)
	delta  = np.random.uniform(-0.00001,0.00001, size = (1000000))
	choice = ['a','b','c']#,'d']
	
	producer = KafkaProducer(bootstrap_servers = 'localhost:9092')

	for i in range (0,len(y)):
		z = 0.0000001 * y[i] +0.00001 + delta[i]
		sign = random.choice(choice)
		if sign =='a':
			x = x+z
		elif sign == 'b':
			x = x + (z/2)
		elif sign == 'c':
			x = x -z
		else:
			x = x - (z/2)
		ticker = Stock
		a = a+datetime.timedelta(seconds = 1)
		seq = ticker+","+str(x)+","+str(a)
		
		producer.send("test",key = ticker,value = seq)

		time.sleep(1)

threads = []
f = 0
file =  open('companylist.csv','r')
for i in file:
	f = f+1
        for line in csv.reader([i], skipinitialspace=True):
            print(line[0],line[2])
            if line[2] == 'n/a':
                a = str(13.29)
            else:
                a = line[2]
		t = myThread(f,line[0],a)
		#globals()['thread%s' % line[0] = threading.Thread(target=print_message, args=(line[0],a))
		t.start()
		threads.append(t)
file.close()
#t = threading.Thread(target=print_message, args=('AAPL',128))
#t2 = threading.Thread(target=print_message, args=('GOOG',276))

#t = threading.Timer(5,print_message, args=('AAPL',128))
#t2 = threading.Timer(5,print_message, args=('GOOG',276))
  
#t.start()
#t2.start()
while True:
	pass
