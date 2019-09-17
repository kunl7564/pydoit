import os
import random
import time
from lk.utils import file_utils
from lk.utils.file_utils import get_filename

def getFileList(path, file_list):
    parents = os.listdir(path)
    for parent in parents:
        child = os.path.join(path, parent)
        if os.path.isdir(child):
            getFileList(child, file_list)
        else:
            if child.endswith("csv") and os.path.getsize(child) < 1024 * 1024:
                try:
                    print(child)
                    file_list.append(child)
                except UnicodeEncodeError:
                    print("err")
    return



def generateFile(out_dir, src_list, level1_dirnum, level2_dirnum, dirfilenum):
    max_index = len(src_list) - 1
    for i in range(level1_dirnum):
        level1_dir = os.path.join(out_dir, str(random.randint(350, 899)))
        file_utils.mkdir(level1_dir)
        print("%d:%s" % (i, level1_dir))
        for j in range(level2_dirnum + random.randint(0, 20)):
            level2_dir = os.path.join(level1_dir, str(random.randint(350, 9999)))
            file_utils.mkdir(level2_dir)
#             print("%d:%s" % (j, level2_dir))
            for k in range(dirfilenum + random.randint(0, 20)):
                srcfile = file_list[random.randint(0, max_index)]
                dstfile = os.path.join(level2_dir, str(random.randint(350, 9999)) + ".csv")
                print("%s->%s" % (srcfile, dstfile))
                file_utils.copy(srcfile, dstfile)
#                 print("%d:%s" % (k, filepath))
    return
    
if __name__ == '__main__':
    file_list = []
    getFileList("/home/samba/ai/tmp/elecm", file_list)
    generateFile("/home/samba/ai/PrivateElecAi/data/dataset/", file_list, 57, 100, 100)
#     for i in range(len(file_list)):
#         print(file_list[random.randint(0, max_index)])
