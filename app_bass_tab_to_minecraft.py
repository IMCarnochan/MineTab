
import streamlit as st
from midiutil import MIDIFile
import tempfile
import os

from bass_tab_to_minecraft import parse_full_fret_tab, export_to_json, export_to_minecraft_commands

st.title("🎸 Bass Tab to Minecraft Converter")

tab_input = st.text_area("Paste your 4-string bass tab below:", height=300)

if st.button("Convert"):
    if not tab_input.strip():
        st.warning("Please paste some tablature first.")
    else:
        events = parse_full_fret_tab(tab_input)
        st.success(f"Parsed {len(events)} playable notes.")

        st.subheader("🎵 Playback (MIDI)")
        midi = MIDIFile(1)
        track = 0
        midi.addTrackName(track, 0, "Bass Line")
        midi.addTempo(track, 0, 100)

        for event in events:
            pitch = 40 + event["pitch"]  # MIDI note number
            time = event["tick"] * 0.25  # quarter notes
            midi.addNote(track, 0, pitch, time, 1, 100)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mid") as tmp:
            midi.writeFile(tmp)
            st.audio(tmp.name, format="audio/midi")

        st.subheader("🗂️ Export Options")
        st.download_button("Download JSON", export_to_json(events), file_name="bass_tab.json")
        st.download_button("Download Minecraft Commands", export_to_minecraft_commands(events), file_name="minecraft_commands.txt")
