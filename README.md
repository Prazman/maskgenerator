# maskgenerator

## Goal
For a given list of words, generate a list of masks covering most of the list

A mask is a combination of letters representing character classes.

Here is the character classes table:
 l : abcdefghijklmnopqrstuvwxyz
u : ABCDEFGHIJKLMNOPQRSTUVWXYZ
d : 0123456789
h : 0123456789abcdef
H : 0123456789ABCDEF
s : special chars
a : luds (minuscules, majuscules, chiffres et caractères spéciaux)
b : 0x00 - 0xff

For example, the mask lllldd covers all combinations of 4 uncaptitalized letters and 2 digits
It's generated space is the number of combinations covered by this mask.
Here the generated space would be (26)^4\*10^2

This program's objective is to generate a series of mask that cover most of the elements in a list,
with a maximum generated space of 81 442 800 000 000

## Usage
- Clone the repository
- Create a folder called "split" inside the repo
- Create a folder called "output" inside the repo
- Run `python maskgenerator.py *path_to_dictionary_file* --split`

If you want to run the script again without repeating the split operations, remove the --split parameter

The splitting operation splits the dictionaray file into files of same length words.
It also removes oversized lines.
Caution: Splitting operation may be long for big dictionaries
The splitted files are kept in the /split folder

At the end of the program, all masks are outputed to /output/masks.dic with their statistics.

### options
`max_generated_space=x` : set x as the program's max generated space. *Default: 81 442 800 000 000*

`max_line_length` : set the max line length for treated words. Oversized lines will be rejected but counted in the ratio. Longer lines = bigger generated space *Default: 9*

`max_mask_combinations` : Number of mask combinations to be tested against. More combinations = more coverage but also longer computation time. *Default : 100*

'mask_rejection_ratio' : Reject the mask if it covers a smaller ratio of the words of same length *Default: 3%*
