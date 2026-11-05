---
tag: CK7G4C
kind: data-structure
slug: levenshtein-automaton
name: Levenshtein automaton
aliases:
- Schulz-Mihov automaton
- k-error automaton
area: strings/approximate-matching
level: advanced
summary: Deterministic automaton that accepts all strings within edit distance k of a fixed word.
solves: [approximate-dictionary-lookup, k-differences-problem]
model: word-ram
complexity:
  vars: {m: the length of the word, k: the error bound, s: the number of states built, ρ: the number of distinct symbols of the word}
  time: {build: "O(s (ρ + 1) m)", step: "O(m)"}
  space: {extra: "O(s (m + ρ))"}
properties: {deterministic: true, recursive: false, online: true}
prereqs: [deterministic-finite-automaton, edit-distance, wagner-fischer-algorithm]
see_also: [approximate-dictionary-lookup, trie, nondeterministic-finite-automaton, sellers-algorithm, myers-bit-parallel-algorithm, bk-tree, dfa-minimization, ukkonen-cutoff-algorithm]
sources:
  - paper: "Klaus U. Schulz and Stoyan Mihov, Fast string correction with Levenshtein automata, International Journal on Document Analysis and Recognition 5(1), 2002"
    locator: the deterministic Levenshtein automaton of a word for a fixed bound k, its construction in time linear in the length of the word, and the parallel walk with the automaton of a dictionary
  - paper: doi:10.1145/375360.375365
    title: Gonzalo Navarro, A guided tour to approximate string matching, ACM Computing Surveys 33(1), 2001
    locator: Section 6.2, Implementing the automaton (Ukkonen 1985 with columns as states, the cap at k + 1, differences in -1, 0, 1, the bound O(min(3^m, m (2 m σ)^k)) on the states, and the lazy construction of Kurtz 1996)
  - paper: "Esko Ukkonen, Finding approximate patterns in strings, Journal of Algorithms 6, 1985"
    locator: pages 132 to 137 (the deterministic automaton whose states are the columns of the dynamic programming table, with entries capped at k + 1)
  - book: isbn:9780521813075
    title: Gonzalo Navarro and Mathieu Raffinot, Flexible Pattern Matching in Strings, Cambridge University Press, 2002
    locator: Chapter 6, Approximate matching (the automaton for approximate matching and its deterministic form)
---

A Levenshtein automaton for a word $W$ and a bound $k$ is a [deterministic finite automaton](/deterministic-finite-automaton/) that accepts exactly the strings $x$ with [edit distance](/edit-distance/) $\operatorname{ed}(W, x) \le k$. Its states are the rows of the [Wagner-Fischer table](/wagner-fischer-algorithm/) of $W$ against the input read so far, with each entry capped at $k + 1$, so one step costs $O(m)$ for a word of length $m$, and a memoized step costs $O(1)$ expected. Its main use is [approximate dictionary lookup](/approximate-dictionary-lookup/): a walk over a [trie](/trie/) of the dictionary in step with the automaton visits only the prefixes that can still lead to a match. Schulz and Mihov built it for a single word in 2002, for spelling correction, and Ukkonen used the same capped columns in 1985 to search a text.

## In plain words

To check whether a typed word is close to a dictionary word, the program fills the classic table of edit costs one letter of the typed word at a time. Each new letter adds one new row, computed from the row before it only. So the last row is all the program needs to remember.

Costs above the allowed number of errors never come back down, so the program writes all of them as one value, "too many". Then only a limited number of different rows can ever occur. Each different row becomes a state of a machine, and each letter moves the machine from one state to the next.

A state in which every entry says "too many" can never lead to a match. A search through a dictionary stored as a tree of prefixes stops at such a state and skips the whole branch below it.

## The abstract type

The edit model is the Levenshtein distance: insertion, deletion and substitution of one character, each at cost 1, and no transpositions. Indices are 0-based. Given a word $W$ of length $m \ge 0$ and an integer $k \ge 0$, the structure represents the language $L_k(W) = \{x : \operatorname{ed}(W, x) \le k\}$ over any alphabet, and supports these operations on states:

- `start()`: the state for the empty input.
- `step(q, c)`: the state after one more symbol $c$.
- `is_match(q)`: whether the input read so far is in $L_k(W)$.
- `can_match(q)`: whether some extension of the input read so far is in $L_k(W)$.
- `distance(q)`: $\min(\operatorname{ed}(W, x), k + 1)$ for the input $x$ read so far.

The derived operation `lookup(D)` returns the words of a finite set $D$ that lie in $L_k(W)$. In search mode the same structure finds the end positions $j \in \{0, \ldots, n\}$ of the approximate occurrences of $W$ in a text, as the [k-differences problem](/k-differences-problem/) asks.

## Representation

