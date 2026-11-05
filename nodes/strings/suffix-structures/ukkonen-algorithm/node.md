---
tag: YN86V8
kind: algorithm
slug: ukkonen-algorithm
name: Ukkonen's algorithm
aliases:
- Ukkonen suffix tree construction
- online suffix tree construction
area: strings/suffix-structures
level: core
summary: Online linear-time suffix tree construction that extends the tree one character at a time.
solves: [suffix-tree-construction]
model: word-ram
complexity:
  vars: {n: the length of the text, σ: the size of the alphabet}
  time: {worst: O(n log σ), constant-alphabet: O(n)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false, online: true, comparison: false}
prereqs: [suffix-tree, suffix-link]
see_also: [implicit-suffix-tree, mccreight-algorithm, weiner-algorithm, suffix-tree-construction, suffix-tree-size-theorem, suffix-trie, blumer-algorithm, potential-method]
sources:
  - paper: doi:10.1007/BF01206331
    title: Esko Ukkonen, On-line construction of suffix trees, Algorithmica 14(3), 1995
    locator: pages 249 to 260; the online suffix trie, the boundary path, the active point and the end point, open transitions, and the linear time bound
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 6, Section 6.1, Ukkonen's linear-time suffix tree algorithm (the extension rules 1 to 3, the skip and count trick, and "once a leaf, always a leaf")
  - paper: doi:10.1007/pl00009177
    title: Robert Giegerich and Stefan Kurtz, From Ukkonen to McCreight and Weiner, a unifying view of linear-time suffix tree construction, Algorithmica 19(3), 1997
    locator: pages 331 to 353
---

Ukkonen's algorithm builds the [suffix tree](/suffix-tree/) of a string by reading it from left to right, one symbol at a time, and keeping after each symbol the [implicit suffix tree](/implicit-suffix-tree/) of the prefix read so far. Three tricks make the total time $O(n)$ for a constant alphabet: leaf edges are open and grow by themselves, a phase stops as soon as the new symbol is already present, and [suffix links](/suffix-link/) move between the places of consecutive suffixes. Appending a unique [sentinel](/sentinel-character/) at the end turns the implicit tree into the true suffix tree. Ukkonen published it in 1995 as a simpler, online form of McCreight's 1976 construction.

## In plain words

Read the text letter by letter. After each letter, the tree must hold every ending of the text read so far. When a new letter comes, every ending gets one letter longer, and one new ending of one letter appears.

Three things save work. First, an ending that already sits on its own leaf grows by itself: the leaf edge says "up to the current end", so nothing has to be done for it. Second, once a short ending is already in the tree, all shorter ones are too, so the work for this letter can stop. Third, after handling one ending, an arrow in the tree leads to the place of the next shorter ending, so the search does not restart at the top. In total, the work is in proportion to the length of the text.

## The problem

**Input.** A string $S = S[0 \ldots n-1]$, 0-based, given one symbol at a time, over an alphabet $\Sigma$ whose symbols can be keys of a child map (the code uses hash maps). For the time bound, $|\Sigma|$ is a constant, or the child maps are balanced trees and the time has a factor $\log |\Sigma|$.

**Output.** After reading $S[0 \ldots j]$, the implicit suffix tree $\mathcal{I}_j$: the compact trie of the suffixes of $S[0 \ldots j]$, in which a suffix may end inside an edge or at an inner node. After reading the sentinel $\$$, which is not in $S$, the tree $\mathcal{I}_n$ is the suffix tree of $S\$$, with one leaf for each of its $n + 1$ suffixes.

## The algorithm

Write $t = S\$$ and $t[a \ldots b)$ for $t[a \ldots b - 1]$. A *place* in the tree is a node, or a point inside an edge. The *active point* $(node, edge, length)$ is the place $length$ symbols down the child edge of $node$ that starts with $t[edge]$; with $length = 0$ it is $node$ itself. A leaf edge stores the end $-1$, which means "the current end of the text", so leaves grow without work. The counter $remainder$ is the number of suffixes that still have to be inserted explicitly. The phase for $t[j]$ is:

```pseudo id=main
UKKONEN(t)                                  ▷ t = S$, read online
L1  node ← root; edge ← 0; length ← 0; remainder ← 0
L2  for j ← 0 to n do                       ▷ phase j: add the symbol c = t[j]
L3      remainder ← remainder + 1; last ← NIL
L4      while remainder > 0 do              ▷ insert t[j − remainder + 1 .. j]
L5          if length = 0 then edge ← j
L6          if node has no child edge starting with t[edge] then
L7              add a leaf (j, open) under node; set link(last) ← node; last ← NIL
            else
L8              w ← that child; if length ≥ |label(w)| then go down to w; continue
L9              if t[start(w) + length] = c then length ← length + 1; set link(last) ← node; break
L10             split the edge into w at length by a new inner node u; add a leaf (j, open)
                under u; set link(last) ← u; last ← u
L11         remainder ← remainder − 1
L12         if node = root and length > 0 then length ← length − 1; edge ← j − remainder + 1
L13         else node ← link(node)              ▷ the root's link is the root
```

