import os
rootdir = 'D:\datasets\HindawiArticles\\2008'

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        print(os.path.join(subdir, file))