import urllib.request
from PIL import Image
import numpy as np
from PIL import ImageOps
from matplotlib import pyplot as plt
# unicode values of each dot in the 2X4 matrix for braille encoding
# (https://github.com/asciimoo/drawille/blob/master/drawille.py)
pixel_map = np.array([[0x01, 0x08], [0x02, 0x10], [0x04, 0x20], [0x40, 0x80]])

# braille unicode characters starts at 0x2800
braille_char_offset = 0x2800


def build_pixel_matrix(img):
    # convert in luminance channel (grayscale)
    img = img.convert('L')
    # We have to hard code the size of the image, otherwise it won't properly display on twitch chat.
    # The length of a line is 35 and the character limit is 500.
    # We also multiply the width by 2 and the height by 4, as 2X4 is the shape of the grid used for braille conversion.
    new_width = 35 * 2
    new_height = 14 * 4
    plt.figure()
    img = img.resize((new_width, new_height), Image.ANTIALIAS)  # We resize the image
    # after several tests this seems to be the best enhancement for most of twitch emotes
    img=ImageOps.autocontrast(img, cutoff=0.1)


    # Build pixel matrix by luminance values
    enhanced_pixel_matrix = [[img.getpixel((x, y)) for x in range(img.width)] for y in range(img.height)]
    # Treat the pixel matrix as a numpy array so we can easily appy trasformations to braille
    npixel_matrix = np.array(enhanced_pixel_matrix)

    return npixel_matrix


def convert_to_braille(pixel_matrix, threshold, mode):
    height = np.shape(pixel_matrix)[0]
    width = np.shape(pixel_matrix)[1]
    step_size_x = 2
    step_size_y = 4
    converted_mat = []
    # this is where the conversion happens. We use a 2X4 pixels window to map a combination of 8 pixels to the
    # corresponding braille character
    for pix_y in range(0, height, step_size_y):
        for pix_x in range(0, width, step_size_x):

            current_window = pixel_matrix[pix_y:pix_y + step_size_y, pix_x:pix_x + step_size_x]
            if mode == 'pos':
                index_to_map = np.argwhere(current_window > threshold)
            elif mode == 'neg':
                index_to_map = np.argwhere(current_window < threshold)

            char_value = np.zeros(8)
            id_val = 0
            for row in index_to_map:
                char_value[id_val] = pixel_map[row[0], row[1]]
                id_val += 1
            converted_mat.append(chr(braille_char_offset + int(char_value.sum())))

    return converted_mat


def handle_request(command_and_link):
    try:
        requested_command = command_and_link[0:9]
        image_link = command_and_link[9::]
        req = urllib.request.Request(image_link, headers={'User-Agent': 'Mozilla/5.0'})
        image = Image.open(urllib.request.urlopen(req))
        pixel_matrix = build_pixel_matrix(image)
        # positive gradient
        if requested_command == '!kekthis ':
            braille_matrix = convert_to_braille(pixel_matrix, threshold=145, mode='pos')

        # negative gradient
        elif requested_command == '!kekthat ':
            braille_matrix = convert_to_braille(pixel_matrix, threshold=145, mode='neg')

        return "".join(braille_matrix)

    except Exception:
        return "".join("MrDestructoid Something went wrong MrDestructoid, I cannot process that link")
