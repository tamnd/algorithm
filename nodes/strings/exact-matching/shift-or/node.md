---
tag: D9WFTK
kind: algorithm
slug: shift-or
name: Shift-Or algorithm
aliases:
- Shift-And algorithm
- bit-parallel exact matching
area: strings/exact-matching
level: core
summary: 'Bit-parallel matching: a machine word tracks all partial matches; O(n ceil(m/w)) time.'
solves: [string-matching]
model: word-ram
complexity:
  vars: {n: the length of the text, m: the length of the pattern, σ: the alphabet size, w: the machine word size}
  time: {worst: Θ(n ⌈m/w⌉), best: Θ(n ⌈m/w⌉), preprocessing: Θ(m + σ ⌈m/w⌉)}
  space: {extra: Θ(σ ⌈m/w⌉)}
properties: {deterministic: true, recursive: false, online: true}
prereqs: [bit-parallelism, string-matching-automaton, word-ram]
see_also: [bitap-algorithm, bit-manipulation, knuth-morris-pratt, backward-dawg-matching, boyer-moore-horspool, approximate-string-matching]
sources:
  - paper: doi:10.1145/135239.135243
    title: R. Baeza-Yates and G. H. Gonnet, A new approach to text searching, Communications of the ACM 35(10) (1992), 74-82
    locator: the Shift-Or algorithm with the state vector and the character masks, and its extensions to classes of characters and mismatches
  - book: isbn:9780521813075
    title: Gonzalo Navarro and Mathieu Raffinot, Flexible Pattern Matching in Strings, Cambridge University Press, 2002
    locator: Chapter 2, String matching, the prefix-based approach (the Shift-And and Shift-Or algorithms as bit-parallel simulation of the nondeterministic automaton)
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 4, Section 4.2 (the Shift-And method and agrep), pages 70-86
  - url: http://www-igm.univ-mlv.fr/~lecroq/string/node6.html
    title: Christian Charras and Thierry Lecroq, Exact String Matching Algorithms, 1997
    locator: Shift Or algorithm (the vectors R_j, the masks S_c, preprocessing in O(m + σ), search in O(n) for a pattern no longer than the word size)
---

The Shift-Or algorithm solves [string matching](/string-matching/) by keeping, in one machine word, the set of all prefixes of the pattern that end at the current text position, and updating that set for each text character with one shift and one OR. It is a [bit-parallel](/bit-parallelism/) simulation of the nondeterministic automaton of the pattern, and runs in $\Theta(n)$ time for patterns no longer than the word size $w$, or $\Theta(n \lceil m/w \rceil)$ in general. Baeza-Yates and Gonnet introduced it in 1992; its extensions to character classes and errors are the base of the [Bitap](/bitap-algorithm/) family and of the agrep tool.

## In plain words

While reading the text, keep a row of switches, one per letter of the word. Switch number $j$ is on when the first $j + 1$ letters of the word end exactly at the letter just read. When switch $m - 1$ is on, the whole word ends here.

When a new letter arrives, each partial match either grows by one letter or dies. Switch $j$ turns on if switch $j - 1$ was on and the letter is the $j$-th letter of the word. Switch 0 turns on if the letter is the first letter of the word.

A computer word holds 64 switches, and moving all switches up by one place, then combining them with a precomputed pattern for the letter, takes two machine operations. So all partial matches advance at once.

## The problem

The input is a text $T[0 \ldots n-1]$ and a pattern $P[0 \ldots m-1]$ over an integer alphabet $\{0, \ldots, \sigma - 1\}$, so a character indexes the mask table; the implementation uses a hash map and accepts any characters. Indices are 0-based. The output is the list of all shifts $s$, $0 \le s \le n - m$, with $T[s \ldots s+m-1] = P$, in increasing order. Occurrences may overlap. If $m = 0$, all shifts $0, \ldots, n$ are output; if $m > n$, nothing is output. The model is the [word RAM](/word-ram/) with words of $w$ binary digits and constant-time shifts and Boolean operations.

## The algorithm

The state $D$ is a vector of $m$ binary digits; digit $j$ is 0 when $P[0 \ldots j]$ ends at the current text position. (Shift-Or uses 0 for "active" so that the shift brings in a 0 at digit 0, which activates the empty prefix for free; Shift-And uses 1 and needs an extra OR with 1.) The mask $B[c]$ has digit $j$ equal to 0 exactly when $P[j] = c$. $1^m$ is the vector of $m$ ones.

```pseudo id=main
SHIFT-OR(T, P)
L1  n ← |T|, m ← |P|
L2  if m = 0 then output 0, 1, …, n and return
L3  B[c] ← 1^m for every character c
L4  for j ← 0 to m − 1 do B[P[j]] ← B[P[j]] AND NOT (1 << j)
L5  D ← 1^m                                 ▷ no prefix is active
L6  for i ← 0 to n − 1 do
L7      D ← ((D << 1) OR B[T[i]]) AND 1^m
L8      if digit m − 1 of D is 0 then output i − m + 1
```

The shift moves each active prefix of length $j$ to length $j + 1$ and puts a 0 at digit 0, for the empty prefix. The OR with $B[T[i]]$ kills every prefix whose next pattern character is not $T[i]$. The AND keeps only $m$ digits, which in a fixed-width word is free when $m = w$. For $m > w$, $D$ and the masks are stored in $\lceil m/w \rceil$ words, and the shift carries the top digit of each word into the next.

## Example

