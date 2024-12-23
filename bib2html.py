import bibtexparser
import re
import sys
from read_people import *

def parse_bib(filename):
    with open(filename) as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
    return bib_database

##
## Turn the Unicode of bibtexparser to ascii
##

def get_bib_date(entry):
    year = entry['year']
    month = 0
    day = 0
    if 'month' in entry:
        month = int(entry['month'])
    if 'day' in entry:
        day = int(entry['day'])
    return (year, month, day)



##
## Generate HTML
##

def normalize_whitespace(string):
    return " ".join(string.split())

def trim_trailing_superscripts(string):
    if('$' in string):
        return string.split('$')[0]
    else:
        return string

def print_authors_html(authors):
    # Reverse the first with the last name
    authors_list = [author.split(',')[1] + " " + author.split(',')[0] for author in authors.split(' and ')]
    # Normalize Whitespace and remove superscripts
    authors_list = [trim_trailing_superscripts(normalize_whitespace(author.strip()))
                    for author in  authors_list]

    # Remove my name
    authors_list.remove("Konstantinos Kallas")

    authors_list = [find_person(author, PEOPLE).format_html() 
                      if find_person(author, PEOPLE) is not None else author
                    for author in authors_list]

    # Format differently if there are more than 2 authors
    if len(authors_list) == 0:
        authors_string = ""
    if len(authors_list) <= 2:
        authors_string = " and ".join(authors_list)
    else:
        authors_string = ", ".join(authors_list[:-1])
        authors_string += ", and " + authors_list[-1]

    return authors_string

def print_title(title):
    return "<b>" + title + "</b>"

def print_infix(infix):
    if ("In submission" in infix
        or "Work In Progress" in infix):
        return "<i>{}</i>".format(infix)
    else:
        return infix

def format_authors(authors):
    authors_string = print_authors_html(authors)
    output_html = ""
    if(authors_string != ""):
        output_html += "<br/>"
        output_html += " &nbsp; with: " + authors_string + ". "
    return output_html

def generate_general_html(entry_index, entry, infix):
    output_html = ""
    output_html += "<li id=\"" + entry["ID"] + "\">"
    output_html += "[" + str(entry_index) + "] "
    output_html += print_title(entry['title']) + ". "
    output_html += print_infix(infix) + ". "
    # output_html += infix + ", " + entry['year'] + ". "
    if 'note' in entry:
        if entry['note'] == 'accepted':
            output_html += "<i>[Accepted]</i> "
    if 'url' in entry:
        output_html += "(<a href=\"" + entry['url'] + "\">link</a>) "
    if 'file' in entry:
        output_html += "(<a href=\"" + entry['file'] + "\">pdf</a>) "
    if 'talk' in entry:
        output_html += "(<a href=\"" + entry['talk'] + "\">talk</a>) "
    if 'award' in entry:
        output_html += "<br/> &#11088 <em>" + entry['award'] + "</em> &#11088 "
    if 'author' in entry:
        output_html += format_authors(entry['author'])
    output_html += "</li>\n"
    return output_html

def generate_talk_html(entry_index, entry):
    infix = '{}, {}'.format(entry['event'], entry['year'])
    if 'host' in entry:
        infix += '. Host: {}'.format(entry['host'])
    return generate_general_html(entry_index, entry, infix)

def generate_paper_html(entry_index, entry):
    ## WARNING: Maybe it is not always 'booktitle'
    if( 'booktitle' in entry):
        booktitle = entry['booktitle']
    else:
        booktitle = entry['journal']
    return generate_general_html(entry_index, entry, booktitle)

def generate_thesis_html(entry_index, entry):
    return generate_general_html(entry_index, entry, '{}. {}'.format(entry['school'], entry['year']))

