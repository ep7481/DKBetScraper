import random
from draftking_class import DraftKings
from xlwt import Workbook

wb = Workbook()
sheet1 = wb.add_sheet('Sheet 1')
gamelist = []
dk = DraftKings(league="MLB")

"""
Find all games and ids
"""
game_ids = dk.get_event_ids()
for game, event_id in game_ids.items():
    print(game, event_id)
    gamelist.append(game)

team1 = random.choice(gamelist).split("@")
sheet1.write(0,0,team1[0])
sheet1.write(1,0,team1[1])
wb.save('Bets.xls')

"""
Updates for the moneylines only
"""
dk.live_odds_stream(
    event_ids=["28335346", "28335344", "28335347"], markets=['Moneyline'])