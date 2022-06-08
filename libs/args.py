import os
import argparse


class game_args():
    def __init__(self):
        self.parser = argparse.ArgumentParser()

        self.parser.add_argument("--source", '-s', default='objects.pkl', type=str, help="Source file (.list or .pkl)")
        self.parser.add_argument("--pack", '-p', default=False, type=bool, help="Pack source file (true or false)")
        self.parser.add_argument("--log", '-l', default=False, type=bool, help="Log in file (true or false)")

        self.args = self.parser.parse_args()
