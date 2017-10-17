import sys
import heapq
import queue
import copy
class Process(object):

    def __init__(self, proc_id, initial_arrival_time, cpu_burst_time,
                 num_bursts, io_time):
        self.proc_id = proc_id

        self.initial_arrival_time = int(initial_arrival_time)
        self.cur_arrive_time=copy.deepcopy(self.initial_arrival_time)
        self.cpu_burst_time = int(cpu_burst_time)
        self.cur_burst_time = copy.deepcopy(self.cpu_burst_time)
        self.left_num = int(num_bursts)
        self.num_bursts = int(num_bursts)
        self.io_time = int(io_time)

        self.algo=''
    def __lt__(self, other):
        if(self.algo=="FCFS" or self.algo=="RR"):
            return self.initial_arrival_time<other.initial_arrival_time
        elif(self.algo=="SRT"):
            return self.cur_burst_time<other.cur_burst_time


def FCFS(self,p_list):
    for i in range(len(p_list)):
        i.algo="FCFS"
    heapq.heapify(p_list)
    q = queue.Queue()
    a = "time 0ms: Simulator started for FCFS [Q <empty>]"
    stat=[]
    stat.append(a)
    time=0
    #print("time 0ms: Simulator started for FCFS [Q <empty>]\n")
    while i in range(2000):
        if p_list is not None:
            pro=p_list.pop()
            q.put(pro.proc_id)
            if(pro.num_bursts-1 is not 0):
                pro.num_bursts-=1
                time=pro.cpu_burst_time
                pro.cur_arrive_time+=time+pro.io_time
                heapq.heappush(p_list,pro)
        else:
            break


def SRT(self,p_list):
    for i in range(len(p_list)):
        i.algo="SRT"
    heapq.heapify(p_list)

def RR(self,p_list):
    for i in range(len(p_list)):
        i.algo="RR"
    heapq.heapify(p_list)
    q=queue.Queue()
    



if __name__ == "__main__":
    # Argument input error handling
    if len(sys.argv) < 3:
        sys.stderr.write("ERROR: Invalid arguments\n")
        sys.stderr.write("USAGE: ./main.py <input-file> <output-file>\n")
        sys.exit()

    # Read the input and output filename
    input_file_str = sys.argv[-2]
    output_file_str = sys.argv[-1]

    # Read the input file
    p_list = []
    f = open(input_file_str, "r")
    for line in f:
        # Skip comments
        if line[0] == "#":
            pass
        # Read each process
        else:
            process_info = line.split("|")
            if len(process_info) != 5:
                sys.stderr.write("ERROR: Invalid input file format\n")
                sys.exit()
            p_list.append(Process(process_info[0], process_info[1],
                                  process_info[2], process_info[3],
                                  process_info[4]))
    f.close()

    # Write simulation results to file
    fp = open(output_file_str, "w+")
    fp.close()