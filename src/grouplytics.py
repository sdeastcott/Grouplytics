import re
import time
import operator
from datetime import datetime
from collections import defaultdict
from src.cipher_decoder import decode


class Grouplytics:
    def __init__(self, messages, members):
        self.messages = messages
        self.members = members
        
    # TODO
    def get_creation_date(self):
        # TODO: I accidentally deleted this code
        return datetime.fromtimestamp(self.group_data['creation_date']).strftime("%m/%d/%y")
    

    def overall_message_report(self):
        total_count = 0
        per_member_count = defaultdict(int)

        for message in self.messages:
            total_count += 1
            per_member_count[message['user_id']] += 1
        
        seconds_surpassed = float(time.time()) - float(self.group_data['creation_date'])
        days_surpassed =  seconds_surpassed / 86400.0
        avg_per_day = round(total_count / days_surpassed, 2)

        avg_per_member = defaultdict(int)
        for user_id in per_member_count:
            avg_per_member[user_id] = round(
                per_member_count[user_id] / days_surpassed, 2)
                
        subreport = self._generate_report('Average Messages Per Day', avg_per_day, avg_per_member)
        return self._generate_report('Message Count', total_count, per_member_count, subreport=subreport)


    def likes_received(self):
        total_count = 0
        likes_received_count = defaultdict(int)
        message_count_per_member = defaultdict(int)

        for message in self.messages:
            message_count_per_member[message['user_id']] += 1
            if message['favorited_by']:
                total_count += len(message['favorited_by'])
                likes_received_count[message['user_id']] += len(message['favorited_by'])

        # Divide total likes received by total messages sent to determine average likes per message
        avg_per_message = defaultdict(int)
        for user_id in likes_received_count:
            avg_per_message[user_id] = round(
                float(likes_received_count[user_id]) / message_count_per_member[user_id], 2)

        subreport = self._generate_report('Likes Received Per Message', None, avg_per_message, includePercent=False)
        report = self._generate_report('Likes Received', total_count, likes_received_count, subreport=subreport)
        return report
        

    def messages_liked(self):
        total_count = 0
        per_member_count = defaultdict(int)

        for message in self.messages:
            favorited_by = message['favorited_by']
            if favorited_by:
                total_count += len(favorited_by)
                for member in favorited_by:
                    if member in self.members: 
                        per_member_count[member] += 1

        return self._generate_report('Messages Liked', total_count, per_member_count)


    def average_word_length(self):
        cumulative_word_count = defaultdict(int)
        cumulative_word_length = defaultdict(int)

        for message in self.messages:
            text = message['text']
            if text:
                for word in text.split():
                    if word.startswith('http') or word.startswith('www') or len(word) > 15: continue
                    cumulative_word_count[message['user_id']] += 1
                    cumulative_word_length[message['user_id']] += len(word)

        # Divide total word length by total word count to determine average word length per member
        avg_word_length = defaultdict(int)
        for user_id in self.members:
            avg_word_length[user_id] = round(float(cumulative_word_length[user_id]) / cumulative_word_count[user_id], 2)

        return self._generate_report('Average Word Length', None, avg_word_length, True, False)


    # TODO: what's the difference between image and linked image?
    def images_shared(self):
        total_count = 0
        per_member_count = defaultdict(int)

        for message in self.messages:
            if message['attachments']:
                for attachment in message['attachments']:
                    if attachment['type'] == 'image' or attachment['type'] == 'linked_image':
                        total_count += 1
                        per_member_count[message['user_id']] += 1

        return self._generate_report('Images Shared', total_count, per_member_count)


    def youth_slang_report(self):
        slang = set()
        with open('src/text/slang.txt', 'r') as f:
            for word in f:
                slang.add(word.strip())

        total_count = 0
        per_member_count = defaultdict(int)

        for message in self.messages:
            if message['text']:
                for word in message['text'].split():
                    if word in slang:
                        total_count += 1
                        per_member_count[message['user_id']] += 1

        return self._generate_report("Youth Slang Count", total_count, per_member_count)


    def swear_word_report(self):
        total_count = 0
        swear_words = decode('src/text/swear_words.txt') # TODO: add more!
        per_member_count = defaultdict(int)

        for message in self.messages:
            if message['text']:
                for word in message['text'].split():
                    if word in swear_words:
                        total_count += 1
                        swear_words[word] += 1
                        per_member_count[message['user_id']] += 1

        if total_count > 9:
            subreport = {"title": 'Top 10 Swear Words', "total": None, "items": [], "subreport": None}
            top_10 = sorted(swear_words.items(), key=operator.itemgetter(1), reverse=True)
            for i in range(0, 10):
                subreport['items'].append({'name': top_10[i][0], 'count': top_10[i][1]})

        report = self._generate_report('Swear Word Count', total_count, per_member_count, subreport=subreport)
        return report


    def dude_report(self):
        total_count = 0
        per_member_count = defaultdict(int)
        pattern = re.compile('d+u+d+e+')

        for message in self.messages:
            if message['text']:
                for word in message['text'].split():
                    if pattern.match(word):
                        total_count += 1
                        per_member_count[message['user_id']] += 1

        return self._generate_report("'dude' count", total_count, per_member_count)

     
    def _generate_report(self, title, total_count, key_val, shouldDescend=True, includePercent=True, subreport=None):
        if total_count == 0: return None

        report = {
            "title": title,
            "total": total_count,
            "items": [],
            "subreport": subreport
        }

        if total_count != 0:
            sorted_count = sorted(key_val.items(), key=operator.itemgetter(1), reverse=shouldDescend)
            report["items"] = [{'name': self.members[x[0]] if x[0] in self.members, 'count': x[1]}]
                                # for x in filter(lambda item: item[1] > 0, sorted_count)]

        return report

    # I removed this from line 181, I don't think it's necessary.
    def _map_member_ID_to_name(self, ID):
        if ID in self.members:
            return self.members[ID]


    '''
    def gossip_report(self):
        # Enter all names into a dictionary for fast lookup
        names = {}
        with open('src/text/names.txt', 'r') as f:
            for line in f:
                name = line.strip()
                names[name] = 0

        # Count all occurrences of names  
        for message in self.messages:
            if message['text']:
                for word in message['text'].split():
                    if word in names:
                        names[word] += 1

        # Sort name occurences and get top 25
        top_25 = []
        sorted_arr = sorted(names.items(), key=operator.itemgetter(1), reverse=True)
        for i in range(0, 25):
            top_25.append({'name': sorted_arr[i][0], 'count': sorted_arr[i][1]})
        
        first_names = []
        for aliases in self.group_data['aliases'].values():
            first_names.append(aliases[-1].split()[0].lower())
        
        revised_top = []
        for name in top_25:
            flag = True
            for first_name in first_names:
                if name['name'] in first_name:
                    flag = False
                    break
            if flag:
                revised_top.append(name)

        revised_top = revised_top[:5]
        report = {"title": 'Gossip Report', "total": None, "items": revised_top, "subreport": None}
        return report
    '''