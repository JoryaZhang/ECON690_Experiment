## ECON 690 Experiment Design
### We aim to design a cooperation game to study how the third-party advice can affect cooperation outcomes.

- We design the experiment to fix the number of people per group (5), and conduct it over
five rounds, each group completed the task only once, under one of three distinct treatment
conditions: no advice (it is the control group), human expert suggestions, or AI-generated
suggestions.

- At the end of 5 rounds, player's total payoff, the result, the suggestions from expert **or** the advice from AI will be
displayed on the screen when people decide whether to cooperate or not. Participants know
whether it is an expert’s opinion or a suggestion based on AI analysis. And all three groups
know get the information on the number of cooperate round in the previous 5
round.

- Each participant is assigned a position order, which they are aware of. Positions are randomly
assigned to individuals in each round.
- In each round, participants simultaneously choose
whether to cooperate or not. The first person in the sequence who chooses not to cooperate
receives a fixed revenue, while all other participants receive nothing. If everyone cooperates,
all participants receive a revenue higher than the fixed amount. At the end of each round,
everyone knows the results, including which positions did not choose to cooperate.

### Coding:

- We design three apps (cooperation_none, cooperation_expert, cooperation_AI) with most of the part identical. The only difference is the type of advice given to the participant.


________________________________


### March 29
Zhuoya

Done:
1. Randomize position at each rounds
2. set the payoff
3. set_payoff: Only the first person who reject can get the benefit
4. Only show the result page at the end of 5 rounds.
   
To-do:
1. Introduction part: explain the rule carefully, highlight
2. Set player payoff reasonably: repeat for 2/3 rounds and then change the payoff, repeat
3. Embellish the interface.
4. Design Result page

### March 30
Done:
1. set different payoff in different rounds
2. solve acculumate payoff

To-do:
1. Introduction part: explain the rule carefully, highlight
2. In the second-half (5 rounds after advice) of the game, make sure to repeat the roles for same player (try store the id_matrix in the first-half)
3. Embellish the interface.
4. Design Result page (Advice, whether to show others' payoff, show cooperation rate etc.)

### April 1
Done:
1. Repeat the roles for same player in the second half
2. Yuxuan: Finish and upload the Instructions part to explain the rule carefully and open to adjustment accordingly due to the bonus amount settings.

To-do:
1. Introduction part: explain the rule carefully, highlight. (Finish the instrunction structure code alreadly)
2. Embellish the interface.
3. Design Result page (Advice, whether to show others' payoff, show cooperation rate etc.)

### April 4
To-do:
1. keep the advice for the 5 rounds in the second phase
2. change the highlight of intruduction
3. add some quizzes to test understanding
4. keep the length of the advice (super similar to each other)
5. add simple questions to gather demographic information in the end

