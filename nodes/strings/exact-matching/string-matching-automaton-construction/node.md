---
tag: HCTKVB
kind: algorithm
slug: string-matching-automaton-construction
name: Computing the string-matching automaton transition function
aliases:
- Computing the transition function
area: strings/exact-matching
level: core
summary: Builds the finite automaton for a pattern by computing, for each state and character, the longest pattern prefix that is a suffix of the input read.
model: word-ram
complexity:
  vars: {m: the length of the pattern, σ: the alphabet size}
  time: {worst: Θ(mσ), best: Θ(mσ)}
  space: {extra: Θ(mσ)}
properties: {deterministic: true, recursive: false}
prereqs: [string-matching-automaton, prefix-function, deterministic-finite-automaton]
see_also: [morris-pratt, knuth-morris-pratt, aho-corasick, suffix-automaton-construction]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 32.3, String matching with finite automata (COMPUTE-TRANSITION-FUNCTION in O(m^3 |Σ|) time), and the exercise of Section 32.4 that computes the transition function in O(m |Σ|) time from the prefix function
  - url: http://www-igm.univ-mlv.fr/~lecroq/string/node4.html
    title: Christian Charras and Thierry Lecroq, Exact String Matching Algorithms, 1997
    locator: Deterministic Finite Automaton algorithm (the function preAut, which copies the row of the lagging state, O(mσ) time and space)
  - paper: doi:10.1137/0206024
    title: D. E. Knuth, J. H. Morris and V. R. Pratt, Fast pattern matching in strings, SIAM Journal on Computing 6(2) (1977), 323-350
    locator: the failure function f, which gives the row of the automaton that a state copies
---

This algorithm computes the transition table $\delta$ of the [string-matching automaton](/string-matching-automaton/) of a pattern $P$ of length $m$ over an alphabet of $\sigma$ characters, in $\Theta(m\sigma)$ time. Each entry $\delta[q][c]$ is the length of the longest prefix of $P$ that is a suffix of $P[0 \ldots q-1]\,c$. The fast method fills row $q$ by copying the row of a lagging state, the state that the automaton reaches on $P[1 \ldots q-1]$, and changing one entry; the direct method of CLRS takes $O(m^3\sigma)$ time.

## In plain words

The table answers: if I have just matched the first $q$ letters of the word and the next letter is $c$, how much of the word is matched now? If $c$ is the next letter of the word, the answer is $q + 1$. Otherwise the answer is the same as for a shorter situation: the one where the first letter of the match is dropped.

So the method keeps a second, lagging position: the state the automaton would be in after reading the word without its first letter. That state is always smaller than $q$, so its row is already filled. Row $q$ is a copy of the lagging row, except for the one letter that continues the word. Then the lagging state moves forward by one letter of the word, using the table itself.

## The problem

The input is a pattern $P[0 \ldots m-1]$ over an integer alphabet $\Sigma = \{0, \ldots, \sigma - 1\}$, so a character can index an array. Indices are 0-based. The output is the table $\delta[0 \ldots m][0 \ldots \sigma-1]$ with $\delta[q][c] = \sigma_P(P[0 \ldots q-1]\,c)$, where the suffix function $\sigma_P(w)$ is the length of the longest prefix of $P$ that is a suffix of $w$. For $m = 0$ the table is one row of zeros. The automaton with this table is used to solve [string matching](/string-matching/), with overlapping occurrences reported.

## The algorithm

```pseudo id=main
COMPUTE-TRANSITION-FUNCTION(P, σ)
L1  m ← |P|, δ[q][c] ← 0 for all 0 ≤ q ≤ m and 0 ≤ c < σ
L2  if m > 0 then δ[0][P[0]] ← 1
L3  X ← 0                                ▷ X = σ_P(P[1 .. q − 1]), the lagging state
L4  for q ← 1 to m do
L5      for c ← 0 to σ − 1 do
L6          δ[q][c] ← δ[X][c]
L7      if q < m then
L8          δ[q][P[q]] ← q + 1
L9          X ← δ[X][P[q]]
L10 return δ
```

Row 0 sends $P[0]$ to state 1 and everything else to 0. For $q \ge 1$, lines L5 and L6 copy row $X$, and line L8 overwrites the one forward transition. Line L9 moves the lagging state over the next pattern character with the table. The lagging state for $q$ equals $\pi[q-1]$, the [prefix function](/prefix-function/) value, so the algorithm also computes $\pi$ as a by-product, without any character comparison of the pattern with itself.

## Example

$P$ = ababaca over $\Sigma$ = {a, b, c}, the pattern used in CLRS. The column $X$ is the lagging state used for row $q$.

| $q$ | $X$ | copied row $\delta[X]$ (a, b, c) | forward entry | row $\delta[q]$ (a, b, c) |
|---|---|---|---|---|
| 0 | | | a to 1 | 1, 0, 0 |
| 1 | 0 | 1, 0, 0 | b to 2 | 1, 2, 0 |
| 2 | 0 | 1, 0, 0 | a to 3 | 3, 0, 0 |
| 3 | 1 | 1, 2, 0 | b to 4 | 1, 4, 0 |
| 4 | 2 | 3, 0, 0 | a to 5 | 5, 0, 0 |
| 5 | 3 | 1, 4, 0 | c to 6 | 1, 4, 6 |
| 6 | 0 | 1, 0, 0 | a to 7 | 7, 0, 0 |
| 7 | 1 | 1, 2, 0 | none | 1, 2, 0 |

