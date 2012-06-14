import argparse
import os
import datetime
import re
import yaml
import fnmatch

# stats
files_parsed = 0
files_collected = 0
files_scanned = 0

def is_exception(filename, config):
    """
    Check to see if the filename is on the config exceptions list
    """
    if 'exceptions' in config:
        filename_lower = filename.lower()
        # do case insensitive match of filename against exceptions and return the outcome
        return any(filename_lower == val.lower() for val in config['exceptions'])
    else:
        return False


def get_files(dir_path, file_mask, recursive, config):
    """
    Gets all the files that will be processed.
    This takes the mask into account as well as the criteria set.
    """
    global files_collected
    global files_scanned
    
    # initialise a list for the files
    files=[]
    for dirname, dirnames, filenames in os.walk(dir_path):
        # run through sub dirs if the recursive option is true
        if recursive:
            for subdirname in dirnames:
                get_files(subdirname, True, config)
        for filename in filenames:
            if fnmatch.fnmatch(filename, file_mask): 
                if not is_exception(filename, config):
                    files_scanned += 1
                    file_path = "%s\%s" % (dirname, filename)
                    if 'criteria' in config:
                        if can_process_file(file_path, config['criteria']): 
                            print 'Adding %s to process list.' % filename
                            files.append(file_path)  
                            files_collected += 1
                        else:
                            print 'Skipping file %s for not matching criteria.' % filename
                    else:
                        print 'Adding %s to process list.' % filename
                        files.append(file_path)  
                        files_collected += 1
                else:
                    print 'Skipping file %s for being an exception.' % filename
    return files

def can_process_file(file_path, criteria):
    """ 
    Use the criteria yaml config to determine if this file
    should be put in the list for processing.
    """
    file_handle = open(file_path, 'r')
    for line in file_handle:
        if re.search(criteria, line) != None:
            file_handle.close()
            return True
    file_handle.close()        
    return False
    
def process_file(file_handle, parse_config):
    file_contents = file_handle.read()
    file_handle.seek(0)
    if 'replace' in parse_config:
        for c in parse_config['replace']:
            file_contents = re.sub(c['find'], c['replace'], file_contents)
    if 'remove' in parse_config:
        for r in parse_config['remove']:
            file_contents = re.sub(r, '', file_contents)
    file_handle.truncate()
    file_handle.write(file_contents)
    return file_handle
            
def process_files(file_list, parse_config):
    global files_parsed
    
    for f in file_list:
        try:
            file = open(f, 'r+')
            print 'Processing: %s' % f
            new_file = process_file(file, parse_config)          
        except IOError as err:
            print 'There was a file error for %s.' % (f)
            print err
        except Exception as err:
            print "There was an error processing file %s: %s" % (f, err.message)
        else:
            files_parsed += 1
            new_file.close()
            print 'Complete: %s' % f

def main(): 
    p = argparse.ArgumentParser(description="Mass edit text files.")
    p.add_argument('config', metavar='C', type=str, help='Config file to use.')
    p.add_argument('dir', metavar='D', type=str, help='Directory to search for files to change.')
    p.add_argument('--recursive', '-r', action="store_false", default=False, help='Recursivly search for files inside dir.')
    args = p.parse_args()
    
    config = parse_yaml(args.config)
    
    for parser in config: 
        print 'Parsing files for: %s' % parser['name']
        files = get_files(args.dir, parser['mask'], args.recursive, parser)
        process_files(files, parser)
    
    print """
Finished!
Files scanned: %d
Files matched: %d
Files parsed: %d
    """ % (files_scanned, files_collected, files_parsed)
 
def parse_yaml(file_path):   
    return yaml.load(file(file_path, 'r'))

    
if __name__ == '__main__':
    main()
    
    
