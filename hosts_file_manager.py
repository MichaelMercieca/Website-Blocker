# import os


class HostsFileManager:
    REDIRECT_IP = "127.0.0.1"
    BLOCK_COMMENT = "# Blocked by Website Blocker"

    def __init__(self, hosts_file_path):
        self.hosts_file_path = hosts_file_path

    def add_entry_hosts(self, site) -> bool:
        """
        Appends a site to the hosts file.
        :param str site: the site to append to the hosts file
        :return: bool
        :raises PermissionError: if script not run with administrative privileges.
        """
        try:
            with open(self.hosts_file_path, 'a') as hosts_file:
                hosts_file.write(f"{self.REDIRECT_IP} {site} {self.BLOCK_COMMENT}\n")
                return True

        except PermissionError:
            print("Permission denied. Please run the script with administrative privileges.")
        except Exception as e:
            print(f"An error occurred: {e}")
        return False

    def remove_entry(self, site) -> bool:
        """
        Removes a site from the hosts file.
        :param str site: the site to remove from the hosts file
        :return: bool
        :raises PermissionError: if script not run with administrative privileges.
        """
        site_removed = False
        try:
            with open(self.hosts_file_path, 'r') as hosts_file:
                lines = hosts_file.readlines()
            with open(self.hosts_file_path, 'w') as hosts_file:
                for line in lines:
                    # Rewrite every line that isn't the line we are removing
                    if not (line.strip().endswith(self.BLOCK_COMMENT) and site in line):
                        hosts_file.write(line)
                    else:
                        site_removed = True
            if not site_removed:
                print("The site you are trying to remove was not found. "
                      "Please check that you spelt it correctly.")
            return site_removed

        except PermissionError:
            print("Permission denied. Please run the script with administrative privileges.")
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def is_blocked(self, site) -> bool:
        """Checks to see whether a particular site is blocked or not."""
        try:
            with open(self.hosts_file_path, 'r') as hosts_file:
                for line in hosts_file:
                    if site in line and line.strip().endswith(self.BLOCK_COMMENT):
                        return True
                return False
        except Exception as e:
            print(f"An error has occurred: {e}")
            return False
