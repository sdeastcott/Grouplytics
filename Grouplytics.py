from GroupMeWrapper import GroupMeWrapper

class Grouplytics:

    def __init__(self, group_ID):
        self.groupme = GroupMeWrapper()
        self.members = self._initialize_group(self.groupme.get_group_members(group_ID))
        self.messages = self.groupme.get_group_messages(group_ID)
        self.message_count = {}

    def generate_message_report(self):
        count = 0
        for message in self.messages:
            count += 1
            self.members[message['user_id']] += 1

        print('Total Message Count: {}'.format(count))
        self._set_member_message_count()
        self._output_report(count)
        self._reset_member_count()

    def swear_word_report(self):
        # TODO: This needs to be pulled from a file that won't be visible to the public.
        swear_words = {

        }

        count = 0
        for message in self.messages:
            text = self._clean_and_tokenize_message(message)
            for word in text:
                if word in swear_words:
                    count += 1
                    swear_words[word] += 1
                    self.members[message['user_id']] += 1

        print("Swear Word Count: {}".format(count))
        self._output_report(count)
        # TODO: Swear word break-down per member
        self._reset_member_count()


    def most_liked_report(self):
        if not self.message_count:
            for message in self.messages:
                self.members[message['user_id']] += 1

            for member, count in self.members.items():
                self.message_count[member] = count

        count = 0
        for message in self.messages:
            if message['favorited_by']:
                count += len(message['favorited_by'])
                self.members[message['user_id']] += len(message['favorited_by'])

        print("Total Likes Received:")
        self._output_report(count)

        print("Likes Received Per Message:")
        names = self._map_user_IDs_to_names()
        for name, user_ID in names.items():
            print('  - {}: {:.2f}'.format(name, float(self.members[user_ID]) / self.message_count[user_ID]))
        print

        self._reset_member_count()


    def biggest_liker_report(self):
        count = 0
        for message in self.messages:
            favorited_by = message['favorited_by']
            if favorited_by:
                count += len(favorited_by)
                for member in favorited_by:
                    self.members[member] += 1

        print("Messages Liked: {}".format(count))
        self._output_report(count)
        self._reset_member_count()


    def biggest_complainer_report(self):
        pass

    def meme_lord_report(self):
        count = 0
        for message in self.messages:
            if message['attachments']:
                for attachment in message['attachments']:
                    # TODO: Not exactly sure what a 'linked_image' entails
                    if attachment['type'] == 'image' or attachment['type'] == 'linked_image':
                        count += 1
                        self.members[message['user_id']] += 1

        print("Dank Memes Shared: {}".format(count))
        self._output_report(count)
        self._reset_member_count()


    def most_popular_time_report(self):
        pass


    def most_popular_day_report(self):
        pass


    def donald_trump_report(self):
        cumulative_word_count = {}
        cumulative_word_length = {}
        for member in self.members:
            cumulative_word_count[member] = 0
            cumulative_word_length[member] = 0

        for message in self.messages:
            text = self._clean_and_tokenize_message(message)
            for word in text:
                cumulative_word_count[message['user_id']] += 1
                cumulative_word_length[message['user_id']] += len(word)

        print("Shortest Average Word Length (AKA, The Donald Trump Report):")
        names = self._map_user_IDs_to_names()
        for name, user_ID in names.items():
            print('  - {}: {:.2f}'.format(name, float(cumulative_word_length[user_ID]) / cumulative_word_count[user_ID]))
        print


    def dude_report(self):
        count = 0
        for message in self.messages:
            text = self._clean_and_tokenize_message(message)
            if [i for i in ['dude', 'dudes', 'duuude', 'duuuude', 'duuuuude', 'duuuuuude'] if i in text]:
                count += 1
                self.members[message['user_id']] += 1

        print("'dude' count: {}".format(count))
        self._output_report(count)
        self._reset_member_count()

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
        occurence_dict = {}
        occurence_dict[word] = 0
        word_count = self._determine_word_count(word)

        print("'{}' count:".format(word))
        self._output_report()
        self._reset_member_count()

    # Say you want to see how often 'Delia Hurley' was mentioned. It would probably
    # make most sense to search for 'Delia' OR 'Hurley' in case someone referred to
    # her by last name.
    # TODO: Need a more descriptive function name
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


    def phrase_report(self, phrase):
        count = 0
        for message in self.messages:
            text = self._clean_and_tokenize_message(message, False)
            if phrase in text:
                count += 1
                self.members[message['user_id']] += 1

        print("Mention of '{}': {}".format(phrase, count))
        self._output_report()
        self._reset_member_count()


    def _output_report(self, count):
        names = self._map_user_IDs_to_names()
        for name, user_ID in names.items():
            print('  - {}: {} ({:.2f}%)'.format(name, self.members[user_ID], (float(self.members[user_ID]) / count) * 100))
        print


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


    def _initialize_group(self, member_set):
        members = {}
        for member in member_set:
            members[member] = 0

        return members


    # TODO: Need to make this scalable
    def _map_user_IDs_to_names(self):
        names = {}
        names['Adam'] = '10976478'
        names['Bennett'] = '12135911'
        names['Neil'] = '16630043'
        names['Ryan'] = '12565290'
        names['Steve'] = '13342675'
        return names


    def _reset_member_count(self):
        for member in self.members:
            self.members[member] = 0


    def _set_member_message_count(self):
        for member, count in self.members.items():
            self.message_count[member] = count


# TODO: Throw all this into a different file and have the user give a configuration file
# to read from, or have them enter the information manually. This will make all this much
# more scalable.
def main():
    groupme = GroupMeWrapper()
    groups = groupme.get_groups()

    for group in groups:
        if group['name'] == 'Tuscaloosa Safe Space Department':
            grouplytics = Grouplytics(group['id'])

    grouplytics.generate_message_report()
    grouplytics.swear_word_report()
    grouplytics.most_liked_report()
    grouplytics.biggest_liker_report()
    grouplytics.donald_trump_report()
    #grouplytics.generate_biggest_complainer_report())
    grouplytics.meme_lord_report()
    #grouplytics.generate_biggest_word_report())
    grouplytics.dude_report()

    GFBFdictionary = {'Steve': ['Kat', 'Katherine'], 'Ryan': ['Elena'], 'Neil': ['Claire'], 'Bennett': ['Slim Payt', 'Payton', 'PJ'], 'Adam': ['Jordan']}
    grouplytics.GFBF_report(GFBFdictionary)

main()