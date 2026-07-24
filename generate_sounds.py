import wave
import struct
import math
import os
import random

SAMPLE_RATE = 22050  # 22.05 kHz for authentic retro lo-fi sound and small size

def write_wav(filename, samples):
    # Ensure parent directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with wave.open(filename, 'w') as w:
        w.setnchannels(1)  # Mono
        w.setsampwidth(2)  # 16-bit PCM (2 bytes)
        w.setframerate(SAMPLE_RATE)
        # Convert float samples (-1.0 to 1.0) to 16-bit signed integers (-32767 to 32767)
        for s in samples:
            val = int(max(-1.0, min(1.0, s)) * 32767)
            w.writeframesraw(struct.pack('<h', val))
    print(f"Generated audio: {filename} ({len(samples)} samples)")

# ----------------------------------------------------
# SOUND EFFECTS (SFX) GENERATORS
# ----------------------------------------------------

def generate_laser_player():
    # Downward frequency sweep from 900 Hz to 200 Hz
    duration = 0.15
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        # Linear sweep equation
        # f(t) = 900 - 700 * (t / 0.15)
        # Phase is integral of 2*pi*f(t) dt = 2*pi * (900*t - 350*t^2/0.15)
        phase = 2.0 * math.pi * (900.0 * t - (350.0 * t * t) / duration)
        
        # Square wave for retro chiptune flavor
        val = 0.25 if math.sin(phase) > 0 else -0.25
        
        # Linear fade envelope
        envelope = 1.0 - (t / duration)
        samples.append(val * envelope)
        
    return samples

def generate_laser_enemy():
    # Slightly longer, deeper frequency sweep from 500 Hz to 100 Hz
    duration = 0.25
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        # f(t) = 500 - 400 * (t / 0.25)
        # Phase = 2*pi * (500*t - 200*t^2/0.25)
        phase = 2.0 * math.pi * (500.0 * t - (200.0 * t * t) / duration)
        
        # Square wave
        val = 0.25 if math.sin(phase) > 0 else -0.25
        
        # Fade envelope
        envelope = 1.0 - (t / duration)
        samples.append(val * envelope)
        
    return samples

def generate_explosion():
    # White noise with low-frequency rumble and rapid decay
    duration = 0.50
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    
    current_noise = 0.0
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        # Sample-and-hold noise every 6 samples to make it sound "crunchy" and 8-bit
        if i % 6 == 0:
            current_noise = random.uniform(-0.4, 0.4)
            
        # Low frequency rumble (sine wave)
        rumble = 0.2 * math.sin(2.0 * math.pi * 80.0 * t)
        
        # Combine noise and rumble
        val = current_noise + rumble
        
        # Exponential-like decay envelope: (1 - t/duration)^2
        envelope = (1.0 - (t / duration)) ** 2
        samples.append(val * envelope)
        
    return samples

def generate_powerup():
    # Classic retro rising arpeggio (quick musical notes)
    duration = 0.3
    num_samples = int(duration * SAMPLE_RATE)
    samples = []
    
    # 3 stepped pitches: C5, E5, G5, C6
    notes_dur = duration / 4
    for i in range(num_samples):
        t = i / SAMPLE_RATE
        # Determine which note to play
        note_index = int(t / notes_dur)
        if note_index == 0:
            freq = 523.25  # C5
        elif note_index == 1:
            freq = 659.25  # E5
        elif note_index == 2:
            freq = 783.99  # G5
        else:
            freq = 1046.50 # C6
            
        phase = 2.0 * math.pi * freq * t
        
        # Triangle wave for a softer, sweet powerup chime
        # Triangle is: 2 * abs(2 * (t * freq - floor(t * freq + 0.5))) - 1
        val = 2.0 * abs(2.0 * (t * freq - math.floor(t * freq + 0.5))) - 1.0
        val *= 0.3  # volume scaling
        
        # Fade envelope at the very end
        envelope = 1.0 if t < 0.2 else (1.0 - (t - 0.2) / 0.1)
        samples.append(val * envelope)
        
    return samples

# ----------------------------------------------------
# MUSIC SEQUENCER SYSTEM
# ----------------------------------------------------

def get_freq(note_name):
    notes = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4, 'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}
    if note_name == ' ':
        return 0.0
    name = note_name[:-1]
    octave = int(note_name[-1])
    semitones = notes[name] + (octave - 4) * 12
    return 440.0 * (2.0 ** (semitones / 12.0))

def generate_music_loop(melody, bass, note_duration):
    # Generates a mix of a square wave melody and triangle wave bass
    samples = []
    num_notes = max(len(melody), len(bass))
    samples_per_note = int(note_duration * SAMPLE_RATE)
    
    # Track phase across note boundaries to prevent audio glitches/clicks
    m_phase = 0.0
    b_phase = 0.0
    
    for i in range(num_notes):
        m_note = melody[i % len(melody)] if melody else ' '
        b_note = bass[i % len(bass)] if bass else ' '
        
        m_freq = get_freq(m_note)
        b_freq = get_freq(b_note)
        
        for s in range(samples_per_note):
            # 1. Melody - Square Wave (25% duty cycle for authentic 8-bit sound)
            if m_freq > 0:
                m_phase += (2.0 * math.pi * m_freq) / SAMPLE_RATE
                if m_phase > 2.0 * math.pi:
                    m_phase -= 2.0 * math.pi
                # 25% duty cycle square wave
                m_val = 0.15 if (m_phase < 0.5 * math.pi) else -0.15
            else:
                m_val = 0.0
                
            # 2. Bass - Triangle Wave
            if b_freq > 0:
                b_phase += (2.0 * math.pi * b_freq) / SAMPLE_RATE
                if b_phase > 2.0 * math.pi:
                    b_phase -= 2.0 * math.pi
                # Triangle wave formula
                norm = b_phase / (2.0 * math.pi)
                if norm < 0.5:
                    b_val = -0.25 + 1.0 * norm
                else:
                    b_val = 0.25 - 1.0 * (norm - 0.5)
            else:
                b_val = 0.0
                
            # Mix voices
            mixed = m_val + b_val
            
            # Note envelope to prevent hard click pops at the note changes
            note_t = s / samples_per_note
            env = 1.0
            if note_t < 0.08:
                env = note_t / 0.08  # Attack
            elif note_t > 0.85:
                env = (1.0 - note_t) / 0.15  # Release
                
            samples.append(mixed * env)
            
    return samples

