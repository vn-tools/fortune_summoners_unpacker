#!/usr/bin/python

import Image
import os, sys
from struct import unpack

class MagicException(Exception):
	pass

def extract_image(f, target_path):
	file_data = f.read()

	magic = ord(file_data[0])

	#found by trial-and-error...
	if magic == 31:
		use_palette = ord(file_data[1073]) & 1 != 1
		pixel_data_offset = 59
		width = unpack('I', file_data[12:16])[0] - unpack('I', file_data[24:28])[0]

	elif magic == 37:
		use_palette = ord(file_data[1073]) & 1 != 1
		pixel_data_offset = 73
		width = unpack('I', file_data[16:20])[0] - unpack('I', file_data[24:28])[0]

	elif magic == 45:
		use_palette = ord(file_data[1131]) & 4 == 4
		pixel_data_offset = 88
		width = unpack('I', file_data[8:12])[0] - unpack('I', file_data[24:28])[0]

	elif magic == 51:
		use_palette = ord(file_data[1131]) & 4 == 4
		pixel_data_offset = 102
		width = unpack('I', file_data[16:20])[0] - unpack('I', file_data[24:28])[0]

	elif magic == 59:
		use_palette = False
		pixel_data_offset = 66
		width = unpack('I', file_data[8:12])[0] - 13019

	elif magic == 67:
		use_palette = ord(file_data[1131]) & 4 == 4
		pixel_data_offset = 80
		width = unpack('I', file_data[12:16])[0] - 13013

	elif magic == 95:
		use_palette = ord(file_data[1131]) & 4 == 4
		pixel_data_offset = 86
		width = unpack('I', file_data[8:12])[0] - 12987

	elif magic == 73:
		use_palette = ord(file_data[1131]) & 4 == 4
		pixel_data_offset = 94
		width = unpack('I', file_data[4:8])[0] - 13005

	elif magic == 85:
		use_palette = True
		pixel_data_offset = 67
		width = unpack('I', file_data[16:20])[0] - unpack('I', file_data[24:28])[0] + 2

	elif magic == 93:
		use_palette = ord(file_data[1131]) & 4 == 4
		pixel_data_offset = 81
		width = unpack('I', file_data[8:12])[0] - unpack('I', file_data[24:28])[0] + 1

	elif magic == 101:
		use_palette = False
		pixel_data_offset = 95
		width = unpack('I', file_data[16:20])[0] - unpack('I', file_data[24:28])[0] + 1

	elif magic == 103:
		use_palette = ord(file_data[1131]) & 4 == 4
		pixel_data_offset = 100
		width = unpack('I', file_data[16:20])[0] - 12979

	elif magic == 107:
		use_palette = False
		pixel_data_offset = 59
		width = unpack('I', file_data[8:12])[0] - unpack('I', file_data[24:28])[0] + 1

	elif magic == 115:
		use_palette = False
		pixel_data_offset = 73
		width = unpack('I', file_data[12:16])[0] - unpack('I', file_data[24:28])[0] + 1

	elif magic == 121:
		use_palette = False
		pixel_data_offset = 87
		width = unpack('I', file_data[4:8])[0] - unpack('I', file_data[24:28])[0] + 1

	elif magic == 129:
		use_palette = ord(file_data[1131]) & 4 == 4
		pixel_data_offset = 102
		width = unpack('I', file_data[12:16])[0] - unpack('I', file_data[24:28])[0]

	elif magic == 137:
		use_palette = False
		pixel_data_offset = 66
		width = unpack('I', file_data[4:8])[0] - unpack('I', file_data[24:28])[0]

	elif magic == 143:
		use_palette = ord(file_data[1131]) & 4 == 4
		pixel_data_offset = 80
		width = unpack('I', file_data[8:12])[0] - unpack('I', file_data[24:28])[0]

	elif magic == 151:
		use_palette = ord(file_data[1131]) & 4 == 4
		pixel_data_offset = 94
		width = unpack('I', file_data[16:20])[0] - unpack('I', file_data[24:28])[0]

	else:
		raise MagicException('Unknown magic', magic)

	if use_palette:
		channels = 1
		palette_offset = 32
		palette = {}
		for i in range(256):
			palette[i] = unpack('BBBB', file_data[palette_offset + i*4:palette_offset + i*4 + 4])
	else:
		channels = 3

	pixel_data = file_data[32 + 256 * 4 + pixel_data_offset:]
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
			except MagicException as e:
				print 'Error', e

	print
