import optparse
import os

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
    
def main():
    p = optparse.OptionParser()
    p.add_option('--dir', '-d', default='.', help='The directory to search for aspx files.')
    p.add_option('--recursive', '-r', action="store_false", default=False, help='Recursivly search for aspx files inside dir.')
    (options, args) = p.parse_args()
    # get all the aspx files to work with
    aspx_files = get_aspx_files(options.dir, options.recursive)
    print aspx_files
    
if __name__ == '__main__':
    main()
    
    
