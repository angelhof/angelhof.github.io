import bibtexparser

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
        month = entry['month']
    if 'day' in entry:
        day = entry['day']
    return (year, month, day)



##
## Generate HTML
##

def normalize_whitespace(string):
    return " ".join(string.split())

def print_authors(authors):
    # Reverse the first with the last name
    authors_list = [author.split(',')[1] + " " + author.split(',')[0] for author in authors.split('and')]
    # Normalize Whitespace
    authors_list = [normalize_whitespace(author.strip()) for author in  authors_list]

    # Format differently if there are more than 2 authors
    if len(authors_list) <= 2:
        authors_string = " and ".join(authors_list)
    else:
        authors_string = ", ".join(authors_list[:-1])
        authors_string += ", and " + authors_list[-1]
        
    return authors_string

def print_title(title):
    return "<b>" + title + "</b>"

def generate_general_html(entry_index, entry, infix):
    output_html = ""
    output_html += "<li id=\"" + entry["ID"] + "\">"
    output_html += "[" + str(entry_index) + "] "
    if 'author' in entry:
        output_html +=  print_authors(entry['author']) + ". "
    output_html += print_title(entry['title']) + ". "
    output_html += infix + ", " + entry['year'] + ". "
    if 'note' in entry:
        if entry['note'] == 'accepted':
            output_html += "<i>[Accepted]</i> "
    if 'url' in entry:
        output_html += "(<a href=\"" + entry['url'] + "\">link</a>) "        
    if 'file' in entry:
        output_html += "(<a href=\"" + entry['file'] + "\">pdf</a>)"
    output_html += "</li>\n"
    return output_html
    
def generate_talk_html(entry_index, entry):
    return generate_general_html(entry_index, entry, entry['event'])

def generate_paper_html(entry_index, entry):
    ## WARNING: Maybe it is not always 'booktitle'
    return generate_general_html(entry_index, entry, entry['booktitle'])

def generate_thesis_html(entry_index, entry):
    return generate_general_html(entry_index, entry, entry['school'])

def generate_entries_html(entries, counter, heading, entry_handler):
    output_html = ""
    output_html += "<h2 class=\"page-heading\">" + heading + "</h2>\n"
    output_html += "<ul class=\"" + str.lower(heading) + " bibliography\">\n"
    sorted_date_entries = sorted(entries, key=get_bib_date, reverse=True)
    for entry_index in range(len(sorted_date_entries)):
        entry = sorted_date_entries[entry_index]
        output_html += entry_handler(entry_index + counter, entry)
    output_html += "</ul>\n"
    return output_html

def generate_papers_html(entries, counter):
    return generate_entries_html(entries, counter, "Papers", generate_paper_html)

def generate_talks_html(entries, counter):
    return generate_entries_html(entries, counter, "Talks", generate_talk_html)
    
def generate_theses_html(entries, counter):
    return generate_entries_html(entries, counter, "Theses", generate_thesis_html)

##
## Export the HTML
##

def export_html(filename, content):
    with open(filename, 'w') as html_file:
        html_file.write(content)

def bib2html_content(in_files_generators):
    counter = 0
    html_content = ""
    html_content += "---\n"
    html_content += "layout: main\n"
    html_content += "overview: true\n"
    html_content += "---\n\n"
    html_content += "<nav>\n"
    html_content += "<h3><a href=\"/index.html\" style=\"color: inherit\">About</a></h3>\n"
    html_content += "<h3 class=\"active\"><a href=\"/pubs.html\" style=\"color: inherit\">Papers</a></h3>\n"
    html_content += "<h3><a href=\"/blog/index.html\" style=\"color: inherit\">Blog</a></h3>"
    html_content += "</nav>\n\n"
    html_content += "<hr>\n\n"
    for in_file, html_generator in in_files_generators:
        bib_content = parse_bib(in_file)
        bib_entries = bib_content.entries
        ## TODO: Sort entries based on descending date
        html_content += html_generator(bib_entries, counter) + "\n"
        counter += len(bib_content.entries)
    return html_content

# Talks
html_content = bib2html_content([('files/papers.bib', generate_papers_html),
                                 ('files/theses.bib', generate_theses_html),
                                 ('files/talks.bib', generate_talks_html)])

export_html("pubs.html", html_content)
print("Publications to HMTL -- Done !")
