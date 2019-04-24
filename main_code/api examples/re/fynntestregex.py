#!/usr/bin/python
import re

phone = "2004-959-559 # This is Phone Number"

def remove_comments(string):
    # Delete Python-style comments from a string
    num = re.sub(r'#.*$', "", string)
    return (num)

def find_numbers(string):
    # find phone number Remove anything othesr than digits
    num = re.sub(r'\D', "", string)
    return ("Phone Num : ", num)

def find_first_email(string):
    #find on email address
    match = re.search(r'[\w\.-]+@[\w\.-]+', string)
    match.group(0)
    return(match.group(0))

def find_all_emails(string):
    # finds multiple email addresses
    line = "should we use regex more often? reckhorn@msu.com let me know at  321dsasdsa@dasdsa.com.lol"
    match = re.findall(r'[\w\.-]+@[\w\.-]+', string)
    return(match)

def find_all_dates(string):
    # match = re.search(r'(\d+/\d+/\d+)',string)
    match = re.findall(r'(\d+/\d+/\d+)', string)
    return(match)
# date="13-11-2017"

# x=re.search("^([1-9] |1[0-9]| 2[0-9]|3[0-1])(.|-)([1-9] |1[0-2])(.|-|)20[0-9][0-9]$",date)

# x.group()
namestring = " hello my name is Anton and I am from Germany"
# x = re.search(r'(([A-Z][a-z]*)[\s-]([A-Z][a-z]*))', namestring)
# x = re.search(r'[A-Z]([a-z]+|\.)(?:\s+[A-Z]([a-z]+|\.))*(?:\s+[a-z][a-z\-]+){0,2}\s+[A-Z]([a-z]+|\.)', namestring)

# print(x.group())

#
# #example of how to use
# print(remove_comments(" Hello #this a test"))
# print(find_numbers("hi 234-566-7889 is my number"))
# print(find_first_email("my name is fynn and my email is spartan1@msu.edu and thats all special@me.com"))
# print(find_all_emails("my name is fynn and my email is spartan1@msu.edu and thats all special@me.com and iamemail@com.com"))
print(find_all_dates("the date is 11/2/3and 1/2/3 lastly 22/4/21"))