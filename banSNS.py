#!/usr/bin/python

import shutil
import argparse
import subprocess
import sys
 
parser = argparse.ArgumentParser(description='Modify /private/etc/hosts to ban to access fb')
parser.add_argument('-m','--mode', help='mode ban/allow',required=True)
args = parser.parse_args()
 
lines = []
hosts_file_path = '/private/etc/hosts'
mode = args.mode

with open(hosts_file_path, 'r') as f:
	for line in f.readlines():
		if mode == 'allow':
			if line.find('facebook.com') != -1 and line[0] != '#':
				line = "#" + line
		elif mode == 'ban':
			if line.find('facebook.com') != -1 and line[0] == '#':
				line = line[1:]
		else:
			sys.exit(0)
		lines.append(line)

with open( hosts_file_path + '_tmp', 'w') as new_host:
	for line in lines:
		new_host.write(line)

try:
	shutil.move(hosts_file_path + '_tmp', hosts_file_path)
	subprocess.call("dscacheutil -flushcache", shell=True)
	subprocess.call("cat " + hosts_file_path, shell=True)
except OSError as e:
    print >>sys.stderr, "Execution failed:", e
