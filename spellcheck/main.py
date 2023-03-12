import os
import openai
import requests
import csv
from dotenv import load_dotenv

# Instantiate environment variables
load_dotenv()
openai.api_key = os.getenv('API_KEY')


def generate_examples():
    """Generate set of few-shot mis-spelling examples for the chat model from source file
    """
    examples = []

    # Read input file
    with open('examples.csv', newline='') as input_file:
        reader = csv.reader(input_file, delimiter=',')

        # Iterate over each row in the input csv file to generate output row
        for row in reader:
            query = row[0]
            answer = row[1]

            examples.append(
                {
                    'query': query,
                    'answer': answer
                }
            )

    return examples


def generate_messages(query, examples):
    """Generate single set of messages for mis-spelling request to chat model, including few_shot examples

    Keyword arguments:
    query -- the search query to be checked for spelling mistakes
    """
    system_message = """You are a search engine for a wholesale e-commerce website. 
    I will provide you with a user entered search query. Respond with true
    if the query is spelled incorrectly, and with false if the query is 
    spelled correctly or if you are unsure."""

    # Add system message
    messages = [
        {
            'role': 'system',
            'content': system_message
        }
    ]

    # Add few shot examples
    for example in examples:
        messages.append(
            {
                'role': 'user',
                'content': example['query']
            }
        )
        messages.append(
            {
                'role': 'assistant',
                'content': example['answer']
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
    examples = generate_examples()
    raw_response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=generate_messages(query, examples),
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
