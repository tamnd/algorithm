---
tag: PV464M
kind: data-structure
slug: phylogenetic-network
name: Phylogenetic network
aliases:
- reticulate network
area: biology/phylogenetics
level: advanced
summary: A rooted directed acyclic graph with labeled leaves. Vertices with two or more parents stand for hybridization, recombination or gene transfer.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of arcs, h: the reticulation number, k: the number of leaves}
  time: {add: "O(n + m)", count: "O(n)", check: "O(n + m)", display: "O(2^h k (n + m))"}
  space: {extra: "O(n + m)"}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [phylogenetic-tree, directed-acyclic-graph, depth-first-search]
see_also: [phylogenetic-network-inference, ancestral-recombination-graph, horizontal-gene-transfer, split-network-construction, maximum-agreement-forest, incomplete-lineage-sorting, newick-format, split-system]
sources:
  - book: isbn:9780521755962
    title: Daniel H. Huson, Regula Rupp and Celine Scornavacca, Phylogenetic Networks, Concepts, Algorithms and Applications, Cambridge University Press, 2010
    locator: the chapters on clusters and rooted phylogenetic networks, with switchings, displayed trees and the classes of networks
  - paper: doi:10.1109/TCBB.2007.70270
    title: Gabriel Cardona, Francesc Rosselló and Gabriel Valiente, Comparison of tree-child phylogenetic networks, IEEE/ACM Transactions on Computational Biology and Bioinformatics 6(4), 2009, pages 552 to 569
    locator: the definition of tree-child networks, the tree paths to leaves, and the bounds on their size
  - paper: "Iyad A. Kanj, Luay Nakhleh, Cuong Than and Ge Xia, Seeing the trees and their branches in the network is hard, Theoretical Computer Science 401, 2008"
    title: Iyad A. Kanj, Luay Nakhleh, Cuong Than and Ge Xia, Seeing the trees and their branches in the network is hard
    locator: the NP-completeness of deciding whether a network displays a given tree
---

A rooted phylogenetic network on a set $X$ of taxa is a directed acyclic graph with one root and with leaves labeled by $X$. In a [phylogenetic tree](/phylogenetic-tree/), every vertex except the root has one parent. A network also allows *reticulations*, vertices with two or more parents, which model a lineage that comes from two ancestors, as in hybridization, recombination or [horizontal gene transfer](/horizontal-gene-transfer/). The reticulation number $h$ counts the extra parent arcs. A network with $h$ binary reticulations displays at most $2^h$ trees, one for each way to keep one parent of every reticulation. The structure on this page stores a network as parent and child lists, keeps it acyclic, and answers the basic questions: the reticulation number, the tree-child test and the set of displayed trees.

## In plain words

A tree says that each species has one parent species. Sometimes this is false: a plant species can come from two others by hybridization, and a bacterium can take genes from an unrelated one. A network draws such a species with two arrows coming in.

Each gene still has a tree. At a hybrid, a gene comes from one of the two parents. So if you choose one incoming arrow at each hybrid and delete the others, you get a tree, and that tree is one possible gene history. The network is a compact summary of all these trees. With $h$ hybrids, there are up to $2^h$ ways to choose. Some choices give the same tree.

## The abstract type

A rooted phylogenetic network $N$ on $X$ is a directed acyclic graph without parallel arcs, with:

- one *root* $\rho$, of in-degree 0 and out-degree 1 or more;
- *leaves*, of in-degree 1 and out-degree 0, labeled one to one by the elements of $X$;
- *tree vertices*, of in-degree 1 and out-degree 2 or more;
- *reticulations*, of in-degree 2 or more and out-degree 1.

The network is *binary* if the root and the tree vertices have out-degree 2 and the reticulations have in-degree 2. The *reticulation number* is $h(N) = \sum_v (\mathrm{indeg}(v) - 1)$ over the vertices other than the root, which equals $|E| - |V| + 1$. A *switching* keeps all arcs into tree vertices and leaves, and exactly one arc into each reticulation. It is a tree with root $\rho$, and its nonempty clusters, the sets of labels below its vertices, define a tree on $X$. $N$ *displays* a tree $T$ if $T$ comes from some switching in this way. $N$ is *tree-child* if every vertex that is not a leaf has a child that is a tree vertex or a leaf.

The operations are:

