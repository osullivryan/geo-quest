from quest import Quest, start_quests


def main():

    quest = Quest(
        name="Hiking",
        lat=47.13299116317882,
        lon=-122.9058568840219,
        tolerance=.1,
        attempts=10,
        final_message="530"
    )

    start_quests([quest])


if __name__ == "__main__":
    main()
