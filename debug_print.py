import sys

class Debug:
    enabled = 0

    @staticmethod
    def print(message):
        if Debug.enabled is 0:
            return
        print(message, file=sys.stderr)
