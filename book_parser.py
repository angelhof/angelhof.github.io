import argparse
import os

from datetime import datetime

def export(filename, content):
    with open(filename, 'w') as html_file:
        html_file.write(content)

def convert_date(date_str):
    # Parse the input date string
    date_obj = datetime.strptime(date_str, "%m/%Y")
    
    # Format the date to "mmmm YYYY"
    formatted_date = date_obj.strftime("%B %Y")
    
    return formatted_date

def parse_args():
    parser = argparse.ArgumentParser(
                    prog='Book Parser',
                    description='Parses a books csv to produce an html page')
    parser.add_argument('filename')
    args = parser.parse_args()
    return args


def parse_book_file(filename):
    with open(filename, 'r') as file:
        lines = [line.strip() for line in file.readlines()]

    data = []
    for line in lines:
        words = line.split('|')
        item = {}
        item['title'] = words[0].strip()
        item['author'] = words[1].strip()
        item['date'] = words[2].strip()
        item['location'] = words[3].strip()
        if len(words) >= 5 and words[4].strip() == '*':
            item['starred'] = True
        else:
            item['starred'] = False
        
        ## Hide a book from the public list
        hidden = False
        if len(words) >= 6 and words[5].strip() == "hidden":
            hidden = True
        if not hidden:
            data.append(item)
    return data


def format_books(data):
    output_html = ""
    output_html += f'<ul>\n'
    for item in data:
        output_html += generate_book_html(item)
    output_html += "</ul>\n"
    return output_html

def generate_book_html(item):
    output = f'<li> {item["title"]} -- {item["author"]} -- {convert_date(item["date"])}'
    if item['starred']:
        output += ' <b>*</b>'
    output += '</li>\n'
    return output

args = parse_args()
data = parse_book_file(args.filename)
output_html = format_books(data)
export('book-list.html', output_html)