"""Module containing classes for processing and playing of pygame audio clips."""
from multiprocessing.dummy import Pool

import pygame


PYGAME_MIN_VOLUME = 0.0078125


def pygame_volume(volume):
    """Convert the given volume to one that can be fed to pygame.mixer's set_volume() method."""
    volume *= 0.0001    # Adjusting from percentage²
    if 0.0005 < volume < PYGAME_MIN_VOLUME:
        volume = PYGAME_MIN_VOLUME  # This stops it going silent when volume is low but not muted.
    return volume


class AudioClip:
    """Class for representing and containing an audio clip."""

    _BASE_PATH = "../audio/"

    def __init__(self, file_name, volume_multiplier=1.0, *, load_async=True):
        """Create an AudioClip instance.

        file_name: the relative path to the audio file from AudioClip._BASE_PATH.
        volume_multiplier: adjust the base volume of this clip if it is naturally too loud.
        load_async: whether to load the clip asynchronously.
        """
        self.path = self._BASE_PATH + file_name
        if load_async:
            self.sound_pool = Pool(processes=1).apply_async(pygame.mixer.Sound, [self.path])
            self._sound = None
        else:
            self._sound = pygame.mixer.Sound(self.path)
        self.volume_multiplier = volume_multiplier

    @property
    def sound(self):
        """Get the pygame.mixer.Sound object for this audio clip."""
        if self._sound is None:
            self._sound = self.sound_pool.get(10)
        return self._sound

    @property
    def is_loaded(self):
        """Get whether the pygame.mixer.Sound object for this audio clip has finished loading."""
        return self.sound_pool.ready()

    def play(self, channel, *, loop: bool, fade: bool):
        """Play the audio clip in the given channel.

        loop: whether or not to loop the audio clip indefinitely.
        fade: whether or not to fade the audio clip in.
        """
        channel.play(self.sound, -1 if loop else 0, fade_ms=1000 if fade else 0)

    def set_volume(self, volume):
        """Set the volume of the audio clip."""
        self.sound.set_volume(pygame_volume(volume * self.volume_multiplier))


class AudioController:
    """Class for controlling audio playback in the game."""

    def __init__(self):
        """Create an AudioController instance."""
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
    """Class representing a type of audio - music, sfx, voice, etc."""

    def __init__(self, music, stops=False, loops=False, fades=False):
        """Create an AudioType instance.

        The `stops` parameter decides whether or not previously
        playing audio is stopped when a new one is played.
        The `loops` parameter decides whether or not the audio loops by default.
        The `fades` parameter decides whether or not new audio fades in by default.
        """
        self._music = music
        self._stored_volume = None

        self._currently_playing = {}
        self.volume = 100

        self._stops = stops
        self._loops = loops
        self._fades = fades

    @property
    def volume(self):
        """Get the current volume of this audio type."""
        return self._volume

    @volume.setter
    def volume(self, value):
        """Set the current volume of this audio type."""
        self._volume = value
        for audio in self.currently_playing.values():
            audio.set_volume(self._music.master_volume * value)

    @property
    def currently_playing(self):
        """Get a dictionary of {channel: audio} pairs.

        The channels show channels that are currently playing clips of this audio type.
        Their corresponding audios show which audio clip they are playing.
        """
        for channel, audio in self._currently_playing.copy().items():
            if channel.get_sound() is not audio.sound:
                self._currently_playing.pop(channel)
        return self._currently_playing

    @property
    def is_muted(self):
        """Return whether or not this audio type is muted."""
        return self.volume == 0

    @property
    def is_playing(self):
        """Get whether or not any clips of this audio type are currently playing."""
        return bool(self.currently_playing)

    def play(self, audio: AudioClip, *, loop=None, fade=None):
        """Play the given song on loop. Mainly for BGM purposes."""
        loop = self._loops if loop is None else loop
        fade = self._fades if fade is None else fade
        if self._stops:
            self.stop()
        audio.set_volume(self._music.master_volume * self.volume)
        channel = pygame.mixer.find_channel()
        audio.play(channel, loop=loop, fade=fade)
        self.currently_playing[channel] = audio

    def stop(self):
        """Stop the currently playing audio."""
        for channel in self.currently_playing.copy():
            self.currently_playing.pop(channel).sound.stop()

    def pause(self):
        """Pause the currently playing audio."""
        for channel in self.currently_playing:
            channel.pause()

    def unpause(self):
        """Unpause the currently paused audio."""
        for channel in self.currently_playing:
            channel.unpause()

    def mute(self):
        """Mute this audio type."""
        self._stored_volume = self.volume
        self.volume = 0

    def unmute(self):
        """Unmute this audio type."""
        if self._stored_volume is None:
            raise ValueError("No stored volume found - unmute() should not have been called.")
        self.volume = self._stored_volume
        self._stored_volume = None

    def toggle_mute(self):
        """Mute this audio type if it's unmuted, unmute it if it's muted."""
        if self.is_muted:
            self.unmute()
        else:
            self.mute()
