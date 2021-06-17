from quest import Quest, start_quests
import datetime


def main():
    now = datetime.datetime.now()
    combination = f"{now.strftime('%-m')}{now.strftime('%d')}"

    quest = Quest(
        name="Hiking",
        lat=47.13299116317882,
        lon=-122.9058568840219,
        tolerance=.1,
        attempts=10,
        final_message=combination
    )

    start_quests([quest])


if __name__ == "__main__":
    main()
