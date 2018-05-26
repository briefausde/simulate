import sys
import getopt
import random


def get_data():
    n = 0
    mode = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], "n:", ["mirror", "random"])
    except getopt.GetoptError:
        print('simulate.py -n <servers count> --<random or mirror>')
        sys.exit()

    for opt, arg in opts:
        if opt == "--mirror":
            mode = True
        elif opt == "--random":
            mode = False
        elif opt == "-n":
            n = arg
        else:
            assert False, "Unknow option"

    return n, mode


def generate_random_servers(n):
    files = [i for i in range(1, 101)] * 2
    servers_list = [[] for _ in range(0, int(n))]

    for _ in range(0, 100):
        shard = files[0]
        files.remove(shard)
        files.remove(shard)

        random.shuffle(servers_list)
        shortest_server = min(map(len, servers_list))  # search server with a minimal length

        is_first_el_in_server = False
        for server in servers_list:
            if len(server) == shortest_server:
                if not is_first_el_in_server:
                    server.append(shard)
                    is_first_el_in_server = True
                else:
                    server.append(shard)
                    break

        # min_server_list = list()
        #
        # for i in range(0, len(result)):
        #     if len(result[i]) == min_server:
        #         min_server_list.append(i)
        #
        # server1 = random.choice(min_server_list)
        # result[server1].append(shard)
        #
        # print(server1)
        # min_server_list.pop(server1)
        #
        # server2 = random.choice(min_server_list)
        # result[server2].append(shard)

    print(servers_list)
    return servers_list


def generate_mirror_servers(n):
    n = int(n)
    if n % 2 != 0:
        print("wrong data")
        sys.exit()
    servers_num = n // 2
    return [set([shard for shard in range((server*5)-4, (server*5)+1)]) for server in range(1, servers_num+1)]*2


def check_lost_shards(storages):
    for i in range(0, len(storages)):
        count = 0
        for j in range(0, len(storages)):
            if i != j:
                for shard in storages[i]:
                    if shard in storages[j]:
                        print(" If {0} and {1} servers dies, we lost shard {2}".format(i+1, j+1, shard))
                        count += 1
                        break
        print("When the {0} server dies first, then the data is lost in {1:0.1f}% cases\n".format(i+1, count/(len(storages)-1)*100))


if __name__ == "__main__":
    n, mode = get_data()
    if mode:
        servers = generate_mirror_servers(n)
    else:
        servers = generate_random_servers(n)

    # servers = [(1, 4, 7, 12, 15), (1, 5, 8, 12, 13), (2, 5, 7, 11, 14), (2, 6, 8, 10, 15), (3, 6, 9, 11, 13), (3, 4, 9, 10, 14)]
    # servers = [(1,2,3,4,5), (1,2,3,4,5), (6,7,8,9,10), (6,7,8,9,10), (11,12,13,14,15), (11,12,13,14,15)]

    check_lost_shards(servers)
