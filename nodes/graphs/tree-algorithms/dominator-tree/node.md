---
tag: GK1MNC
kind: data-structure
slug: dominator-tree
name: Dominator tree
aliases:
- dominators tree
area: graphs/tree-algorithms
level: advanced
summary: Tree in which each vertex's parent is its immediate dominator in a flow graph.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {build: O(m log n), query: O(1)}
  space: {extra: Θ(n)}
prereqs: [dominators-problem, rooted-tree, euler-tour-technique, depth-first-search]
see_also: [lengauer-tarjan-algorithm, dominators-problem, lowest-common-ancestor, euler-tour-subtree-queries, block-cut-tree, transpose-graph, strongly-connected-components, directed-acyclic-graph]
sources:
  - paper: doi:10.1145/357062.357071
    title: "Thomas Lengauer and Robert Endre Tarjan, A fast algorithm for finding dominators in a flowgraph, ACM Transactions on Programming Languages and Systems 1(1) (1979), 121-141"
    locator: Section 1 (Lemma 1, the dominators of a vertex are its ancestors in the tree defined by idom) and Section 3 (the computation of idom)
  - paper: "Ron Cytron, Jeanne Ferrante, Barry K. Rosen, Mark N. Wegman and F. Kenneth Zadeck, Efficiently computing static single assignment form and the control dependence graph, ACM Transactions on Programming Languages and Systems 13(4) (1991), 451-490"
    locator: the dominance frontier, computed by a bottom-up walk of the dominator tree, and its use to place phi-functions
  - book: isbn:9780521820608
    title: Andrew W. Appel with Jens Palsberg, Modern Compiler Implementation in Java, second edition
    locator: Chapter 18 (Loop optimizations, the section on dominators and the dominator tree) and Chapter 19 (Static single-assignment form, the dominance frontier and the efficient computation of the dominator tree)
  - url: https://www.cs.rice.edu/~keith/EMBED/dom.pdf
    title: "Keith D. Cooper, Timothy J. Harvey and Ken Kennedy, A Simple, Fast Dominance Algorithm"
    locator: the representation of all dominator sets by the idom array, and the dominance-frontier algorithm
---

The dominator tree of a flow graph $G$ with start vertex $r$ has the vertices reachable from $r$, with $r$ as root and the [immediate dominator](/dominators-problem/) $\mathrm{idom}(v)$ as the parent of every other vertex $v$. Its key property is that the dominators of $v$, the vertices that lie on every path from $r$ to $v$ in $G$, are exactly the ancestors of $v$ in the tree. So the whole dominance relation, which can have $\Theta(n^2)$ pairs, is stored in $n$ numbers, and with entry and exit times from one walk of the tree, the question "does $a$ dominate $b$" takes $O(1)$ time. The tree is built in $O(m \log n)$ time by the [Lengauer-Tarjan algorithm](/lengauer-tarjan-algorithm/) and is the central structure of optimizing compilers.

## In plain words

Picture a building with one entrance and one-way doors between rooms. A room guards another room if every way from the entrance to the second room goes through the first. For each room, the nearest guard is the last room you are forced to pass on any way in.

Draw an arrow from each room to its nearest guard. The arrows form a family tree with the entrance at the top. The surprising part is that all the guards of a room are exactly the rooms above it in this family tree, no more and no fewer. So one small tree answers every question about guards, and with a stopwatch reading from one walk around the tree, each question takes a single comparison.

## The abstract type

A flow graph is a directed graph with vertices $0, \ldots, n - 1$, $m$ edges and a start vertex $r$. It is unweighted; self-loops and parallel edges are allowed. The tree is rooted at $r$, and its vertices keep their numbers from $G$. Vertices that $r$ cannot reach are not in the tree.

- **BUILD$(G, r)$.** Build the structure.
- **IDOM$(v)$.** The parent of $v$, or none for $r$ and for unreachable vertices.
- **DOMINATES$(a, b)$.** True if every path from $r$ to $b$ contains $a$. A vertex dominates itself; an unreachable vertex dominates nothing and is dominated by nothing.
- **DOMINATORS$(v)$.** The list of dominators of $v$, from $v$ up to $r$.
- **CHILDREN$(v)$.** The vertices whose immediate dominator is $v$.

The structure is static: a change of $G$ needs a new build.

## Representation

