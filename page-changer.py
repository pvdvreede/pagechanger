import argparse
import os
import datetime
import re
import yaml
import fnmatch

# stats
files_parsed = 0
files_collected = 0

# array of parsable and rejected files
parsed_list = []


def get_files(dir_path, file_mask, recursive):
    global files_collected
    
    # initialise a list for the files
    files=[]
    for dirname, dirnames, filenames in os.walk(dir_path):
        # run through sub dirs if the recursive option is true
        if recursive:
            for subdirname in dirnames:
                get_files(subdirname, True)
        for filename in filenames:
            if fnmatch.fnmatch(filename, file_mask):
                print 'Adding %s to process list.' % filename
                files.append("%s\%s" % (dirname, filename))  
                files_collected += 1    
    return files

def process_file(file_handle, parse_config):
    file_contents = file_handle.read()
    file_handle.seek(0)
    for c in parse_config['replace']:
        print c
        file_contents = re.sub(c['find'], c['replace'], file_contents)
    for r in parse_config['remove']:
        print r
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
            raise err
        else:
            files_parsed += 1
            new_file.close()

def main(): 
    p = argparse.ArgumentParser(description="Mass edit text files.")
    p.add_argument('config', metavar='C', type=str, help='Config file to use.')
    p.add_argument('dir', metavar='D', type=str, help='Directory to search for files to change.')
    p.add_argument('--recursive', '-r', action="store_false", default=False, help='Recursivly search for files inside dir.')
    args = p.parse_args()
    
    config = parse_yaml(args.config)
    
    for parser in config: 
        print 'Parsing files for: %s' % parser['name']
        files = get_files(args.dir, parser['mask'], args.recursive)
        process_files(files, parser)
    
    print """
Finished!
Files matched: %d
Files parsed: %d
    """ % (files_collected, files_parsed)
 
def parse_yaml(file_path):   
    return yaml.load(file(file_path, 'r'))

    
if __name__ == '__main__':
    main()
    
    
