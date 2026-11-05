---
tag: EG33JY
kind: algorithm
slug: esu-algorithm
name: ESU algorithm
aliases:
- Wernicke's ESU
area: graphs/network-analysis
level: advanced
summary: Enumerates connected k-subgraphs exactly once each by extension sets.
solves: [network-motif-enumeration]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, k: the size of the subgraphs, Δ: the largest degree, s: the number of connected vertex sets with at most k vertices}
  time: {worst: "O(n + m + k (k + Δ) s)"}
  space: {extra: "O(n + m + k^2 Δ)"}
properties: {deterministic: true, recursive: true}
history:
  year: 2005
  people: [Sebastian Wernicke]
  note: Presented at WABI 2005 and in full in the IEEE/ACM Transactions on Computational Biology and Bioinformatics in 2006, together with the sampling version RAND-ESU; the tool FANMOD implements both.
prereqs: [induced-subgraph, connected-graph, depth-first-search, network-motif]
see_also: [network-motif-enumeration, network-motif, subgraph-isomorphism, canonical-labeling, nauty, triangle-counting, graph-isomorphism-problem]
sources:
  - paper: doi:10.1109/TCBB.2006.51
    title: Sebastian Wernicke, Efficient detection of network motifs, IEEE/ACM Transactions on Computational Biology and Bioinformatics 3(4), 347 to 359 (2006)
    locator: Section 3, the algorithms ENUMERATESUBGRAPHS and EXTENDSUBGRAPH, the ESU-tree, and the lemma that each connected induced subgraph of size k is a leaf exactly once; Section 4, RAND-ESU and its unbiased sampling
  - paper: doi:10.1007/11557067_14
    title: Sebastian Wernicke, A faster algorithm for detecting network motifs, Algorithms in Bioinformatics, WABI 2005, Lecture Notes in Computer Science 3692, 165 to 177 (2005)
    locator: the first version of the ESU enumeration and of the sampling by the ESU-tree
  - paper: doi:10.1093/bioinformatics/btl038
    title: Sebastian Wernicke and Florian Rasche, FANMOD, a tool for fast network motif detection, Bioinformatics 22(9), 1152 to 1153 (2006)
    locator: the implementation of ESU and RAND-ESU, with nauty for the classification of the subgraphs
  - paper: doi:10.1093/bioinformatics/bth163
    title: N. Kashtan, S. Itzkovitz, R. Milo and U. Alon, Efficient sampling algorithm for estimating subgraph concentrations and detecting network motifs, Bioinformatics 20(11), 1746 to 1758 (2004)
    locator: the edge-sampling method that RAND-ESU replaces, and its bias
  - paper: doi:10.1126/science.298.5594.824
    title: R. Milo, S. Shen-Orr, S. Itzkovitz, N. Kashtan, D. Chklovskii and U. Alon, Network motifs, simple building blocks of complex networks, Science 298(5594), 824 to 827 (2002)
    locator: the counting of the subgraphs with 3 and 4 vertices that ESU speeds up
---

The ESU algorithm, short for *enumerate subgraphs*, lists every connected [induced subgraph](/induced-subgraph/) with $k$ vertices of a graph, each exactly once. It grows a connected set from its smallest vertex $v$, one vertex at a time, and takes each new vertex from an *extension set*: the neighbours of the current set that are larger than $v$ and that were not already neighbours of the set before the last vertex was added. This rule makes the search a tree whose leaves are exactly the connected $k$-sets, so no set is found twice and no table of found sets is needed. Sebastian Wernicke gave it in 2005 as the core of [network motif](/network-motif/) detection, where each set found is then classified by its isomorphism class; its sampling version RAND-ESU visits each branch at random and gives unbiased estimates of the counts.

## In plain words

Picture a group of people where some pairs are friends, and you want every team of $k$ people in which everyone is linked to the rest through friends in the team. Start with one person, the "captain", and let the team grow by inviting friends of team members, one at a time.

Two rules stop the same team from being built twice. First, the captain is always the member with the smallest number, so a team is built only from its own captain. Second, when you decide not to invite someone who was on the list, you never put them back on it later. A newly invited member can only add friends who were not already within reach. Every team then has exactly one way to be built.

## The problem

The input is a simple undirected [graph](/graph/) $G = (V, E)$ with $V = \{0, 1, \dots, n-1\}$ and $m$ edges, and an integer $k \ge 1$. The numbers of the vertices give the order that the method uses. For $S \subseteq V$, let $N(S)$ be the set of vertices outside $S$ that have a neighbour in $S$, and $N[S] = S \cup N(S)$.

The output is every set $S \subseteq V$ with $|S| = k$ whose induced subgraph $G[S]$ is [connected](/connected-graph/), each exactly once. For [network motif enumeration](/network-motif-enumeration/), each $S$ is then given the isomorphism class of $G[S]$, for example by a [canonical labeling](/canonical-labeling/) with [nauty](/nauty/), and the classes are counted.

