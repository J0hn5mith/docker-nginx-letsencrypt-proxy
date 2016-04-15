#! /usr/bin/python

# Event Listener Process for supervisor
# Invoked a script designed to periodically request updates 
import sys
import subprocess

def write_stdout(s):
	sys.stdout.write(s)
	sys.stdout.flush()

def write_stderr(s):
	sys.stderr.write(s)
	sys.stderr.flush()

def main():
	while True:
		write_stdout('READY\n') # transition from ACKNOWLEDGED to READY
		line = sys.stdin.readline()  # read header line from stdin
		write_stderr(line) # print it out to stderr
		headers = dict([ x.split(':') for x in line.split() ])
		data = sys.stdin.read(int(headers['len'])) # read the event payload
		res = subprocess.call("/opt/letsencrypt-run.sh", stdout=sys.stderr) # don't mess with real stdout
		write_stderr(data)
		write_stdout('RESULT 2\nOK') # transition from READY to ACKNOWLEDGED

if __name__ == '__main__':
	# Do this first
	subprocess.call("/opt/letsencrypt-run.sh", stdout=sys.stderr)
	main()
	import sys