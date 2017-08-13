import os
import time
from src.groupme import GroupMe
from src.grouplytics import Grouplytics


def _get_required_info():
    file_name = _get_file()

    with open(file_name, 'r', encoding="utf_8") as f:
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


def _format_check(file_name):
    with open(file_name, 'r', encoding="utf-8") as f:
        lines = f.readlines()
        if lines[0].strip().startswith('ACCESS_TOKEN'):
            if lines[1].strip().startswith('GROUP_NAME:'):
                if lines[2].strip().startswith('GROUP_MEMBERS:'):
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

        time.sleep(1)
        print()


def report_to_text(report):
    with open('report.txt', 'a') as f:
        out = []
        if report['total'] is None:
            out.append(report['title'])
        else:
            out.append("{} - {}".format(report['title'], report['total']))

        for item in report['items']:
            out.append("- {}: {}".format(item['name'], item['count']))

        out.append("\n")
        f.write("\n".join(out))
        
    if report['subreport']:
        report_to_text(report['subreport'])


def main():
    required_info = _get_required_info()
    access_token = required_info['Access Token']
    group_name = required_info['Group Name']
    groupme = GroupMe(access_token)
    group_id = groupme.get_group_id(group_name)
    members = groupme.get_members(group_id)
    messages = groupme.get_messages(group_id, True)
    grouplytics = Grouplytics(members, messages)

    with open('report.txt', 'w') as f:
        f.write("Group Creation Date: ")
        f.write(grouplytics.get_creation_date() + '\n' + '\n')
    
    report_to_text(grouplytics.overall_message_report())
    report_to_text(grouplytics.likes_received())
    report_to_text(grouplytics.messages_liked())
    report_to_text(grouplytics.average_word_length())
    report_to_text(grouplytics.swear_word_report())
    report_to_text(grouplytics.dude_report())
    report_to_text(grouplytics.youth_slang_report())
    report_to_text(grouplytics.images_shared())

main()
