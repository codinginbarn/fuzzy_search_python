import re
import time
import os
import argparse
import logging
from Levenshtein import distance as levenshtein_distance

MAX_SIMILAR_LENGTH = 1
MAX_LEVENSHTEIN_DISTANCE = 2

def is_near_len(s1, s2):
    return abs(len(s1) - len(s2)) <= MAX_SIMILAR_LENGTH

def log(message):
    logging.info(message)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Fuzzy search within a file using Levenshtein distance.")
    parser.add_argument('--mxSimLen', '-msl', type=int, default=1,
                        help="Max 'similar length' difference - if length difference of words is less or equal to this, words are considered as similar length and should be checked by Levenshtein")
    parser.add_argument('--mxLevDist', '-mld', type=int, default=2,
                        help="Max tolerated Levenshtein distance")
    parser.add_argument('--source', '-src', required=True, type=str, help="Destination of file to be searched")
    parser.add_argument('--find', '-f', required=True, type=str, help="Phrase to find")
    return parser.parse_args()

def read_file(file_path):
    with open(file_path, "r") as file:
        return ' ' + re.sub(r"\s+", " ", file.read()) + ' '

def validate_path(file_path):
    # Ensure the provided path is absolute
    if not os.path.isabs(file_path):
        raise ValueError("The file path must be absolute.")
    
    # Prevent directory traversal attacks
    base_dir = os.path.abspath(os.getcwd())
    target_path = os.path.abspath(file_path)
    if not target_path.startswith(base_dir):
        raise ValueError("Invalid file path: Path traversal detected.")
    
    return target_path

def fuzzy_search(hay, needle, max_sim_len, max_lev_dist):
    hay_tokens = hay.split()
    needle_tokens = needle.split()
    i_range = len(hay_tokens) - len(needle_tokens)
    num_results = 0

    for ht_index in range(i_range):
        if not is_near_len(hay_tokens[ht_index], needle_tokens[0]):
            continue

        if all(is_near_len(hay_tokens[ht_index + j], needle_token) for j, needle_token in enumerate(needle_tokens[1:], 1)):
            matched_words = 0
            for needle_token in needle_tokens:
                if levenshtein_distance(needle_token, hay_tokens[ht_index + matched_words]) > max_lev_dist:
                    break
                matched_words += 1

            if matched_words == len(needle_tokens):
                found_text = " ".join(hay_tokens[ht_index:ht_index + matched_words])
                print(found_text)
                num_results += 1

    return num_results

def main():
    logging.basicConfig(level=logging.INFO, format='[INFO ] %(message)s')
    args = parse_arguments()

    global MAX_SIMILAR_LENGTH, MAX_LEVENSHTEIN_DISTANCE
    MAX_SIMILAR_LENGTH = args.mxSimLen
    MAX_LEVENSHTEIN_DISTANCE = args.mxLevDist

    start_time = time.time()

    try:
        validated_path = validate_path(args.source)
    except ValueError as e:
        log(str(e))
        return

    haystack = read_file(validated_path)
    log(f"File size {os.path.getsize(validated_path) / 1_000_000.0:.2f} MB")
    log(f"Searching for \"{args.find}\"")

    num_results = fuzzy_search(haystack, args.find, MAX_SIMILAR_LENGTH, MAX_LEVENSHTEIN_DISTANCE)

    elapsed_time = time.time() - start_time
    log(f"Found {num_results} results in {elapsed_time:.2f} s")

if __name__ == "__main__":
    main()
