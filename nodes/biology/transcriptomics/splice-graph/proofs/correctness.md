---
title: The splice graph is a DAG in which every input alignment is a path, every edge comes from an alignment, and the path count is right
proves: [correctness]
status: full
---

We use the BUILD pseudocode of the page and its 0-based, half-open coordinates. An alignment $a$ is a list of blocks $[s_1, e_1), \ldots, [s_r, e_r)$ with $s_i < e_i$ and $e_i < s_{i+1}$. Each pair $(e_i, s_{i+1})$ is an intron with donor $e_i$ and acceptor $s_{i+1}$. Let $B$ be the set of all blocks of all alignments, $I$ the set of introns, $C$ the set of donors and acceptors (line L2), and $U = \bigcup B$ the covered bases.

## 1. The nodes

Line L3 merges the blocks into the maximal intervals $[x, y)$ of $U$; blocks that touch or overlap are merged. Line L4 cuts each such interval at the points of $C$ strictly inside it. So the nodes are disjoint intervals that partition $U$, and they are numbered in coordinate order.

**Lemma 1.** A point $p$ is the end of one node and the start of the next node if and only if $p$ is inside a maximal interval of $U$ and $p \in C$. Every point of $C$ is a node boundary: each donor is the end of a node and each acceptor is the start of a node.

*Proof.* The first sentence is the definition of line L4. A donor $d = e_i$ is the end of a block, so $d - 1 \in U$. Either $d$ is the end of a maximal interval of $U$, and then the last node of that interval ends at $d$, or $d$ is strictly inside a maximal interval, and then line L4 cuts at $d$. In both cases a node ends at $d$. An acceptor $s_{i+1}$ is the start of a block, and the same argument gives a node that starts there. $\square$

So no node holds a donor or an acceptor strictly inside it, and the nodes are the largest intervals with this property: two nodes that touch are separated by a point of $C$, and two nodes that do not touch are separated by uncovered bases. The test file checks this against a position-by-position definition.

## 2. Every alignment is a path

For a block $[s, e)$, let $\mathrm{span}(s, e)$ be the nodes that overlap it, in order. Line L5 adds an edge between each pair of consecutive nodes of each span.

**Lemma 2.** The nodes of $\mathrm{span}(s, e)$ are consecutive and each one ends where the next starts.

*Proof.* The block lies inside one maximal interval of $U$, because it is covered. Inside that interval the nodes are consecutive and touch, by line L4. The nodes that overlap $[s, e)$ form a contiguous run of them. $\square$

**Theorem 1.** For every input alignment $a$, the list $\mathrm{path}(a)$, which is the concatenation of the spans of its blocks, is a path of the graph. Its spelled exons have the same introns as $a$.

*Proof.* Inside one block, consecutive nodes are joined by line L5. Between blocks $i$ and $i + 1$, the last node of $\mathrm{span}(s_i, e_i)$ ends at $e_i$, because by Lemma 1 a node ends at $e_i$ and the bases $e_i - 1$ and $e_i$ are in different nodes. In the same way the first node of the next span starts at $s_{i+1}$. Line L6 adds exactly the edge from the node that ends at $e_i$ to the node that starts at $s_{i+1}$. So every consecutive pair of $\mathrm{path}(a)$ is an edge. Merging the nodes of each span gives one exon per block, which ends at $e_i$ and starts at $s_{i+1}$ at each intron. $\square$

## 3. Every edge comes from an alignment, and the graph is acyclic

**Theorem 2.** The edge set equals the set of consecutive pairs of $\mathrm{path}(a)$ over all input alignments $a$. Every edge $(u, v)$ has $\mathrm{end}(u) \le \mathrm{start}(v)$, so $u < v$, and the graph is a DAG in which the node order is a topological order.

*Proof.* Line L5 adds the consecutive pairs inside spans, and line L6 adds the pairs at introns; by the proof of Theorem 1 these are exactly the consecutive pairs of the paths, and the lines add nothing else. An edge of line L5 joins touching nodes, so $\mathrm{end}(u) = \mathrm{start}(v)$. An edge of line L6 goes from a node ending at a donor $e_i$ to a node starting at $s_{i+1} > e_i$. Node ids follow coordinates, so $u < v$ for every edge, and no cycle exists. $\square$

## 4. Counting and listing paths

COUNT-PATHS sets $w(v) = 1$ for a source and $w(v) = \sum_{(u, v)} w(u)$ otherwise, in increasing order of $v$, and returns $\sum_{v \text{ sink}} w(v)$.

**Theorem 3.** $w(v)$ is the number of paths from a source to $v$, so the result is the number of source-to-sink paths.

*Proof.* By induction on $v$. All predecessors $u$ of $v$ have $u < v$ by Theorem 2, so $w(u)$ is final when $v$ is processed. A source has only the one-node path. A path from a source to a non-source $v$ ends with exactly one edge $(u, v)$, and removing it leaves a path from a source to $u$; this is a bijection, so the count is $\sum_u w(u)$. $\square$

The listing of all paths by depth-first search from every source is correct for the same reason: in a DAG every walk is a path, every extension by an edge is explored, and the search stops at sinks. The test file compares both with a brute force over all subsets of nodes.

## 5. What is not true

A source-to-sink path need not be a transcript: the graph also holds every combination of the splice choices, also those that no input alignment has. And a transcript need not be a source-to-sink path: if two alignments start at different points of the same exon, the node that holds both starts is the same, and the graph forgets which start was used. Both are limits of the model, not errors of the construction. $\blacksquare$
