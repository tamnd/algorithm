---
tag: AQCD8D
kind: theorem
slug: suffix-automaton-size-theorem
name: Suffix automaton size theorem
aliases:
- linear size of suffix automata
area: strings/suffix-structures
level: core
summary: A suffix automaton of an n-character string has at most 2n-1 states and 3n-4 transitions.
prereqs: [suffix-automaton]
see_also: [suffix-tree-size-theorem, blumer-algorithm, suffix-automaton-construction, suffix-link, myhill-nerode-relation, minimal-dfa-uniqueness, distinct-substrings-counting, suffix-trie]
sources:
  - paper: doi:10.1016/0304-3975(85)90157-4
    title: A. Blumer, J. Blumer, D. Haussler, A. Ehrenfeucht, M. T. Chen and J. Seiferas, The smallest automaton recognizing the subwords of a text, Theoretical Computer Science 40, 1985
    locator: pages 31 to 55; the bounds of 2n − 1 states and 3n − 4 edges for n ≥ 3, and the strings that reach them
  - paper: doi:10.1016/0304-3975(86)90041-1
    title: Maxime Crochemore, Transducers and repetitions, Theoretical Computer Science 45, 1986
    locator: pages 63 to 86; the size of the minimal suffix automaton
  - book: isbn:9780521848992
    title: Maxime Crochemore, Christophe Hancart and Thierry Lecroq, Algorithms on Strings, Cambridge University Press, 2007
    locator: Chapter 5, Structures for indexes (the bounds on the number of states and arcs of the suffix automaton)
---

The [suffix automaton](/suffix-automaton/) of a string of length $n$ has at most $2n - 1$ states for $n \ge 2$ and at most $3n - 4$ transitions for $n \ge 3$. Both bounds are tight: $\texttt{ab}^{n-1}$ reaches $2n - 1$ states, and $\texttt{ab}^{n-2}\texttt{c}$ reaches $3n - 4$ transitions. So, although the automaton recognizes all $\Theta(n^2)$ substrings, it has linear size, independent of the alphabet. Blumer, Blumer, Haussler, Ehrenfeucht, Chen and Seiferas proved the bounds in 1985.

## Statement

Let $S = S[0 \ldots n-1]$ be a string over any alphabet, 0-based, with no sentinel. The suffix automaton of $S$ is the minimal deterministic automaton that accepts the suffixes of $S$, without the dead state. Its states are the classes of substrings of $S$ with the same set $endpos$ of end positions, with $\{\varepsilon\}$ as the initial state, and its transitions go from the class of $x$ to the class of $xc$ whenever $xc$ is a substring.

**Theorem.**

1. **(States.)** For $n \ge 2$, the automaton has at most $2n - 1$ states. Equality holds if and only if $S = \texttt{a}\texttt{b}^{n-1}$ for two different symbols $\texttt{a}, \texttt{b}$.
2. **(Transitions.)** For $n \ge 3$, the automaton has at most $3n - 4$ transitions. Equality holds for $S = \texttt{a}\texttt{b}^{n-2}\texttt{c}$ with three different symbols.
3. **(Lower bounds.)** It always has at least $n + 1$ states and at least $n$ transitions, with equality for $S = \texttt{a}^n$.

For $n = 1$ there are 2 states and 1 transition.

## In plain words

The automaton groups the pieces of the text by the places where they end. A new letter at the end of the text can change the grouping in only two places: the whole text gets a new group, and at most one old group splits into two. So each letter adds at most two groups, and the first two letters add only one each. That gives at most $2n - 1$ groups.

The arrows between groups come in two kinds. The main arrows form a tree, one into each group. Each other arrow can be matched with a different ending of the text, and there are fewer than $n$ such endings. So the number of arrows is also small.

## Proof

Write $len(v)$ for the length of the longest string $long(v)$ of a state $v$. We use the online construction of the [suffix automaton](/suffix-automaton/) page, whose correctness is proved there: adding a symbol $c$ to $S$ creates one new state $cur$, and at most one more, a clone, which happens only when the walk of line L3 stops at a state $p$ with a transition on $c$, that is, when $c$ already occurs in $S$ after some suffix of $S$.

**States.** The automaton of the empty string has 1 state. Adding $S[0]$ creates no clone, since the initial state has no transitions yet. Adding $S[1]$ creates no clone: the walk either reaches NIL or stops at the initial state with a transition to the state of $S[0]$, whose length is $1 = 0 + 1$, so line L5 applies. Each later symbol adds at most 2 states. So for $n \ge 2$ there are at most $1 + 1 + 1 + 2(n - 2) = 2n - 1$ states.

*Equality.* All $n - 2$ steps after the second one must clone. If $S[1] = S[0] = \texttt{a}$, the third symbol either is $\texttt{a}$, and the walk stops at the state of $\texttt{a}$ with the transition to the state of $\texttt{aa}$ of length 2, no clone; or is new, no clone. So $S[1] = \texttt{b} \ne \texttt{a}$. Now let $S[0 \ldots k] = \texttt{ab}^k$ with $k \ge 1$, and add $c$. A clone needs $c$ to occur already, so $c \in \{\texttt{a}, \texttt{b}\}$. If $c = \texttt{a}$: no nonempty suffix $\texttt{b}^i$ or $\texttt{ab}^k$ is followed by $\texttt{a}$ in $S$, so the walk stops at the initial state, whose transition on $\texttt{a}$ goes to the state $\{\texttt{a}\}$ of length 1 (the only string ending at position 0); no clone. So $c = \texttt{b}$, and by induction $S = \texttt{ab}^{n-1}$. Conversely, the states of $\texttt{ab}^{n-1}$ are $\{\varepsilon\}$, $\{\texttt{a}\}$, $\{\texttt{ab}^i\}$ for $1 \le i \le n - 2$, $\{\texttt{b}^i\}$ for $1 \le i \le n - 2$, and $\{\texttt{b}^{n-1}, \texttt{ab}^{n-1}\}$: in total $2 + 2(n - 2) + 1 = 2n - 1$.