# ----------------------------------------------------
# MAIN GENERATION PIPELINE
# ----------------------------------------------------

def main():
    print("Starting Programmatic 8-bit Retro Audio Generator...")
    
    # 1. Generate SFX
    laser_p = generate_laser_player()
    laser_e = generate_laser_enemy()
    explosion = generate_explosion()
    p_up = generate_powerup()
    
    # 2. Generate Music Loops
    # Intro Theme: slow, atmospheric sci-fi arpeggio
    intro_melody = ['C4', 'E4', 'G4', 'B4', 'C5', 'B4', 'G4', 'E4', 'A4', 'C5', 'E5', 'G5', 'A5', 'G5', 'E5', 'C5']
    intro_bass = ['C3', 'C3', 'C3', 'C3', 'G3', 'G3', 'G3', 'G3', 'A3', 'A3', 'A3', 'A3', 'F3', 'F3', 'F3', 'F3']
    intro_theme = generate_music_loop(intro_melody, intro_bass, 0.35)
    
    # Game Phase 1: upbeat, heroic retro theme
    game_melody = ['E4', 'G4', 'A4', 'B4', 'A4', 'B4', 'C5', 'D5', 'E5', 'D5', 'C5', 'B4', 'A4', 'G4', 'F4', 'D4']
    game_bass = ['E3', 'E3', 'G3', 'G3', 'A3', 'A3', 'B3', 'B3', 'C3', 'C3', 'A3', 'A3', 'F3', 'F3', 'D3', 'D3']
    game_theme = generate_music_loop(game_melody, game_bass, 0.25)
    
    # Game Phase 2: mysterious minor key theme
    p2_melody = ['A4', 'C5', 'E5', 'D5', 'E5', 'G5', 'A5', 'G5', 'F5', 'E5', 'D5', 'C5', 'B4', 'G4', 'A4', ' ']
    p2_bass = ['A3', 'E3', 'A3', 'C3', 'D3', 'A3', 'D3', 'F3', 'C3', 'G3', 'C3', 'E3', 'E3', 'B2', 'A3', 'E3']
    phase2_theme = generate_music_loop(p2_melody, p2_bass, 0.22)
    
    # Game Phase 3: cosmic, high-pitched rapid theme
    p3_melody = ['B4', 'D5', 'F#5', 'E5', 'F#5', 'A5', 'B5', 'A5', 'G5', 'F#5', 'E5', 'D5', 'C#5', 'A4', 'B4', ' ']
    p3_bass = ['B3', 'F#3', 'B3', 'D3', 'E3', 'B3', 'E3', 'G3', 'D3', 'A3', 'D3', 'F#3', 'F#3', 'C#3', 'B3', 'F#3']
    phase3_theme = generate_music_loop(p3_melody, p3_bass, 0.20)
    
    # Boss Theme: fast, dramatic chromatic steps
    boss_melody = ['C4', 'C#4', 'D4', 'D#4', 'E4', 'D#4', 'D4', 'C#4', 'C4', 'C#4', 'D4', 'D#4', 'E4', 'D#4', 'D4', 'C#4']
    boss_bass = ['C3', 'C3', 'C3', 'C3', 'C#3', 'C#3', 'C#3', 'C#3', 'D3', 'D3', 'D3', 'D3', 'D#3', 'D#3', 'D#3', 'D#3']
    boss_theme = generate_music_loop(boss_melody, boss_bass, 0.18)
    
    # 3. Save files to all necessary locations
    # Paths lists for copies
    destinations = [
        "c:\\Users\\dbofe\\OneDrive\\Documentos\\star blaster 26\\Star-Blaster",  # root
        "c:\\Users\\dbofe\\OneDrive\\Documentos\\star blaster 26\\Star-Blaster\\star-blaster-wasm" # wasm folder
    ]
    
    for path in destinations:
        # Save SFX
        write_wav(os.path.join(path, "explode.wav"), explosion)
        write_wav(os.path.join(path, "sounds", "laser_player.wav"), laser_p)
        write_wav(os.path.join(path, "sounds", "laser_enemy.wav"), laser_e)
        write_wav(os.path.join(path, "sounds", "powerup.wav"), p_up)
        
        # Save BGM
        write_wav(os.path.join(path, "sounds", "intro.wav"), intro_theme)
        write_wav(os.path.join(path, "sounds", "game.wav"), game_theme)
        write_wav(os.path.join(path, "sounds", "phase2.wav"), phase2_theme)
        write_wav(os.path.join(path, "sounds", "phase3.wav"), phase3_theme)
        write_wav(os.path.join(path, "sounds", "boss.wav"), boss_theme)

    print("Audio assets generated successfully!")

if __name__ == '__main__':
    main()
