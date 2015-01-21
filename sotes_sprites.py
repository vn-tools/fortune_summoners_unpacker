#!/usr/bin/python

import Image
import os, sys
from struct import unpack

def guess_image_dimension(
	dimension_candidates,
	main_delta,
	additional_deltas,
	pixels_size):
	dimension = False
	for base in dimension_candidates:
		for delta in additional_deltas:
			possible_dimension = base + delta + main_delta
			if possible_dimension < 0:
				continue
			if pixels_size % possible_dimension == 0:
				return possible_dimension
	raise Exception('Cannot figure out the image dimensions')


def extract_image(f, target_path):
	file_data = f.read()

	weird_data = unpack('8I', file_data[0:32])
	weird_data2 = unpack('14I', file_data[32 + 256 * 4:32 + 256 * 4 + 56])
	pixel_data_offset = 56 + weird_data2[12] - weird_data2[10]
	pixel_data = file_data[32 + 256 * 4 + pixel_data_offset:]

	width = guess_image_dimension(
		weird_data[1:5],
		- weird_data[6],
		[0, 1, 2, 3],
		len(pixel_data))

	height = guess_image_dimension(
		weird_data2[0:5],
		- weird_data2[10],
		[0],
		len(pixel_data))

	use_palette = width * height * 3 != len(pixel_data)

	if use_palette:
		channels = 1
		palette_offset = 32
		palette = {}
		for i in range(256):
			palette[i] = unpack('BBBB', file_data[palette_offset + i*4:palette_offset + i*4 + 4])
	else:
		channels = 3

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
