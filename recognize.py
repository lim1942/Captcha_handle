# -*- coding: utf-8 -*-
# @Author: lim
# @Email: lim1942@163.com
# @Date:  2018-01-30 09:36:10
# @Last Modified by:  lim
# @Last Modified time:  2018-01-30 10:49:15

import os
from PIL import Image, ImageFile


def letters(img):
	"""get the x location when img move in
	labels has the greatest match"""

	#load label img and binarization
	LABELS = Image.open('merge_label.jpg')
	LABELS = LABELS.convert('L')
	pix_ = LABELS.load()
	for y in range(LABELS.size[1]):
		for x in range(LABELS.size[0]):
			if  pix_[x,y]<=200:
				pix_[x,y] = 0
			if pix_[x,y]>230:
				pix_[x,y] =255

	A = img.load()
	B = LABELS.load()

	#move img in labels img get x 
	mx = 1000000
	max_x = 0
	x = 0
	for x in range(LABELS.size[0] - img.size[0]):
		_sum = 0
		for i in range(img.size[0]):
			for j in range(img.size[1]):
				_sum = _sum + abs(B[x + i, j] - A[i, j])
		if _sum < mx:
			mx = _sum
			max_x = x
	return max_x


def recognize(content):
	"""get a bytes img to recognize
	"""
	STR = '123456789aAbBcCdDeEfFgGQvXz'

	#laod img and convert it to L
	p = ImageFile.Parser()
	p.feed(content)
	im = p.close()
	im = im.convert('L')
	pix_ = im.load()

	#binarization and hand the interference line
	for y in range(im.size[1]):
		for x in range(im.size[0]):
			if pix_[x,y]<10:
				pix_[x,y] = 244
			if pix_[x,y]>=10 and pix_[x,y]<=230:
				pix_[x,y] = 0
			if pix_[x,y]>230:
				pix_[x,y] =255

	# hand noise remained by the line
	for y in range(im.size[1])[1:-1]:
		for x in range(im.size[0])[1:-1]:
			if pix_[x,y]==0:
				weight = 0 
				if pix_[x-1,y-1] !=0:
					weight +=1
				if pix_[x-1,y+1] !=0:
					weight +=1
				if pix_[x,y-1] !=0:
					weight +=1
				if pix_[x,y+1] !=0:
					weight +=1	
				if pix_[x+1,y-1] !=0:
					weight +=1
				if pix_[x+1,y+1] !=0:
					weight +=1
				if weight>4:
					pix_[x,y] =255

	#crop picture in the vertical direction
	box = (0,10,150,28)
	im = im.crop(box)

	#crop the piece of char to recognize in labels
	result = ''
	pix_ = im.load()
	x = 22
	for i in range(5):
		box = (x,0,x+18,18)
		x +=21
		img = im.crop(box)
		r_x = letters(img)
		result +=STR[r_x//18]

	return result


if __name__ == '__main__':
	with open('test.jpg','rb') as f:
		content = f.read()
	print recognize(content)