def generate_entries_html(entries, counter, heading, entry_handler):
    output_html = ""
    output_html += "<h3 id=\"" + heading.lower() + "\" class=\"page-heading\">"
    output_html += heading + "</h3>\n"
    output_html += "<ul class=\"" + str.lower(heading) + " bibliography\">\n"
    sorted_date_entries = sorted(entries, key=get_bib_date, reverse=True)
    for entry_index in range(len(sorted_date_entries)):
        entry = sorted_date_entries[entry_index]
        if(not 'note' in entry or
           not entry['note'] == 'cv-only'):
            output_html += entry_handler(counter, entry)
            counter += 1
    output_html += "</ul>\n"
    return output_html, counter

def generate_papers_html(entries, counter):
    return generate_entries_html(entries, counter, "Papers", generate_paper_html)

def generate_talks_html(entries, counter):
    return generate_entries_html(entries, counter, "Talks", generate_talk_html)

def generate_theses_html(entries, counter):
    return generate_entries_html(entries, counter, "Theses/Reports", generate_thesis_html)



def get_conf_name(entry):
    ## WARNING: Maybe it is not always 'booktitle'
    if( 'booktitle' in entry):
        booktitle = entry['booktitle']
    else:
        booktitle = entry['journal']
    return booktitle

def get_short_conf_name(entry):
    conf_name = get_conf_name(entry)
    # Match the short conference names in parentheses
    pattern = r'\((.*?)\)'

    # Use re.findall to find all occurrences of the pattern in the input text
    matches = re.findall(pattern, conf_name)

    ## Assert that to make sure this is correct
    assert(len(matches) == 1)
    return matches[0]

def generate_indexed_paper_html(entry):
    short_conf_name = get_short_conf_name(entry)

    output_html = ""
    output_html += "<li id=\"" + entry["ID"] + "\">"
    output_html += f'{entry["title"]} '
    if 'file' in entry:
        link_href = entry['file']
    elif 'url' in entry:
        link_href = entry['url']

    links_html = f'<a href="{link_href}">{short_conf_name}</a>'
    if ('github' in entry):
        system_name=entry['github']
        if 'system' in entry:
            system_name=entry['system']
        links_html += f', <a href="https://github.com/{entry["github"]}">{system_name}</a> '
        links_html += f'<a class="github-button" href="https://github.com/{entry["github"]}" data-icon="octicon-star"  data-show-count="true" aria-label="Star {entry["github"]} on GitHub">Star</a>'
    
    if ('video' in entry):
        video_entry=entry['video']
        links_html += f', <a href="{video_entry}">video</a>'
    output_html += f'({links_html})'
    
    if 'award' in entry:
        output_html += f'&#11088 <em>{entry["award"]}</em> &#11088 '
    output_html += "</li>\n"
    return output_html

def generate_indexed_papers_html(entries, _counter):
    categories = {
        "cloud": "Cloud Software Systems",
        "shell": "Compilers and Systems for Shell Scripts"
    }
    category_papers = {}
    for key in categories:
        category_papers[key] = []

    for entry in entries:
        if ('note' in entry and
            entry['note'] in categories.keys()):
            paper_html = generate_indexed_paper_html(entry)
            category_papers[entry['note']].append(paper_html)
    
    output_html = ""

    for key, category_name in categories.items():
        output_html += f'<h3 id="{key}" class="page-heading">{category_name}</h2>\n'
        output_html += f'<ul>\n'
        for indexed_paper_html in category_papers[key]:
            output_html += indexed_paper_html
        output_html += "</ul>\n"

    return output_html, _counter


##
## Tex backend
##

def print_authors_tex(authors):
    # Reverse the first with the last name
    authors_list = [author.split(',')[1] + " " + author.split(',')[0] for author in authors.split(' and ')]
    # Normalize Whitespace
    authors_list = [normalize_whitespace(author.strip()) for author in  authors_list]

    # Format differently if there are more than 2 authors
    if len(authors_list) == 0:
        authors_string = ""
    if len(authors_list) <= 2:
        authors_string = " and ".join(authors_list)
    else:
        authors_string = ", ".join(authors_list[:-1])
        authors_string += ", and " + authors_list[-1]

    return authors_string


