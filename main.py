from moxchange import CLI, MockFeed, Simulator

VERSION = "dev"

cli = CLI()
feed = MockFeed(amount_of_klines=500, starting_price=100.0)
simulator = Simulator(feed)


def main():
    cli.print_banner(version=VERSION, port=8765)
    try:
        while True:
            simulator.step()
    except StopIteration:
        print("Simulation complete.")


if __name__ == "__main__":
    main()
