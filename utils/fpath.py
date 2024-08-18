import os
import sys


BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
Res_Path = os.path.join(BASE_DIR, "res")

Pic_Path = os.path.join(Res_Path, "pics")
Data_Path = os.path.join(Res_Path, "data")

Version_Path = os.path.join(Data_Path, "version.json")
Lyr_Path = os.path.join(Data_Path, "lyr.txt")
Icon_Path = os.path.join(Pic_Path, "icons")
File_Path = os.path.join(Data_Path, "data.json")

Log_Path = os.path.join(Data_Path, "logs")
RP_Path = os.path.join(Data_Path, "record.png")

pro_cat_path = os.path.join(Res_Path, "cat.json")


pic_path = os.path.join(BASE_DIR, "pic")



