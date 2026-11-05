---
tag: BAZPF7
kind: data-structure
slug: subsequence-automaton
name: Subsequence automaton
aliases:
- subsequence DFA
- next-occurrence table
area: sequences/subsequence-problems
level: advanced
summary: A linear-size automaton that answers subsequence queries against many patterns in time linear in pattern length.
implements: []
model: word-ram
complexity:
  vars: {n: the length of the text, σ: the alphabet size, k: the length of the pattern}
  time: {worst: Θ(k)}
  space: {extra: Θ(n σ)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [subsequence-checking, deterministic-finite-automaton]
see_also: [subsequence, distinct-subsequences, suffix-automaton, trie, binary-search, longest-common-subsequence]
sources:
  - paper: "Ricardo A. Baeza-Yates, Searching subsequences, Theoretical Computer Science 78(2), 1991, 363-376"
    locator: the automaton that recognizes all subsequences of a text, its construction and its use to test many patterns against one text
  - paper: "Maxime Crochemore, Bořivoj Melichar and Zdeněk Troníček, Directed acyclic subsequence graph: overview, Journal of Discrete Algorithms 1(3-4), 2003, 255-280"
    locator: the directed acyclic subsequence graph of one text and of a set of texts, its construction and its size
---

The subsequence automaton of a text $T$ of length $n$ is a [deterministic finite automaton](/deterministic-finite-automaton/) with states $0, 1, \ldots, n$ that accepts exactly the [subsequences](/subsequence/) of $T$. From state $i$, the letter $c$ leads to the first position after $i$ where $c$ occurs in $T$, so the automaton stores a next-occurrence table of $(n + 1) \sigma$ entries for an alphabet of size $\sigma$. After this table is built, in $\Theta(n \sigma)$ time, the question "is $P$ a subsequence of $T$?" takes one table lookup for each letter of $P$, independent of $n$. Baeza-Yates described it in 1991; with a set of texts it is also called the directed acyclic subsequence graph.

## In plain words

To check if a short word is hidden in a long text, with gaps allowed, you look for its first letter, then for its second letter after that, and so on. Done by hand, each search scans the text.

The automaton does all these searches in advance. For each place in the text and each letter, it writes down where that letter next appears. Then a check only follows the notes: start at the beginning, look up the next place of each letter of the word, and jump there. If a lookup says "no more", the word is not hidden in the text. The cost of a check depends on the length of the word, not of the text, which pays off when many words are checked against one text.

## The abstract type

The structure is built once from a text $T = t_1 \cdots t_n$ over an alphabet $\Sigma$ of size $\sigma$ and does not change. It supports:

- **CONTAINS($P$).** Return true if and only if $P \preceq T$, that is, $P$ is a subsequence of $T$.
- **STEP($q$, $c$).** From a state $q$, which stands for the prefix $t_1 \cdots t_q$ already used, return the end of the leftmost occurrence of $c$ after it. With STEP, a caller can embed a pattern letter by letter, or stop and resume.
- **COUNT-DISTINCT.** Return the number of distinct subsequences of $T$, the empty one included.

It is the static, many-query form of [subsequence checking](/subsequence-checking/): the single test costs $\Theta(n)$ by a scan, and the automaton moves this cost into the preprocessing.

## Representation

The states are the integers $0, \ldots, n$, and all of them are accepting. The transition table is

$$\mathrm{nxt}[i][c] = \min\{ j : i < j \le n,\ t_j = c \},$$

or NIL if $c$ does not occur in $t_{i+1} \cdots t_n$. A NIL entry means that the automaton has no move, so it rejects. The table has $n + 1$ rows of $\sigma$ entries, each an integer in $[1, n]$ or NIL. Row $i - 1$ differs from row $i$ only in the entry of $t_i$, which is $i$. The letters are mapped to $0, \ldots, \sigma - 1$, for example by a hash table over the letters of $T$; a letter that is not in $T$ has no column, and its lookups give NIL.

The transitions only go from a state to a larger state, so the automaton is acyclic, and every state has at most $\sigma$ outgoing edges.

## Operations

```pseudo id=main
BUILD(T[1 .. n])
L1  nxt[n][c] ← NIL for each letter c
L2  for i ← n downto 1 do
L3      nxt[i − 1] ← a copy of nxt[i]
L4      nxt[i − 1][T[i]] ← i
L5  return nxt

CONTAINS(nxt, P[1 .. k])
L6  q ← 0
L7  for each letter c of P, in order do
L8      q ← nxt[q][c]                     ▷ NIL if c is not a letter of T
L9      if q = NIL then return false
L10 return true

COUNT-DISTINCT(nxt)
L11 for i ← n downto 0 do cnt[i] ← 1 + the sum of cnt[nxt[i][c]] over the letters c with nxt[i][c] ≠ NIL
L12 return cnt[0]
```

BUILD fills the rows from right to left: row $i - 1$ is row $i$ with the entry of $t_i$ set to $i$. CONTAINS runs the automaton on $P$. STEP($q$, $c$) is line L8 alone. COUNT-DISTINCT counts the paths that start at state $i$, since each path spells one distinct subsequence of $t_{i+1} \cdots t_n$.

## Example

Take $T = $ banana, with $n = 6$ and the letters a, b, n. The table, with a dash for NIL:

| state $i$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| a | 2 | 2 | 4 | 4 | 6 | 6 | - |
| b | 1 | - | - | - | - | - | - |
| n | 3 | 3 | 3 | 5 | 5 | - | - |

- **bnn.** From 0, b goes to 1, n to 3, n to 5. All three moves exist, so bnn $\preceq$ banana, embedded at positions 1, 3, 5.
- **nb.** From 0, n goes to 3, and $\mathrm{nxt}[3][\text{b}]$ is NIL. So nb is not a subsequence.
- **aaaa.** From 0 the a moves go to 2, 4, 6, and the fourth a finds NIL at state 6.
- **Counting.** From $\mathrm{cnt}[6] = 1$ down: $\mathrm{cnt}[5] = 2$, $\mathrm{cnt}[4] = 1 + 1 + 2 = 4$, $\mathrm{cnt}[3] = 1 + 4 + 2 = 7$, $\mathrm{cnt}[2] = 1 + 4 + 7 = 12$, $\mathrm{cnt}[1] = 1 + 12 + 7 = 20$ and $\mathrm{cnt}[0] = 1 + 12 + 20 + 7 = 40$. So banana has 40 distinct subsequences, the empty one included, the same number as the recurrence on the [distinct subsequences](/distinct-subsequences/) page gives.

## Correctness

The proof rests on one invariant: after CONTAINS has read $p_1 \cdots p_r$ without NIL, $q$ is the end of the leftmost embedding of $p_1 \cdots p_r$ in $T$, that is, the least $q$ such that $p_1 \cdots p_r \preceq t_1 \cdots t_q$. Each step takes the first occurrence of the next letter after $q$, which is the greedy choice of [subsequence checking](/subsequence-checking/); an exchange argument shows that an embedding that ends later cannot leave more room for the rest of $P$. If a lookup gives NIL, the letter does not occur after the least possible end, so it does not occur after any end, and $P \not\preceq T$. BUILD is correct by induction from row $n$ down: the first occurrence of $c$ after $i - 1$ is at $i$ if $t_i = c$, and otherwise it is the first occurrence after $i$. For COUNT-DISTINCT, the automaton is deterministic, so distinct words take distinct paths, and the words that can be read from state $i$ are the subsequences of $t_{i+1} \cdots t_n$. The proof file also shows that no deterministic automaton for the subsequences of $T$ has fewer states.

## Complexity

- **Build.** $n$ copies of a row of $\sigma$ entries: $\Theta(n \sigma)$ time and space, plus the time to map the letters.
- **Query.** CONTAINS does at most $k$ lookups of $O(1)$ time each on the [word RAM](/word-ram/): $O(k)$, and $\Theta(k)$ when $P \preceq T$. This does not depend on $n$.
- **Many queries.** $q$ patterns of total length $K$ cost $\Theta(n \sigma + K)$, against $\Theta(q n)$ worst-case time for $q$ separate scans.
- **Count.** COUNT-DISTINCT is $\Theta(n \sigma)$ additions, on numbers of up to $O(n \log \sigma)$ bits, since the count is at most $\sigma^{n+1}$.
- **Concrete size.** For a text of $10^6$ bytes over the 26 lowercase letters, the table has about $2.6 \times 10^7$ entries; with 4-byte entries this is about 100 MB. For the 256 byte values it is ten times more, which is the reason for the compact variant below.

## Variants

- **Position lists with binary search.** Store, for each letter $c$, the sorted list of its positions in $T$. STEP($q$, $c$) is the first entry of the list of $c$ that is larger than $q$, found by [binary search](/binary-search/). The lists have $n$ entries in all, so the space is $\Theta(n)$ for any alphabet, and a query costs $O(k \log n)$.
- **Online construction.** Appending a letter $c$ at position $n + 1$ sets $\mathrm{nxt}[i][c] = n + 1$ for the states $i$ from the previous occurrence of $c$ up to $n$, and adds an empty row. Each entry is written once, so the total is still $\Theta(n \sigma)$.
- **A set of texts.** The directed acyclic subsequence graph of Crochemore, Melichar and Troníček accepts the words that are a subsequence of at least one text of a set, or of all texts. Its states are sets of positions, one in each text, and its size can grow fast with the number of texts.
- **Shortest non-subsequence.** A shortest word that is not a subsequence of $T$ is a shortest path from state 0 to a missing transition. A table filled from right to left, like COUNT-DISTINCT, with a minimum in place of the sum, finds it in $\Theta(n \sigma)$ time.
- **Substrings instead.** For contiguous patterns, the [suffix automaton](/suffix-automaton/) plays the same part: it accepts the substrings of $T$ in linear size.

## When to use it

Use it when one fixed text is tested against many patterns: dictionary words against a long string, or many candidate commands against one keystroke history. Use the table when $\sigma$ is small, such as letters or DNA, and the position lists when $\sigma$ is large or memory is tight. For a single query, a plain scan in $\Theta(n)$ time and $O(1)$ space is simpler and faster than the build. For questions about the longest shared subsequence of two texts, see the [longest common subsequence](/longest-common-subsequence/).

## Pitfalls

- **Memory.** The full table is $(n + 1) \sigma$ entries. With bytes or Unicode as the alphabet, it is easy to run out of memory; map only the letters of $T$, or use the position lists.
- **Off by one.** State $i$ means "the first $i$ letters are used", and $\mathrm{nxt}[i][c]$ looks strictly after $i$. With $\ge$ in place of $>$, a repeated letter such as the second a of "aa" maps to the same position as the first.
- **Letters not in $T$.** A pattern letter that never occurs in $T$ must give NIL, not a lookup error.
- **Big counts.** The number of distinct subsequences grows exponentially; use big integers or a modulus.
- **Not for substrings.** The automaton accepts patterns with gaps. A substring search needs a [string matching](/string-matching/) method or a suffix structure.

## Implementations

## History

Baeza-Yates studied the problem of searching subsequences in 1991 and described the automaton that accepts all subsequences of a text, with its construction and its use for many patterns. Crochemore, Melichar and Troníček gave an overview of the directed acyclic subsequence graph for one text and for a set of texts in 2003.

## References
