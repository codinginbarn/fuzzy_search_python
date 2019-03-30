import re
import time
import os
import argparse

MAX_SIMILAR_LENGTH = 1
MAX_LEVENSHTEIN_DISTANCE = 2

# calculates leveshtein distance between two strings
def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 
            deletions = current_row[j] + 1     
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]


def levenshtein_pass(s1, s2, diff):
    diff = levenshtein(s1, s2)
    if diff < MAX_LEVENSHTEIN_DISTANCE:
        return True
    else:
        return False


# tolerate max length difference of 1
def is_near_len(s1, s2):
    if abs(len(s1) - len(s2)) < MAX_SIMILAR_LENGTH :
        return True
    else:
        return False

def log(message):
    print("[INFO ] " + message)



# PARSE ARGS

parser = argparse.ArgumentParser()
parser.add_argument('--mxSimLen', '-msl', 
    help="Max 'similar length' difference - if length difference of words is less or equal "
    + "to this, words are considered as similar length and should be checked by Levenshtein", 
    type=int, 
    default=1)
parser.add_argument('--mxLevDist', '-mld', 
    help="Max tolerated Levenshtein distance", 
    type= int, 
    default=2)
parser.add_argument('--source', '-src', help="Destination of file to be searched", type=str)
parser.add_argument('--find', '-f', help="Phrase to find", type=str)

args = parser.parse_args()

if args.source is None or args.find is None:
    print("*** Arguments -src and/or -f missing. Run with -h for details")
    exit()

if args.mxSimLen is not None:
    MAX_SIMILAR_LENGTH = args.mxSimLen + 1

if args.mxLevDist is not None:
    MAX_LEVENSHTEIN_DISTANCE = args.mxLevDist + 1


# PROCESS HAY AND NEEDLE

start = time.time()

file = open(args.source, "r")
hay = ' ' + file.read() + ' '
hay = re.sub("\\s+", " ", hay)  # remove whitespace, linebreaks etc.
file.close()
hay_tokens = hay.split()

log("File size " + str(os.path.getsize(args.source) / 1000000.0) + " MB")

needle = args.find
needle_tokens = needle.split()
log("Searching for \"" + needle + "\"")

# FIND NEEDLE 

num_results = 0
i_token = 0
i_range = len(hay_tokens) - len(needle_tokens)
for i_token in range(i_range):
    hay_token = hay_tokens[i_token]

    # if length of words is similar, they are checked for similarity
    if is_near_len(hay_token, needle_tokens[0]):
        matched_words = 0
        total_difference = 0

        # for every word in needle, check if corresponding word from 
        # source is similar, starting from current token
        for needle_token in needle_tokens:
            token_diff = 0;

            # break check if any of the words fails  
            if not levenshtein_pass(needle_token, hay_tokens[i_token + matched_words], token_diff):
                break
            matched_words += 1
            total_difference += token_diff

        # if every word is similar, phrase is found - print corresponding text from hay
        if matched_words == len(needle_tokens):
            found_text = ""
            i = 0
            for i in range(matched_words):
                found_text = found_text + hay_tokens[i_token + i] + " "
            print(found_text)
            num_results += 1

# LOG

end = time.time()
elapsed_time = end-start
log("Found " + str(num_results) + " results in " + str(round(elapsed_time, 2)) + " s")
