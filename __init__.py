from mycroft import MycroftSkill, intent_file_handler
from mycroft.messagebus.message import Message
from mycroft.util.parse import match_one
import time

class CommonStorytelling(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        self.add_event('storytelling.response', self.handle_response)

    @intent_file_handler('storytelling.common.intent')
    def handle_storytelling_common(self, message):
        self.log.info('commonstorytelling is calles')
        if message.data.get("story") is None:
            response = self.get_response('which_story', num_retries=0)
            if response is None:
                return
        else:
            response = message.data.get("story")
            self.speak_dialog('let_me_think', data={"story": response})
            self.stories = []
            self.bus.emit(Message("storytelling", {'story': response}))
            time.sleep(5)
            if self.stories is []:
                self.speak_dialog('no_story')
                return
            stories = sorted(self.stories, reverse=True)
            story = stories[0]
            if float(story[0]) < 0.8:
                self.speak_dialog('that_would_be', data={"story": story[2]})
                response = self.ask_yesno('is_it_that')
                if not response or response is 'no':
                    self.speak_dialog('no_story')
                    return
            self.speak_dialog('i_know_that', data={"story": story[2]})
            self.settings['story'] = story
            self.log.info('choose ' + str(stories[0]))
            self.bus.emit(Message("storytelling."+story[1], {'story': story[2]}))


    def handle_response(self, message):
        self.log.info('response gotten from ' + message.data.get('skill'))
        self.stories.append((str(message.data.get('confidence')),
                             message.data.get('skill'),
                             message.data.get('title')))


def create_skill():
    return CommonStorytelling()

