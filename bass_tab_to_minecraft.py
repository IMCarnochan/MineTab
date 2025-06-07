NOTE_BLOCKS = {
    'E': 4,   # Low E string = Minecraft pitch 4
    'A': 9,
    'D': 14,
    'G': 19
}

def fret_to_minecraft_pitch(string_note, fret):
    base = NOTE_BLOCKS.get(string_note.upper(), None)
    if base is None:
        return None
    pitch = base + fret
    return pitch if 0 <= pitch <= 24 else None

def parse_full_fret_tab(tab_text):
    lines = [line.strip() for line in tab_text.splitlines() if "|" in line]
    tab_strings = {'G': "", 'D': "", 'A': "", 'E': ""}

    for line in lines:
        string = line[0].upper()
        if string in tab_strings:
            parts = line[2:].split('|')
            tab_line = ''.join(parts)
            tab_strings[string] = tab_line

    max_len = max(len(line) for line in tab_strings.values())
    midi_events = []

    i = 0
    while i < max_len:
        for string in 'GDAE':
            line = tab_strings[string]
            if i >= len(line):
                continue
            char = line[i]
            if char.isdigit():
                fret_str = char
                if i + 1 < len(line) and line[i + 1].isdigit():
                    fret_str += line[i + 1]
                    i += 1
                fret = int(fret_str)
                pitch = fret_to_minecraft_pitch(string, fret)
                if pitch is not None:
                    midi_events.append({
                        "tick": i,
                        "string": string,
                        "fret": fret,
                        "pitch": pitch
                    })
        i += 1

    return midi_events

def export_to_json(events):
    import json
    return json.dumps(events, indent=2)

def export_to_minecraft_commands(events, sound="block.note_block.pling"):
    commands = []
    for event in events:
        pitch = event["pitch"]
        pitch_ratio = round(2 ** ((pitch - 12) / 12), 3)
        command = f'/playsound {sound} master @a ~ ~ ~ {pitch_ratio} 1'
        commands.append(command)
    return "\n".join(commands)