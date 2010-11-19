#!/usr/bin/env python

import sys
import os
import getopt
import optparse

sys.path.append(os.path.join(sys.path[0], '../lib'))
import ReleaseManagerLib

def usage():
    print "%s <version> <SourceDir> <ReleaseDir>" % os.path.basename(sys.argv[0])
    print "Example: %s v2.5 /tmp/glideinWMS /tmp/release_dir" % os.path.basename(sys.argv[0])

def parse_opts(argv):
    parser = optparse.OptionParser(usage='%prog [options]',
                                   version='v0.1',
                                   conflict_handler="resolve")
    parser.add_option('--release-version',
                      dest='relVersion',
                      action='store',
                      metavar='<release version>',
                      help='glideinWMS version to release')
    parser.add_option('--source-dir',
                      dest='srcDir',
                      action='store',
                      metavar='<source directory>',
                      help='directory containing the glideinWMS source code')
    parser.add_option('--release-dir',
                      dest='relDir',
                      action='store',
                      metavar='<release directory>',
                      help='directory to store release tarballs and webpages')
    
    if len(argv) < 4:
        print "ERROR: Insufficient arguments specified"
        parser.print_help()
        sys.exit(1)
    options, remainder = parser.parse_args(argv)
    if len(remainder) > 1:
        parser.print_help(file)
    if not required_args_present(options):
        print "ERROR: Missing required arguments"
        parser.print_help()
        sys.exit(1)
    return options
    
def required_args_present(options):
    if ( (options.relVersion == None) or
         (options.srcDir == None)  or
         (options.releaseDir == None)):
        return False
    return True
#   check_required_args


#def main(ver, srcDir, relDir):
def main(argv):
    options = parse_opts(argv)
    sys.exit(1)
    ver = options.relVersion
    srcDir = options.srcDir
    relDir = options.releaseDir
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
    main(sys.argv)
