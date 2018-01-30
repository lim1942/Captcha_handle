#author:lim
#Email: lim1942@163.com

https://github.com/lim1942/captcha_hand/blob/master/dataset/39baB.jpg

基于python2.7利用pillow进行的验证码识别。
#use pillow in python2.7 to recognize captcha
因为验证码规整，故使用滑动法进行识别。 
#Because the pictures are neat,use sliding method to recognize.
hand.py 处理数据集验证码，得到用于识别的merge_labels.jpg 模板
#hand.py hand the dataset to get a long (merge_labels.jpg) letter template
recognize.py 进行验证码识别的模块。
#recognize.py hand captcha and recognize it
