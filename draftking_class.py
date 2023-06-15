import asyncio
import requests
from draftkings_stream import stream

id_dict = {"NFL": "88808", "MLB": "84240"}


class DraftKings:
    def __init__(self, league="MLB"):
        self.league = league
        self.pregame_url = f"https://sportsbook.draftkings.com//sites/US-SB/api/v5/eventgroups/{id_dict[self.league]}?format=json"
        self.uri = "wss://ws-draftkingseu.pusher.com/app/490c3809b82ef97880f2?protocol=7&client=js&version=7.3.0&flash=false"

    def get_event_ids(self) -> dict:
        event_ids = {}
        response = requests.get(self.pregame_url).json()
        for event in response['eventGroup']['events']:
            event_ids[event['name']] = event['eventId']
        return event_ids

    def get_pregame_odds(self) -> list:
        # List that will contain dicts [one for each game]
        games_list = []

        # Requests the content from DK's API, loops through the different games & collects all the material deemed relevant
        response = requests.get(self.pregame_url).json()
        games = response['eventGroup']['offerCategories'][0]['offerSubcategoryDescriptors'][0]['offerSubcategory']['offers']
        for game in games:
            # List that will contain dicts [one for each market]
            market_list = []
            for market in game:
                try:
                    market_name = market['label']
                    if market_name == "Moneyline":
                        home_team = market['outcomes'][1]['label']
                        away_team = market['outcomes'][0]['label']
                    # List that will contain dicts [one for each outcome]
                    outcome_list = []
                    for outcome in market['outcomes']:
                        try:
                            # if there's a line it should be included in the outcome description
                            line = outcome['line']
                            outcome_label = outcome['label'] + " " + str(line)
                        except:
                            outcome_label = outcome['label']
                        outcome_odds = outcome['oddsDecimal']
                        outcome_list.append(
                            {"label": outcome_label, "odds": outcome_odds})
                    market_list.append(
                        {"marketName": market_name, "outcomes": outcome_list})
                except Exception as e:
                        print()
                        continue
            games_list.append(
                {"game": f"{home_team} v {away_team}", "markets": market_list})

        return games_list

    def live_odds_stream(self, event_ids=None, markets=None):
        asyncio.run(stream(
            uri=self.uri, league_id=id_dict[self.league], event_ids=event_ids, markets=markets))
