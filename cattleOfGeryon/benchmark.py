import requests
import sys
import time
import datetime
from colorama import Fore
from colorama import Style
from multiprocessing import Process, Queue
import argparse

#url = ("http://en.wikipedia.org/wiki/Main_Page")
url = sys.argv[1]
nbr_requests = sys.argv[2]
nbr_clients = sys.argv[3]

try:
    r = requests.get(url)
    print(f"\n{Fore.GREEN}SITE WEB OK{Style.RESET_ALL}\n")
except:
    print(f"{Fore.RED}Site Web inexistant{Style.RESET_ALL}\n")
    sys.exit(0)

def ft_mysiege(url, nbr_requests):
    success = 0
    fail = 0
    a = 0
    start = datetime.datetime.now()
    start = start.timestamp()
    cumul_size = 0
    longest_transaction = 0.00;
    shortest_transaction = 10000;
    response_time = 0;

    print(f"{Fore.CYAN}")
    while (a < int(nbr_requests)):
        r = requests.get(url)
        if (r.status_code == 200):
            success = success + 1
        else:
            fail = fail + 1
        print("HTTP/" + str(r.raw.version), end='          ')
        print(r.status_code, r.reason, end='          ')
    
        time_exec = round(requests.get(url).elapsed.total_seconds(), 2)
        response_time = response_time + time_exec
        print(time_exec, end='        ')
        size = len(r.content)
        cumul_size = cumul_size + size
        if (time_exec > longest_transaction):
            longest_transaction = time_exec
        if (time_exec < shortest_transaction):
            shortest_transaction = time_exec
        print(size, end='           ')
        get = str(r.request)
        print(get[18:21], end='         ')
        print(url)
        a = a + 1
    end = datetime.datetime.now()
    end = end.timestamp()
    duration = end - start
    elapsed_time= round(duration, 2)
    response_time = response_time / float(nbr_requests)
    transaction_rate = float(nbr_requests) / elapsed_time
    cumul_size = cumul_size / 1000000
    throughput = cumul_size / elapsed_time
    availability = int(success) / int(nbr_requests) * 100
    print(f"\n{Fore.YELLOW}Total of requests:           " + nbr_requests + "\n")
    print("Availability:                " + str(int(availability)) + "%")
    print("Elapsed time:                " + str(elapsed_time) + " secs")
    print("Data transferred:            " + str(round(cumul_size, 2)) + " MB")
    print("Response time:               " + str(round(response_time, 3)) + " secs")
    print("Transaction rate:            " + str(round(transaction_rate, 2)) + " trans/sec")
    print("Throughput:                  " + str(round(throughput, 2)) + "MB/sec")
    print("Successful transactions:     " + str(success))
    print("Failed transactions:         " + str(fail))
    print("Longest transaction:         " + str(longest_transaction))
    print("Shortest transaction:        " + str(shortest_transaction))

if __name__=='__main__':
    i = 0
    print(f"\n{Style.BRIGHT}** MY_SIEGE 0.1")
    print("The server is now under siege ! ...\n")
    print("= = = = = = = = = = = = = = = = = = = = = = = = = ")
    while (i < int(nbr_clients)):
        p1 = Process(target = ft_mysiege, args = (url, nbr_requests))
        p1.start()
        #p1.join()
        i = i + 1
    

