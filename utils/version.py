import time
import utils.file_controls as F
import json


def version_control(v_path, flag=False):
    """版本控制脚本"""
    F.checkfile(v_path)
    t = time.localtime(time.time())
    data = time.strftime('%y%m%d%H%M', t)

    try:
        with open(v_path) as version_file:
            version = json.load(version_file)
    except json.JSONDecodeError:
        version = data
    if flag:
        version = data
        with open(v_path, "w") as version_file:
            json.dump(version, version_file)

    return version


if __name__ == '__main__':
    version = version_control("../res/data/version.json", True)
    print(version)

