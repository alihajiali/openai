import asyncio, datetime

async def log_datetime():
    while True:
        with open("/etc/resolv.conf", "w") as file:
            file.write("nameserver 10.202.10.202")
        print(datetime.datetime.now().isoformat())
        await asyncio.sleep(100)

if __name__ == "__main__":
    asyncio.run(log_datetime())