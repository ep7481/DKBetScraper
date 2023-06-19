import random
import mysql.connector
from mysql.connector import Error
from draftking_class import DraftKings

gamelist = []
dk = DraftKings(league="MLB")

"""
Find all games and ids
"""
game_ids = dk.get_event_ids()
for game, event_id in game_ids.items():
    print(game, event_id)
    gamelist.append(game)

try:
    connection = mysql.connector.connect(
        host='localhost',
        database='bets_db',
        user='root',
        password=''
    )

    if connection.is_connected():
        print('Connected to MySQL database')
except Error as e:
    print('Error while connecting to MySQL', e)

cursor = connection.cursor()

delete_query = "DELETE FROM bets"
cursor.execute(delete_query)
print("Previous data deleted successfully")

team1 = random.choice(gamelist).split("@")
team2 = team1[0]
team3 = team1[1]


query = "INSERT INTO bets (Teamone, Teamtwo) VALUES (%s, %s)"

data = (team2, team3)
cursor.execute(query, data)


connection.commit()

cursor.close()
connection.close()
"""
Updates for the moneylines only
"""
dk.live_odds_stream(
    event_ids=["28335346", "28335344", "28335347"], markets=['Moneyline'])

