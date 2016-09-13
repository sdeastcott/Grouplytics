class Grouplytics:
    def __init__(self, members, messages):
        self.members = members
        self.messages = messages 
        self.total_message_count_per_member = self._initialize_per_member_count()


    def total_message_report(self):
        count = 0
        per_member_count = self._initialize_per_member_count()
        for message in self.messages:
            count += 1
            per_member_count[message['user_id']] += 1
            self.total_message_count_per_member[message['user_id']] += 1

        print('Total Message Count: {}'.format(count))
        self._output_report(count, per_member_count)


    def swear_word_report(self):
        # TODO: Encode this so we can display on GitHub
        swear_words = {}

        count = 0
        per_member_count = self._initialize_per_member_count()
        for message in self.messages:
            text = self._clean_and_tokenize_message(message)
            for word in text:
                if word in swear_words:
                    count += 1
                    swear_words[word] += 1
                    per_member_count[message['user_id']] += 1

        print("Swear Word Count: {}".format(count))
        self._output_report(count, per_member_count)


    def most_liked_report(self):
        count = 0
        per_member_count = self._initialize_per_member_count()
        for message in self.messages:
            if message['favorited_by']:
                count += len(message['favorited_by'])
                per_member_count[message['user_id']] += len(message['favorited_by'])

        print("Total Likes Received:")
        self._output_report(count, per_member_count)

        print("Likes Received Per Message:")
        names = self._map_member_IDs_to_names(per_member_count)
        for name, user_ID in names.items():
            print('  - {}: {:.2f}'.format(name, float(per_member_count[user_ID]) / self.total_message_count_per_member[user_ID]))
        print()


    def biggest_liker_report(self):
        count = 0
        per_member_count = self._initialize_per_member_count()
        for message in self.messages:
            favorited_by = message['favorited_by']
            if favorited_by:
                count += len(favorited_by)
                for member in favorited_by:
                    per_member_count[member] += 1

        print("Messages Liked: {}".format(count))
        self._output_report(count, per_member_count)


    def meme_lord_report(self):
        count = 0
        per_member_count = self._initialize_per_member_count()
        for message in self.messages:
            if message['attachments']:
                for attachment in message['attachments']:
                    # TODO: Not exactly sure what a 'linked_image' entails
                    if attachment['type'] == 'image' or attachment['type'] == 'linked_image':
                        count += 1
                        per_member_count[message['user_id']] += 1

        print("Dank Memes Shared: {}".format(count))
        self._output_report(count, per_member_count)


    def donald_trump_report(self):
        members = self._initialize_per_member_count()
        cumulative_word_count = {}
        cumulative_word_length = {}
        for member in members:
            cumulative_word_count[member] = 0
            cumulative_word_length[member] = 0

        for message in self.messages:
            text = self._clean_and_tokenize_message(message)
            for word in text:
                cumulative_word_count[message['user_id']] += 1
                cumulative_word_length[message['user_id']] += len(word)

        print("Shortest Average Word Length (AKA, The Donald Trump Report):")
        names = self._map_member_IDs_to_names(members)
        for name, user_ID in names.items():
            print('  - {}: {:.2f}'.format(name, float(cumulative_word_length[user_ID]) / cumulative_word_count[user_ID]))
        print()


    def dude_report(self):
        count = 0
        per_member_count = self._initialize_per_member_count()
        for message in self.messages:
            text = self._clean_and_tokenize_message(message)
            if [i for i in ['dude', 'dudes', 'duuude', 'duuuude', 'duuuuude', 'duuuuuude'] if i in text]:
                count += 1
                per_member_count[message['user_id']] += 1

        print("'dude' count: {}".format(count))
        self._output_report(count, per_member_count)


    # Pass in a dictionary with member user IDs being the keys and lists of GF/BF aliases being the values
    # Example: {'Steven': ['Kat', 'Katherine'], 'Bennett': ['Payton', 'PP', 'Slim Payt']}
    # TODO: Function name could use some work.
    def GFBF_report(self, GFBFdictionary):
        count = 0

        for member, aliases in GFBFdictionary.items():
            for i in range(len(aliases)):
                aliases[i] = aliases[i].lower()

        user_IDs = self._map_user_IDs_to_names()
        for message in self.messages:
            text = self._clean_and_tokenize_message(message, False)
            for member, aliases in GFBFdictionary.items():
                for name in aliases:
                    if name in text and message['user_id'] == user_IDs[member]:
                        count += 1
                        self.members[message['user_id']] += 1
                        break

        print("Mention of BF/GF: {}".format(count))
        self._output_report(count)
        self._reset_member_count()


    def single_word_report(self, word):
        word_count = self._determine_word_count(word)
        print("'{}' count:".format(word))
        self._output_report(word_count)

    def most_popular_day_report(self):
        import datetime as dt
        refDate = dt.datetime.fromtimestamp(messages[0]["created_at"])
        refDate -= dt.timedelta(minutes = refDate.minute, seconds = refDate.second, microseconds = refDate.microsecond)
        timeElapsed = 86400 # 86400 seconds per day; unix time measured in seconds

        count = 0
        maxCount = 0
        for message in self.messages:
            if message['created_at'] in range(refDate, refDate - timeElapsed):
                count += 1
            else:
                if count > maxCount:
                    maxCount = count
                    maxDate = refDate
                refDate -= timeElapsed # changing reference date to day before
                count = 1 # adding the message not in range to count for next day
                
        print('Most Popular Day Report:\n')
        print('Date: {}\n'.format(maxDate.strftime('%Y-%m-%d')))
        print('Total Messages: {}\n'.format(maxCount))

    # Say you want to see how often 'Delia Hurley' was mentioned. It would probably
    # make most sense to search for 'Delia' OR 'Hurley' in case someone referred to
    # her by just her first or last name.
    # TODO: Incomplete; also need a more descriptive function name.
    def multiple_word_report(self, words):
        count = 0
        occurrence_dict = {}

        for word in words:
            occurrence_dict[word] = 0

        for message in self.messages:
            text = self._clean_and_tokenize_message(message)
            if [x for x in words if x in text]:
                count += 1
                occurence_dict[word] += 1
                self.members[message['user_id']] += 1


    # TODO: Incomplete
    def phrase_report(self, phrase):
        count = 0
        for message in self.messages:
            text = self._clean_and_tokenize_message(message, False)
            if phrase in text:
                count += 1
                self.members[message['user_id']] += 1

        print("Mention of '{}': {}".format(phrase, count))
        self._output_report()


    def _output_report(self, count, per_member_count):
        names = self._map_member_IDs_to_names(per_member_count) 
        for name, user_ID in names.items():
            print('  - {}: {} ({:.2f}%)'.format(name, per_member_count[user_ID], (float(per_member_count[user_ID]) / count) * 100))
        print()


    def _determine_word_count(self, word_to_search):
        count = 0
        for message in self.messages:
            text = self._clean_and_tokenize_message(message)
            if word in text:
                count += 1
        return count


    def _clean_and_tokenize_message(self, msg, tokenize = True):
        if not msg['text']:
            return ""

        message = msg['text']
        message = message.strip().split()
        for i in range(0, len(message)):
            word = ''.join(x for x in message[i] if x.isalnum())
            word = word.lower()
            # TODO: Better way to check for this?
            if not word.startswith('http'):
                message[i] = word

        if not tokenize:
            message = ' '.join(message)

        return message


    def _initialize_per_member_count(self):
        ID_and_count = {}
        for name, ID in self.members.items():
            ID_and_count[ID] = 0
        return ID_and_count


    def _map_member_IDs_to_names(self, per_member_count):
        name_and_count = {}
        for ID, count in per_member_count.items():
            for name in self.members: 
                if ID == self.members[name]:
                    name_and_count[name] = ID
        return name_and_count
