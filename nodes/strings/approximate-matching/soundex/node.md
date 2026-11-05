---
tag: 8WZ6WZ
kind: algorithm
slug: soundex
name: Soundex
aliases:
- American Soundex
area: strings/approximate-matching
level: intro
summary: Phonetic encoding that maps a name to a letter plus three digits.
solves: [phonetic-string-matching]
model: word-ram
complexity:
  vars: {L: the length of the name}
  time: {worst: Θ(L)}
  space: {extra: O(1)}
properties: {deterministic: true, exact: false, online: true, recursive: false}
history:
  year: 1918
  people: [Robert C. Russell, Margaret K. Odell]
  note: Russell patented an index of names by sound groups in 1918, and Knuth credits the system to Odell and Russell. The United States used the American form to index census records.
prereqs: [phonetic-string-matching, hash-function]
see_also: [metaphone, phonetic-string-matching, edit-distance, jaro-winkler-distance, approximate-dictionary-lookup, approximate-string-matching]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, Sorting and Searching, second edition
    locator: Chapter 6, the introduction to searching (the Soundex rules and the examples Euler, Gauss, Hilbert, Knuth, Lloyd and Lukasiewicz)
  - url: https://www.archives.gov/research/census/soundex
    title: United States National Archives and Records Administration, The Soundex Indexing System
    locator: the coding guide, with the rule for letters separated by H or W and the examples Ashcraft, Tymczak and Pfister
  - paper: "Robert C. Russell, Index, United States Patent 1,261,167, 1918"
    locator: the original patent of the name index by sound groups
  - paper: doi:10.1145/146370.146380
    title: Karen Kukich, Techniques for automatically correcting words in text, ACM Computing Surveys 24(4), 1992
    locator: pages 377 to 439 (phonetic codes such as Soundex among the methods for spelling correction)
---

Soundex is a phonetic code that maps a name to its first letter and three digits, so that names which sound alike in English get the same code. Robert and Rupert both get R163, and Ashcraft and Ashcroft both get A261. It is the classic method of [phonetic string matching](/phonetic-string-matching/): to find a name with an unknown spelling, compare codes instead of letters. The code is computed in one left-to-right pass, in time linear in the length of the name.

## In plain words

Clerks who index names have a problem: the same family name is written in many ways. Soundex gives each name a short label so that names that sound alike get the same label.

Keep the first letter. Then turn each consonant into a digit, so that consonants that sound alike, such as the letters for the sounds of p and b, share a digit. Drop the vowels. When two neighbouring letters give the same digit, write that digit only once. Stop at three digits, and add zeros if there are fewer.

To look up a name, compute its label and read all the names that have the same label. This finds many spellings of a name, but it also finds some names that only share the label by chance.

## The problem

The input is a name: a string that holds at least one ASCII letter. Letters are compared without case, and other characters, such as spaces, hyphens and apostrophes, are ignored. The output is a string of length 4: an upper-case letter followed by three digits. This page uses the American Soundex rules as the US National Archives and Knuth state them. Matching is exact on codes: two names match when their codes are equal. There is no error bound $k$ and no index set to report.

The letters get these digits:

| digit | letters | sound group |
|---|---|---|
| 1 | B, F, P, V | lip sounds |
| 2 | C, G, J, K, Q, S, X, Z | throat and hiss sounds |
| 3 | D, T | tongue on the teeth |
| 4 | L | |
| 5 | M, N | nasal sounds |
| 6 | R | |
| none | A, E, I, O, U, Y, H, W | vowels and weak letters |

The rules are:

1. Keep the first letter of the name.
2. Give each later letter its digit, and drop A, E, I, O, U, Y, H and W.
3. Two letters with the same digit that stand side by side in the name, or that have only H or W between them, give the digit once. This also holds for the first letter and the letter after it. A vowel between two such letters splits them, and both give the digit.
4. Keep the first three digits. Add zeros if there are fewer than three.

## The algorithm

```pseudo id=main
SOUNDEX(name)                              ▷ name holds at least one letter
L1  s ← the letters of name, in upper case
L2  out ← s[0], last ← code(s[0])          ▷ code(A, E, I, O, U, Y, H, W) = 0
L3  for i ← 1 to |s| − 1 do
L4      c ← code(s[i])
L5      if s[i] is H or W then continue    ▷ last does not change
L6      if c ≠ 0 and c ≠ last then append c to out
L7      last ← c                           ▷ a vowel sets last to 0
L8      if out has 3 digits then exit the loop
L9  return out, with zeros added up to length 4
```

The variable $last$ holds the digit of the last letter that is not H or W. Line L6 writes a digit only when it differs from $last$, which is rule 3. Line L5 skips H and W without a change of $last$, so a digit on each side of an H or a W counts once. A vowel sets $last$ to 0 in line L7, so the same digit after a vowel is written again. The first letter sets $last$ in line L2, so a second letter with the same digit, as in Pfister, gives no digit.

