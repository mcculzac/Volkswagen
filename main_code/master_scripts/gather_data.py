###################
# Zac McCullough
# mccul157@msu.edu
# 3/13
###################

"""
This will  be given a model python location and it will run the script and log clicks and then put data into unclean
data folder.
"""

#########
# imports
#########

import sys
import ctypes
import os
import threading
import importlib.util
from pywinauto.win32_hooks import Hook, KeyboardEvent, MouseEvent
sys.path.append('../')


###############
# function defs
###############

def execute_auto(path: str) -> None:
    """
    Given the path to the python automation script execute and records the keyboard logs
    :param path: relative path, direct path OR if just a file name (no parenteces), executes in automations
                 with same name
    :return: None
    """

    output_file = '../data/unclean_data/'

    file_source = ''
    name_of_auto = ''
    # if path ends with the .py, remove it
    if path[-3:] == '.py':
        path = path[:-3]
    # conditions
    if '/' not in path and '\\' not in path:
        # we don't have a path, we just have a direct name
        file_source = '../automations/' + path
        name_of_auto = path
    elif '.' in path:
        # we have a relative path
        file_source = path

        # for these we just split the path name via / or \ and take the last one which is the name
        if '/' in path:
            name_of_auto = path.split('/')[-1]
        elif '\\' in path:
            name_of_auto = path.split('\\')[-1]
        else:
            raise ValueError('Have . in path, implying relative, but no parentaces! ' + path)
    elif ':' in path:
        # we have a full path like C:/
        file_source = path
        if '/' in path:
            name_of_auto = path.split('/')[-1]
        elif '\\' in path:
            name_of_auto = path.split('\\')[-1]
        else:
            raise ValueError('Have : in path, implying full path, but no parentaces! ' + path)
    else:
        raise ValueError('Could not parse path type! Error: ', path)

    # set output file
    output_file += name_of_auto + '.csv'
    # set the script path
    script_path = file_source + '.py'

    if not os.path.exists(script_path):
        raise ValueError('Script path not found! Error: ', script_path)

    open(output_file, 'w').close()  # wipe the file of data

    # define on event for logger
    def on_event(args) -> None:
        """
        Event handler that is called every time an event occurs (SLOW!)
        :param args: our events
        :return: none
        """
        with open(output_file, 'a') as f:
            if isinstance(args, KeyboardEvent) and args.event_type == 'key down':
                if args.current_key.lower() == 'return':
                    f.write('\n')
                else:
                    f.write(str(args.current_key) + ',')

    spec = importlib.util.spec_from_file_location("automationTask", script_path)
    task = importlib.util.module_from_spec(spec)

    def listen():
        # set up hook
        hook = Hook()
        hook.handler = on_event
        hook.hook(keyboard=True, mouse=True)

        hook.listen()

    def run_script():
        spec.loader.exec_module(task)

    # https://stackoverflow.com/questions/323972/is-there-any-way-to-kill-a-thread
    def terminate_thread(thread):
        """Terminates a python thread from another thread.

        :param thread: a threading.Thread instance
        """
        if not thread.isAlive():
            return

        exc = ctypes.py_object(SystemExit)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            ctypes.c_long(thread.ident), exc)
        if res == 0:
            raise ValueError("nonexistent thread id")

    t = threading.Thread(target=listen)
    t.start()
    run_script()
    terminate_thread(t)
    print('end_all!')


def __main__():
    execute_auto('warehouse_data.py')


__main__()






