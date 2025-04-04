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
    NAME_IN_URL = 'position_shuffle'
    PLAYERS_PER_GROUP = 3 ##!!!!! 3 is for testing change it back###
    NUM_ROUNDS = 4 ##!!!!! 2 is for testing change it back###
    FST_ROLE = '1st'
    SCD_ROLE = '2nd'
    TRD_ROLE = '3rd'
    FOUR_ROLE = '4th'
    FIF_ROLE = '5th'

    # Payoff settings
    PAYOFF_S1 = cu(2)   # Prize if the first "No" in rounds 1–5
    PAYOFF_S2 = cu(4)   # Prize if the first "No" in rounds 6–10
    PAYOFF_GOOD = cu(6) # If everyone cooperates
    PAYOFF_LOSE = cu(0) # Others if someone quits

class Subsession(BaseSubsession):
    """
    Random grouping for the first 5 rounds.
    For rounds 6–10, copy the group matrix from 5 rounds ago.
    """
    def creating_session(self):
        if self.round_number <= 5:
            self.group_randomly()
        else:
            self.group_like_round(self.round_number - 5)

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
    age = models.IntegerField(label="1. What is your age?", min=10, max=100)

    gender = models.StringField(
        choices=[
            ['male', 'Male'],
            ['female', 'Female'],
            ['nonbinary', 'Non-binary'],
            ['prefer_not_say', 'Prefer not to say'],
        ],
        label="2. What is your gender?",
        widget=widgets.RadioSelect
    )

    country = models.StringField(label="3. What country are you from?")

    ai_familiarity = models.StringField(
        choices=[
            ['none', 'None'],
            ['low', 'Low'],
            ['medium', 'Medium'],
            ['high', 'High'],
            ['expert', 'Expert'],
        ],
        label="4. How familiar are you with Artificial Intelligence (AI)?",
        widget=widgets.RadioSelect
    )

# FUNCTIONS

# This function random the positions of player each round and store the group matrix
# set the round number as 4 for now, change it to 10 at last
def creating_session(subsession):
    #change the criterion to 5
    # advice_type = subsession.session.config['advice_type']
    # player = subsession.get_players()
    # if advice_type == 1:
    #     player.participant.vars['advice_type'] = 'None'
    # elif advice_type == 2:
    #     player.participant.vars['advice_type'] = 'Expert'
    # elif advice_type == 3:
    #     player.participant.vars['advice_type'] = 'AI'
    if subsession.round_number <= 2:
        subsession.group_randomly()
    if subsession.round_number >2:
        #change to '-5'
        subsession.group_like_round(subsession.round_number-2)


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
        # Show advice in round 5(For test, 3!!)
        show_advice = (self.round_number == 2)
        
        # Pass prize information, the cooperation question, and roles
        if player.round_number<=3 or (player.round_number >5 and player.round_number <=8): 
            prize = C.PAYOFF_S1
        elif (player.round_number > 3 and player.round_number <= 5) or (player.round_number > 8):
            prize = C.PAYOFF_S2
        return {
                'prize_if_no': prize,
                'prize_if_yes': C.PAYOFF_GOOD,
                'role': player.role,
                'cooperation_question': "Do you want to cooperate?"  # Add the cooperation question here
                'show_advice': show_advice,
            }
        
    
# class PositionDisplay(Page):
#     form_model = 'player'
#     form_fields = []

#     def before_next_page(self):
#         # Shuffle positions at the start of each round
#         set_positions(self.group)

#     def vars_for_template(self):
#         return {
#             'player_position': self.player.position,
#             'all_positions': [(p.id_in_group, p.position) for p in self.group.get_players()]
#         }


class ResultsWaitPage(WaitPage):
    """
    WaitPage to ensure all players have chosen.
    Then set payoffs.
    """
    after_all_players_arrive = set_payoffs


class Results(Page):
    """
    Show results only on round 5 or round 10.
    Optionally reset payoffs after round 5 if desired.
    """
    form_model = 'player'
    def is_displayed(self):

        return self.round_number == 2 or self.round_number == C.NUM_ROUNDS

    def vars_for_template(self):
        # Example: reset everyone's payoff to 0 after round 5
        # (Remove if you don't want to reset.)
        # advice_type = self.participant.vars['advice_type']
        if self.round_number == 3:
            for p in self.group.get_players():
                p.participant.payoff = cu(0)
        return {
            # 'advice_type': advice_type,
            'total_payoff': self.participant.payoff
        }

class Demographic(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'country', 'ai_familiarity']
    def is_displayed(self):

        return self.round_number == C.NUM_ROUNDS

page_sequence = [Introduction, AgentPage, ResultsWaitPage, Results, Demographic]

# page_sequence = [Introduction, AgentPage, Results]
