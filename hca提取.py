import os

def extract_hca(file_path, directory_path, start_seq, block_marker=None):
    with open(file_path, 'rb') as f:
        content = f.read()
    start_index = 0
    count = 0
    while True:
        start_index = content.find(start_seq, start_index)
        if start_index == -1:
            break
        next_start_index = content.find(start_seq, start_index + len(start_seq))
        if next_start_index == -1:
            end_index = len(content)
        else:
            end_index = next_start_index
        extracted = content[start_index:end_index]
        if block_marker is None or block_marker in extracted:
            file_extension = '.hca'
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            new_name = f"{base_name}_{count}{file_extension}"
            if start_seq == b'\xC8\xC3\xC1\x00\x03\x00\x00\x60':
                new_name = f"{base_name}_{count}_enc{file_extension}"
            new_path = os.path.join(directory_path, new_name)
            with open(new_path, 'wb') as new_f:
                new_f.write(extracted)
            print(f"Extracted and saved {new_name}")
            count += 1
        start_index += len(start_seq)

def main():
    dir_path = input("请输入要处理的文件夹路径: ")
    if not os.path.isdir(dir_path):
        print(f"错误: {dir_path} 不是一个有效的目录。")
        return
    start_seq_1 = b'\x48\x43\x41\x00'
    start_seq_2 = b'\xC8\xC3\xC1\x00\x03\x00\x00\x60'
    hca_block_marker = b'\x66\x6D\x74'

    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(root, file)
            print(f"Processing file: {file_path}")
            with open(file_path, 'rb') as f:
                content = f.read()
            found = False
            start_index = 0
            while not found:
                start_index = content.find(start_seq_1, start_index)
                if start_index == -1:
                    break
                next_start_index = content.find(start_seq_1, start_index + len(start_seq_1))
                if next_start_index == -1:
                    end_index = len(content)
                else:
                    end_index = next_start_index
                extracted = content[start_index:end_index]
                if hca_block_marker in extracted:
                    extract_hca(file_path, dir_path, start_seq_1, hca_block_marker)
                    found = True
                start_index += len(start_seq_1)
            if not found:
                extract_hca(file_path, dir_path, start_seq_2)

if __name__ == "__main__":
    main()