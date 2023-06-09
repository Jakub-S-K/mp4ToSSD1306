import numpy as np
import cv2
import sys
import os

file_format = ".png"
base_file_name = "slideshow_kumo"

def main():
    os.chdir("vid")
    file_list = []
    for root, dirs, files in os.walk(".", topdown=True):
        for file in files:
            if file[-(len(file_format)):] == file_format:
                trimmed = file[:-(len(file_format))]
                if not trimmed.find(base_file_name):
                    file_list.append([trimmed[:len(base_file_name)], int(trimmed[len(base_file_name):])])

    file_list.sort(key=lambda a : a[1])
    wyjscie = open("../" + base_file_name + ".h", "w+")
    print_begin(wyjscie, base_file_name+"_multiple")
    wyjscie.write("\n" + str(hex(len(file_list))) + ", //IMG CNT")
    for file in file_list:
        part = horizontally_segments(file[0] + str(file[1]) + file_format)
        print_body(wyjscie, part)
    print_end(wyjscie)
    wyjscie.close()

def horizontally_segments(file):
    img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)

    buffer = []
    counter = 1
    byte = 0

    for y in range(int(img.shape[0]/8)):
        for x in range(int(img.shape[1]/8)):
            for y_i in range(8):
                for x_i in range(8):
                    if img[y*8 + x_i][x*8 + y_i]:
                        byte |= 1

                    if counter % 8 == 0:
                        inverted_byte = 0
                        for baka in range(8):
                            inverted_byte |= ((1 & (byte >> baka)) << 7 - baka)

                        buffer.append(inverted_byte)
                        byte = 0
                    else:
                        byte <<= 1

                    counter += 1

    return (buffer)

def vertically():
    img = cv2.imread("vid/test0.png", cv2.IMREAD_GRAYSCALE)

    cv2.imshow("test", img)
    buffer = []
    counter = 1
    byte = 0

    print(img.shape)

    for y in range(int(img.shape[0]/8)):
        for x in range(img.shape[1]):
            for i in range(8):
                if img[y + i][x]:
                    byte |= 1

                if counter % 8 == 0:
                    buffer.append(byte)
                    byte = 0
                else:
                    byte <<= 1

                counter += 1

    print_to_header(buffer, "test")

def horizontally():
    img = cv2.imread("vid/test0.0.png", cv2.IMREAD_GRAYSCALE)

    cv2.imshow("test", img)
    buffer = []
    counter = 1
    byte = 0

    print(img.shape)

    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            if img[y][x]:
                byte |= 1

            if counter % 8 == 0:
                buffer.append(byte)
                byte = 0
            else:
                byte <<= 1

            counter += 1

    print_to_header(buffer, "test")



def horizontally():
    img = cv2.imread("vid/test0.0.png", cv2.IMREAD_GRAYSCALE)

    cv2.imshow("test", img)
    buffer = []
    counter = 1
    byte = 0

    print(img.shape)

    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            if img[y][x]:
                byte |= 1

            if counter % 8 == 0:
                buffer.append(byte)
                byte = 0
            else:
                byte <<= 1

            counter += 1

    print_to_header(buffer, "test")


def multi_print(buf, name):
    pass

def print_to_header(buf, name):
    print("const unsigned char " + name + " [] = {")
    print("0x40,") #DATA COMMAND
    print_body(buf)
    sys.stdout.write("\b\b \n")
    sys.stdout.write("};")
    #print("")

def print_begin(file, name):
    file.write("const unsigned char " + name + " [] = {")

def print_end(file):
    file.seek(file.tell() - 7, os.SEEK_SET)
    file.truncate()
    file.write("\n};")

def print_body(file, buf):
    file.write("\n0x40, //DATA COMMAND\n") #DATA COMMAND
    cnt = -15
    for x in buf:
        if cnt % 16 == 1 and cnt > 0:
            file.write("\n")
        
        file.write(hex(x) +", ")
        cnt += 1

def append_body(buf):
    cnt = -15
    for x in buf:
        if cnt % 16 == 1 and cnt > 0:
            buf.append("\n")
        
        buf.append((hex(x) + ", "))
        cnt += 1



if __name__ == '__main__':
    main()