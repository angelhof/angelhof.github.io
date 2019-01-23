import bibtexparser

def parse_bib(filename):
    with open(filename) as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
    return bib_database

##
## Turn the Unicode of bibtexparser to ascii
##

def asciify_unicode(unicode_string):
    if type(unicode_string) is unicode:
        return unicode_string.encode('ascii')
    else:
        return unicode_string
    
def asciify_unicode_entry(entry):
    new_entry = {}
    for key in entry.keys():
        new_entry[asciify_unicode(key)] = asciify_unicode(entry[key])
    return new_entry
        
def asciify_unicode_entries(entries):
    return map(asciify_unicode_entry, entries)


##
## Generate HTML
##

def generate_general_html(entry_index, entry, infix):
    output_html = ""
    output_html += "<li id=\"" + entry["ID"] + "\">"
    output_html += "[" + str(entry_index) + "] "
    output_html += entry['title'] + ". "
    output_html += infix + ", " + entry['year'] + ". "
    output_html += "(<a href=\"" + entry['file'] + "\">PDF</a>)"
    output_html += "</li>\n"
    return output_html
    
def generate_talk_html(entry_index, entry):
    return generate_general_html(entry_index, entry, entry['event'])

def generate_thesis_html(entry_index, entry):
    return generate_general_html(entry_index, entry, entry['school'])

def generate_talks_html(entries, counter):
    output_html = ""
    output_html += "<h2 class=\"page-heading\">Talks</h2>\n"
    output_html += "<ul class=\"talks bibliography\">\n"
    for entry_index in xrange(len(entries)):
        entry = entries[entry_index]
        output_html += generate_talk_html(entry_index + counter, entry)
    output_html += "</ul>\n"
    return output_html
    
def generate_theses_html(entries, counter):
    output_html = ""
    output_html += "<h2 class=\"page-heading\">Theses</h2>\n"
    output_html += "<ul class=\"theses bibliography\">\n"
    for entry_index in xrange(len(entries)):
        entry = entries[entry_index]
        output_html += generate_thesis_html(entry_index + counter, entry)
    output_html += "</ul>\n"
    return output_html

##
## Export the HTML
##

def export_html(filename, content):
    with open(filename, 'w') as html_file:
        html_file.write(content)

def bib2html_content(in_files_generators):
    counter = 0
    html_content = ""
    for in_file, html_generator in in_files_generators:
        bib_content = parse_bib(in_file)
        ascii_content = asciify_unicode_entries(bib_content.entries)
        ## TODO: Sort entries based on descending date
        html_content += html_generator(ascii_content, counter) + "\n"
        counter += len(bib_content.entries)
    return html_content

# Talks
html_content = bib2html_content([('files/theses.bib', generate_theses_html),
                                 ('files/talks.bib', generate_talks_html)])

export_html("papers.html", html_content)
print("Done !")
