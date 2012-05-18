import optparse
import os
import datetime

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

def get_aspx_files(dir_path, recursive):
    # initialise a list for the aspx files
    aspx_files=[]
    for dirname, dirnames, filenames in os.walk(dir_path):
        # run through sub dirs if the recursive options is true
        if recursive:
            for subdirname in dirnames:
                get_aspx_files(subdirname, True)
        for filename in filenames:
            if filename[-4:] == 'aspx':
                aspx_files.append("%s\%s" % (dirname, filename))                
    return aspx_files
 
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
    p = optparse.OptionParser()
    p.add_option('--dir', '-d', default='.', help='The directory to search for aspx files.')
    p.add_option('--recursive', '-r', action="store_false", default=False, help='Recursivly search for aspx files inside dir.')
    p.add_option('--logfile', '-l', default=None, help='Log file to output results and file lists.')
    (options, args) = p.parse_args()
    # get all the aspx files to work with
    aspx_files = get_aspx_files(options.dir, options.recursive)
    for file_path in aspx_files:
        file = open(file_path)
        print 'Checking file %s.' % file_path
        if not can_process_file(file, file_path):
            print 'The file %s cannot be processed automatically.' % file_path
        file.close()
        
    if options.logfile:
        write_to_log(options.logfile)
    
    print """
    Finished!
    Files parsed: %d
    Files Rejected: %d
    """ % (files_parsed, files_rejected)
        
    
if __name__ == '__main__':
    main()
    
    
