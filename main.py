import platform
from hosts_file_manager import HostsFileManager
from blocked_sites_manager import BlockedSitesManager

# TODO Add function for running in admin mode
# TODO Make links clickable and take you to that link
# TODO Inform users about reloading search engine for it to work


def main():
    # Determine the path to the hosts file based on the OS
    HOSTS_FILE_PATH = "/etc/hosts" if platform.system() != "Windows"\
        else r"C:\Windows\System32\drivers\etc\hosts"
    SENTENCES_FILE_PATH = "blocked_sites_sentences.json"
    ADMIN_PASSWORD = "Zebbug2007"
    ADMIN_PROMISE = ("I promise that I am only deleting this site because of"
                     " a bug or issue that won't let me remove it normally.")

    hosts_manager = HostsFileManager(HOSTS_FILE_PATH)
    sites_manager = BlockedSitesManager(SENTENCES_FILE_PATH)

    choice = -1
    while choice != 0:
        print()
        choice = int(input(
            '1. Block site\n'
            '2. Unblock site\n'
            '3. List blocked sites\n'
            '4. ADMIN TOOLS\n'
            '0. Quit\n'
            'Choose : '
        ))
        print()

        if choice == 1:
            site_to_block = input('Type the site to block: ')
            no_of_sentences = int(input('Type the number of sentences to have for this site: '))
            sentence_list = [input('Enter sentence '+str(i+1)+': ') for i in range(no_of_sentences)]

            if sites_manager.add_site_to_sentences_dict(site_to_block, sentence_list):
                if hosts_manager.add_entry_hosts(site_to_block):
                    print(f"{site_to_block} has been blocked.")
            else:
                print('Site has already been blocked.')

        elif choice == 2:
            site_to_unblock = input('Type the site to unblock: ')
            sentences = sites_manager.load_sentences()

            if site_to_unblock in sentences:
                unblock = True
                print(f"To unblock {site_to_unblock}, please enter the following sentences:")
                for index, sentence in enumerate(sentences[site_to_unblock]):
                    print(f"\"{sentence}\"")
                    user_input = input("Type sentence no " + str(index+1) + " exactly as shown: ")
                    if not user_input == sentence:
                        unblock = False
                        break

                if unblock:
                    if hosts_manager.remove_entry(site_to_unblock):
                        sites_manager.remove_site_from_sentences_dict(site_to_unblock)
                        print(f"{site_to_unblock} has been unblocked.")
                else:
                    print("Incorrect sentence. The site remains blocked.")
            else:
                print(f"{site_to_unblock} is not currently blocked or no sentence is associated with it.")

        elif choice == 3:
            sites_manager.list_sites(True)

        elif choice == 0:
            print('Thank you for using the website blocker. It will help you stay focused.')

        elif choice == 4:
            inp = input('Enter admin password: ')
            if inp == ADMIN_PASSWORD:
                choice_admin = -1
                while choice_admin != 0:
                    print()
                    choice_admin = int(input(
                        'Admin Tools:\n'
                        '1. Remove site without sentences\n'
                        '0. Back\n'
                        'Choice: '
                    ))
                    print()

                    if choice_admin == 1:
                        inp = input('Recite the promise to perform the action:\n'
                                    + ADMIN_PROMISE + '\n->')
                        site_to_unblock = input('Enter site to unblock: ')
                        if inp == ADMIN_PROMISE:
                            if hosts_manager.remove_entry(site_to_unblock):
                                sites_manager.remove_site_from_sentences_dict(site_to_unblock)

                    elif choice_admin == 0:
                        print('\n********\n')
                    else:
                        print('Invalid input. Please try again.')
            else:
                print('Invalid admin password.')
        else:
            print('Invalid input. Please try again.')


if __name__ == "__main__":
    main()