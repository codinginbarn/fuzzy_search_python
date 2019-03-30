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
