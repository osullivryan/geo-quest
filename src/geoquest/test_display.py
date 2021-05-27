from .display import QuestDisplay


def test_single_quest_display():
    display = QuestDisplay()

    display.draw_quest(1, 3)
    display.draw_attempts(1, 10)
    display.draw_distance(500.0)
