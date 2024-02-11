from dotenv import load_dotenv

import spotify


def partition(lst, size):
    return [lst[i:i + size] for i in range(0, len(lst), size)]


if __name__ == '__main__':
    load_dotenv()
    spotify.collect_new_tracks()
