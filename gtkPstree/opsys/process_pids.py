import os
def ListPID(path, owner=None):

    l = []
    pids = os.listdir(path)
    for pid in pids:
        fullname = path + '/' + pid
        if os.path.isdir(fullname) and pid[0].isdigit():
            if owner is None or owner == os.stat(fullname).st_uid:
                # print("XXX ", pid)  # debug
                l.append(pid)
    return l

if __name__ == '__main__':
    print(ListPID('/proc'))
