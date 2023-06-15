from draftking_class import DraftKings

dk = DraftKings(league="MLB")

"""
Find all games and ids
"""
game_ids = dk.get_event_ids()
for game, event_id in game_ids.items():
    print(game, event_id)

"""
Updates for the moneylines only
"""
dk.live_odds_stream(
    event_ids=["28335346", "28335344", "28335347"], markets=['Moneyline'])