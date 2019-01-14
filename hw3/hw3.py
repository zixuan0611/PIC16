# import modules
import re
import urllib2
import happiness_dictionary


# a function performs the same action as type(), and can recognize integers, floats, strings, and lists
def mytype(v):
    v_input = str(v)
    if re.search(r'\[[-\d*\.,\s]*\d*\]', v_input):  # to recognize lists that can only contain numbers
        return_type = "list"
    elif re.search(r'[0-9]\.[0-9]', v_input):
        return_type = "float"
    elif re.search(r'[0-9]', v_input):
        return_type = "int"
    else:  # if not the above, then the type is string
        return_type = "string"

    return return_type

# test cases
#print (mytype(1))
#print (mytype(1.1))
#print (mytype("hello"))
#print (mytype([]))

# a function that takes as input a list of file names and returns a list of the names of all pdf files
def findpdfs(L):
    return_list = []
    for item in L:
        if re.search('^([a-zA-Z0-9]*)\.pdf$', item):
            name = re.sub('^([a-zA-Z0-9]*)\.pdf$', r'\1', item)  # form the file name without pdf extension
            return_list.append(name)

    return return_list

# simple test
# print (findpdfs(["lecture1.pdf", "456.jpg", "123.pdf"]))


# a function that takes a input a URL and output all the found email address
def findemail(url):
    output_list = []
    page = urllib2.urlopen(url).read()  # open and read the page
    # page = "hangjie AT math DOT ucla DOT edu" a temporary test for the regular espression
    at_list = [' AT ', ' at ', '[AT]', '[at]']
    # strictly followed the instructions, there is space for AT and at but no space for [AT] and [at]
    dot_list = [' DOT ', ' dot ', '[dot]', '[DOT]']
    # similar to the at_list
    for c in at_list:
        page = page.replace(c, '@')  # convert to no hidden version
    for b in dot_list:
        page = page.replace(b, '.')  # same as above conversion

    email_list = re.findall(r'(\w+@\w+(\.\w+)+)', page)
    for k in email_list:
        output_list.append(k[0])

    # print output_list
    return output_list

# simple test:
# a = "http://www.math.ucla.edu/~anderson/"
# findemail(a)


# a function that uses the happiness dictionary to rate the happiness score of the input text
def happiness(text):
    happy_dic = happiness_dictionary.happiness_dictionary  # get the dictionary
    words = re.split(r'\s+', text)  # get the word list
    happy = 0
    counter = 0
    for word in words:
        if not re.search(r'\w', word[-1]):  # eliminate special characters
            word = word[:-1]
        if not re.search(r'\w', word[0]):   # eliminate special characters
            word = word[1:]
        if word in happy_dic.keys():  # if happiness word found, add the score
            happy += happy_dic[word]
            counter += 1
    if counter == 0:  # avoid zero division
        return 0

    return happy/counter  # return the average

# test
# print (happiness("happiness: :love 7-9pm 10:00:00PM"))