Let $K = k + 1$. A state is a tuple $R$ of $m + 1$ integers in $\{0, \ldots, K\}$. After the input $x$, the state is the capped row $R_x[i] = \min(\operatorname{ed}(W[0..i), x), K)$ for $0 \le i \le m$. A hash table maps each row that has occurred to a small integer id. A second hash table holds the transitions found so far, keyed by the pair of a state id and a symbol class. All symbols that do not occur in $W$ act alike, so they share one class, and each state has at most $\rho + 1$ transitions, where $\rho$ is the number of distinct symbols of $W$.

**Invariant.** Each stored row is $R_x$ for some input $x$, and the stored transition from the id of $R_x$ by the class of $c$ leads to the id of $R_{xc}$.

## Operations

```pseudo id=main
START(W, k)
L1  K ← k + 1
L2  return the state of the row R with R[i] = min(i, K) for i = 0..m
STEP(R, c)                         ▷ first look up (R, class of c) in the memo table
L3  R'[0] ← min(R[0] + 1, K)       ▷ search mode: R'[0] ← 0
L4  for i ← 1 to m do
L5      R'[i] ← min(R[i−1] + [W[i−1] ≠ c], R[i] + 1, R'[i−1] + 1, K)
L6  return the state of R' (a new id if R' is new), and store the transition
IS-MATCH(R)
L7  return R[m] ≤ k
CAN-MATCH(R)
L8  return min(R[0], ..., R[m]) ≤ k
LOOKUP(trie of D)
L9  stack ← [(root, START(W, k))]
L10 while stack is not empty do pop (u, R)
L11     if u ends a word y and IS-MATCH(R) then report y
L12     for each child v of u by a symbol c: R' ← STEP(R, c); if CAN-MATCH(R') then push (v, R')
```

Line L5 is the Wagner-Fischer recurrence for one new column, with every value capped at $K$. The cap does not change any answer: each new entry is a minimum of old entries plus 0 or 1, so capping before or after the step gives the same row. The row with all entries $K$ is the dead state. It maps to itself on every symbol, so line L12 never pushes a node below it. To build the whole automaton, run a search over the states from the start, with one symbol of each class.

In search mode, line L3 keeps $R'[0] = 0$. The row is then the capped column of the [Sellers table](/sellers-algorithm/), as in Ukkonen's automaton, and the state after the text prefix $T[0..j)$ is a match exactly when $j$ is an end position. A search-mode automaton has no dead state.

## Example

Take $W = \texttt{cat}$ and $k = 1$, so $K = 2$. The symbol classes are $\texttt{a}$, $\texttt{c}$, $\texttt{t}$ and "other". The whole automaton has 13 states, in the order in which a search from the start makes them:

| state | row $R$ | on a | on c | on t | on other | match |
|---|---|---|---|---|---|---|
| 0 | 0 1 2 2 | 1 | 2 | 3 | 3 | |
| 1 | 1 1 1 2 | 4 | 5 | 7 | 6 | |
| 2 | 1 0 1 2 | 8 | 9 | 10 | 9 | |
| 3 | 1 1 2 2 | 4 | 5 | 6 | 6 | |
| 4 | 2 2 1 2 | 6 | 6 | 7 | 6 | |
| 5 | 2 1 2 2 | 4 | 6 | 6 | 6 | |
| 6 | 2 2 2 2 | 6 | 6 | 6 | 6 | dead |
| 7 | 2 2 2 1 | 6 | 6 | 6 | 6 | yes |
| 8 | 2 1 0 1 | 11 | 11 | 12 | 11 | yes |
| 9 | 2 1 1 2 | 4 | 6 | 7 | 6 | |
| 10 | 2 1 1 1 | 4 | 6 | 7 | 6 | yes |
| 11 | 2 2 1 1 | 6 | 6 | 7 | 6 | yes |
| 12 | 2 2 1 0 | 7 | 7 | 7 | 7 | yes |

State 12 is the row of $\texttt{cat}$ itself, state 8 the row of $\texttt{ca}$, and state 7 the row of $\texttt{cats}$, $\texttt{coat}$, $\texttt{cart}$, $\texttt{scat}$, $\texttt{cut}$ and $\texttt{at}$, each at distance exactly 1. For this word no two states can be merged, so the automaton is minimal. That does not hold in general: for $W = \texttt{ab}$ and $k = 2$ there are 14 rows, and [DFA minimization](/dfa-minimization/) leaves 12 states.

A lookup of $\texttt{cat}$ with $k = 1$ in the dictionary $\{\texttt{cat}, \texttt{cart}, \texttt{act}, \texttt{at}, \texttt{coat}, \texttt{cut}, \texttt{dog}, \texttt{cats}, \texttt{scat}, \texttt{a}, \varepsilon\}$ reports $\texttt{at}$, $\texttt{cart}$, $\texttt{cat}$, $\texttt{cats}$, $\texttt{coat}$, $\texttt{cut}$ and $\texttt{scat}$. The walk stops at the prefix $\texttt{do}$, whose row is dead, so it never reads the $\texttt{g}$. The prefix $\texttt{ac}$ has the row 2 1 2 2, which is alive, but $\texttt{act}$ reaches the dead state, since $\operatorname{ed}(\texttt{cat}, \texttt{act}) = 2$. The word $\texttt{a}$ ends in state 1 and the empty word in state 0, and neither state matches.

