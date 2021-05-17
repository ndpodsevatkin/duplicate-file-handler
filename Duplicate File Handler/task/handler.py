import sys
import os
import hashlib

args = sys.argv
if len(args) != 2:
    print('Directory is not specified')
else:
    file_format = input('Enter the file format:\n')
    print("Size sorting options:\n1. Descending\n2. Ascending")
    hashes = {}
    for root, _, files in os.walk(args[1]):
        for name in files:
            if name.endswith(file_format):
                file_path = os.path.join(root, name)
                size = os.path.getsize(file_path)
                if size not in hashes:
                    hashes[size] = {}   # creates a dict for size as key
                with open(file_path, 'rb') as f:    # working wth binary files because of hashing
                    f_data = f.read()
                file_hash = hashlib.md5()
                file_hash.update(f_data)
                f_hash_hex = file_hash.hexdigest()  # return hash in hex format
                if f_hash_hex not in hashes[size]:
                    hashes[size][f_hash_hex] = []   # creates a list which will store file paths as values for hash
                hashes[size][f_hash_hex].append(file_path)

    while True:
        sort_opts = int(input("Enter a sorting option:\n"))
        reverse = True if sort_opts == 1 else False
        if sort_opts < 1 or sort_opts > 2:
            print('Wrong option')
        else:
            break

    for size in sorted(hashes.keys(), reverse=reverse):
        print(f"{size} bytes")
        for names in hashes[size].values():
            for name in names:
                print(name)

    count = 1
    counts = {}
    while True:
        is_duplicate = input('Check for duplicates?\n')
        if is_duplicate == 'yes':
            for size in sorted(hashes.keys(), reverse=reverse):
                hash_duplicates = {f_hash: f_list for f_hash, f_list in hashes[size].items() if len(f_list) > 1}
                if len(hash_duplicates) < 1:    # we're not interested in empty lists
                    continue
                print(f"{size} bytes")
                for f_hash, names in hash_duplicates.items():
                    print(f"Hash: {f_hash}")
                    for name in names:
                        print(f"{count}. {name}")   # assign number for every file path
                        counts[count] = name
                        count += 1
            break
        elif is_duplicate == 'no':
            break
        else:
            print('Wrong option')
    correct_nums = []   # a list which stores correct nums from usr input
    while True:
        delete_files = input('Delete files?\n')
        free_space = 0
        if delete_files == 'yes':
            while True:
                file_nums = input('Enter file numbers to delete:\n').split()
                if file_nums:
                    for i in file_nums:
                        try:
                            int(i)
                        except ValueError:
                            print('Wrong format')
                            break
                        if int(i) in counts.keys():
                            free_space += os.path.getsize(counts[int(i)])
                            os.remove(counts[int(i)])
                            correct_nums.append(i)
                        else:
                            print('Wrong format')
                            break
                    if len(correct_nums) == len(file_nums):
                        print(f"Total freed up space: {free_space} bytes")
                        break

                else:
                    print('Wrong format')

        elif delete_files == 'no':
            break
        else:
            print('Wrong format')
