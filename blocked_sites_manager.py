import json
import os   # used to check whether the sentences file was created yet or not


class BlockedSitesManager:
    def __init__(self, sentences_file_path):
        self.sentences_file_path = sentences_file_path

    def load_sentences(self):
        """Loads the sentences file"""
        if os.path.exists(self.sentences_file_path):
            with open(self.sentences_file_path, 'r') as file:
                return json.load(file)
        return {}

    def save_sentences(self, sentences):
        """Saves the sentences file"""
        with open(self.sentences_file_path, 'w') as file:
            json.dump(sentences, file)

    def add_site_to_sentences_dict(self, site, sentences):
        """
        Adds a site with its sentences to the sentences dictionary.
        :param str site: The site to add
        :param list sentences: The sentences of the site to add
        :return: bool
        """
        sentences_dict = self.load_sentences()
        if site not in sentences_dict:
            sentences_dict[site] = sentences
            self.save_sentences(sentences_dict)
            return True
        else:
            return False

    def remove_site_from_sentences_dict(self, site):
        """
        Removes a site from the sentences dictionary.
        :param str site: The site to remove
        :return: bool
        """
        sentences_dict = self.load_sentences()
        if site in sentences_dict:
            del sentences_dict[site]
            self.save_sentences(sentences_dict)
            return True
        return False

    def list_sites(self, print_sites=False):
        """
        Returns the sentences dictionary.
        :param bool print_sites: If set to `True`, prints the sites in a
        predetermined format. Set to `False` if you want to make your own
        customised version.
        :return: dict
        """
        blocked_sites_list = self.load_sentences()
        if print_sites:
            print('LIST OF BLOCKED SITES:')
            print()
            for key, value in blocked_sites_list.items():
                print(f"->{key}:")
                for index, sentence in enumerate(value):
                    print(f"   {index+1}. {sentence}")
                print()
        return self.load_sentences()
