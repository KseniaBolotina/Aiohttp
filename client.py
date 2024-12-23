import aiohttp
import asyncio

async def main():
    session = aiohttp.ClientSession()

    # response = await session.get('http://127.0.0.1:8080/ad/1')
    # print(response.status)
    # print(await response.text())

    # response = await session.post(
    #     "http://127.0.0.1:8080/ad",
    #     json={
    #             "header": "ad_1",
    #             "description": "description_1",
    #             "owner": "owner_1"
    #         }
    # )
    # print(response.status)
    # print(await response.json())

    # response = await session.patch(
    #     "http://127.0.0.1:8080/ad/1",
    #     json={
    #             "header": "ad_new"
    #         }
    # )
    # print(response.status)
    # print(await response.text())

    # response = await session.delete('http://127.0.0.1:8080/ad/1')
    # print(response.status)
    # print(await response.text())


    await session.close()

asyncio.run(main())