import sys
import getopt
import random


def get_data():
    n = 0
    mode = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], "n:", ["mirror", "random"])
    except getopt.GetoptError:
        print('simulate.py -n <num of servers> --<random or mirror>')
        sys.exit()

    for opt, arg in opts:
        if opt == "--mirror":
            mode = True
        elif opt == "--random":
            mode = False
        elif opt == "-n":
            n = arg
        else:
            assert False, "Unknown option"

    return int(n), mode


def generate_random_servers(n):
    shards = list(range(1, 101)) * 2
    servers_list = [[] for _ in range(0, n)]

    for shard in range(1, 101):
        random.shuffle(servers_list)
        shortest_server = min(map(len, servers_list))  # search list with a minimal length

        for _ in range(2):
            shards.remove(shard)

            for server in servers_list:
                if len(server) == shortest_server:
                    server.append(shard)
                    break

    return servers_list


def generate_mirror_servers(n):
    if n % 2 != 0:
        print("n should be even number")
        sys.exit()
    servers_num = n // 2
    return [[shard for shard in range((server*5)-4, (server*5)+1)] for server in range(1, servers_num+1)]*2


def check_lost_shards(num_of_servers, storage):
    servers = dict(zip(range(1, num_of_servers+1), storage))

    for server, shards in servers.items():
        count = 0
        for server_second, shards_second in servers.items():
            if server != server_second:
                lost_shards = set(shards) & set(shards_second)
                if lost_shards:
                    count += 1
                    print(" If {} and {} servers dies, we lost shards {}".format(server, server_second, lost_shards))
        print("When {} server die first, then data is lost in {:0.1f}% cases\n".format(server, count/(len(storage) - 1) * 100))


if __name__ == "__main__":
    num_of_servers, generate_mode = get_data()

    if generate_mode:
        servers = generate_mirror_servers(num_of_servers)
    else:
        servers = generate_random_servers(num_of_servers)

    print(servers)
    check_lost_shards(num_of_servers, servers)
