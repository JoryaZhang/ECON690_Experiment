from otree.api import *
import random

doc = """
This experiment involves assigning random positions to players in each round.
Each player is assigned a unique position from 1 to 5 in each round. The positions 
are shuffled every round, and players are informed of their position.
"""

class C(BaseConstants):
    ##!!!!! Reduce players and round is for testing, change it back!!!!###
    NAME_IN_URL = 'position_shuffle'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 2 ##!!!!! 2 is for testing change it back###
    FST_ROLE = '1st'
    SCD_ROLE = '2nd'
    TRD_ROLE = '3rd'
    FOUR_ROLE = '4th'
    FIF_ROLE = '5th'

    PAYOFF_BAD = cu(4)  # Prize if the player chooses "No"
    PAYOFF_GOOD = cu(10)
    PAYOFF_LOSE = cu(0)

class Subsession(BaseSubsession):
    def creating_session(self):
        self.group_randomly()


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    cooperate = models.BooleanField(
        choices=[[True, 'Yes'], [False, 'No']],
        doc="""This player's decision""",
        widget=widgets.RadioSelect,
    )


# FUNCTIONS
# def set_positions(group: Group):
#     players = group.get_players()
#     random.shuffle(positions)  # Shuffle positions
#     for i, player in enumerate(players):
#         player.position = positions[i]
def creating_session(subsession):
    subsession.group_randomly()

def other_player(player: Player):
    return player.get_others_in_group()[0]

def set_payoffs(group: Group):
    players = group.get_players()

    # Find the first player who chose "No"
    first_no_player = None
    for player in players:
        if player.cooperate is False:
            first_no_player = player
            break  # Stop at the first player who chooses "No"

    # Set payoffs based on the new rule
    if first_no_player:
        for player in players:
            if player.cooperate is False:
                if player == first_no_player:
                    player.payoff = C.PAYOFF_BAD  # First "No" player gets PAYOFF_BAD
                else:
                    player.payoff = C.PAYOFF_LOSE  # Other "No" players get PAYOFF_LOSE
            else:
                player.payoff = C.PAYOFF_GOOD  # Players who choose "Yes" get PAYOFF_GOOD
    else:
        for player in players:
            player.payoff = C.PAYOFF_GOOD  # If all choose "Yes", everyone gets PAYOFF_GOOD

    # Update the total payoff for each player


# PAGES
class Introduction(Page):
    pass

class AgentPage(Page):
    form_model = 'player'
    form_fields = ['cooperate']  
    def vars_for_template(player):
        # Pass prize information, the cooperation question, and roles
        return {
            'prize_if_no': C.PAYOFF_BAD,
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
        # Show results only after the last round
        return player.round_number == C.NUM_ROUNDS
    def vars_for_template(player):
        # Pass total payoff to the template
        return {
            'total_payoff': player.payoff
        }
page_sequence = [Introduction, AgentPage, ResultsWaitPage, Results]
