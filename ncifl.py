from collections import defaultdict
import csv

def get_points(place, num_fencers=1, novice=False):
    # attendance point
    total = 1
    if not novice:
        # medal points
        total += max(0, 4 - place)
        # 4th is actually tie for third
        if place == 4:
            total += 1
        # interval points
        total += 5
        interval = round(num_fencers / 10.0)
        intervals = 5
    else:
        # interval points
        total += 3
        interval = round(round(num_fencers / 2.0) / 3)
        intervals = 3
    for i in xrange(intervals):
        if place <= interval * (i + 1):
            break
        total -= 1
    return total

if __name__ == '__main__':
    with open('2014/Berkeley.csv', 'rU') as f:
        results = [row for row in csv.DictReader(f)]
    num_fencers_by_event = defaultdict(int)
    for result in results:
        num_fencers_by_event[result['event']] += 1
    num_fencers_by_event = dict(num_fencers_by_event)
    standings = defaultdict(int)
    standings_by_event = defaultdict(dict)
    for result in results:
        points = get_points(int(result['place']),
                            int(num_fencers_by_event[result['event']]),
                            "novice" in result['event'].lower())
        standings[result['club']] += points
        if result['club'] in standings_by_event[result['event']]:
            standings_by_event[result['event']][result['club']] += points
        else:
            standings_by_event[result['event']][result['club']] = points
    standings = dict(standings)
    standings_by_event = dict(standings_by_event)
    