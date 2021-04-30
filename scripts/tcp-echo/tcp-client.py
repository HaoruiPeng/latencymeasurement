import aiohttp
import asyncio
import time
import numpy as np
import pandas as pd

async def get_action(seq_no, SERVER_URL):
    send_time = timw.mononic()
    async with aiohttp.ClientSession() as session:
        async with session.get(SERVER_URL) as response:
            r = await response.text()
            receive_time = time.mononic()
            delay = receive_time - send_time
            return seq_no, delay

async def main(period):
    seq_no = 0
    pending_tasks = set()
    sem = asyncio.Semaphore(500)
    SERVER_URL = 'http://130.235.202.196'
    df_array = np.empty([10000, 2])
    ind = 0
    current_time = time.mononic()
    next_step = current_time + period
    while True:
        seq_no += 1
        async with sem:
            pending_tasks.add(asyncio.create_task(get_action(seq_no, SERVER_URL))
            diff = next_step - time.mononic()
            (done_tasks, pending_tasks) = await asyncio.wait(
                                        pending_tasks,
                                        return_when=asyncio.ALL_COMPLETED,
                                        timeout=max(0, diff)
                                        )
            for task in done_tasks:
                seq_num, delay = task.result()
                df_array[ind] = [seq_num, delay]
                ind += 1
                if ind >= 10000:
                    break
        await asyncio.sleep(max(0, next_step - time.monotonic()))
        next_step += period
        if ind >= 10000:
            break
    return df


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    period = 0.02
    main_group = asyncio.gather(main(period))
    result = loop.run_until_complete(main_group)
    columns = ['seq_no', 'delay']
    df = pd.DataFrame(result[0][0], columns=columns)
    df.to_pickle("tcp_measure.pkl")