- **ADD-VERTEX$(v, \ell)$.** Add a vertex, with the label $\ell$ if it will be a leaf.
- **ADD-ARC$(u, v)$.** Add the arc $u \to v$, or reject it if it closes a directed cycle.
- **RETICULATION-NUMBER.** Return $h(N)$.
- **IS-VALID.** Check the four kinds of vertices above.
- **IS-TREE-CHILD.** Check the tree-child condition.
- **DISPLAYED-TREES.** Return the set of trees that $N$ displays, each as its set of clusters.

## Representation

- **Child lists and parent lists.** A hash table maps each vertex to the list of its children and another maps it to the list of its parents, as in an [adjacency list](/adjacency-list/) with both directions. The in-degree, which tells a reticulation from a tree vertex, is the length of the parent list.
- **Labels.** A table from leaves to taxa.
- **Arc count.** A counter, so that $|E|$ costs $O(1)$.

Both directions are stored because the questions use both: acyclicity and clusters walk down, and switchings choose among the parents. In files, networks are usually written in extended [Newick format](/newick-format/), where a reticulation appears once for each parent with the same tag, such as `#H1`.

## Operations

```pseudo id=main
ADD-ARC(u, v)
L1  if v reaches u by a depth-first search over child lists, reject: the arc closes a cycle
L2  append v to children(u) and u to parents(v)
RETICULATION-NUMBER()
L3  return the sum of |parents(v)| − 1 over the vertices v with a parent
IS-TREE-CHILD()
L4  for each vertex v with children: if every child c of v has |parents(c)| ≥ 2, return false
L5  return true
DISPLAYED-TREES()
L6  for each choice of one parent p(r) for every reticulation r do
L7      keep the arc into each vertex with one parent, and the arc p(r) → r for each reticulation
L8      compute the clusters of the switching in postorder, and drop the empty ones
L9  return the set of the cluster sets
```

Line L1 is the only place where acyclicity can break, because a new cycle must use the new arc. The search starts at $v$, so it also rejects a loop $u \to u$. Line L3 counts, for each vertex, the parents beyond the first. Line L8 removes empty clusters, which come from parts of a switching that lead to no leaf, and the set of clusters ignores vertices with one child, so the result is a tree on $X$ without extra vertices. Line L9 collects the trees in a set, because different switchings can give the same tree.

## Example

Take $X = \{a, b, c\}$, the root $\rho$, tree vertices $u$ and $v$, and one reticulation $r$, with the arcs

$$\rho \to u,\quad \rho \to v,\quad u \to a,\quad u \to r,\quad v \to r,\quad v \to c,\quad r \to b.$$

The taxon $b$ is a hybrid of the lineage of $a$ and the lineage of $c$.

| vertex | parents | children | kind |
|---|---|---|---|
| $\rho$ | none | $u$, $v$ | root |
| $u$ | $\rho$ | $a$, $r$ | tree vertex |
| $v$ | $\rho$ | $r$, $c$ | tree vertex |
| $r$ | $u$, $v$ | $b$ | reticulation |
| $a$, $b$, $c$ | one each | none | leaves |

**Reticulation number.** Only $r$ has a second parent, so $h = 1$. Also $|E| - |V| + 1 = 7 - 7 + 1 = 1$.

**Tree-child.** $\rho$ has the tree vertices $u$ and $v$, $u$ has the leaf $a$, $v$ has the leaf $c$, and $r$ has the leaf $b$. So the network is tree-child.

**Displayed trees.** There are two switchings:

| arc kept into $r$ | clusters | tree |
|---|---|---|
| $u \to r$ | $\{a, b\}$, $\{a, b, c\}$ and the singletons | `((a,b),c);` |
| $v \to r$ | $\{b, c\}$, $\{a, b, c\}$ and the singletons | `(a,(b,c));` |

In the switching with $u \to r$, the vertex $v$ has the one child $c$, so its cluster is $\{c\}$, a singleton.

**A rejected arc.** ADD-ARC$(r, u)$ would close the cycle $u \to r \to u$. Line L1 finds that $u$ reaches $r$ and rejects it.

**A second reticulation.** Put a new vertex $w$ on the arc $v \to c$, so that $v \to w \to c$, and add the arc $u \to w$. Now $h = 2$, and $v$ has only the reticulations $r$ and $w$ as children, so the network is not tree-child. Its four switchings give four different trees: `((a,b),c);`, `(a,(b,c));`, `((a,c),b);` and the star `(a,b,c);`. The star comes from the switching in which $u$ is the parent of both $r$ and $w$. Then $u$ has the three leaves as descendants, and $v$ leads to no leaf.

## Correctness

