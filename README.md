# Monitor_Local - Tasks submit and monitor software for Linux system
Monitor_Local is a software that can executes and monitors multiple tasks on Linux system. The tasks can be executed in specified order based on your input tasks list file.

## Introduction
A task is a shell script, if you want to execute a lot of tasks in a specified order, for example, you want to execute task1.sh and task2.sh parrallel and then execute task3.sh after they are finished, you can use monitor_local.  
Monitor_Local use ZODB to store the information of tasks and use crontab of Linux to monitor the execution of the tasks.

## Installation
First, you must make sure that you have installed Python 2.7, and then you just need to download the software and uncompress it into a suitable path.

## How to specify the order of tasks
In monitor_local, a task means a shell scripts, you can specify the execution order of multiple tasks by tasks list file. There are 2 formats of the list file you can use.  
**Note**: The path of the shell scripts must be absolute path.

### *Format 1*
In this format, one or more lines represent one task, you can specify the line number of each task, the list file will be split into several shell scripts and these scripts will be executed parallel. E.g.:  
```
echo start task 1 at `date`
/path/to/task1.sh
echo finish task 1 at `date`
echo start task 2 at `date`
/path/to/task2.sh
echo finish task 2 at `date`
```
If you specify that every 3 lines represent one task, the task list above will be split into 2 shell scripts as below, and these two shell scripts will be executed parallel.  
*script_1.sh*  
```
echo start task 1 at `date`
/path/to/task1.sh
echo finish task 1 at `date`
```
*script_2.sh*  
```
echo start task 2 at `date`
/path/to/task2.sh
echo finish task 2 at `date`
```

### *Format 2*
In this format, you can put two tasks separated  by space or Tab in one line, the second task will be executed after the first task is finished. E.g.:
```
/path/to/task1.sh
/path/to/task2.sh  /path/to/task3.sh
/path/to/task2.sh  /path/to/task4.sh
```
It means that task1.sh and task2.sh will be executed parallel first, task3.sh and task4.sh will be executed parallel after task2.sh is finished.

## How to use
You can use monitor_local as below:

`python bin/pymonitor_local.py subcommand [options]`

The subcommands you can use are shown as below.

### *setdefault*
You can use this subcommand to change the config of monitor_local. E.g.:

`python bin/pymonitor_local.py setdefault -n 10`

This means to set the monitor_local to checks the status of running tasks and executes new tasks every 10 minutes. You can use `python bin/pymonitor_local.py setdefault -h` to get more help information about this subcommand.

### *qsubsge*
This subcommand used to add tasks described in the tasks list file of *Format 1* into a project. E.g.:

`python bin/pymonitor_local.py qsubsge -i task.list -p myProject -L 3`

The options you can use are shown as below:

Option|Required|Description
-|-|-
-i|Yes|Task list file as *Format 1* described above
-p|Yes|The project name you want to add tasks to
-L|No|Number of lines for each job
-n|No|Maximum number of parallel jobs for the project
-m|No|Add mode of the tasks. 0 means add new jobs parallel with the old jobs, 1 means add new jobs depend on the old jobs

### *taskmonitor*
This subcommand used to add tasks described in the tasks list file of *Format 2* into a project. E.g.:

`python bin/pymonitor_local.py taskmonitor -i task.list -p myProject -n 5`

The options you can use are shown as below:

Option|Required|Description
-|-|-
-i|Yes|Task list file as *Format 2* described above
-p|Yes|The project name you want to add tasks to
-n|No|Maximum number of parallel jobs for the project
