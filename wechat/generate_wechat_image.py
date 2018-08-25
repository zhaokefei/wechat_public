# -*- coding:utf-8 -*-

import re
import os
import math
import uuid

import itchat
from PIL import Image


class GenerateWechatImage(object):

    def __init__(self):
        self.uuid = None
        self.qrcode = None

    def try_login(self):
        itchat.auto_login(qrCallback=self.login_qrcode_callback,
                          loginCallback=self.get_friend_imgs)

    def login_qrcode_callback(self, uuid, status, qrcode):
        file_name = uuid + '.jpg'
        f = open(file_name, 'wb')
        f.write(qrcode)
        read_file = f.read()
        self.qrcode = read_file
        self.uuid = uuid

    def get_friend_imgs(self, get_img_nums=100):
        save_path = self.uuid
        if os.path.exists(save_path):
            save_path = input(u'该路径已存在，请输入其他目录路径: ')
        os.mkdir(save_path)
        friends = itchat.get_friends()
        if get_img_nums > len(friends):
            get_img_nums = len(friends)
            print(u'需要获取的图片数量大于好友数量，取好友数量： %s' % len(friends))
        for num, friend in enumerate(friends):
            friend_name = friend['NickName'] or friend['UserName']
            friend_name = re.sub(r'[\s+]', '_', friend_name)
            friend_img = itchat.get_head_img(userName=friend['UserName'])
            with open(save_path + '/' + friend_name + str(num+1).zfill(3) + '.jpg', 'wb') as f:
                print(u'正在写入 %s 的图像, 还要写入 %s 个' % (friend_name, get_img_nums-num))
                f.write(friend_img)
            if num > get_img_nums:
                print(u'%s 个图片写入完毕' % get_img_nums)
                break
        self.generate_image(self.uuid)

    def generate_image(self, path, gen_filename='multi_img'):
        images = os.listdir(path)
        row_num = int(math.sqrt(len(images)))
        slide_size = int(640/row_num)
        thum_size = (slide_size, slide_size)
        toImage = Image.new('RGBA', (640, 640))
        x = 0; y = 0
        invilid_imgs = []
        for num, img in enumerate(images):
            if img.endswith('.jpg'):
                print(u'写入第 {} 个图片; 图片名为: {}'.format(num, img))
                img = path + '/' + img
                try:
                    im = Image.open(img)
                except OSError:
                    print(u'%s 未写入' % img)
                    invilid_imgs.append(img)
                    continue
                if im.size != thum_size:
                    thum_im = im.resize(thum_size, Image.ANTIALIAS)
                else:
                    thum_im = im
                toImage.paste(thum_im, (x * slide_size, y * slide_size))
                x += 1
                if x == row_num:
                    x = 0
                    y += 1
        print(u'未写入的图片有: {}'.format(' @|@ '.join(invilid_imgs)))
        toImage.save(path + '/' + gen_filename + '.jpg')
        print(u'生成的文件位于: {}; 名为: {}'.format(path, gen_filename + '.jpg'))