**Directed graphs.** A motif in a directed graph is a weakly connected induced subgraph. Run ESU on the underlying undirected graph, which lists the same vertex sets, and classify each $G[S]$ with its arcs.

## The algorithm

```pseudo id=main
ESU(G, k)
L1  for each vertex v of G, in increasing order do
L2      ext ← {u ∈ N(v) : u > v}
L3      EXTEND({v}, ext, v)
L4  return

EXTEND(sub, ext, v)
L5  if |sub| = k then
L6      output sub; return
L7  while ext ≠ ∅ do
L8      remove a vertex w from ext
L9      ext′ ← ext ∪ {u ∈ N(w) : u > v and u ∉ N[sub]}
L10     EXTEND(sub ∪ {w}, ext′, v)
```

The vertices that line L9 adds are the *exclusive neighbours* of $w$: neighbours of $w$ that are not in $sub$ and not adjacent to $sub$. A vertex that was in $N(sub)$ and was removed from $ext$ at line L8 stays out of every later extension set of this branch, and this is what keeps the sets apart.

**The ESU-tree.** The calls form a tree: the root has the children $\{v\}$ for each vertex $v$, and each call of EXTEND has one child for each vertex it removes at line L8. Its leaves at depth $k$ are the output. Line L8 may take the vertices in any order; the output set does not depend on it. The implementation keeps $ext$ as a list and takes its first vertex.

**Ties and disconnected graphs.** There are no ties, since every choice is fixed by the order of the vertices and of $ext$. A set is never extended across components, so a graph whose components all have fewer than $k$ vertices has no output, and an isolated vertex appears only for $k = 1$. For $k > n$ the output is empty.

## Example

Take the vertices 0 to 4 and the edges $\{0,1\}$, $\{0,2\}$, $\{1,2\}$, $\{1,4\}$, $\{2,3\}$, $\{3,4\}$, a 5-cycle $0, 1, 4, 3, 2$ with the chord $\{1, 2\}$, and $k = 3$. Each row is a call of EXTEND, with $ext$ as it is when the call starts; indentation shows depth.

| call | $sub$ | $ext$ | result |
|---|---|---|---|
| root 0 | $\{0\}$ | $[1, 2]$ | |
| &nbsp;&nbsp;take 1 | $\{0, 1\}$ | $[2, 4]$ | 4 is an exclusive neighbour of 1 |
| &nbsp;&nbsp;&nbsp;&nbsp;take 2 | $\{0, 1, 2\}$ | | output |
| &nbsp;&nbsp;&nbsp;&nbsp;take 4 | $\{0, 1, 4\}$ | | output |
| &nbsp;&nbsp;take 2 | $\{0, 2\}$ | $[3]$ | 1 is not added back: it is in $N(\{0\})$ |
| &nbsp;&nbsp;&nbsp;&nbsp;take 3 | $\{0, 2, 3\}$ | | output |
| root 1 | $\{1\}$ | $[2, 4]$ | 0 is smaller than 1 |
| &nbsp;&nbsp;take 2 | $\{1, 2\}$ | $[4, 3]$ | |
| &nbsp;&nbsp;&nbsp;&nbsp;take 4 | $\{1, 2, 4\}$ | | output |
| &nbsp;&nbsp;&nbsp;&nbsp;take 3 | $\{1, 2, 3\}$ | | output |
| &nbsp;&nbsp;take 4 | $\{1, 4\}$ | $[3]$ | |
| &nbsp;&nbsp;&nbsp;&nbsp;take 3 | $\{1, 3, 4\}$ | | output |
| root 2 | $\{2\}$ | $[3]$ | |
| &nbsp;&nbsp;take 3 | $\{2, 3\}$ | $[4]$ | |
| &nbsp;&nbsp;&nbsp;&nbsp;take 4 | $\{2, 3, 4\}$ | | output |
| root 3 | $\{3\}$ | $[4]$ | |
| &nbsp;&nbsp;take 4 | $\{3, 4\}$ | $[\,]$ | dead end |
| root 4 | $\{4\}$ | $[\,]$ | dead end |

The output is the 7 sets $\{0,1,2\}$, $\{0,1,4\}$, $\{0,2,3\}$, $\{1,2,4\}$, $\{1,2,3\}$, $\{1,3,4\}$, $\{2,3,4\}$. The other 3 of the $\binom{5}{3} = 10$ sets, $\{0,1,3\}$, $\{0,2,4\}$ and $\{0,3,4\}$, are not connected. Classifying them gives 1 triangle, $\{0,1,2\}$, and 6 paths. The call for $\{3, 4\}$ shows that a branch can end without output.

## Correctness

Two invariants hold at each call EXTEND($sub$, $ext$, $v$): $sub$ is connected, holds $v$ and otherwise only vertices larger than $v$; and $ext \subseteq N(sub)$ holds only vertices larger than $v$. So each output is a connected set of $k$ vertices with smallest vertex $v$.