The invariant is that the graph has no directed cycle. It holds for the empty graph, ADD-VERTEX adds no arc, and a cycle created by ADD-ARC$(u, v)$ would consist of the new arc and a path from $v$ to $u$, which line L1 rules out. The reticulation number formula follows from counting arc heads: the in-degrees sum to $|E|$, and the formula subtracts 1 for each vertex except the root. For displayed trees, each switching is a tree, because every vertex except the root has exactly one parent and the graph is acyclic, so following parents always ends at the root. Conversely, any subgraph that witnesses a displayed tree extends to a switching with the same nonempty clusters, by choosing the parents that the subgraph uses. The proof file also shows that the tree-child test is equivalent to the condition that every vertex has a path to a leaf that avoids reticulations.

## Complexity

| operation | time | reason |
|---|---|---|
| ADD-VERTEX | $O(1)$ expected | hash table inserts |
| ADD-ARC | $O(n + m)$ | one depth-first search |
| RETICULATION-NUMBER | $O(n)$ | one pass over the parent lists, or $O(1)$ with the arc counter |
| IS-VALID, IS-TREE-CHILD | $O(n + m)$ | one pass over all lists |
| DISPLAYED-TREES | $O(2^h k (n + m))$ | $2^h$ switchings in the binary case, each with $n$ clusters of up to $k$ labels |

The space is $O(n + m)$ for the lists, plus the output. A network with $k$ leaves can be large in general. A binary tree-child network with $k$ leaves has at most $k - 1$ reticulations (Cardona, Rosselló and Valiente 2009), so its size is $O(k)$.

Deciding whether a network displays one given tree is NP-complete in general (Kanj, Nakhleh, Than and Xia 2008). So the exponential cost of DISPLAYED-TREES in $h$ cannot be avoided in general, even for one tree. For restricted classes, for example tree-child networks, the question can be answered in polynomial time.

## Variants

- **Tree-child networks.** Every non-leaf vertex has a child that is not a reticulation. Every vertex then has a path to a leaf through tree vertices, and the network is determined by small summaries such as its path counts. Many questions that are hard in general become polynomial.
- **Galled trees and level-$k$ networks.** In a galled tree, the cycles of the underlying undirected graph do not share vertices. A level-$k$ network has at most $k$ reticulations in each biconnected component. Level 1 is the class of galled trees.
- **Time-consistent networks.** The vertices can get times so that the two parents of a reticulation live at the same time, as a real hybridization requires.
- **Unrooted networks.** Without a root, the graph is undirected, and [split networks](/split-network-construction/) are a different kind of unrooted network that shows conflicting signal without explicit events.
- **Ancestral recombination graphs.** An [ancestral recombination graph](/ancestral-recombination-graph/) is a network with times and with a genomic interval on each arc, which tells which part of the genome follows which parent.

## When to use it

Use a phylogenetic network when the history of the taxa is not a tree: hybrid species in plants, admixture in populations, gene transfer in bacteria, or recombination within a gene. It is also the output type of [network inference](/phylogenetic-network-inference/), which looks for a network with few reticulations that displays given gene trees. When gene trees disagree only because of [incomplete lineage sorting](/incomplete-lineage-sorting/), a species tree is enough, and a network can overfit.

## Pitfalls

- **Displayed trees are not all distinct.** A triangle, with a vertex $u$ that is the parent of a reticulation $r$ and the root as its other parent, gives the same tree for both switchings. Count trees, not switchings.
- **Reticulation number is not identifiable from trees alone.** Different networks can display the same set of trees, so a network inferred from gene trees is one of several equally good answers.
- **Missing cycle check.** Without line L1, a wrong arc can make a cycle, and then a switching is no longer a tree, and the cluster computation loops.
- **Mixing up the kinds.** A vertex with two parents and two children is not allowed in this definition. Split it into a reticulation followed by a tree vertex before you run the validity check.
- **Deep networks.** Long paths make recursive searches overflow. The implementation uses explicit stacks.

## Implementations

## History

Networks for reticulate evolution were drawn long before algorithms for them. Formal models came in the 1990s, with ancestral recombination graphs from population genetics and hybridization networks from phylogenetics. Galled trees were studied for recombination by Gusfield and coauthors and by Wang, Zhang and Zhang. Cardona, Rosselló and Valiente introduced tree-child networks in a paper that appeared in 2009. Kanj, Nakhleh, Than and Xia (2008) showed that deciding whether a network displays a tree is NP-complete. The book of Huson, Rupp and Scornavacca (2010) put the rooted and unrooted kinds of networks into one framework.

## References
