---
tag: 7DN50X
kind: concept
slug: prefix-function
name: Prefix function (failure function)
aliases:
- failure function
- border array
- pi array
area: strings/exact-matching
level: core
summary: For each prefix, the length of its longest proper border.
prereqs: [border, string-period, amortized-cost]
see_also: [knuth-morris-pratt, morris-pratt, prefix-occurrence-counting, z-algorithm, string-matching-automaton-construction, failure-link, string-compression-by-period]
sources:
  - url: https://cp-algorithms.com/string/prefix-function.html
    title: CP-Algorithms, Prefix function. Knuth-Morris-Pratt algorithm
    locator: the definition, the trivial and the efficient algorithms, and the applications
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 32.4, The Knuth-Morris-Pratt algorithm (the prefix function, COMPUTE-PREFIX-FUNCTION, its amortized analysis and its correctness)
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Section 2.3 (the values sp and sp' of KMP) and Section 3.3 (the original preprocessing for Knuth-Morris-Pratt)
  - paper: doi:10.1137/0206024
    title: D. E. Knuth, J. H. Morris and V. R. Pratt, Fast pattern matching in strings, SIAM Journal on Computing 6(2) (1977), 323-350
    locator: the failure function f and the next table, and their computation in linear time
---

The prefix function of a string $P$ gives, for each prefix of $P$, the length of its longest proper [border](/border/): the longest proper prefix of that prefix that is also its suffix. It can be computed for all $m$ prefixes in $O(m)$ time with at most $2m$ character comparisons. It is the table behind [Morris-Pratt](/morris-pratt/) and [Knuth-Morris-Pratt](/knuth-morris-pratt/) matching, where it says how far the pattern can move after a mismatch, and it also gives the [period](/string-period/) of every prefix.

## In plain words

Take a word and look at its first few letters. Sometimes the same letters also end the word: in "abacab", the start "ab" is also the end. Such a part is called a border. The prefix function records, for each starting piece of a word, how long its longest border is, without counting the whole piece.

Why is this useful? When you search for a word in a text and a letter does not match, the part that matched is a starting piece of the word. Its longest border tells you the longest piece that can still be the start of a new match. So you can continue from there, and you never need to read the text again.

The whole table can be built in one pass over the word.

## The idea

**Definition.** Let $P = P[0 \ldots m-1]$ be a string over any alphabet. Indices are 0-based. A string $u$ is a *border* of $x$ when $u$ is both a prefix and a suffix of $x$. A border is *proper* when $|u| < |x|$. The empty string is a proper border of each non-empty string. The prefix function of $P$ is the array $\pi[0 \ldots m-1]$ with

$$\pi[q] = \max\{\, k : 0 \le k \le q \text{ and } P[0 \ldots k-1] = P[q-k+1 \ldots q] \,\},$$

the length of the longest proper border of the prefix $P[0 \ldots q]$ of length $q + 1$. So $\pi[0] = 0$ always. Some texts index by the length of the prefix instead, with $\pi[q]$ for $P[0 \ldots q-1]$, or store $-1$ at index 0; the values are the same up to this shift.

**Borders and periods.** A string $x$ of length $\ell$ has a border of length $b$ exactly when $p = \ell - b$ is a period of $x$, that is $x[i] = x[i + p]$ for each $0 \le i < \ell - p$. Both conditions say $x[0 \ldots b-1] = x[\ell - b \ldots \ell - 1]$. So the smallest period of $P[0 \ldots q]$ is $q + 1 - \pi[q]$.

**Lemma 1 (border of a border).** If $u$ is a border of $x$ and $v$ is a border of $x$ with $|v| < |u|$, then $v$ is a border of $u$. Conversely, a border of a border of $x$ is a border of $x$.

*Proof.* $v$ and $u$ are both prefixes of $x$ and $|v| < |u|$, so $v$ is a prefix of $u$. They are both suffixes of $x$, so $v$ is a suffix of $u$. For the converse, if $v$ is a prefix of $u$ and $u$ is a prefix of $x$, then $v$ is a prefix of $x$, and the same holds for suffixes. $\square$

**Lemma 2 (the chain of borders).** The lengths of all borders of $P[0 \ldots q]$, other than the whole prefix, are $\pi[q], \pi^{(2)}[q], \ldots, 0$, where $\pi^{(i+1)}[q] = \pi[\pi^{(i)}[q] - 1]$ while $\pi^{(i)}[q] > 0$.

*Proof.* By induction on the length. The longest proper border has length $\pi[q]$ by definition. By Lemma 1, the proper borders of $P[0 \ldots q]$ shorter than $k > 0$, where $k$ is a border length, are exactly the proper borders of the border $P[0 \ldots k-1]$, and the longest of them has length $\pi[k-1]$. The lengths strictly decrease, so the chain reaches 0. $\square$

**Lemma 3 (extension).** For $q \ge 1$, $\pi[q] = k + 1$, where $k$ is the largest border length of $P[0 \ldots q-1]$ (proper, so $k \le q - 1$) with $P[k] = P[q]$; and $\pi[q] = 0$ if no such $k$ exists.

*Proof.* If $P[0 \ldots j]$ is a proper border of $P[0 \ldots q]$ with $j \ge 0$, then $P[0 \ldots j-1]$ is a border of $P[0 \ldots q-1]$ of length $j \le q - 1$, and $P[j] = P[q]$. Conversely, a border of length $k$ of $P[0 \ldots q-1]$ with $P[k] = P[q]$ gives a proper border of length $k + 1 \le q$ of $P[0 \ldots q]$. So the non-empty proper borders of $P[0 \ldots q]$ are exactly the extensions, and the longest one comes from the largest $k$. $\square$

In particular $\pi[q] \le \pi[q-1] + 1$: the value grows by at most one at each step.

**Computation.** Lemmas 2 and 3 give the algorithm: try the border lengths of $P[0 \ldots q-1]$ from the longest down, along the chain, and stop at the first $k$ with $P[k] = P[q]$.

```pseudo id=main
COMPUTE-PREFIX-FUNCTION(P)
L1  m ← |P|, π[0] ← 0, k ← 0          ▷ k = π[q − 1]
L2  for q ← 1 to m − 1 do
L3      while k > 0 and P[k] ≠ P[q] do
L4          k ← π[k − 1]                ▷ next shorter border
L5      if P[k] = P[q] then k ← k + 1
L6      π[q] ← k
L7  return π
```

**Cost.** The variable $k$ starts at 0, line L5 increases it by at most 1 per iteration of line L2, so by at most $m - 1$ in total, and it never becomes negative. Each pass of line L4 decreases $k$ by at least 1, because $\pi[k-1] \le k - 1$. So line L4 runs at most $m - 1$ times in total. This is an [amortized](/amortized-cost/) argument with the [potential](/potential-method/) $k$. Each pass of line L4 costs one comparison, and each iteration of line L2 costs one more comparison at line L5, so the total is at most $2(m - 1)$ comparisons and $O(m)$ time. Only equality tests are used, so the alphabet can be general, and the extra space is the array itself.

**The strong version.** Knuth, Morris and Pratt also use a stronger table, often written $\mathrm{next}$: the longest proper border $u$ of $P[0 \ldots q-1]$ such that the character after $u$ differs from $P[q]$. A mismatch at $P[q]$ then never tries the same character again. The plain prefix function is the table of [Morris-Pratt](/morris-pratt/), and the strong one is the table of [Knuth-Morris-Pratt](/knuth-morris-pratt/).

## Examples

**The prefix function of aabaaab.**

| $q$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| $P[q]$ | a | a | b | a | a | a | b |
| $\pi[q]$ | 0 | 1 | 0 | 1 | 2 | 2 | 3 |
| smallest period $q + 1 - \pi[q]$ | 1 | 1 | 3 | 3 | 3 | 4 | 4 |

For $q = 6$, the prefix is aabaaab. Its proper borders are aab and the empty string, with lengths $\pi[6] = 3$ and $\pi[\pi[6] - 1] = \pi[2] = 0$, as Lemma 2 says.

**A trace of the computation** on aabaaab. The column "chain" lists the values that $k$ takes at line L3.

| $q$ | $P[q]$ | chain of $k$ | comparisons | $\pi[q]$ |
|---|---|---|---|---|
| 1 | a | 0 | 1 | 1 |
| 2 | b | 1, 0 | 2 | 0 |
| 3 | a | 0 | 1 | 1 |
| 4 | a | 1 | 1 | 2 |
| 5 | a | 2, 1 | 2 | 2 |
| 6 | b | 2 | 1 | 3 |

At $q = 5$, the longest border of aabaa is aa, but $P[2]$ = b differs from $P[5]$ = a. The next border is $P[0 \ldots \pi[1] - 1]$ = a, and $P[1]$ = a matches, so $\pi[5] = 2$. The total is 8 comparisons, within the bound $2(m - 1) = 12$.

**More values.**

| $P$ | $\pi$ |
|---|---|
| abacabab | 0 0 1 0 1 2 3 2 |
| aaaaa | 0 1 2 3 4 |
| abcd | 0 0 0 0 |

For $a^m$ the value is $\pi[q] = q$, so every prefix has period 1. For a string with distinct characters, every value is 0.

**A non-example.** The whole prefix is a border of itself, but it is not proper, so it never counts: $\pi[q] \le q$, never $q + 1$. Counting it would make the search loop of KMP shift by zero and run forever.

## Where it is used

- [Morris-Pratt](/morris-pratt/) and [Knuth-Morris-Pratt](/knuth-morris-pratt/) matching: after a mismatch with $q$ characters matched, the pattern continues with $\pi[q - 1]$ characters matched.
- [The string-matching automaton](/string-matching-automaton-construction/): its transition function is built in $O(m\sigma)$ time from the prefix function.
- [Counting the occurrences of each prefix](/prefix-occurrence-counting/) in a string, by summing along the border chains.
- The [period](/string-period/) of a string is $m - \pi[m-1]$, and the string is a power $u^k$ with $k \ge 2$ exactly when this period divides $m$ and is less than $m$. See [compression by period](/string-compression-by-period/).
- The [failure links](/failure-link/) of [Aho-Corasick](/aho-corasick/) are the prefix function generalized to a trie of many patterns.
- [String matching](/string-matching/) by one call: compute the prefix function of $P \# T$, with a separator $\#$ not in the alphabet, and report the positions where the value equals $m$.

## References
