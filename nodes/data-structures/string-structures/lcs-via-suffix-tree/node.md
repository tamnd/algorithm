---
tag: 2AY22B
kind: algorithm
slug: lcs-via-suffix-tree
name: Longest common substring via suffix tree
area: data-structures/string-structures
level: core
summary: Find the longest common substring by marking leaves of a generalized suffix tree and taking the deepest node with both marks.
solves: [longest-common-substring]
model: word-ram
complexity:
  vars: {n: the total length of the two strings}
  time: {worst: Θ(n)}
  space: {extra: Θ(n)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: true, comparison: false, recursive: false}
history:
  year: 1973
  people: [Peter Weiner]
  note: Weiner's paper on linear-time suffix tree construction gave the longest common substring of two strings in linear time as an application.
prereqs: [suffix-tree, generalized-suffix-tree, ukkonen-algorithm]
see_also: [longest-common-substring, generalized-suffix-tree, suffix-tree, ukkonen-algorithm, suffix-automaton, lcp-array, sentinel-character, distinct-substrings-counting]
sources:
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences
    locator: Section 7.4 (APL4, the longest common substring of two strings) and Section 6.4 (generalized suffix trees)
  - paper: Peter Weiner, Linear pattern matching algorithms, Proceedings of the 14th Annual Symposium on Switching and Automata Theory (SWAT 1973), doi:10.1109/SWAT.1973.13
    locator: pages 1 to 11, the position tree and its applications
  - paper: Esko Ukkonen, On-line construction of suffix trees, Algorithmica 14(3), 1995, doi:10.1007/BF01206331
    locator: pages 249 to 260, the online construction used by the implementation
---

The longest common substring of two strings $A$ and $B$ can be found in linear time with one [generalized suffix tree](/generalized-suffix-tree/): build the [suffix tree](/suffix-tree/) of $A \# B \$$, where $\#$ and $\$$ are new symbols, mark each leaf by the string its suffix starts in, and pass the marks up the tree. A node whose subtree has leaves of both strings spells a string that occurs in both, and the deepest such node, measured by the length of its path label, spells a longest common substring. The method takes $\Theta(\lvert A \rvert + \lvert B \rvert)$ time and space for a constant or integer alphabet, against $\Theta(\lvert A \rvert \lvert B \rvert)$ for the dynamic programming method. The problem itself is described on [longest common substring](/longest-common-substring/); this page is about the suffix tree algorithm.

## In plain words

Put both strings into one suffix tree, so that every ending of $A$ and every ending of $B$ is a path from the root to a leaf. Two endings share a path from the root for as long as they start with the same letters. So a point in the tree that is reached by an ending of $A$ and by an ending of $B$ spells letters that occur in both strings.

Color each leaf by the string its ending comes from. Then walk the tree from the bottom up and give each branching point the colors of the leaves below it. The branching points with both colors spell common pieces. Among them, pick the one farthest from the root in letters. Its path is the answer.

## The problem

**Input.** Strings $A$ and $B$ over an alphabet $\Sigma$, with $\lvert A \rvert + \lvert B \rvert = n$.

**Output.** A string $X$ of maximum length such that $X$ occurs in both $A$ and $B$, given as $(\ell, i, j)$ with $A[i .. i+\ell-1] = B[j .. j+\ell-1] = X$. If the strings share no symbol, $\ell = 0$.

## The algorithm

Let $\#$ and $\$$ be two different symbols not in $\Sigma$, and let $S = A \# B \$$. A suffix of $S$ that starts at a position $p \le \lvert A \rvert$ is an *$A$-suffix*, and the others are *$B$-suffixes*. The *string depth* $depth(v)$ of a node $v$ is the length of its path label $label(v)$.

```pseudo id=main
LCS-SUFFIX-TREE(A, B)
L1  S ← A · # · B · $
L2  build the suffix tree of S, for example with Ukkonen's algorithm
L3  for each node v of the tree in postorder:
L4      if v is a leaf for the suffix S[p ..] then mark(v) ← {A} if p ≤ |A| else {B}
L5      else mark(v) ← the union of mark(w) over the children w of v
L6      if mark(v) = {A, B} and depth(v) > best then best ← depth(v); v* ← v
L7  if no node was chosen then return (0, 0, 0) else return (best, the start of an A-suffix below v*, the start in B of a B-suffix below v*)
```

The string depths are computed in the same walk, top down: the depth of a child is the depth of its parent plus the length of the edge label. The start of the suffix of a leaf $v$ is $\lvert S \rvert - depth(v)$. Each node also keeps the start of one $A$-suffix and one $B$-suffix below it, taken from any child, so that line L7 can report positions. The answer $X$ is $label(v^*)$.

The terminator $\$$ makes every suffix of $S$ end at a leaf, since no suffix is then a prefix of another. The separator $\#$ stops a common prefix of an $A$-suffix and a $B$-suffix from running across the end of $A$.

## Example

Let $A$ = xabxac and $B$ = abcabxabcd, so $S$ = xabxac#abcabxabcd\$ has 18 symbols. Its suffix tree has 18 leaves, 10 inner nodes other than the root, and 29 nodes in all. The inner nodes with their path labels, string depths and marks are:

| label | depth | marks |
|---|---|---|
| a | 1 | A, B |
| ab | 2 | A, B |
| abc | 3 | B |
| abxa | 4 | A, B |
| b | 1 | A, B |
| bc | 2 | B |
| bxa | 3 | A, B |
| c | 1 | A, B |
| xa | 2 | A, B |
| xab | 3 | A, B |

