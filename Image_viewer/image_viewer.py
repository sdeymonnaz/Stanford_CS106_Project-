# image_viewer.py

"""This program shows a window to load an image and display several
buttons to applied filters to it. The user interface was developed with
library PySimpleGUI and image processing with Pillow"""

'''All five necessary libraries are imported'''
import io
import os
import PySimpleGUI as sg
from PIL import Image, ImageOps
import random

'''Constants MIN and MAX SCALE are first declared to set the limits to
RGB colors change for the get_color function'''
MIN_SCALE = 0
MAX_SCALE = 1.5

'''The PYSimpleGUI user interface is created using a red theme and setting
the compatible file types to PNG, JPEG, TIFF, BMP, and GIFF. Then the program
window is created with a space to display the selected image and several
buttons below to activate the filters. The window title is set to "Image Fun
Processor"(?)'''
sg.theme('DarkRed')

file_types = [("JPEG (*.jpg)", "*.jpg"),
            ("PNG (*.png)", "*.png"),
            ("TIFF (*.tiff)", "*.tiff"),
            ("BMP (*.bmp)", "*.bmp"),
            ("GIF (*.gif)", "*.gif"),
            ("All files (*.*)", "*.*")]


def main():
    layout = [
        [sg.Image(key="-IMAGE-")],
        [
            sg.Text("Image File"),
            sg.Input(size=(25, 1), key="-FILE-"),
            sg.FileBrowse(file_types=file_types),
            sg.Button("Original Image"),
        ],
        [
            sg.Button("B&W"),
            sg.Button("Code in Place Filter"),
            sg.Button("House Filter"),
            sg.Button("Random Filter"),
            sg.Button("Exit")
        ],
    ]
    window = sg.Window("Image Fun Processor", layout)

    '''A while loop is initiated to handle the flow control. The loop will
    break if the windows is closed or the exit button is clicked on.
    There are five buttons to execute:
    -Original image will show the image as it is.
    -B&W converts the image to grayscale using the pillow built-in function
    -Random filter will chose a random RGB combination to each individual
    pixel and merge them in a new image.
    -Code in Place filter is the brand filter explained in the 2021 CS106
    Stanford course.
    -House filter is my own selection of colors to process images.
    -Exit will close the program.
    '''
    while True:
        event, values = window.read()
        filename = values["-FILE-"]

        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        if event == "Original Image":
            loaded_image = get_image(filename, values)
            show_image(loaded_image, window)

        if event == "B&W":
            loaded_image = get_image(filename, values)
            image_bw = ImageOps.grayscale(loaded_image)
            show_image(image_bw, window)

        if event == "Random Filter":
            loaded_image = get_image(filename, values)
            color = get_color()
            image = loaded_image.convert("RGB")
            r, g, b = image.split()
            r = r.point(lambda i: i * color[0])
            g = g.point(lambda i: i * color[1])
            b = b.point(lambda i: i * color[2])
            image_comb = Image.merge('RGB', (r, g, b))
            show_image(image_comb, window)

        if event == "Code in Place Filter":
            loaded_image = get_image(filename, values)
            image = loaded_image.convert("RGB")
            r, g, b = image.split()
            r = r.point(lambda i: i * 1.5)
            g = g.point(lambda i: i * 0.7)
            b = b.point(lambda i: i * 1.5)
            image_comb = Image.merge('RGB', (r, g, b))
            show_image(image_comb, window)

        if event == "House Filter":
            loaded_image = get_image(filename, values)
            image = loaded_image.convert("RGB")
            r, g, b = image.split()
            r = r.point(lambda i: i * 1.1)
            g = g.point(lambda i: i * 0.9)
            b = b.point(lambda i: i * 0.5)
            image_comb = Image.merge('RGB', (r, g, b))
            show_image(image_comb, window)

    window.close()


'''Function get_image loads the picture and change its format to
thumbnail 400x400 pixels to streamline the processing time'''


def get_image(filename, values):
    if os.path.exists(filename):
        image = Image.open(values["-FILE-"])
        image.thumbnail((400, 400))
        return image


'''Function show_image receives an image, original or processed, 
save in memory and display it in the program window'''


def show_image(image_received, window):
    bio = io.BytesIO()
    image_received.save(bio, format="PNG")
    window["-IMAGE-"].update(data=bio.getvalue())


''''Function get_color returns a tuple with three number scales to
apply to each RGB pixel value in the Random Filter event.'''


def get_color():
    red_scale = random.uniform(MIN_SCALE, MAX_SCALE)
    green_scale = random.uniform(MIN_SCALE, MAX_SCALE)
    blue_scale = random.uniform(MIN_SCALE, MAX_SCALE)
    return red_scale, green_scale, blue_scale


if __name__ == "__main__":
    main()
