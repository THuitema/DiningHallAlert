from umd import DiningHall
import django
import db

SOUTH = "South"
YAHENTAMITSI = "Yahentamitsi"
TWO_FIFTY_ONE = "251"
HALLS = {SOUTH: 16, YAHENTAMITSI: 19, TWO_FIFTY_ONE: 51}


def process_commands(dining_halls: list[DiningHall]):
    conn = db.connect()
    for hall in dining_halls:
        hall.check_for_alerts(conn)
    conn.close()


def main():
    the_y = DiningHall(name=YAHENTAMITSI, location_num=HALLS[YAHENTAMITSI])
    south = DiningHall(name=SOUTH, location_num=HALLS[SOUTH])
    two_fifty_one = DiningHall(name=TWO_FIFTY_ONE, location_num=HALLS[TWO_FIFTY_ONE])

    dining_halls = [the_y, south, two_fifty_one]

    process_commands(dining_halls)


if __name__ == "__main__":
    main()
