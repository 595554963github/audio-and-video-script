import os

def extract_content(file_path, directory_path, start_sequence, block_marker, end_sequence=None):
    with open(file_path, 'rb') as file:
        content = file.read()
        start_index = content.find(start_sequence)
        if start_index == -1:
            print(f"No start sequence found in {file_path}")
            return

        # 从第一个文件头开始读取
        content = content[start_index:]
        count = 0
        while True:
            start_index = content.find(start_sequence)
            if start_index == -1:
                print(f"No more start sequences found in {file_path}")
                break

            # 从找到的字节序列开始，直到下一个字节序列结束
            next_start_index = content.find(start_sequence, start_index + len(start_sequence))
            if next_start_index == -1:
                # 如果没有找到下一个文件头，则提取剩余的内容
                end_index = len(content)
            else:
                # 提取从文件头到下一个文件头之前的内容
                end_index = next_start_index

            # 提取内容
            extracted_data = content[start_index:end_index]
            # 检查是否为有效数据
            if block_marker in extracted_data and (end_sequence is None or end_sequence in extracted_data):
                # 生成新的文件名，默认以源文件名作为前缀，后面用数字递增
                file_extension = '.hca' if end_sequence is None else '.hca'
                new_filename = f"{os.path.splitext(os.path.basename(file_path))[0]}_{count}{file_extension}"
                new_filepath = os.path.join(directory_path, new_filename)
                # 保存到新文件
                with open(new_filepath, 'wb') as new_file:
                    new_file.write(extracted_data)
                print(f"Extracted and saved {new_filename}")
                count += 1
            else:
                print(f"Invalid data found in {file_path}, skipping...")

            # 更新内容，继续查找
            if next_start_index == -1:
                break
            content = content[next_start_index:]

def extract_encrypted_hca_content(file_path, directory_path):
    encrypted_hca_start_sequence = b'\xC8\xC3\xC1\x00\x03\x00\x00\x60'
    with open(file_path, 'rb') as file:
        content = file.read()
        start_index = content.find(encrypted_hca_start_sequence)
        if start_index == -1:
            print(f"No encrypted HCA start sequence found in {file_path}")
            return

        # 从第一个加密文件头开始读取
        content = content[start_index:]
        count = 0
        while True:
            start_index = content.find(encrypted_hca_start_sequence)
            if start_index == -1:
                print(f"No more encrypted HCA start sequences found in {file_path}")
                break

            # 从找到的字节序列开始，直到下一个字节序列结束
            next_start_index = content.find(encrypted_hca_start_sequence, start_index + len(encrypted_hca_start_sequence))
            if next_start_index == -1:
                # 如果没有找到下一个加密文件头，则提取剩余的内容
                end_index = len(content)
            else:
                # 提取从加密文件头到下一个加密文件头之前的内容
                end_index = next_start_index

            # 提取内容
            extracted_data = content[start_index:end_index]
            new_filename = f"{os.path.splitext(os.path.basename(file_path))[0]}_{count}_enc.hca"
            new_filepath = os.path.join(directory_path, new_filename)
            with open(new_filepath, 'wb') as new_file:
                new_file.write(extracted_data)
            print(f"Extracted and saved encrypted HCA file: {new_filename}")
            count += 1

            # 更新内容，继续查找
            if next_start_index == -1:
                break
            content = content[next_start_index:]

def main():
    directory_path = input("请输入要处理的文件夹路径: ")
    if not os.path.isdir(directory_path):
        print(f"错误: {directory_path} 不是一个有效的目录。")
        return

    # 定义要查找的字节序列
    hca_start_sequence = b'\x48\x43\x41\x00'
    hca_block_marker = b'\x66\x6D\x74'
    encrypted_hca_start_sequence = b'\xC8\xC3\xC1\x00\x03\x00\x00\x60'

    # 将序列组合成一个列表（这里简化了，因为只处理两种类型，不再需要字典形式，可直接用列表即可）
    sequences = [
        ('hca', hca_start_sequence, hca_block_marker, None),
        ('encrypted_hca', encrypted_hca_start_sequence, None, None)
    ]

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            print(f"Processing file: {file_path}")
            found = False
            for seq_type, start_sequence, block_marker, end_sequence in sequences:
                if seq_type == 'hca':
                    if extract_content(file_path, directory_path, start_sequence, block_marker, end_sequence):
                        found = True
                        break
                elif seq_type == 'encrypted_hca':
                    extract_encrypted_hca_content(file_path, directory_path)
                    found = True
                    break
            if not found:
                print(f"未找到符合条件的数据在 {file_path}")

if __name__ == "__main__":
    main()