In search mode, the automaton of $\texttt{GATAA}$ with $k = 1$ reports the end positions 6, 7, 8 and 12 in the text $\texttt{CAGATAAGAGAA}$.

## Correctness

Appending one symbol to the input adds one column to the Wagner-Fischer table, and line L5 is its recurrence. Capping commutes with the step, because $\min(\min(a, K) + d, K) = \min(a + d, K)$ for $d \ge 0$. So by induction the state after $x$ is the capped row of $x$, and `is_match` tests $\operatorname{ed}(W, x) \le k$. A row with an entry $R[i] \le k$ can still match, by appending $W[i..m)$, and the all-$K$ row maps to itself, so `can_match` is exact and the pruned walk misses no word. The full proof, with the bound on the number of states, is below.

## Complexity

A new row costs $O(m)$ time and $O(m)$ space, and its hash costs $O(m)$ expected time. A stored transition costs $O(1)$ expected time. Building all $s$ states costs $O(s (\rho + 1) m)$ expected time and $O(s (m + \rho))$ space.

The number of states is bounded in terms of $m$ and $k$ only. After an input of length $L$, every entry with $|i - L| > k$ is $K$, since $\operatorname{ed}(W[0..i), x) \ge |i - L|$, and two neighbouring entries differ by at most 1. So the live part of a row is a window of at most $2k + 1$ entries, fixed by its first value and its steps, and every input longer than $m + k$ is dead. This gives at most $(m + k + 1)(k + 2)\,3^{2k} + 1$ states, which is $O(m)$ for a fixed $k$. Actual counts are much lower: the word $\texttt{abcdefgh}$ gives 33, 107 and 329 states for $k = 1, 2, 3$, and $\texttt{aaaaaaaa}$ gives 19, 28 and 37.

For search mode, Ukkonen bounded the number of states by $O(\min(3^m, m (2 m \sigma)^k))$ for an alphabet of size $\sigma$. After the automaton is built, the search reads each text symbol with one transition, so it takes $O(n)$ time for a text of length $n$.

A dictionary lookup costs $O(1)$ expected time for each trie node that the walk visits, plus the cost of the new states. The walk pops the nodes whose string is within distance $k$ of some prefix of $W$, and computes one step for each child of such a node.

## Variants

- **Schulz-Mihov construction.** Their states are sets of positions of the [nondeterministic automaton](/nondeterministic-finite-automaton/), reduced by a subsumption order. Precomputed tables that depend only on $k$ give the automaton for any word in time linear in $m$ for a fixed $k$.
- **Window rows.** Store only the window of $2k + 1$ entries and the offset $L$. A step then costs $O(k)$.
- **Lazy search automaton.** Kurtz built the states of Ukkonen's search automaton only when the text reaches them, which bounds the memory by $O(m n)$ for a text of length $n$.
- **Transpositions.** For the optimal string alignment form of the [Damerau-Levenshtein distance](/damerau-levenshtein-distance/), a state holds the last two rows, because the transposition term reads the row before the last one.
- **Bit-parallel simulation.** Instead of building states, simulate the nondeterministic automaton with bit vectors, as [Wu-Manber](/wu-manber-approximate-matching/) and [Myers](/myers-bit-parallel-algorithm/) do.

## When to use it

Use it for spelling correction and fuzzy search in a large static dictionary that is stored as a trie or as a minimal automaton, with a small $k$ such as 1 or 2. The walk then reads a tiny part of the dictionary for each query. For a metric index without a trie use a [BK-tree](/bk-tree/), and for a single text search with larger $k$ a bit-parallel algorithm needs no preprocessing that grows with $k$.

## Pitfalls

- **Alphabet size.** A full transition table over a large alphabet, such as Unicode, is huge. Map all symbols that are not in the word to one class.
- **The cap.** Entries must be capped at exactly $k + 1$, both in the stored rows and in the comparison of rows. Without the cap the number of states is unbounded.
- **Word mode and search mode.** The first entry grows by 1 in word mode and stays 0 in search mode. Mixing them matches whole words against substrings or the other way round.
- **Growth with k.** The number of states grows fast with $k$. For $k \ge 3$ on long words, a lazy construction or a bit-parallel simulation is safer.
- **Transpositions.** A typo such as $\texttt{act}$ for $\texttt{cat}$ costs 2 in this model. Use the transposition variant when such typos matter.

## Implementations

## History

Esko Ukkonen proposed in 1985 a deterministic automaton for approximate search whose states are the columns of the dynamic programming table. He capped the entries at $k + 1$ and showed that neighbouring entries differ by at most 1, which bounds the number of states. Stefan Kurtz built this automaton lazily in 1996, as Navarro's survey reports. In 2002 Klaus Schulz and Stoyan Mihov defined the Levenshtein automaton of a single word and built it in linear time for a fixed bound, for the correction of words against large dictionaries.

## References
