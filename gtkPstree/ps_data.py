from opsys.process_status import ProcessTreeNode
import copy

data = [
    {'pid2node': {
        1: ProcessTreeNode('bash',   'R', 1, 0, 1000, 0, [], []),
        2: ProcessTreeNode('bash',   'S', 2, 0, 1000, 0, [], []),
        3: ProcessTreeNode('perl',   'R', 3, 0, 1000, 0, [], []),
        4: ProcessTreeNode('bash',   'T', 4, 0, 1000, 0, [], []),
        },
    'levels': [ [1, 2, 3, 4], ]
     },
    {'pid2node': {
        3009: ProcessTreeNode('gnome-keyring-dddd', 'R', 3009, 1931, 1000, 0, [], []),
        3011: ProcessTreeNode('init',            'S', 3011,    1, 1000, 0, [], []),
        3098: ProcessTreeNode('dbus-daemon',     'R', 3098, 3011, 1000, 1, [], []),
        3108: ProcessTreeNode('mediascanner',    'T', 3108, 3011, 1000, 1, [], []),
        3112: ProcessTreeNode('upstart',         'R', 3112, 3011, 1000, 1, [], []),
        3117: ProcessTreeNode('url-dispatcher',  'S', 3117, 3112, 1000, 2, [], []),
        3218: ProcessTreeNode('bamfdaemon',      'R', 3218, 3112, 1000, 2, [], []),
        3995: ProcessTreeNode('cat',             'R', 3995, 3218, 1000, 3, [], []),
        },
    'levels': [ [3009, 3011],
               [3098, 3108, 3112],
               [3117, 3218],
               [3995], ]
     },
    {'pid2node': {
        1: ProcessTreeNode('bash',   'R', 1, 0, 1000, 0, [], []),
        2: ProcessTreeNode('bash',   'S', 2, 0, 1000, 0, [], []),
        3: ProcessTreeNode('perl',   'R', 3, 0, 1000, 0, [], []),
        4: ProcessTreeNode('bash',   'T', 4, 0, 1000, 0, [], []),
        5: ProcessTreeNode('bash',   'R', 5, 1, 1000, 1, [], []),
        6: ProcessTreeNode('ssh',    'S', 6, 4, 1000, 1, [], []),
        7: ProcessTreeNode('glade',  'R', 7, 5, 1000, 2, [], []),
        8: ProcessTreeNode('python', 'R', 8, 5, 1000, 2, [], []),
        },
     'levels': [ [1, 2, 3, 4], [5, 6], [7, 8] ],
     },
    {'pid2node': {
        1: ProcessTreeNode('bash',   'R', 1, 0, 1000, 0, [], []),
        2: ProcessTreeNode('bash',   'S', 2, 0, 1000, 0, [], []),
        3: ProcessTreeNode('perl',   'R', 3, 2, 1000, 1, [], []),
        4: ProcessTreeNode('bash',   'T', 4, 2, 1000, 1, [], []),
        5: ProcessTreeNode('bash',   'R', 5, 2, 1000, 1, [], []),
        6: ProcessTreeNode('ssh',    'S', 6, 2, 1000, 1, [], []),
        7: ProcessTreeNode('glade',  'R', 7, 2, 1000, 1, [], []),
        8: ProcessTreeNode('python', 'R', 8, 2, 1000, 1, [], []),
        },
     'levels': [ [1, 2],
                 [3, 4, 5, 6, 7, 8],
                 ]
     },
    {'pid2node': {
        13: ProcessTreeNode('unity-settings',  'S', 01, 0, 1000, 0, [], []),
        01: ProcessTreeNode('hud-service',     'S', 01, 0, 1000, 0, [], []),
        02: ProcessTreeNode('at-spi-buf-lun',  'S', 02, 0, 1000, 0, [], []),
        03: ProcessTreeNode('gnome-session',   'S', 03, 0, 1000, 0, [], []),
        04: ProcessTreeNode('at-spi2-registr', 'S', 04, 0, 1000, 0, [], []),
        05: ProcessTreeNode('indicator-keybo', 'S', 05, 0, 1000, 0, [], []),
        06: ProcessTreeNode('dconf-service',   'S', 06, 0, 1000, 0, [], []),
        07: ProcessTreeNode('glade',           'S', 07, 2, 1000, 1, [], []),
        18: ProcessTreeNode('pokeymon-au',     'S', 18, 3, 1000, 1, [], []),
        19: ProcessTreeNode('nm-applet',       'S', 19, 3, 1000, 1, [], []),
        10: ProcessTreeNode('tracker-store',   'S', 10, 3, 1000, 1, [], []),
        11: ProcessTreeNode('tracker-miner-f', 'S', 11, 3, 1000, 1, [], []),
        12: ProcessTreeNode('tracker-miner-f', 'S', 12, 3, 1000, 1, [], []),
        },
     'levels': [ [13, 1, 2,  3,  4,  5, 6],
                 [7,  8, 9, 10, 11, 12] ]
     },

    ]

def get_data(i):
    item = data[i]
    return item['levels'], copy.deepcopy(item['pid2node'])

if __name__ == '__main__':
    print(get_data(0))
