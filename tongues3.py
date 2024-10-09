import argparse
import json

from TongueDrawer import TongueDrawer


arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('config_file')
parsed_args = arg_parser.parse_args()

config_file_path = parsed_args.config_file
with open(config_file_path, 'r') as config_file:
    config = json.load(config_file)

tongue_drawer = TongueDrawer(config['family'],
                             options_domain=config['domain'],
                             options_dynamics=config['dynamics'],
                             options_image=config['images'],
                             options_other=config['misc'])

tongue_drawer.draw_the_tongues()







































