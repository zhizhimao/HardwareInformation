# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 13:48:26 2017
@author: 星空飘飘
Anaconda 3-5.1.0
Python 3.6.4
hardware.py
"""

import psutil
from datetime import datetime  # 时间格式转换


def get_cpu():
    '''获取CPU核数，CPU使用率，每颗CPU使用率'''
    cpu_num = psutil.cpu_count()  # CPU核算
    cpu_total = psutil.cpu_percent()  # 总的CPU使用率
    cpu = psutil.cpu_percent(percpu=True)  # 每颗CPU使用率
    return 'CPU核数:{0}核;总CPU使用率:{1}%;每颗CPU使用率:{2}%' .format(cpu_num, cpu_total, cpu)


def get_mem():
    '''获取内存信息'''
    mem = psutil.virtual_memory()  # 内存所有信息
    mem_total = round(mem.total/(1024*1024*1024))  # 系统总计内存 round对数字进行四舍五入，把字节换算单位GB
    mem_used = round(mem.used/(1024*1024*1024))  # 已使用内存
    mem_free = round(mem.free/(1024*1024*1024))  # 空闲内存
    mem_percent = mem.percent
    swap = psutil.swap_memory()  # 虚拟所有内存信息
    swap_total = round(swap.total/(1024*1024*1024))  # 系统总计虚拟内存
    swap_used = round(swap.used/(1024*1024*1024))  # 已使用虚拟内存
    swap_free = round(swap.free/(1024*1024*1024))  # 空闲虚拟内存
    return '系统内存:{0}G;已使用内存:{1}G;内存占用率:{4}%;虚拟内存:{2}G;已使用虚拟内存:{3}G;' .format(mem_total, mem_used, swap_total, swap_used, mem_percent)


def get_disk(char='c:'):
    '''获取硬盘信息'''
    psutil.disk_io_counters(perdisk=True)  # 所有硬盘IO信息
    psutil.disk_io_counters()  # 磁盘IO信息包括read_count(读IO数)，write_count(写IO数)read_bytes(IO写字节数)，read_time(磁盘读时间)，write_time(磁盘写时间)
    psutil.disk_partitions()  # 磁盘的完整分区信息
    disk = psutil.disk_usage(char)  # 获取分区的状态信息
    disk_total = round(disk.total/(1024*1024*1024))
    disk_used = round(disk.used/(1024*1024*1024))
    disk_free = round(disk.free/(1024*1024*1024))
    return '{0}盘容量：{1}G;已使用{2}G;剩余容量{3}G;' .format(char, disk_total, disk_used, disk_free)


def get_net():
    '''获取网络信息'''
    psutil.net_io_counters(pernic=True)  # 单个网卡的io信息，加上pernic=True
    net = psutil.net_io_counters()
    net.bytes_sent  # 已发送字节
    net.bytes_recv  # 已接收字节
    net.packets_sent  # 已发送包
    net.packets_recv  # 已接收包
    tcp_all = psutil.net_connections()  # 获取TCP网络状态连接
    listen = []
    established = []
    for sconn in tcp_all:
        if sconn.status == 'LISTEN':
            listen.append('监听:IP:{0};端口:{1};进程:{2}' .format(sconn.laddr[0], sconn.laddr[1], sconn.pid))  # 如果是监听状态打印IP和端口、进程号
        elif sconn.status == 'ESTABLISHED':
            established.append('连接:IP:{0};端口:{1};进程:{2}' .format(sconn.laddr[0], sconn.laddr[1], sconn.pid))  # 如果是连接状态打印IP和端口、进程号
    return listen, established


def get_boot_time():
    '''获取开机时间'''
    psutil.boot_time() #显示开机时间
    boot = datetime.fromtimestamp(psutil.boot_time ()).strftime("%Y-%m-%d %H:%M:%S")    #转换成自然时间
    return ('计算机开机时间:{0}' .format(boot))


def get_login_user():
    '''获取系统登录用户信息'''
    login = psutil.users()
    name = login[0].name
    host = login[0].host
    started = datetime.fromtimestamp(login[0].started).strftime("%Y%m%d_%H:%M:%S")
    return '当前系统登录用户:{0};登录IP:{1};登录时间:{2}' .format(name, host, started)


def get_pid():
    '''获取进程信息'''
    pid_all_num = psutil.pids()  # 获取所有进程pid号
    '''
    p = psutil.Process()  # 获取当前运行的pid
    p.name()  # 进程名
    p.exe()  # 进程的bin路径
    p.cwd()  # 进程的工作目录绝对路径
    p.status()  # 进程状态
    datetime.fromtimestamp(p.create_time()).strftime("%Y%m%d_%H:%M:%S")  # 进程创建时间
    p.cpu_times()  # 进程的cpu时间信息,包括user,system两个cpu信息
    p.cpu_affinity()  # get进程cpu亲和度,如果要设置cpu亲和度,将cpu号作为参考就好
    p.memory_percent()  # 进程内存利用率
    p.memory_info()  # 进程内存rss,vms信息
    p.io_counters()  # 进程的IO信息,包括读写IO数字及参数
    p.as_dict()  # 返回进程列表
    p.num_threads()  # 进程开启的线程数
    p.cpu_percent(interval=2)/8  # cpu使用率 /8：除以8颗CPU
    '''
    pid_cpu = []
    for num in pid_all_num:
        print(num, psutil.Process(num).name())
        pid_cpu.append('PID:{0};进程名:{1};' .format(num, psutil.Process(num).name()))
    return pid_cpu


if __name__ == '__main__':
    get_cpu()  # 获取CPU核数，CPU使用率，每颗CPU使用率
    get_mem()  # 获取内存信息
    get_disk()  # 获取硬盘信息
    get_net()  # 获取网络信息
    get_boot_time()  # 获取开机时间
    get_login_user()  # 获取系统登录用户信息
    get_pid()  # 获取进程信息
