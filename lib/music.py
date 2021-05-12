from multiprocessing.dummy import Pool

import pygame


def pygame_volume(volume):
    """Convert the given volume to one that can be fed to pygame.mixer's set_volume() method."""
    volume *= 0.0001    # Adjusting from percentage²
    if 0.0005 < volume < 0.0078125:
        volume = 0.0078125  # pygame's min volume. This stops it going silent when volume is low but not muted.
    return volume


class Audio:
    """Class for representing and containing an audio clip."""

    def __init__(self, file_name, volume_multiplier=1.0, *, load_async=True):
        self.path = f"../audio/{file_name}"
        if load_async:
            self.sound_pool = Pool(processes=1).apply_async(pygame.mixer.Sound, [self.path])
            self._sound = None
        else:
            self._sound = pygame.mixer.Sound(self.path)
        self.volume_multiplier = volume_multiplier  # Used for adjusting tracks that are naturally too loud/quiet

    @property
    def sound(self):
        if self._sound is None:
            self._sound = self.sound_pool.get(10)
        return self._sound

    @property
    def is_loaded(self):
        return self.sound_pool.ready()

    def play(self, channel, *, loop: bool, fade: bool):
        """Play the audio clip. Loops indefinitely if loop is True. Fades in if fade is True."""
        channel.play(self.sound, -1 if loop else 0, fade_ms=1000 if fade else 0)

    def set_volume(self, volume):
        """Set the volume of the audio clip."""
        self.sound.set_volume(pygame_volume(volume * self.volume_multiplier))


class Music:
    """Class for controlling audio playback in the game."""

    def __init__(self):
        self.is_muted = False
        self.master_volume = 100
        self.music = AudioType(self, stops=True, loops=True, fades=True)
        self.sound = AudioType(self)
        self.voice = AudioType(self)

    def stop(self):
        """Stop all currently playing audio."""
        self.music.stop()
        self.sound.stop()
        self.voice.stop()

    def mute(self):
        """Mute all game audio."""
        self.music.mute()
        self.sound.mute()
        self.voice.mute()
        self.is_muted = True

    def unmute(self):
        """Unmute all game audio (if it was muted)."""
        self.music.unmute()
        self.sound.unmute()
        self.voice.unmute()
        self.is_muted = False

    def toggle_mute(self):
        """Enable mute if it's off, disable it if it's on."""
        if self.is_muted:
            self.unmute()
        else:
            self.mute()


class AudioType:
    """Class representing a type of audio - music, sfx, voice, etc.

    The `stops` parameter decides whether or not previously playing audio is stopped when playing a new one.
    The `loops` parameter decides whether or not the audio loops by default.
    The `fades` parameter decides whether or not new audio fades in by default.
    """

    def __init__(self, music, stops=False, loops=False, fades=False):
        self.music = music
        self.stored_volume = None

        self.currently_playing = {}
        self.volume = 100

        self.stops = stops
        self.loops = loops
        self.fades = fades

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value):
        self._volume = value
        for audio in self.currently_playing.values():
            audio.set_volume(self.music.master_volume * value)

    @property
    def is_muted(self):
        return self.volume == 0

    @property
    def is_playing(self):
        return any((channel.get_busy() for channel in self.currently_playing.keys()))

    def play(self, audio: Audio, *, loop=None, fade=None):
        """Play the given song on loop. Mainly for BGM purposes."""
        loop = self.loops if loop is None else loop
        fade = self.fades if fade is None else fade
        if self.stops:
            self.stop()
        audio.set_volume(self.music.master_volume * self.volume)
        channel = pygame.mixer.find_channel()
        audio.play(channel, loop=loop, fade=fade)
        self.currently_playing[channel] = audio

    def stop(self):
        """Stop the currently playing audio."""
        for channel in self.currently_playing.copy():
            self.currently_playing.pop(channel).sound.stop()

    def pause(self):
        """Pause the currently playing audio."""
        for channel in self.currently_playing.keys():
            channel.pause()

    def unpause(self):
        """Unpause the currently paused audio."""
        for channel in self.currently_playing.keys():
            channel.unpause()

    def mute(self):
        """Mute this audio type."""
        self.stored_volume = self.volume
        self.volume = 0

    def unmute(self):
        """Unmute this audio type."""
        if self.stored_volume is None:
            raise ValueError("No stored_volume found - unmute() should not have been called.")
        self.volume = self.stored_volume
        self.stored_volume = None

    def toggle_mute(self):
        """Mute this audio type if it's unmuted, unmute it if it's muted."""
        if self.is_muted:
            self.unmute()
        else:
            self.mute()
