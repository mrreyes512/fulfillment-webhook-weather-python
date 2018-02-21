import os
import psycopg2
from urllib import parse
import texttable

import json

os.environ['DATABASE_URL'] = 'postgres://ylbzmiqhvzznyp:1a0c5aa46adada3c12335e44ff26cc3dba1d0d8cf70c5938dd910a205874f6c9@ec2-50-19-105-188.compute-1.amazonaws.com:5432/dddev09qk12ksl'


def dbConnection(line_query):
    parse.uses_netloc.append("postgres")
    url = parse.urlparse(os.environ["DATABASE_URL"])
    # DATABASE_URL set in : heroku config

    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )

    cur = conn.cursor()
    cur.execute(line_query)

    query_results = cur.fetchall()

    return query_results


def queryRecords():

    line_query = "SELECT ticket_id, first_name, issue_type FROM public.example_table"
    result = dbConnection(line_query)

    # process data back from db
    # records = []

    # for r in result:
    #     ticket_id = r[0]
    #     first_name = r[1]
    #     issue_type = r[2]
    #     records.append(
    #         {'ticket_id': ticket_id,
    #          'first_name': first_name,
    #          'issue_type': issue_type
    #          })
        # records.append({ticket_id, first_name, issue_type})
        # print(ticket_id, first_name, issue_type)

    formatted = formatRecords(result)

    return formatted


def formatRecords(result):
    tab = texttable.Texttable()
    headings = ['Ticket ID', 'First Name', 'Issue Type']
    tab.header(headings)

    for row in result:
        tab.add_row(row)

    s = tab.draw()
    print(s)

    # print("Formatted Records\n----------------------")
    #
    # headings = ['Ticket ID', 'First Name', 'Issue Type']
    # print(headings)

    # for record in records:
    #     print(record[10])


def queryLineResponse(data):
    speech = "The line looks like:\n Ticket Id | First Name | Issue Type\n ------------------------------------\n"
    # Iterate through records in the data, and append them to the 'speech' variable
    # for record in data:
    #     ticket_id = record.get('ticket_id')
    #     first_name = record.get('first_name')
    #     issue_type = record.get('issue_type')
    #
    #     speech + "{} | {} | {}\n---------------\n".format(ticket_id, first_name, issue_type)
    speech = speech + str(data)
    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        "data": data,
    }

mystring = queryRecords()

print(mystring)

# mystring = [
#     {
#         'ticket_id': 1,
#         'first_name': 'Mark',
#         'issue_type': 'testing'
#     },
#     {
#         'ticket_id': 2,
#         'first_name': 'Sandra',
#         'issue_type': 'port turnup'
#     },
#     {
#         'ticket_id': 3,
#         'first_name': 'Aidan',
#         'issue_type': 'cpe config issues'
#     },
#     {
#         'ticket_id': 4,
#         'first_name': 'Olivia',
#         'issue_type': 'firmeware upgrade'
#     },
#     {
#         'ticket_id': 5,
#         'first_name': 'Sqoop',
#         'issue_type': 'other'
#     }
# ]
# smallString = {'ticket_id': 1, 'first_name': 'Mark', 'issue_type': 'testing'}
#
# speech = "The line looks like:\n Ticket Id | First Name | Issue Type\n ------------------------------------\n"
#
# # Print original
# print("\nMy String : " + str(mystring) + "\nFormatted below:\n-------\n")
#
# # Print List
# for row in smallString:
#     print(row.first_name)
#
# print("\n-------\n")
#
# # Print header
# print(smallString)
