import math
import numpy as np
from LightPipes import *
import matplotlib
import matplotlib.pyplot as plt

def get_middle(list):
	dim = math.floor(len(list)/2)
	return dim

def SLM_mask(width, x, y, value_re, value_im, F):
	# translate mm into pixels
	pixel_size = F._siz/F.grid_dimension
	width_in_pixels = width/pixel_size
	x_in_pixels = (math.floor(x/pixel_size))
	y_in_pixels = (math.floor(y/pixel_size))

	F1=F.copy(F)

	mid = get_middle(F1.field)
	half_width = width_in_pixels/2

	if half_width % 1 != 0:
		F1.field[mid+x_in_pixels,mid+x_in_pixels] = complex(value_re, value_im)
		for i in range(math.ceil(half_width)):
			for j in range(math.ceil(half_width)):
				F1.field[mid+x_in_pixels-i,mid+y_in_pixels-j] = complex(value_re, value_im)
				F1.field[mid+x_in_pixels+i,mid+y_in_pixels+j] = complex(value_re, value_im)
				F1.field[mid+x_in_pixels+i,mid+y_in_pixels-j] = complex(value_re, value_im)
				F1.field[mid+x_in_pixels-i,mid+y_in_pixels+j] = complex(value_re, value_im)

	else:
		half_width = int(half_width)
		for i in range(- half_width, half_width):
			for j in range(- half_width, half_width):
				F1.field[mid+x_in_pixels+i,mid+y_in_pixels+j] = complex(value_re, value_im)

	return F1

def bypixel_mask(F, mask):

	if len(mask)!=len(mask[0]):
		print("Error, mask is not rectangular! Supply rectangular mask.")

	if len(mask)!=len(F.field):
		print("Error, dims of mask are not equal to dims of field! Supply equal dims.")

	M = np.zeros((len(mask),len(mask)),dtype=complex)

	for i in range(len(mask)):
		for j in range(len(mask)):
			M[i,j] = complex(math.cos(mask[i,j]), math.sin(mask[i,j]))

	F1=F.copy(F)

	for i in range(len(mask)):
			for j in range(len(mask)):
				F1.field[i,j] = M[i,j]

	F_res = F1

	return F_res