**Each set at most once.** Let a call remove $w_1, w_2, \dots, w_r$ from $ext$ in this order. Each $w_j$ lies in $N(sub)$, and it is not in the extension set of the child of any later $w_i$: line L8 removed it, and line L9 adds only vertices outside $N[sub]$, a set that only grows along a branch. So every set below the child of $w_j$ contains $w_j$, and no set below the child of $w_i$, for $i > j$, does. Sets in different subtrees differ, and the roots differ in their smallest vertex.

**Each set at least once.** Let $S$ be connected, with $|S| = k$ and smallest vertex $v$. Follow from the root $\{v\}$ the branch that, at each call, takes the first vertex of $S$ that line L8 removes. Along it, $sub \subseteq S$ and every vertex of $S \setminus sub$ that is adjacent to $sub$ is in $ext$; since $S$ is connected, such a vertex exists until $sub = S$, which is output. The full proof is in [the proof page](proofs/correctness.md).

## Complexity

- **The size of the tree.** By the argument above, two calls never have the same $sub$, so the ESU-tree has at most $s$ calls of EXTEND, where $s$ is the number of connected sets with at most $k$ vertices. Each call at depth $j$ has $|ext| \le |N(sub)| \le j\Delta$, so $s \le n \sum_{j<k} j!\,\Delta^{j}$, which is $O(n (k-1)!\,\Delta^{k-1})$ for $\Delta \ge 2$.
- **One call.** Copying $ext$, scanning $N(w)$ and updating $N[sub]$ cost $O(k\Delta)$, and sorting an output set costs $O(k \log k)$, so a call costs $O(k(k + \Delta))$.
- **Total time.** Building the adjacency lists costs $O(n + m)$, so the time is $O(n + m + k(k + \Delta)\, s)$. The leaves are at least the output, but a branch can die before depth $k$, as in the example, so the time is not bounded by the output alone: a graph whose components all have fewer than $k$ vertices has no output and $s > 0$.
- **Space.** The recursion has depth $k$, and each level keeps a list $ext$ and a set $N[sub]$ of $O(k\Delta)$ vertices, so the extra space is $O(n + m + k^2 \Delta)$, apart from the output.

## Properties

- **No duplicate check.** Each set is produced once by the structure of the search, so ESU keeps no hash table of found sets, unlike methods that grow sets from every vertex.
- **Order-free.** The set of outputs does not depend on the order in which line L8 takes vertices, only on the numbering of the vertices.
- **Unique paths.** Each output leaf has a unique path from the root, which is what RAND-ESU uses.
- **Not output-linear.** Dead branches cost time; in graphs with many small components or long paths, they can outnumber the leaves.

## Variants and improvements

- **RAND-ESU.** Fix probabilities $p_1, \dots, p_k$ and enter each child at depth $d$ with probability $p_d$. Since each connected $k$-set has one path from the root, it is reached with probability exactly $\prod_d p_d$, so the count of a class divided by this product is an unbiased estimate of its true count. Smaller $p_d$ near the leaves cut the most work, since the deep levels of the tree usually hold most of the calls.
- **Classification.** For $k \le 4$ or so, a table indexed by the adjacency bits of $G[S]$ in a fixed vertex order replaces a call to nauty.
- **Without recursion.** An explicit stack of $(sub, ext, N[sub])$ frames avoids deep calls and copies.
- **Counting without listing.** Methods based on relations between graphlet counts, or on color-coding, count the classes without visiting each set; see [network motif enumeration](/network-motif-enumeration/).

## When to use it

Use ESU to list or count all connected induced subgraphs of size 3 to about 8 in a sparse graph, for [network motif](/network-motif/) detection or graphlet degree statistics, or RAND-ESU for estimates when the number of sets is too large. For triangles alone, a dedicated [triangle counting](/triangle-counting/) method is far faster. For a fixed pattern, not all patterns of a size, use [subgraph isomorphism](/subgraph-isomorphism/) search.

## Pitfalls

- **Forgetting the closed neighbourhood.** Line L9 must exclude $N[sub]$, not only $sub$. Excluding only $sub$ puts back the vertices that an earlier sibling took, and sets are listed many times.
- **Updating $N[sub]$ in place.** The set must be restored after each child returns, or copied per call; otherwise siblings see the neighbours of the previous child.
- **The condition $u > v$.** It compares with the root $v$, not with $w$. Comparing with $w$ loses sets whose vertices are not added in increasing order.
- **Expecting few outputs.** The number of connected $k$-sets of a graph with a vertex of large degree is of order $\Delta^{k-1}$; a hub of degree $10^4$ and $k = 4$ already gives about $10^{11}$ sets.

## Implementations

## History

Milo and co-authors introduced network motifs in 2002 and counted subgraphs with 3 and 4 vertices by full enumeration in the real network and in many random ones. Kashtan, Itzkovitz, Milo and Alon gave in 2004 an edge-sampling estimator whose sampling probabilities are unequal and need a correction. Sebastian Wernicke presented ESU and RAND-ESU at WABI 2005 and in a journal version in 2006, and with Florian Rasche released the tool FANMOD, which classifies the sets with nauty and was much faster than the earlier tools for sizes up to 8.

## References
