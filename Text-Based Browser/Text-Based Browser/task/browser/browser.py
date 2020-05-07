import os
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Back, Style


def get_text_from_web(url):
    soup = BeautifulSoup(url, 'html.parser')
    parse_tags = ['title', 'p', 'a', 'h1', 'h2', 'h3', 'h3', 'h4', 'h5', 'h6', 'h7', 'ul', 'ol', 'li']
    output_file = soup.find_all(parse_tags)
    prev_line = ""
    output_text = ""
    for line in output_file:
        content_line = line.string
        if content_line and content_line != prev_line:
            prev_line = content_line
            if line.name == "a":
                output_text += Fore.BLUE + content_line.strip() + Fore.RESET
            output_text += content_line.strip()
            output_text += "\n"
    return output_text


def check_website(url):
    len_url = len(url)-1
    dot_found = False
    index_dot = None
    while len_url >= 0 and dot_found is False:
        if url[len_url] == '.':
            dot_found = True
            index_dot = len_url
            break
        len_url -= 1
    return dot_found, index_dot


def file_make_operation(url, dot_index):
    file_name = requests.get("https://"+url)
    value = None
    if file_name:
        value = get_text_from_web(file_name.content)
        file_name_text = url[:dot_index]
    else:
        print("Error: Incorrect URL")
        return
    path = dir_name+"/"+file_name_text+".txt"
    with open(path, 'w') as file_input:
        file_input.writelines(value)
    file_output_operation(file_name_text)


def file_output_operation(url):
    path = dir_name+"/"+url+".txt"
    with open(path, 'r') as file_output:
        output_content = file_output.read()
        print(output_content)


dir_name = "tb_tabs"
back_stack = []
cwd = os.getcwd()
if not os.path.exists(dir_name):
    os.makedirs(dir_name)
url_input = input()
cmd_list = []
while url_input != "exit":
    ans, index = check_website(url_input)
    if ans is True:
        file_make_operation(url_input, index)
        cmd_list.append(url_input[:index])
        back_stack.append(url_input[:index])
    elif url_input in cmd_list:
        file_output_operation(url_input[:index])
        back_stack.append(url_input[:index])
    elif url_input == "back":
        if len(back_stack) != 0:
            file_output_operation(back_stack[-2])
            ans = back_stack.pop()
    else:
        print("Error: Incorrect URL")
    url_input = input()
    os.chdir(cwd)




