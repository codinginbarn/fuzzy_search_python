# fuzzy_search
Python script for fast text fuzzy search (based on Levenshtein's distance)

## Usage
This script searches for phrases in large text (```.txt```) files, with some difference tolerance.  
Optimised for natural human readable text (articles, books..) as it heavily relies on words separated by whitespaces.   
** Does not work with substrings (eg. will not find '*brown*' in '*quickbrownfox*')
## Parameters
Run with -h for details

* ```-src```  source file path (required)
* ```-f```  string to find (required)
* ```-msl```  max word length difference 
* ```-mld```  max Levenshtein distance 

## Examples
Default max Levenshtein distance (LD) is 2 and max word length difference (WLD) is 1:
 
text part | to find | match | reason
--------- | ------- | ----- | -
QUICK BROWN FOX JUMPS  | brown fox | yes | case insensitive
quick bro**nw** fox jumps | brown fox | yes | LD=2, WLD=0
quick brown**n** fox jumps | brown fox | yes | LD=1, WLD=1
quick **green** fox jumps | brown fox | no | ~~LD=3~~, WLD=0
quick brown**nn** fox jumps | brown fox | no | LD=2, ~~WLD=2~~

# fuzzy_search_v2

Here is a README for `search_v2.py`:

# Fuzzy Search Python Script

`search_v2.py` is a Python script for performing fuzzy text searches within a file using the Levenshtein distance algorithm.

## Features

- Perform fuzzy text searches in a file
- Configurable maximum similar length difference
- Configurable maximum tolerated Levenshtein distance
- Log search results and execution time

## Requirements

- Python 3.x
- `python-Levenshtein` library

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/codinginbarn/fuzzy_search_python.git
   ```
2. Navigate to the repository directory:
   ```sh
   cd fuzzy_search_python
   ```
3. Install the required library:
   ```sh
   pip install python-Levenshtein
   ```

## Usage

Run the script with the following command:
```sh
python search_v2.py --source <path_to_file> --find <phrase_to_find> [--mxSimLen <max_similar_length>] [--mxLevDist <max_levenshtein_distance>]
```

### Arguments

- `--source` (`-src`): Path of the file to be searched (required)
- `--find` (`-f`): Phrase to find (required)
- `--mxSimLen` (`-msl`): Max 'similar length' difference (default: 1)
- `--mxLevDist` (`-mld`): Max tolerated Levenshtein distance (default: 2)

### Example

```sh
python search_v2.py --source example.txt --find "fuzzy search" --mxSimLen 1 --mxLevDist 2
```

## Logging

The script uses the `logging` module to log information. By default, it logs to the console with the `[INFO]` level.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

No support, use at your own risk.

---

This README provides an overview of the script, its features, usage instructions, and contribution guidelines.
