# -*- coding: utf-8 -*-
import os
import time
import random
from slackclient import SlackClient
# starterbot's ID as an environment variable
BOT_ID='to be replaced'
SLACK_BOT_TOKEN='to be replaced'
BOT_NAME = 'dr.hannibal'
# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"

CONTEXT_1 = ["Hello","Hi", "Good morning","Good evening","Greetings","Hey",
"hello","hi", "good morning","good evening","greetings","hey"]
CONTEXT_2 = ["afraid","fear"]
CONTEXT_3 = ["problem"]
CONTEXT_4 = ["mother","father","brother","sister","children","husband","wife","mate","family"]
CONTEXT_5 = ["love", "relationsip", "boyfriend", "girlfriend"]
CONTEXT_6 = ["conflict"]
CONTEXT_7 = ["yes", "yep", "don`t know"]
CONTEXT_8 = ["advice", "to do"]
CONTEXT_9 = ["Bye", "See you soon", "Thank you", "Good bye"]

REPLY_1 = ["Hello. How can I help you?"]
REPLY_2 = ["I fully understand you.",
           "Do you want to talk about it?",
           "I understand, it worries you much.",
           "How often it happens with you?",
           "Tell me more about it.",
           "What do you feel at this?",
           "Have you noticed this before?"]
REPLY_3 = ["I am ready to listen to you.",
            "I think nothing is impossible. All the problems to which we have come, you are able to solve by yourself.",
            "Do you want to talk about it?",
            "I understand, it worries you much.",
            "How often it happens with you?",
            "What do you feel at this?",
            "What you feel in these cases?",
            "Why do you want to solve this problem?",
            "Most problems usually come from your childhood. ",
            "Tell me about your family.",
            "Have you noticed this before?",
            "How long have you got this problem?",
            "Why did you decide to solve this problem now?",
            "Tell me more about it"]
REPLY_4 = ["Most problems usually come from your childhood. Tell me about your family.",
            "What do you feel at this?",
            "What you feel in these cases?",
            "Why do you want to solve this problem?",
            "Most problems usually come from your childhood. ",
            "Tell me about your family.",
            "Have you noticed this before?",
            "How long have you got this problem?",
            "Why did you decide to solve this problem now?"]
REPLY_4 = ["Most problems usually come from your childhood. Tell me about your family."]
REPLY_5 = ["Most problems usually come from your childhood. Tell me about your family.",
            "I am ready to listen to you.",
            "Tell me more about it.",
            "I think nothing is impossible. All the problems to which we have come, you are able to solve by yourself.",
            "Do you want to talk about it?", 
            " I understand, it worries you much.",
            "How often it happens with you?",
            "Tell me more about it.",
            "What do you feel at this?",
            "What you feel in these cases?",
            "Why do you want to solve this problem?",
            "Most problems usually come from your childhood. Tell me about your family.",
            "Have you noticed this before?",
            "How long have you got this problem?",
            "Why did you decide to solve this problem now?",
            "The relationship between people is very difficult, but we should find common ground",
            "Imagine yourself in the place of this person, how do you see the situation?"]
REPLY_6 = ["The relationship between people is very difficult, but we should find common ground",
            "Imagine yourself in the place of this person, how do you see the situation?",
            " Which solutions to this problem do you see?"]
REPLY_7 = ["Do you want to tell something else? ","Justify your answer"]
REPLY_8 = ["Positive emotions is the main thing for you now.",
            "I think nothing is impossible. All the problems to which we have come, you are able to solve by yourself.  Do you practice a health promotion? I would advise you to fully sleep and eat. Also you can try yourself in sport.",
            "Firstly, I suggest you do some thing that will lift your spirits.You can do engage some hobby. It can be drawing, sports, shopping, walking, meeting with friends.",
            "I advise you to exercise.",
            "I think your problem can be easily solved for several meetings. I invite the full-time counseling."]
REPLY_9 = ["I think your problem can be easily solved for several meetings."," I invite the full-time counseling."]
REPLY_10 = ["I fully understand you. ",
            "I think nothing is impossible. All the problems to which we have come, you are able to solve by yourself. ",
            "Do you want to talk about it? ",
            "Do you want to tell something else? ",
            "I understand, it worries you much. ",
            "How often it happens with you? ",
            "Justify your answer",
            "What do you mean?",
            "Tell me more about it.",
            "What do you feel at this?",
            "Most problems usually come from your childhood. Tell me about your family."]

# instantiate Slack client
slack_client = SlackClient(SLACK_BOT_TOKEN)
def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    if check_input(command,CONTEXT_1):
        response = random.choice(REPLY_1)
    elif check_input(command,CONTEXT_2):
        response = random.choice(REPLY_2)
    elif check_input(command,CONTEXT_3):
        response = random.choice(REPLY_3)
    elif check_input(command,CONTEXT_4):
        response = random.choice(REPLY_4)
    elif check_input(command,CONTEXT_5):
        response = random.choice(REPLY_5)
    elif check_input(command,CONTEXT_6):
        response = random.choice(REPLY_6)
    elif check_input(command,CONTEXT_7):
        response = random.choice(REPLY_7)
    elif check_input(command,CONTEXT_8):
        response = random.choice(REPLY_8)
    elif check_input(command,CONTEXT_9):
        response = random.choice(REPLY_9)
    else:
        response = random.choice(REPLY_10)
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def check_input(command, replies):
    for reply in replies:
        if reply in command:
            return True
    return False
def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None

if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")