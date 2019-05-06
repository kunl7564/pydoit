import os
import random
import time
from utils import file_utils
from utils.file_utils import get_filename

def getFileList(path, file_list):
    parents = os.listdir(path)
    for parent in parents:
        child = os.path.join(path, parent)
        if os.path.isdir(child):
            getFileList(child, file_list)
        else:
            if child.endswith("csv") & os.path.getsize(child) < 1024 * 1024:
                file_list.append(child)
#                 print(child)
    return



def generateFile(out_dir, src_list, level1_dirnum, level2_dirnum, dirfilenum):
    max_index = len(src_list) - 1
    for i in range(level1_dirnum):
        level1_dir = os.path.join(out_dir, str(random.randint(350, 899)))
        os.mkdir(level1_dir)
        print("%d:%s" % (i, level1_dir))
        for j in range(level2_dirnum + random.randint(0, 20)):
            level2_dir = os.path.join(level1_dir, str(random.randint(350, 9999)))
            os.mkdir(level2_dir)
#             print("%d:%s" % (j, level2_dir))
            for k in range(dirfilenum + random.randint(0, 20)):
                srcfile = file_list[random.randint(0, max_index)]
                dstfile = os.path.join(level2_dir, str(random.randint(350, 9999)) + ".csv")
                print(srcfile + " " + dstfile)
                file_utils.copy(srcfile, dstfile)
#                 print("%d:%s" % (k, filepath))
    return
    
if __name__ == '__main__':
    file_list = [1, 2, 3]
    getFileList("F:\data\elecm", file_list)
#     generateFile("A:\\ai\\PrivateElecAi\\data\\dataset", file_list, 57, 100, 100)
#     for i in range(len(file_list)):
#         print(file_list[random.randint(0, max_index)])
