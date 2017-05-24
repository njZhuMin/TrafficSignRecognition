# -*- coding:utf-8 -*-
import json
import pylab as pl
import anno_func
# import random
# import numpy as np
# import cv2


def select_label():
    """
    Read annotations from TT100K
    Select labels beginning with 'pl*','ph*','pw*'
    Generate new annotations.json for selected image
    :return: null
    """
    datadir = '/media/silverlining/FAF2924BF2920BCF/TT100K/data'
    filedir = 'annotations.json'
    ids = open('ids.txt').read().splitlines()

    # modify attribute types
    annos = json.loads(open(filedir).read())
    types = []
    for type in annos['types']:
        if type[0:2] == 'pl' or type[0:2] == 'ph' or type[0:2] == 'pw':
            types.append(type)
    annos['types'] = types

    file_out = open('categories.json', 'w')
    for id in ids:
        anno = annos['imgs'][id]
        objects = anno['objects']
        if objects:
            my_objects = []
            for object in objects:
                category = object['category']
                if category[0:2] == 'pl' or category[0:2] == 'ph' or category[0:2] == 'pw':
                    # object['category'] = 'none'
                    my_objects.append(object)
            if my_objects:
                anno['objects'] = my_objects

    file_out.write('{"imgs":')
    file_out.write(json.dumps(annos['imgs']))
    file_out.write(',"types":')
    file_out.write(json.dumps(annos['types']))
    file_out.write('}')
    file_out.close()


# imgid = random.sample(ids, 1)[0]
# print annos['imgs'][imgid]

def draw_pic(annos, datadir, imgid):
    """
    Draw boundary by annotation, function call of anno_func.py
    Library pylab is required
    :param annos: annotation of region
    :param datadir: image directory
    :param imgid: image id
    :return: null
    """
    imgdata = anno_func.load_img(annos, datadir, imgid)
    imgdata_draw = anno_func.draw_all(annos, datadir, imgid, imgdata)
    pl.figure(figsize=(20, 20))
    pl.imshow(imgdata_draw)
    pl.show()


def remove_pic():
    annos1 = json.loads(open('annotations.json').read())
    annos2 = json.loads(open('categories.json').read())
    images1 = annos1['imgs']
    images2 = annos2['imgs']

    img_ids1 = []
    img_ids2 = []
    for image in images1:
        img_ids1.append(image)

    for image in images2:
        img_ids2.append(image)

    for id in img_ids2:
        if id not in img_ids1:
            print id


if __name__ == '__main__':
    select_label()
    # remove_pic()
