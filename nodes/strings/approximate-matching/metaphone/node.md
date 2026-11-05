---
tag: SN7VAT
kind: algorithm
slug: metaphone
name: Metaphone
aliases:
- Metaphone phonetic algorithm
area: strings/approximate-matching
level: intro
summary: Phonetic encoding that maps English words to rule-based consonant codes.
solves: [phonetic-string-matching]
model: word-ram
complexity:
  vars: {L: the length of the word}
  time: {worst: Θ(L)}
  space: {extra: O(L)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1990
  people: [Lawrence Philips]
  note: Philips published Metaphone in the magazine Computer Language in 1990 as a better phonetic code than Soundex for English words.
prereqs: [soundex, phonetic-string-matching]
see_also: [soundex, phonetic-string-matching, edit-distance, jaro-winkler-distance, approximate-dictionary-lookup]
sources:
  - paper: "Lawrence Philips, Hanging on the Metaphone, Computer Language 7(12), December 1990"
    locator: the original article with the transformation rules for English spelling
  - paper: "Lawrence Philips, The double metaphone search algorithm, C/C++ Users Journal 18(6), June 2000"
    locator: the successor Double Metaphone, with a primary and an alternate code
  - paper: doi:10.1145/146370.146380
    title: Karen Kukich, Techniques for automatically correcting words in text, ACM Computing Surveys 24(4), 1992
    locator: pages 377 to 439 (phonetic keys among the methods for the correction of isolated words)
---

Metaphone is a phonetic code that maps an English word to a string of consonant sounds, with rules that look at groups of letters such as PH, TH, CK and the soft C. Lawrence Philips published it in 1990 to fix the main weakness of [Soundex](/soundex/), which codes each letter alone. Two words match when their codes are equal, so Smith and Smyth both give SM0, and Catherine and Kathryn both give K0RN. The code takes one pass over the word, in time linear in its length.

## In plain words

English spelling and English sounds do not match well. The letters PH sound like F, the C in "city" sounds like S, and the K in "knight" is silent. A code that looks at single letters, like Soundex, misses these cases.

Metaphone reads the word from left to right and asks, for each letter, how it sounds in its place. It looks at the letter before and the letters after. A silent letter gives nothing. A letter that sounds like another letter gives that other letter. Vowels count only at the start of the word.

The result is a short string of sound symbols. Words that sound alike get the same string, even when their spellings differ. A search for a name then compares these strings instead of the spellings.

## The problem

The input is a word. Letters are compared without case, and characters that are not ASCII letters are ignored. The output is a string over the symbols B, F, H, J, K, L, M, N, P, R, S, T, W, X, Y and 0, where X stands for the sound "sh" and 0 (zero) for "th". A vowel A, E, I, O or U can appear as the first symbol only. Two words match when their codes are equal. There is no error bound and no index to report. This page uses no fixed length, while many programs cut the code to 4 or 6 symbols.

Philips stated the rules in words, and published programs read some of them in different ways. This page gives one exact reading of the original rule list. Other programs can give other codes for some words.

**Preparation.**

1. Remove each letter that is equal to the letter before it, except C.
2. If the word starts with KN, GN, PN, AE or WR, remove the first letter.

**The letters.** Each letter of the prepared word gives the output of the first case below that holds. "Before" and "after" refer to the neighbours in the prepared word, and the vowels are A, E, I, O and U.

| letter | cases, in order |
|---|---|
| vowel | itself at the start of the word; else nothing |
| B | nothing at the end of the word after M; else B |
| C | K in SCH; X before IA or H; S before I, E or Y; else K |
| D | J before GE, GY or GI; else T |
| G | nothing before H when the H is not last and is not before a vowel; nothing in GN or GNED at the end; nothing after D and before E, I or Y; J before I, E or Y; else K |
| H | nothing after C, G, P, S or T, or after a W at the start; nothing after a vowel when no vowel follows; else H |
| K | nothing after C; else K |
| P | F before H; else P |
| Q | K |
| S | X before H, IO or IA; else S |
| T | X before IA or IO; 0 before H; nothing before CH; else T |
| V | F |
| W | W at the start before H; W before a vowel; else nothing |
| X | S at the start; else KS |
| Y | Y before a vowel; else nothing |
| Z | S |
| F, J, L, M, N, R | itself |

## The algorithm

```pseudo id=main
METAPHONE(word)
L1  s ← the letters of word, in upper case
L2  w ← s without each letter that equals the letter before it, except C
L3  if w starts with KN, GN, PN, AE or WR then remove w[0]
L4  for i ← 0 to |w| − 1 do
L5      if w[i] is a vowel then append w[i] to out if i = 0, and go to the next i
L6      find the first case of the table for w[i] whose condition holds at position i
L7      append the output of that case to out    ▷ it can be empty
L8  return out
```

Each case tests at most the letter before $w[i]$ and three letters after it, all in the prepared word $w$. The output does not feed back into the tests. Pairs such as PH, TH, SH and CH are coded by their first letter, and the H after them is silent by its first case.

## Example

The word $\texttt{Catherine}$ has no double letters and no special start, so $w = \texttt{CATHERINE}$.

| $i$ | letter | case that holds | output | code so far |
|---|---|---|---|---|
| 0 | C | else K (A follows) | K | K |
| 1 | A | vowel, not at the start | | K |
| 2 | T | 0 before H | 0 | K0 |
| 3 | H | nothing after T | | K0 |
| 4 | E | vowel | | K0 |
| 5 | R | itself | R | K0R |
| 6 | I | vowel | | K0R |
| 7 | N | itself | N | K0RN |
| 8 | E | vowel | | K0RN |

For $\texttt{Kathryn}$, K gives K, TH gives 0, R gives R, the Y before N gives nothing, and N gives N. So the two names share the code K0RN, while their Soundex codes are C365 and K365.

More codes from the table:

| word | code | word | code |
|---|---|---|---|
| Knight | NT | Wright | RT |
| Philips | FLPS | Phillips | FLPS |
| Smith | SM0 | Smyth | SM0 |
| Stephen | STFN | Steven | STFN |
| Taylor | TLR | Tailor | TLR |
| Thumb | 0M | Xavier | SFR |
| Nation | NXN | Judge | JJ |
| Thompson | 0MPSN | Tomson | TMSN |

The last pair is a non-example: the two names sound alike, but the TH of Thompson gives 0 and its P gives P, so the codes differ.

## Correctness

The specification is the table, so the proof has two parts. First, lines L2 and L3 produce the prepared word: an induction over the letters shows that line L2 removes a letter exactly when it repeats the letter before it and is not C. Second, for each position, the program tests the cases of the letter in the order of the table and outputs the first one that holds. No case reads the output, so the concatenation of the outputs is the code. The full proof is below.

## Complexity

Each step of line L4 reads at most five letters of $w$ and appends at most two symbols. So the time is $\Theta(L)$ in the worst case for a word of length $L$, and the extra space is $O(L)$ for $w$ and the code. To search a list of $N$ words, compute each code once and group the words by code in a hash table. A query then costs one code plus the size of its group.

## Properties

- **An equivalence, not a distance.** Two words match or do not match, with no degree of similarity.
- **Context rules.** Unlike [Soundex](/soundex/), the code of a letter depends on its neighbours, so PH gives F and the C of "city" gives S.
- **Keeps the first sound, not the first letter.** Knight gives NT and Catherine gives K0RN. So Catherine and Kathryn match, which Soundex misses.
- **No fixed length.** The code has about one symbol for each consonant sound, so long words get long codes unless a program cuts them.
- **English only.** The rules follow English spelling.

## Variants and improvements

- **Double Metaphone.** Philips published it in 2000. It returns a primary and an alternate code, and it has rules for names of Slavic, Germanic, Romance and other origin. Two words match when one code of each word agrees.
- **Metaphone 3.** A later commercial version by Philips with more rules.
- **Fixed length.** Many programs keep only the first 4 symbols, as Soundex does.
- **Phonetic key plus distance.** A search can collect the words with the same key, then rank them by [edit distance](/edit-distance/) or by the [Jaro-Winkler distance](/jaro-winkler-distance/).

## When to use it

Use Metaphone to find English words or names that sound alike, for example in a spelling checker that suggests words, or in a search of names. It is more accurate than [Soundex](/soundex/) for English, and as fast. For names from many languages, use Double Metaphone. For typing errors that do not change the sound, use an [edit distance](/edit-distance/).

## Pitfalls

- **Different programs, different codes.** The original rules are in words, and programs differ in cases such as GH, SCH and the doubled letters. Do not compare codes from two different programs.
- **Truncation.** Codes cut to 4 symbols collide more often. Use the same length for all words.
- **Initial vowels.** A vowel counts only at the start, so Aeon and Eon both give EN, after the AE rule.
- **Not for other languages.** The rules give poor codes for words that are not English.

## Implementations

## History

Lawrence Philips published Metaphone in the magazine Computer Language in December 1990. He designed it as a replacement for Soundex that follows the rules of English pronunciation. In 2000 he published Double Metaphone in the C/C++ Users Journal, with an alternate code for words of other origin.

## References
