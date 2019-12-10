#!/usr/bin/python

import os, sys

def listRepo():

	path = "/home/pi/Bureau/BTMachines_git/Samples/"
	dirs = os.listdir( path )
	return dirs

def listFiles(fileTo):

	path = "/home/pi/Bureau/BTMachines_git/Samples/"+fileTo+"/"
	dirs = os.listdir( path )
	return dirs

def listSaves():

	path = "/home/pi/Bureau/BTMachines_git/Machine_1/saves/"
	dirs = os.listdir( path )
	return dirs
