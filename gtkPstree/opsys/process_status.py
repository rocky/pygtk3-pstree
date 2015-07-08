import re
from collections import namedtuple

ProcessTreeNode = namedtuple('ProcessTreeNode',
                             'Name State Pid PPid RealUid Depth PosInfo Children')

def GetProcessTreeNode(path):

    status = ProcessTreeNode(None, None, None, None, None, None, [], [])
    with open(path) as fd:
        for line in fd.readlines():
            fieldCount = 0
            if ':' not in line: continue
            l = line.split(":")
            k = l[0].strip()
            v = l[1].strip()

            if k == "Name":
                status = status._replace(Name = v)
                fieldCount += 1
            elif k == "State":
                status = status._replace(State = v)
                fieldCount += 1
            elif k == "Pid":
                status = status._replace(Pid = int(v))
                fieldCount += 1
            elif k == "PPid":
                status = status._replace(PPid = int(v))
                fieldCount += 1
            elif k == "Uid":
                f = re.split('\s+', v)
                if len(f) == 4:
                    status = status._replace(RealUid = int(f[0]))
                    fieldCount += 1
                    pass
                pass
            if fieldCount == 5: break
            pass
        pass
    return status


if __name__ == '__main__':
    status = GetProcessTreeNode('/proc/1/status')
    print(status)
