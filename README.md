
# README

做设计的时候遇到拼接长图的情况，但是发现没有什么好用的能拼接gif的工具。\
于是自己写了个gif拼接小工具。

可以自动拼接gif、png和jpg等常见格式。

## 效果

| 从上至下                     | 从下至上                    | 从左至右                    | 从右至左                    |
| ---------------------------- | --------------------------- | --------------------------- | --------------------------- |
| ![tb](/picture/outpt_TB.gif) | ![bt](picture/outpt_BT.gif) | ![lr](picture/outpt_LR.gif) | ![rl](picture/outpt_RL.gif) |

## 使用

### 克隆仓库
```bash
git clone https://github.com/Delsart/picjoint.git
```
### 安装依赖
```bash
pip install -r requirement.txt
```

### 运行命令
拼接当前文件夹的所有图片
```bash
python index.py
```

指定文件夹
```bash
python index.py -f /inputfilepath/path
```

指定文件和拼接方向
```bash
python index.py -d TB /path1/1.gif /path2/path/2.jpeg /path3/3.gif
```

同时指定文件夹和文件
```bash
python index.py -f /inputfilepath/path /path1/1.gif /path2/path/2.jpeg /path3/3.gif
```

指定输出尺寸
```bash
python index.py -w 1000 -h 2000
```

## 选项
```
options:
-d   --direction      <direction>                            [string]['TB', 'BT', 'LR', 'RL'][default: TB]
                      'TB' top to bottom
                      'BT' bottom to top
                      'LR' left to right
                      'RL' right to left
-o   --output         <output file name>                                           [string][default: result]
-f   --fold           <input files fold>                                                            [string]
-q   --quality        <quality>                                                          [float][default: 1]
-w   --width          <output width>                                                                   [int]
-h   --height         <output height>                                                                  [int]
-m   --mode           <output mode default>    [string]['1', 'L', 'P', 'RGB', 'RGBA', 'CMYK'][default: RGBA]

[file1, file2, ...]   <input files>                                                                 [string]
```

## Todo
- [x] ~~自适应宽高/指定宽or高~~
- [ ] gif拼接时帧率匹配/等待
- [ ] gif拼接时最终输出帧率
- [ ] 网格布局
- [ ] 最大输出文件大小
