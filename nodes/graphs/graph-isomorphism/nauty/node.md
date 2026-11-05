---
tag: RGG08G
kind: algorithm
slug: nauty
name: nauty
aliases:
- McKay's nauty
- No AUTomorphisms, Yes?
area: graphs/graph-isomorphism
level: advanced
summary: McKay's practical canonical labeling and automorphism package based on individualization-refinement search.
solves: [canonical-labeling, graph-automorphism, graph-isomorphism-problem]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(n! n^4), best: O(n^2 (n + m))}
  space: {extra: O(n^2)}
properties: {deterministic: true, recursive: false, directed: false}
prereqs: [individualization-refinement, partition-refinement, canonical-labeling, graph-automorphism-group]
see_also: [bliss, weisfeiler-leman, automorphism-orbit, equitable-partition, cai-furer-immerman-construction, graph-isomorphism-problem]
sources:
  - paper: "Brendan D. McKay, Practical graph isomorphism, Congressus Numerantium 30, 45 to 87 (1981)"
    locator: Sections 2 to 5 (the search tree, the canonical labeling, the use of automorphisms to prune, and the group order from the first path)
  - paper: doi:10.1016/j.jsc.2013.09.003
    title: Brendan D. McKay and Adolfo Piperno, Practical graph isomorphism, II, Journal of Symbolic Computation 60, 94 to 112 (2014)
    locator: Sections 2 to 4 (the general individualization-refinement framework, the pruning rules, and the comparison of nauty and Traces)
  - paper: "Takunari Miyazaki, The complexity of McKay's canonical labeling algorithm, in Groups and Computation II, DIMACS Series in Discrete Mathematics and Theoretical Computer Science 28, 1997, 239 to 256"
    locator: the whole paper (an exponential lower bound for nauty on graphs built from Fürer's gadgets)
---

nauty, by Brendan McKay, is the classical program for [canonical labeling](/canonical-labeling/) and [automorphism groups](/graph-automorphism/) of graphs. It searches a tree of vertex partitions: each node is an [equitable partition](/equitable-partition/), each child [individualizes](/individualization-refinement/) one vertex of a chosen cell and refines again, and each leaf is a labeling of the graph. The canonical form is the best relabeled graph found at a leaf, and two leaves with the same relabeled graph give an automorphism, which is used to cut the rest of the tree. It handles most graphs with thousands of vertices in a fraction of a second, but there are families on which it takes exponential time.

## In plain words

To decide if two networks are the same, give each one a standard numbering of its points and compare the results. nauty finds the standard numbering by repeated sorting: points are first grouped by how they connect to each group, and when a group cannot be split further, one point in it is singled out, which lets the sorting go on. Every way of singling out points gives a numbering, so the program explores a tree of choices and keeps the numbering that makes the network look "largest". When two choices give the same picture, it has found a symmetry of the network, and it uses that symmetry to skip choices that would only repeat work.

## The problem

The input is a simple undirected graph $G$ on $V = \{0, \ldots, n-1\}$, with an optional vertex coloring that isomorphisms must keep; nauty itself also takes directed graphs, and edge colors are encoded by layers of vertices. The output is a canonical labeling $\lambda$, meaning that the relabeled colored graph $\lambda(G)$ is the same for all graphs isomorphic to $G$; generators of $\mathrm{Aut}(G)$; and the order $|\mathrm{Aut}(G)|$. Two graphs are isomorphic exactly when their canonical forms are equal, so this also solves the [graph isomorphism problem](/graph-isomorphism-problem/).

## The algorithm

A partition is an ordered list of cells. REFINE splits cells by the number of neighbors in each cell, as in [partition refinement](/partition-refinement/), with the pieces ordered by that number. Individualizing $w$ puts $\{w\}$ first in place of its cell. The target cell is the first smallest cell of size at least 2.

```pseudo id=main
NAUTY(G, colors)
L1  π0 ← REFINE(G, the cells of equal color, in color order)
L2  push the root frame (π0, empty prefix)
L3  while the stack is not empty do
L4      if the top partition π is discrete then pop it and let F be λ(G) for the labeling λ of π
L5          if no leaf is stored then store it as the first leaf and the best leaf
L6          else if F equals the first or the best leaf then record the automorphism between the two labelings
L7          else if F is larger than the best leaf then make it the best leaf
L8      else C ← the target cell of π, chosen once per frame
L9          take the next w in C not in the orbit of a tried w' under the found automorphisms fixing the prefix; if none, pop
L10         push the frame (REFINE(G, π with w individualized), prefix + w)
L11 |Aut| ← the product over the first path of the orbit sizes of its first child; return the best leaf, the automorphisms and |Aut|
```

The implementation keeps $F$ as the color sequence and the adjacency rows as integers, compares leaves as tuples, and finds orbits with a union-find over the generators that fix the prefix.

## Example

The cycle $C_6$ with vertices $0, \ldots, 5$ and edges $\{i, i + 1 \bmod 6\}$. It is regular, so the root partition is the single cell $\{0, \ldots, 5\}$. The search makes seven calls to REFINE:

| step | prefix | refined partition | event |
|---|---|---|---|
| 1 | none | $\{0, 1, 2, 3, 4, 5\}$ | target cell is the whole set |
| 2 | 0 | $\{0\}, \{2, 4\}, \{3\}, \{1, 5\}$ | target cell $\{2, 4\}$ |
| 3 | 0, 2 | $\{0\}, \{2\}, \{4\}, \{3\}, \{5\}, \{1\}$ | first leaf, stored as best |
| 4 | 0, 4 | $\{0\}, \{4\}, \{2\}, \{3\}, \{1\}, \{5\}$ | same graph: automorphism $(1\,5)(2\,4)$ |
| 5 | 1 | $\{1\}, \{3, 5\}, \{4\}, \{0, 2\}$ | 1 is not in the orbit $\{0\}$ of the reflection |
| 6 | 1, 3 | $\{1\}, \{3\}, \{5\}, \{4\}, \{0\}, \{2\}$ | same graph: the rotation $v \mapsto v + 1$ |
| 7 | 1, 5 | $\{1\}, \{5\}, \{3\}, \{4\}, \{2\}, \{0\}$ | same graph: the reflection $(0\,1)(2\,5)(3\,4)$ |

After step 7, vertices 2 to 5 are in the orbit of 0 under the rotation, so the root has no more children. The first path has orbit sizes 6 at the root and 2 at the node with prefix 0, so $|\mathrm{Aut}(C_6)| = 12$. The full tree, without pruning, has 19 nodes and 12 leaves.

In the same implementation, the Petersen graph needs 25 calls (full tree: 221 nodes) and gets $|\mathrm{Aut}| = 120$; the $4 \times 4$ rook's graph needs 43 calls and gets 1152; the Shrikhande graph needs 21 and gets 192. These two strongly regular graphs with parameters $(16, 6, 2, 2)$ are not told apart by refinement, but their canonical forms differ.

## Correctness

The [full proof](proofs/correctness.md) has three parts.

- **Invariance.** REFINE, individualization, the target cell rule and the leaf value use only adjacency counts, cell sizes and cell positions. So a renaming $\gamma$ of the vertices maps the search tree of $G$ onto the tree of $G^\gamma$, and leaves to leaves with the same relabeled graph. The largest leaf value is therefore the same for isomorphic graphs, and it is the graph itself relabeled, so it is a canonical form.
- **Safe pruning.** An automorphism that fixes the prefix of a node maps the node to itself and the subtree of one child onto the subtree of another, with the same leaf values. Skipping children in the orbit of a tried child therefore never loses the best leaf.
- **Group order.** The automorphisms that fix the prefix of the $d$-th node on the first path form a chain of stabilizers ending in the trivial group. Every child in the orbit of the first child leads to a leaf equal to the first leaf, which records an automorphism that moves the first child there. So the found generators give the full orbits, and the orbit-stabilizer theorem gives the product.

## Complexity

| case | time | space |
|---|---|---|
| one REFINE call in this implementation | $O(n^2 (n + m))$ | $O(n + m)$ |
| best case: the root refinement is discrete | $O(n^2 (n + m))$ | $O(n^2)$ |
| worst case: at most $n!$ leaves and $e \cdot n!$ nodes | $O(n! \cdot n^4)$ | $O(n^2)$ stack, $O(n^2)$ per stored generator |

nauty's own REFINE is much faster: it uses a splitter queue with the "skip the largest piece" rule, which gives $O((n + m) \log n)$ per refinement. The search size is the real cost. For graphs whose root refinement is discrete, which is almost all graphs, there is no search at all. For vertex-transitive and strongly regular graphs, each level needs individualization, and automorphism pruning keeps the tree small. Miyazaki (1997) showed that nauty takes exponential time on graphs built from Fürer's gadgets, and Neuen and Schweitzer (2018) extended such lower bounds to every [individualization-refinement](/individualization-refinement/) algorithm.

## Properties

- **Exact.** The canonical form, the generators and the group order are exact, not heuristic.
- **Colored input.** Colors restrict the root partition; directed graphs and edge colors are encoded as colored graphs.
- **Generators, not the whole group.** The group order may be astronomically large, as for $K_n$ with $n!$ automorphisms, but the number of stored generators stays small in practice.
- **Orbits as a by-product.** The union-find over all found generators gives the [automorphism orbits](/automorphism-orbit/).
- **Deterministic.** The same input always gives the same canonical form; it depends on the version of the program, so canonical forms from different tools or versions must not be mixed.

## Variants and improvements

- **Node invariants.** nauty can compute an extra invariant at each node, such as counts of triangles or cliques through vertices, to split cells that refinement cannot split, which helps on strongly regular graphs and designs.
- **Best-path and first-path pruning.** A node whose partition, compared by a node invariant, is worse than the best path at the same depth cannot hold the best leaf and is cut.
- **Traces.** Piperno's program, part of the nauty distribution since 2013, searches the tree breadth first, uses traces of the refinement as node invariants, and finds automorphisms by random walks; it is much faster on hard families (McKay and Piperno 2014).
- **[bliss](/bliss/)** and saucy use sparse data structures and more pruning, and are fast on large sparse graphs.
- **The programs geng and genbg** in the nauty package generate all graphs of a given size up to isomorphism, using canonical labeling to reject duplicates.

## When to use it

Use nauty, Traces or bliss whenever you need canonical forms or automorphism groups of real graphs: removing isomorphic duplicates in a collection, symmetry breaking in SAT and integer programs, computing the symmetries of a chemical or combinatorial structure. Use plain [color refinement](/weisfeiler-leman/) when a fast but incomplete test is enough, and [VF2](/vf2-algorithm/) when you need subgraph matching rather than whole-graph canonical forms. Do not expect polynomial time on adversarial inputs such as CFI graphs.

## Pitfalls

- **Comparing forms across versions or tools.** A canonical form is canonical only for one program with fixed options; store the graph, not only the form, if it must outlive the software.
- **Non-invariant tie breaking.** Ordering split pieces by vertex number, or choosing the target cell by its smallest vertex, gives a valid labeling but not a canonical one.
- **Pruning with automorphisms that do not fix the prefix.** Only the stabilizer of the individualized vertices may be used at a node.
- **Treating the leaf count as $|\mathrm{Aut}|$.** With pruning the visited leaves are far fewer than $|\mathrm{Aut}|$; the order comes from the orbit sizes on the first path.
- **Recursion.** A recursive search can go $n - 1$ levels deep; this implementation uses an explicit stack.

## Implementations

## History

Brendan McKay developed nauty from the late 1970s and described its method in "Practical graph isomorphism" (1981), with the search tree of refined partitions, the use of automorphisms for pruning and the computation of the group order from the first path. The program became the standard tool for graph enumeration and computational group theory. Miyazaki (1997) showed exponential worst-case behavior. In 2014 McKay and Piperno described the general framework again, together with Traces, and nauty and Traces are distributed together.

## References
