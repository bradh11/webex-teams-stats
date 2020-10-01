from webexteamssdk import WebexTeamsAPI, ApiError
import csv

api = WebexTeamsAPI(
    access_token="<token here>"
)

teamName = input(
    "Enter the team name if this is a team, otherwise leave blank: ")
roomName = input(
    "Enter the room name if this is a standalone room, otherwise leave blank for all rooms in a team: "
)
roomId = input("Enter the roomId: ")


def main(teamName, roomName, roomId):
    if teamName:
        for team in api.teams.list():
            print(team.name)
            if team.name == teamName:
                team_filename = team.name.replace("/", "_")
                with open(f"{team_filename}.csv", "w+", newline="") as csvfile:
                    csvwriter = csv.writer(
                        csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
                    )

                    for room in api.rooms.list(teamId=team.id):
                        for msg in api.messages.list(roomId=room.id):
                            print(room.title + " @ " + str(msg.created))
                            # data.append({ "created": msg.created, "personId": msg.personId, "roomId": msg.roomId })
                            msgCreated = ""
                            roomTitle = ""
                            msgPersonEmail = ""

                            try:
                                msgCreated = msg.created
                            except:
                                pass

                            try:
                                roomTitle = room.title
                            except:
                                pass

                            try:
                                msgPersonEmail = msg.personEmail
                            except:
                                pass

                            csvwriter.writerow(
                                [msgCreated, roomTitle, msgPersonEmail])
                            csvfile.flush()
                break

    if roomName or roomId:
        with open("%s.csv" % (roomName,), "w+", newline="") as csvfile:
            csvwriter = csv.writer(
                csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
            )
            if not roomName:
                room = api.rooms.get(roomId)
            else:
                allrooms = api.rooms.list()
                for room_details in allrooms:
                    if roomName == room_details.title:
                        room = room_details
                    else:
                        print(f"could not find {roomName}")
                        return
            for msg in api.messages.list(roomId=room.id):
                print(room.title + " @ " + str(msg.created))
                # data.append({ "created": msg.created, "personId": msg.personId, "roomId": msg.roomId })
                msgCreated = ""
                roomTitle = ""
                msgPersonEmail = ""

                try:
                    msgCreated = msg.created
                except:
                    pass

                try:
                    roomTitle = room.title
                except:
                    pass

                try:
                    msgPersonEmail = msg.personEmail
                except:
                    pass

                csvwriter.writerow([msgCreated, roomTitle, msgPersonEmail])
                csvfile.flush()


if __name__ == "__main__":
    main(teamName=teamName, roomName=roomName, roomId=roomId)
