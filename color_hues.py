import colorsys
import random

## define color ranges
hue_options = {
#    'red1' : (0.9861, 1.0),
#    'red2' : (0.0, 0.0278),
#    'red_orange' : (0.0278, 0.0556),
    'orange_brown': (0.0556, 0.1111),
#    'orange_yellow' : (0.1111, 0.1389),
#    'yellow' : (0.1389, 0.1667),
    'yellow_green' : (0.1667, 0.2222),
#    'green' : (0.2222, 0.3889),
    'green_cyan' : (0.3889, 0.4694),
    'cyan' : (0.4694, 0.5556),
    'cyan_blue' : (0.5556, 0.6111),
#    'blue' : (0.6111, 0.6667),
#    'blue_magenta' : (0.6667, 0.7778),
#    'magenta' : (0.7778, 0.8889),
    'magenta_pink' : (0.8889, 0.9167),
    'pink' : (0.9167, 0.9583),
#    'pink_red' : (0.9583, 0.9861),
#    'random' : (0.0, 1.0)
}

## define saturation and values ranges
sv_options = {
    'upper' : (0.5, 1.0),
    'lower' : (0.0, 0.5),
    'medium' : (0.25, 0.75),
    'narrow_upper' : (0.7, 1.0),
    'medium_upper' : (0.8, 0.9),
    'narrow_lower' : (0.0, 0.25),
    'narrow_medium' : (0.375, 0.625),
    '0.7' : (0.7,0.7),
    '0.8' : (0.8,0.8),
    '0.9' : (0.9,0.9),
    'full' : (0.0, 1.0),
    'top' : (1.0, 1.0),
    'bottom' : (0.0, 0.0)
}

# Useful functions
def GetIterHues(hues):
    """Iterates on all the possible hues"""
    return random.choice(hue_options.keys()) if hues == 'cycle' else hues


def GetRandomSquareColor(hue_name, saturation, value):
    """Sets a random color for a square from within the inputs ranges"""
    if hue_name == 'random_options' or hue_name == 'cycle':
        hues_temp = random.choice(hue_options.keys())
        print hues_temp
    elif hue_name == 'red':
        hues_temp = random.choice('red1', 'red2')
    else:
        hues_temp = hue_name

    hsv_tuple = (random.uniform(hue_options.get(hues_temp)[0], hue_options.get(hues_temp)[1]),
                 random.uniform(sv_options.get(saturation)[0], sv_options.get(saturation)[1]),
                 random.uniform(sv_options.get(value)[0], sv_options.get(value)[1]))

    rgb_tuple = hsv2rgb(*hsv_tuple)
    color = rgb_tuple

    return color


def hsv2rgb(h, s, v):
    """Convert HSV colors to RGB"""
    return tuple(int(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))