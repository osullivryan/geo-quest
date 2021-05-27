from .quest import Quest, start_quests


def test_single_quest():
    q = Quest('test', 0, 0, 10, "got it!")

    print(q.distance_to(10, 10))

    pass


def test_two_quests():
    q1 = Quest('test', 0, 0, 1000000, 10, "got it 1!")
    q2 = Quest('test', 0, 0, 10, 10, "got it 2!")

    start_quests([q1, q2])