import sys
import heapq
import queue
import copy
class Process(object):

    def __init__(self, proc_id, initial_arrival_time, cpu_burst_time,
                 num_bursts, io_time):
        self.proc_id = proc_id
        self.arrival_time=int(initial_arrival_time)
        self.initial_arrival_time = int(initial_arrival_time)
        self.cur_arrive_time=copy.deepcopy(self.initial_arrival_time)
        self.cpu_burst_time = int(cpu_burst_time)
        self.last_burst_time = 0
        self.cur_burst_time = 0
        self.left_num = int(num_bursts)
        self.num_bursts = int(num_bursts)
        self.io_time = int(io_time)
        self.sch_burst_time = 0
        self.wait_t=0
        self.end_t=-1
        self.prempt_num=0
        self.last_burst_time=0
        self.algo=''
    def __lt__(self, other):
        if(self.algo=="FCFS" or self.algo=="RR"):
            if self.arrival_time<other.arrival_time:
                return True
            elif self.arrival_time==other.arrival_time:
                return self.proc_id<other.proc_id
            else:
                return False
        elif(self.algo=="SRT"):
            if self.cpu_burst_time-self.cur_burst_time<other.cpu_burst_time-other.cur_burst_time:
                return True
            elif self.cpu_burst_time-self.cur_burst_time==other.cpu_burst_time-other.cur_burst_time:
                return self.proc_id < other.proc_id
            else:
                return False

def printq(proc):
    if len(proc) == 0:
        return "[Q <empty>]"
    else:
        s = "[Q"
        for i in proc:
            s += " " + str(i.proc_id)
        s += "]"
    return s

def FCFS(p_list):

    F_proc=copy.deepcopy(p_list)
    for i in F_proc:
        i.algo="FCFS"
    heapq.heapify(F_proc)
    ready = []
    t=0
    t_cs=8
    num_cs=0
    proc=[None]
    ended=[]
    block=[]
    print( "time %dms: Simulator started for FCFS %s" % (t,  printq(ready)))
    time_schedule=[]
    for i in F_proc:
        if(i.initial_arrival_time not in time_schedule):
            heapq.heappush(time_schedule,i.initial_arrival_time)
    if(0 in time_schedule):
        time_schedule.pop(0)
    context_switch=-1

    while True:

        if context_switch == t:
            context_switch = -1
            num_cs += 1
            if proc[0] is not None:
                if (t + proc[0].sch_burst_time) not in time_schedule:
                    heapq.heappush(time_schedule,t + proc[0].sch_burst_time)
                proc[0].sch_burst_time = 0
                print( "time %dms: Process %s started using the CPU %s" \
                    % (t, proc[0].proc_id, printq(ready)))

        # =
        # Handle the process that finishes the current burst
        if proc[0] is not None and \
                proc[0].cur_burst_time == proc[0].cpu_burst_time:
            proc[0].left_num -= 1
            # Terminated the process after all cpu burst
            if proc[0].left_num == 0:
                proc[0].end_t = t
                ended.append(proc[0])
                print( "time %dms: Process %s terminated %s" % (t, proc[0].proc_id,
                    printq(ready)))
            # If more to go, add to IO block
            else:
                print( "time %dms: Process %s completed a CPU burst; %d burst to go" \
                    " %s" % (t, proc[0].proc_id, proc[0].left_num, printq(ready)))

                end_t = t + proc[0].io_time+t_cs/2
                proc[0].arrival_time = end_t
                proc[0].cur_burst_time = 0
                proc[0].last_burst_time = 0
                block.append(proc[0])
                block.sort()
                if end_t not in time_schedule:
                    heapq.heappush(time_schedule,end_t)
                print( "time %dms: Process %s switching out of CPU; will blocked on I/O until time %dms" \
                    " %s" % (t, proc[0].proc_id, end_t, printq(ready)))
            # Reset current process
            proc[0] = None
            # Start context switch
            context_switch = t + t_cs/2
            if context_switch not in time_schedule:
                heapq.heappush(time_schedule,context_switch)

        # =
        # Add processes to the queue for there initial arrive
        for i in range(len(F_proc)):
            if F_proc[0].initial_arrival_time == t:
                temp = F_proc.pop(0)
                ready.append(temp)
                print( "time %dms: Process %s arrived and added to ready queue %s" % (t, temp.proc_id,printq(ready)))
            else:
                break
        # Add processes to the queue after IO block
        for i in range(len(block)):
            if block[0].arrival_time == t:
                temp = block.pop(0)
                ready.append(temp)
                print( "time %dms: Process %s completed I/O %s" % (t, temp.proc_id,
                    printq(ready)))
            else:
                break
        oldp=copy.deepcopy(proc[0])

        if context_switch == -1:
            if proc[0] is None and len(ready) != 0:
                proc[0] = ready.pop(0)
                proc[0].sch_burst_time = proc[0].cpu_burst_time-proc[0].cur_burst_time
            # Do context switch if current process changed
            if proc[0] is None:
                pass
            elif proc[0] is not None and oldp is None:
                context_switch = t + t_cs / 2
                if context_switch not in time_schedule:
                    heapq.heappush(time_schedule, context_switch)
            elif proc[0].proc_id != oldp.proc_id:
                context_switch = t + t_cs/2
                if context_switch not in time_schedule:
                    heapq.heappush(time_schedule,context_switch)
            # Add the new scheduled burst time
            elif proc[0] is not None and proc[0].sch_burst_time != 0:
                if (t+proc[0].sch_burst_time) not in time_schedule:
                    heapq.heappush(time_schedule,t+proc[0].sch_burst_time)
                proc[0].sch_burst_time = 0

        if len(time_schedule)==0:
            break
        time_schedule.sort()
        dif_t = time_schedule.pop(0) - t
        for i in range(len(ready)):
            # Fix the wait time difference for context switch
            # WARNING: This might cause the individual wait time wrong
            if i == 0 and context_switch != -1 and proc[0] is None:
                pass
            else:
                ready[i].wait_t += dif_t

        if context_switch == -1 and proc[0] is not None:
            proc[0].cur_burst_time += dif_t

        t += dif_t
    print("time %dms: Simulator ended for FCFS" % (t))

