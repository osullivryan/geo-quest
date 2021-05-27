from .display import QuestDisplay
from .get_location import get_current_lat_lon


def test_single_quest_display():
    display = QuestDisplay()
    location = get_current_lat_lon()

    display.draw_center(f"{round(location[0], 4),round(location[1], 4)}")
    pass
