import websockets
import json
from traceback import print_exc


async def stream(uri: str, league_id: str, event_ids: list, markets: list):
    try:
        # connects to the web server
        ws = await websockets.connect(uri)

        # sends a subscription message to the server with info regarding the odds data we want to receive updates on
        await ws.send(
            json.dumps({"event": "pusher:subscribe", "data": {"auth": "", "channel": f"nj_ent-eventgroupv2-{league_id}"}}
                       )
        )

        while True:
            try:
                new_message = await ws.recv()
                message_json = json.loads(new_message)

                event = message_json['event']
                if not event == "offer-updated":
                    if event == 'pusher:connection_established':
                        print("Connection established!")
                        continue
                    elif event == 'pusher_internal:subscription_succeeded':
                        print("Subscription succeeded, awaits new odds updates...")
                        continue
                    else:
                        continue

                content = json.loads(message_json['data'])
                event_id = content['data'][0]['eventId']
                if event_ids:
                    # if a list of event_ids is provided, this checks whether
                    # the update is relevant or not
                    if not event_id in event_ids:
                        continue

                market = content['data'][0]['label']
                if markets:
                    # if a list of wanted markets is provided, this checks whether
                    # the update is relevant or not
                    if not market in markets:
                        continue

                # if the WS event type is correct [offer-updated], the event_id is
                # for one of the games of interest & finally the market is included in the list of
                # wanted markets, then the below section is executed
                outcomes = content['data'][0]['outcomes']
                print(f"New odds update for '{market}'")
                for outcome in outcomes:
                    print("Line:", outcome['line'])
                    print("Outcome:", outcome['label'])
                    print("Price:", outcome['oddsDecimal'])
                    if not outcome == outcomes[-1]:
                        print()
                print("Awaits more updates...")
                print()

            except websockets.WebSocketException:
                print_exc()
                break

            except Exception:
                print_exc()

        await ws.close()

    except:
        print_exc()