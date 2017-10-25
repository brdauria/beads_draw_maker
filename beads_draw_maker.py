import matplotlib.pyplot as plt
from matplotlib import patches
from basic_units import BasicUnit
from basic_units import cm, inch
import json, sys
from os.path import expanduser
debug_on = False

def debug(*kwargs):
    if debug_on:
        print(*kwargs)

def image():
    img = []
    img.append('xxxxxxxxxxxxx')
    img.append('xxxxxxxxxxxxx')
    img.append('xxxxxxrxxxxxx')
    img.append('xxxxxrrrxxxxx')
    img.append('xxxxrryrrxxxx')
    img.append('xxxxxrrrxxxxx')
    img.append('xxxxxxrxxxxxx')
    img.append('xxxxxxgxxxxxx')
    img.append('xxxxxxgxxxxxx')
    img.append('xxxxxxgxggxxx')
    img.append('xxxxxxggggxxx')
    img.append('xxxxxxggxxxxx')
    img.append('xxxxxxgxxxxxx')
    img.append('xxxxxxgxxxxxx')
    img.append('xxxxbbbbbxxxx')
    img.append('xxxxxxxxxxxxx')
    img.append('xxxxxxxxxxxxx')
    img.append('xxxxxxxxxxxxx')
    return img

def plot(ax, img):
    yoffset = int((paper_y - len(img)) / 2)
    xoffset = int((paper_x - len(img[0])) / 2)
    debug('xoffset:',xoffset,' yoffset:',yoffset)
    y = paper_y - yoffset

    colors = config['colors']
    show_dots = config['show_dots']
    for line in img:
        y -= 1
        x = xoffset
        for c in line:
            x += 1
            color = colors.get(c, ['None', c])
            if color is not None:
                ec, fc = color
                p = patches.Circle((x * pin, y * pin), 0.5 * pin, lw=1, ec=ec, fc=fc, zorder=0, axes=ax)
                ax.add_patch(p)
            elif show_dots:
                    p = patches.Circle((x * pin, y * pin), 0.1, fc='k', zorder=0, axes=ax)
                    ax.add_patch(p)

def read_config():
    global config
    with open('config.json', 'r') as f:
        config = json.load(f)

    global pin
    pin = BasicUnit('pin', 'pins')
    space = config['pins_space_cm']  # 9.2 / (20 - 1) = 0.4842105263
    pin.add_conversion_factor(cm, space)
    pin.add_conversion_factor(inch, space / 2.54)

    cm.add_conversion_factor(pin, 1 / space)
    inch.add_conversion_factor(pin, 2.54 / space)

    global paper_x, paper_y
    global paper_x_in_inches, paper_y_in_inches
    paper_x = config['pins_x'] - 1
    paper_y = config['pins_y'] - 1
    paper_x_in_inches = (paper_x * pin).convert_to(inch).get_value()
    paper_y_in_inches = (paper_y * pin).convert_to(inch).get_value()
    debug(paper_x_in_inches,',',paper_y_in_inches)

def read_image(fname):
    with open(fname) as f:
        content = f.readlines()
    return [x.strip() for x in content] # remove `\n` at the end of each line

if __name__ == "__main__":
    read_config()

    if len(sys.argv) > 1:
        img = read_image(sys.argv[1])
    else:
        img = image()

    fig = plt.figure(figsize=(paper_x_in_inches, paper_y_in_inches))
    fig.subplots_adjust(bottom=0, top=1, left=0, right=1)
    ax = fig.add_subplot(111, aspect='equal')
    ax.xaxis.set_units(pin)
    ax.yaxis.set_units(pin)

    ax.set_xlim((0, paper_x * pin))
    ax.set_ylim((0, paper_y * pin))

    plot(ax, img)

    base_dir = config['base_dir']
    if base_dir[0] == '~':
        base_dir = expanduser("~") + base_dir[1:]

    file_name = config['file_name']
    plt.savefig(base_dir + file_name, dpi=config['DPI'])

    if config['show_on_screen']:
        plt.show()
