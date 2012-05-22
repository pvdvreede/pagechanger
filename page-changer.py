import argparse
import os
import datetime
import re
import yaml
import fnmatch

# tags in file to look for
HEAD = '<head'
HEAD_END = '</head>'
SCRIPT = '<script'
STYLE = '<style'
BODY_END = '</body>'

CURRENT_MASTER_IDENT = '<%=msHtmlHead%>'

# stats
files_parsed = 0
files_rejected = 0
files_updated = 0

# array of parsable and rejected files
rejected_list = []
parseable_list = []
non_master_list = []

def get_files(dir_path, file_mask, recursive):
    # initialise a list for the files
    files=[]
    for dirname, dirnames, filenames in os.walk(dir_path):
        # run through sub dirs if the recursive options is true
        if recursive:
            for subdirname in dirnames:
                get_files(subdirname, True)
        for filename in filenames:
            if fnmatch.fnmatch(filename, file_mask):
                print 'Adding %s to process list.' % filename
                files.append("%s\%s" % (dirname, filename))                
    return files

def process_file(file_handle, parse_config):
    for line in file_handle:
        for r in parse_config['remove']:
            line = re.sub(r, '', line)
            file_handler.write(line)
    return file_handle
            
def process_files(file_list, parse_config):
    for f in file_list:
        try:
            file = open(f, 'r+')
            print 'Processing: %s' % f
            new_file = process_file(file, parse_config)
            new_file.close()
        except IOError as err:
            print 'There was a file error for %s: %s' % (f, err)
            file.close()
            
                
    
def can_process_file(file_handle, file_path):
    global files_parsed
    global files_rejected
    global rejected_list
    global parseable_list
    global non_master_list
    
    eligable_file = False
    
    # check to see if its even using the current inheritence setup
    for line in file_handle:
        if line.find(CURRENT_MASTER_IDENT) != -1:
            eligable_file = True
            break
    # if not then log and dont bother re processing the file
    if not eligable_file:
        non_master_list.append(file_path)
        return False
    
    # reset the file cursor
    file_handle.seek(0)
    
    files_parsed += 1
    
    head_pos = False  
    body_end_pos = False
    for line in file_handle:
        if line.find(HEAD) != -1:
            head_pos = True
            continue
        if line.find(HEAD_END) != -1:
            head_pos = False
            continue
        if line.find(BODY_END) != -1:
            body_end_pos = True
            continue
        if line.find(SCRIPT) != -1:
            if head_pos or body_end_pos:
                files_rejected += 1
                rejected_list.append(file_path)
                return False
        if line.find(STYLE) != -1:
            if head_pos or body_end_pos:
                files_rejected += 1
                rejected_list.append(file_path)
                return False
    parseable_list.append(file_path)
    return True

def write_to_log(file_path):
    file = open(file_path, 'w')
    file.write('Master page parsing bot\n')
    file.write('Run time: %s\n' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    file.write('Files parsed: %d\n' % files_parsed)
    file.write('Files rejected: %d\n' % files_rejected)
    file.write('\n')
    file.write('The following files are parseable:\n')
    for path in parseable_list:
        file.write('%s\n' % path)
    file.write('\n')
    file.write('The following files have to be done manually:\n')
    for path in rejected_list:
        file.write('%s\n' % path)
    file.write('\n')
    file.write('The following files dont use the current MXCWebPage inheritence so may or maynot need master page addition:\n')
    for path in non_master_list:
        file.write('%s\n' % path)
    file.close()
    
def main(): 
    p = argparse.ArgumentParser(description="Mass edit text files.")
    p.add_argument('config', metavar='C', type=str, help='Config file to use.')
    p.add_argument('dir', metavar='D', type=str, help='Directory to search for files to change.')
    p.add_argument('--recursive', '-r', action="store_false", default=False, help='Recursivly search for files inside dir.')
    p.add_argument('--logfile', '-l', default=None, help='Log file to output results and file lists.')
    args = p.parse_args()
    
    config = parse_yaml(args.config)
    
    for parser in config: 
        print 'Parsing files for: %s' % parser['name']
        files = get_files(args.dir, parser['mask'],args.recursive)
        process_files(files, parser)
    
    if args.logfile:
        write_to_log(options.logfile)
    
    print """
    Finished!
    Files parsed: %d
    Files Rejected: %d
    """ % (files_parsed, files_rejected)
 
def parse_yaml(file_path):   
    return yaml.load(file(file_path, 'r'))

    
if __name__ == '__main__':
    main()
    
    