def SRT(self,p_list):
    for i in range(len(p_list)):
        i.algo="SRT"
    heapq.heapify(p_list)

def RR(p_list):
    R_proc=copy.deepcopy(p_list)
    for i in R_proc:
        i.algo="RR"
    heapq.heapify(R_proc)
    ready = []
    t = 0
    t_cs = 8
    t_slice=70
    num_cs = 0
    proc = [None]
    ended = []
    block = []
    print("time %dms: Simulator started for RR %s" % (t, printq(ready)))
    time_schedule = []
    for i in R_proc:
        if (i.initial_arrival_time not in time_schedule):
            heapq.heappush(time_schedule, i.initial_arrival_time)
    if (0 in time_schedule):
        time_schedule.pop(0)
    context_switch = -1

    while True:

        if context_switch == t:
            context_switch = -1
            num_cs += 1
            if proc[0] is not None:
                if (t + proc[0].sch_burst_time) not in time_schedule:
                    heapq.heappush(time_schedule, t + proc[0].sch_burst_time)
                proc[0].sch_burst_time = 0
                print("time %dms: Process %s started using the CPU %s" \
                      % (t, proc[0].proc_id, printq(ready)))

        # =
        # Handle the process that finishes the current burst
        if proc[0] is not None and \
                        proc[0].cur_burst_time == proc[0].cpu_burst_time:
            proc[0].left_num -= 1
            # Terminated the process after all cpu burst
            if proc[0].left_num == 0:
                proc[0].end_t = t
                ended.append(proc[0])
                print("time %dms: Process %s terminated %s" % (t, proc[0].proc_id,
                                                               printq(ready)))
            # If more to go, add to IO block
            else:
                print("time %dms: Process %s completed a CPU burst; %d burst to go" \
                      " %s" % (t, proc[0].proc_id, proc[0].left_num, printq(ready)))

                end_t = t + proc[0].io_time + t_cs / 2
                proc[0].arrival_time = end_t
                proc[0].cur_burst_time = 0
                proc[0].last_burst_time = 0
                block.append(proc[0])
                block.sort()
                if end_t not in time_schedule:
                    heapq.heappush(time_schedule, end_t)
                print("time %dms: Process %s switching out of CPU; will blocked on I/O until time %dms" \
                      " %s" % (t, proc[0].proc_id, end_t, printq(ready)))
            # Reset current process
            proc[0] = None
            # Start context switch
            context_switch = t + t_cs / 2
            if context_switch not in time_schedule:
                heapq.heappush(time_schedule, context_switch)

        # =
        # Add processes to the queue for there initial arrive
        for i in range(len(R_proc)):
            if R_proc[0].initial_arrival_time == t:
                temp = R_proc.pop(0)
                ready.append(temp)
                print("time %dms: Process %s arrived and added to ready queue %s" % (t, temp.proc_id, printq(ready)))
            else:
                break
        # Add processes to the queue after IO block
        for i in range(len(block)):
            if block[0].arrival_time == t:
                temp = block.pop(0)
                ready.append(temp)
                print("time %dms: Process %s completed I/O %s" % (t, temp.proc_id,
                                                                  printq(ready)))
            else:
                break
        oldp = copy.deepcopy(proc[0])

        if context_switch == -1:
            if proc[0] is None and len(ready) != 0:
                proc[0] = ready.pop(0)
                proc[0].sch_burst_time = min(t_slice, proc[0].cpu_burst_time-proc[0].cur_burst_time)
            elif proc[0] is not None and proc[0].cur_burst_time != proc[0].last_burst_time and (proc[0].cur_burst_time % t_slice) == 0:
                if len(ready) == 0:
                    proc[0].sch_burst_time = min(t_slice, proc[0].cpu_burst_time-proc[0].cur_burst_time)
                    print( "time %dms: Time slice expired; no preemption because ready queue is empty %s"%(t,printq(ready)))
                else:
                    proc[0].last_burst_time = proc[0].cur_burst_time
                    proc[0].prempt_num += 1
                    ready.append(proc[0])
                    proc[0] = None
                    print( "time %dms: Time slice expired; process %s preempted with %dms" \
                           " to go %s" % (t,ready[-1].proc_id, ready[-1].cpu_burst_time-ready[-1].cur_burst_time,printq(ready)))
            # Do context switch if current process changed
            if proc[0] is None and oldp is None:
                pass
            elif proc[0] is None and oldp is not None:
                context_switch = t + t_cs / 2
                if context_switch not in time_schedule:
                    heapq.heappush(time_schedule, context_switch)
            elif proc[0] is not None and oldp is None:
                context_switch = t + t_cs / 2
                if context_switch not in time_schedule:
                    heapq.heappush(time_schedule, context_switch)
            elif proc[0].proc_id != oldp.proc_id:
                context_switch = t + t_cs / 2
                if context_switch not in time_schedule:
                    heapq.heappush(time_schedule, context_switch)
            # Add the new scheduled burst time
            elif proc[0] is not None and proc[0].sch_burst_time != 0:
                if (t + proc[0].sch_burst_time) not in time_schedule:
                    heapq.heappush(time_schedule, t + proc[0].sch_burst_time)
                proc[0].sch_burst_time = 0

        if len(time_schedule) == 0:
            break
        time_schedule.sort()
        dif_t = time_schedule.pop(0) - t
        for i in range(len(ready)):
            # Fix the wait time difference for context switch
            # WARNING: This might cause the individual wait time wrong
            if i == 0 and context_switch != -1 and proc[0] is None:
                pass
            else:
                ready[i].wait_t += dif_t

        if context_switch == -1 and proc[0] is not None:
            proc[0].cur_burst_time += dif_t

        t += dif_t
    print("time %dms: Simulator ended for RR" % (t))




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
    RR(p_list)
    # Write simulation results to file
    fp = open(output_file_str, "w+")
    fp.close()