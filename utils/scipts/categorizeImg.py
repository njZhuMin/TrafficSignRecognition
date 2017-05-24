# -*- coding:utf-8 -*-
import json
from PIL import Image
global base_path
base_path = '/media/silverlining/FAF2924BF2920BCF/TT100K/data/'


def parse_json(filename, filesave):
    f_open = open(filename, 'r')
    buf = f_open.read()
    f_open.close()

    f_save = open(filesave, 'w')
    anno = json.loads(buf)
    imgs = anno['imgs']
    types = anno['types']

    json_out = ''
    json_out += '{"imgs":{'
    # f_save.write('{"imgs":{')

    for index in imgs:
        objects = imgs[index]['objects']
        if objects:
            for object in objects:
                category = object['category']
                myobjects = []
                if category[0:2] == 'ph' or category[0:2] == 'pl' or category[0:2] == 'pm':
                    myobjects.append(object)

            imgs[index]['objects'] = myobjects
            json_out = json_out + '"' + index + '":'
            json_out = json_out + json.dumps(imgs[index])
            json_out += ','

            # f_save.write('"' + index + '":')
            # f_save.write(json.dumps(imgs[index]))
            # f_save.write(',')
    json_out = json_out[:-1]
    json_out += '},"types":['

    for type in types:
        if type[0:2] == 'ph' or type[0:2] == 'pl' or type[0:2] == 'pm':
            json_out = json_out + '"' + type + '",'
            # f_save.write('"' + type + '",')

    json_out = json_out[:-1]
    json_out += ']}'
    f_save.write(json_out)
    # f_save.write(']}')
    f_save.close()


def get_crop(filename):
    f_open = open(filename, 'r')
    buf = f_open.read()
    f_open.close()

    anno = json.loads(buf)
    imgs = anno['imgs']

    for index in imgs:
        objects = imgs[index]['objects']
        if objects:
            for object in objects:
                category = object['category']
                if category[0:2] == 'ph' or category[0:2] == 'pl' or category[0:2] == 'pm':
                    img_path = imgs[index]['path']
                    abs_path = base_path + img_path
                    im = Image.open(abs_path)
                    im_crop = im.crop((object['bbox']['xmin'], object['bbox']['ymin'], object['bbox']['xmax'], object['bbox']['ymax']))
                    out_filename = 'crop/' + img_path.split('/')[0] + '/' + category + '_' + index + '.jpg'
                    im_crop.save(out_filename)


def add_mask(filename, filesave):
    f_open = open(filename, 'r')
    buf = f_open.read()
    f_open.close()
    f_save = open(filesave, 'w')

    anno = json.loads(buf)
    imgs = anno['imgs']
    types = anno['types']
    mask_types = ["rain", "snow", "fog"]
    mask_alpha = {"rain": 0.5, "fog": 0.75, "snow": 0.5}
    aug_images = {}

    offset = 0
    for index in imgs:
        objects = imgs[index]['objects']
        if objects:
            for object in objects:
                category = object['category']
                if category[0:2] == 'ph' or category[0:2] == 'pl' or category[0:2] == 'pm':
                    for mask_type in mask_types:
                        img_path = imgs[index]['path']
                        abs_path = base_path + img_path
                        mask_path = base_path + '/mask/' + mask_type + '.png'
                        ''' mask image '''
                        src_img = Image.open(abs_path).convert('RGBA')
                        mask_img = Image.open(mask_path).resize(src_img.size).convert('RGBA')
                        im = Image.blend(src_img, mask_img, mask_alpha[mask_type])

                        out_file = base_path + img_path.split('/')[0] + '/' + index + \
                                        '_' + mask_type + '.jpg'
                        im.save(out_file)

                        ''' vvvvvvvvvvvv NOT USED : mask traffic sign only vvvvvvvvvvvv '''
                        # mask_img = Image.open(mask_path + 'fog.png')
                        # mask_width = int(object['bbox']['xmax'] - object['bbox']['xmin'])
                        # mask_height = int(object['bbox']['ymax'] - object['bbox']['ymin'])
                        # mask_x, mask_y = int(object['bbox']['xmin']), int(object['bbox']['ymin'])
                        # mask_img = Image.open('rain.png').resize((mask_width, mask_height)).convert('RGBA')
                        # src_img.paste(mask_img, (mask_x, mask_y), mask=mask_img)
                        ''' ^^^^^^^^^^^^ NOT USED : mask traffic sign only ^^^^^^^^^^^^ '''

                        ''' augment json annotations '''
                        aug_images.setdefault(100000+offset, {})
                        aug_images[100000+offset]['path'] = img_path.split('/')[0] + '/' + index + \
                                        '_' + mask_type + '.jpg'
                        aug_images[100000+offset]['id'] = 100000 + offset
                        aug_images[100000+offset]['objects'] = imgs[index]['objects']
                        # print img_path
                        print aug_images[100000+offset]
                        offset += 1

    imgMerged = dict(imgs, **aug_images)
    json_out = ''
    json_out += '{"imgs":{'

    for index in imgMerged:
        json_out = json_out + '"' + str(index) + '":'
        json_out = json_out + json.dumps(imgMerged[index])
        json_out += ','

    json_out = json_out[:-1]
    json_out += '},"types":['

    for type in types:
        json_out = json_out + '"' + type + '",'

    json_out = json_out[:-1]
    json_out += ']}'
    f_save.write(json_out)
    f_save.close()


def count_categories(filename):
    f_open = open(filename, 'r')
    buf = f_open.read()
    f_open.close()

    anno = json.loads(buf)
    imgs = anno['imgs']

    count = {}
    for index in imgs:
        objects = imgs[index]['objects']
        if objects:
            for object in objects:
                category = object['category']
                if category[0:2] == 'ph' or category[0:2] == 'pl' or category[0:2] == 'pm':
                    if not count.has_key(category[0:2]):
                        count[category[0:2]] = 1
                    else:
                        count[category[0:2]] += 1

                    if not count.has_key(category):
                        count[category] = 1
                    else:
                        count[category] += 1

    # for key in count.keys():
    #     print key, count[key]

    print count['pl'], count['ph'], count['pm']


if __name__ == '__main__':
    # get_crop('annotations.json')
    # parse_json('annotations.json', 'annos.json')
    # count_categories('annotations.json')
    add_mask('annos.json', 'aug_annotations.json')

    # image1 = Image.open('1967.jpg').convert("RGBA")
    # image2 = Image.open('rain.png').resize(image1.size).convert("RGBA")
    # image3 = Image.open('fog.png').resize(image1.size).convert("RGBA")
    # image4 = Image.open('snow.png').resize(image1.size).convert("RGBA")
    #
    # im1 = Image.blend(image1, image2, 0.5)
    # im1.save('rain_1967.jpg')
    # im2 = Image.blend(image1, image3, 0.75)
    # im2.save('fog_1967.jpg')
    # im3 = Image.blend(image1, image4, 0.5)
    # im3.save('snow_1967.jpg')
