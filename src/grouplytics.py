import re
import operator
from collections import defaultdict
from src.cipher_decoder import decode


class Grouplytics:
    def __init__(self, group_data):
        self.group_data = group_data
        self.messages = group_data['messages']
        self.members = group_data['members']
        

    def overall_message_report(self):
        total_count = 0
        per_member_count = defaultdict(int)

        for message in self.messages:
            total_count += 1
            per_member_count[message['user_id']] += 1

        return self._generate_report('Message Count', total_count, per_member_count)


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
        for user_ID in likes_received_count:
            avg_per_message[user_ID] = round(
                float(likes_received_count[user_ID]) / message_count_per_member[user_ID], 2)

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
            if message['text']:
                for word in message['text'].split():
                    cumulative_word_count[message['user_id']] += 1
                    cumulative_word_length[message['user_id']] += len(word)

        # Divide total word length by total word count to determine average word length per member
        avg_word_length = defaultdict(int)
        for user_ID in self.members:
            avg_word_length[user_ID] = round(float(cumulative_word_length[user_ID]) / cumulative_word_count[user_ID], 2)

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

        # Remove any aliases from top 25.
        revised_top = []
        aliases = self.group_data['aliases']
        for name in top_25:
            for user_aliases in aliases.values():
                if name['name'] in user_aliases:
                    revised_top.append(name)
                    break

        revised_top = revised_top[:5]
        report = {"title": 'Gossip Report', "total": None, "items": revised_top, "subreport": None}
        return report


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
        report = {
            "title": title,
            "total": total_count if isinstance(total_count, int) else None,
            "items": [],
            "subreport": subreport
        }

        if total_count != 0:
            # Sort dictionary by count so each report appears sorted. 
            sorted_count = sorted(key_val.items(), key=operator.itemgetter(1), reverse=shouldDescend)
            report["items"] = [{'name': self._map_member_ID_to_name(x[0]), 'count': x[1]} for x in filter(lambda item: item[1] > 0, sorted_count)]

        return report


    def _map_member_ID_to_name(self, ID):
        if ID in self.members:
            return self.members[ID]

    '''
    def _clean_and_tokenize(self, messages):
        tokenized = []

        for message in messages:
            if not message['text']: continue
            text = message['text']
            text = text.strip().split()

            for i in range(0, len(text)):
                word = ''.join(x for x in text[i] if x.isalnum())
                word = word.lower()
                if word.startswith('http'): continue
                text[i] = word
            
            message['text'] = text
            tokenized.append(message)
	    
        return tokenized
 

    def _clean_and_tokenize_message(self, message):
        if not msg['text']: return ""
        message = message['text']
        message = message.strip().split()

        for i in range(0, len(message)):
            word = ''.join(x for x in message[i] if x.isalnum())
            word = word.lower()
            if not word.startswith('http'):
                message[i] = word
            
        return message


    def _map_member_IDs_to_names(self, per_member_count):
        name_and_count = {}

        for member_ID, count in per_member_count.items():
            for ID, name in self.members:
                if member_ID == ID:
                    name_and_count[name] = count

        return name_and_count


    def _initialize_per_member_count(self):
        ID_and_count = {}

        for ID in self.members:
            ID_and_count[ID] = 0

        return ID_and_count
    '''
