from fontTools.varLib import models
from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'simplesurvey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    # Name of the participant
    name = models.StringField(label = "What's your name?")

    # Age of the participant
    age = models.IntegerField(label = "What's your age?", min=13, max =125)

    # Hair color with specific choices
    hair_color = models.StringField(
        label = "What's your hair color?",
        choices = ['brown','red','black','blue','golden'],
        widget=widgets.RadioSelectHorizontal
    )


# PAGES
class Survey(Page):
    # In this page, we will fill in player variables, so the relevant model is 'player.'
    form_model = 'player'

    # We will specifically fill in the name
    form_fields = ['name','age','hair_color']

class IQ_test(Page):
    iq_answer1 = models.StringField(
        label = 'What is your answer?',
        choices = ['A','B','C','D'],
        widget=widgets.RadioSelectHorizontal
    )

class Results(Page):
    pass


page_sequence = [Survey, IQ_test, Results]
