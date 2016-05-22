import time
import util
import multicraftapi
from time import gmtime, strftime

config = util.get_json_file("config.json")
api = multicraftapi.MulticraftAPI(config["multicraftapi"]["location"], config["multicraftapi"]["user"], config["multicraftapi"]["key"])

servers = {}
restarts = {}
backuptimes = {}


def get_servers():
    global servers

    server_list = api.list_servers()["data"]["Servers"]
    for server in server_list:
        servers[server] = api.get_server(server)["data"]["Server"]
        if server not in restarts:
            restarts[server] = 0
        if server not in backuptimes:
            backuptimes[server] = 0


def check_servers():
    print("==================================================")
    for server in servers:
        if round(time.time() - restarts[server]) < config["ignore_after_start_delay"]:
            print("Skipping server " + servers[server]["name"])
            continue

        status = api.get_server_status(server)["data"]["status"]
        print(status + ("    " if status == "online" else "   ") + servers[server]["name"])

        if status == "offline":
            server_name = servers[server]["name"]
            server_name = server_name.replace(" ", "_")
            server_name = server_name.lower()

            backup_location = strftime(config["backup_location"], gmtime())
            backup_location = backup_location.replace("{SERVER_NAME}", server_name)
            server_location = config["server_location"] + servers[server]["dir"]

            print(server_location, " => ", backup_location)

            string = strftime("Backing up " + servers[server]["name"] + ". Last backup took %M minutes and %S seconds.", gmtime(backuptimes[server]))
            print(string)
            api.send_all_console_command("say " + string)

            start_time = time.time()

            util.zip_directory(server_location, backup_location)

            finish_time = time.time() - start_time

            string = strftime("Finished backing up " + servers[server]["name"] + ". Backup took %M minutes and %S seconds.", gmtime(finish_time))
            print(string)
            api.send_all_console_command("say " + string)

            api.start_server(server)
            restarts[server] = time.time()
            backuptimes[server] = finish_time


get_servers()

print("Starting.")
while True:
    t = round(time.time())

    if t % 30 == 0:
        check_servers()
        get_servers()
