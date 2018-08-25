# -*- coding:utf-8 -*-
from __future__ import unicode_literals

import os
import math

import itchat
import shutil
from PIL import Image


class GenerateWechatImage(object):

    def __init__(self, user_name):
        self.qrcode = None
        self.user_name = user_name

    def try_login(self):
        new_instance = itchat.new_instance()
        new_instance.auto_login(qrCallback=self.login_qrcode_callback,
                                loginCallback=self.get_friend_imgs)
        new_instance.run()

    def login_qrcode_callback(self, uuid, status, qrcode):
        file_name = self.user_name + '.jpg'
        with open(file_name, str('wb')) as f:
            f.write(qrcode)
        read_file = open(file_name, str('r+'))
        self.qrcode = read_file

    def get_friend_imgs(self, get_img_nums=100):
        save_path = self.user_name
        if os.path.exists(save_path):
            shutil.rmtree(save_path)
        os.makedirs(save_path)
        friends = itchat.get_friends()
        if get_img_nums > len(friends):
            get_img_nums = len(friends)
            # print('friend count： %s' % len(friends))
        for num, friend in enumerate(friends):
            friend_img = itchat.get_head_img(userName=friend['UserName'])
            with open(save_path + '/' + str(num+1).zfill(3) + '.jpg', str('wb')) as f:
                # print('still need to write %s' % (get_img_nums-num))
                f.write(friend_img)
            if num > get_img_nums:
                # print('%s has been writed done' % get_img_nums)
                break
        self.generate_image(save_path)

    def generate_image(self, path, gen_filename='multi_img'):
        images = os.listdir(path)
        row_num = int(math.sqrt(len(images)))
        if row_num == 0:
            row_num = 1
        slide_size = int(640/row_num)
        thum_size = (slide_size, slide_size)
        toImage = Image.new('RGB', (640, 640))
        x = 0; y = 0
        invilid_imgs = []
        for num, img in enumerate(images):
            if img.endswith('.jpg'):
                # print('write {} picture'.format(num))
                img = path + '/' + img
                try:
                    im = Image.open(img)
                except OSError:
                    # print('%s not write in' % img)
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
        toImage.save(path + '/' + gen_filename + '.jpg')
        # print('generator file: {}; name: {}'.format(path, gen_filename + '.jpg'))

