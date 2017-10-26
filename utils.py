# coding=UTF-8

import time
import signal
from functools import wraps
from os.path import join, getsize
import os
log_dir = './logs/'

def initiDir(dir):
    # Detect whether the directory is existing, if not then create
    if os.path.exists(dir) == False:
        os.makedirs(dir)

def getCurrentPath():
    import os
    print(os.getcwd())


def format_time(t):
    import time
    format = '%Y-%m-%d %l:%M %p'
    value = time.localtime(int(t))
    dt = time.strftime(format, value)


def log(*args, **kwargs):
    args = " ".join(args)
    format = '%Y-%m-%d %H:%M:%S'
    # time.time() return the unix time
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)

    if kwargs == {}:
        kwargs = ''
    with open(log_dir + 'log.txt', 'a+') as f:
        print >> f, dt, args, kwargs

# Estimate the function/method running time
# How to use: @fn_timer before the function
def fn_timer(fn):
    @wraps(fn)
    def function_timer(*args, **kwargs):
        t0 = time.time()
        result = fn(*args, **kwargs)
        t1 = time.time()
        print("Total time running {}: {} seconds".format(fn.__name__,str(t1 - t0)))
        return result
    return function_timer


def commandLineTool(command):
    import os
    re = os.system(command)
    return re


# read the file
def readFile(file):
    data = None
    path = os.path.split(file)[0]
    filename = os.path.split(file)[1]
    try:
        with open(file, 'rb') as f:
            data = f.read()
    except IOError:
        print("无法打开文件 或 无法找到当前文件 {}".format(filename))
        return None
    return data

# Get the file directory inside the directory
def getDirFileLists(dir):
    file_paths = []
    for parent, dirnames, filenames in os.walk(dir):
        for filename in filenames:
            file_paths.append(parent+filename)
    # print(file_paths)
    return file_paths

# Delete the all files inside the directory
def deleteAllFiles(dir):
    import os
    imgList = os.listdir(dir)
    for fileName in imgList:
        file = os.path.join(dir, fileName)
        os.remove(file)


# Calculate the total Size inside the directory
def getdirsize(dir):
    size = 0
    for root, dirs, files in os.walk(dir):
        size += sum([getsize(join(root, name)) for name in files])
    size = size/1024/1024

    import math
    num = size * 1000
    num = math.floor(num) / 1000
    return str(num)+'MB'


# Todo
def time_limit(interval):
    def wraps(func):
        def handler(signum, frame):
            #TODO have a test, let it directly return
            print('tim_limit RuntimeError')
            # raise RuntimeError()
        def deco(*args, **kwargs):
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(interval)
            res = func(*args, **kwargs)
            signal.alarm(0)
            return res
        return deco
    return wraps

def _initialize_dirs_for_utils():
    initiDir(log_dir)

if __name__ == '__main__':
    # _initialize_dirs_for_utils()
    log('test', 'dd', 'dddd', a = 'dd')


    # a = ['ab']
    # print("%")