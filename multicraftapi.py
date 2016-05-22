import requests
import hashlib
import hmac
import json
from util import print_line, colors


class MulticraftAPI:
    multicraft_location = ""
    multicraft_user = ""
    multicraft_key = ""
    debug = False

    def __init__(self, location, user, key, debug=False):
        self.multicraft_location = location
        self.multicraft_user = user
        self.multicraft_key = key
        self.debug = debug

    def print_debug(self, w):
        if self.debug:
            print_line(w)

    def send_request(self, operation, content=None):
        params = {}
        if content is not None:
            params = content

        params["_MulticraftAPIMethod"] = operation
        params["_MulticraftAPIUser"] = self.multicraft_user

        keystr = ""

        for param in params:
            keystr += param + str(params[param])

        key = hmac.new(self.multicraft_key.encode('utf-8'), keystr.encode('utf-8'), hashlib.sha256).hexdigest()
        params["_MulticraftAPIKey"] = key

        request = requests.post(self.multicraft_location, params)

        self.print_debug(colors.YELLOW + str(request.elapsed) + colors.END + " / ")
        self.print_debug(colors.GREEN if request.status_code == 200 else colors.RED)
        self.print_debug(str(request.status_code) + " " + request.reason + colors.END)

        if not request.status_code == 200:
            self.print_debug("\n")
            return {}

        result = json.loads(request.text)

        self.print_debug(" / ")
        self.print_debug(colors.GREEN + "success" if result["success"] else colors.RED + "error")
        if not result["success"]:
            self.print_debug(": ")

            error_string = ""
            for error in result["errors"]:
                error_string += error + ", "

            self.print_debug(error_string[:-2])

        self.print_debug(colors.END + "\n")

        return result

    # User functions

    def list_users(self):
        return self.send_request("listUsers")

    def find_users(self, field, value):
        return self.send_request("findUsers", {"field": field, "value": value})

    def get_user(self, user_id):
        return self.send_request("getUser", {"id": user_id})

    def get_current_user(self):
        return self.send_request("getCurrentUser")

    def update_user(self, user_id, field, value):
        return self.send_request("updateUser", {"id": user_id, "field": field, "value": value})

    def create_user(self, name, email, password):
        return self.send_request("createUser", {"name": name, "email": email, "password": password})

    def delete_user(self, user_id):
        return self.send_request("deleteUser", {"id": user_id})

    def get_user_role(self, user_id, server_id):
        return self.send_request("getUserRole", {"user_id": user_id, "server_id": server_id})

    def set_user_role(self, user_id, server_id, role):
        return self.send_request("setUserRole", {"user_id": user_id, "server_id": server_id, "role": role})

    def get_user_ftp_access(self, user_id, server_id):
        return self.send_request("getUserFtpAccess", {"user_id": user_id, "server_id": server_id})

    def set_user_fep_access(self, user_id, server_id, mode):
        return self.send_request("setUserFtpAccess", {"user_id": user_id, "server_id": server_id, "mode": mode})

    def get_user_id(self, name):
        return self.send_request("getUserId", {"name": name})

    def validate_user(self, name, password):
        return self.send_request("validateUser", {"name": name, "password": password})

    def generate_user_api_key(self, user_id):
        return self.send_request("generateUserApiKey", {"user_id": user_id})

    def get_user_api_key(self, user_id):
        return self.send_request("getUserApiKey", {"user_id": user_id})

    def remove_user_api_key(self, user_id):
        return self.send_request("removeUserApiKey", {"user_id": user_id})

    # Player functions

    def list_players(self, server_id):
        return self.send_request("listPlayers", {"server_id": server_id})

    def find_players(self, server_id, field, value):
        return self.send_request("findPlayers", {"server_id": server_id, "field": field, "value": value})

    def get_player(self, player_id):
        return self.send_request("getPlayer", {"id": player_id})

    def update_player(self, player_id, field, value):
        return self.send_request("updatePlayer", {"id": player_id, "field": field, "value": value})

    def create_player(self, server_id, name):
        return self.send_request("createPlayer", {"server_id": server_id, "name": name})

    def delete_player(self, player_id):
        return self.send_request("deletePlayer", {"id": player_id})

    def assign_player_to_user(self, player_id, user_id):
        return self.send_request("assignPlayerToUser", {"player_id": player_id, "user_id": user_id})

    # Command functions

    def list_commands(self, server_id):
        return self.send_request("listCommands", {"server_id": server_id})

    def find_commands(self, server_id, field, value):
        return self.send_request("findCommands", {"server_id": server_id, "field": field, "value": value})

    def get_command(self, command_id):
        return self.send_request("getCommand", {"id": command_id})

    def update_command(self, command_id, field, value):
        return self.send_request("updateCommand", {"id": command_id, "field": field, "value": value})

    def create_command(self, server_id, name, role, chat, response, run):
        return self.send_request("createCommand", {"server_id": server_id, "name": name, "role": role, "chat": chat, "response": response, "run": run})

    def delete_command(self, command_id):
        return self.send_request("deleteCommand", {"id": command_id})

    # Server functions

    def list_servers(self):
        return self.send_request("listServers")

    def find_servers(self, field, value):
        return self.send_request("findServers", {"field": field, "value": value})

    def list_servers_by_connection(self, connection_id):
        return self.send_request("listServersByConnection", {"connection_id", connection_id})

    def list_servers_by_owner(self, user_id):
        return self.send_request("listServersByOwner", {"user_id": user_id})

    def get_server(self, server_id):
        return self.send_request("getServer", {"id": server_id})

    def update_server(self, server_id, field, value):
        return self.send_request("updateServer", {"id": server_id, "field": field, "value": value})

    def create_server_on(self, daemon_id=0, no_commands=0, no_setup_script=0):
        return self.send_request("createServerOn", {"daemon_id": daemon_id, "no_commands": no_commands, "no_setup_script": no_setup_script})

    def create_server(self, name="", port=0, players=0, no_setup_script=0):
        return self.send_request("createServer", {"name": name, "port": port, "players": players, "no_setup_script": no_setup_script})

    def suspend_server(self, server_id, stop=1):
        return self.send_request("suspendServer", {"id": server_id, "stop": stop})

    def resume_server(self, server_id, start=1):
        return self.send_request("resumeServer", {"id": server_id, "start": start})

    def delete_server(self, server_id, delete_dir="no", delete_user="no"):
        return self.send_request("deleteServer", {"id": server_id, "delete_dir": delete_dir, "delete_user": delete_user})

    def get_server_status(self, server_id, player_list=0):
        return self.send_request("getServerStatus", {"id": server_id, "player_list": player_list})

    def get_server_owner(self, server_id):
        return self.send_request("getServerOwner", {"server_id": server_id})

    def set_server_owner(self, server_id, user_id):
        return self.send_request("setServerOwner", {"server_id": server_id, "user_id": user_id})

    def get_server_config(self, server_id):
        return self.send_request("getServerConfig", {"id": server_id})

    def update_server_config(self, server_id, field, value):
        return self.send_request("updateServerConfig", {"server_id": server_id, "field": field, "value": value})

    def start_server_backup(self, server_id):
        return self.send_request("startServerBackup", {"id": server_id})

    def get_server_backup_status(self, server_id):
        return self.send_request("getServerBackupStatus", {"id": server_id})

    def start_server(self, server_id):
        return self.send_request("startServer", {"id": server_id})

    def stop_server(self, server_id):
        return self.send_request("stopServer", {"id": server_id})

    def restart_server(self, server_id):
        return self.send_request("restartServer", {"id": server_id})

    def kill_server(self, server_id):
        return self.send_request("killServer", {"id": server_id})

    def start_all_servers(self):
        return self.send_request("startAllServers")

    def stop_all_servers(self):
        return self.send_request("stopAllServers")

    def restart_all_servers(self):
        return self.send_request("restartAllServers")

    def kill_all_servers(self):
        return self.send_request("killAllServers")

    def send_console_command(self, server_id, command):
        return self.send_request("sendConsoleCommand", {"server_id": server_id, "command": command})

    def send_all_console_command(self, command):
        return self.send_request("sendAllConsoleCommand", {"command": command})

    def run_command(self, server_id, command_id, run_for=0):
        return self.send_request("runCommand", {"server_id": server_id, "command_id": command_id, "run_for": run_for})

    def get_server_log(self, server_id):
        return self.send_request("getServerLog", {"id": server_id})

    def clear_server_log(self, server_id):
        return self.send_request("clearServerLog", {"id": server_id})

    def get_server_chat(self, server_id):
        return self.send_request("getServerChat", {"id": server_id})

    def clear_server_chat(self, server_id):
        return self.send_request("clearServerChat", {"id": server_id})

    def send_server_control(self, server_id, command):
        return self.send_request("sendServerControl", {"id": server_id, "command": command})

    def get_server_resources(self, server_id):
        return self.send_request("getServerResources", {"id": server_id})

    def move_server(self, server_id, daemon_id):
        return self.send_request("moveServer", {"server_id": server_id, "daemon_id": daemon_id})

    # Daemon functions

    def list_connections(self):
        return self.send_request("listConnections")

    def find_connections(self, field, value):
        return self.send_request("findConnections", {"field": field, "value": value})

    def get_connection(self, connection_id):
        return self.send_request("getConnection", {"id": connection_id})

    def remove_connection(self, connection_id):
        return self.send_request("removeConnection", {"id", connection_id})

    def get_connection_status(self, connection_id):
        return self.send_request("getConnectionStatus", {"id": connection_id})

    def get_connection_memory(self, connection_id, include_suspended=0):
        return self.send_request("getConnectionMemory", {"id": connection_id, "include_suspended": include_suspended})

    def get_statistics(self, daemon_id=0, include_suspended=0):
        return self.send_request("getStatistics", {"daemon_id": daemon_id, "include_suspended": include_suspended})

    # Settings functions

    def list_settings(self):
        return self.send_request("listSettings")

    def get_setting(self, key):
        return self.send_request("getSetting", {"key": key})

    def set_setting(self, key, value):
        return self.send_request("setSetting", {"key": key, "value": value})

    def delete_setting(self, key):
        return self.send_request("deleteSetting", {"key": key})

    # Schedule functions

    def list_schedules(self):
        return self.send_request("listSchedules")

    def find_schedules(self, server_id, field, value):
        return self.send_request("findSchedules", {"server_id": server_id, "field": field, "value": value})

    def get_schedule(self, schedule_id):
        return self.send_request("getSchedule", {"id": schedule_id})

    def update_schedule(self, schedule_id, field, value):
        return self.send_request("updateSchedule", {"id": schedule_id, "field": field, "value": value})

    def create_schedule(self, server_id, name, ts, interval, cmd, status, for_):
        return self.send_request("createSchedule", {"server_id": server_id, "name": name, "ts": ts, "interval": interval, "cmd": cmd, "status": status, "for": for_})

    def delete_schedule(self, server_id):
        return self.send_request("deleteSchedule", {"id": server_id})

    # Database functions

    def get_database_info(self, server_id):
        return self.send_request("getDatabaseInfo", {"server_id": server_id})

    def create_database(self, server_id):
        return self.send_request("createDatabase", {"server_id": server_id})

    def change_database_password(self, server_id):
        return self.send_request("changeDatabasePassword", {"server_id": server_id})

    def delete_database(self, server_id):
        return self.send_request("deleteDatabase", {"server_id": server_id})
