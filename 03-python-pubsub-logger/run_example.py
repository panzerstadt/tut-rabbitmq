import os
from multiprocessing import Process
import multiprocessing
import time
import sys
import psutil

# https://stackoverflow.com/questions/17856928/how-to-terminate-process-from-python-using-pid


def cleanup():
    for process in psutil.process_iter():
        # use dir(process) to navigate
        try:
            pid = process.pid
            status = process.status()
            name = process.name()
            cmdline = process.cmdline()

            if name == "Python":
                print("\nPython Process: Status: ", status)
                print(cmdline[-1])
                if "consumer.py" in cmdline[-1]:
                    print("DELETING...")
                    process.kill()

                # print(dir(process))
            elif name == "sh":
                print("\nShell Process: Status: ", status)
                print(cmdline[-1])
                if "consumer_logs" in cmdline[-1]:
                    print("DELETING...")
                    process.kill()

        except:
            continue
            # print(" [WARNING] Zombie process", process)

        # if process.cmdline() == ['python', 'StripCore.py']:
        #     print('Process found. Terminating it.')
        #     process.terminate()
        #     break


dirpath = os.getcwd()
consumer_process = dirpath + "/consumer.py"
producer_process = dirpath + "/producer.py"

consumer_output_path = dirpath + "/consumer_logs"
producer_output_path = dirpath + "/producer_logs"


def script1():
    p = multiprocessing.current_process()
    print('Starting:', p.name, p.pid)
    os.system("python3 " + consumer_process)


def script2():
    p = multiprocessing.current_process()
    print('Starting:', p.name, p.pid)
    os.system("python3 " + producer_process)
    print('Exiting:', p.name, p.pid)


if __name__ == '__main__':
    print("this test requires your RabbitMQ broker to be running, on port 5673 (default is 5672")

    print("\nCleaning up previous processes:")
    cleanup()

    print("\nRunning Example:")
    c = Process(name="consumer", target=script1)
    c.daemon = True
    p = Process(name="producer", target=script2)
    p.daemon = False
    c.start()
    p.start()
    p.join()
    time.sleep(10)

    cleanup()


# manual check for processes we forgot to kill: `ps -ef | grep "python"`

# oops! if you forgot to terminate your consumer process (because it's a daemon), check these
# https://makandracards.com/makandra/16881-help-me-there-is-a-zombie-process
# https://stackoverflow.com/questions/17407263/kill-process-by-ppid-in-python
