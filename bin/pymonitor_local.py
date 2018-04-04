#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
Task monitor system for local machine.
------------------------
Created by Ma Yubin
Version 0.1.0 (20180322)
'''

import os
import sys
import argparse
import re
import logging
import logging.handlers
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'lib', 'python2.7', 'site-packages'))
import myConfigFile
import myProjectDB

# create logger
logger_main = logging.getLogger('monitor_local')
logger_main.setLevel(logging.DEBUG)
logger_ZODB = logging.getLogger('ZODB')
logger_ZODB.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter('%(asctime)s %(name)s-%(levelname)s: %(message)s', datefmt='[%Y-%m-%d %H:%M:%S]')
# create file handler
logDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'log')
if not os.path.isdir(logDir):
    os.makedirs(logDir)
logFile = os.path.join(logDir, 'monitor_local.log')
fh = logging.handlers.RotatingFileHandler(logFile, mode='a', maxBytes=10000000, backupCount=5)
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
# create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
# add the handlers to the logger
logger_main.addHandler(fh)
logger_main.addHandler(ch)
logger_ZODB.addHandler(fh)
logger_ZODB.addHandler(ch)

def parseArgs():
    '''Parse the arguments from command line'''
    
    desc = '''
    Task monitor system for local machine.
    Created by Ma Yubin
    Version 0.1.0 (20180322)\
    '''
    parser = argparse.ArgumentParser(
        usage='%(prog)s subcommand [options]',
        description=desc,
        formatter_class=argparse.RawDescriptionHelpFormatter
        )
    subparsers = parser.add_subparsers(
        title='subcommands',
        description='you can use -h/--help after subcommand to check the help information.',
        prog=os.path.basename(sys.argv[0]),
        dest='subcommand',
        metavar='',
        )
    
    def emailAddr(optStr):
        if not re.match(r'\w+@\w+', optStr):
            raise argparse.ArgumentTypeError('%s is not a email address' % optStr)
        return optStr
    
    def projName(optStr):
        if not re.match(r'^\w+$', optStr):
            raise argparse.ArgumentTypeError('Special character is not allowed in project name.')
        return optStr
    
    # the subcommand: setdefault
    parser_1 = subparsers.add_parser(
        'setdefault', usage='%(prog)s [options]',
        formatter_class=argparse.RawTextHelpFormatter,
        help='Set default value.'
        )
    parser_1.add_argument('-e', type=emailAddr, metavar='<Email>', dest="opt_e", help='set defualt email address.')


    # the subcommand: qsubsge
    parser_2 = subparsers.add_parser(
        'qsubsge', usage='%(prog)s -i <File> -p <STR> [options]',
        formatter_class=argparse.RawTextHelpFormatter,
        help='Add a qsub_sge.pl format task list.'
        )
    parser_2.add_argument('-i', required=True, metavar='<FILE>', dest="opt_i", help='input work.sh file, required.')
    parser_2.add_argument('-p', required=True, type=projName, metavar='<STR>', dest="opt_p", help='project name for monitor, required.')
    parser_2.add_argument('-L', type=int, default=1, metavar='<INT>', dest="opt_L", help='number of lines for each job. [%(default)d]')
    parser_2.add_argument('-n', type=int, default=10, metavar='<INT>', dest="opt_n", help='maximum number of jobs. [%(default)d]')
    parser_2.add_argument(
        '-m', type = int, choices = [0, 1], default = 0, metavar = '<INT>', dest = "opt_m",
        help = "Operation mode for submitting in the same project. [%(default)d]\n" +
            "   0   Submit new jobs parallel with the old jobs.\n" +
            "   1   Submit new jobs depend on the old jobs."
        )
    
    # the subcommand: taskmonitor
    parser_3 = subparsers.add_parser(
        'taskmonitor', usage = '%(prog)s -i <File> -p <STR> [options]',
        formatter_class = argparse.RawTextHelpFormatter,
        help = 'Add a task_monitor.py format task list.'
        )
    parser_3.add_argument('-i', required = True, metavar = '<FILE>', dest = "opt_i", help = 'input config.txt file, required.')
    parser_3.add_argument('-p', required = True, metavar = '<STR>', dest = "opt_p", help = 'project name for monitor, required.')
    parser_3.add_argument('-n', type = int, metavar = '<INT>', dest = "opt_n", help = 'maximum number of jobs.')
    
    # the subcommand: cron
    parser_4 = subparsers.add_parser(
        'cron', usage = '%(prog)s [options]',
        formatter_class = argparse.RawTextHelpFormatter,
        help = 'Do cron job.')
    
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)
    
    args = parser.parse_args()
    return args

def setdefault(argsObj, cfgObj):
    if argsObj.opt_e:
        cfgObj.setDefEmail(argsObj.opt_e)

def importProject(argsObj, cfgObj):
    prjDBDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'projectDB')
    if not os.path.isdir(prjDBDir):
        os.makedirs(prjDBDir)
    
    taskListFile = argsObj.opt_i
    projectName  = argsObj.opt_p
    projectDB    = cfgObj.getPrjDB(projectName)
    if projectDB == '':
        projectDB = os.path.join(prjDBDir, projectName + '.db')
        logger_main.info("New project. Project Name: %s, Project db: %s", projectName, projectDB)
        logger_main.info("Add project to global config file")
        cfgObj.addProject(projectName, projectDB)
    else:
        logger_main.info("Existing project. Project Name: %s, Project db: %s", projectName, projectDB)
    
    myProjectDBObj = myProjectDB.MyProjectDB(projectName, projectDB)
    if argsObj.subcommand == 'qsubsge':
        myProjectDBObj.importQsubsge(taskListFile, argsObj.opt_m, argsObj.opt_L)
    else:
        myProjectDBObj.importPymonitor(taskListFile)

if __name__ == '__main__':
    args = parseArgs()
    
    cfgDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'conf')
    cfgFileObj = myConfigFile.MyCfgFile(cfgDir)
    
    command = args.subcommand
    if command == 'setdefault':
        setdefault(args, cfgFileObj)
    elif command == 'qsubsge' or command == 'taskmonitor':
        importProject(args, cfgFileObj)
    elif command == 'cron':
        pass