# -*- coding:utf-8 -*-
from PIL import Image
import struct
import os


def read_image(filename):
    f = open(filename, 'rb')
    index = 0
    buf = f.read()
    f.close()

    magic, images, rows, columns = struct.unpack_from('>IIII', buf, index)
    index += struct.calcsize('>IIII')

    for i in xrange(images):
        image = Image.new('L', (columns, rows))

        for x in xrange(rows):
            for y in xrange(columns):
                image.putpixel((y, x), int(struct.unpack_from('>B', buf, index)[0]))
                index += struct.calcsize('>B')

        print 'save ' + str(i) + ' image'
        image.save('mnist_image/' + str(i) + '.png')


def read_label(filename, savefile):
    f = open(filename, 'rb')
    index = 0
    buf = f.read()
    f.close()

    magic, labels = struct.unpack_from('>II', buf, index)
    index += struct.calcsize('>II')

    label_arr = [0] * labels

    for x in xrange(labels):
        label_arr[x] = int(struct.unpack_from('>B', buf, index)[0])
        index += struct.calcsize('>B')

    save = open(savefile, 'w')

    save.write(','.join(map(lambda x: str(x), label_arr)))
    save.write('\n')

    save.close()
    print 'save labels success'


if __name__ == '__main__':
    if not os.path.exists('mnist_image'):
        os.mkdir('mnist_image')

    read_image('t10k-images-idx3-ubyte')
    read_label('t10k-labels-idx1-ubyte', 'label.txt')

