from dolphin_memory_engine import *
import time


# Get memory location from 32bit pointer
def read_pointer(ptr):
    return int.from_bytes(read_bytes(ptr, 4), 'big')


print("Connecting to dolphin...")
hook()
if not is_hooked():
    raise Exception("Connection failed")
print("Connected!")

RaceMgr_ptr = 0x804163A8



RaceMgr = int.from_bytes(read_bytes(RaceMgr_ptr, 4), 'big')

rankings = {}
for i in range(8):
    rankings[f"Kart {i + 1}"] = 0.0

latest_dist = 0
while True:
    # Get RaceMgr.mKartChecker[i]
    for array_index in range(0, 8):
        ptr_array_offset = array_index * 4
        mKartChecker_offset = 0x48
        kart_checker_ptr = RaceMgr + mKartChecker_offset + ptr_array_offset
        kart_checker = read_pointer(kart_checker_ptr)

        # Get kartChecker.mRaceProgression
        race_progression = read_float(kart_checker + 0x54)
        # For player 1
        if array_index == 0:
            # previous = latest_dist
            # latest_dist = race_progression
            # distance_traveled = latest_dist - previous
            # speed = distance_traveled * 1000
            # Sector index is at 0x81258ba0
            sector_index = read_word(kart_checker + 0x3c)
            getLap = read_word(kart_checker + 0x2c)
            print("Sector: " + str(sector_index) + " Lap: " + str(getLap))
        print(f"Kart {array_index + 1}: {race_progression:.3f}")
        rankings[f"Kart {array_index + 1}"] = race_progression

    print(sorted(rankings, key=rankings.get, reverse=True))
    print("----")
    time.sleep(0.5)
