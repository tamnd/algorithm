---
tag: TM3QDZ
kind: problem
slug: palindrome-recognition
name: Palindrome recognition
aliases:
- palindrome testing
- palindrome check
area: strings/palindromes
level: intro
summary: Decide whether a given string is a palindrome, in linear time with two pointers.
model: comparison-model
complexity:
  vars: {n: the length of the string}
  time: {worst: Θ(n)}
prereqs: [palindrome, two-pointers]
see_also: [manacher, longest-palindromic-substring, palindrome-substring-queries, adversary-argument, multitape-turing-machine, polynomial-rolling-hash, string-equality-testing, context-free-language]
sources:
  - paper: doi:10.1016/s0019-9958(65)90399-2
    title: F. C. Hennie, One-tape, off-line Turing machine computations, Information and Control 8(6) (1965), 553-578
    locator: the crossing-sequence method and its application to the recognition of palindromes (quadratic time on one tape)
  - paper: doi:10.1145/800113.803644
    title: Zvi Galil, Real-time algorithms for string-matching and palindrome recognition, Proceedings of the 8th ACM Symposium on Theory of Computing (STOC 1976), 161-173
    locator: the real-time recognition of palindromes by random access machines and by Turing machines
  - paper: doi:10.1145/321892.321896
    title: Glenn Manacher, A new linear-time on-line algorithm for finding the smallest initial palindrome of a string, Journal of the ACM 22(3) (1975), 346-351
    locator: the whole paper (the online test of each prefix for being a palindrome)
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 9, Section 9.2, Finding all maximal palindromes in linear time (pages 197 to 199)
---

Palindrome recognition is the problem of deciding whether a string is a [palindrome](/palindrome/), that is, whether it equals its own reversal. The two-pointer scan compares the first symbol with the last, the second with the second to last, and so on, and answers in $\Theta(n)$ time with at most $\lfloor n/2 \rfloor$ symbol comparisons. An [adversary argument](/adversary-argument/) shows that $\lfloor n/2 \rfloor$ equality comparisons are necessary, so the scan is exactly optimal. The problem is a standard example in the theory of computation: a one-tape Turing machine needs quadratic time for it, and a one-pass algorithm needs linear memory unless it uses randomness.

## In plain words

Put one finger on the first letter and one finger on the last letter. If the two letters differ, the word is not a palindrome, and you can stop. If they are the same, move both fingers one step toward the middle and compare again. When the fingers meet or cross, every letter has been matched with its mirror letter, so the word is a palindrome.

You look at each mirror pair one time, so a word of a hundred letters needs at most fifty comparisons. A method that only compares letters cannot do with fewer. With fewer comparisons, some letter is not tied to its mirror letter by any chain of comparisons, and a change of that letter goes unseen.

## Definition

**Input.** A string $s = s[0..n-1]$ of length $n \ge 0$ over an [alphabet](/alphabet/) $\Sigma$. Indices are 0-based. The algorithm may only test two symbols for equality; no order on $\Sigma$ is used, and $\Sigma$ may be of any size.

**Output.** YES if $s = s^R$, that is, if
$$ s[i] = s[n-1-i] \quad \text{for all } 0 \le i < \lfloor n/2 \rfloor, $$
and NO otherwise. The empty string and each string of length 1 are palindromes. Even and odd lengths need no separate treatment: for odd $n$ the middle symbol $s[(n-1)/2]$ is its own mirror and is never compared.

**Cost model.** In the [comparison model](/comparison-model/) the cost is the number of equality tests $s[i] = s[j]$ between two positions. Time on a [word RAM](/word-ram/) is the number of steps; it is $\Theta(n)$ for the scan below.

## Variants

- **Normalized test.** Before the test, map the string to a normal form, for example lower case with spaces and punctuation removed. The phrase `Never odd or even` passes only after this step. The normal form is part of the problem statement and must be stated.
- **All prefixes, online.** Read $s$ one symbol at a time and, after each symbol, say whether the prefix read so far is a palindrome. This is the problem of Manacher's 1975 paper, which finds the smallest initial palindrome online. Galil (1976) made it real-time: a constant number of steps after each symbol.
- **Streaming with little memory.** Read $s$ once and keep little memory. A deterministic algorithm needs $\Omega(n)$ memory (see Bounds). A randomized one keeps two [polynomial hashes](/polynomial-rolling-hash/), one of the prefix read forward and one read backward, and answers correctly with high probability in $O(\log n)$ memory words.
- **Queries on substrings.** Many questions "is $s[i..j]$ a palindrome?" on one string. Preprocessing in $O(n)$ time gives $O(1)$ time per query: see [palindrome substring queries](/palindrome-substring-queries/).
- **Other symmetries.** In DNA the test is against the reverse complement: see [reverse-complement palindrome](/reverse-complement-palindrome/).

## Examples

The scan compares $s[i]$ with $s[n-1-i]$ for $i = 0, 1, \ldots$ and stops at the first mismatch.

| $s$ | $n$ | pairs compared | comparisons | answer |
| --- | --- | --- | --- | --- |
| $\varepsilon$ | 0 | none | 0 | YES |
| `a` | 1 | none | 0 | YES |
| `abba` | 4 | (0, 3) a = a, (1, 2) b = b | 2 | YES |
| `racecar` | 7 | (0, 6) r = r, (1, 5) a = a, (2, 4) c = c | 3 | YES |
| `abca` | 4 | (0, 3) a = a, (1, 2) b $\ne$ c | 2 | NO |
| `abcbba` | 6 | (0, 5) a = a, (1, 4) b = b, (2, 3) c $\ne$ b | 3 | NO |
| `ab` | 2 | (0, 1) a $\ne$ b | 1 | NO |

