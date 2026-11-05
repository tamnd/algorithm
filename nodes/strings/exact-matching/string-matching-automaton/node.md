---
tag: 3VKE1X
kind: data-structure
slug: string-matching-automaton
name: String-matching automaton
aliases:
- KMP automaton
- pattern-matching automaton
area: strings/exact-matching
level: core
summary: A DFA over the alphabet whose state is the longest pattern prefix matching the current text suffix; one transition per text character.
solves: [string-matching]
model: word-ram
complexity:
  vars: {n: the length of the text, m: the length of the pattern, σ: the alphabet size}
  time: {build: Θ(mσ), step: O(1), search: Θ(n)}
  space: {extra: Θ(mσ)}
properties: {deterministic: true, recursive: false, online: true}
prereqs: [deterministic-finite-automaton, prefix-function, string-matching]
see_also: [string-matching-automaton-construction, knuth-morris-pratt, morris-pratt, aho-corasick, suffix-automaton, alphabet]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 32.3, String matching with finite automata (the suffix function, FINITE-AUTOMATON-MATCHER, the lemmas on the suffix function and the correctness theorem)
  - url: http://www-igm.univ-mlv.fr/~lecroq/string/node4.html
    title: Christian Charras and Thierry Lecroq, Exact String Matching Algorithms, 1997
    locator: Deterministic Finite Automaton algorithm (construction in O(mσ) time and space, search in O(n) time, each text character inspected once)
  - paper: doi:10.1137/0206024
    title: D. E. Knuth, J. H. Morris and V. R. Pratt, Fast pattern matching in strings, SIAM Journal on Computing 6(2) (1977), 323-350
    locator: the discussion of the pattern-matching machine and of its failure links as a compact form of the automaton
---

The string-matching automaton of a pattern $P$ of length $m$ is a [deterministic finite automaton](/deterministic-finite-automaton/) with states $0, \ldots, m$ in which, after reading any text, the state is the length of the longest prefix of $P$ that is a suffix of the text read. It accepts exactly when the state is $m$, so running it over a text $T$ reports every occurrence of $P$ with one table lookup per text character. The table has $(m + 1)\sigma$ entries and is built in $\Theta(m\sigma)$ time by [the construction algorithm](/string-matching-automaton-construction/).

## In plain words

Imagine a counter that says how much of the word you have just seen at the end of what you read. A new letter either makes the counter grow by one, or it breaks the match, and then the counter drops to some smaller value.

The automaton is a table that gives this new value in advance, for every counter value and every letter. Searching is then trivial: read the text, look up the next counter value in the table for each letter, and report a match whenever the counter equals the length of the word.

The table costs memory for every pair of counter value and letter, so it fits small alphabets best, such as DNA or bytes with a short word.

## The abstract type

The structure stores a fixed pattern $P[0 \ldots m-1]$ over an integer [alphabet](/alphabet/) $\Sigma = \{0, \ldots, \sigma - 1\}$. Indices are 0-based. Define the suffix function $\sigma_P(w)$ of a string $w$ as the length of the longest prefix of $P$ that is a suffix of $w$. The operations are:

- **build$(P)$**: create the automaton.
- **step$(q, c)$**: for a state $q = \sigma_P(w)$, return $\sigma_P(wc)$.
- **search$(T)$**: return every shift $s$, $0 \le s \le n - m$, with $T[s \ldots s+m-1] = P$, in increasing order. Occurrences may overlap. For $m = 0$ the output is all shifts $0, \ldots, n$, and for $m > n$ it is empty.

## Representation

- A table $\delta[0 \ldots m][0 \ldots \sigma - 1]$ of integers in $\{0, \ldots, m\}$, with $\delta[q][c] = \sigma_P(P[0 \ldots q-1]\,c)$.
- The accepting state $m$.

For a general alphabet, map the distinct characters of $P$ to columns $0, \ldots, k-1$ with $k \le m$, and use one extra column for every other character: such a character occurs nowhere in $P$, so it sends every state to 0. The implementation does this with a hash map, so a step costs $O(1)$ expected time.

Row $q$ differs from row $\pi[q-1]$ only in the column $P[q]$, where $\pi$ is the [prefix function](/prefix-function/). So most of the table repeats earlier rows, which is what the compact representations below exploit.

## Operations

```pseudo id=main
AUTOMATON-SEARCH(T, δ, m)                ▷ δ built by COMPUTE-TRANSITION-FUNCTION(P)
L1  m ← the accepting state of δ
L2  if m = 0 then output 0, 1, …, |T| and return
L3  q ← 0                                ▷ q = σ_P(T[0 .. i − 1])
L4  for i ← 0 to |T| − 1 do
L5      q ← δ[q][T[i]]                   ▷ step(q, T[i])
L6      if q = m then
L7          output i − m + 1
```

Build is the algorithm of the page [string-matching automaton construction](/string-matching-automaton-construction/): row 0 sends $P[0]$ to 1 and everything else to 0, and row $q$ copies the row of the state $X$ reached on $P[1 \ldots q-1]$, then sets the column $P[q]$ to $q + 1$. Step is one lookup. Search, lines L1 to L7, applies step to each text character and reports the accepting states. After a full match, no special case is needed: row $m$ already sends the state to the right shorter prefix.

