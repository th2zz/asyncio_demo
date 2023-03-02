import asyncio 
seq = [i for i in range(50000)]
BATCH_SIZE=50

# this demo does some work on a long sequence batch by batch asynchronously

async def gather_with_concurrency(n: int, coros):
    semaphore = asyncio.Semaphore(n)
    async def sem_task(task):
        async with semaphore:
            return await asyncio.create_task(task)
    return await asyncio.gather(*[sem_task(coro) for coro in coros])

async def work(info):
    await asyncio.sleep(2)
    print(f"working on {info}")

async def async_batch_generator():
    for i in range(0, len(seq), BATCH_SIZE):
        batch = seq[i : i + BATCH_SIZE]
        yield batch


async def gen_tasks():
    tasks = []
    async for batch in async_batch_generator():
        tasks.append(work(batch))
    return tasks

async def main():
    tasks = await gen_tasks()
    await gather_with_concurrency(100, tasks)
    
asyncio.run(main())

