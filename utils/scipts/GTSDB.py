# -*- coding:utf-8 -*-
import os
import Image
import csv


def trans_pic(arg, dirname, filename):
    """
    This function transfer ppm format to png
    :param arg: pass to os.path.walk()
    :param dirname: directory of images
    :param filename: image file name
    :return: null
    """
    for filename in os.listdir(dirname):
        filepath = os.path.join(dirname, filename)
        # ppm format
        if not os.path.isdir(filepath) and filepath[-3:] == 'ppm':
            # use Image lib to save as png format
            img = Image.open(filepath)
            fname = filepath[:-4]
            img.save(fname + '.png')
            os.remove(fname + '.ppm')


def delete_pic():
    """
    Given a list, delete non-selected images according to path
    :return: null
    """
    files = set()
    for i in range(0, 600):
        # image name from '00000' to '00599'
        files.add(str(i).zfill(5))

    gt_file = open('gt.txt', 'rb')
    gt_content = gt_file.read().splitlines()
    for line in gt_content:
        file_name = line.split(',')[0][:-4]
        if file_name in files:
            # if image selected, remove from path set
            files.remove(file_name)
    gt_file.close()

    for fname in files:
        # do delete iteratively
        os.remove(fname + '.png')

        
def classify_pic():
    """
    Select labels beginning with 'pl*','ph*','pw*'
    and generate new list of labels
    :return: null
    """
    labels = {}
    label_file = open('labels.txt', 'rb')
    label_content = label_file.read().splitlines()
    for label in label_content:
        # create mapping
        labels[int(label.split(':')[0])] = label.split(':')[1]
    label_file.close()

    annos = []
    gt_file = open('gt.txt', 'rb')
    gt_content = gt_file.read().splitlines()
    for line in gt_content:
        # assemble file name
        file_name = line.split(';')[0][:-4] + '.png'
        clazz = line.split(';')[-1]
        new_line = []
        if int(clazz) in labels.keys():
            new_line.append(file_name)
            for index in range(1, 5):
                new_line.append(line.split(';')[index])
            new_line.append(labels[int(clazz)])
        if new_line:
            # add selected file path and label
            annos.append(','.join(new_line))
    gt_file.close()

    # output file
    gt_file = open('gt.txt', 'w')
    for anno in annos:
        gt_file.write(anno + '\n')
    gt_file.close()


def alter_csv(arg, dirname, filename):
    """
    NOT USED: alter csv annotations in GTSRB
    :param arg: pass to os.path.walk()
    :param dirname: directory of images
    :param filename: image file name
    :return: null
    """
    for filename in os.listdir(dirname):
        filepath = os.path.join(dirname, filename)

        if not os.path.isdir(filepath) and filepath[-3:] == 'csv':
            with open(filepath, 'rb') as csvfile:
                content = []
                spamreader = csv.DictReader(csvfile, delimiter=',')
                for row in spamreader:
                    row['Filename'] = row['Filename'][:-4] + '.png'
            
                    labels = {}

                    f_label = open('labels.txt', 'rb')
                    lines = f_label.read().splitlines()
                    for line in lines:
                        path = line.split(':')[0]
                        id = line.split(':')[1]
                        labels[path] = id
                        if filepath.split('/')[1] == path:
                            row['ClassId'] = labels[path]
                    f_label.close()

                    content.append(row)
            
            with open(filepath, 'w') as csvfile:
                fieldnames = ['Filename', 'Width', 'Height', 'Roi.X1', 'Roi.Y1', 'Roi.X2', 'Roi.Y2', 'ClassId']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for row in content:
                    writer.writerow(row)


if __name__ == '__main__':
    # os.path.walk('.', alter_csv, ())
    os.path.walk('.', trans_pic, ())
    classify_pic()
    delete_pic()
