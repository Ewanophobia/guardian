import asyncio
import csv

from tqdm import tqdm
from time import sleep
from roblox import Client
from datetime import datetime, timezone

GROUPS = [
    5618951,
    #6593843,
    #11541448,
    #10496736,
    #17105126,
    #1211022,
    #16810243,
    #13693544,
    #16723072
]

FIELDS = ["display_name", "username", "description", "user_id"]
MAX_FRIEND_DEPTH = 2

client = Client()

FOUR_YEARS = 365 * 4

def unicodeify(text):
    return u"" + str(text)

async def main():
    predators = []

    for group_id in GROUPS:
        group = await client.get_group(group_id)
        roles = await group.get_roles()
        first_rank_priority = roles[1].rank # skips guest

        async for member in group.get_members():
            if member.role.rank == first_rank_priority:  # the first role
                user = None

                while user is None:
                    try:
                        user = await client.get_user(member.id)
                    except:
                        sleep(1)
                        pass

                if (datetime.now(timezone.utc) - user.created).days < FOUR_YEARS:
                    print(f"Inserted {user.name} from {group.name}")
                    predators.append(user)

    async def loop_through_friends(depth): # unused as it throttles roblox too quickly
        if depth == MAX_FRIEND_DEPTH:
            return

        for predator in predators:
            user = await client.get_user(predator)

            print(f"Spider-webbing down 1 level, exploring {user.name}'s friends")

            for friend in await user.get_friends():
                if friend.id not in predators:
                    print(f"Inserted {friend.name} from {user.name}'s friend list")
                    predators.append(friend.id)
                    await loop_through_friends(depth + 1)

    print("Writing .csv")

    with tqdm(total=len(predators)) as loading_bar:
        with open("predators.csv", "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file)
            writer.writerow(FIELDS)

            for index, user in enumerate(predators):
                    writer.writerow(
                        (unicodeify(user.display_name), unicodeify(user.name), unicodeify(user.description), user.id)
                    )

                    loading_bar.update(index)

    print(f"Finished with {len(predators) - 1} rows")

asyncio.get_event_loop().run_until_complete(main())