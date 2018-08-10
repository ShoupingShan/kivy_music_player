# 音乐播放器

## 1. 简介
  ![surface](/ima/surface.png)

  主要利用`Python`中的`Kivy`工具包完成的简易音乐播放器，目前
主要完成的功能有：

    1. 开始播放音乐
    2. 暂停播放
    3. 停止播放
    4. 上一首/下一首
    5. 声音大小调节
    6. 歌词动态显示
    7. 进度条滑块
    8. 动态时间显示
## 2. Install
    $ sudo add-apt-repository ppa:kivy-team/kivy
    $ sudo apt-get update
    $ sudo apt-get install python-kivy
    $ sudo apt-get install python-pygame
## 3. 目录

### **Font/**

  保存中文字体（`Kivy`暂时不支持中文）

### **lrc/**

  ![lrc](/ima/lrc.png)

  保存歌词文件，注意，所有歌词在开始计算时间前有`[offset:]`标记

  ![offset](/ima/offset.jpg)

### **music/**

  保存歌曲文件

  ![music](/ima/music.png)
