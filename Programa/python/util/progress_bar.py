import sys
import os

def progress_bar(i,label="concluido"):
    label = f"{i}% {label} : "
    bar_size = _get_bar_size(label)
    filled_blocks = _get_filled_blocks(i, bar_size)
    empty_blocks = _get_empty_blocks(filled_blocks, bar_size)
    bar = "█" * filled_blocks + "░" * empty_blocks
    sys.stdout.write(f"\r{label}{bar}")
    sys.stdout.flush()

def _get_bar_size(label):
    terminal_size = os.get_terminal_size()
    return terminal_size.columns - len(label) - 2 # 2 extra characters for the brackets

def _get_filled_blocks(i, bar_size):
    return round(i / 100 * bar_size)

def _get_empty_blocks(filled_blocks, bar_size):
    return bar_size - filled_blocks
