
import argparse
import re
import subprocess
import time 
import datetime 
import os
  

# argument parsing
parser = argparse.ArgumentParser(description="Make some samples (names of people).")
parser.add_argument("logfile", type=str, help="celery log file")
parser.add_argument("errfile", type=str, help="batch err file")
args = parser.parse_args()


def single_task_times():
    pre_lines = subprocess.check_output(f"grep \" succeeded in \" {args.logfile}", shell=True).decode('ascii')

    pre_list = pre_lines.strip().split("\n")

    task_durations = []
    for line in pre_list:
        matches = re.search(r"\d+.\d+s:", line)
        if matches:
            match = matches.group(0)
            match = float(match.strip("s:"))
            task_durations.append(match)

    print("- " + task_durations)

def merlin_run_time():
    pre_line = subprocess.check_output(f"grep \"real \" {args.errfile}", shell=True).decode('ascii')
    pre_line = pre_line.strip()
    matches = re.search(r"\d+.\d+s:", pre_line)

def start_verify_time():
    pre_line = subprocess.check_output(f"grep -m1 \"verify\" {args.logfile}", shell=True).decode('ascii')
    pre_line = pre_line.strip()
    matches = re.search(r"\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d,\d\d\d", pre_line)
    match = matches[0]
    element = datetime.datetime.strptime(match, "%Y-%m-%d %H:%M:%S,%f")
    timestamp = datetime.datetime.timestamp(element)
    print("- start verify : " + str(timestamp))
    
def start_run_workers_time():
    pre_line = subprocess.check_output(f"grep -m1 \"\" {args.logfile}", shell=True).decode('ascii')
    pre_line = pre_line.strip()
    matches = re.search(r"\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d,\d\d\d", pre_line)
    match = matches[0]
    element = datetime.datetime.strptime(match, "%Y-%m-%d %H:%M:%S,%f")
    timestamp = datetime.datetime.timestamp(element)
    print("- start run-workers : " + str(timestamp))
    
def start_sample1_time():
    pre_line = subprocess.check_output(f"grep -m1 \"Executing step 'null_step'\" {args.logfile}", shell=True).decode('ascii')
    pre_line = pre_line.strip()
    matches = re.search(r"\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d,\d\d\d", pre_line)
    match = matches[0]
    element = datetime.datetime.strptime(match, "%Y-%m-%d %H:%M:%S,%f")
    timestamp = datetime.datetime.timestamp(element)
    print("- start samp1 : " + str(timestamp))
    

def main():
    single_task_times()
    #merlin_run_time()
    start_verify_time()
    start_run_workers_time()
    start_sample1_time()

if __name__ == "__main__":
    main()
