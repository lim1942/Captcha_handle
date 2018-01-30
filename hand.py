# -*- coding: utf-8 -*-
# @Author: lim
# @Email: lim1942@163.com
# @Date:  2018-01-29 16:54:15
# @Last Modified by:  lim
# @Last Modified time:  2018-01-30 10:49:35

import os
from PIL import Image


def img_hand(path):
	"""get char piece and save them"""

	labels = path.replace('dateset\\','').replace('.jpg','')

	#convert to L
	im = Image.open(path)
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

	# crop and get piece of char
	x = 22
	pix_ = im.load()
	print labels
	for i in labels:
		print i
		if i.isupper():
			i+=i
		box = (x,0,x+18,18)
		img = im.crop(box)
		name = i+'.jpg'
		name = os.path.join('labels',name)
		img.save(name)
		x +=21


def get_label():
	"""get different char piece by dateset and save them"""
	PATH = 'dateset'
	for root,dirs,files in os.walk(PATH):
		for file in files:
			path = os.path.join(PATH,file)
			img_hand(path)


def merge_label():
	"""merge every piece of char img"""
	PATH = 'labels'
	x =0
	imgs = []
	for root,dirs,files in os.walk(PATH):
		for file in files:
			path = os.path.join(PATH,file)
			imgs.append(Image.open(path))

	new_img = Image.new('L', (486, 18), (255))
	for i in imgs:
		new_img.paste(i, (x, 0))
		x+=18
	new_img.save('merge_labels.jpg')


if __name__ == '__main__':
	merge_label()