The node "abxa" has two leaves below it: the $A$-suffix abxac#... at position 1 of $S$, and the $B$-suffix abxabcd\$ at position 10 of $S$, which is position 3 of $B$. It is the deepest node with both marks, so the answer is $X$ = abxa, with $(\ell, i, j) = (4, 1, 3)$. The nodes "abc" and "bc" are marked by $B$ only: "abc" occurs twice in $B$ and never in $A$.

## Correctness

The proof rests on one fact: a string $X \neq \varepsilon$ occurs in both $A$ and $B$ if and only if some $A$-suffix and some $B$-suffix of $S$ both start with $X$, and then the lowest node $v$ whose path label has $X$ as a prefix is an ancestor of two leaves of the two kinds, so $mark(v) = \{A, B\}$ and $depth(v) \ge \lvert X \rvert$. Conversely, the label of an inner node with both marks is a common prefix of an $A$-suffix and a $B$-suffix, and the separators keep it inside $A$ and inside $B$, so it is a common substring. So the maximum string depth over the nodes with both marks is the length of a longest common substring. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

**Time.** Building the suffix tree of $S$ takes $O(n)$ time for a constant alphabet with Ukkonen's algorithm, or for an integer alphabet with [Farach's algorithm](/farach-algorithm/). The tree has $n + 2$ leaves and at most $n + 1$ inner nodes, and the walk of lines L3 to L6 spends $O(1)$ per node and per edge, which is $O(n)$. With a constant number of marks, the union at line L5 is a bitwise OR. In total $\Theta(n)$.

**Space.** $\Theta(n)$ words for the tree, the marks and the depths.

**Comparison with other methods.**

| method | time | space |
|---|---|---|
| dynamic programming on all pairs of end positions | $\Theta(\lvert A \rvert \lvert B \rvert)$ | $O(\min(\lvert A \rvert, \lvert B \rvert))$ |
| this algorithm | $\Theta(n)$ | $\Theta(n)$ words |
| suffix array and [LCP array](/lcp-array/) of $S$, max LCP over neighbours from different strings | $\Theta(n)$ | $\Theta(n)$ words, with smaller constants |
| [suffix automaton](/suffix-automaton/) of $A$, then run $B$ through it | $O(n)$ | $O(\lvert A \rvert)$ |

## Properties

- **Deterministic and exact.** It always returns a longest common substring, with no randomness.
- **Non-comparison.** It indexes children by symbol, so it is not a comparison algorithm; with comparisons only, building the suffix tree costs $O(n \log \sigma)$.
- **Reusable index.** The same tree answers other questions about $A$ and $B$, such as all maximal common substrings, at no extra build cost.

## Variants and improvements

- **Several strings.** For $k$ strings $S_1, \ldots, S_k$ with $k$ different separators, the deepest node whose subtree has leaves of at least $m$ of the strings gives the longest substring common to at least $m$ of them. Counting the number of different colors below each node takes $O(n)$ total time with lowest common ancestor queries (Gusfield, Section 7.6).
- **All common substrings of length at least $L$.** Report every node with both marks and depth at least $L$; each is a maximal group of common substrings.
- **Suffix array form.** In the suffix array of $S$, a longest common substring is the maximum of $LCP[r]$ over the ranks $r$ where the suffixes of ranks $r - 1$ and $r$ come from different strings. This uses less memory and is the usual choice in practice.
- **Suffix automaton form.** Build the [suffix automaton](/suffix-automaton/) of $A$ and read $B$ through it, keeping the length of the longest suffix of the prefix of $B$ read so far that occurs in $A$; follow suffix links on a mismatch. The maximum of this length is the answer, using space proportional to $\lvert A \rvert$ only.
- **Smaller tree for one string.** Build the suffix tree of $A$ only, and walk $B$ through it with suffix links, as in matching statistics. This also uses $O(\lvert A \rvert)$ space.

## When to use it

Use it when the suffix tree of the strings is needed anyway, or when several such questions are asked about the same strings. For a single longest common substring query on long strings, the suffix array version or the suffix automaton version is simpler and uses less memory. For short strings, the $\Theta(\lvert A \rvert \lvert B \rvert)$ dynamic program is shorter to write and fast enough.

## Pitfalls

- **One separator only.** With $S = A B \$$ and no $\#$, a common prefix of an $A$-suffix and a $B$-suffix can run across the end of $A$ into $B$, and the answer can be a string that does not occur in $A$. The separator must be a symbol that occurs in neither string.
- **No terminator.** Without $\$$, some suffixes end inside edges, have no leaf, and get no mark.
- **Depth in edges.** The deepest node must be measured by string depth, the number of symbols on the path, not by the number of edges.
- **Leaf of the separator.** The suffix that starts at $\#$ counts as an $A$-suffix in line L4. Its label starts with $\#$, so it shares no prefix with a $B$-suffix and does no harm, but code that counts it as a $B$-suffix must still keep the separator out of the answer.
- **Recursion.** The postorder walk on a tree of depth up to $n$ must use an explicit stack in languages with a small call stack.

## Implementations

The Python implementation encodes the symbols of $A$ and $B$ by their code points, and uses $-1$ and $-2$ as the separator and the terminator, so that they cannot occur in the input. It builds the tree with Ukkonen's algorithm, storing leaf edges with an open end, and walks it in postorder with an explicit stack. The tests compare the length with the dynamic programming answer on random strings and check that the reported positions spell the same string in both inputs.

## History

Weiner introduced the suffix tree, under the name position tree, in 1973 and gave the longest common substring of two strings in linear time as one of its applications. Gusfield (Section 7.4) recounts that Knuth had conjectured that linear time was not possible for this problem, before Weiner's result. McCreight (1976) and Ukkonen (1995) gave simpler constructions of the tree. The version for many strings and the color counting with lowest common ancestors are due to Hui (1992).

## References
