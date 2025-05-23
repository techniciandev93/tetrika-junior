from datetime import datetime


def get_time_presence(intervals):
    datetime_intervals = []
    for index in range(0, len(intervals), 2):
        datetime_intervals.append(
            [
                datetime.utcfromtimestamp(intervals[index]),
                datetime.utcfromtimestamp(intervals[index + 1]),
            ]
        )
    return datetime_intervals


def merge_intervals(intervals):
    if not intervals:
        return []
    intervals.sort()
    merged = [intervals[0]]
    for current_start, current_end in intervals[1:]:
        last_start, last_end = merged[-1]
        if current_start <= last_end:
            merged[-1] = (last_start, max(last_end, current_end))
        else:
            merged.append((current_start, current_end))
    return merged


def appearance(intervals: dict[str, list[int]]) -> int:
    intersections = []
    pupil_time_presence = get_time_presence(intervals['pupil'])
    tutor_time_presence = get_time_presence(intervals['tutor'])
    lesson_time_presence_start, lesson_time_presence_end = get_time_presence(intervals['lesson'])[0]
    for pupil_time_start, pupil_time_end in pupil_time_presence:
        for tutor_time_start, tutor_time_end in tutor_time_presence:
            intersection_start = max(pupil_time_start, tutor_time_start, lesson_time_presence_start)
            intersection_end = min(pupil_time_end, tutor_time_end, lesson_time_presence_end)
            if intersection_start < intersection_end:
                intersections.append((intersection_start, intersection_end))
    merged = merge_intervals(intersections)
    return sum(int((end - start).total_seconds()) for start, end in merged)


if __name__ == '__main__':
    tests = [
        {'intervals': {'lesson': [1594663200, 1594666800],
                       'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
                       'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
         'answer': 3117
         },
        {'intervals': {'lesson': [1594702800, 1594706400],
                       'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564,
                                 1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096,
                                 1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500,
                                 1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
                       'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
         'answer': 3577
         },
        {'intervals': {'lesson': [1594692000, 1594695600],
                       'pupil': [1594692033, 1594696347],
                       'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
         'answer': 3565
         },
    ]
    for i, test in enumerate(tests):
        test_answer = appearance(test['intervals'])
        assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
