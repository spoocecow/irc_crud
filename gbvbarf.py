import random
import inspect, os

_thisfile = inspect.getfile(inspect.currentframe())
cwd = os.path.dirname(os.path.abspath(_thisfile))

g_gbvfile = os.path.join(cwd, "txt", "gbv.txt")
g_preferredLength = 50

def start_quoting(lines, start_i):
    retlines = []
    chance_to_stop = 0
    loop_i = 0
    while chance_to_stop < g_preferredLength and start_i < len(lines):
        loop_i += 1
        # random chance to jump around (more likely the longer we go)
        if random.random() < 0.13 + (loop_i * 0.1):
            start_i = find_start(lines)
            loop_i = 0

        line = lines[start_i]
        if not line.strip():
            # random chance to find new stanza (less likely the longer we go)
            if random.random() < 0.75 - (loop_i * 0.1):
                start_i = find_start(lines)
                chance_to_stop += ((1 + random.random()) * 10)
                loop_i = 0
                continue
            else:
                break
        retlines.append( line.strip() )
        start_i += 1
        chance_to_stop += ((0.15 + random.random()) * len(line))
    return ' / '.join(retlines).strip()

def find_start(lines):
    bad = True
    while bad:
        i = random.randint(0, len(lines) - 1)
        line = lines[i]
        if line.strip():
            return i

def gbvbarf():
    with open(g_gbvfile) as lyrics_f:
        lines = lyrics_f.readlines()
    start_i = find_start(lines)
    return start_quoting(lines, start_i)

def main():
    text = gbvbarf()
    with open(r"C:\tmp\gbvbarf.txt", 'w+') as out:
        out.write(text)

if __name__ == "__main__":
    main()