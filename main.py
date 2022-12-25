import os
import time
import asyncio
import aiohttp
import aiofiles


async def write_to_file(content):
    output_file = await aiofiles.open('output.txt', mode='a')
    await output_file.write(f"{content}\n")


async def get_bool(session, data):
    first_url = 'http://localhost:8080'
    second_url = 'http://localhost:8081'
    async with session.post(first_url, data=data) as first_response:
        first_data = await first_response.text()
    async with session.post(second_url, data=data) as second_response:
        second_data = await second_response.text()
    return str(first_data == second_data)


async def main():
    async with aiohttp.ClientSession() as session:
        responses = []

        with open(os.path.realpath("370098-lines.txt"), mode='r') as input_file:
            start = time.time()
            for line in input_file:
                data = await get_bool(session, line.strip())
                responses.append(asyncio.ensure_future(
                    write_to_file(data)))
            end = time.time()

        await asyncio.gather(*responses)
        print(f"Time to complete: {round(end - start, 2)}")


if __name__ == "__main__":
    asyncio.run(main())