**Transitions.** Call a transition $u \xrightarrow{c} w$ *solid* if $len(w) = len(u) + 1$, and *soft* otherwise.

*Solid transitions: one into each state other than the initial one.* For $w \ne$ initial, write $long(w) = yc$. The state $u$ of $y$ has $len(u) \ge |y|$, and $long(u)c$ is in $w$ (by the well-definedness of transitions), so $len(u) + 1 \le len(w) = |y| + 1$. So $len(u) = |y|$, and $u \xrightarrow{c} w$ is solid. If $u' \xrightarrow{c'} w$ is also solid, then $long(u')c'$ is a string of $w$ of length $len(w)$, so it equals $long(w) = yc$, and $u' = u$, $c' = c$. So there are exactly (number of states $- 1$) solid transitions.

*Prefixes of longest strings are longest.* If $v$ is a state and $y$ a prefix of $long(v)$, then $y$ is the longest string of its state. Otherwise some $zy$ with $z$ nonempty has $endpos(zy) = endpos(y)$; then every occurrence of $y$ is preceded by $z$, so every occurrence of $long(v) = yr$ is preceded by $z$, and $z \cdot long(v)$ is in $v$, a contradiction. Reading $long(v)$ from the initial state therefore uses only solid transitions: the state reached after each prefix $y$ has $len = |y|$. The same argument applies to $S$ itself, which is the longest string of its state, and to its prefixes.

*Soft transitions: at most $n - 1$.* Map a soft transition $u \xrightarrow{c} w$ to a nonempty suffix $\sigma = long(u)\, c\, r$ of $S$, choosing any $r$ that extends the substring $long(u)c$ to a suffix. Reading $\sigma$ from the initial state first reads $long(u)$ by solid transitions only, then takes the soft transition $u \xrightarrow{c} w$. So the transition is the first soft transition on the path of $\sigma$, and different soft transitions are mapped to different suffixes. The path of $S$ itself has no soft transition, so $S$ is not in the image. The image therefore lies among the $n - 1$ nonempty proper suffixes of $S$.

*Total.* The number of transitions is at most (states $- 1$) $+ (n - 1)$. If the automaton has at most $2n - 2$ states, this is at most $3n - 4$. If it has $2n - 1$ states, then $S = \texttt{ab}^{n-1}$, whose transitions are counted directly: two from $\{\varepsilon\}$, one from $\{\texttt{a}\}$, one from each $\{\texttt{ab}^i\}$ and each $\{\texttt{b}^i\}$ with $i \le n - 2$, and none from the last state, $2n - 1$ in total, which is at most $3n - 4$ for $n \ge 3$.

**Lower bounds.** The prefixes $S[0 \ldots e]$, $0 \le e < n$, have pairwise different smallest end positions, so they lie in $n$ different states, which are also different from $\{\varepsilon\}$: at least $n + 1$ states. The solid transitions alone number states $- 1 \ge n$. For $\texttt{a}^n$ the states are $\{\texttt{a}^i\}$ for $0 \le i \le n$ and the transitions are $\texttt{a}^i \to \texttt{a}^{i+1}$. $\blacksquare$

## Consequences

- **Linear space for any alphabet.** With transitions in hash maps or sorted lists, the automaton takes $O(n)$ words even when the alphabet is large, unlike a trie with arrays of children.
- **Linear-time construction.** The bound on the number of clones is the starting point of the amortized analysis of the [Blumer algorithm](/blumer-algorithm/): the total work of the walks is $O(n)$.
- **Distinct substrings and occurrence counts in $O(n)$.** Any computation that does constant work for each state and transition, such as counting [distinct substrings](/distinct-substrings-counting/) or the occurrences of each class, runs in linear time.
- **The suffix link tree.** The states, with the suffix links as parent pointers, are the nodes of the suffix tree of the reversed string in which the nodes of all its suffixes are explicit. So the bound $2n - 1$ also bounds that tree, in line with the [suffix tree size theorem](/suffix-tree-size-theorem/).

## Tightness

| $S$ | $n$ | states | transitions |
|---|---|---|---|
| $\texttt{aaaa}$ | 4 | 5 | 4 |
| $\texttt{abbb}$ | 4 | 7 = $2n - 1$ | 7 |
| $\texttt{abbc}$ | 4 | 6 | 8 = $3n - 4$ |
| $\texttt{abbbbc}$ | 6 | 10 | 14 = $3n - 4$ |

An exhaustive search over all strings of length up to 9 over two and three letters finds that the maximum number of states is $2n - 1$, reached only by $\texttt{ab}^{n-1}$ up to renaming, and the maximum number of transitions is $3n - 4$ for $n \ge 3$, reached by $\texttt{ab}^{n-2}\texttt{c}$ and, for $n = 3$, also by strings such as $\texttt{aab}$. The two maxima are not reached by the same string for $n \ge 4$, so the total size is less than $5n - 5$.

## History

Blumer, Blumer, Haussler, Ehrenfeucht, Chen and Seiferas proved both bounds in their 1985 paper on the directed acyclic word graph, together with the strings that reach them, and gave the online linear-time construction. Crochemore (1986) obtained the same linear size for the minimal suffix automaton and studied the factor automaton, whose size bounds are similar.

## References
