# page-changer

### File alteration bot for programmatically altering large amount of files with Regular Expressions

page-changer can be used to search through text based files and make change to the text by adding, deleting, changing or a combination of all three.

This is done using a config file to tell page-changer what to alter in what file type.

#### Usage

page-changer uses a config file that you specify as a command line argument to know what files to change.

The format of the config file is:

    <file mask to alter>:
        remove:
            - <reg ex to remove from line>
            
        add:
            - text: <text to place>
              [above | below]: <the line above or below to put the text>
              
        replace: 
            - find: <text to that will be replaced use %rep%>
              replace: <text to replace>