def print_title_tex(title):
    return '\\textbf{{{}}}'.format(title)

def print_infix_tex(infix):
    if ("In submission" in infix
        or "Work In Progress" in infix):
        return "\\emph{{{}}}".format(infix)
    else:
        return infix

def format_authors_tex(authors):
    authors_string = print_authors_tex(authors)
    output_tex = authors_string + ". \\\\\n"
    return output_tex

def generate_paper_tex(entry):
    output_tex = "\\begin{minipage}{\\textwidth}\n"
    output_tex += print_title_tex(entry['title']) + ". \\\\\n"
    if 'note' in entry:
        if entry['note'] == 'accepted':
            output_tex += "<i>[Accepted]</i> "
    if 'author' in entry:
        output_tex += format_authors_tex(entry['author'])
    if( 'booktitle' in entry):
        booktitle = entry['booktitle']
    else:
        booktitle = entry['journal']
    output_tex += print_infix_tex(booktitle) + "."
    if 'award' in entry:
        output_tex += "\\\\\n \\emph{" + entry['award'] + ".}"
    output_tex += "\n\\end{minipage}\n\n"
    return output_tex
    

def generate_papers_tex(entries, counter):
    output_tex = ""
    sorted_date_entries = sorted(entries, key=get_bib_date, reverse=True)
    for entry_index in range(len(sorted_date_entries)):
        entry = sorted_date_entries[entry_index]
        output_tex += generate_paper_tex(entry)
        counter += 1
    return output_tex, counter

def generate_talk_tex(entry):
    output_tex = "\\begin{minipage}{\\textwidth}\n"
    output_tex += print_title_tex(entry['title']) + ". \hfill {\em " + entry["year"] + "}\\\\\n"
    if 'event' in entry:
        output_tex += f'Event: {entry["event"]}.'
    if 'host' in entry:
        output_tex += "\\\\\n Host: " + entry['host'] + "."
    output_tex += "\n\\end{minipage}\n\n"
    return output_tex
    

def generate_talks_tex(entries, counter):
    output_tex = ""
    sorted_date_entries = sorted(entries, key=get_bib_date, reverse=True)
    for entry_index in range(len(sorted_date_entries)):
        entry = sorted_date_entries[entry_index]
        output_tex += generate_talk_tex(entry)
        counter += 1
    return output_tex, counter


##
## Export the HTML
##

def export(filename, content):
    with open(filename, 'w') as html_file:
        html_file.write(content)

def bib2output_content(in_files_generators):
    counter = 0
    html_content = ""
    for in_file, html_generator in in_files_generators:
        bib_content = parse_bib(in_file)
        bib_entries = bib_content.entries
        ## TODO: Sort entries based on descending date
        new_html_content, new_counter = html_generator(bib_entries, counter)
        html_content += new_html_content + "\n"
        counter = new_counter
    return html_content

# Talks

check_people = True
if(len(sys.argv) == 2):
    if(sys.argv[1] == "--no-check"):
        check_people = False
## First retrieve the people file
print("Parsing people...")
PEOPLE = parse_check_people(check = check_people)
print("People parsed successfully!")

html_content = bib2output_content([('files/papers.bib', generate_papers_html),
                                   ('files/talks.bib', generate_talks_html),
                                   ('files/theses.bib', generate_theses_html)])

export("pubs.html", html_content)
print("Publications to HMTL -- Done !")

indexed_papers_html = bib2output_content([('files/papers.bib', generate_indexed_papers_html)])

export("indexed_paper_list.html", indexed_papers_html)
print("Indexed Publications to HMTL -- Done !")

tex_content = bib2output_content([('files/papers.bib', generate_papers_tex)])
export("cv/pubs.tex", tex_content)
talks_tex_content = bib2output_content([('files/talks.bib', generate_talks_tex)])
export("cv/talks.tex", talks_tex_content)
print("Publications to Tex -- Done !")
