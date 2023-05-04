

# Fuzex

Python based fuzzer with a regex like syntax. Supports generation of strings and variables specified in files. 


## Installation

Install the fuzex source through github. Then install the needed packages.

```bash
git clone https://github.com/abhishekg999/Fuzex
cd Fuzex
pip install -r requirements.txt
```


## Usage/Examples

```bash
usage: fuzex.py [-h] -c CMD [-o [OUTPUT]] [-f]

Fuzex command line arguments

optional arguments:
  -h, --help            show this help message and exit
  -c CMD, --cmd CMD     input command (required)
  -o [OUTPUT], --output [OUTPUT]
                        output file (default: stdout)
  -f, --force           Will allow Fuzex to process a large generation of words
```

By default, Fuzex is limited to generating 100000 lines. To bypass, use the `--force` flag.

## Commands
If you know basic Regex, you know Fuzex! Fuzex commands currently support basic operations such as groups, character ranges, and repeated characters.


#### Characters typed as they are will be generated as they are.
```re
python fuzex.py -c "abc"

Output:
abc
```

#### You can quantify how many times to repeat a character inside `{}`. You can specify 1 number to repeat a character that many times, two numbers to specify a range, or only the last number to specify 0 to n.
```re
python fuzex.py -c "ab{2}c{4}"

Output:
abbcccc
```
```re
python fuzex.py -c "ab{,2}c{3,4}"

Output:
accc
acccc
abccc
abcccc
abbccc
abbcccc
```

#### You can group characters using `(` and `)`. Repetitions act on the entire group.
```re
python fuzex.py -c "hello (world ){1,5}"

Output:
hello world 
hello world world
hello world world world
hello world world world world
hello world world world world world
```

#### The quantifier `?` can be used in place of `{,1}`. It stands for optional.
```re
python fuzex.py -c "i( don't)? like chicken"

Output:
i like chicken
i don't like chicken
```

#### You can specify character groups using `[` and `]`.
```re
python fuzex.py -c "[ABCDEF] is the best letter!"

Output:
A is the best letter!
B is the best letter!
C is the best letter!
D is the best letter!
E is the best letter!
F is the best letter!
```

#### You can also use `-` inside a group to specify a range of characters
```re
python fuzex.py -c "[A-F] is the best letter!"

Output:
A is the best letter!
B is the best letter!
C is the best letter!
D is the best letter!
E is the best letter!
F is the best letter!
```

```re
python fuzex.py -c "1?[0-9]"

Output:
0
1
2
...
18
19
```

## Roadmap

Fuzex currently supports basic Regex like syntax.

- Need to add OR expression
- Need to add support for Variables (this will allow specifying strings from an input file)

## Lessons Learned
- I thought this would be a cool project for generating custom wordlists. Imagine wanting to bruteforce a custom HTTP header or query parameter with a non standard string input. 
- I initially wanted to use a library to parse the grammer, but instead decided it would be cool to make it all manually. This is more of a learning aspect of this project for me.
- The Parser, Lexer, and Abstract Syntax Tree creation is entirely custom and can be seen in `/lib/core`. I learned alot about implementing parsers while making this.


## Authors
- [@abhishekg999](https://www.github.com/abhishekg999)