For `racecar` the middle symbol `e` at index 3 is never compared.

## Known algorithms

**Two-pointer scan.** This is the [two-pointers](/two-pointers/) technique with the pointers moving toward each other.

```pseudo id=two-pointer
IS-PALINDROME(s)                    ▷ s[0 .. n − 1]
L1  i ← 0, j ← n − 1
L2  while i < j do
L3      if s[i] ≠ s[j] then return NO
L4      i ← i + 1, j ← j − 1
L5  return YES
```

*Correctness.* Before each test of line L2, $j = n - 1 - i$ and $s[k] = s[n-1-k]$ for all $k < i$. This holds at the start ($i = 0$), and line L4 keeps it after a successful test in line L3. The loop runs while $i < n - 1 - i$, that is, while $i < (n-1)/2$, so it stops with $i = \lfloor n/2 \rfloor$, and by then all the pairs of the definition are equal. A NO from line L3 is a pair that differs. *Cost.* The quantity $j - i$ drops by 2 at each round, so there are at most $\lfloor n/2 \rfloor$ rounds and comparisons, and $O(1)$ extra space.

**Other ways.**

- Build $s^R$ and test $s = s^R$ with a [string equality test](/string-equality-testing/): $\Theta(n)$ time, $\Theta(n)$ extra space, up to $n$ comparisons.
- Compare polynomial hashes of $s$ and of $s^R$: $O(n)$ time, a one-sided error (a false YES) with small probability.
- [Manacher's algorithm](/manacher/) answers the test for every prefix and every substring at once, in $O(n)$ time; the plain test is the case "is the maximal palindrome at the center $(n-1)/2$ of length $n$".

## Bounds

**Upper bound.** The two-pointer scan uses at most $\lfloor n/2 \rfloor$ equality comparisons and $\Theta(n)$ time in the worst case, which is a palindrome. On a string whose first and last symbols differ it stops after one comparison.

**Lower bound in the comparison model.** Let $|\Sigma| \ge 2$ and let $A$ be a deterministic algorithm that learns about $s$ only from tests "$s[i] = s[j]$?". Then $A$ makes at least $\lfloor n/2 \rfloor$ tests on the input $a^n$.

*Proof.* On $a^n$ every test answers "equal". Let $G$ be the graph on the positions $0, \ldots, n-1$ with an edge $\{i, j\}$ for each test that $A$ makes on $a^n$, and suppose that $G$ has fewer than $\lfloor n/2 \rfloor$ edges. Each edge lowers the number of connected components by at most one, so $G$ has more than $n - \lfloor n/2 \rfloor = \lceil n/2 \rceil$ components. Group the positions into the $\lceil n/2 \rceil$ mirror classes $\{i, n-1-i\}$. If each component of $G$ were a union of mirror classes, there would be at most $\lceil n/2 \rceil$ components. So some position $i$ and its mirror $n-1-i \ne i$ are in different components. Let $C$ be the component of $i$, and let $s'$ have the symbol $b \ne a$ at the positions of $C$ and $a$ elsewhere. Each test that $A$ makes on $a^n$ compares two positions joined by an edge, so the two positions are in the same component, and the answer on $s'$ is also "equal". So $A$ runs the same way on $s'$ and on $a^n$ and gives the same answer. But $a^n$ is a palindrome and $s'$ is not, because $s'[i] = b \ne a = s'[n-1-i]$. This is a contradiction. $\blacksquare$

So the scan is exactly optimal in the worst case. In a model that reads symbols one at a time, the same idea shows that each position except the middle must be read on a palindrome input, so $2\lfloor n/2 \rfloor$ reads are needed, and the scan uses that many.

**Streaming memory.** Let $n$ be even and $\Sigma = \{a, b\}$. A deterministic one-pass algorithm must be in different memory states after the $2^{n/2}$ different first halves $u$: if two first halves $u \ne u'$ led to the same state, then the inputs $u u^R$ (a palindrome) and $u' u^R$ (not a palindrome, since its first half is not the reversal of its second half) would get the same answer. So it needs at least $n/2$ binary memory cells.

**Turing machines.** Hennie (1965) proved, with crossing sequences, that a one-tape Turing machine needs $\Omega(n^2)$ steps to recognize palindromes, and the obvious zig-zag machine reaches $O(n^2)$. A [multitape Turing machine](/multitape-turing-machine/) copies the input to a second tape and compares it backwards in $O(n)$ steps. Galil (1976) showed that the online version, a verdict after each symbol, can be done in real time.

**Languages.** The palindromes over two or more symbols form a [context-free language](/context-free-language/) that is not regular, so no finite automaton recognizes them. The [palindrome](/palindrome/) page gives the grammar and the proof.

## Reductions

- **To string equality.** $s$ is a palindrome if and only if $s = s^R$. Building $s^R$ costs $O(n)$.
- **To the longest palindromic substring.** $s$ is a palindrome if and only if its [longest palindromic substring](/longest-palindromic-substring/) has length $n$. So recognition is no harder than that problem, and any lower bound for recognition holds for it.
- **To substring queries.** Recognition is one [palindrome substring query](/palindrome-substring-queries/) with $i = 0$ and $j = n - 1$.

## Applications

- **Word games and normalization.** Checking palindromic words and phrases, with an explicit normalization step.
- **A step of other algorithms.** The expand-around-center method for the [longest palindromic substring](/longest-palindromic-substring/) is the two-pointer scan run outward from each center. The backtracking of [palindrome partitioning](/palindrome-partition-backtracking/) tests many substrings.
- **Teaching lower bounds.** The problem shows an exact comparison lower bound, a memory lower bound for streams, and a time separation between one-tape and multitape Turing machines.
- **Biology.** The reverse-complement version finds restriction sites in DNA.

## References