$P$ = abab ($m = 4$), $T$ = aababab ($n = 7$). The masks, written from digit 3 down to digit 0, are $B[$a$]$ = 1010 and $B[$b$]$ = 0101.

| $i$ | $T[i]$ | $D$ after line L7 (digits 3 to 0) | active prefixes | output |
|---|---|---|---|---|
| 0 | a | 1110 | a | |
| 1 | a | 1110 | a | |
| 2 | b | 1101 | ab | |
| 3 | a | 1010 | a, aba | |
| 4 | b | 0101 | ab, abab | 1 |
| 5 | a | 1010 | a, aba | |
| 6 | b | 0101 | ab, abab | 3 |

At $i = 4$, digit 3 is 0, so abab ends at position 4 and the shift $4 - 4 + 1 = 1$ is output. The two occurrences at 1 and 3 overlap, and both are found because the prefix ab stays active inside the first one.

## Correctness

The invariant is: after line L7 for position $i$, digit $j$ of $D$ is 0 exactly when $P[0 \ldots j] = T[i - j \ldots i]$. Digit $j$ of the new $D$ is the OR of digit $j - 1$ of the old $D$ (or 0 for $j = 0$) and digit $j$ of $B[T[i]]$, so it is 0 exactly when $P[0 \ldots j-1]$ ended at $i - 1$ and $P[j] = T[i]$. Digit $m - 1$ is then 0 exactly when $P$ ends at $i$. The full proof is below.

## Complexity

- **Search.** Each text character costs a constant number of word operations on $\lceil m/w \rceil$ words, so the time is $\Theta(n \lceil m/w \rceil)$ in the best and the worst case, and $\Theta(n)$ when $m \le w$. It does not depend on the text or on the number of occurrences.
- **Preprocessing.** $\Theta(\sigma \lceil m/w \rceil)$ to set the masks and $\Theta(m)$ to clear one digit per pattern position, so $\Theta(m + \sigma \lceil m/w \rceil)$.
- **Space.** $\Theta(\sigma \lceil m/w \rceil)$ words for the masks, plus the state.
- **Comparison model.** The algorithm makes no character comparisons at all; it does one table lookup per text character.

| claim | value |
|---|---|
| search, $m \le w$ | $\Theta(n)$ |
| search, general | $\Theta(n \lceil m/w \rceil)$ |
| preprocessing | $\Theta(m + \sigma \lceil m/w \rceil)$ |
| extra space | $\Theta(\sigma \lceil m/w \rceil)$ words |

## Properties

- **Online and real time.** Each text character is read once and costs constant work for $m \le w$, and an occurrence is reported when its last character is read.
- **Integer alphabet.** The masks are indexed by characters. Characters not in $P$ share the mask $1^m$, so a hash map with a default works for any alphabet.
- **Flexible.** A mask can allow several characters at one position, so classes of characters, don't-care symbols and case-insensitive search need only a change of the masks.
- **Branch-free.** The inner loop has no data-dependent branch except the test for a match, which makes it fast on modern processors.

## Variants and improvements

- **Shift-And.** The same algorithm with 1 for active prefixes: $D \leftarrow ((D \ll 1) \mathbin{|} 1) \mathbin{\&} B[T[i]]$ with complemented masks.
- **Character classes.** Clear digit $j$ in $B[c]$ for every $c$ allowed at position $j$; the search is unchanged.
- **Errors.** Keeping $k + 1$ state vectors, one per number of errors, gives matching with up to $k$ mismatches or edits in $O(kn \lceil m/w \rceil)$ time: the [Bitap](/bitap-algorithm/) algorithm of Wu and Manber, used in agrep. See [approximate string matching](/approximate-string-matching/).
- **Backward bit-parallelism.** [Backward DAWG matching](/backward-dawg-matching/) simulated with bit vectors (BNDM) reads windows from the right and skips characters on average.
- **Long patterns.** For $m > w$, keep only the first $w$ characters in the bit-parallel filter and verify candidates directly.

## When to use it

Use Shift-Or for short patterns, up to the word size, especially over small alphabets such as DNA, and when the pattern has classes of characters or wildcards. It is simple, needs no backtracking, and works on streams. For long patterns over large alphabets, a [Boyer-Moore](/boyer-moore/)-style algorithm that skips characters is faster.

## Pitfalls

- **Overflow of the shift.** In a fixed-width language, $D \ll 1$ for $m = w$ drops the top digit, which is correct; but for $m < w$, digits above $m - 1$ must be ignored or masked, or a later test on the whole word fails. Line L7 masks with $1^m$.
- **The meaning of 0 and 1.** In Shift-Or a 0 digit means active; mixing in the Shift-And convention (testing for 1) reports wrong positions.
- **Characters absent from the pattern.** Their mask must be all ones, which kills every partial match; a default of 0 would activate every prefix. The test `test_edges` searches y in xyz.
- **Patterns longer than a word.** With a single 64-bit word, a longer pattern silently loses its top digits. The test `test_long_pattern` uses a pattern of 101 characters, which Python's unbounded integers handle.

## Implementations

## History

Ricardo Baeza-Yates and Gaston Gonnet presented the Shift-Or algorithm in "A new approach to text searching" (Communications of the ACM, 1992), with extensions to classes of characters and to mismatches. Wu and Manber extended it to edit distance in the same year and built the agrep tool on it. The nondeterministic-automaton view and the Shift-And form are developed in the book of Navarro and Raffinot, which also describes the backward variant BNDM.

## References
