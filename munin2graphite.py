#!/usr/bin/env python

from os import listdir
from os.path import isfile, join
import subprocess, re
import socket
import time

startTime = time.time()

### config

HOSTNAME = socket.gethostname()

MUNIN_RUN_PATH = "/usr/sbin/munin-run"		# path to muni-run executable
MUNIN_PLUGINS_PATH = "/etc/munin/plugins"	# path to munin plugins config dir with symlinks

CARBON_SERVER = '192.168.200.27'	# ip adress of your graphite server
CARBON_PORT = 2003					# port
CARBON_PREFIX = "munin."			# prefix
CARBON_PROTOCOL = "udp"				# udp or tcp (tcp is fallback)

###

# get munin plugin symlinks
plugins = [ f for f in listdir(MUNIN_PLUGINS_PATH) if isfile(join(MUNIN_PLUGINS_PATH,f)) ]

#open socket
if CARBON_PROTOCOL == "udp":
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
else:
	sock = socket.socket()

sock.connect((CARBON_SERVER, CARBON_PORT))

#cycle through all munin plugins and send data
for plugin in plugins:
	cmd = MUNIN_RUN_PATH + ' ' + plugin
	#print HOSTNAME, 'plugin :', plugin
	output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	outputlines = filter(lambda x:len(x)>0,(line.strip() for line in output.stdout))
	for out in outputlines:
		split_out = out.split(' ')
		key = re.sub('\.value$', '', split_out[0])
		value = split_out[1]
		node = CARBON_PREFIX + HOSTNAME + '.' + plugin + '.' + key
		#print node, value
		graphite_message = node + ' ' + value + ' %d\n' % int(time.time())
		sock.sendall(graphite_message)

# send script execution time
scripttime = time.time() - startTime
print 'Script execution time ', ("%g" % (scripttime)) , " seconds"

node = CARBON_PREFIX + HOSTNAME + '.' + 'script.execution_time' 
message = node + ' ' + str(scripttime) + ' %d\n' % int(time.time())
sock.sendall(message)

sock.close()
