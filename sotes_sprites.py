#!/usr/bin/python

import Image
import os, sys
from struct import unpack

def extract_image(f, target_path):
	file_data = f.read()

	use_palette = ord(file_data[1131]) & 4 == 4
	magic = ord(file_data[0])

	#found by trial-and-error...
	if magic == 31:
		use_palette = ord(file_data[1073]) & 1 != 1
		pixel_data_offset = 1115
		width = unpack('I', file_data[12:16])[0] - 13045

	elif magic == 37:
		use_palette = ord(file_data[1073]) & 1 != 1
		pixel_data_offset = 1129
		width = unpack('I', file_data[16:20])[0] - 13039

	elif magic == 45:
		pixel_data_offset = 1144
		width = unpack('I', file_data[8:12])[0] - 13031

	elif magic == 51:
		pixel_data_offset = 1158
		width = unpack('I', file_data[16:20])[0] - 13025

	elif magic == 59:
		use_palette = False
		pixel_data_offset = 1122
		width = unpack('I', file_data[8:12])[0] - 13019

	elif magic == 67:
		pixel_data_offset = 1136
		width = unpack('I', file_data[12:16])[0] - 13013

	elif magic == 95:
		pixel_data_offset = 1142
		width = unpack('I', file_data[8:12])[0] - 12987

	elif magic == 73:
		pixel_data_offset = 1150
		width = unpack('I', file_data[1140:1144])[0] - 13005

	elif magic == 103:
		pixel_data_offset = 1156
		width = unpack('I', file_data[1152:1156])[0] - 12979

	else:
		raise Exception('Unknown magic', magic)

	if use_palette:
		channels = 1
		palette_offset = 32
		palette = {}
		for i in range(256):
			palette[i] = unpack('BBBB', file_data[palette_offset + i*4:palette_offset + i*4 + 4])
	else:
		channels = 3

	pixel_data = file_data[pixel_data_offset:]
	height = len(pixel_data) / (width * channels)

	print 'magic  ', magic
	print 'offset ', pixel_data_offset
	print 'width  ', width
	print 'height ', height
	print 'palette', use_palette

	img = Image.new('RGB', (width, height), 'black')
	pixels = img.load()
	for y in range(height):
		for x in range(width):
			index = (y * width + x) * channels
			if use_palette:
				i = ord(pixel_data[index])
				r = palette[i][0]
				g = palette[i][1]
				b = palette[i][2]
			else:
				r = ord(pixel_data[index])
				g = ord(pixel_data[index + 1])
				b = ord(pixel_data[index + 2])
			pixels[x, height - 1 - y] = (b, g, r)
	img.save(target_path)

paths = sys.argv[1:]
if len(paths) == 0:
	print 'Usage: ' + sys.argv[0] + ' PATHS'

for path in paths:
	target_path = path + '.png'
	print target_path

	if os.path.exists(target_path):
		print 'Target file already exists'
	else:
		with open(path) as f:
			try:
				extract_image(f, target_path)
				print 'Image saved'
			except Exception as e:
				print 'Error', e

	print
