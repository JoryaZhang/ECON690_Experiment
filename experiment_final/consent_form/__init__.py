from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'consent_form'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    consent = models.BooleanField()


# PAGES
class Consent_Form(Page):
    form_model = 'player'
    form_fields = ['consent']

class No_Consent(Page):
    @staticmethod
    def is_displayed(player):
        return player.consent == 0


page_sequence = [Consent_Form, No_Consent]
