import os
import subprocess
import glob

def convert_files(input_directory):
    file_count = 0  # 用于记录合并文件的计数

    # 获取用户输入的视频格式和音频格式
    video_format = input("请输入视频格式（例如：mkv、m2v、h264等）：")
    audio_format = input("请输入音频格式（例如：wav、mp3、hca、adx等）：")

    # 遍历指定目录
    for root, dirs, files in os.walk(input_directory):
        # 找到所有指定格式的视频文件
        video_files = [f for f in files if f.endswith(video_format)]
        for video_index, video_file in enumerate(video_files):
            # 找到对应的音频文件
            audio_file = video_file.replace(video_format, audio_format)
            video_path = os.path.join(root, video_file)
            audio_path = os.path.join(root, audio_file)

            # 处理输出视频文件名，确保只有1个.
            output_file = video_file.replace(video_format, '.mp4')
            if '.' in output_file[:output_file.rfind('.')]:
                base_name = output_file[:output_file.rfind('.')].replace('.', '')
                ext = output_file[output_file.rfind('.'):]
                output_file = base_name + ext

            output_path = os.path.join(root, output_file)

            if os.path.exists(audio_path):
                # 构建FFmpeg命令（有对应音频文件的情况）
                ffmpeg_command = [
                    'ffmpeg', '-i', video_path, '-i', audio_path, '-c:v', 'libx265',
                    '-preset', 'fast', '-b:v', '20M', '-r', '60', '-crf', '16',
                    '-vf', 'scale=2048:1080', '-c:a', 'aac', '-b:a', '1536k',
                    output_path, '-hide_banner'
                ]
            else:
                # 构建FFmpeg命令（无对应音频文件的情况）
                ffmpeg_command = [
                    'ffmpeg', '-i', video_path, '-c:v', 'libx265',
                    '-preset', 'fast', '-b:v', '20M', '-r', '60', '-crf', '16',
                    '-vf', 'scale=2048:1080', output_path, '-hide_banner'
                ]

            # 打印并执行FFmpeg命令
            print(f'执行命令: {" ".join(ffmpeg_command)}')
            subprocess.run(ffmpeg_command, check=True)

            # 打印处理的文件信息
            if os.path.exists(audio_path):
                print(f'合并 {video_file} 和 {audio_file} 成 {output_file}')
            else:
                print(f'将 {video_file} 转换成 {output_file}')

            # 删除源文件（如果存在音频文件也删除）
            os.remove(video_path)
            if os.path.exists(audio_path):
                os.remove(audio_path)

            # 增加计数
            file_count += 1

    # 打印总共处理的文件数量
    print(f'总共处理的文件数量: {file_count}')

if __name__ == "__main__":
    input_directory = input("请输入目录路径: ")
    if not os.path.isdir(input_directory):
        print(f"错误: {input_directory} 不是一个有效的目录。")
    else:
        convert_files(input_directory)