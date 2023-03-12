import os
import openai
import requests
import csv
from dotenv import load_dotenv

# Instantiate environment variables
load_dotenv()
openai.api_key = os.getenv('API_KEY')


def generate_messages(query):
    """Generate single set of messages for mis-spelling request to chat model, including few_shot examples

    Keyword arguments:
    query -- the search query to be checked for spelling mistakes
    """
    system_message = """You are a search engine for a wholesale e-commerce website. 
    I will provide you with a search query. Respond with the spell corrected query 
    if the query is spelled incorrectly, and with the same query if the query is 
    spelled correctly, and with "unsure" if you are unsure."""

    few_shots = [
        {
            'query': 'candals',
            'answer': 'candles'
        },
        {
            'query': 'plus size clothing',
            'answer': 'plus size clothing'
        },
        {
            'query': 'man neclesses',
            'answer': 'man necklaces'
        },
        {
            'query': 'home decor',
            'answer': 'home decor'
        },
        {
            'query': 'abstrac',
            'answer': 'abstract'
        },
        {
            'query': 'goldkette 15 it',
            'answer': 'unsure'
        }
    ]

    # Add system message
    messages = [
        {
            'role': 'system',
            'content': system_message
        }
    ]

    # Add few shot examples
    for shot in few_shots:
        messages.append(
            {
                'role': 'user',
                'content': shot['query']
            }
        )
        messages.append(
            {
                'role': 'assistant',
                'content': shot['answer']
            }
        )

    # Add user input query
    messages.append(
        {
            'role': 'user',
            'content': query
        }
    )

    return messages


def chat(query):
    """Send mis-spelling check request to, and process response from openai chat model

    Keyword arguments:
    query -- the search query to be checked for spelling mistakes
    """
    raw_response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=generate_messages(query),
        temperature=0,
    )

    response = raw_response.choices[0].message.content

    return response


# Instantiate output data
output_data = []

# Read input file
with open('input.csv', newline='') as input_file:
    reader = csv.reader(input_file, delimiter=',')

    # Iterate over each row in the input csv file to generate output row
    for row in reader:
        query = row[0]
        response = chat(query)

        print([query, response])  # debug
        output_data.append([query, response])

# Write to output file
with open('output.csv', 'w', newline='') as output_file:
    spamwriter = csv.writer(output_file, delimiter=',')

    # Write each query response to the output file
    for row in output_data:
        spamwriter.writerow(row)