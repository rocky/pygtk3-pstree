def clamp(x, lower, upper):
    return lower if x < lower else upper if x > upper else x


def IsDegree1(level, pid2node):
    for pid in level:
        if pid2node[pid].Children != 1: return False
        pass
    return True

ROOT_LEVEL = 0  # depth of root level


def arrange(levels, pid2node,
            width, debug=False, MIN_XSPACE=10, MIN_YSPACE=10, MAX_XSPACE=30,
            fontHeight=17):
    """Add printing coordinates to pids in pid2node. This routine uses
    as input process nodes sorted by level and position. This information is in
    'levels'. The roots are given in 'levels[0]'. Within a level
    pids are grouped by the parent process they belong to.

    A list of the starting X positions is returned.

    This is port from the C code of the same name.
    """
    global ROOT_LEVEL
    # MAX_XSPACE = 30  # Make artificially too small for testing. */

    maxDepth = max([len(l) for l in levels])

    # Compute the new height of the canvas.
    new_height = (maxDepth+1) * (fontHeight+MIN_YSPACE)

    if maxDepth == 0: return []

    # Compute the number of empty pixels to distribute horizontally
    # between words.

    Virtual_Breadth = []
    treeDepth = len(levels)-1
    xfill = width
    yspace = 0
    max_ypos = MIN_YSPACE
    maxlabels = []
    for i, level in enumerate(levels):
        # FIXME: there is a bug here
        ll = len(level)
        maxlabel = max([len(pid2node[i].Name) for i in level] + [0])
        maxlabels.append(maxlabel)
        Virtual_Breadth.append(ll)

        # If we know there is going to be a big fanout, increase the
        # width between levels by adding to MaxLabel
        if i < treeDepth and ll+5 < len(levels[i+1]):
            maxlabel += 50
            pass

        if (xfill > maxlabel):
            xfill -= maxlabel
            pass
        pass

    xfill = 65  # FIXME
    xspace = xfill / (treeDepth + 1)
    if debug:
        print("width %d, xfill: %d, xspace %d"
              % (width, xfill, xspace))
        print("maxDepth %d" % maxDepth)
        pass

    # Keep horizontal spacing withing acceptable bounds
    xspace = clamp(xspace, MIN_XSPACE, MAX_XSPACE)

    next_xpos = xspace >> 1
    last_node = None

    # Position each node of the tree. Keep track of the maximum boundaries...
    new_width = 0
    levels_x = []
    for i, level in enumerate(levels):
        ll = len(level)

        # Compute the next level's horizontal position.
        xpos = next_xpos
        levels_x.append(xpos)
        next_xpos = xpos + maxlabels[i]*fontHeight/2 + xspace

        new_width = max(new_width, next_xpos - xspace)

        if IsDegree1(level, pid2node):
            #  Set position of each node on this level horizontally
            # across from its parent. */ I believe the other
            # heuristics will catch this case so we could in theory
            # remove this. However handling this special case is easy,
            # and fast.

            if debug:
                print("Level %ld degree 1 parent" % i)

            Virtual_Breadth[i] = Virtual_Breadth[i-1]

            for j, pid in enumerate(level):
                node = pid2node[pid]
                parent = pid2node[node.PPid]
                if len(node.PosInfo) != 0: del node.PosInfo[0:]
                vrank, rank, x, y = parent.PosInfo
                node.PosInfo.extend((vrank, j, xpos, y))
                pass
            pass
        else:
            ypos = 0
            virtual_rank = 0
            child = 0            # Which child of parent am I?

            #  Use previous spacing unless this level has more
            #  children than last.
            if i == ROOT_LEVEL or ll > Virtual_Breadth[i-1]:
                yspace = (new_height - ll*fontHeight) / ll
                # Keep vertical spacing withing acceptable bounds.
                yspace = max(MIN_YSPACE, yspace)
            else:
                Virtual_Breadth[i] = Virtual_Breadth[i-1]

            # if debug: print("yspace %d" % yspace)

            virtual_rank = 0
            # Position vertically by equally distributing the space.
            for j, pid in enumerate(level):
                node = pid2node[pid]
                # if node.Name == 'nautilus':
                #     from trepan.api import debug; debug()
                y = ypos + ((yspace+1) >> 1)
                node_y = y + fontHeight
                ypos = node_y + (yspace >> 1)
                if ypos > max_ypos: max_ypos = ypos
                # print("XXX pid: %d x: %d, y: %d" % (pid, xpos, node_y))
                # if pid == 8: debug()
                node.PosInfo.extend((virtual_rank, j, xpos, node_y))
                virtual_rank += 1

                if i == ROOT_LEVEL: continue

                # Which child of the parent are we?
                if last_node and node.PPid == last_node.PPid:
                    child += 1
                else:
                    child = 1
                    pass

                parent = pid2node[node.PPid]
                virtual_rank_diff = node.PosInfo[0] - parent.PosInfo[0]

                if virtual_rank_diff < 0 and \
                       Virtual_Breadth[i] == Virtual_Breadth[i-1]:
                    # Parent is further down than this node and we the virtual
                    # we are using the same virtual breadth.
                    #
                    # Try position the virtual rank so the mid child
                    # is as close to or less to the rank of the
                    # parent, but not so much that the overall virtual
                    # breadth is not increased.
                    #
                    #   NOTE: all *diff things are measured in the
                    #   negative! (or up)
                    togo = ll - node.PosInfo[1]
                    # from trepan.api import debug; debug()
                    diff = Virtual_Breadth[i-1] - parent.PosInfo[0] - togo
                    child_diff = child - (len(parent.Children) >> 1)+1

                    if diff >= 0:
                        # This node room to spare, even if it is
                        # across from the parent. Set for this since
                        # we don't want it further down than that.
                        diff = 0
                        pass

                    if child_diff < diff:
                        # As positioned now, the mid child would be
                        # further down than its parent. Adjust the mid
                        # child up if possible.
                        if virtual_rank_diff < child_diff:
                            diff = child_diff
                        else:
                            # Just keep things the way they were going
                            # to be anyway.
                            diff = 0
                            pass
                        pass

                    new_virtual_rank = parent.PosInfo[0] + diff

                    new_ypos = parent.PosInfo[3] + (diff*(yspace+fontHeight))

                    # The below tends to position the first children
                    # across from the parent when we'd really like the
                    # mid child positioned across, all things being
                    # equal.

                    if node.PosInfo[0] <= new_virtual_rank:
                        virtual_rank = new_virtual_rank
                        node.PosInfo[0] = virtual_rank
                        node.PosInfo[3] = new_ypos
                        ypos = node.PosInfo[3] + (yspace >> 1)
                        pass
                    pass
                last_node = node
                pass
            pass
        pass

    return next_xpos, new_height + ((fontHeight+MIN_YSPACE) << 1), \
           levels_x + [next_xpos]
