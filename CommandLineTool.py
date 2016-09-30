import os
import time
from src.GroupMeWrapper import GroupMeWrapper
from src.Grouplytics import Grouplytics

def _get_required_info():
    file_name = _get_file()
    with open(file_name) as f:
        token = f.readline().strip()
        token = token.split(':', 1)[1].strip()
        name = f.readline().strip()
        name = name.split(':', 1)[1].strip()

        member = f.readline().strip()
        member = member.split(':', 1)[1].strip()
        members = []
        members.append(member)
        for remaining in f:
            members.append(remaining.strip())

    required_info = {}
    required_info['Access Token'] = token
    required_info['Group Name'] = name
    required_info['Group Members'] = members
    return required_info


# TODO: Should probably make this more robust 
def _format_check(file_name):
    with open(file_name) as f:
        lines = f.readlines()
        if lines[0].startswith('ACCESS_TOKEN'):
            if lines[1].startswith('GROUP_NAME:'):
                if lines[2].startswith('GROUP_MEMBERS:'):
                    return True
        return False


def _get_file():
    while True:
        file_name = input("Enter file name (must end in .txt): ")
        if file_name.endswith('.txt'):
            if os.path.isfile(file_name):
                if _format_check(file_name):
                    print("Thanks! Now be patient, this is going to take a minute.\n") 
                    return file_name
                else:
                    print("Detected incorrect file format. Be sure to follow the example provided in config.txt!")
            else:
                print("File doesn't exist. Make sure it's in the same directory as this script!")
        else:
            print("That's not a text file. Make sure you're including the .txt extension!")

        time.sleep(2)
        print()


def main():
    required_info = _get_required_info()

    groupme = GroupMeWrapper(required_info['Access Token'], required_info['Group Name'], required_info['Group Members'])
    grouplytics = Grouplytics(groupme.members, groupme.messages)

    
    with open('report.txt', 'w') as f:
        f.write(grouplytics.swear_word_report())
        f.write(grouplytics.overall_message_report())
        f.write(grouplytics.most_liked_report())
        f.write(grouplytics.biggest_liker_report())
        f.write(grouplytics.donald_trump_report())
        f.write(grouplytics.meme_lord_report())
        f.write(grouplytics.dude_report())

    # grouplytics.most_popular_day_report()
    # GFBFdictionary = {'Steve': ['Emily'], 'Ryan': ['Elena'], 'Neil': ['Claire'], 'Bennett': ['Slim Payt', 'Payton', 'PJ'], 'Adam': ['Jordan']}
    # grouplytics.GFBF_report(GFBFdictionary)
main()
