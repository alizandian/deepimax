Overview:
Deepimax is an adversarial search over deep decision trees, a better alternative to MinimaxABP or Expectimax made in 2015 for my university article.
It's also submitted as a paper in the 2015 IEEE Hamedan Student Branch. Code: C-IT16-09950264
Deepimax offers more efficient and practical searching in terms of time and space complexity.

Project:
This project has been made for the deepimax implementation and comparison to other available ones in the same area (Minimax, Expectimax, etc...) for benchmarking.
A game based on Fox and Sheeps has been made as an environment or playground in a python application with minimum dependencies.

Install:
The easiest way is to use conda like below, but you still can manually create the environment, but keep in mind the python and plotly versions.

make conda environment as follows:
- conda create --name [name] python=3.7
- conda activate [name]
install plotly
- conda install plotly

To assure everything is in place, use 'conda list' and compare installed packages with the following, which is a tested working environment:

# Name                    Version                   Build  Channel
ca-certificates           2019.11.27                    0
certifi                   2019.11.28               py37_0
openssl                   1.1.1d               he774522_3
pip                       20.0.2                   py37_0
plotly                    4.4.1                      py_0
python                    3.7.6                h60c2a47_2
retrying                  1.3.3                    py37_2
setuptools                45.1.0                   py37_0
six                       1.14.0                   py37_0
sqlite                    3.30.1               he774522_0
vc                        14.1                 h0510ff6_4
vs2015_runtime            14.16.27012          hf0eaf9b_1
wheel                     0.33.6                   py37_0
wincertstore              0.2                      py37_0

FoxAndSheeps.py is the root file, start the python project from here.

Algorithms Variables and Heuristics (parameters):
Fox & Sheeps: You can select 'bot' or 'player' to represent these roles in the game. 
player: In cases you want to play against the bots.
bot: You can choose among benchmark algorithms like Minimax, Minimax alpha beta pruning, and Expectimax or the proposed algorithm Deepimax.

depth: All these algorithms have a property called 'depth', which indicates how far the algorithm is allowed to go deep in the decision tree (for testing purposes)
Deepimax has two more properties, roa and doa (range of accuracy and depth of accuracy) which is best to leave as it is unless you know what you're doing.
Max Moves: You can select game move counts for each time you press Start, and then for that amount the game proceeds.
Turn time: Time cap for each turn.

Heuristic algorithms parameters (Evaluation function aspects)
These variables are changeable in the UI, for controlling the bots behaviors (change to current values could result in abnormal behaviors, proceed with caution!)
SM (Sheeps Separation): How important is for all sheep to stay close to each other.
SCM (Effectiveness of remaining sheeps count): How important is reducing sheep counts
ADM (Average distance between the fox and sheeps): How important is fox's distance to the center of cheeps.
AMM (Available move count): How important is not being in surrounding spots.
ACM (Available capture count): How important is having more options to capture sheeps.

Don't forget to press 'accept' for these heuristics changes.

Statistics and charts:
You can generate charts and diagrams for better comparison tools, seeing time and space complexity and the made and gauged tree itself!
for such uses, check 'Draw Tree' which draws the tree after each play.
for comparing time and space complexity, check the 'Compare' radio button.
These two are based on plotly, which will open a browser and shows the result in there.
