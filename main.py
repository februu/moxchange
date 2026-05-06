from moxchange import CLI, CSVFeed, Simulator

VERSION = "dev"

cli = CLI()
feed = CSVFeed("data.csv")
simulator = Simulator(feed)


def main():
    cli.print_banner(version=VERSION, port=8765)
    simulator.step()


if __name__ == "__main__":
    main()
