import openai
import os
import extractor
import argparse

from dotenv import load_dotenv

def main():
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    parser = argparse.ArgumentParser(description='Generate project from a prompt.')
    parser.add_argument('desc', type=str, help='Project description')
    args = parser.parse_args()

    project_desc = args.desc
    prompt = f"""Create a {project_desc}.

Provide a clean, full example and include all the files needed to run the project.
The files should be formatted as follows:

[START!]
[START filename1]
code for filename1
[END filename1]

[START filename2]
code for filename2
[END filename2]
[END!]"""

    print("Generating code...")
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    )

    reply = completion.choices[0].message.content

    print("Saving reply to output.txt")
    with open("output.txt", "w") as f:
        f.write(reply)

    print("Extracting files...")
    extractor.extract_files(reply)

    print('Done!')


if __name__ == "__main__":
    main()
