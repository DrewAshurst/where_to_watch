from classes import Gui
import yaml
from pathlib import Path


def main():
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    g = Gui(config)


if __name__ == '__main__':
    main()
