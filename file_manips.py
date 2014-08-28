#!/usr/bin/env python
#
# file_manips.py
#
# A collection of useful methods for manipulating strings with respect to file
# paths and filenames
#
# Author A R Back - 31/01/2014 <ab571@sussex.ac.uk> : First revision
###############################################################################
import shutil
import list_manips
import os

def cut_path(path):
    """ When supplied a filepath, returns a substring that is the just the 
    filename
    """
    filename = path[path.rfind("/")+1:]
    return filename

def split_path(path):
    """ When supplied a filepath, returns a tuple of the filename and 
    directories
    """
    dir_ = path[:path.rfind("/")+1]
    filename = path[path.rfind("/")+1:]
    return (dir_, filename)

def strip_ext(filename):
    """ Returns a filename without its file extension e.g. myFile.cc would
    return myFile
    """
    s=filename
    sub=s[:s.find(".")]
    return sub

def split_ext(filename):
    """ As strip_ext, but returns the filename and extension in a tuple """
    s=filename
    name=s[:s.find(".")]
    ext=s[s.find("."):]
    return name, ext

def copy_file(source, destination, passnum=1, version=2, overwrite=False):
    """ A useful function to handle copying files to a different directory
    """
    def get_true_dest_from_message(detail):
        message = str(detail).split()
        if (message[2] == "'/home/ashley/Google"): # For Google Drive ONLY
            true_dest = message[2]+" "+message[3] 
        else:
            true_dest = message[2]
        true_dest = true_dest[1:-1] # strip excess "'"
        return true_dest

    is_copied = False
    while not is_copied:
        try:
            shutil.move(source, destination)
            is_copied = True
            print "writing to", destination
        except shutil.Error as detail:
            print "file_manips.copy_file: warning,", detail
            true_dest = get_true_dest_from_message(detail)
            path, file_name = split_path(true_dest)
            name, ext = split_ext(file_name)
            if (name.find("p") == -1):
                new_source = name + "_p" + str(passnum) + ext
                os.rename(source, new_source)
                source = new_source
                print "file_manips.copy_file: warning, renaming source file to:"
                print source
            if overwrite:
                print "file_manips.copy_file: warning, file:"
                print " -->", true_dest
                print "will be overwritten, do you wish to continue y/[n]"
                delete_file = raw_input()
                if (delete_file == "y"):
                    os.remove(true_dest)
                else:
                    print "moving", source, "to", true_dest, "aborted!"
                    is_copied = True
            else:
                new_source = name[:name.find("_p" + str(passnum))+3] 
                new_source += "_q" + str(version) + ext
                os.rename(source, new_source)
                source = new_source
                print "file_manips.copy_file: warning, renaming source file to:"
                print source
                version += 1
