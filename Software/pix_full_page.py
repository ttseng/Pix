# pix_full_page.py
# 
# This version of the pix script will print on an entire 8.5x11 sheet of paper
# 
# Written by ttseng 8/23/16

import os
import pygame, sys
import picamera
import cups
import time
from time import sleep
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from reportlab.pdfbase.pdfmetrics import stringWidth 
from reportlab.lib.colors import black, HexColor
from reportlab.platypus.flowables import Image
import RPi.GPIO as GPIO

FONTNAME = "Helvetica"
FONTSIZE = 25
SMALLFONTSIZE = 20

# page dimensions
PG_WIDTH = 8.5*inch
PG_HEIGHT = 11*inch

# image dimensions
WIDTH = 1024
HEIGHT = 768
SCALE = 0.56

LED_PIN = 14
BUTTON_PIN = 4

def generatePage():
	# camera.start_preview()
	camera.capture("test.jpg")

	# create a pdf file with this image
	c = canvas.Canvas("test.pdf")
	offset = 0.75*inch
	x = 0.15*inch
	y = PG_HEIGHT+offset/4
	c.drawImage("test.jpg", x, y-HEIGHT*SCALE-0.15*inch, WIDTH*SCALE, HEIGHT*SCALE)

	# add date
	date = time.strftime("%A %b %e").upper()
	c.setFont(FONTNAME, FONTSIZE)
	c.drawString(x, y, date)
	# add other fields
	projectLabel = "I'm working on... "
	c.setFont(FONTNAME, FONTSIZE)
	c.drawString(x, y-HEIGHT*SCALE-0.75*inch, projectLabel)
	c.save()

def printPage():
	# print the image
	conn = cups.Connection()
	printers = conn.getPrinters()
	for printer in printers:
		print printer, printers[printer]["device-uri"]
	printer_name = printers.keys()[1] # 0 for ML, 1 for HATCH
 
	conn.printFile(printer_name, "test.pdf", "test", {})


# SETUP
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, bouncetime=200)
camera = picamera.PiCamera()
camera.resolution = (WIDTH, HEIGHT)
# camera.start_preview()

def blinkLED():
	GPIO.output(LED_PIN, GPIO.HIGH)
	time.sleep(1)
	GPIO.output(LED_PIN, GPIO.LOW)
	time.sleep(1)

while(True):
	# check for button input
	
	if GPIO.event_detected(BUTTON_PIN):
		print("Button Pressed")
		# turn on LED	
		GPIO.output(LED_PIN, GPIO.HIGH)
	
		# print picture
		generatePage()
		printPage()
		
		# turn off LED
		GPIO.output(LED_PIN, GPIO.LOW)
