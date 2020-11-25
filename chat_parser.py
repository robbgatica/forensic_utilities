""" 
Script Name: chat_parser.py
Version: 1.0
Python Version: 3.7
Author: Robb Gatica

This script parses and organizes cached Discord chat data and outputs it to a readable format (.txt file).  Its not the 
most elegant solution since it requires a separate step before running the script, but it worked for me.  

The Discord 'Cache' folder is located in the user's directory under AppData->Roaming->discord. You will first need to use a 
web cache viewer to view and export all the files.  This one worked for me: https://www.nirsoft.net/utils/chrome_cache_view.html

Once you've copied all the files from the cache viewer to a folder on your computer, run this script against that directory
and it will find all the relevant JSON files and output the results to a text file in the same directory as this script. 

Specifically, this script extracts the following: "id", "content", "author[username]", "timestamp". 

Usage example: python chat_parser.py /Users/username/(directory where you copied cache files)

"""
from __future__ import print_function
from datetime import datetime
import os
import sys
import io
import json

def main():
    folder = ''
    file_content = None
    json_files = []

    # Making sure an argument is passed to the script
    if len(sys.argv) > 1:
        folder = os.path.abspath(sys.argv[1])
    
    # Verify that sys.argv[1] is a directory
    if os.path.isdir(folder):
        print(f'{folder} loaded successfully...')
    else:
        print(f'Directory not found: {folder}')

    # Make a list of all json files that start with '50' or 'limit'
    for root, dirs, files in os.walk(folder):
            for file in files:
                if (file.startswith('50') and file.endswith('.json')) or (file.startswith('limit') and file.endswith('.json')):
                    json_files.append(file)
    
    #Loop through json_files and parse out conversation data
    for file in json_files:
        temp_file = os.path.join(folder, file)
        try: 
            with open(temp_file) as current:
                file_content = json.load(current)
        except:
            print(f'Error loading file: {temp_file}')
            continue

        parse(file_content, file, json_files)

def is_empty(filepath):
    return os.path.exists(filepath) and os.stat(filepath).st_size == 0

def parse(file_content, file_name, file_list):
    filepath = os.path.join(os.getcwd(), 'discord_parsed_chat_log_' + datetime.now().strftime('%m_%d_%Y_%H%M') + '.txt')
    with io.open(filepath, 'a+', encoding='utf-8') as f:
        if is_empty(filepath):
            print(f'*** Total chat files found: {len(file_list)} ***', end='\n\n', file=f)   
        print(f'Transcript for {file_name}', file=f)
        print((len(file_name)+15)*'=', file=f)

        for i, message in enumerate(file_content):
            if 'author' in file_content[i].keys():
                username = message.get('author')['username']
                print(f' Username: {username:<12}', file=f)
            if 'id' in file_content[i].keys():
                message_id = message.get('id')
                print(f'MessageID: {message_id:<12}', file=f)
            if 'timestamp' in file_content[i].keys():
                timestamp = message.get('timestamp')
                print(f'Timestamp: {timestamp:<12}', file=f)
            if 'content' in file_content[i].keys():
                content = message.get('content')
                print(f'  Message: {content:<12}', end='\n\n', file=f)

if __name__ == '__main__':
    main()
    