"Set link(last)" does nothing when $last$ is NIL. The new leaf in lines L7 and L10 is the leaf of the suffix that starts at $j - remainder + 1$.

**The three rules.** In Gusfield's terms, each suffix $t[i \ldots j-1]$ is extended by $c$ in one of three ways. *Rule 1:* it ends at a leaf; the open leaf edge extends it for free. *Rule 2:* it ends at a place where $c$ does not follow; add a leaf, after splitting the edge if the place is inside an edge (lines L7 and L10). *Rule 3:* $c$ already follows it; do nothing (line L9). The suffixes handled by rule 1 are the long ones, those by rule 3 the short ones, and the $remainder$ suffixes in the middle are those still waiting.

**Why a phase may stop at rule 3.** If $t[i \ldots j]$ is already in the tree, every shorter suffix $t[i' \ldots j]$, $i' > i$, is a substring of it and so also in the tree. The suffixes $t[i \ldots j]$ to $t[j \ldots j]$ stay implicit, and $remainder$ remembers how many there are; the active point is the place of the longest of them.

**Skip and count.** Line L8 moves down an edge by comparing only its length with $length$, not its symbols. This is correct because the string at the active point is known to be in the tree.

## Example

Take $S = \texttt{abab}$, $t = \texttt{abab\$}$.

| $j$ | $c$ | what happens | active point after | $remainder$ after | nodes |
|---|---|---|---|---|---|
| 0 | a | rule 2 at the root: leaf for suffix 0 | root | 0 | 2 |
| 1 | b | leaf 0 grows to ab (rule 1); rule 2 at the root: leaf for suffix 1 | root | 0 | 3 |
| 2 | a | leaves grow to aba, ba; $\texttt{a}$ is already on edge aba: rule 3 | (root, a, 1) | 1 | 3 |
| 3 | b | leaves grow to abab, bab; $\texttt{ab}$ is already there: rule 3 | (root, a, 2) | 2 | 3 |
| 4 | \$ | three inserts, see below | root | 0 | 8 |

Before phase 4 the implicit tree has only the root and two leaf edges, $\texttt{abab}$ and $\texttt{bab}$; the suffixes $\texttt{ab}$ and $\texttt{b}$ end inside them. Phase 4 has $remainder = 3$:

1. The active point $(\text{root}, \texttt{a}, 2)$ is inside the edge $\texttt{abab\$}$, and $\$$ does not follow. Line L10 splits it with the inner node $\texttt{ab}$ and adds the leaf of suffix 2. Then $remainder = 2$, and line L12 moves to $(\text{root}, \texttt{b}, 1)$.
2. Inside the edge $\texttt{bab\$}$, line L10 splits it with the inner node $\texttt{b}$, adds the leaf of suffix 3, and sets the suffix link $\texttt{ab} \to \texttt{b}$. Then $remainder = 1$ and the active point is the root.
3. At the root there is no edge for $\$$: line L7 adds the leaf of suffix 4 and sets the link $\texttt{b} \to$ root.

The final tree has the root, the inner nodes $\texttt{ab}$ and $\texttt{b}$, and 5 leaves, 8 nodes, as the [suffix tree size theorem](/suffix-tree-size-theorem/) allows.

## Correctness

The proof keeps, at the start of each phase $j$: (U1) the tree is the implicit suffix tree of $t[0 \ldots j-1]$, with open leaf edges; (U2) the suffixes $t[i \ldots j-1]$ for $i \le j - 1 - remainder$ end at leaves, and the others, $t[j - remainder \ldots j-1]$ down to the empty one, are present but do not end at leaves; (U3) the active point is the place of $t[j - remainder \ldots j-1]$; (U4) every inner node other than the last one created has a correct suffix link. The leaves handle rule 1. Each pass of the inner loop applies rule 2 to the longest waiting suffix, which turns it into a leaf, and moves the active point to the next shorter suffix, by line L12 at the root or by the suffix link in line L13 followed by skip and count. Rule 3 ends the phase with all shorter suffixes present. A new inner node $u$ for $x c'$ gets its link in the next pass, which handles $x$ and either stops at, finds, or creates the node of $x$. At the end, the sentinel makes all $n + 1$ suffixes end at leaves. The proof file gives the details.

## Complexity

**Leaves.** Each pass of the inner loop that does not break creates one leaf (lines L7 and L10), and a leaf stays a leaf forever. There are at most $n + 1$ leaves, so the inner loop runs at most $n + 1$ times with rule 2 and at most $n + 1$ times with rule 3 (once per phase), in total $O(n)$ times.

**Skip and count.** Each step of line L8 goes down one node. Consider the node depth of the active node, the number of nodes on its path from the root. A suffix link lowers it by at most one, because each ancestor of $node$ other than the root has a suffix link to an ancestor of $link(node)$, and these are different. Line L12 and the start of a phase do not raise it. The node depth never exceeds $n + 1$, and it drops by at most one in each of the $O(n)$ passes of the inner loop, so the total number of steps down in line L8 is $O(n)$.

**Total.** Each step costs $O(1)$ with constant-time child lookup, so the algorithm runs in $O(n)$ time for a constant alphabet and $O(n \log |\Sigma|)$ with balanced child maps. The tree has at most $2n + 1$ nodes, so the space is $O(n)$ words.

| resource | bound |
|---|---|
| time, constant alphabet or hashing | $O(n)$, expected for hashing |
| time, ordered child maps | $O(n \log \lvert\Sigma\rvert)$ |
| time of one phase | $O(n)$ worst, $O(1)$ amortized |
| space | $O(n)$ words |

## Properties

- **Online.** After each symbol, the tree indexes the prefix read so far: `contains(P)` works on the implicit tree at any time.
- **Not real-time.** One phase can take $\Theta(n)$ time, for example the sentinel phase of $\texttt{a}^n\$$, which inserts $n + 1$ leaves.
- **Uses no symbol order.** Only equality of symbols is tested; the order is needed only to list children in order afterwards.
- **Iterative.** No recursion, so it runs on long texts in Python without stack trouble.

## Variants and improvements

- **McCreight's algorithm.** Inserts the suffixes from the longest, with the same suffix links and skip and count; Giegerich and Kurtz show that Ukkonen's algorithm, restricted to the whole text, does the same steps. See [McCreight's algorithm](/mccreight-algorithm/).
- **Weiner's algorithm.** Inserts the suffixes from the shortest, reading the text from right to left. See [Weiner's algorithm](/weiner-algorithm/).
- **Online suffix trie.** Ukkonen's paper first builds the [suffix trie](/suffix-trie/) online with suffix links, in time proportional to its size, and then compacts it.
- **Generalized suffix tree.** Run the algorithm on several strings in turn, each with its own end marker, to get the [generalized suffix tree](/generalized-suffix-tree/).
- **Sliding window.** Variants keep the suffix tree of the last $w$ symbols, deleting the oldest leaf as each symbol enters, for Lempel-Ziv compression.
- **Suffix automaton.** The online construction of the [suffix automaton](/suffix-automaton/) by [Blumer and others](/blumer-algorithm/) has the same left-to-right, suffix-link-driven structure.

## When to use it

Use Ukkonen's algorithm when the text arrives as a stream and the index must be usable at any time, or when you want a linear-time suffix tree for a constant alphabet with one pass and no recursion. For a fixed large text, building the [suffix array](/suffix-array/) with [SA-IS](/sa-is/) and then the tree from the arrays is often faster and uses less memory, because suffix tree nodes with child maps are large and cause cache misses.

## Pitfalls

- **Setting the suffix link late or to the wrong node.** The link of a new inner node must be set in the next pass of the same phase, to the node where that pass inserts, splits, or stops by rule 3. Forgetting the rule 3 case leaves the link pointing at the root.
- **Wrong edge after the root step.** In line L12, the next suffix starts one symbol later, so the edge must be reset to $j - remainder + 1$; keeping the old edge symbol gives a wrong tree for strings such as $\texttt{abcabxabcd}$.
- **Comparing symbols during skip and count.** Line L8 must compare only lengths. Reading the symbols there is correct but loses the linear bound.
- **No sentinel.** Without the final $\$$, suffixes that are prefixes of other suffixes stay implicit, inside edges, with no leaf. Code that collects occurrences at leaves then misses them.
- **A sentinel that occurs in the text.** If $\$$ is a byte that also appears in $S$, the final tree is wrong. Use a value that cannot occur, as the code does with a private object.

## Implementations

## History

Esko Ukkonen presented the algorithm in 1992 and published it in Algorithmica in 1995. It was the third linear-time suffix tree construction, after Weiner (1973) and McCreight (1976), and the first online one that reads the text from left to right. Its presentation via the suffix trie, the boundary path and open edges made it the version most often taught; Gusfield's 1997 book presents it first, with the extension rules. Giegerich and Kurtz (1997) showed how the three classic algorithms relate.

## References
