import os

def count_chars():
    cwd = os.getcwd()    
    char_dir_path = cwd + '/characters/'
    char_dirs = os.listdir(char_dir_path)
    for char_dir in char_dirs:
        print char_dir, ' -> ', len(os.listdir(char_dir_path+char_dir))

if __name__ == '__main__':
    count_chars()

    
