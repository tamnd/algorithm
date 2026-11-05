---
tag: 045TZR
kind: algorithm
slug: bit-parallel-regex-matching
name: Bit-parallel regex matching
aliases:
- Shift-Or regex matching
- Baeza-Yates-Gonnet bit-parallel NFA
area: automata-and-parsing/regular-expressions
level: advanced
summary: Simulates the Glushkov automaton of a regex on bit vectors, so each text symbol costs a few table lookups and one AND.
solves: [regex-matching, regex-search]
model: word-ram
complexity:
  vars: {m: the number of nodes of the regular expression, k: the number of symbol occurrences in the expression, n: the length of the text, b: the number of bits of a table index, w: the number of bits of a machine word}
  time: {worst: O(m k^2 + (2^b + n) ⌈k/b⌉ ⌈k/w⌉)}
  space: {extra: O(2^b ⌈k/b⌉ ⌈k/w⌉ + k^2)}
properties: {deterministic: true, recursive: false, online: true}
history:
  year: 1992
  people: [Sun Wu, Udi Manber, Gonzalo Navarro, Mathieu Raffinot]
  note: Wu and Manber simulated Thompson's automaton with bit vectors in agrep; Navarro and Raffinot used the Glushkov automaton, which needs one table instead of one per symbol.
prereqs: [glushkov-automaton, bit-parallelism, nfa-simulation]
see_also: [shift-or, bitap-algorithm, thompson-nfa-simulation, lazy-dfa-construction, myers-bit-parallel-algorithm, regex-search, subset-construction, bit-vector]
sources:
  - book: isbn:9780521813075
    title: Gonzalo Navarro and Mathieu Raffinot, Flexible Pattern Matching in Strings, Cambridge University Press (2002)
    locator: Chapter 5, Regular expression matching (bit-parallel simulation of the Thompson and Glushkov automata, and the splitting of the tables)
  - paper: doi:10.1007/3-540-44688-5_1
    title: Gonzalo Navarro and Mathieu Raffinot, Compact DFA representation for fast regular expression search, Algorithm Engineering (WAE 2001), Lecture Notes in Computer Science 2141
    locator: pp. 1 to 13 (the Glushkov representation in (m+1)(2^(m+1) + |Σ|) bits, against m(2^(2m+1) + |Σ|) bits for the method of Wu and Manber)
  - paper: doi:10.1007/s00453-004-1120-3
    title: Gonzalo Navarro and Mathieu Raffinot, New techniques for regular expression searching, Algorithmica 41(2) (2004)
    locator: pp. 89 to 116 (bit-parallel search with the Glushkov automaton, and a backward search that can skip text characters)
  - paper: doi:10.1145/135239.135244
    title: Sun Wu and Udi Manber, Fast text searching allowing errors, Communications of the ACM 35(10) (1992)
    locator: pp. 83 to 91
  - paper: doi:10.1145/135239.135243
    title: Ricardo Baeza-Yates and Gaston H. Gonnet, A new approach to text searching, Communications of the ACM 35(10) (1992)
    locator: pp. 74 to 82 (the Shift-Or algorithm for strings)
---

Bit-parallel regex matching simulates a nondeterministic automaton for a [regular expression](/regular-expression/) by storing the set of active states as the bits of machine words, so that one text symbol updates all states with a few word operations. The best-known form uses the [Glushkov automaton](/glushkov-automaton/): since every move into a state reads the symbol of that state, the next set is $T[D] \mathbin{\&} B[c]$, a lookup in one precomputed table followed by one AND with the mask of the symbol $c$. When the automaton has at most $w$ states this costs $O(1)$ per symbol after a table of $2^{k+1}$ words, and larger automata split the table into pieces.

## In plain words

An automaton for a pattern can be in many states at once. Write the set of current states as a row of bits, one bit per state, and pack the row into one or a few machine words.

For the Glushkov automaton, each state belongs to one letter of the pattern, and every arrow into it reads that letter. So a step has two parts. First, find all states that can follow the current ones, whatever the next letter is. This depends only on the current row, so it can be looked up in a table made in advance. Second, keep only the states of the letter just read, with one AND against a fixed mask for that letter.

If the table is too big, cut the row into pieces of a few bits, look up each piece in its own small table, and OR the results.

## The problem

**Notation.** This site writes regular expressions with $r \mid s$ for union, $rs$ for concatenation, $r^*$ for the star, $\varepsilon$ for the empty string and $\emptyset$ for the empty language. Star binds tightest, then concatenation, then union.

The input is a regular expression $r$ with $m$ nodes and $k$ symbol leaves, and a text $y = y_1 \cdots y_n$. The output is true if $y \in L(r)$; this is [regex matching](/regex-matching/). The search form, which reports every $e$ such that some substring $y_{s+1} \cdots y_e$ is in $L(r)$, is a variant below ([regex search](/regex-search/)).

