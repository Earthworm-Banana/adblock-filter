import os
import argparse
from datetime import datetime
from pathlib import Path
from colorama import init, Fore

def parse_arguments():
    parser = argparse.ArgumentParser(description='Combine adblock filter files.')
    parser.add_argument('-t', '--title', default="Earthworm-Banana's Filters", help='Title for the combined filter file')
    parser.add_argument('-hp', '--homepage', default='https://github.com/Earthworm-Banana/adblock-filter', help='Homepage URL for the filter file')
    parser.add_argument('-ns', '--no-subtitle', action='store_true', help='Disable the subtitle addition')
    parser.add_argument('-nm', '--no-metadata', action='store_true', help='Do not add metadata to the combined file')
    parser.add_argument('-nsm', '--no-site-specific-metadata', action='store_true', help='Prevent adding metadata to each site-specific section')
    return parser.parse_args()

def find_filter_files(directory='Site Specific', exclude_file='all.txt'):
    directory_path = Path(directory)
    return [file for file in directory_path.glob('*.txt') if file.name != exclude_file]

def get_file_last_modified(file_path):
    return datetime.fromtimestamp(file_path.stat().st_mtime)

def preserve_file_timestamps(func):
    def wrapper(file_path, *args, **kwargs):
        original_times = (file_path.stat().st_atime, file_path.stat().st_mtime)
        func(file_path, *args, **kwargs)
        os.utime(file_path, original_times)
    return wrapper

@preserve_file_timestamps
def update_site_specific_file(file_path, args, content):
    last_modified = get_file_last_modified(file_path).strftime('%Y/%m/%d')
    filename_without_extension = file_path.stem
    title_line = f"! Title: {args.title} ({filename_without_extension})\n"
    homepage_line = f"! Homepage: {args.homepage}\n"
    modified_line = f"! Last modified: {last_modified}\n"

    content_sorted = sorted(set(line.strip() for line in content))  # Deduplicate, strip, and sort
    content_sorted_with_newlines = [line + '\n' for line in content_sorted]

    with open(file_path, 'w') as file:
        if not args.no_site_specific_metadata:
            file.writelines([title_line, homepage_line, modified_line, '\n'])
        file.writelines(content_sorted_with_newlines)

def read_filter_file(file_path, args):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return [line for line in lines if not line.startswith('!')]

def write_combined_file(file_content, latest_modified_date, args):
    with open('all.txt', 'w') as file:
        file.write(file_content)
    os.utime('all.txt', (latest_modified_date.timestamp(), latest_modified_date.timestamp()))

def main():
    init()
    args = parse_arguments()

    print(Fore.GREEN + "Starting the process of combining filter files...")

    filter_files = find_filter_files()
    combined_filters = []
    latest_modified_date = datetime.min

    for file_path in filter_files:
        print(Fore.YELLOW + f"Updating and processing {file_path.name}...")
        file_modified_date = get_file_last_modified(file_path)
        if file_modified_date > latest_modified_date:
            latest_modified_date = file_modified_date

        filters = read_filter_file(file_path, args)
        update_site_specific_file(file_path, args, filters)

        if not args.no_site_specific_metadata:
            combined_filters.append("\n\n\n")
            subtitle = f"! Source File: {file_path.stem}\n! {file_modified_date.strftime('%Y/%m/%d')}"
            combined_filters.append(subtitle)
        combined_filters.extend(filters)

    if not args.no_metadata:
        metadata = f"! Title: {args.title} (All)\n! Homepage: {args.homepage}\n! Last modified: {latest_modified_date.strftime('%Y/%m/%d')}"
        combined_filters.insert(0, metadata)

    write_combined_file(''.join(combined_filters), latest_modified_date, args)
    print(Fore.GREEN + "Filter files combined and updated successfully into all.txt")

if __name__ == "__main__":
    main()
