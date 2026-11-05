---
tag: YP87B9
kind: technique
slug: individualization-refinement
name: Individualization-refinement
aliases:
- individualize and refine
area: graphs/graph-isomorphism
level: advanced
summary: Branch by individualizing one vertex, then refine the partition; the basis of nauty and bliss.
prereqs: [partition-refinement, equitable-partition, weisfeiler-leman, canonical-labeling]
see_also: [nauty, bliss, graph-automorphism, automorphism-orbit, generic-backtracking-algorithm, cai-furer-immerman-construction]
sources:
  - paper: "Brendan D. McKay, Practical graph isomorphism, Congressus Numerantium 30, 45 to 87 (1981)"
    locator: Sections 2 to 5 (the search tree of refined partitions, equivalent leaves, and pruning by automorphisms)
  - paper: doi:10.1016/j.jsc.2013.09.003
    title: Brendan D. McKay and Adolfo Piperno, Practical graph isomorphism, II, Journal of Symbolic Computation 60, 94 to 112 (2014)
    locator: Sections 2 and 3 (the general framework of individualization-refinement, node invariants, and the pruning rules)
  - paper: doi:10.1145/3188745.3188900
    title: Daniel Neuen and Pascal Schweitzer, An exponential lower bound for individualization-refinement algorithms for graph isomorphism, STOC 2018
    locator: the whole paper (graphs on which every such algorithm visits exponentially many nodes)
---

Individualization-refinement is the technique behind the fastest practical programs for [canonical labeling](/canonical-labeling/) and [graph automorphism](/graph-automorphism/), such as [nauty](/nauty/), Traces and [bliss](/bliss/). It alternates two steps: refinement, which splits a vertex partition until it is [equitable](/equitable-partition/), and individualization, which gives one vertex of a non-singleton cell its own cell and so forces refinement to go on. Branching over all vertices of the chosen cell gives a search tree whose leaves are labelings of the graph, and the best leaf is the canonical form. Automorphisms found during the search prune most of the tree.

## In plain words

Give every point a color and keep recoloring: two points with the same color but different numbers of neighbors of some color get different colors. When nothing changes, some colors may still be shared by many points, and then you cannot tell those points apart. So pick one of them and give it a brand-new color, and recolor again. Repeat until every point has its own color; this gives a numbering of the points. Since you did not know which point to pick, try each one, which builds a tree of choices. Each leaf is a numbering, and you keep the one that gives the "largest" picture of the network. Two leaves that give the same picture reveal a symmetry, and symmetries let you skip branches.

## When it applies

- The objects are graphs or other combinatorial structures (colored graphs, digraphs, hypergraphs, designs, codes, matrices) that can be encoded as vertex-colored graphs.
- The questions are isomorphism, canonical forms, automorphism group generators, or vertex orbits.
- Refinement alone, that is, [color refinement](/weisfeiler-leman/), does not finish: it leaves cells of more than one vertex, for example on regular graphs, where it does nothing at all.
- The cost of the search depends on the symmetry and the structure of the graph, not only on $n$; it is fast on most graphs met in practice and exponential on special families.

## The template

Graphs here are undirected, with optional vertex colors; directed and edge-colored graphs work the same way. A partition is ordered: a list of cells.

```pseudo id=main
IR(G, initial ordered partition π0)
L1  π ← REFINE(G, π0)
L2  push the root node (π, empty prefix)
L3  while the stack is not empty do
L4      take a node ν = (π, prefix)
L5      if π is discrete then
L6          let λ number the vertices in cell order and compare λ(G) with the stored leaves
L7          if λ(G) equals a stored leaf then record the automorphism between them
L8          else if λ(G) is better than the best leaf then make λ the best leaf
L9      else C ← TARGET-CELL(π)
L10         for each w in C not in the orbit of an earlier child under the known automorphisms fixing prefix do
L11             push (REFINE(G, π with w individualized), prefix + w)
L12 return the best leaf as the canonical labeling and the recorded automorphisms
```

The three parts must be isomorphism-invariant: if a permutation $\gamma$ maps $G$ to $G^\gamma$, then REFINE, TARGET-CELL and any node invariant applied to the image of a node give the image of the result. Then $\gamma$ maps the search tree of $G$ onto the search tree of $G^\gamma$, the leaves give the same set of relabeled graphs, and the best one is a canonical form.

## Classic examples

The counts below come from the simple version in the [nauty](/nauty/) page: every cell is a splitter in each pass, the target cell is the first smallest non-singleton cell, and pruning uses automorphism orbits only.

