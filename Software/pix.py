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
FONTSIZE = 15
SMALLFONTSIZE = 11

# page dimensions
PG_WIDTH = 8.5*inch
PG_HEIGHT = 11*inch

# image dimensions
WIDTH = 1024
HEIGHT = 768
SCALE = 0.25

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
	projectLabel = "Project: "
	c.setFont(FONTNAME, SMALLFONTSIZE)
	c.drawString(x, y-0.5*inch-HEIGHT*SCALE, projectLabel)
	contactLabel = "Contact: "
	c.drawString(x, y-1.5*inch-HEIGHT*SCALE, contactLabel)
	# draw border
	c.strokeColor = HexColor("#D8D8D8")
	bottomX = -0.1*inch
	bottomY = PG_HEIGHT/2-offset
	c.rect(bottomX, bottomY, PG_WIDTH/2, PG_HEIGHT*2, stroke=True, fill=False)
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
GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING, bouncetime=200)
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
