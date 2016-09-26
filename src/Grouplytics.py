import operator
from src.CipherDecoder import decode

class Grouplytics:
    def __init__(self, members, messages):
        self.members = members
        self.messages = messages 
        self.total_message_count_per_member = self._initialize_per_member_count()


    def overall_message_report(self):
        total_count = 0
        per_member_count = self._initialize_per_member_count()
         
        for message in self.messages:
            total_count += 1
            per_member_count[message['user_id']] += 1
            self.total_message_count_per_member[message['user_id']] += 1
         
        return self._generate_report('Message Count', total_count, per_member_count)
         
         
    def swear_word_report(self):
        total_count = 0
        swear_words = decode('swear_words.txt')
        per_member_count = self._initialize_per_member_count()

        for message in self.messages:
            text = self._clean_and_tokenize_message(message)
            for word in text:
                if word in swear_words:
                    total_count += 1
                    swear_words[word] += 1
                    per_member_count[message['user_id']] += 1

        report = self._generate_report('Swear Word Count', total_count, per_member_count)
        report += 'Top 10: \n' 
        top_10 = sorted(swear_words.items(), key = operator.itemgetter(1), reverse = True)
        for i in range(0, 10): 
            report += '  - {}: {}\n'.format(top_10[i][0], top_10[i][1])
         
        return report + '\n'
        
 
    def most_liked_report(self):
        total_count = 0
        per_member_count = self._initialize_per_member_count()
        for message in self.messages:
            if message['favorited_by']:
                total_count += len(message['favorited_by'])
                per_member_count[message['user_id']] += len(message['favorited_by'])

        # Divide total likes received by total messages sent to determine average likes per message
        avg_per_message = self._initialize_per_member_count()
        for user_ID in per_member_count:
            avg_per_message[user_ID] = round(float(per_member_count[user_ID]) / self.total_message_count_per_member[user_ID], 2)

        report = self._generate_report('Total Likes Received', total_count, per_member_count)
        report += self._generate_report('Likes Received Per Message', None, avg_per_message, True, False)
        return report


    def biggest_liker_report(self):
        total_count = 0
        per_member_count = self._initialize_per_member_count()
        for message in self.messages:
            favorited_by = message['favorited_by']
            if favorited_by:
                total_count += len(favorited_by)
                for member in favorited_by:
                    per_member_count[member] += 1

        return self._generate_report('Messages Liked', total_count, per_member_count)


    def meme_lord_report(self):
        total_count = 0
        per_member_count = self._initialize_per_member_count()
        for message in self.messages:
            if message['attachments']:
                for attachment in message['attachments']:
                    if attachment['type'] == 'image' or attachment['type'] == 'linked_image':
                        total_count += 1
                        per_member_count[message['user_id']] += 1

        return self._generate_report('Dank Memes Shared', total_count, per_member_count)


    def donald_trump_report(self):
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
            
        return self._generate_report('The Donald Trump Report (AKA: Shortest Average Word Length)', None, avg_word_length, False, False)


    def dude_report(self):
        total_count = 0
        per_member_count = self._initialize_per_member_count()
        for message in self.messages:
            text = self._clean_and_tokenize_message(message)
            # TODO: This will inevitably miss some. Has to be a better way to generate permutations
            if [i for i in ['dude', 'dudes', 'duuude', 'duuuude', 'duuuuude', 'duuuuuude', 'duudddeee'] if i in text]:
                total_count += 1
                per_member_count[message['user_id']] += 1

        return self._generate_report("'dude' count", total_count, per_member_count) 


    # Pass in a dictionary with member user IDs being the keys and lists of GF/BF aliases being the values
    # Example: {'Mike': ['Eleanor', 'Ellie'], 'Bennett': ['Payton', 'PP', 'Slim Payt']}
    def GFBF_report(self, GFBF_dictionary):
        count = 0
        name_and_ID = self._map_user_IDs_to_names()
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


    def most_popular_hour_report(self):
        import datetime as dt
        ref_date = dt.datetime.fromtimestamp(self.messages[0]["created_at"])
        ref_date -= dt.timedelta(minutes=ref_date.minute, seconds=ref_date.second, microseconds=ref_date.microsecond)
        time_elapsed = 3600  # 3600 seconds per hour; unix time measured in seconds

        count = 0
        max_count = 0
        max_date = ref_date
        for message in self.messages:
            if dt.datetime.fromtimestamp(message['created_at']) > ref_date:
                count += 1
            else:
                if count > max_count:
                    max_count = count
                    max_date = ref_date
                    ref_date -= dt.timedelta(seconds=time_elapsed)  # changing reference date to hour before
                count = 1  # adding the message not in range to count for next hour

        print('Most Popular Day Report:\n')
        print('Date: {}\n'.format(max_date.strftime('%Y-%m-%d')))
        print('Total Messages: {}\n'.format(max_count))


    def most_popular_day_report(self):
        import datetime as dt
        ref_date = dt.datetime.fromtimestamp(self.messages[0]["created_at"])
        ref_date -= dt.timedelta(hours= ref_date.hour, minutes=  ref_date.minute, seconds = ref_date.second, microseconds = ref_date.microsecond)
        time_elapsed = 86400 # 86400 seconds per day; unix time measured in seconds

        count = 0
        max_count = 0
        max_date = ref_date
        for message in self.messages:
            if dt.datetime.fromtimestamp(message['created_at']) > ref_date:
                count += 1
            else:
                if count > max_count:
                    max_count = count
                    max_date = ref_date
                    ref_date -= dt.timedelta(seconds= time_elapsed) # changing reference date to day before
                count = 1 # adding the message not in range to count for next day
                
        print('Most Popular Day Report:\n')
        print('Date: {}\n'.format(max_date.strftime('%Y-%m-%d')))
        print('Total Messages: {}\n'.format(max_count))


    def most_popular_week_report(self):
        import datetime as dt
        ref_date = dt.datetime.fromtimestamp(self.messages[0]["created_at"])
        ref_date -= dt.timedelta(days= ref_date.day ,minutes=ref_date.minute, seconds=ref_date.second, microseconds=ref_date.microsecond)
        time_elapsed = 604800  # 604800 seconds per week; unix time measured in seconds

        count = 0
        max_count = 0
        max_date = ref_date
        for message in self.messages:
            if dt.datetime.fromtimestamp(message['created_at']) > ref_date:
                count += 1
            else:
                if count > max_count:
                    max_count = count
                    max_date = ref_date
                    ref_date -= dt.timedelta(seconds=time_elapsed)  # changing reference date to week before
                count = 1  # adding the message not in range to count for next week

        print('Most Popular Day Report:\n')
        print('Date: {}\n'.format(max_date.strftime('%Y-%m-%d')))
        print('Total Messages: {}\n'.format(max_count))


    def _generate_report(self, title, total_count, per_member_count, shouldDescend = True, includePercent = True):
        report = title + ': {}\n'.format(total_count if isinstance(total_count, int) else '')
        
        if total_count == 0:
            return report
        
        # Sort dictionary by count so each report appears sorted. 
        sorted_count = sorted(per_member_count.items(), key = operator.itemgetter(1), reverse = shouldDescend)
         
        if includePercent: 
            return self._generate_report_with_percent(report, total_count, sorted_count)
        
        for i in range(0, len(sorted_count)):
            report += '  - {}: {}\n'.format(self._map_member_ID_to_name(sorted_count[i][0]), sorted_count[i][1])

        return report + '\n'
         

    def _generate_report_with_percent(self, report, total_count, sorted_count):
        for i in range(0, len(sorted_count)):
            report += '  - {}: {} ({:.2f}%)\n'.format(self._map_member_ID_to_name(sorted_count[i][0]),
                  sorted_count[i][1], (float(sorted_count[i][1]) / total_count) * 100)

        return report + '\n'


    def _clean_and_tokenize_message(self, msg, tokenize = True):
        message = msg['text']
        if message == None: return ""
        message = message.strip().split()

        for i in range(0, len(message)):
            word = ''.join(x for x in message[i] if x.isalnum())
            word = word.lower()
            if not word.startswith('http'):
                message[i] = word

        if not tokenize: message = ' '.join(message)
        return message


    def _initialize_per_member_count(self):
        ID_and_count = {}
        for name, ID in self.members.items():
            ID_and_count[ID] = 0
        return ID_and_count


    def _map_member_ID_to_name(self, ID):
        for name in self.members: 
            if ID == self.members[name]:
                return name 


    def _map_member_IDs_to_names(self, per_member_count):
        name_and_count = {}
        for ID, count in per_member_count.items():
            for name in self.members: 
                if ID == self.members[name]:
                    name_and_count[name] = ID
        return name_and_count

    '''
    IN PROGRESS
    def single_word_report(self, word):
        word_count = self._determine_word_count(word)
        print("'{}' count:".format(word))
        self._output_report(word_count)

    def phrase_report(self, phrase):
        count = 0
        per_member_count 	
        for message in self.messages:
            text = self._clean_and_tokenize_message(message, False)
            if phrase in text:
                count += 1
                self.members[message['user_id']] += 1

        print("Mention of '{}': {}".format(phrase, count))
        self._output_report()

    def _determine_word_count(self, word_to_search):
        count = 0
        for message in self.messages:
            text = self._clean_and_tokenize_message(message)
            if word in text:
                count += 1
        return count
    '''