## Example

$P$ = ababaca over $\Sigma$ = {a, b, c}, the example of CLRS. The table:

| state $q$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| matched $P[0 \ldots q-1]$ | | a | ab | aba | abab | ababa | ababac | ababaca |
| $\delta[q][$a$]$ | 1 | 1 | 3 | 1 | 5 | 1 | 7 | 1 |
| $\delta[q][$b$]$ | 0 | 2 | 0 | 4 | 0 | 4 | 0 | 2 |
| $\delta[q][$c$]$ | 0 | 0 | 0 | 0 | 0 | 6 | 0 | 0 |

The run on $T$ = abababacaba:

| $i$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| $T[i]$ | a | b | a | b | a | b | a | c | a | b | a |
| state after | 1 | 2 | 3 | 4 | 5 | 4 | 5 | 6 | 7 | 2 | 3 |

The state reaches 7 at $i = 8$, so the output is the shift $8 - 7 + 1 = 2$. At $i = 5$, the text read ends with ababab: the prefix ababa cannot be extended by b, but its border abab can, so $\delta[5][$b$] = 4$. [Morris-Pratt](/morris-pratt/) finds the same state by following the border chain; the automaton has the answer in one step. In state 7, a b leads to state 2, because the text then ends with ab, and an a leads to state 1.

## Correctness

The key fact is the suffix-function recursion: if $q = \sigma_P(w)$, then $\sigma_P(wc) = \sigma_P(P[0 \ldots q-1]\,c)$. Every prefix of $P$ that is a suffix of $wc$ has length at most $q + 1$, so it is a suffix of $P[0 \ldots q-1]\,c$, which is itself a suffix of $wc$. So $\delta[q][c]$ is exactly step$(q, c)$, and by induction the state after reading $T[0 \ldots i]$ is $\sigma_P(T[0 \ldots i])$. That value equals $m$ exactly when $P$ ends at position $i$. The full proof is below.

## Complexity

| operation | time | notes |
|---|---|---|
| build | $\Theta(m\sigma)$ | each of the $(m+1)\sigma$ entries is written once |
| step | $O(1)$ | one table lookup |
| search | $\Theta(n)$ | exactly one step per text character |
| space | $\Theta(m\sigma)$ | the table |

The search time does not depend on the pattern at all: each character costs one step, the best possible real-time behavior. The cost moves to the table, which is too large for big alphabets: Unicode with a pattern of 100 characters would need millions of entries. With the hash-map columns of the implementation, the table has at most $(m+1)(m+1)$ entries, but a step costs a hash lookup.

## Variants

- **Failure links instead of a table.** Store only the forward edge of each state and the [prefix function](/prefix-function/). This is [Morris-Pratt](/morris-pratt/) and, with the strong failure table, [Knuth-Morris-Pratt](/knuth-morris-pratt/): $\Theta(m)$ space, amortized $O(1)$ per character instead of worst-case $O(1)$.
- **Sparse table.** Simon observed that the automaton has at most $2m$ transitions that do not lead to state 0, so storing only those gives $O(m)$ space and a search with a list lookup per character (Charras and Lecroq list this as Simon's algorithm).
- **Many patterns.** The automaton of [Aho-Corasick](/aho-corasick/) is the same construction on a trie of patterns.
- **All factors.** The [suffix automaton](/suffix-automaton/) recognizes every substring of a text instead of one pattern; it is the structure behind [backward DAWG matching](/backward-dawg-matching/).
- **Bit-parallel simulation.** [Shift-Or](/shift-or/) simulates the nondeterministic version of the automaton, where all partial matches are active at once, with one word per state set.

## When to use it

Use the automaton when the alphabet is small and the text is a stream in which each character must be handled in constant time, such as a hardware or network filter, or when the same pattern is searched in a very long text. For one search with a large alphabet, [KMP](/knuth-morris-pratt/) has the same total time with $\Theta(m)$ space, and a [Boyer-Moore](/boyer-moore/) variant is faster on average.

## Pitfalls

- **The row of state $m$.** The table needs a row for state $m$, and it must not reset to 0, or overlapping occurrences are lost. The test `test_edges` searches aaaa in $a^{10}$ and expects 7 shifts.
- **Characters outside the alphabet.** A raw array indexed by character code fails or reads garbage for a character with no column. The implementation maps every unknown character to one column of zeros; the test `test_states_are_sigma` reads the letter z, which is in no pattern.
- **Memory for large alphabets.** A full table over 16-bit characters with a long pattern can need hundreds of megabytes. Restrict the columns to the characters of the pattern.
- **The empty pattern.** The automaton has only state 0, which is accepting, so every shift $0, \ldots, n$ is an occurrence, including the one before any character is read. Line L2 handles it.

## Implementations

## History

Matching with a finite automaton is the direct application of the theory of finite automata of the 1950s and 1960s, and the textbook construction appears in CLRS. Knuth, Morris and Pratt describe their algorithm as a pattern-matching machine and point out that its failure links represent the automaton compactly, so that it can be built in time independent of the alphabet. Aho and Corasick extended the automaton to many patterns in 1975, and Simon showed in the 1990s that the single-pattern automaton has only $O(m)$ significant transitions.

## References
