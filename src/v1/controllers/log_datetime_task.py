import asyncio, datetime

async def log_datetime():
    while True:
        print(datetime.datetime.now().isoformat())
        await asyncio.sleep(100)

if __name__ == "__main__":
    asyncio.run(log_datetime())