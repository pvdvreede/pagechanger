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
