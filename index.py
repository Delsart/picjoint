import getopt
import math
import os
import sys

from PIL import Image, ImageSequence

m_name = 'picjoint'
m_version = 'v0.01'

directions = ['TB', 'BT', 'LR', 'RL']
file_types = ['.jpeg', '.jpg', '.png', '.gif', '.webp']
image_modes = ['1', 'L', 'P', 'RGB', 'RGBA', 'CMYK']

message_help = '%s %s usage:' % (m_name, m_version)+'''
-d   --direction      <direction>                              [string]['TB', 'BT', 'LR', 'RL'][default: TB]
                      'TB' top to bottom
                      'BT' bottom to top
                      'LR' left to right
                      'RL' right to left
-o   --output         <output file name>                                           [string][default: result]
-f   --fold           <input files fold>                                                            [string]
-q   --quality        <quality>                                                                      [float]
-w   --width          <output width>                                                                   [int]
-h   --height         <output height>                                                                  [int]
-m   --mode           <output mode default>    [string]['1', 'L', 'P', 'RGB', 'RGBA', 'CMYK'][default: RGBA]

[file1, file2, ...]   <input files>                                                                 [string]
'''
message_error_dirction = " must be ['TB', 'BT', 'LR', 'RL']"
message_error_mode = " must be ['1', 'L', 'P', 'RGB', 'RGBA', 'CMYK']"
message_error_quality = "quality must in (0,1], the input is "


# 检查文件类型
def fileTypeCheck(fn):
    for i, itype in enumerate(file_types):
        if fn.endswith(itype):
            return (True, i)
    return (False, -1)


# 处理命令行参数
def main(argv):
    try:
        opts, args = getopt.getopt(
            argv, "d:o:f:q:w:h:m:", ['direction', "output", "fold", "quality", 'width', 'height', 'mode'])
    except getopt.GetoptError:
        print(message_help)
        sys.exit(2)

    # 处理返回值options是以元组为元素的列表。
    output_name = 'result'
    direction = 'TB'
    input_fold = ''
    quality = 1
    specifyed_width = 0
    specifyed_height = 0
    specifyed_mode = 'RGBA'
    for opt, arg in opts:
        if opt in ("-d", "--direction"):
            direction = arg
            if not direction in directions:
                print(opt+message_error_dirction)
                sys.exit(2)
        elif opt in ("-o", "--output"):
            output_name = arg
        elif opt in ("-f", "--fold"):
            input_fold = arg
        elif opt in ("-q", "--quality"):
            quality = float(arg)
            if quality > 1 or quality <= 0:
                print(message_error_quality + arg)
                sys.exit(2)
        elif opt in ("-w", "--width"):
            specifyed_width = int(arg)
        elif opt in ("-h", "--height"):
            specifyed_height = int(arg)
        elif opt in ("-m", "--mode"):
            specifyed_mode = arg
            if not specifyed_mode in image_modes:
                print(opt+message_error_mode)
                sys.exit(2)

    # files
    file_paths = args
    # 打开文件
    input_images, output_Type = openImage(input_fold, file_paths)
    # 处理文件
    joint(input_images, direction, quality, specifyed_width,
          specifyed_height, output_name, output_Type, specifyed_mode)


# 打开文件，同时根据打开的文件判断输出类型
def openImage(fold, paths):

    temp_l = [os.path.join(fold, fn)
              for fn in os.listdir(fold)] if not fold == '' else[]
    temp_l.extend([path for path in paths])
    if len(temp_l) < 1:
        temp_l = [fn for fn in os.listdir()]
    f_l = []
    otype = 0
    for t in temp_l:
        success, ftype = fileTypeCheck(t)
        if success:
            f_l.append(t)
            if ftype > otype:
                otype = ftype

    return ([Image.open(fn) for fn in f_l], otype)


# 拼接图片
def joint(im_list, direction, quality, specifyed_width, specifyed_height, output_name, output_type, mode):

    # 计算尺寸
    max_width = 0
    max_height = 0
    input_total_width = 0
    input_total_height = 0
    input_num = len(im_list)
    for i in im_list:
        w, h = i.size
        input_total_width += w
        input_total_height += h

        if w > max_width:
            max_width = w
        if h > max_height:
            max_height = h

    max_width = max_width*quality
    max_height = max_height*quality

    if not specifyed_width == 0:
        max_width = specifyed_width
    if not specifyed_height == 0:
        max_height = specifyed_height

    handle_width = False
    if directions.index(direction) < 2:
        handle_width = True

    max_frames = 0
    ims = []
    total_width = 0
    total_height = 0
    for i in im_list:
        w, h = i.size
        radio_x = 0
        radio_y = 0
        if handle_width:
            radio_x = max_width/w
            if not specifyed_height == 0:
                radio_y = specifyed_height/input_total_height
            else:
                radio_y = radio_x
        else:
            radio_y = max_height/h
            if not specifyed_width == 0:
                radio_x = specifyed_width/input_total_width
            else:
                radio_x = radio_y
        new_w = round(w*radio_x)
        new_h = round(h*radio_y)
        total_width += new_w
        total_height += new_h
        frames = [frame.resize((new_w, new_h), Image.BILINEAR)
                  for frame in ImageSequence.Iterator(i)]
        max_frames = len(frames) if len(frames) > max_frames else max_frames
        ims.append({'frames': frames, 'size': (new_w, new_h)})

    # 拼接图片
    new_w = math.floor(max_width) if handle_width else total_width
    new_h = math.floor(max_height)if not handle_width else total_height
    results = []

    print('mode:', mode)
    print('frames:', max_frames)
    print('width:', new_w)
    print('height:', new_h)
    print('type:', file_types[output_type])
    print('')

    for frame_num in range(max_frames):
        # 创建空白长图
        result = Image.new(mode, (new_w, new_h))
        position = 0
        for i, im in enumerate(ims):
            frame_index = frame_num if frame_num < len(
                im['frames']) else (len(im['frames'])-1)

            if direction == directions[0]:
                result.paste(im['frames'][frame_index], box=(0, position))
                position += im['size'][1]

            if direction == directions[1]:
                position += new_h-im['size'][1] if i < 1 else -im['size'][1]
                result.paste(im['frames'][frame_index], box=(0, position))

            if direction == directions[2]:
                result.paste(im['frames'][frame_index], box=(position, 0))
                position += im['size'][0]

            if direction == directions[3]:
                position += new_w-im['size'][0] if i < 1 else -im['size'][0]
                result.paste(im['frames'][frame_index], box=(position, 0))

        results.append(result)

    # 保存图片
    print('saving...')
    if len(results) < 2:
        results[0].save(output_name+file_types[output_type])
    else:
        results[0].save(output_name+file_types[output_type], save_all=True, loop=True,
                        append_images=results[1:], duration=max_frames/30, optimize=True, disposal=1)


if __name__ == "__main__":
    main(sys.argv[1:])
