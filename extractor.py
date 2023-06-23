import re
import datetime
import os
import pathlib

def extract_files(message, output_dir=None):
    if not output_dir:
        output_dir = f'out{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}'
    
    os.mkdir(output_dir)

    parser_on = False
    inside_file = False

    for line in message.split("\n"):
        if line == '```':
            continue
        
        if line.startswith("[START!]"):
            parser_on = True
            continue
        
        if parser_on:
            if line.startswith("[START "):
                file_content = ""
                filename = re.search(r"\[START (.*)\]", line).group(1)
                if not filename:
                    raise Exception("Filename not found!")
                
                inside_file = True
            elif line.startswith("[END "):
                print(f"  {filename}")
                with open(pathlib.Path(output_dir) / filename, "w") as f:
                    f.write(file_content)
                
                inside_file = False
            elif line.startswith("[END!]"):
                parser_on = False
            elif inside_file:
                file_content += line + "\n"
