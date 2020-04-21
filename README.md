# how to start an examples

terminal 1 - the queue
```
cd mq-docker && docker-compose up
```

terminal 2 (or more if you want multiple workers) - the workers (consumers)
```
cd 02-python && python3 worker.py
```

terminal 3 - the senders (publishers)
```
cd 02-python && python3 new_task.py
```

browser
```
go to localhost:15673 with login and pw as 'guest'
```

the queue and messages are currently set as 'durable', meaning they will persist across restarts.

