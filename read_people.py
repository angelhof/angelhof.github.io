import requests

class Person:
    def __init__(self, args):
        self.name = args[0]
        if (args[1] == "-"):
            self.url = None
        else:
            self.url = args[1]

    def is_name(self, name):
        return self.name == name

    def valid_url(self):
        if(self.url is None):
            return true
        else:
            try:
                resp = requests.get(self.url)
            except requests.exceptions.SSLError as err:
                print("SSLError:", err)
                return False
            ## Linkedin returns 999
            if(resp.status_code == 999):
                if("linkedin" in self.url):
                    return True
            return resp.status_code == requests.codes.ok

    def format_html(self):
        if(self.url is None):
            return self.name
        else:
            output = '<a class="name-link" href="{}">{}</a>'.format(self.url, self.name)
            return output

def find_person(name, people):
    for person in people:
        if(person.name == name):
            return person
    print(" !! ERROR:", name, "not found in people")
    exit(1)

def parse_people():
    filename = "files/people.csv"
    with open(filename) as people_f:
        lines = [line.split("|") for line in people_f.readlines()]
        clean_lines = [[word.strip() for word in line] for line in lines]
    people = [Person(line) for line in clean_lines]
    return people

def check_people_valid(people):
    for person in people:
        if (not person.valid_url()):
            print(" !! WARNING: Url:", person.url, "for:", person.name, "is not valid !!")

def parse_check_people(check = True):
    people = parse_people()
    if(check):
        check_people_valid(people)
    return people