| graph | $\lvert \mathrm{Aut} \rvert$ | full search tree: nodes, leaves | with orbit pruning: nodes | generators found |
|---|---|---|---|---|
| cycle $C_6$ | 12 | 19, 12 | 7 | 3 |
| Petersen graph | 120 | 221, 120 | 25 | 10 |
| Shrikhande graph | 192 | 305, 192 | 21 | 10 |
| $4 \times 4$ rook's graph | 1152 | 2033, 1152 | 43 | 13 |

- **The cycle $C_6$.** Refinement does nothing, as the graph is regular. Individualizing vertex 0 and refining gives the cells $\{0\}, \{2, 4\}, \{3\}, \{1, 5\}$. Individualizing 2 then makes the partition discrete. The tree has 12 leaves, one per automorphism, as every leaf gives the same relabeled graph.
- **The Petersen graph.** After individualizing one vertex, refinement gives the cells of size 1, 6 and 3 (the vertex, the vertices at distance 2, and its neighbors). It stops there because the graph is distance-regular; one more individualization is needed before the partition splits into more cells.
- **Strongly regular graphs.** The rook's graph and the Shrikhande graph have the same parameters $(16, 6, 2, 2)$, and refinement from the unit partition does nothing on either. After individualizing one vertex both give cells of sizes 1, 9 and 6, so this step alone does not tell them apart; after a second individualization the partitions differ (cell sizes $1, 6, 3, 1, 3, 2$ against $1, 2, 4, 1, 2, 1, 1, 2, 2$). The canonical forms differ, so the graphs are not isomorphic.
- **Leaves give automorphisms.** In each row the leaves of the full tree number $\lvert \mathrm{Aut} \rvert$ here, because each graph is vertex-transitive and every leaf yields the same relabeled graph. In general the leaves that give one relabeled graph are in one-to-one correspondence with the automorphisms, so the number of leaves is $\lvert \mathrm{Aut} \rvert$ times the number of distinct relabeled graphs.

## Variations

- **Target cell rules.** First non-singleton cell, first smallest, first largest, or the cell with the most non-trivial joins to other cells (nauty's default rule is of this last kind). The rule changes the tree size a lot but not the correctness, as long as it is invariant.
- **Node invariants.** A value computed at each node, such as the sequence of splits done by refinement (the trace), compared with the same value on the best path. A node whose invariant is worse than the best path's at the same depth cannot lead to the best leaf and is cut. Traces and [bliss](/bliss/) rely on this.
- **Automorphism pruning.** Two children $w, w'$ of a node whose prefix is fixed by an automorphism mapping $w$ to $w'$ have isomorphic subtrees; only one needs to be searched. nauty also uses the orbits of the stabilizer to cut whole subtrees on the first path.
- **Breadth-first and random search.** Traces explores the tree level by level and uses random walks to find automorphisms early (McKay and Piperno 2014).
- **Component and cell recursion.** bliss and other tools split the problem when the graph or a cell decomposes, which helps on sparse graphs.
- **Stronger refinement.** Refinement by [k-WL](/k-dimensional-weisfeiler-leman/) cuts more but costs more per node; practical tools stay with color refinement.

## Pitfalls

- **A refinement that is not invariant.** Splitting cells by an order that depends on vertex names, for example by the smallest vertex of a group, breaks the canonical form: isomorphic graphs can get different forms. Order pieces only by invariant data, such as neighbor counts.
- **Comparing leaves by the partition, not by the graph.** Two leaves are equivalent when the relabeled graphs are equal; equal cell sizes along the path prove nothing.
- **Pruning with automorphisms that do not fix the prefix.** Orbits must be taken in the group of automorphisms that fix every vertex individualized so far, or the pruned subtree may hold the best leaf.
- **Expecting polynomial time.** Neuen and Schweitzer (2018) built graphs on which every individualization-refinement algorithm with color refinement, whatever its cell rule and pruning, visits exponentially many nodes; [CFI graphs](/cai-furer-immerman-construction/) are the basis.
- **Deep recursion.** The tree depth can reach $n - 1$, for example on a graph whose automorphism group fixes nothing until many vertices are individualized; use an explicit stack.

## Exercises

1. Show that the leaves of the full tree that give the same relabeled graph as a fixed leaf are in one-to-one correspondence with the automorphisms of $G$. (Hint: an automorphism maps the tree onto itself.)
2. Prove that, if REFINE, TARGET-CELL and the leaf order are invariant, then $G \cong H$ implies that the best leaves of their trees give equal relabeled graphs.
3. For $C_n$, count the nodes of the full search tree with the first smallest cell rule, and the nodes left by orbit pruning.

## References
