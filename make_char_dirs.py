import os

def make_char_dir(initial_char_dir):
    char_dir = initial_char_dir
    while 1:
        if os.path.exists(char_dir):
            char_dir = char_dir+'_'
        else:
            os.mkdir(char_dir)
            return char_dir
        
char_list = ['ka','kha','ga','nga',
             'ca','cha','ja','nya',
             'ta','tha','da','na',
             'pa','pha','ba','ma',
             'tsa','tsha','dza','wa',
             'zha','za','a','ya',
             'ra','la','sha','sa',
             'ha','aa']
cwd = os.getcwd()
char_dir = make_char_dir(cwd+'/characters/')
for char in char_list:
    os.mkdir(char_dir+char)
print 'dirs created'

    
