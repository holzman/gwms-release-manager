#!/usr/bin/env python

import sys
import os
sys.path.append(os.path.join(sys.path[0], '../lib'))
import ReleaseManagerLib


def usage():
    print "%s <version> <SourceDir> <ReleaseDir>" % os.path.basename(sys.argv[0])
    print "Example: %s v2.5 /tmp/glideinWMS /tmp/release_dir" % os.path.basename(sys.argv[0])

def main(ver, srcDir, relDir):
    print "___________________________________________________________________"
    print "Creating following glideinWMS release"
    print "Version=%s\nSourceDir=%s\nReleaseDir=%s" % (ver, srcDir, relDir)
    print "___________________________________________________________________"
    print 
    rel = ReleaseManagerLib.Release(ver, srcDir, relDir)

    rel.addTask(ReleaseManagerLib.TaskClean(rel))
    rel.addTask(ReleaseManagerLib.TaskSetupReleaseDir(rel))
    #rel.addTask(ReleaseManagerLib.TaskPylint(rel))
    rel.addTask(ReleaseManagerLib.TaskVersionFile(rel))
    rel.addTask(ReleaseManagerLib.TaskTar(rel))
    rel.addTask(ReleaseManagerLib.TaskFrontendTar(rel))
    rel.addTask(ReleaseManagerLib.TaskFactoryTar(rel))
 
    rel.executeTasks()
    rel.printReport()
     
if __name__ == "__main__":
    if (len(sys.argv) != 4):
        usage()
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])
