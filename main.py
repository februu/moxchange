from moxchange import CLI, EventBus, MockFeed, Simulator
from moxchange.events import KlineEvent
from moxchange.services import AccountService

DEBUG = True
VERSION = "dev"

bus = EventBus()

cli = CLI()

feed = MockFeed(symbol="BTCUSD", amount_of_klines=500, starting_price=100.0)

account_service = AccountService(bus)

simulator = Simulator(bus, feed, account_service)

if DEBUG:
    bus.subscribe(KlineEvent, cli.on_candle_event)

def main():
    cli.print_banner(version=VERSION, port=8765)
    try:
        while True:
            simulator.step()
    except StopIteration:
        print("Simulation complete.")


if __name__ == "__main__":
    main()
