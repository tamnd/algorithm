---
tag: XE8A8C
kind: data-structure
slug: suffix-automaton
name: Suffix automaton
aliases:
- DAWG
- directed acyclic word graph
area: strings/suffix-structures
level: core
summary: The minimal deterministic automaton accepting all suffixes of a string; built online in linear time.
implements: [full-text-index]
model: word-ram
complexity:
  vars: {n: the length of the text, m: the length of the pattern, σ: the size of the alphabet}
  time: {query: O(m), build: O(n log σ), build-constant-alphabet: O(n)}
  space: {extra: O(n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [suffix, deterministic-finite-automaton]
see_also: [suffix-automaton-size-theorem, blumer-algorithm, suffix-automaton-construction, suffix-link, suffix-tree, suffix-trie, myhill-nerode-relation, distinct-substrings-counting]
sources:
  - paper: doi:10.1016/0304-3975(85)90157-4
    title: A. Blumer, J. Blumer, D. Haussler, A. Ehrenfeucht, M. T. Chen and J. Seiferas, The smallest automaton recognizing the subwords of a text, Theoretical Computer Science 40, 1985
    locator: pages 31 to 55; the DAWG, the end-set equivalence, the bounds 2n − 1 and 3n − 4, and the online construction
  - paper: doi:10.1016/0304-3975(86)90041-1
    title: Maxime Crochemore, Transducers and repetitions, Theoretical Computer Science 45, 1986
    locator: pages 63 to 86; the minimal suffix automaton and its linear-time construction
  - book: isbn:9780521848992
    title: Maxime Crochemore, Christophe Hancart and Thierry Lecroq, Algorithms on Strings, Cambridge University Press, 2007
    locator: Chapter 5, Structures for indexes (the suffix automaton, its size and its online construction)
---

The suffix automaton of a string $S$ is the smallest [deterministic finite automaton](/deterministic-finite-automaton/) that accepts exactly the [suffixes](/suffix/) of $S$. If every state is made accepting, it accepts exactly the substrings of $S$, so it is a full-text index: a pattern of length $m$ is found by following $m$ transitions. Its states are the classes of substrings with the same set of end positions; there are at most $2n - 1$ of them and at most $3n - 4$ transitions for $n \ge 3$, by the [suffix automaton size theorem](/suffix-automaton-size-theorem/). It is built online, one symbol at a time, in $O(n)$ time for a constant alphabet by the [algorithm of Blumer and others](/blumer-algorithm/), with [suffix links](/suffix-link/) as the main tool.

## In plain words

Think of a machine that reads a word letter by letter and says "yes" if the word is a piece of the text. A [suffix trie](/suffix-trie/) is such a machine, but it can be huge, with one node for each different piece.

Many pieces behave the same way: they appear at exactly the same places in the text, ending at the same letters. For example, in "abbb" the pieces "bbb" and "abbb" both end only at the last letter. Whatever letters you add after them, the answer is the same. So the machine can treat them as one state. Merging all such pieces gives the smallest possible machine, and it has at most about twice as many states as the text has letters. It can be built while the text is read, one letter at a time.

## The abstract type

The suffix automaton implements the static [full-text index](/full-text-index/) of a text $S$: `contains(P)`, `count(P)` and the position of the first occurrence of $P$. It also answers "is $P$ a suffix of $S$?" and gives the number of distinct substrings. Unlike most indexes, it can be extended at the right end: `extend(c)` turns the automaton of $S$ into the automaton of $Sc$.

## Representation

The text is $S = S[0 \ldots n-1]$, 0-based, over any alphabet: the code uses symbols as keys of hash maps and tests them for equality, with no order. No sentinel is appended. For a substring $x$, let $endpos(x)$ be the set of end positions of its occurrences, $\{\, e : S[e - |x| + 1 \ldots e] = x \,\}$, and $endpos(\varepsilon) = \{-1, 0, \ldots, n-1\}$ by convention. Two substrings are equivalent if they have the same $endpos$. This is the [Myhill-Nerode relation](/myhill-nerode-relation/) of the language of suffixes of $S$, restricted to substrings, so the classes are the states of the minimal automaton.

Each state $v$ stores:

- $next(v)$, a map from symbols to states: the transition on $c$ goes from the class of $x$ to the class of $xc$;
- $len(v)$, the length of the longest string of the class;
- $link(v)$, the [suffix link](/suffix-link/): the class of the longest suffix of the strings of $v$ that is not in $v$;
- $first(v)$, the smallest element of $endpos$ of the class, for first occurrences.

**Invariant.**

- **(A1) Classes are suffix intervals.** The strings of a state $v \ne$ initial are the suffixes of its longest string $long(v)$ with lengths $len(link(v)) + 1, \ldots, len(v)$.
- **(A2) Transitions.** For a substring $x$ in state $v$ and a symbol $c$ with $xc$ a substring, $next(v)[c]$ is the state of $xc$; no other transitions exist.
- **(A3) Links.** $len(link(v)) < len(v)$, and the links form a tree rooted at the initial state.
- **(A4) Acceptance.** The suffixes of $S$ are the strings of the states on the link path from the state of $S$ (called $last$) to the initial state.

The number of distinct nonempty substrings is $\sum_{v \ne \text{init}} (len(v) - len(link(v)))$, by (A1).

## Operations

```pseudo id=main
SAM-EXTEND(c)                             ▷ the automaton of S becomes that of Sc
L1  cur ← a new state with len(cur) = len(last) + 1
L2  p ← last
L3  while p ≠ NIL and next(p)[c] = NIL do next(p)[c] ← cur; p ← link(p)
L4  if p = NIL then link(cur) ← init
    else q ← next(p)[c]
L5      if len(p) + 1 = len(q) then link(cur) ← q
L6      else clone ← a copy of q (same next, same link) with len(clone) = len(p) + 1
L7          while p ≠ NIL and next(p)[c] = q do next(p)[c] ← clone; p ← link(p)
L8          link(q) ← clone; link(cur) ← clone
L9  last ← cur

WALK(P)                                   ▷ the state of P, or NIL
L10 v ← init; for each symbol c of P do v ← next(v)[c]; if v = NIL then return NIL
L11 return v
```

**Build.** Start with the initial state alone, and call SAM-EXTEND for each symbol of $S$. The new suffixes of $Sc$ are $xc$ for the suffixes $x$ of $S$, which line L3 visits along the link path of $last$. Those $xc$ that are new substrings go to $cur$. The first $xc$ that already exists lies in a state $q$; if $q$ also holds longer strings that are not suffixes of $Sc$, their end positions now differ from those of $xc$, and lines L6 to L8 split $q$ into two states. The full construction, with its analysis, is on the page of the [Blumer algorithm](/blumer-algorithm/).

**Contains.** $P$ is a substring if and only if WALK$(P) \ne$ NIL, in $O(m)$ time.

**Count.** The number of occurrences of $x$ is $|endpos(x)|$. Give each non-clone state other than the initial one the value 1, then add the value of each state to its link, in order of decreasing $len$. Then $count(P)$ is the value at WALK$(P)$. A non-clone state is created at one position $e$ as the class of the prefix $S[0 \ldots e]$, and $e \in endpos(x)$ exactly when the state of $S[0 \ldots e]$ is in the link subtree of the state of $x$.

**First occurrence.** $first(cur) = e$ when $cur$ is created for position $e$, and a clone copies $first(q)$. The first occurrence of $P$ starts at $first(\text{WALK}(P)) - m + 1$.

**Suffix test.** $P$ is a suffix of $S$ if and only if WALK$(P)$ is on the link path from $last$, by (A4).

## Example

Build the suffix automaton of $S = \texttt{abbb}$. Each state is written as its class of strings.

| after | new states | clone | states with $len$ and $link$ |
|---|---|---|---|
| a | $\{a\}$ | none | $\{\varepsilon\}$ 0; $\{a\}$ 1 → $\varepsilon$ |
| ab | $\{b, ab\}$ | none | $\{b, ab\}$ 2 → $\varepsilon$ |
| abb | $\{bb, abb\}$ | $\{b\}$ split off $\{b, ab\}$ | $\{ab\}$ 2 → $\{b\}$; $\{bb, abb\}$ 3 → $\{b\}$; $\{b\}$ 1 → $\varepsilon$ |
| abbb | $\{bbb, abbb\}$ | $\{bb\}$ split off $\{bb, abb\}$ | $\{abb\}$ 3 → $\{bb\}$; $\{bbb, abbb\}$ 4 → $\{bb\}$; $\{bb\}$ 2 → $\{b\}$ |

In the step for the second $\texttt{b}$, the walk of line L3 starts at $last = \{b, ab\}$, which has no transition on $\texttt{b}$, and adds one to $cur$. It goes on to $\{\varepsilon\}$, which has the transition $\texttt{b} \to \{b, ab\}$. Here $len(\varepsilon) + 1 = 1 < 2$: the string $\texttt{b}$ now ends at positions 1 and 2, but $\texttt{ab}$ only at position 1, so the class splits. The clone $\{b\}$ gets the transitions of $\{b, ab\}$, and the transition of $\{\varepsilon\}$ on $\texttt{b}$ moves to the clone.

The final automaton has 7 states and 7 transitions:

| state | $len$ | $link$ | transitions |
|---|---|---|---|
| $\{\varepsilon\}$ | 0 | none | a → $\{a\}$, b → $\{b\}$ |
| $\{a\}$ | 1 | $\{\varepsilon\}$ | b → $\{ab\}$ |
| $\{b\}$ | 1 | $\{\varepsilon\}$ | b → $\{bb\}$ |
| $\{ab\}$ | 2 | $\{b\}$ | b → $\{abb\}$ |
| $\{bb\}$ | 2 | $\{b\}$ | b → $\{bbb, abbb\}$ |
| $\{abb\}$ | 3 | $\{bb\}$ | b → $\{bbb, abbb\}$ |
| $\{bbb, abbb\}$ | 4 | $\{bb\}$ | none |

The suffixes $\texttt{abbb}, \texttt{bbb}, \texttt{bb}, \texttt{b}, \varepsilon$ are the strings on the link path from $last = \{bbb, abbb\}$. The counts are $count(\texttt{b}) = 3$, $count(\texttt{bb}) = 2$, $count(\texttt{abb}) = 1$, and the number of distinct nonempty substrings is $1 + 1 + 1 + 1 + 1 + 2 = 7$: a, b, ab, bb, abb, bbb and abbb. For $\texttt{abbb}$, $n = 4$, the $2n - 1 = 7$ states reach the bound of the size theorem.

## Correctness

The invariant (A1) to (A4) holds for the empty string. In SAM-EXTEND, the end positions change only for the suffixes of $Sc$, which gain the new position $n$. The suffixes $xc$ that did not occur before have $endpos = \{n\}$, the same as $Sc$, and line L3 sends them to $cur$. The first existing one, $x_0 c$ with $x_0$ the longest string of $p$, lies in $q$. If $len(q) = len(p) + 1$, then $x_0 c$ is the longest string of $q$, all strings of $q$ are suffixes of $Sc$, and they all gain $n$ together: $q$ stays one class, and it is the link of $cur$. Otherwise the strings of $q$ longer than $len(p) + 1$ are not suffixes of $Sc$ and keep their end positions, while the shorter ones gain $n$; the clone takes the shorter ones, with the same outgoing transitions, and line L7 redirects to the clone the transitions that read a short one. The proof file gives the details, including (A4).

## Complexity

The costs assume child maps with $O(1)$ lookup: arrays for a constant alphabet, or hashing in expectation. Ordered maps add a factor $\log |\Sigma|$ to each step.

| operation | time | notes |
|---|---|---|
| build | $O(n)$ for a constant alphabet | amortized $O(1)$ per symbol |
| contains, suffix test | $O(m)$ | |
| count | $O(m)$ after an $O(n)$ pass | |
| first occurrence | $O(m)$ | |
| distinct substrings | $O(n)$ | one pass over the states |
| space | at most $2n - 1$ states and $3n - 4$ transitions | $n \ge 3$ |

The linear time of the build is amortized: the loops of lines L3 and L7 can be long for one symbol, but a potential argument on the length of the link path of $last$ bounds their total by $O(n)$; see the [Blumer algorithm](/blumer-algorithm/).

## Variants

- **Factor automaton.** Make all states accepting; the minimal automaton of the substrings may then have fewer states, since states are merged that differ only in which strings are suffixes. Crochemore and others study both automata.
- **Compact DAWG.** Compress chains of states with one outgoing transition, as the suffix tree compresses the trie; the result has $O(n)$ size with fewer nodes.
- **Generalized suffix automaton.** The automaton of a set of strings, built by resetting $last$ to the initial state at each new string, with extra care for transitions that already exist.
- **Link tree as a suffix tree.** The suffix links of the automaton of $S$ form the [suffix tree](/suffix-tree/) of the reversed string, so one construction gives both structures.
- **Factor oracle.** A smaller automaton with $n + 1$ states that accepts all substrings and some other strings, due to Allauzen, Crochemore and Raffinot; it is used for fast filtering in pattern matching.

## When to use it

Use a suffix automaton when the text grows at the right end and must be queried at any time, or for problems on all substrings that it answers by one pass over its states: the number of distinct substrings, the longest common substring of two strings (read the second string through the automaton of the first, falling back by suffix links), the $k$-th smallest substring, or the number of occurrences of every substring. It is short to code, which makes it popular in programming contests. For pattern search in a fixed large text, a [suffix array](/suffix-array/) uses less memory, and it gives the positions of all occurrences directly.

## Pitfalls

- **Forgetting to copy the link and transitions into the clone.** The clone must copy $next(q)$ and $link(q)$ exactly, and only then become the link of $q$ and $cur$.
- **Stopping the redirect loop too late.** Line L7 must stop at the first $p$ whose transition on $c$ is not $q$; redirecting transitions that point elsewhere breaks the automaton.
- **Counting clones as occurrences.** A clone does not stand for a new end position. Giving it the initial count 1 overcounts: in $\texttt{abb}$ the count of $\texttt{b}$ would be 3.
- **Recursion over the link tree.** The link tree of $\texttt{a}^n$ is a path of length $n$. Sort the states by $len$ (a counting sort works, since $len \le n$) instead of a recursive walk.
- **Transitions as arrays for large alphabets.** An array of size $|\Sigma|$ at each of up to $2n - 1$ states is too large for byte or word alphabets; use hash maps or sorted lists.

## Implementations

## History

Blumer, Blumer, Ehrenfeucht, Haussler, Chen and Seiferas introduced the directed acyclic word graph (DAWG) in their 1985 paper, with the size bounds and the online linear-time construction. Crochemore (1986) studied the minimal suffix automaton and the factor automaton and gave linear-time constructions, and Blumer and others extended the DAWG to sets of strings in 1987. The name suffix automaton is now common, especially in Crochemore's books and in programming contests.

## References
