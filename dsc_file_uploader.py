#!/usr/bin/env python3

import glob
import re
import time
import pathlib

def list_conf_file(dir_path):
    conf_list = list()
    tmp_list = glob.glob(dir_path)

    for i in tmp_list:
        if 'sample' not in i:
            conf_list.append(i)
    return conf_list

def find_xml_stored_dir(dsc_conf):
    with open(dsc_conf, 'r') as f:
        for line in f:
            line = line.rstrip()
            if re.search(r'^run_dir', line):
                xml_path = line.replace('run_dir','').split('"')[1]
    return xml_path

def find_files_by_mtime(dir_path):

    file_list = list()
    current_epoch = int(time.time())
    upper_mtime = current_epoch - int(61)
    lower_mtime = current_epoch - int(300)

    tmp_list = glob.glob(dir_path)

    for i in tmp_list:
        fname = pathlib.Path(i)
        if upper_mtime > int(fname.stat().st_mtime) > lower_mtime:
            file_list.append(i)
    return file_list
        
if __name__ == '__main__':
    file_list = list()
    conf_list = list_conf_file(dir_path=r'/etc/dsc/*dsc*conf*')

    for conf in conf_list[0:1]:
        xml_path = find_xml_stored_dir(conf)
        search_path = f"{xml_path}/*"
        file_list = find_files_by_mtime(dir_path=r'%s' % search_path)
        #print(file_list)

    for i in file_list:
        print(f"sshpass -p aaa scp {i} ansible_adm@:")