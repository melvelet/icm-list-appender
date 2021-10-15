import csv
import glob
import click as click


def yield_csv_files_in_directory(directory: str, all_editions: bool = False, remove_lists: bool = False):
    file_no = 0
    for file in sorted(glob.glob(directory + "/*.csv"), reverse=all_editions):
        if ("\\_" in file and not remove_lists) or ("\\_" not in file and remove_lists):
            continue
        icm_list = list()
        file_no += 1
        with open(file, encoding='latin-1') as csvfile:
            for entry in csv.reader(csvfile, delimiter=','):
                icm_list.append(entry[11])
            yield file_no, file[len(directory) + 1:-len("*.csv") + 1], icm_list[1:]


class ICMListAppender:
    def __init__(self, entries_per_list: int, all_editions: bool):
        self.list_starts = list()
        self.imdb_urls = list()
        self.entries_per_list = entries_per_list
        self.all_editions = all_editions

    def append_list(self, name: str, icm_list: list):
        list_start = len(self.imdb_urls) + 1

        for i, entry in enumerate(icm_list):
            if self.entries_per_list and i >= self.entries_per_list:
                break

            if entry not in self.imdb_urls:
                self.imdb_urls.append(entry)

        self.list_starts.append((list_start, len(self.imdb_urls), name))

    def intersection(self, icm_list: list):
        for url in self.imdb_urls.copy():
            if url not in icm_list:
                self.imdb_urls.pop(self.imdb_urls.index(url))

    def remove_list(self, icm_list: list):
        for i, entry in enumerate(icm_list):
            if entry in self.imdb_urls:
                self.imdb_urls.remove(entry)

    def print_results_to_file(self, directory):
        with open(directory + '/results.txt', 'w') as file:
            digits = len(str(self.list_starts[-1][1]))
            for start, end, list_name in self.list_starts:
                file.write(f"#{str(start).zfill(digits)}-#{str(end).zfill(digits)}: Last in {list_name}\n")
            if self.list_starts:
                file.write('\n\n\n')

            for url in self.imdb_urls:
                file.write(url + '\n')


@click.command()
@click.option("-a", "--all-editions", is_flag=True, required=False, help='Order the file names in ascending order')
@click.option("-d", "--directory", type=str, required=True, help='Directory name of the lists to be processed')
@click.option("-e", "--entries-per-list", type=int, required=False, help='Maximum number of entries per list to be '
                                                                         'processed')
@click.option("-i", "--intersection", is_flag=True, required=False, help='Only keep movies that are part of every list'
                                                                         ' (intersection)')
def go(directory, all_editions, entries_per_list, intersection):
    if not entries_per_list:
        entries_per_list = False
    icm_list_appender = ICMListAppender(entries_per_list, all_editions)
    for file_no, name, file in yield_csv_files_in_directory(directory, all_editions):
        if intersection and file_no > 1:
            icm_list_appender.intersection(file)
        else:
            icm_list_appender.append_list(name, file)
    for _, _, file in yield_csv_files_in_directory(directory, all_editions, remove_lists=True):
        icm_list_appender.remove_list(file)
    icm_list_appender.print_results_to_file(directory)


if __name__ == '__main__':
    go()
