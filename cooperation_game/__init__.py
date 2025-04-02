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
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 4 ##!!!!! 2 is for testing change it back###
    FST_ROLE = '1st'
    SCD_ROLE = '2nd'
    TRD_ROLE = '3rd'
    FOUR_ROLE = '4th'
    FIF_ROLE = '5th'

    PAYOFF_S1 = cu(2)  # Prize if the player chooses "No"
    PAYOFF_GOOD = cu(6)
    PAYOFF_LOSE = cu(0)
    PAYOFF_S2 = cu(4)

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    def shuffle_role(group):
        group.get_players()


class Player(BasePlayer):
    cooperate = models.BooleanField(
        choices=[[True, 'Yes'], [False, 'I quit']],
        doc="""This player's decision""",
        widget=widgets.RadioSelect,
    )


# FUNCTIONS

# This function random the positions of player each round and store the group matrix
# set the round number as 4 for now, change it to 10 at last
def creating_session(subsession):
    #change the criterion to 5
    if subsession.round_number <= 2:
        subsession.group_randomly()
    if subsession.round_number >2:
        #change to '-5'
        subsession.group_like_round(subsession.round_number-2)
# def creating_session(subsession):
#     positions = []
#     if subsession.round_number <= 2:
#         subsession.group_randomly()
#         positions.append(subsession.get_group_matrix())
#     if subsession.round_number >2:
#         subsession.set_group_matrix(positions[-1])
#\\\\ didn't work\\\\\



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
    if player.round_number <=3:
    # Set payoffs based on the new rule
        if first_no_player is not None:
            for player in players:
                if player == first_no_player:
                    player.payoff = C.PAYOFF_S1  # First "No" player gets PAYOFF_S1
                else:
                    player.payoff = C.PAYOFF_LOSE  # Other players get PAYOFF_LOSE
        else:
            for player in players:
                player.payoff = C.PAYOFF_GOOD  # Everyone gets PAYOFF_GOOD
    elif player.round_number > 3:
        # Set payoffs based on the original rule
        if first_no_player is not None:
            for player in players:
                if player == first_no_player:
                    player.payoff = C.PAYOFF_S2  # First "No" player gets PAYOFF_S2
                else:
                    player.payoff = C.PAYOFF_LOSE  # Other players get PAYOFF_LOSE
        else:
            for player in players:
                player.payoff = C.PAYOFF_GOOD  # Everyone gets PAYOFF_GOOD


# PAGES
class Introduction(Page):
    pass

class AgentPage(Page):
    form_model = 'player'
    form_fields = ['cooperate']  
    def vars_for_template(player):
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
    
    after_all_players_arrive = set_payoffs 


class Results(Page):
    form_model = 'player'
    def is_displayed(player):
        # Show results only on round 2 or the final round
        return player.round_number == 2 or player.round_number == C.NUM_ROUNDS
    def vars_for_template(player):
        if player.round_number == 3:
            #reset everyone's payoff to zero
            for p in player.group.get_players():
                p.participant.payoff = cu(0)
        # Pass total payoff to the template
        return {
            'total_payoff': player.participant.payoff
        }
page_sequence = [Introduction, AgentPage, ResultsWaitPage, Results]

# page_sequence = [Introduction, AgentPage, Results]