The program displays and continuously updates using PyGTK the GNU/Linux processes as a tree or forest. The roots of the tree are on the left-hand side and the leaf processes (with no children) are on the right-hand side. The status of each process (running, sleeping, stopped, etc.) can be indicated by a color. Different users can appear as different colors too.

Within each level, processes are grouped so that those with the same parent process id are grouped together. Within this, processes are arranged by userid with lower number uid's appearing towards the top. In general, the order of children is the order in which they were spawned, with the older processes appearing towards towards the top.

In contrast to pstree and many tree-widget based programs, the overall tree display uses diagonal lines; some effort is made to effectively use the full 2-dimensional area of the screen by balancing levels and centering the children of a node between their parent. A goal of the program is to visually give a picture of what's going on. So when possible processes are kept close to their parents so one needn't scroll around too much and so that there isn't a lot of redrawing as processes are created or destroyed.

One can click on a process to get more information (via ps) about that process.

This is a port of the older C and Motif X program `xps <http://motif-pstree.sourceforge.net>`_.
