import os

def extract_files_with_conditions(path):
    extracted_files = []

    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'rb') as f:
                content = f.read()

                index = 0
                current_header_start = None
                file_count = 1  # 用于为同一文件的多个片段编号
                while index < len(content):
                    header_start_index = content.find(b'\x80\x00', index)
                    if header_start_index == -1:
                        # 如果没有找到更多的头部，将剩余内容作为最后一个片段
                        if current_header_start is not None:
                            search_range = content[current_header_start:]
                            extracted_files.append((file, search_range, file_count))
                            file_count += 1
                        break

                    # 检查从找到的b'\x80\x00'开始的10个字节里面是否包含固定序列
                    if (b'\x03\x12\x04\x01\x00\x00' in content[header_start_index:header_start_index + 10]) or (
                            b'\x03\x12\x04\x02\x00\x00' in content[header_start_index:header_start_index + 10]):
                        next_header_index = content.find(b'\x80\x00', header_start_index + 1)
                        if current_header_start is None:
                            current_header_start = header_start_index
                        else:
                            search_range = content[current_header_start:header_start_index]
                            if b'\x28\x63\x29\x43\x52\x49' in search_range:
                                extracted_files.append((file, search_range, file_count))
                                file_count += 1
                            current_header_start = header_start_index

                    index = header_start_index + 1

    return extracted_files

if __name__ == "__main__":
    input_path = input("请输入要遍历的文件夹路径: ")
    extracted_files = extract_files_with_conditions(input_path)

    for file_name, file_content, count in extracted_files:
        file_dir, file_ext = os.path.splitext(input_path)  # 获取输入路径的目录和扩展名，这里只取目录部分
        if count == 1:
            output_file_path = os.path.join(file_dir, f"{os.path.splitext(file_name)[0]}.adx")
        else:
            output_file_path = os.path.join(file_dir, f"{os.path.splitext(file_name)[0]}_{count}.adx")
        with open(output_file_path, 'wb') as f:
            f.write(file_content)

        print(f"已提取文件: {output_file_path}")

    print(f"共提取出 {len(extracted_files)} 个符合条件的文件片段。")