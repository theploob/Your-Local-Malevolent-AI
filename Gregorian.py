import asyncio
import time
import ClientHolder

name_prefix = "Cyber "
name_array = ["Greg", "Ian", "Greg", "Ian", "Greg", "Ian", "Greg"]


async def update():
    new_name = name_prefix
    new_name += name_array[time.localtime(time.time()).tm_wday]
    client = ClientHolder.GetClient()
    guild = await client.fetch_guild(791511639501439006)
    member = await guild.fetch_member(202168431024406528)
    await member.edit(nick=new_name)


# Call run_as_task from a thread other than the main thread owning the Client
async def run_as_task():
    main_loop = ClientHolder.get_client_asyncio_event_loop()
    send_fut = asyncio.run_coroutine_threadsafe(update(), main_loop)
    send_fut.result()
