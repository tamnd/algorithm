---
tag: NCDQ46
kind: data-structure
slug: generalized-suffix-automaton
name: Generalized suffix automaton
aliases:
- suffix automaton of a set of strings
area: strings/suffix-structures
level: advanced
summary: A suffix automaton over several strings, built by inserting each string into one automaton.
model: word-ram
complexity:
  vars: {N: the total length of the strings, m: the number of strings, q: the length of the pattern}
  time: {worst: O(N)}
  space: {extra: O(N)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [suffix-automaton, suffix-link, generalized-suffix-tree]
see_also: [suffix-automaton, generalized-suffix-tree, longest-common-substring, suffix-automaton-construction, blumer-algorithm, trie, matching-statistics, distinct-substrings-counting]
sources:
  - paper: doi:10.1145/28869.28873
    title: Anselm Blumer, Janet Blumer, David Haussler, Ross McConnell and Andrzej Ehrenfeucht, Complete inverted files for efficient text retrieval and analysis, Journal of the ACM 34(3), 1987
    locator: pages 578 to 595, the DAWG of a set of strings and its linear size
  - paper: doi:10.1016/j.tcs.2009.03.034
    title: Mehryar Mohri, Pedro Moreno and Eugene Weinstein, General suffix automaton construction algorithm and space bounds, Theoretical Computer Science 410(37), 2009
    locator: pages 3553 to 3562, the construction of the suffix automaton of a set of strings and its size bounds
  - book: isbn:9780521848992
    title: Maxime Crochemore, Christophe Hancart and Thierry Lecroq, Algorithms on Strings, Cambridge University Press, 2007
    locator: Chapter 5 (Structures for indexes), the suffix automaton and its construction with suffix links
---

A generalized suffix automaton of strings $S_0, \ldots, S_{m-1}$ is a deterministic automaton whose paths from the start state spell exactly the substrings of the strings, with one state for each class of substrings that end at the same set of places. It is the [suffix automaton](/suffix-automaton/) of a set, built online by inserting each string from the start state with one change to the usual extension step: if the needed transition already exists, reuse it or split its target. With $N$ the total length, it has at most $2N$ states and is built in $O(N)$ time for a constant alphabet, and like the [generalized suffix tree](/generalized-suffix-tree/) it answers multi-string questions such as the [longest common substring](/longest-common-substring/).

## In plain words

A suffix automaton of one word is a small machine that reads a piece of text letter by letter and says, at each step, whether what it has read so far is a piece of the word. Pieces that always end at the same places in the word share one state, which keeps the machine small.

For many words, build one machine for all of them. Start from the first state for each word and feed its letters one by one. Sometimes the step that a new letter needs is already in the machine from an earlier word. Then use it, and split a state in two if it holds pieces that now end at different places.

The result reads every piece of every word. Mark each state with the words in which its pieces occur. Then the deepest state marked with all the words gives their longest common piece.

## The abstract type

The structure is built from a list of strings and supports:

- `contains(P)`: is $P$ a substring of some $S_k$;
- `strings_containing(P)`: the indices $k$ with $P$ a substring of $S_k$;
- `distinct_substrings()`: the number of distinct nonempty substrings of all the strings together;
- `longest_common_substring(k)`: the length of the longest string that occurs in at least $k$ of the strings.

New strings can be added at any time, and each added string can grow symbol by symbol.

## Representation

The symbols are only tested for equality and used as keys of the transition maps; no sentinel and no separator is needed. Positions are 0-based.

**Classes.** For a nonempty string $u$, let $\mathrm{end}(u)$ be the set of pairs $(k, e)$ such that $u$ is a suffix of $S_k[0 \ldots e]$. Two substrings are equivalent if they have the same end set. Each class is a set of strings $u$ of lengths in an interval $(\ell', \ell]$, each a suffix of the longest one. The automaton has one state for each class and a root for the empty string.

**Fields.** For each state $v$: $len(v)$, the length of its longest string; $link(v)$, the [suffix link](/suffix-link/), the state of the longest suffix of the strings of $v$ that is in another class, so $len(link(v)) = \ell'$; and the transitions $\delta(v, c)$, kept in a hash map. The strings of $v$ are the suffixes of its longest string of lengths $len(link(v)) + 1$ to $len(v)$, so $v$ holds $len(v) - len(link(v))$ strings.

**Invariant.** After the strings $S_0, \ldots, S_{k-1}$ and a prefix $S_k[0 \ldots e]$ are inserted, the automaton is the generalized suffix automaton of those strings, and the variable $last$ is the state of the class of $S_k[0 \ldots e]$.

**Size.** The suffix links form a tree, the suffix tree of the reversed strings: each state is a node where a prefix of some string ends, or a node with at least two children, or the root. At most $N$ states hold a prefix, and the states with two or more children are fewer than the leaves, so there are at most $2N$ states when $N \ge 1$.

## Operations

```pseudo id=main
GSA-EXTEND(last, c)                      ▷ returns the state of the string of last followed by c
L1  if δ(last, c) exists then q ← δ(last, c)
L2      if len(q) = len(last) + 1 then return q
L3      else return SPLIT(last, c, q)
L4  cur ← new state with len(last) + 1; p ← last
L5  while p ≠ nil and δ(p, c) does not exist do δ(p, c) ← cur; p ← link(p)
L6  if p = nil then link(cur) ← root
L7  else q ← δ(p, c); if len(q) = len(p) + 1 then link(cur) ← q
L8      else link(cur) ← SPLIT(p, c, q)
L9  return cur
SPLIT(p, c, q)                           ▷ q holds strings that are too long for the new class
L10 clone ← new state with len(p) + 1, link(q) and a copy of the transitions of q
L11 while p ≠ nil and δ(p, c) = q do δ(p, c) ← clone; p ← link(p)
L12 link(q) ← clone; return clone
```

**Build.** For each string $S_k$: set $last \leftarrow root$, then for each symbol $c$ of $S_k$ set $last \leftarrow \text{GSA-EXTEND}(last, c)$, and record $last$ as the state of the prefix.

**The extra check (L1 to L3).** When the string $x$ of $last$ followed by $c$ is already a substring of an earlier string, no new state is needed for it. If $xc$ is the longest string of $q = \delta(last, c)$, then $q$ is its state (L2). Otherwise $q$ also holds longer strings that do not end at the new place, so $q$ is split: the strings up to length $len(last) + 1$ move to a clone (L3). Lines L4 to L9 are the usual extension of the [suffix automaton construction](/suffix-automaton-construction/).

**Queries.** `contains(P)` follows the transitions from the root. For `strings_containing`, give each prefix state of $S_k$ the bit $k$, then pass the bits up the suffix links in order of decreasing $len$; the bits of a state are the strings that contain its strings. `distinct_substrings` is the sum of $len(v) - len(link(v))$ over the states other than the root. `longest_common_substring(k)` is the largest $len(v)$ over the states with at least $k$ bits set.

## Example

The strings are $S_0 = \texttt{aab}$ and $S_1 = \texttt{ab}$.

**Inserting `aab`.** The three steps take the usual path (L4 to L9) and create the states 1 (`a`), 2 (`aa`) and 3 (`aab`, `ab`, `b`), with $link(2) = 1$ and $link(3) = 0$.

**Inserting `ab`.** From the root, $\delta(0, \texttt{a}) = 1$ and $len(1) = 1 = len(0) + 1$, so line L2 returns state 1: `a` is already a state. Then $\delta(1, \texttt{b}) = 3$, but $len(3) = 3 \ne len(1) + 1 = 2$. State 3 holds `aab`, which ends only in $S_0$, and `ab` and `b`, which now also end in $S_1$. Line L3 splits it: the clone, state 4 with $len = 2$, takes `ab` and `b`, the transitions $\delta(1, \texttt{b})$ and $\delta(0, \texttt{b})$ move to it, and $link(3) = 4$.

| state | $len$ | $link$ | transitions | strings of the class | end set | strings containing |
|---|---|---|---|---|---|---|
| 0 | 0 | none | a to 1, b to 4 | the empty string | all | 0, 1 |
| 1 | 1 | 0 | a to 2, b to 4 | a | (0, 0), (0, 1), (1, 0) | 0, 1 |
| 2 | 2 | 1 | b to 3 | aa | (0, 1) | 0 |
| 3 | 3 | 4 | none | aab | (0, 2) | 0 |
| 4 | 2 | 0 | none | ab, b | (0, 2), (1, 1) | 0, 1 |

The count of distinct substrings is $(1 - 0) + (2 - 1) + (3 - 2) + (2 - 0) = 5$: `a`, `aa`, `aab`, `ab` and `b`. The deepest state with both strings is state 4, so the longest common substring has length 2 (`ab`).

**A second example.** For $S_0 = \texttt{ab}$ and $S_1 = \texttt{cb}$, the last step reaches line L8: the new state `cb` needs a link, and $\delta(0, \texttt{b})$ leads to the state of `ab`, `b`, which is split. The automaton has 6 states: the root, `a`, `ab`, `c`, `cb` and `b`.

## Correctness

The full proof is in the proof file of this page. The invariant is that the automaton is the generalized suffix automaton of the strings inserted so far and that $last$ is the state of the current prefix. Adding $c$ to the current prefix $x$ adds the new end $(k, e + 1)$ to the end sets of the suffixes of $xc$, and to no other string.

1. If $xc$ is not yet a substring (no transition on $c$ from $last$), the step is the classic one for a single string, since the classic proof only uses the suffix links and lengths of the states on the suffix path of $x$, which have the same meaning here.
2. If $xc$ is already a substring and is the longest string of its class $q$, then every string of $q$ is a suffix of $xc$ that gains the same new end, so $q$ stays one class and is the answer.
3. Otherwise $q$ has strings longer than $xc$; they do not gain the new end, while $xc$ and its suffixes in $q$ do. So the class splits at the length $len(last) + 1$, and the clone takes the shorter part, with the transitions of $q$, because the right extensions of both parts are the same up to this point.

## Complexity

| operation | time | space |
|---|---|---|
| build | $O(N)$ amortized for a constant alphabet; $O(N \log \sigma)$ with sorted maps for $\sigma$ symbols, or $O(N)$ expected with hash maps | at most $2N$ states and $O(N)$ transitions |
| `contains(P)` | $O(q)$ | |
| `strings_containing(P)` | $O(q)$ after an $O(N m / w)$ pass over the bit sets, with $w$ the word size | $O(N m / w)$ words |
| `distinct_substrings` | $O(N)$ | |
| `longest_common_substring(k)` | $O(N m / w)$ | |

The amortized bound of the construction carries over from the single-string proof: the loops of L5 and L11 are paid for by the decrease of the depth of $last$ in the suffix link tree. Each string starts again from the root, which only lowers that depth. The bit sets can be replaced by a counter per state and a marker of the last string that touched it, when only the number of strings is needed.

## Variants

- **Building from a trie.** Insert the strings into a [trie](/trie/) first, then build the automaton in breadth-first order of the trie, each node extending the state of its parent. This avoids the repeated work on shared prefixes and gives a bound in the number of trie nodes.
- **Separators.** Join the strings with distinct separators and build the single-string [suffix automaton](/suffix-automaton/) of the result. This is simple but the automaton also reads strings that cross a separator, which must be filtered out, and it has more states.
- **CDAWG.** The compact DAWG of Blumer et al. merges the chains of states with one out-transition, as a suffix tree compacts a trie.
- **Minimal automaton.** The generalized suffix automaton is not always the smallest automaton for the substrings of the set. For `ab` and `cb` it has 6 states, while the minimal automaton of the substrings has 3: the root, one state after `a` or `c`, and one after `b`. The minimal one can be found with [DFA minimization](/dfa-minimization/), but it loses the end-set meaning of the states.

## When to use it

Use it for questions about all substrings of a set of strings that are solved by walking a text through an automaton: the longest common substring of several strings, the [matching statistics](/matching-statistics/) of a text against a collection, the number of distinct substrings of a collection, or the number of strings that contain a pattern. It is short to write and needs no suffix sorting. When positions of occurrences are needed, the [generalized suffix tree](/generalized-suffix-tree/) or a suffix array of the joined strings is more direct.

## Pitfalls

- **Missing the check of L1.** The single-string extension, run from the root for each new string, always creates a new state. If the transition already exists, that state is unreachable or duplicates an existing class. For $\texttt{aab}$ and $\texttt{ab}$ it gives 7 states instead of 5, and counts such as the number of distinct substrings come out wrong.
- **Resetting $last$.** Each string must start from the root, not from the last state of the previous string; otherwise the automaton reads strings that cross the border between two strings.
- **Order of propagation.** The bits must flow up the suffix links from longer to shorter states, so the states must be taken in order of decreasing $len$ (a counting sort by $len$ does it in linear time).
- **Clone transitions.** The clone must copy all transitions of $q$, and $q$ keeps its own; sharing one map between them breaks later steps.

## Implementations

The Python class keeps the transitions in dictionaries, records the state of each prefix, and computes the bit sets of the strings on demand. The tests compare it with a brute-force list of the substrings and their end sets, on random lists of strings over alphabets of size 1, 2 and 4 and on lists with $\texttt{a}^n$ and $(\texttt{ab})^n$.

## History

In 1985, Blumer, Blumer, Haussler, Ehrenfeucht, Chen and Seiferas described the DAWG, the suffix automaton of one string, and its linear-time online construction. Their 1987 paper "Complete inverted files for efficient text retrieval and analysis" extended it to a set of strings and introduced the compact DAWG. Many later programs built the automaton of a set with the single-string algorithm, with or without separators. Mohri, Moreno and Weinstein gave in 2009 a general construction for a set of strings, with size bounds.

## References
