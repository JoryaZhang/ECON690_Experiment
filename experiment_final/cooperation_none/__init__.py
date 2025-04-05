from otree.api import *
import random

doc = """
This experiment involves assigning random positions to players in each round.
Each player is assigned a unique position from 1 to 5 in each round. The positions 
are shuffled every round, and players are informed of their position.
"""
#####################
# 1. Check the criterion (highlighted lines), should change to 5/10 rounds
# 2. Check whether everyone's payoff is correct
#####################

class C(BaseConstants):
    ##!!!!! Reduce players and round is for testing, change it back!!!!###
    NAME_IN_URL = 'cooperation_none'
    PLAYERS_PER_GROUP = 5
    NUM_ROUNDS = 10
    FST_ROLE = '1st'
    SCD_ROLE = '2nd'
    TRD_ROLE = '3rd'
    FOUR_ROLE = '4th'
    FIF_ROLE = '5th'


    # Payoff settings
    PAYOFF_S1 = cu(3)   # Prize if the first "No" in rounds 1–5
    PAYOFF_GOOD = cu(6) # If everyone cooperates
    PAYOFF_LOSE = cu(0) # Others if someone quits

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    # def shuffle_role(group):
    #    group.get_players()
    pass

class Player(BasePlayer):
    cooperate = models.BooleanField(
        choices=[
            [True, 'Yes'],
            [False, 'I quit']
        ],
        doc="This player's decision each round",
        widget=widgets.RadioSelect,
    )

    # Demographic fields
    age = models.IntegerField(
        label="What is your age?",
        min=10,
        max=100,
    )

    gender = models.StringField(
        label="What is your gender?",
        choices=['Male', 'Female', 'Non-binary', 'Prefer not to say'],
        widget=widgets.RadioSelect,
    )

    country = models.StringField(
        label="What country do you currently live in?"
    )

    familiarity_ai = models.StringField(
        label="How familiar are you with Artificial Intelligence (AI)?",
        choices=[
            'Never heard before',
            'Slightly familiar',
            'Frequently use it',
            'Extremely familiar (major or expert in this field)'
        ],
        widget=widgets.RadioSelect,
    )

    education_level = models.StringField(
        label="What is your highest level of education?",
        choices=[
            'Less than high school',
            'High school diploma',
            'Some college',
            'Bachelor’s degree',
            'Master’s degree',
            'Doctorate or higher'
        ],
        widget=widgets.RadioSelect,
    )

    field_of_study = models.StringField(
        label="What is your field of study or work?"
    )

    english_proficiency = models.StringField(
        label="What is your English proficiency?",
        choices=[
            'Basic',
            'Intermediate',
            'Advanced',
            'Native'
        ],
        widget=widgets.RadioSelect,
    )

    prior_experiment_experience = models.StringField(
        label="Have you participated in online experiments before?",
        choices=['Yes', 'No', 'Not sure'],
        widget=widgets.RadioSelect,
    )

# FUNCTIONS

# This function random the positions of player each round and store the group matrix
# set the round number as 4 for now, change it to 10 at last
def creating_session(subsession):
    """
    Random grouping for the first 5 rounds.
    For rounds 6–10, copy the group matrix from 5 rounds ago.
    """

    if subsession.round_number <= 5:
        subsession.group_randomly()
    if subsession.round_number >5:
        #change to '-5'
        subsession.group_like_round(subsession.round_number-5)


# def shuffle_role(group: Group):
#     group.get_players()

def set_payoffs(group: Group):
    players = group.get_players()
    # Find the first player who chose "No"
    first_no_player = None
    for player in players:
        if player.cooperate is False:
            first_no_player = player
            break  # Stop at the first player who chooses "No"

    # Set payoffs based on the new rule
        # First 5 rounds
    if first_no_player is not None:
            # The first "No" gets PAYOFF_S1, others get 0
            for p in players:
                if p == first_no_player:
                    p.payoff = C.PAYOFF_S1  # First "No" player gets PAYOFF_S1
                else:
                    p.payoff = C.PAYOFF_LOSE  # Other players get PAYOFF_LOSE
    else:
            # Everyone cooperates
            for p in players:
                p.payoff = C.PAYOFF_GOOD  # Everyone gets PAYOFF_GOOD

def avg_payoff(group: Group):
    players = group.get_players()

    # Find the player(s) with the highest total payoff
    avg_payoff = sum(player.participant.payoff for player in players) / C.PLAYERS_PER_GROUP

    return avg_payoff


# PAGES
class Introduction(Page):
    """
    Shows multi-step instructions.
    Only displayed in round 1 (optional).
    """
    form_model = 'player'
    def is_displayed(player):
        # Show results only on round 2 or the final round
        return player.round_number == 1

class AgentPage(Page):
    """
    Page where players choose 'Yes' or 'I quit'.
    """
    form_model = 'player'
    form_fields = ['cooperate']
    def vars_for_template(player):

        # Pass prize information, the cooperation question, and roles
        return {
                'prize_if_no': C.PAYOFF_S1,
                'prize_if_yes': C.PAYOFF_GOOD,
                'role': player.role,
                'cooperation_question': "Do you want to cooperate?"  # Add the cooperation question here
            }




class ResultsWaitPage(WaitPage):
    """
    WaitPage to ensure all players have chosen.
    Then set payoffs.
    """
      # Increment the succeed counter
    after_all_players_arrive = set_payoffs


class Results(Page):
    """
    Show results only on round 5 or round 10.
    Optionally reset payoffs after round 5 if desired.
    """
    form_model = 'player'
    def is_displayed(self):

        return self.round_number == 5 or self.round_number == C.NUM_ROUNDS

    def vars_for_template(self):
        # self.participant.cooperate_count = 4
        # Calculate the number of successful cooperation rounds
        group = self.group
        avg = avg_payoff(group)
        if self.round_number == 5:
            round = int(avg // C.PAYOFF_GOOD)
        else:
            round = int(avg // (C.PAYOFF_GOOD *2))
        return {
            'succeed': round,
            'total_payoff': self.participant.payoff
            # 'succeed': self.success1 + self.success2 + self.success3 + self.success4 + self.success5,
        }
        # Example: reset everyone's payoff to 0 after round 5
        # (Remove if you don't want to reset.)
        # advice_type = self.participant.vars['advice_type']

class Demographic(Page):
    form_model = 'player'
    form_fields = [
        'age',
        'gender',
        'country',
        'familiarity_ai',
        'education_level',
        'field_of_study',
        'english_proficiency',
        'prior_experiment_experience',
    ]

    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS

class Finished(Page):
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS

    def vars_for_template(player):
        # Randomly pick 2 different rounds
        all_rounds = player.in_all_rounds()
        random_rounds = random.sample(all_rounds, 2)
        round1 = random_rounds[0]
        round2 = random_rounds[1]

        # Calculate total: fixed $5 + sum of 2 selected rounds
        bonus_amount = round1.payoff + round2.payoff
        total_dollars = cu(5) + bonus_amount

        # Save to participant for later export if needed
        player.participant.payoff = total_dollars

        return {
            'bonus1': round1.payoff,
            'bonus2': round2.payoff,
            'round1_number': round1.round_number,
            'round2_number': round2.round_number,
            'fixed_amount': cu(5),
            'total_bonus': bonus_amount,
            'total_payoff': total_dollars,
        }

page_sequence = [Introduction, AgentPage, ResultsWaitPage, Results, Demographic, Finished]