- $idom[0 .. n - 1]$: the parent of each vertex, with $-1$ for $r$ and for unreachable vertices.
- $children[v]$: the list of children, ordered by label.
- $tin[v]$ and $tout[v]$: the entry time of $v$ and the exit time of its subtree in a preorder walk of the tree, so that the subtree of $v$ has entry times $tin[v], \ldots, tout[v] - 1$, as in the [Euler tour technique](/euler-tour-technique/).
- $depth[v]$: the depth in the tree, the number of strict dominators of $v$.

All arrays have length $n$, so the space is $\Theta(n)$, independent of $m$.

## Operations

```pseudo id=main
BUILD(G, r)
L1  idom ← the immediate dominators of G from r     ▷ Lengauer-Tarjan, O(m log n)
L2  for each reachable v ≠ r, by label, do append v to children[idom(v)]
L3  t ← 0; S ← stack holding (r, enter)
L4  while S is not empty do
L5      pop (v, phase) from S
L6      if phase = enter then tin[v] ← t; t ← t + 1; push (v, exit); push (c, enter) for each child c, last child first
L7      else tout[v] ← t

DOMINATES(a, b)
L8  if a or b is not reachable from r then return false
L9  return tin[a] ≤ tin[b] and tout[b] ≤ tout[a]

DOMINATORS(v)
L10 L ← empty list; while v ≠ none do append v to L; v ← idom(v)
L11 return L
```

Line L1 can use any algorithm for the [dominators problem](/dominators-problem/); the page's implementation uses the simple Lengauer-Tarjan algorithm. Lines L3 to L7 walk the tree with an explicit stack, so a tree of depth $10^5$ needs no recursion.

## Example

Take the flow graph on $0, \ldots, 8$ with start 0 and the 11 edges

$$0 \to 1,\; 1 \to 2,\; 2 \to 3,\; 2 \to 4,\; 3 \to 4,\; 3 \to 7,\; 4 \to 5,\; 5 \to 6,\; 6 \to 3,\; 7 \to 8,\; 8 \to 6.$$

Its immediate dominators are $idom = [-, 0, 1, 2, 2, 4, 2, 3, 7]$, so the dominator tree is

```
0
└── 1
    └── 2
        ├── 3
        │   └── 7
        │       └── 8
        ├── 4
        │   └── 5
        └── 6
```

The walk enters the vertices in the order $0, 1, 2, 3, 7, 8, 4, 5, 6$:

| $v$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| $tin[v]$ | 0 | 1 | 2 | 3 | 6 | 7 | 8 | 4 | 5 |
| $tout[v]$ | 9 | 9 | 9 | 6 | 8 | 8 | 9 | 6 | 6 |

- DOMINATES$(3, 8)$: $3 \le 5$ and $6 \le 6$, so true. Indeed, 8 is entered only from 7, and 7 only from 3.
- DOMINATES$(4, 6)$: $6 \le 8$ but $tout[6] = 9 > 8 = tout[4]$, so false: the path $0, 1, 2, 3, 7, 8, 6$ avoids 4.
- DOMINATES$(3, 6)$ is false too, because of the path $0, 1, 2, 4, 5, 6$. Vertex 6 is a child of 2 although the edges into it come from 5 and 8.
- DOMINATORS$(8) = 8, 7, 3, 2, 1, 0$.

Simple shapes: on the single-vertex graph, the tree is the root alone and DOMINATES$(0, 0)$ is true. On a path $0 \to 1 \to \cdots \to n - 1$, the tree is the same path and $a$ dominates $b$ exactly when $a \le b$. On a star $0 \to 1, \ldots, 0 \to n - 1$ the tree is the same star, even if edges between leaves are added, since each leaf can still be reached directly from 0.

## Correctness

The full proof is in the proof file. It rests on three facts about dominance in a flow graph.