The Glushkov automaton of $r$ has states $0, \ldots, k$: state 0 is initial, and state $p \ge 1$ is the $p$-th symbol leaf, with symbol $\mathrm{sym}(p)$. $\mathrm{Follow}(0)$ is the set of positions that can begin a word, $\mathrm{Follow}(p)$ the set that can come after $p$, and $F$ the set of accepting states. A set $D \subseteq \{0, \ldots, k\}$ is stored as the integer $\sum_{p \in D} 2^p$, and $\&$, $\mid$ and $\gg$ are bitwise AND, OR and right shift. A parameter $b \ge 1$ is the number of bits of a table index.

## The algorithm

```pseudo id=main
BITPARALLEL(r, y, b)                        ▷ y = y1 ... yn; true iff y ∈ L(r)
L1  (sym, Follow, F) ← the Glushkov automaton of r, as bit masks over the states 0..k
L2  for each position q ≥ 1 do B[sym(q)] ← B[sym(q)] | 2^q     ▷ B[c] = 0 for other symbols
L3  s ← k + 1                               ▷ the number of states
L4  g ← ⌈s / b⌉                             ▷ the number of chunks
L5  for j ← 0 to g − 1 and v ← 1 to 2^b − 1 do T_j[v] ← T_j[v without its lowest bit] | Follow(jb + index of the lowest bit of v)
L6  D ← 1                                   ▷ only state 0
L7  for i ← 1 to n do
L8      E ← T_0[D & (2^b − 1)] | T_1[(D ≫ b) & (2^b − 1)] | ... | T_{g−1}[(D ≫ (g − 1)b) & (2^b − 1)]
L9      D ← E & B[y_i]
L10     if D = 0 then return false
L11 return D & F ≠ 0
```

$T_j[0] = 0$, and entries for states beyond $k$ are never used. Line L5 fills each table in increasing order of $v$, so the entry for $v$ with its lowest bit removed is ready. Line L8 computes $\bigcup_{p \in D} \mathrm{Follow}(p)$, and line L9 keeps the states whose symbol is $y_i$.

## Example

Let $r = (a \mid b)^* ab$, with positions $1 = a$, $2 = b$, $3 = a$ and $4 = b$, as on the [Glushkov automaton](/glushkov-automaton/) page. The sets are $\mathrm{Follow}(0) = \mathrm{Follow}(1) = \mathrm{Follow}(2) = \{1, 2, 3\}$, $\mathrm{Follow}(3) = \{4\}$, $\mathrm{Follow}(4) = \emptyset$, and $F = \{4\}$. Write sets as five bits, with state 4 on the left. Then $B[a] = 01010$, $B[b] = 10100$, $F = 10000$, and with $b = 8$ there is one table, with $T[00001] = T[10100] = 01110$ and $T[01010] = 11110$. On $y = abab$:

| $i$ | $y_i$ | $D$ before | $T[D]$ | $B[y_i]$ | $D$ after |
|---|---|---|---|---|---|
| 1 | $a$ | 00001 | 01110 | 01010 | 01010 |
| 2 | $b$ | 01010 | 11110 | 10100 | 10100 |
| 3 | $a$ | 10100 | 01110 | 01010 | 01010 |
| 4 | $b$ | 01010 | 11110 | 10100 | 10100 |

The last $D$ has bit 4, so $abab$ is accepted. With $b = 2$, the five bits are cut into the chunks $\{0, 1\}$, $\{2, 3\}$ and $\{4\}$, and line L8 ORs three lookups in tables of 4 entries.

**Search.** For $r = ab^*a$ and the text $babbaa$, the search variant reports the end positions 5 and 6: the substrings $abba$ and $aa$.

## Correctness

The Glushkov automaton is *homogeneous*: every move into a state $q$ reads $\mathrm{sym}(q)$, and state 0 has no incoming move. So the set of states reached from $D$ by reading $c$ is
$$\{q : q \in \mathrm{Follow}(p) \text{ for some } p \in D, \ \mathrm{sym}(q) = c\} = \Big(\bigcup_{p \in D} \mathrm{Follow}(p)\Big) \cap B[c].$$
Line L5 makes $T_j[v]$ equal to the union of $\mathrm{Follow}(jb + i)$ over the bits $i$ of $v$, by induction on $v$. The chunks of $D$ split $D$ into disjoint parts, and the union over $D$ is the union over its parts, so line L8 computes $\bigcup_{p \in D} \mathrm{Follow}(p)$, and line L9 computes the set above. By induction on $i$, after line L9 the set $D$ is the set of states that the automaton can reach by reading $y_1 \cdots y_i$. If it is empty, no longer input can reach a state, so line L10 is right to stop. At the end, $y$ is accepted if and only if a reachable state is accepting, which is line L11, and the Glushkov automaton accepts exactly $L(r)$. Every loop has a fixed number of rounds, so the algorithm stops. The full proof is below.

## Complexity

