import time
import util
import multicraftapi
from time import gmtime, strftime

config = util.get_json_file("hidden_config.json")
server_data = util.get_json_file("server_data.json")
api = multicraftapi.MulticraftAPI(config["multicraftapi"]["location"], config["multicraftapi"]["user"], config["multicraftapi"]["key"], config["debug"]["show_api_request_info"])

servers = {}


def get_servers():
    global servers

    server_list = api.list_servers()["data"]["Servers"]
    for server in server_list:
        servers[server] = api.get_server(server)["data"]["Server"]
        if server not in server_data["restarts"]:
            server_data["restarts"][server] = 0
        if server not in server_data["backup_times"]:
            server_data["backup_times"][server] = 0

    util.set_json_file("server_data.json", server_data, True)


def check_servers():
    if config["debug"]["show_server_status_info"]:
        print("==================================================")
    for server in servers:
        if round(time.time() - server_data["restarts"][server]) < config["ignore_after_start_delay"]:
            print("Skipping server " + servers[server]["name"])
            continue

        status = api.get_server_status(server)["data"]["status"]
        if config["debug"]["show_server_status_info"]:
            print(status + ("    " if status == "online" else "   ") + servers[server]["name"])

        if status == "offline":
            server_name = servers[server]["name"]
            server_name = server_name.replace(" ", "_")
            server_name = server_name.lower()

            backup_location = strftime(config["backup_location"], gmtime())
            backup_location = backup_location.replace("{SERVER_NAME}", server_name)
            server_location = config["server_location"] + servers[server]["dir"]

            print(server_location, " => ", backup_location)

            string = strftime("Backing up " + servers[server]["name"] + ". Last backup took %M minutes and %S seconds.", gmtime(server_data["backup_times"][server]))
            print(string)
            api.send_all_console_command("say " + string)

            start_time = time.time()

            # util.zip_directory(server_location, backup_location, config["debug"]["show_folders_in_backup_progress"], config["debug"]["show_files_in_backup_progress"])

            finish_time = time.time() - start_time

            string = strftime("Finished backing up " + servers[server]["name"] + ". Backup took %M minutes and %S seconds.", gmtime(finish_time))
            print(string)
            api.send_all_console_command("say " + string)

            api.start_server(server)
            server_data["restarts"][server] = time.time()
            server_data["backup_times"][server] = finish_time

            util.set_json_file("server_data.json", server_data, True)


print("Starting initial check...")

get_servers()
check_servers()

print("Startup done. Polling every 30 seconds.")
while True:
    t = round(time.time())

    if t % 30 == 0:
        check_servers()
        get_servers()