1. **Dominance is a partial order.** It is reflexive; it is transitive, because a path to $c$ passes $b$, and its prefix up to $b$ passes $a$; and it is antisymmetric: if $a \ne b$ and $b$ dominates $a$, then $b$ lies on a simple path to $a$ before its end, and the prefix of that path up to $b$ is a path to $b$ that avoids $a$.
2. **The strict dominators of $v$ form a chain.** On a simple path from $r$ to $v$, if $a$ comes before $b$, then $a$ dominates $b$: otherwise a path to $b$ that avoids $a$, followed by the rest of the simple path from $b$ to $v$, avoids $a$. So any two strict dominators are comparable, and the last one, $\mathrm{idom}(v)$, is dominated by all the others.
3. **The dominators of $v$ are $v$ and the dominators of $\mathrm{idom}(v)$.** By transitivity and by fact 2. Following $\mathrm{idom}$ removes $v$ from the set each time, so it reaches $r$, the graph of $\mathrm{idom}$ edges is a tree, and by induction the dominators of $v$ are its ancestors.

Lines L3 to L7 assign preorder entry times and exit times, so $a$ is an ancestor of $b$ exactly when $tin[a] \le tin[b]$ and $tout[b] \le tout[a]$. With fact 3, line L9 is correct. Line L10 lists the ancestors, which are the dominators.

## Complexity

| operation | time |
|---|---|
| BUILD | $O(m \log n)$ with the simple Lengauer-Tarjan algorithm; $O(m\, \alpha(m, n))$ or $O(n + m)$ with the faster ones; lines L2 to L7 add $O(n)$ |
| IDOM, DOMINATES | $O(1)$ |
| DOMINATORS$(v)$ | $O(1 + depth(v))$, the size of the answer |
| CHILDREN$(v)$ | $O(1)$ to return the list |

The structure takes $\Theta(n)$ space after the build; the build itself needs $O(n + m)$ for the graph and its reverse.

## Variants

- **Postdominator tree.** The dominator tree of the [transpose graph](/transpose-graph/) from the exit vertex. In a compiler it gives control dependence.
- **Nearest common dominator.** The deepest vertex that dominates both $a$ and $b$ is $\mathrm{lca}(a, b)$ in the dominator tree, so any [lowest common ancestor](/lowest-common-ancestor/) structure answers it.
- **Dominance frontier.** $DF(a)$ is the set of vertices $b$ such that $a$ dominates a predecessor of $b$ but does not strictly dominate $b$. For each vertex $b$ with two or more predecessors $p$, walk up from each $p$ to $\mathrm{idom}(b)$, adding $b$ to $DF$ of each vertex passed. The total cost is the size of the output.
- **Dynamic dominator trees.** Maintained under edge insertions and deletions, at a higher cost per update.
- **Dominator trees of acyclic graphs.** Built in topological order, one leaf at a time, by an LCA of the predecessors.
- **Heap dominator trees.** Built over the object graph of a program's heap, rooted at a virtual vertex joined to the roots of the heap. The retained size of an object is the sum of sizes in its subtree.

## When to use it

Use the dominator tree whenever a program needs "is $a$ on every path to $b$" for many pairs, or the closest such vertex: loop detection, SSA construction, code motion, control dependence, memory leak analysis, and the vertex connectivity of directed graphs. For a single pair, one graph search from $r$ with $a$ removed is enough. In an undirected graph, the [block-cut tree](/block-cut-tree/) gives the same information more simply.

## Pitfalls

- **Confusing the dominator tree with a DFS tree.** The parent of $v$ need not be a predecessor of $v$ in $G$, as vertex 6 in the example shows, and a DFS tree edge need not be a dominator edge.
- **Unreachable vertices.** They have no dominators. Leaving them in the arrays with stale values makes DOMINATES return true for them by accident.
- **Strict versus non-strict.** DOMINATES$(v, v)$ is true by the convention used here; a compiler that wants "strictly dominates" must also check $a \ne b$.
- **Multiple entries.** Dominance is defined from one start vertex. A graph with several entries needs a virtual start vertex with an edge to each entry.
- **Recursion depth.** Both the dominator computation and the tree walk must be iterative in Python, since control-flow graphs and test paths can be $10^5$ vertices deep.

## Implementations

## History

Dominance was introduced by Prosser in 1959 for the analysis of flow diagrams, and Lowry and Medlock used dominators to find loops in the IBM FORTRAN H compiler in 1969. Lengauer and Tarjan stated the ancestor property of the tree as the first lemma of their 1979 paper and gave the near-linear algorithm that made the tree cheap to build. Cytron, Ferrante, Rosen, Wegman and Zadeck (1991) used the tree and the dominance frontiers to construct static single assignment form, which made the dominator tree a standard part of every optimizing compiler.

## References