- **Preprocessing.** The Glushkov sets take $O(m k^2)$ time as on that page, or less with star normal form. Line L2 takes $O(k \lceil k/w \rceil)$. Line L5 fills $g \cdot 2^b$ entries with $g = \lceil (k+1)/b \rceil$, each with one OR of $(k + 1)$-bit vectors, so $O(2^b \lceil k/b \rceil \lceil k/w \rceil)$ time.
- **Per symbol.** Line L8 does $g$ lookups and ORs of $\lceil (k+1)/w \rceil$ words, and line L9 one AND. So the text costs $O(n \lceil k/b \rceil \lceil k/w \rceil)$.
- **One word.** If $k + 1 \le w$ and $b = k + 1$, each symbol costs $O(1)$: one lookup and one AND. The table has $2^{k+1}$ words, and the masks $|\Sigma|$ words. A DFA table with the same $2^{k+1}$ subsets as states would have $2^{k+1} |\Sigma|$ entries, so homogeneity saves a factor of $|\Sigma|$.
- **Space.** $g \cdot 2^b$ table entries of $\lceil (k+1)/w \rceil$ words, plus the Follow masks and the symbol masks.
- **Choosing $b$.** A larger $b$ means fewer lookups per symbol and larger tables; $b$ is chosen so that the tables fit in the cache.

## Properties

- **Online and worst-case linear.** For a fixed pattern, the time is linear in $n$, with no exponential case, and the text is read once from left to right.
- **A subset construction on the fly.** The value of $D$ is the state of the DFA of the [subset construction](/subset-construction/), but only the sets that occur are ever formed, and the transition is computed instead of stored.
- **Strings as a special case.** For $r = a_1 a_2 \cdots a_k$, $\mathrm{Follow}(p) = \{p + 1\}$, so $T[D]$ is $D$ shifted left by one bit, and the search variant is the Shift-And form of the [Shift-Or](/shift-or/) algorithm of Baeza-Yates and Gonnet (1992).
- **Yes or no only.** Like other set simulations, it decides membership and finds the end of each match, but it keeps no capture positions.
- **Regular only.** Backreferences cannot be simulated with a fixed set of states.

## Variants and improvements

- **Search.** Add state 0 again before each symbol: $D \leftarrow (T[D] \mathbin{\&} B[y_i]) \mid 1$, and report $i$ whenever $D \mathbin{\&} F \ne 0$. This finds every end position of a match in one pass.
- **Thompson automaton.** Wu and Manber (1992) simulated Thompson's automaton with bit vectors in agrep. Its states are not homogeneous, and the $\varepsilon$-closure must be applied too, so the tables are indexed by about $2m$ bits instead of $k + 1$. Navarro and Raffinot (2001) report $m(2^{2m+1} + |\Sigma|)$ bits for this method against $(m + 1)(2^{m+1} + |\Sigma|)$ for the Glushkov form, where their $m$ is the number of symbols.
- **Backward search.** Navarro and Raffinot (2004) run the automaton of the reversed expression backward in a window of the text and skip text symbols that cannot be part of a match, as the BNDM family does for strings.
- **Errors.** Wu and Manber keep one vector for each number of errors allowed, and combine them at each step, to find approximate matches. For plain strings, the [Myers bit-vector algorithm](/myers-bit-parallel-algorithm/) encodes the edit-distance table in bit vectors in a different way.
- **Character classes.** A position with a class such as `[a-z]` sets its bit in $B[c]$ for every $c$ in the class; nothing else changes.

## When to use it

Use it for searching with patterns of up to a few hundred symbols when the worst case matters, as in grep-like tools: the inner loop is short and has no branches that depend on the data. For long patterns, the cost per symbol grows with $k^2/(bw)$, and a [lazy DFA](/lazy-dfa-construction/) that caches the sets that occur is often faster. When the pattern is a plain string, use [Shift-Or](/shift-or/) or a skipping algorithm instead.

## Pitfalls

- **Table size.** The tables have $2^b$ entries each; $b = k + 1$ is only possible for small patterns. Choose $b$ around 8 to 16 and split.
- **Forgetting state 0.** State 0 is bit 0 of $D$. In the search variant it must be added before every symbol, including the first.
- **Counted repetition.** `x{2,1000}` unrolls into about 1000 copies of $x$, so $k$, and with it the number of words per vector, grows by that factor ([bounded repetition](/bounded-repetition/)).
- **Symbols that do not occur.** A text symbol that is not in the pattern has $B[c] = 0$, and the match fails at once; the table of masks must give 0, not an error.

## Implementations

## History

Baeza-Yates and Gonnet (1992) introduced the Shift-Or algorithm, which keeps the state of a string matcher in the bits of a word. Wu and Manber (1992) extended bit-parallelism to regular expressions and approximate matching, simulating Thompson's automaton, and used it in agrep. Navarro and Raffinot (2001, 2004) used the Glushkov automaton, whose homogeneity gives the update $T[D] \mathbin{\&} B[c]$ with a single table, and combined it with backward search.

## References
