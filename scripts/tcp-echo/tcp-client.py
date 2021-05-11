import aiohttp
import asyncio
import time
import argparse
import numpy as np
import pandas as pd
import os

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--dir', action="store")
parser.add_argument('-s', '--service', action="store")
args = parser.parse_args()

result_dir =  args.dir
if not os.path.exists(result_dir):
    os.makedirs(result_dir)

serviceType = args.service
if serviceType == "local":
    SERVER_URL = "http://localhost:8080/tcp"
if serviceType == "clusterIP":
    SERVER_URL = 'http://130.235.202.196:31619/tcp'
if serviceType == "nodePort":
    SERVER_URL = 'http://130.235.202.199:31234/tcp'
if serviceType == "Host":
    SERVER_URL = 'http://130.235.202.199:8080/tcp'

async def get_action(seq_no):
    send_time = time.monotonic()
    async with aiohttp.ClientSession() as session:
        print('get')
        async with session.post(SERVER_URL, data=b'ddd') as response:
            r = await response.text()
            receive_time = time.monotonic()
            delay = receive_time - send_time
            return seq_no, delay

async def main(period):
    seq_no = 0
    pending_tasks = set()
    done_tasks = set()
    # SERVER_URL = 'http://130.235.202.199:31234'
    # SERVER_URL = 'http://130.235.202.199:8080'
    df_array = np.empty([15000, 2])
    uf_array = np.empty([15000, 2])
    ind = 0
    indu = 0
    current_time = time.monotonic()
    next_step = current_time
    while True:
        start_time = time.monotonic()
        next_step += period
        for task in done_tasks:
            seq_num, delay = task.result()
            df_array[ind] = [seq_num, delay]
            ind += 1
            if ind >= 15000:
                break
        if indu >= 150:
            break
        seq_no += 1
        await asyncio.sleep(0.002)
        uf_array[indu] = [start_time, time.monotonic() - start_time]
        indu += 1
        pending_tasks.add(asyncio.create_task(get_action(seq_no)))
        (done_tasks, pending_tasks) = await asyncio.wait(
                                    pending_tasks,
                                    return_when=asyncio.ALL_COMPLETED,
                                    timeout=max(0, next_step - time.monotonic())
                                    )
    return df_array, uf_array


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    period = 0.02
    main_group = asyncio.gather(main(period))
    result = loop.run_until_complete(main_group)
    columns = ['seq_no', 'delay']
    ucolumns = ['time', 'clien_execution']
    print(result)
    df = pd.DataFrame(result[0][0], columns=columns)
    uf = pd.DataFrame(result[0][1], columns=ucolumns)
    df.to_pickle(result_dir + "/tcp_{}_delay.pkl".format(serviceType))
    uf.to_pickle(result_dir + "/tcp_{}.pkl_execution".format(serviceType))