The lagging states $0, 0, 1, 2, 3, 0, 1$ for $q = 1, \ldots, 7$ are the prefix function of ababaca. At $q = 5$, the matched part is ababa; dropping the first letter gives baba, on which the automaton reaches state 3 (aba). So a b after ababa leads where a b after aba leads, to state 4, while c continues the pattern to state 6. The final row, for the full match, copies row 1: after ababaca, a b gives ab and an a gives a.

## Correctness

Let $X_q = \sigma_P(P[1 \ldots q-1])$. If $c$ is not the next pattern character (or $q = m$), no prefix of $P$ of length $q + 1$ ends the string $P[0 \ldots q-1]\,c$, so every candidate is a suffix of $P[1 \ldots q-1]\,c$, the string without its first letter. By the suffix-function recursion of the [automaton](/string-matching-automaton/), $\sigma_P(P[1 \ldots q-1]\,c) = \delta[X_q][c]$, and $X_q < q$, so that row is ready. The same recursion gives $X_{q+1} = \delta[X_q][P[q]]$, which is line L9. The full proof is below.

## Complexity

- **Time.** Line L1 initializes $(m + 1)\sigma$ entries, and lines L5 and L6 copy $m$ rows of $\sigma$ entries. Lines L2, L8 and L9 cost $O(1)$ per row. The total is $\Theta(m\sigma)$, in the best and the worst case, because every entry of the output is written.
- **Space.** $\Theta(m\sigma)$ for the table, which is the output; $O(1)$ more.
- **The direct method.** CLRS compute each entry by trying $k = \min(m, q+1), \ldots, 0$ and testing whether $P[0 \ldots k-1]$ is a suffix of $P[0 \ldots q-1]\,c$, which costs $O(m)$ per test, so $O(m^3\sigma)$ in total. CLRS note that it can be improved to $O(m\sigma)$ with the prefix function, which is what this page does.

| method | time |
|---|---|
| direct (CLRS Section 32.3) | $O(m^3\sigma)$ |
| lagging state (this page) | $\Theta(m\sigma)$ |
| from the prefix function | $\Theta(m\sigma)$ after $O(m)$ |

## Properties

- **Integer alphabet.** Characters index the rows, so the alphabet must be $\{0, \ldots, \sigma-1\}$ or mapped to it.
- **No pattern comparisons.** The method never compares two pattern characters; all the information comes through table lookups. The prefix function falls out as the sequence of lagging states.
- **Incremental.** Row $q$ depends only on $P[0 \ldots q]$ and on earlier rows, so appending a character to the pattern costs $\Theta(\sigma)$ for one new row.

## Variants and improvements

- **From the prefix function.** Compute $\pi$ first, then set $\delta[q][c] = q + 1$ if $c = P[q]$, and $\delta[\pi[q-1]][c]$ otherwise, for $q \ge 1$. This is the same as the lagging state, since $X_q = \pi[q-1]$.
- **Compact automata.** Store only the forward edges and the failure function, which is [Morris-Pratt](/morris-pratt/), or only the transitions that do not go to state 0, at most $2m$ of them (Simon's construction).
- **Many patterns.** The same lagging-state idea, along the failure links of a trie, builds the automaton of [Aho-Corasick](/aho-corasick/).
- **All factors.** The [suffix automaton construction](/suffix-automaton-construction/) builds an automaton for every substring of a string, in linear time.

## When to use it

Use it when you want the full table, for a pattern over a small alphabet that will be searched in a long stream with constant time per character. For a large alphabet, do not build the full table: use [KMP](/knuth-morris-pratt/), or limit the columns to the characters that occur in $P$ plus one column for all others.

## Pitfalls

- **Copying a reference instead of a row.** In Python, `delta[q] = delta[x]` makes two rows the same list, so line L8 then changes row $X$ too. Copy the row. The test `test_table_against_naive` compares every table with the direct method.
- **The row of state $m$.** Line L4 must run to $q = m$. Without row $m$, the automaton cannot continue after a full match, and overlapping occurrences are lost.
- **Moving the lagging state too early.** Line L9 must run after row $q$ is filled, since $X$ can equal $q - 1$ and line L9 reads row $X$. Moving it before line L5 copies the wrong row; for $P$ = aa, row 1 would copy row 1 itself.
- **Pattern of length 0.** Line L2 must not read $P[0]$ when $m = 0$. The test `test_edges` builds the table of the empty pattern.

## Implementations

## History

The direct construction appears in CLRS, where the automaton is presented before the Knuth-Morris-Pratt algorithm, and a linear-in-$m\sigma$ construction from the prefix function is left as an exercise there. Knuth, Morris and Pratt (1977) obtained their failure function as a compact form of the same automaton. The lagging-state formulation is the one given by Charras and Lecroq in their handbook of exact string matching algorithms.

## References
