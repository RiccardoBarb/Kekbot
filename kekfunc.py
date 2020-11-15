import urllib.request
from PIL import Image, ImageOps, ImageFilter
import numpy as np


# unicode values of each dot in the 2X4 matrix for braille encoding
# (https://github.com/asciimoo/drawille/blob/master/drawille.py)
pixel_map = np.array([[0x01, 0x08], [0x02, 0x10], [0x04, 0x20], [0x40, 0x80]])

# braille unicode characters starts at 0x2800
braille_char_offset = 0x2800

# sizes
height = 15
width = 30
step_size_x = 2
step_size_y = 4


def build_pixel_matrix(img):
    # convert in luminance and alpha channels (grayscale with preserved background from certain png)
    img = img.convert('LA')
    # We have to hard code the size of the image, otherwise it won't properly display on twitch chat.
    # The length of a line is 35 and the character limit is 500. Line of 30 seems acceptable for multiple screen sizes.
    # We also multiply the width by 2 and the height by 4, as 2X4 is the shape of the grid used for braille conversion.
    new_width = width * step_size_x
    new_height = height * step_size_y
    img = img.resize((new_width, new_height), Image.ANTIALIAS)  # We resize the image
    # After several tests this seems to be the best set of enhancement for most of twitch emotes: first
    # we get rid of the alpha channel, and compress the details of the image by applying posterization.
    # We also equalize the image to better visualize dark pictures.
    # This procedures might leave some noise which we remove with a median filter.
    # Finally we enhance the edge and sharpness of the filtered image, apply some smoothing and enhance the details.
    # The result is not always perfect but it works for most twitch and BTTV emotes at the current resolution.
    img = img.convert('L')
    img = ImageOps.posterize(img, bits=6)
    img = ImageOps.equalize(img)
    # prepare filters
    median_filter = ImageFilter.MedianFilter(3)
    edge_enhance = ImageFilter.EDGE_ENHANCE_MORE()
    sharpness_filter = ImageFilter.SHARPEN()
    smooth_filter = ImageFilter.SMOOTH()
    detail_filter = ImageFilter.DETAIL()
    # apply filters
    img = img.filter(median_filter)
    img = img.filter(edge_enhance)
    img = img.filter(smooth_filter)
    img = img.filter(sharpness_filter)
    img = img.filter(detail_filter)
    # Build pixel matrix with luminance values
    enhanced_pixel_matrix = [[img.getpixel((x, y)) for x in range(img.width)] for y in range(img.height)]
    # Treat the pixel matrix as a numpy array so we can easily apply transformations to braille
    npixel_matrix = np.array(enhanced_pixel_matrix)

    return npixel_matrix


def convert_to_braille(pixel_matrix, threshold, mode):
    real_height = np.shape(pixel_matrix)[0]
    real_width = np.shape(pixel_matrix)[1]
    converted_mat = []
    # this is where the conversion happens. We use a 2X4 pixels window to map a combination of 8 pixels to the
    # corresponding braille character
    for pix_y in range(0, real_height, step_size_y):
        for pix_x in range(0, real_width, step_size_x):

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
            converted_mat.extend(chr(braille_char_offset + int(char_value.sum())))

    return converted_mat


def handle_request(command_and_link, emotes):
    try:
        # if the request is triggered by a command
        if ('!kek' in command_and_link) & (not emotes.is_url(command_and_link)):
            requested_command = command_and_link[0:9]
            image_reference = command_and_link[9::]
            emotes.reference = image_reference
            image_link = emotes.retrieve_emote()
            req = urllib.request.Request(image_link, headers={'User-Agent': 'Mozilla/5.0'})
            image = Image.open(urllib.request.urlopen(req))
            pixel_matrix = build_pixel_matrix(image)
            reshaped_mat = [chr(braille_char_offset) * width]
            # positive gradient
            if requested_command == '!kekthis ':
                braille_matrix = convert_to_braille(pixel_matrix, threshold=145, mode='pos')
                for r in range(0, len(braille_matrix), width):
                    reshaped_mat.append("".join(braille_matrix[r:r + width]))

            # negative gradient
            elif requested_command == '!kekthat ':
                braille_matrix = convert_to_braille(pixel_matrix, threshold=145, mode='neg')
                for r in range(0, len(braille_matrix), width):
                    reshaped_mat.append("".join(braille_matrix[r:r + width]))
        else:
            # if the request is triggered by a reward without a command we set positive gradient
            image_reference = command_and_link
            emotes.reference = image_reference
            image_link = emotes.retrieve_emote()
            req = urllib.request.Request(image_link, headers={'User-Agent': 'Mozilla/5.0'})
            image = Image.open(urllib.request.urlopen(req))
            pixel_matrix = build_pixel_matrix(image)
            reshaped_mat = [chr(braille_char_offset) * width]
            braille_matrix = convert_to_braille(pixel_matrix, threshold=145, mode='pos')
            for r in range(0, len(braille_matrix), width):
                reshaped_mat.append("".join(braille_matrix[r:r + width]))

        return "\n".join(reshaped_mat)

    except Exception:
        return "".join("MrDestructoid Something went wrong MrDestructoid, cannot process that")
