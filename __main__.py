from rich.console import Console
from rich.markdown import Markdown
from src.build_dataset import download_data
from src.saveBreakouts import find_breakouts
from src.export import export_interactive, export_static_chart, export_csv
import yaml
import sys

config_file = open("config.yaml", "r")
config = yaml.safe_load(config_file)

welcome = """[bold]Welcome to breakoutfinder![/bold]\r
This is a little tool for helping you find breakouts from the past and view them in static or \
interactive charts and spreadsheets. This is solely educational, nothing generated by this program is financial advice. \
And there will probably some flaws in the breakout detection."""


download_data_message = """\
First, you need some stock data to look for breakouts in. Would you like to download the data from Yahoo Finance? \
It will require about 2GB of free disk space. \
"""


data_required_message = """\
Okay. This tool requires some stock data to work. Since there is none available at this point, you will now quit the program.\
"""

find_breakouts_message = """\
We are all good to go finding breakouts. Ready? It may take a long time.
"""

console = Console()
console.print(welcome, style="white")
console.print(download_data_message, style="yellow")

download_yahoo = input("Y/n: ")
if download_yahoo.lower() != "n" and download_yahoo.lower() != "no":
  with console.status("[bold green]Downloading data from Yahoo Finance...") as status:
    download_data(config['exchanges'])
else:
  console.print(data_required_message, style="red")
  sys.exit()
    
console.print(find_breakouts_message, style="yellow")
search_now = input("Y/n: ")

if search_now.lower() != "n" and search_now.lower() != "no":
  callbacks = []
  for exp in config['exports']:
    if exp == "img":
      callbacks.append(export_static_chart)
    elif exp == "interactive":
      callbacks.append(export_interactive)
    elif exp == "csv":
      callbacks.append(export_csv)
      
  find_breakouts(
    config['exchanges'],
    config,
    callbacks
    )
else:
  console.print("Okay! Then there's nothing more to do. This program will now stop.",
                style="red")