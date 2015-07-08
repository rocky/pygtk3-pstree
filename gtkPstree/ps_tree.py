from pwd import getpwuid
from opsys.process_pids import ListPID
from opsys.process_status import GetProcessTreeNode


class PsTree():

    def __init__(self, debug=False):
        self.debug = debug
        self.id2name = {}
        self.reset()
        return

    def reset(self):
        self.pid2node = {}

    def get_id2name(self, uid):
        """For a given uid, return the uid's name. We cache in id2name
        results since this is done over and over and doesn't change."""
        try:
            if uid in self.id2name: return self.id2name[uid]
            entry = getpwuid(uid)
            self.id2name[uid] = entry.pw_name
            return entry.pw_name
        except KeyError:
            return '??'

    def dumpLevels(self,  levels):
        assert isinstance(levels, list)
        for i, level in enumerate(levels):
            print("Level %d len: %d" % (i, len(level),))
            for j, pid in enumerate(level):
                info = self.pid2node[pid]
                if info is None: continue
                print("%d: pid %d (%s), ppid %d, kids: %d" %
                      (j, info.Pid, info.Name, info.PPid, len(info.Children),))
                pass
            pass
        return

    def levelSort(self, pids, roots):
        levels = [roots]
        worklist = list(roots)
        maxDepth = 0
        i = 0
        # from trepan.api import debug; debug()
        while i < len(worklist):
            # println(i, len(worklist)) // debug
            node = self.pid2node[worklist[i]]
            depth = node.Depth + 1
            if depth > maxDepth and(node.Children) > 0:
                levels.append([])
                maxDepth = depth
                pass
            for child in node.Children:
                childNode = self.pid2node[child]
                self.pid2node[child] = childNode._replace(Depth=depth)
                childNode = self.pid2node[child]
                levels[depth].append(childNode.Pid)
                worklist.append(child)
                # if i > 10: break # debug
                pass
            i += 1
            pass

        if self.debug: self.dumpLevels(levels)
        return levels

    def buildChildren(self, pids):
        """Build a list of children for each pid and find the roots of the
        trees"""
        roots = []
        for pid in pids:
            node = self.pid2node[pid]
            ppid = int(node.PPid)
            if ppid == 0 or ppid not in self.pid2node:
                roots.append(pid)
                self.pid2node[pid] = node._replace(Depth=0)
            else:
                parent = self.pid2node[self.pid2node[ppid].Pid]
                parent.Children.append(pid)
                pass
            pass

        if self.debug: print("Roots:", len(roots))
        for i, root in enumerate(roots):
            info = self.pid2node[root]
            if self.debug:
                print("%d: pid %d (%s), %d, uid %s" %
                      (i, info.Pid, info.Name, info.PPid,
                       self.get_id2name(info.RealUid),))
            pass
        levels = self.levelSort(pids, list(roots))
        return levels, self.pid2node

    def GatherPidInfo(self, pids):
        ipids = []
        for pid in pids:
            pseudoStatFile = "/proc/" + pid + "/status"
            info = GetProcessTreeNode(pseudoStatFile)
            if info is not None:
                # print("pid %s (%s), %d, %s, uid %d (%s)" %
                #        (pid, info.Name, info.PPid, info.State, info.RealUid,
                #     			get_id2name(info.RealUid),))
                self.pid2node[info.Pid] = info
                ipids.append(info.Pid)
            else:
                print("Error getting info on %s" % pid)
                pass
            pass
        return ipids


if __name__ == '__main__':
    pstree = PsTree(debug=True)
    # user = 1000
    user = None
    pids = ListPID("/proc", user)
    ipids = pstree.GatherPidInfo(pids)
    pstree.buildChildren(ipids)
    pass
