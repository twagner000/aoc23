from pathlib import Path


def get_puzzle_input(script_path, strip=True):
    p = Path(script_path)
    with open(p.parent.parent / 'data' / p.parts[-1].replace('.py', '.txt'), 'r') as f:
        puzzle_input = f.read()
    if strip:
        return puzzle_input.strip()
    else:
        return puzzle_input
