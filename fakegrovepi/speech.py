# fake speech module 

def say(words):
    """ Say these words as text-to-speech

    They will be spoken on the loudspeaker of your device (or whatever audio output you
    have connected.)

    This is useful for things like making yourself aware of sensor event detections.
    """
    print("Saying:",words)