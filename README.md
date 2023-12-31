# hh音乐播放器

这是一个基于PySide6开发的音乐播放器。

## 主要功能

1. **音乐搜索**: 用户可以在搜索框中输入歌曲名、歌手或者专辑，点击搜索按钮，音乐播放器会自动搜索到相关的音乐。
2. **音乐播放**: 用户可以点击搜索结果中的播放按钮来播放音乐。
3. **音乐下载**: 用户可以点击搜索结果中的下载按钮来下载音乐，下载的音乐会被保存在用户设定的目录中。
4. **批量下载**: 用户可以选择多首歌曲进行批量下载。
5. **历史播放**: 用户可以查看历史播放列表
6. **下载管理**: 用户可以在"下载"菜单中查看下载任务的进度，以及已经下载的文件。
7. **日志查看**: 用户可以在"日志"菜单中查看应用的运行日志。

## 使用方法

1. 运行`main.py`文件来启动音乐播放器。

## 注意事项

1. 音乐播放器需要网络连接才能进行音乐搜索和下载,目前音源来自酷我。
2. 由于版权问题，部分歌曲可能无法播放或者下载。
3. 音乐播放器目前仅支持`.mp3`格式的音乐播放和下载。
4. 配置文件 & 日志等
   - 配置文件目录: 用户家目录/.hh_music.config
   - 运行日志文件: 用户家目录/.hh_music.log
   - 收听历史文件: 用户家目录/.hh_music_history_play_list.data
## 开发环境

- Python 3.8+
- PySide6
- Qt Designer
- loguru
- requests
- PyInstaller

如果你对这个音乐播放器有任何问题或者建议，欢迎通过GitHub提交issue或者pull request。
