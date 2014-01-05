#!/usr/bin/python

import shutil
import argparse
import subprocess
import sys
 
parser = argparse.ArgumentParser(description='Modify /private/etc/hosts to ban to access fb')
parser.add_argument('-s','--status', help='mode ban/allow', required=True)
args = parser.parse_args()
 
lines = []
hosts_file_path = '/private/etc/hosts'
status = args.status
facebooks = 'facebook.com www.facebook.com login.facebook.com'.split()
twitters = 'twitter.com www.twitter.com'.split()

if not status in 'allow ban origin backup'.split():
	sys.exit(0)

if not status == 'origin':
	with open(hosts_file_path, 'r') as f:
		if status == 'allow':
			for line in f.readlines():
				for sns in facebooks + twitters:
					if line.find(sns) != -1:
						break
				else:
					lines.append(line)

		elif status == 'ban':
			for line in f.readlines():
				lines.append(line)

			for sns in facebooks + twitters:
				line = '127.0.0.1 ' + sns + "\n"
				lines.append(line)

elif status == 'origin':
	origin = '''
##
# Host Database
#
# localhost is used to configure the loopback interface
# when the system is booting.  Do not change this entry.
##
127.0.0.1                  localhost
255.255.255.255	broadcasthost
::1                            localhost 
fe80::1%lo0	        localhost
'''
	lines = origin

with open( hosts_file_path + '_tmp', 'w') as new_host:
	for line in lines:
		new_host.write(line)

try:
	shutil.move(hosts_file_path + '_tmp', hosts_file_path)
	subprocess.call("dscacheutil -flushcache", shell=True)
	subprocess.call("cat " + hosts_file_path, shell=True)
except OSError as e:
    print >>sys.stderr, "Execution failed:", e
