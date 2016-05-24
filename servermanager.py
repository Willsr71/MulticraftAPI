import time
import util
import threading
import multicraftapi
from time import gmtime, strftime

config = util.get_json_file("hidden_config.json")
server_data = util.get_json_file("server_data.json")
api = multicraftapi.MulticraftAPI(config["multicraftapi"]["location"], config["multicraftapi"]["user"], config["multicraftapi"]["key"], config["debug"]["show_api_request_info"])

servers = {}
active_backups = {}


class ServerBackupThread(threading.Thread):
    def __init__(self, server):
        threading.Thread.__init__(self)
        self.server = server

    def run(self):
        server_name = self.server["name"]
        server_name = server_name.replace(" ", "_")
        server_name = server_name.lower()

        backup_location = strftime(config["backup_location"], gmtime())
        backup_location = backup_location.replace("{SERVER_NAME}", server_name)
        server_location = config["server_location"] + self.server["dir"]

        print(server_location, " => ", backup_location)

        string = strftime("Backing up " + self.server["name"] + ". Last backup took %M minutes and %S seconds.", gmtime(server_data["backup_times"][self.server["id"]]))
        print(string)
        api.send_all_console_command("say " + string)

        start_time = time.time()

        try:
            util.zip_directory(server_location, backup_location, config["debug"]["show_folders_in_backup_progress"], config["debug"]["show_files_in_backup_progress"])
        except PermissionError:
            string = "Backup for server " + self.server["name"] + " failed. Permission Error."
            print(string)
            api.send_all_console_command("say " + string)

        finish_time = time.time() - start_time

        string = strftime("Finished backing up " + self.server["name"] + ". Backup took %M minutes and %S seconds.", gmtime(finish_time))
        print(string)
        api.send_all_console_command("say " + string)

        api.start_server(self.server["id"])
        server_data["restarts"][self.server["id"]] = time.time()
        server_data["backup_times"][self.server["id"]] = finish_time

        util.set_json_file("server_data.json", server_data)

        del active_backups[self.server["id"]]


def get_servers():
    global servers

    server_list = api.list_servers()["data"]["Servers"]
    for server in server_list:
        servers[server] = api.get_server(server)["data"]["Server"]
        if server not in server_data["restarts"]:
            server_data["restarts"][server] = 0
        if server not in server_data["backup_times"]:
            server_data["backup_times"][server] = 0

    util.set_json_file("server_data.json", server_data)


def check_servers():
    if config["debug"]["show_server_status_info"]:
        print("==================================================")
    for server in servers:
        if round(time.time() - server_data["restarts"][server]) < config["ignore_after_start_delay"]:
            if config["debug"]["show_server_status_info"]:
                print("Skipping server " + servers[server]["name"])
            continue

        status = api.get_server_status(server)["data"]["status"]
        if config["debug"]["show_server_status_info"]:
            print(status + ("    " if status == "online" else "   ") + servers[server]["name"])

        if status == "offline" and server not in active_backups:
            server_to_pass = servers[server]
            server_to_pass["id"] = server

            thread = ServerBackupThread(server_to_pass)
            thread.start()
            active_backups[server] = thread


print("Starting initial check...")

get_servers()
check_servers()

print("Startup done. Polling every 30 seconds.")
while True:
    t = round(time.time())

    if t % 30 == 0:
        check_servers()
        get_servers()
