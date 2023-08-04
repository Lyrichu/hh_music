#!/bin/bash
# 使用pyinstaller 打包
app_name="HH音乐播放器"
app_icon=resource/icons/music_app_icon.png
pyinstaller --windowed --name=$app_name --icon=$app_icon --add-data="resource:resource" main.py