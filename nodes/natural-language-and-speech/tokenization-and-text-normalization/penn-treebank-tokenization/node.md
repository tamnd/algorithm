---
tag: BK6WGY
kind: algorithm
slug: penn-treebank-tokenization
name: Penn Treebank tokenization
aliases:
- PTB tokenizer
area: natural-language-and-speech/tokenization-and-text-normalization
level: intro
summary: Rule-based English word tokenization by regular expressions that splits off punctuation and clitics such as n't and 's, as in the Penn Treebank.
solves: [text-tokenization]
model: word-ram
complexity:
  vars: {n: the number of characters of the input line}
  time: {worst: O(n)}
  space: {extra: O(n)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1995
  people: [Robert MacIntyre, Mitchell P. Marcus, Beatrice Santorini, Mary Ann Marcinkiewicz]
  note: The Penn Treebank (Marcus, Santorini and Marcinkiewicz 1993) fixed the token conventions. Robert MacIntyre wrote the sed script that applies them at the University of Pennsylvania in late 1995.
prereqs: [text-tokenization, regular-expression]
see_also: [sentence-boundary-detection, punkt-sentence-tokenizer, part-of-speech-tagging, unicode-text-segmentation, subword-tokenization, maximal-munch, finite-state-transducer, tts-text-normalization]
sources:
  - url: https://aclanthology.org/J93-2004/
    title: Mitchell P. Marcus, Beatrice Santorini and Mary Ann Marcinkiewicz, Building a large annotated corpus of English, the Penn Treebank, Computational Linguistics 19(2), 1993
    locator: pages 313 to 330 (the corpus, its part-of-speech tag set and its annotation process)
  - url: https://github.com/andre-martins/TurboParser/blob/master/scripts/tokenizer.sed
    title: Robert MacIntyre, tokenizer.sed, the Penn Treebank tokenizer, University of Pennsylvania, 1995 (copy in the TurboParser repository)
    locator: the whole script, 33 substitutions in order, with the header comments on one sentence per line
  - url: https://www.nltk.org/api/nltk.tokenize.treebank.html
    title: NLTK documentation, module nltk.tokenize.treebank (TreebankWordTokenizer)
    locator: the class TreebankWordTokenizer, a port of the sed script with extra rules and the option convert_parentheses
---

Penn Treebank tokenization splits one English sentence into word tokens by an ordered list of regular expression substitutions, the convention used by the Penn Treebank. It separates punctuation, splits clitics such as n't, 's and 're from their words ("can't" becomes "ca" and "n't", "John's" becomes "John" and "'s"), and writes double quotes as an open quote ` `` ` and a close quote ` '' `. It is one rule set for the [tokenization](/text-tokenization/) problem, which has no single right answer: the problem page compares it with other conventions and with [subword tokenization](/subword-tokenization/). The original tool is a sed script by Robert MacIntyre, and it expects one sentence per line, so it must run after [sentence boundary detection](/sentence-boundary-detection/).

## In plain words

The program reads one sentence and puts spaces into it, then cuts it at the spaces. The rules run one after another, and each rule works on the whole sentence.

First it marks quotes that open a quotation. Then it puts spaces around commas, colons, dollar signs, brackets, question marks and the like, and before the period at the end of the sentence. Then it marks the remaining quotes as closing quotes. Last, it cuts off short endings such as "n't", "'s" and "'ll", and splits a few joined words such as "cannot" and "gonna" into two parts.

The order matters. A later rule sees the spaces that earlier rules added, and some rules need them.

## The problem

The input is one line $x$ of English text that holds one sentence. The output is a list of tokens, the fields of $x$ after the substitutions, split at runs of white space. The convention says what a token is, so the specification is the rule list itself. The tokens are not given with character offsets, because the open and close quotes replace the double quote character.

## The algorithm

Each line applies one group of rules of the sed script to the whole string, from left to right, and replaces every non-overlapping match.

```pseudo id=main
PTB-TOKENIZE(x)                            ▷ x is one sentence on one line, |x| = n
L1  replace a " at the start of x by `` and a space
L2  replace each " after a space or one of ( [ { < by a space, ``, and a space
L3  put spaces around each ... and around each of , ; : @ # $ % &
L4  split the period at the end of x from the character before it, unless that is a period; closing ) ] } > " ' may follow it
L5  put spaces around each ? and !, each bracket ( ) [ ] { } < >, and each --
L6  add one space at the start and one at the end of x
L7  replace each remaining " by a space, '', and a space
L8  split off a single ' after a word, and 's 'm 'd 'll 're 've n't (and 'S 'M 'D 'LL 'RE 'VE N'T) before a space
L9  split cannot, d'ye, gimme, gonna, gotta, lemme, more'n, 'tis, 'twas and wanna into two tokens
L10 return the fields of x between runs of spaces
```

Line L4 is the only rule for periods. It splits off the last period only, so "Mr." and "3.50" inside the sentence stay whole. Line L6 gives every word a space after it, which the clitic rules of line L8 need, because each of them matches the clitic and the space after it. Lines L2 and L7 decide between an open and a close quote by position only: a double quote at the start or after a space or an opening bracket opens a quotation, and every other one closes it. In the implementation, each line is a list of compiled patterns, and the sed replacement `&` (the whole match) becomes `\g<0>`.

## Example

Take $x$ = `He said, "I can't pay $3.50 for John's book."` The table shows the string after each line that changes it. Runs of spaces are shown as they are.

| after | string |
|---|---|
| L1 | unchanged, because $x$ does not start with a double quote |
| L2 | `He said,  `` I can't pay $3.50 for John's book."` |
| L3 | `He said ,   `` I can't pay  $ 3.50 for John's book."` |
| L4 | `He said ,   `` I can't pay  $ 3.50 for John's book ." ` |
| L5 | unchanged |
| L6 | the same with one more space at each end |
| L7 | `He said ,   `` I can't pay  $ 3.50 for John's book . ''` |
| L8 | `He said ,   `` I ca n't pay  $ 3.50 for John 's book . ''` |
| L9 | unchanged |

Line L10 gives 16 tokens: He, said, `,`, ` `` `, I, ca, n't, pay, `$`, 3.50, for, John, 's, book, `.`, ` '' `. The period of 3.50 stays inside its token, because line L4 looks only at the end of the line. In line L4 the period is followed by a double quote, which the closing-mark part of the pattern allows. In line L8 the rule for n't matches "n't " in "can't ", so the word becomes "ca n't"; the rule for 's matches "'s " in "John's ".

Three more cases from the tests: "Mr. Smith gonna stay." gives Mr., Smith, gon, na, stay, `.`; "'Tis cannot." gives 'T, is, can, not, `.`; and "It's the students' book." gives It, 's, the, students, `'`, book, `.`.

## Correctness

A convention has no external truth to check, so the proof in proofs/correctness.md shows three things. First, each line of the pseudocode applies the same substitutions as the sed script in the same order, so the function computes the tokens of the script. Second, every rule writes back the characters it matched, in order, and only adds spaces, except that double quotes become open or close quotes and line L4 drops trailing white space. So the tokens, joined and with the quote tokens written back as double quotes, give the input without its white space. Third, each of the 18 characters `,;:@#$%&?!()[]{}<>` ends up as a token by itself, because no rule removes a space next to it. The tests also compare the implementation with the sed script itself on 500 random lines, when a sed program is present.

## Complexity

- **Time.** Each of the 29 substitutions is one left to right pass of a regular expression with a bounded pattern, so it takes $O(m)$ time on a string of length $m$. A rule at most triples the length of the string, and the number of rules is fixed, so the total time is $O(n)$ for an input of $n$ characters. In practice the string grows by a few spaces per token.
- **Space.** $O(n)$ for the current string and the token list.

## Properties

- **Only spaces are added.** Apart from the quote marks, the tokens spell the input exactly, so a detokenizer can undo most of the changes.
- **Position decides the quote type.** A double quote right after a word, as in `said"`, always closes, and one after a space always opens.
- **One sentence at a time.** A period inside the line is never split off, so the input must already be split into sentences.
- **Case-sensitive clitic rules.** The script lists the lower case and the all upper case forms, so "WON'T" gives WO and N'T, but a mixed form such as "Won'T" is not split.
- **No offsets.** The output has no character offsets, because quotes are rewritten.

## Variants and improvements

- **Bracket symbols.** The treebank files write brackets as -LRB-, -RRB-, -LSB-, -RSB-, -LCB- and -RCB-. The sed script has these rules as comments, for use with a tagger, and the NLTK port has the option convert_parentheses.
- **The NLTK port.** NLTK's TreebankWordTokenizer is a port of the script with a few extra rules, for example for more contractions and for the separation of single quotes. Its output differs from the script on some inputs, so say which one you use.
- **Lexer-based tokenizers.** The Stanford PTBTokenizer is a finite-state lexer that follows the same conventions on running text with several sentences, and it handles abbreviations with a word list. A lexer reads the text once with the [maximal munch](/maximal-munch/) rule, instead of many passes.
- **Other conventions.** The Moses tokenizer for machine translation, the [Unicode word boundary rules](/unicode-text-segmentation/) and the pre-tokenizers of subword models use other conventions. Penn Treebank tokens are the input of most English treebank parsers and taggers trained on the WSJ section.

## When to use it

Use it when you train or evaluate on Penn Treebank data, or on any English corpus that follows its conventions, because a parser or [part-of-speech tagger](/part-of-speech-tagging/) trained on these tokens expects "ca n't" and not "can't". Measurements such as parsing F1 or perplexity are comparable only between systems that use the same tokens. For other languages, for text with many sentences per line, or for a neural model with its own vocabulary, use a tokenizer made for that case.

## Pitfalls

- **Several sentences on one line.** Line L4 splits only the last period of the line. "I like it. You do too." gives it. with the period attached. Run [sentence boundary detection](/sentence-boundary-detection/) first.
- **A final abbreviation.** Line L4 cannot tell an abbreviation from the end of a sentence, so "met in the U.S." gives U.S and a period. The treebank solves this case in the data, not with this rule.
- **Rules out of order.** If line L6 runs after line L8, the last word of the line has no space after it, and a clitic such as 's at the end of the line is not split. Keep the order of the script.
- **A wrong open quote.** Line L2 opens a quotation only after a space or an opening bracket. In "x="y"", the first quote after "=" is taken as a close quote by line L7. Fix the input or accept the convention.
- **Non-ASCII text.** The rules know only ASCII quotes, dashes and ellipses. Curly quotes, the Unicode ellipsis and long dashes pass through unchanged unless you map them first.

## Implementations

## History

The Penn Treebank project at the University of Pennsylvania annotated over 4.5 million words of American English with part-of-speech tags, and a part of it with skeletal parses (Marcus, Santorini and Marcinkiewicz 1993). Its token conventions, with separate clitics and the `` and '' quotes, became the standard input of English taggers and parsers trained on the Wall Street Journal section. Robert MacIntyre wrote the sed script that applies the conventions to new text in late 1995. Later tools, such as the NLTK port and the Stanford PTBTokenizer, keep the conventions and change the implementation.

## References
