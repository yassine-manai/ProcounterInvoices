import time
import sys
from colorama import init, Fore

# Initialize colorama
init()

colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE]

def animate(delay=0.1, duration=7, bar_length=150):
    """
    Displays an animated progress bar in the console with changing colors.

    The progress bar fills up over the specified duration and cycles through
    different colors.

    Parameters:
        delay (float): The delay in seconds between updates to the progress bar.
        duration (float): The total duration in seconds for the progress bar to fill.
        bar_length (int): The length of the progress bar.

    Returns:
        None
    """
    
    end_time = time.time() + duration
    while time.time() <= end_time:
        for color in colors:
            progress = (time.time() + delay - (end_time - duration)) / duration
            filled_length = int(bar_length * progress)
            bar = color + '█' * filled_length + Fore.RESET + '-' * (bar_length - filled_length)
            sys.stdout.write(f'\r|{bar}|')
            sys.stdout.flush()
            time.sleep(delay)
    sys.stdout.write(f'\r|{"█" * bar_length}  | Done! \n')



  