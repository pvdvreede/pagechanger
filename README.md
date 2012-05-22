# page-changer

### File alteration bot for programmatically altering large amount of files with Regular Expressions

page-changer can be used to search through text based files and make change to the text by adding, deleting, changing or a combination of all three.

This is done using a config file to tell page-changer what to alter in what file type.

#### Installation

page-changer is a single file script so it can just be downloaded on its own. 

It does have a dependancy on [PyYAML](http://pyyaml.org/wiki/PyYAML), so this needs to be installed on the system along with Python.

#### Usage

page-changer uses a YAML config file that you specify as a command line argument to know what files to change.

The format of the config file is:

      - name: <name of the set>
        remove:
            - <reg ex to remove from line>
            
        add:
            - text: <text to place>
              position: [above | below]
              current: <the text to place above or below>
              
        replace: 
            - find: <text to that will be replaced use %rep%>
              replace: <text to replace>
                
      - name: ... <put n or more parser sets, to parse different file types, or alterations required>

An example file would be:

    - name: html
      mask: 'Search.html'
      remove:
      - <head>
      - <html xmlns="http://www.w3.org/1999/xhtml">
      - </head>
      - <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
      - </html>
      - </body>
      - <body>
      replace:
      - find: colou*r
        replace: something else

To run the config over a set of files use the command line tool:

    python page-changer.py config.yaml /path/to/files/to/search
    
Here are the command line options and arguments:

    usage: page-changer.py [-h] [--recursive] C D

    Mass edit text files.

    positional arguments:
      C                Config file to use.
      D                Directory to search for files to change.

    optional arguments:
      -h, --help       show this help message and exit
      --recursive, -r  Recursivly search for files inside dir.