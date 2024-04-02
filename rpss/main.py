import asyncio

from roblox import Client

GROUP_ID = 13276

print("Enter the ID of the Roblox group you want the worm to begin at")

# id_string = input()
id_sanitised = GROUP_ID # int(id_string)

print("Beginning...")

client = Client()

async def main():
    group = await client.get_group(id_sanitised)

    print("Name: ", group.name)
    print("Description: ", group.description)

    predators = []

    roles = await group.get_roles()
    first_rank_priority = roles[1].rank # skips guest

    async for user in group.get_members():
        if user.role.rank == first_rank_priority: # the first role
            profile = await client.get_user(user.id)

            user_chosen_texts = [
                profile.description,
                profile.display_name,
                profile.name
            ]

            print(f"username: { profile.name }\ndescription: { profile.description }\n")

asyncio.get_event_loop().run_until_complete(main())