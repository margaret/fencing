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

def sort_dict_by_val(d):
    return sorted(d.items(), key=lambda x: x[1], reverse=True)
    #return sorted(d.items(), key=operator.itemgetter(1), reverse=True)

def print_ordered(d):
    # prints items sorted by value
    for key in d:
        print key
        for item in sort_dict_by_val(d[key]):
            print item
        print "\n"

def tournament_points(tournament_file, print_results=False):
    """
    {Event1:
      {school1: points1,
      school2: points2
      },
    Event2: 
      etc
    }
    """
    with open(tournament_file, 'rU') as f:
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

    if print_results:
        print_ordered(standings_by_event)

    return standings_by_event


def aggregate_points(tournament_results):
    """
    tournament_results is a list of filenames for tournaments to aggregate
    prints schools and scores by total points from all tournaments
    """
    # each of these is a dict of events to dicts of points by school
    # {Mixed Foil: {SLO: 3, Cal: 42}}
    results = [tournament_points(tournament) for tournament in tournament_results]

    # get list of all events in case events differ between tournaments
    # shouldn't be the case for ncifl but whatever.
    events = set()
    for result in results:
        for event in result.keys():
            events.add(event)

    all_results = dict(zip(events, [{} for i in xrange(len(events))]))
    for result in results:
        for event in result:
            # combine with the results from this tournament
            for school in result[event]:
                try:
                    all_results[event][school] += result[event][school]
                except KeyError:
                    all_results[event][school] = result[event][school]

    print_ordered(all_results)

    totals = {}
    for event in all_results:
        for school in all_results[event]:
            try:
                totals[school] += all_results[event][school]
            except KeyError:
                totals[school] = all_results[event][school]

    rank = 1
    for score in sort_dict_by_val(totals):
        print rank, score
        rank += 1
                

if __name__ == '__main__':
    print "Cal Poly 2014\n"
    aggregate_points(['2014/CalPoly.csv'])

    print 

    aggregate_points(['2014/Berkeley.csv', '2014/CalPoly.csv'])
