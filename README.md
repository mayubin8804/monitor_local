# Monitor_Local - Tasks submit and monitor software for Linux system
Monitor_Local is a software that can executes and monitors multiple tasks on Linux system. The tasks can be executed in specified order based on your config file.

## Introduction
A task is a shell script, if you want to execute a lot of tasks in a specified order, for example, you want to execute task1.sh and task2.sh parrallel and then execute task3.sh after they are finished, you can use monitor_local.  
Monitor_Local use ZODB to store the information of tasks and use crontab to monitor the execution of the tasks.

## Installation
First, you must make sure that you have installed Python 2.7. And then you just need to download the software and uncompress it into a suitable path.

## How to use
The only program you need to use in monitor_local is `bin/pymonitor_local.py`, there are several subcommand for this program.
