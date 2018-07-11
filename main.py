# -*-coding:utf-8-*-
from kivy.app import App
import load_file_name
from kivy.uix.listview import ListView
from kivy.uix.gridlayout import GridLayout
from kivy.config import Config
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.listview import ListItemButton, ListView
import time
import kivy
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
# 用于播放声音
from kivy.core.audio import SoundLoader
import os
'''
本次作业要做一个 播放器 软件, 以后的项目中会把这个软件功能完善, 这只是初步的阶段

为了实现播放声音, 本次引入了一个新的类 SoundLoader
具体用法很简单, 下面第一行加载声音返回一个类, 第二行调用 play() 方法播放
audio = SoundLoader.load('mipha.mp3')
audio.play()        # 播放声音


audio.stop()        # 停止播放
audio.get_pos()     # 当前播放到的时间, 单位是秒, 只有在播放的时候才能获取, 否则是 0
audio.length        # 声音的长度, 单位是秒
audio.volume = 1    # 设置/读取音量, 值范围是 0 到 1, 1 是最大音量

详细介绍可以参考官方文档(不建议, 本作业用不着)
https://kivy.org/docs/api-kivy.core.audio.html


界面要求 3 个控件
1, 显示播放进度的 label, 格式如下(当前时间 分:秒 / 总时间 分:秒)
    00:00/04:12
2, 播放按钮
    开始更新播放进度, 一秒更新一次
3, 停止按钮
    停止更新播放进度并且播放进度清零, 声音停止
'''
log = print
kivy.resources.resource_add_path('Font/')
font = kivy.resources.resource_find('simkai.ttf')
def file_name(file_dir, Str):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == Str:
                L.append(os.path.join(root, file))
    return L
def find_slider(lrc_time, T):
    index = -1
    for i in range(len(lrc_time)):
        if T > lrc_time[i]:
            continue
        else:
            index = i
            break
    return index
def find_s(str, S):
    index = -1
    for i in range(len(str)):
        if str[i] == S:
            index = i
    return index
def count_time(Str):
    minute = int(Str[0:2])
    second = float(Str[3:8])
    return minute*60 + second
def load_lrc(filename):
    lrc_time = []
    lrc_word = []
    flag = False
    for line in open(filename):
        if 'offset' in line:
            flag = True
            continue

        if flag:
            index = find_s(line, ']')
            lrc_ = (line[1:index ])
            if lrc_ == '':
                continue
            lrc_time.append(count_time(lrc_))
            lrc_word.append(line[(index + 1):(len(line)-1)])
    return lrc_time,lrc_word
def font_name():
    """
    苹果系统和微软系统需要不同的字体文件
    """
    from sys import platform
    if platform == "darwin":
        return 'Arial Unicode'
    elif platform == "win32":
        return 'SimHei'
    else:
        print('not support')
