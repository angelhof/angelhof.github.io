import os 
import os.path

def export_html(filename, content):
    with open(filename, 'w') as html_file:
        html_file.write(content)

def group_by_year(pics):
    year_dic = {}
    for pic in pics:
        year = int(pic.split("_")[0])
        if year in year_dic:
            year_dic[year].append(pic)
        else:
            year_dic[year] = [pic]
    return year_dic


def generate_year_html(year, html_content = ""):
    html_content += "<h3>" + str(year) + "</h3>\n" 
    return html_content

def generate_pic_html(filename, html_content = ""):
    file_path = os.path.join(ESCAPE_ROOMS_DIR, filename)
    html_content += "<img src=\""
    html_content += "/" + file_path
    html_content += "\" alt=\""
    html_content += filename
    html_content += "\" style=\"height:"
    html_content += IMAGE_HEIGHT
    html_content += ";\">\n"
    return html_content

def generate_pics_html(pics, html_content = ""):
    sorted_by_name = sorted(pics)
    for filename in sorted_by_name:
        html_content = generate_pic_html(filename, html_content)
    return html_content

def generate_content_html(year_dic, html_content = ""):
    years = sorted(year_dic.keys())
    for year in years:
        html_content = generate_year_html(year, html_content)
        year_pics = year_dic[year]
        html_content = generate_pics_html(year_pics, html_content)
        html_content += "<hr>\n"
    return html_content

def generate_html(year_dic, html_content = ""):
    html_content += "---\n"
    html_content += "layout: hidden\n"
    html_content += "overview: true\n"
    html_content += "---\n\n"
    html_content += "<p>" + INTRODUCTION + "</p>\n"
    html_content = generate_content_html(year_dic, html_content)
    return html_content

# Talks

## This script creates the static directory for escape room pictures
## by iterating over all escape room pictures that exist in the folder

ESCAPE_ROOMS_DIR = os.path.join("files", "escape_rooms")
FILENAME = "escape_rooms.html"
IMAGE_HEIGHT = "250px"
escape_room_pics = [f for f in os.listdir(ESCAPE_ROOMS_DIR) if os.path.isfile(os.path.join(ESCAPE_ROOMS_DIR, f))]

INTRODUCTION = "Hey, you found the \"hidden\" directory of pictures from escape rooms that I have been to. Unfortunately, I am not going as often as I did during the past years, but I hope that this directory keeps growing :) At the moment it contains " + str(len(escape_room_pics)) + " pictures."

grouped_by_year = group_by_year(escape_room_pics)
html_content = generate_html(grouped_by_year)

export_html(FILENAME, html_content)
print("Escape room HMTL -- Done !")
