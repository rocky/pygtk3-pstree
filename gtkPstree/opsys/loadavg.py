import re
from collections import namedtuple

LoadAvg = namedtuple('LoadAvg',
                     'Last1Min Last5Min Last15Min ProcessRunning ProcessTotal LastPID'
                     )

def ReadLoadAvg(path):

    loadavg = None
    with open(path) as fd:
        for line in fd.readlines():

            fields = re.split('\s+', line.strip())

            if len(fields) < 5:
                raise TypeError, "Cannot parse loadavg, need 5 fields: " + content

            process = fields[3].split("/")

            if len(process) != 2:
                raise TypeError, "Missing / in field 3 of load average " + content

            Last1Min = float(fields[0])
            Last5Min = float(fields[1])
            Last15Min= float(fields[2])
            ProcessRunning = int(process[0])
            ProcessTotal = int(process[1])
            LastPid = int(fields[4])
            loadavg = LoadAvg(Last1Min, Last5Min, Last15Min, ProcessRunning, ProcessTotal,
                              LastPid)
            pass
        pass
    return loadavg

if __name__ == '__main__':
    loadavg = ReadLoadAvg('/proc/loadavg')
    print(loadavg)