class MusicPlayerApp(App):
    def build(self):
        self.config_window()
        root = self.setup_ui()
        return root

    def config_window(self):
        """
        这里设置了 3 个属性, 这是固定的写法
        分别是 禁止缩放, 宽度 768, 高度 1024
        """
        g = 'graphics'
        Config.set(g, 'resizable', True)
        Config.set(g, 'width', 1024)
        Config.set(g, 'height', 768)

    def setup_ui(self):
        # layout = BoxLayout(orientation='vertical')
        layout = FloatLayout(size=(1024, 768))
        button_config1 = dict(
            text='播放',
            font_size=40,
            background_color = (0,1,0,1),
            # pos=(80, 30),
            # size=(150, 80),
            pos_hint={'x':0.1, 'y':0.06},
            size_hint=(0.15,0.13),
            font_name=font,  # 字体名字也可以在初始化的时候配置
        )
        button_config2 = dict(
            text='停止',
            background_color=(1, 0, 0, 1),
            font_size=40,
            # pos=(680, 30),
            # size=(150, 80),
            pos_hint={'x': 0.78, 'y': 0.06},
            size_hint=(0.15, 0.13),
            font_name=font,  # 字体名字也可以在初始化的时候配置
        )
        button_config3 = dict(
            text='暂停',
            background_color=(1, 0, 1, 0.7),
            font_size=40,
            # pos=(380, 30),
            # size=(150, 80),
            pos_hint={'x': 0.45, 'y': 0.06},
            size_hint=(0.15, 0.13),
            font_name=font,  # 字体名字也可以在初始化的时候配置
        )
        button_config4 = dict(
            text='>',
            font_size=40,
            # pos=(380, 30),
            # size=(150, 80),
            pos_hint={'x': 0.64, 'y': 0.08},
            size_hint=(0.1, 0.08),
            font_name=font,  # 字体名字也可以在初始化的时候配置
        )
        button_config5 = dict(
            text='<',
            font_size=40,
            # pos=(380, 30),
            # size=(150, 80),
            pos_hint={'x': 0.30, 'y': 0.08},
            size_hint=(0.1, 0.08),
            font_name=font,  # 字体名字也可以在初始化的时候配置
        )
        button1 = Button(**button_config1)
        button1.bind(on_press=self.button_press)
        layout.add_widget(button1)

        button2 = Button(**button_config2)
        button2.bind(on_press=self.button_press2)
        layout.add_widget(button2)

        button3 = Button(**button_config3)
        button3.bind(on_press=self.button_press3)
        layout.add_widget(button3)

        button4 = Button(**button_config4)
        button4.bind(on_press=self.button_press4)
        layout.add_widget(button4)

        button5 = Button(**button_config5)
        button5.bind(on_press=self.button_press5)

        layout.add_widget(button5)

        slider1 = Slider(y=150, pos_hint={'x': .1, 'y':0.25},size_hint=(.45, None),min= 0,max=100,value= 0,value_track=True, value_track_color=[0, 0, 1, 0.5])
        slider1.bind(value=self._set_music_offset)
        self.slider1 = slider1
        layout.add_widget(slider1)

        slider = Slider(y=150, pos_hint={'x': .7, 'y':0.25},value= 50, size_hint=(.25, None), value_track=True, value_track_color=[1, 0, 0, 1])
        # slider = Slider(min= 0,max=100,value= 50,value_track=True, value_track_color=[1, 0, 0, 1])
        slider.bind(value= self._set_volum_offset)
        self.slider = slider
        layout.add_widget(slider)

        slider2 = Slider(y=90, pos_hint={'x': .7, 'y':0.19}, size_hint=(.25, None), min=0, max=100, value=0,value_track=True, value_track_color=[1, 0, 1, 0.5])

        slider2.bind(value=self._set_music_delay)
        self.slider2 = slider2
        layout.add_widget(slider2)

        # 把 result 这个输入框用类的属性存起来之后要使用
        # 类属性在类的任何函数中都可以创建, 并不一定要在 __init__ 中创建
        # self.filename = '1.mp3'
        music_dir = 'music'
        lrc_dir = 'lrc'
        self.music_play_count = 0
        self.music_list = file_name(music_dir, '.mp3')  #载入歌单以及歌词
        self.lrc_list = file_name(lrc_dir, '.lrc')
        self.filename = self.music_list[self.music_play_count]
        self.lrc_filename = self.lrc_list[self.music_play_count]
        self.lrc_time, self.lrc_word = load_lrc(self.lrc_filename)
        audio = SoundLoader.load(self.filename)
        self.audio = audio
        self.pre_time = self.audio.get_pos()  # 当前播放到的时间, 单位是秒, 只有在播放的时候才能获取, 否则是 0
        self.length = self.audio.length
        self.pre_slider_time = self.audio.get_pos()
        self.minute = 0
        self.second = 0
        self.delay = 0.025  # 缓解由于调整进度条导致的音乐音卡顿现象
        self.flag = False
        self.length_minute = 0
        self.length_second = 0
        self.button1 = button1
        self.button2 = button2
        self.button3 = button3
        self.button4 = button4
        self.button5 = button5

        #
        self.length_minute = int(self.length / 60)
        self.length_second = int(self.length) - self.length_minute * 60
        if self.length_second < 10:
            self.str_length_second = '0' + str(self.length_second)
        else:
            self.str_length_second = str(self.length_second)
        if self.length_minute < 10:
            self.str_length_minute = '0' + str(self.length_minute)
        else:
            self.str_length_minute = str(self.length_minute)
        left_part = '00:00:'
        self.right_part = self.str_length_minute + ':' + self.str_length_second
        label_config = dict(
            text=left_part + '/' + self.right_part,
            font_size=50,
            halign='center',    # 横向居中显示
        )
        label = Label(**label_config)
        self.label = label
        layout.add_widget(label)
        label_config = dict(
            text=self.filename[6:len(self.filename)],
            font_size=50,
            font_name = font,
            # pos_hint = (20,180),
            # pos=(380, 30),
            # size=(150, 80),
            pos_hint={'x': 0.5, 'y': 0.78},
            size_hint=(0.1, 0.08),
            color = (0, 1, 1, 0.75)
            # halign='justify',  # 横向居中显示
        )
        label1 = Label(**label_config)
        self.label1 = label1
        layout.add_widget(label1)
        label_config = dict(
            text=self.filename[6:len(self.filename)],
            font_size=35,
            font_name=font,
            color=(0.7, 0.3, 1, 0.75),
            pos_hint={'x': 0.5, 'y': 0.62},
            size_hint=(0.1, 0.08),
            # halign='justify',  # 横向居中显示
        )
        label2 = Label(**label_config)
        self.label2 = label2
        layout.add_widget(label2)
        label_config = dict(
            text=str(int(self.slider.value))+'%',
            font_size=25,
            # pos=(420, -70),
            pos_hint={'x': .47, 'y': -0.19}
        )
        label3 = Label(**label_config)
        self.label3 = label3
        layout.add_widget(label3)
        label_config = dict(
            text='音量',
            font_name=font,
            font_size=25,
            # pos=(150, -70),
            pos_hint={'x': .16, 'y': -0.19}
        )

        label4 = Label(**label_config)
        self.label4 = label4
        layout.add_widget(label4)
        label_config = dict(
            text=str(int(self.slider1.value)) + '%',
            font_size=25,
            # pos=(90, -70),
            pos_hint={'x': .07, 'y': -0.19}
        )
        label5 = Label(**label_config)
        self.label5 = label5
        layout.add_widget(label5)
        label_config = dict(
            text='进度',
            font_name=font,
            font_size=25,
            # pos=(-420, -70),
            pos_hint={'x': 0.015, 'y': - 0.09},
            size_hint=(0.1, 0.8),
        )
        label6 = Label(**label_config)
        self.label6 = label6
        layout.add_widget(label6)
        label_config = dict(
            text='延迟',
            font_name=font,
            font_size=25,
            # pos=(-420, -150),
            pos_hint={'x': .16, 'y': -0.25}
        )
        label6 = Label(**label_config)
        self.label6 = label6
        layout.add_widget(label6)
        # list_view = ListView(item_strings=[str(index) for index in range(5)])
        #
        # layout.add_widget(list_view)

        # 歌单


        # data = [{'text': str(i), 'is_selected': False} for i in self.music_list]
        #
        # args_converter = lambda row_index, rec: {'text': rec['text'],
        #                                          'size_hint_y': None,
        #                                          'font_name' : font,
        #                                          'pos_hint' : {'x': .7},
        #                                          'size_hint' : (.23, None),
        #                                          'height': 25}
        #
        # list_adapter = ListAdapter(data=data,
        #                            args_converter=args_converter,
        #                            cls=ListItemButton,
        #                            selection_mode='single',
        #                            allow_empty_selection=False)
        #
        # list_view = ListView(adapter=list_adapter)
        # layout.add_widget(list_view)

        # 注意，你需要在当前目录放一个音乐文件并替换 a.mp3 这个名字为你的音乐文件
        Clock.schedule_interval(self.timer, 0.005)
        return layout
    def button_press(self, button):
        self.lrc_time,self.lrc_word = load_lrc(self.lrc_filename)
        self.point = 0
        self.audio.play()
        self.flag = True
        self.pre_time = self.audio.get_pos()
        self.length = self.audio.length
        self.length_minute = int(self.length / 60)
        self.length_second = int(self.length) - self.length_minute*60
        if self.length_second < 10:
            self.str_length_second = '0' + str(self.length_second)
        else:
            self.str_length_second = str(self.length_second)
        if self.length_minute < 10:
            self.str_length_minute = '0' + str(self.length_minute)
        else:
            self.str_length_minute = str(self.length_minute)
        left_part = '00:00'
        self.label.text = left_part + '/' +self.right_part
        print('按钮点击', button)
    def button_press2(self, button2):
        self.flag = False
        self.pre_time = self.audio.get_pos()
        self.second = 0
        self.minute = 0
        self.point = 0
        self.slider1.value = 0
        self.label1.text = self.filename
        self.audio.stop()
        left_part = '00:00'
        self.label.text = left_part + '/' + self.right_part
        print('按钮点击', button2)
    def button_press3(self, button3):
        if self.button3.text == '暂停':
            self.flag = False
            self.pre_time = self.audio.get_pos()
            self.button3.background_color = (0, 1, 0, 0.7)
            self.audio.stop()
            self.button3.text = '继续'
        else:
            self.flag = True
            self.audio.play()
            self.button3.background_color = (1, 0, 1, 0.7)
            self.slider1.value = int((self.pre_time/self.length)*100)
            self.audio.seek(self.pre_time)
            self.button3.text = '暂停'
            index = find_slider(self.lrc_time, self.pre_time)
            self.point = index
            self.pre_time = self.audio.get_pos()
            self.pre_slider_time = self.audio.get_pos()   #用于暂停/开始之后恢复进度条状态
    def button_press4(self,button4):

        self.music_play_count += 1
        self.music_play_count = self.music_play_count % len(self.music_list)
        self.audio.stop()
        self.filename = self.music_list[self.music_play_count]
        self.lrc_filename = self.lrc_list[self.music_play_count]
        audio = SoundLoader.load(self.filename)
        self.audio = audio
        self.lrc_filename = self.lrc_list[self.music_play_count]

        self.point = 0
        self.audio.play()
        self.slider1.value = 0
        self.label2.text = self.filename[6:len(self.filename)]
        self.label1.text = self.filename[6:len(self.filename)]
        self.flag = True
        self.lrc_time, self.lrc_word = load_lrc(self.lrc_filename)
        self.pre_time = self.audio.get_pos()
        self.pre_slider_time = self.audio.get_pos()
        self.length = self.audio.length
        self.length_minute = int(self.length / 60)
        self.length_second = int(self.length) - self.length_minute * 60
        if self.length_second < 10:
            self.str_length_second = '0' + str(self.length_second)
        else:
            self.str_length_second = str(self.length_second)
        if self.length_minute < 10:
            self.str_length_minute = '0' + str(self.length_minute)
        else:
            self.str_length_minute = str(self.length_minute)
        self.right_part = self.str_length_minute + ':' + self.str_length_second
        left_part = '00:00'
        self.label.text = left_part + '/' + self.right_part
    def button_press5(self,button5):
        self.music_play_count -= 1
        self.music_play_count = self.music_play_count % len(self.music_list)
        self.audio.stop()
        self.filename = self.music_list[self.music_play_count]
        self.lrc_filename = self.lrc_list[self.music_play_count]
        audio = SoundLoader.load(self.filename)
        self.audio = audio
        self.point = 0
        self.audio.play()
        self.slider1.value = 0
        self.label2.text = self.filename[6:len(self.filename)]
        self.label1.text = self.filename[6:len(self.filename)]
        self.lrc_time, self.lrc_word = load_lrc(self.lrc_filename)
        self.flag = True
        self.pre_time = self.audio.get_pos()
        self.pre_slider_time = self.audio.get_pos()
        self.length = self.audio.length
        self.length_minute = int(self.length / 60)
        self.length_second = int(self.length) - self.length_minute * 60
        if self.length_second < 10:
            self.str_length_second = '0' + str(self.length_second)
        else:
            self.str_length_second = str(self.length_second)
        if self.length_minute < 10:
            self.str_length_minute = '0' + str(self.length_minute)
        else:
            self.str_length_minute = str(self.length_minute)
        left_part = '00:00'
        self.right_part = self.str_length_minute + ':' + self.str_length_second
        self.label.text = left_part + '/' + self.right_part
    def _set_music_delay(self, instance, value):
        self.delay = value/5000
        print(self.delay)
    def _set_volum_offset(self, instance, value):
        self.audio.volume = value / 100
        self.label3.text = str(int(self.slider.value))+'%'
    def _set_music_offset(self, instance, value):
        if self.flag:
            self.audio.seek((value / 100) * self.length)
            index = find_slider(self.lrc_time, (value / 100) * self.length)
            self.point = index
        self.minute = int((value / 100) * self.length / 60)
        self.second = int((value / 100) * self.length) - self.minute * 60
        if self.second > 59:
            self.minute += 1
            self.second = 0

        if self.second < 10:
            str_second = '0' + str(self.second)
        else:
            str_second = str(self.second)
        if self.minute < 10:
            str_minute = '0' + str(self.minute)
        else:
            str_minute = str(self.minute)
        left_part = str_minute + ':' + str_second
        self.label.text = left_part + '/' +self.right_part

        # self.point
        self.label5.text = str(int(self.slider1.value))+'%'
    def timer(self, dt):
        if self.flag == True:
            new_time = self.audio.get_pos()  # 当前播放到的时间, 单位是秒, 只有在播放的时候才能获取, 否则是 0
            new_slider_time = self.audio.get_pos()
            # print(self.point)

            # 校准歌词进度
            if abs(self.lrc_time[self.point] - new_time) < 0.3:
                self.label1.text = self.lrc_word[self.point]
                self.point += 1
                if self.point >= len(self.lrc_word):
                    self.point -= 1
            # 校准播放时间显示
            if abs(new_time - self.length) <= 1:
                self.second = 0
                self.minute = 0
                self.point = 0
                self.pre_time = self.audio.get_pos()
            if new_time - self.pre_time >= 1:
                self.second += 1
                self.pre_time = new_time

            # 校准播放进度条，每4s更新一次
            if new_slider_time - self.pre_slider_time >= 4:
                new_time = self.audio.get_pos()

                self.slider1.value = float((new_time + self.delay) / self.length) * 100
                self.pre_slider_time = new_slider_time
            #更新音乐播放时间
            if self.second > 59:
                self.minute += 1
                self.second = 0

            if self.second < 10:
                str_second = '0' + str(self.second)
            else:
                str_second = str(self.second)
            if self.minute < 10:
                str_minute = '0' + str(self.minute)
            else:
                str_minute = str(self.minute)
            left_part = str_minute + ':' + str_second
            self.label.text = left_part +'/'+ self.right_part
def main():
    MusicPlayerApp().run()


if __name__ == '__main__':
    main()
