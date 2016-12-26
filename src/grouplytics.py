import re
import operator
from src.cipher_decoder import decode


class Grouplytics:
    def __init__(self, members, messages):
        self.members = members
        self.messages = messages
        # TODO: I don't like this
        self.total_message_count_per_member = self._initialize_per_member_count()


    def overall_message_report(self):
        total_count = 0
        # TODO: I don't like how we have to initialize this for every report. Way to reduce redundancy?
        per_member_count = self._initialize_per_member_count()

        for message in self.messages:
            total_count += 1
            per_member_count[message['user_id']] += 1

        return self._generate_report('Message Count', total_count, per_member_count)

    def likes_received(self):
        total_count = 0
        per_member_count = self._initialize_per_member_count()
        total_message_count_per_member = self._initialize_per_member_count()

        for message in self.messages:
            total_message_count_per_member[message['user_id']] += 1
            if message['favorited_by']:
                total_count += len(message['favorited_by'])
                per_member_count[message['user_id']] += len(message['favorited_by'])

        # Divide total likes received by total messages sent to determine average likes per message
        avg_per_message = self._initialize_per_member_count()
        for user_ID in per_member_count:
            avg_per_message[user_ID] = round(
                float(per_member_count[user_ID]) / total_message_count_per_member[user_ID], 2)

        subreport = self._generate_report('Likes Received Per Message', None, avg_per_message, includePercent=False)
        report = self._generate_report('Likes Received', total_count, per_member_count, subreports=[subreport])
        return report

    def messages_liked(self):
        total_count = 0
        per_member_count = self._initialize_per_member_count()

        for message in self.messages:
            favorited_by = message['favorited_by']
            if favorited_by:
                total_count += len(favorited_by)
                for member in favorited_by:
                    if member in per_member_count: 
                        per_member_count[member] += 1

        return self._generate_report('Messages Liked', total_count, per_member_count)

    def swear_word_report(self):
        total_count = 0
        swear_words = decode('swear_words.txt') # TODO: add more!
        per_member_count = self._initialize_per_member_count()

        for message in self.messages:
            text = self._clean_and_tokenize_message(message)
            for word in text:
                if word in swear_words:
                    total_count += 1
                    swear_words[word] += 1
                    per_member_count[message['user_id']] += 1

        if total_count > 9:
            subreport = {"title": 'Top 10', "type": 'Top 10', "total": None, "items": [], "subreports": None}
            top_10 = sorted(swear_words.items(), key=operator.itemgetter(1), reverse=True)
            for i in range(0, 10):
                subreport['items'].append({'name': top_10[i][0], 'count': top_10[i][1]})

        report = self._generate_report('Swear Word Count', total_count, per_member_count, subreports=[subreport])
        return report

    # TODO: what's the difference between image and linked image?
    def images_shared(self):
        total_count = 0
        per_member_count = self._initialize_per_member_count()
        for message in self.messages:
            if message['attachments']:
                for attachment in message['attachments']:
                    if attachment['type'] == 'image' or attachment['type'] == 'linked_image':
                        total_count += 1
                        per_member_count[message['user_id']] += 1

        return self._generate_report('Images Shared', total_count, per_member_count)

    def average_word_length(self):
        cumulative_word_count = {}
        cumulative_word_length = {}
        members = self._initialize_per_member_count()

        for user_ID in members:
            cumulative_word_count[user_ID] = 0
            cumulative_word_length[user_ID] = 0

        for message in self.messages:
            text = self._clean_and_tokenize_message(message)
            for word in text:
                cumulative_word_count[message['user_id']] += 1
                cumulative_word_length[message['user_id']] += len(word)

        # Divide total word length by total word count to determine average word length per member
        avg_word_length = self._initialize_per_member_count()
        for user_ID in members:
            avg_word_length[user_ID] = round(float(cumulative_word_length[user_ID]) / cumulative_word_count[user_ID], 2)

        return self._generate_report('Average Word Length', None, avg_word_length, True, False)

    def dude_report(self):
        total_count = 0
        per_member_count = self._initialize_per_member_count()
        pattern = re.compile('d+u+d+e+')

        for message in self.messages:
            text = self._clean_and_tokenize_message(message)
            for word in text:
                if pattern.match(word):
                    total_count += 1
                    per_member_count[message['user_id']] += 1

        return self._generate_report("'dude' count", total_count, per_member_count)


    # Example: {'Mike': ['Eleanor', 'Ellie'], 'Bennett': ['Payton', 'PP', 'Slim Payt']}
    # TODO: consider scrapping. too hard to have user configure.
    # IDEA! who talks about boys the most; who talks about girls the most. would need to filter out sexually amibiguous names
    def GFBF_report(self, GFBF_dictionary):
        count = 0
        name_and_ID = self._map_member_IDs_to_names()
        per_member_count = self._initialize_per_member_count()

        for member, aliases in GFBF_dictionary.items():
            for i in range(len(aliases)):
                aliases[i] = aliases[i].lower()

        for message in self.messages:
            text = self._clean_and_tokenize_message(message, False)
            for member, GFBF_aliases in GFBF_dictionary.items():
                for GFBF_name in GFBF_aliases:
                    if name in text and message['user_id'] == name_and_ID[member]:
                        count += 1
                        per_member_count[message['user_id']] += 1
                        break

        print("Mention of BF/GF: {}".format(count))
        self._output_report(count)


    def _generate_report(self, title, total_count, per_member_count, shouldDescend=True, includePercent=True, subreports=[]):
        report = {
            "type": title, # both type and title for flexibility
            "title": title,
            "total": total_count if isinstance(total_count, int) else None,
            "items": [],
            "subreports": subreports 
        }

        if total_count == 0:
            return report

        # Sort dictionary by count so each report appears sorted. 
        sorted_count = sorted(per_member_count.items(), key=operator.itemgetter(1), reverse=shouldDescend)

        report["items"] = [{'name': self._map_member_ID_to_name(x[0]), 'count': x[1]}
                           for x in filter(lambda item: item[1] > 0, sorted_count)]
        return report

    def _clean_and_tokenize_message(self, msg):
        if not msg['text']: return ""
        message = msg['text']
        message = message.strip().split()

        for i in range(0, len(message)):
            word = ''.join(x for x in message[i] if x.isalnum())
            word = word.lower()
            if not word.startswith('http'):
                message[i] = word
            
        return message

    def _initialize_per_member_count(self):
        ID_and_count = {}
        for ID in self.members:
            ID_and_count[ID] = 0
        return ID_and_count

    def _map_member_ID_to_name(self, ID):
        if ID in self.members:
            return self.members[ID]

    def _map_member_IDs_to_names(self, per_member_count):
        name_and_count = {}
        for member_ID, count in per_member_count.items():
            for ID, name in self.members:
                if member_ID == ID:
                    name_and_count[name] = count
        return name_and_count
