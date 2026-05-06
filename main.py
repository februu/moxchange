from moxchange import CLI, MockFeed, Simulator, EventBus, EventType

VERSION = "dev"


cli = CLI()
feed = MockFeed(amount_of_klines=500, starting_price=100.0)
bus = EventBus()

bus.subscribe(EventType.CANDLE, cli.on_candle_event)

simulator = Simulator(bus, feed)


def main():
    cli.print_banner(version=VERSION, port=8765)
    try:
        while True:
            simulator.step()
    except StopIteration:
        print("Simulation complete.")


if __name__ == "__main__":
    main()
