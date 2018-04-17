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
In the tasks list file of this format, every line represent one task, all tasks in the file will be executed parallel. E.g.:  
```
/path/to/task1.sh
/path/to/task2.sh
/path/to/task3.sh
```

### *Format 2*


## How to use
You can use monitor_local as below:

`python bin/pymonitor_local.py subcommand [options]`

The subcommands you can use are shown as below.

### *setdefault*
You can use this subcommand to change the config of monitor_local. E.g.:

`python bin/pymonitor_local.py setdefault -n 10`

This means to set the monitor_local to checks the status of running tasks and executes new tasks every 10 minutes. You can use `python bin/pymonitor_local.py setdefault -h` to get more help information about this subcommand.

### *qsubsge*