## Example

The name $\texttt{Ashcraft}$. The table shows the state after each letter.

| $i$ | letter | digit | action | $last$ | out |
|---|---|---|---|---|---|
| 0 | A | 0 | first letter | 0 | A |
| 1 | S | 2 | write 2 | 2 | A2 |
| 2 | H | 0 | skip (line L5) | 2 | A2 |
| 3 | C | 2 | same as $last$, no digit | 2 | A2 |
| 4 | R | 6 | write 6 | 6 | A26 |
| 5 | A | 0 | vowel | 0 | A26 |
| 6 | F | 1 | write 1, three digits, stop | 1 | A261 |

The code is A261. If H counted as a vowel, C would give a second 2, and the code would be A226. Some old programs make this mistake.

More codes from the rules:

| name | code | name | code |
|---|---|---|---|
| Robert | R163 | Rupert | R163 |
| Rubin | R150 | Lee | L000 |
| Tymczak | T522 | Pfister | P236 |
| Honeyman | H555 | Lukasiewicz | L222 |
| Euler | E460 | Ellery | E460 |
| Gauss | G200 | Ghosh | G200 |
| Hilbert | H416 | Heilbronn | H416 |
| Knuth | K530 | Kant | K530 |

In Tymczak, Z follows C with the same digit 2, so it gives no digit, but the K after the vowel A gives a new 2. In Honeyman, each N and the M are split by vowels, so the code has three 5s.

## Correctness

The code is defined by the four rules, and the proof shows that the loop applies them. The invariant of line L3 has two parts. First, $last$ is the digit of the last letter before position $i$ that is not H or W, or of the first letter. Second, $out$ holds the first letter and the digits of the letters before position $i$ that rule 3 keeps. The early exit of line L8 is safe, because rule 4 drops all digits after the third one. The full proof is below.

## Complexity

The loop does $O(1)$ work for each letter, so the time is $\Theta(L)$ for a name of length $L$ in the worst case, and line L8 can stop it earlier. The extra space is $O(1)$ beyond the copy of the letters, and a version that reads the name in place needs no copy. To find the names with a given code in a list of $N$ names, compute all codes once and group the names by code, for example in a hash table. A query then costs the time of one code plus the number of names in its group.

## Properties

- **Not a distance.** Soundex gives an equivalence relation: two names match or do not match. It gives no degree of similarity.
- **Many collisions.** Zeros appear only at the end of a code, so there are $26 \cdot (1 + 6 + 6^2 + 6^3) = 6734$ possible codes, and many unrelated names share a code. For example Lloyd and Ladd share L300, and Lukasiewicz and Lissajous share L222.
- **Misses.** Two spellings with a different first letter never match, for example Kant and Cant (K530 and C530).
- **English only.** The digit groups follow English consonants. Other languages need other rules.

## Variants and improvements

- **Simplified Soundex.** Some programs treat H and W as vowels. This gives A226 for Ashcraft. Some programs also merge equal digits across vowels.
- **Longer codes.** Keep more than three digits to reduce collisions.
- **Daitch-Mokotoff Soundex.** A code with six digits and rules for groups of letters, made for Slavic and Germanic names.
- **Metaphone and its successors.** [Metaphone](/metaphone/) uses rules on groups of letters, such as PH and the soft C, and codes English pronunciation more closely.
- **Phonetic code plus distance.** Some systems compare the codes, then rank the candidates by [edit distance](/edit-distance/) or [Jaro-Winkler distance](/jaro-winkler-distance/).

## When to use it

Use Soundex to find English family names with uncertain spellings in genealogy records and old indexes, where Soundex codes are already stored. It is fast and simple, and other systems understand its codes. For a better match of English pronunciation use [Metaphone](/metaphone/), and for typing errors use an [edit distance](/edit-distance/) or the [Jaro-Winkler distance](/jaro-winkler-distance/).

## Pitfalls

- **H and W.** They are not vowels in rule 3. Treating them as vowels gives other codes for names such as Ashcraft.
- **The first letter.** Its digit counts for rule 3, so Pfister is P236, not P123.
- **Prefixes.** Names such as Van Dyke or O'Hara can be coded with or without the prefix. Archives often code both forms.
- **Non-letters.** Remove spaces, hyphens and apostrophes before the coding, and decide how to handle accented letters.
- **An empty input.** A name without letters has no code. The program must reject it.

## Implementations

## History

Robert C. Russell received United States patents for an index of names by sound groups in 1918 and 1922. Knuth credits the system to Margaret K. Odell and Robert C. Russell. The American form on this page was used to index United States census records, and the National Archives publish its rules. Knuth describes Soundex at the start of the chapter on searching in The Art of Computer Programming, with the examples Euler and Ellery, Gauss and Ghosh, Hilbert and Heilbronn, Knuth and Kant, Lloyd and Ladd, and Lukasiewicz and Lissajous.

## References
