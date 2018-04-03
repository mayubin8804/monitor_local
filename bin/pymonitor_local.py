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
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'lib', 'python2.7', 'site-packages'))
import myConfigFile

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
    
    # the subcommand: cron
    parser_3 = subparsers.add_parser(
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
    print "Creating database. This might take a while..."
    projectName = argsObj.opt_p
    projectDB   = cfgObj.getPrjDB(projectName)
    if projectDB == '':
        projectDB = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'projectDB', projectName + '.db')
        cfgObj.addProject(projectName, projectDB)
    

if __name__ == '__main__':
    args = parseArgs()
    
    cfgDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'conf')
    cfgFileObj = myConfigFile.MyCfgFile(cfgDir)
    
    command = args.subcommand
    if command == 'setdefault':
        setdefault(args, cfgFileObj)
    elif command == 'qsubsge':
        pass