import urllib.request
from PIL import Image
import numpy as np

ASCII_CHARS = "⠿⠽⠛⠮⠭⠗⠕⠚⠇⠃⠌⠁⠂⠄"


def build_pixel_matrix(image):
    # convert in luminance channel (grayscale)
    image = image.convert('L')
    # we have to hard code the size of the image, otherwise it won't properly display on twitch chat
    # an alternative could be int(image.size[0] / image.size[1] * MAX_WIDTH) to maintain the aspect ratio, but it won't
    # work in most cases
    new_width = 35
    new_height = 14
    image = image.resize((new_width, new_height), Image.ANTIALIAS)  # We resize the image

    # Build pixel matrix by luminance values
    original_pixel_matrix = [[image.getpixel((x, y)) for x in range(image.width)] for y in range(image.height)]

    # Treat the pixel matrix as a numpy array so we can apply contrast enhancement
    npixel_matrix = np.array(original_pixel_matrix)

    # Get brightness range
    min_pix = np.min(npixel_matrix)
    max_pix = np.max(npixel_matrix)

    # Make a Look-Up Table to translate image values
    lut = np.zeros(256, dtype=np.uint8)
    lut[min_pix:max_pix + 1] = np.linspace(start=0, stop=255, num=(max_pix - min_pix) + 1, endpoint=True,
                                           dtype=np.uint8)

    pixel_matrix = lut[npixel_matrix]

    return pixel_matrix


def convert_to_ascii(pixel_matrix):
    # We map the luminance of each pixel in the matrix to the corresponding ascii
    ascii_matrix = []
    for row in pixel_matrix:
        ascii_row = []

        for pixel in row:
            ascii_row.append(ASCII_CHARS[int((len(ASCII_CHARS) - 1) * (pixel / 255))])

        ascii_matrix.append(ascii_row)

    return ascii_matrix


def handle_request(image_link):
    try:
        req = urllib.request.Request(image_link, headers={'User-Agent': 'Mozilla/5.0'})
        image = Image.open(urllib.request.urlopen(req))
        pixel_matrix = build_pixel_matrix(image)
        ascii_matrix = convert_to_ascii(pixel_matrix)
        flatten_matrix = [pixel for row in ascii_matrix for pixel in row]

    except Exception:
        raise SystemExit(f"The url does not refer to a picture!")

    return "".join(flatten_matrix)
