#!/usr/bin/python

import os, sys

def listRepo(fileTo):

	path = "/home/pi/Bureau/BTMachines_git/Samples/"+fileTo+"/"
	dirs = os.listdir( path )
	return dirs
