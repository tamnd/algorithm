---
tag: C536CB
kind: algorithm
slug: split-decomposition
name: Split decomposition
area: biology/phylogenetics
level: research
summary: Writes a distance matrix as a sum of weighted, weakly compatible split metrics and a split-prime rest, using the isolation index of Bandelt and Dress.
solves: [split-network-construction]
model: real-ram
complexity:
  vars: {n: the number of taxa}
  time: {worst: "O(n^6)"}
  space: {extra: "O(n^3)"}
properties: {deterministic: true, exact: true, online: true, recursive: false}
history:
  year: 1992
  people: [Hans-Jurgen Bandelt, Andreas W. M. Dress]
  note: Bandelt and Dress defined the isolation index and the canonical split decomposition of a metric in 1992. Huson made it practical in SplitsTree, which draws the result as a splits graph.
prereqs: [split-system, tree-metric, four-point-condition]
see_also: [neighbor-net, split-network-construction, phylogenetic-network, neighbor-joining, splits-of-a-tree, least-squares-phylogeny, metric-space, phylogenetic-tree]
sources:
  - paper: doi:10.1016/1055-7903(92)90021-8
    title: Hans-Jurgen Bandelt and Andreas W. M. Dress, Split decomposition, a new and useful approach to phylogenetic analysis of distance data, Molecular Phylogenetics and Evolution 1(3), 1992, pages 242 to 252
    locator: the isolation index, d-splits, and the method for distance data in phylogenetics
  - paper: "Hans-Jurgen Bandelt and Andreas W. M. Dress, A canonical decomposition theory for metrics on a finite set, Advances in Mathematics 92(1), 1992"
    title: Hans-Jurgen Bandelt and Andreas W. M. Dress, A canonical decomposition theory for metrics on a finite set
    locator: the theorems that d-splits are weakly compatible, number at most n(n-1)/2, and leave a split-prime residue, and the incremental computation
  - paper: "Daniel H. Huson, SplitsTree, analyzing and visualizing evolutionary data, Bioinformatics 14(1), 1998"
    title: Daniel H. Huson, SplitsTree, analyzing and visualizing evolutionary data
    locator: the software that computes split decompositions and draws them as splits graphs
  - book: isbn:9780521755962
    title: Daniel H. Huson, Regula Rupp and Celine Scornavacca, Phylogenetic Networks, Concepts, Algorithms and Applications, Cambridge University Press, 2010
    locator: the chapter on splits and unrooted phylogenetic networks, with split decomposition and weak compatibility
---

Split decomposition, introduced by Bandelt and Dress (1992), takes a distance matrix $d$ on $n$ taxa and finds all splits $A \mid B$ of the taxa that $d$ supports, each with a weight called its *isolation index*. The supported splits, the *d-splits*, are always weakly compatible, there are at most $\binom{n}{2}$ of them, and
$$d = d_0 + \sum_{S} \alpha_S\, \delta_S,$$
where $\delta_S$ is the split metric of $S$ (1 for taxa on different sides, 0 otherwise) and the rest $d_0$ supports no split at all. If $d$ is a [tree metric](/tree-metric/), the d-splits are the edges of the tree and the indices are the edge lengths, so the method generalizes tree reconstruction. If the data do not fit a tree, the d-splits include incompatible splits, and they are drawn as a [split network](/split-network-construction/). The algorithm on this page adds the taxa one at a time and runs in $O(n^6)$ time.

## In plain words

A tree with branch lengths gives a distance between each pair of taxa: the length of the path between them. Each branch splits the taxa into two groups, and it adds its length to every distance between the two groups. So a tree distance is a sum of simple pieces, one per branch.

Real distances do not come from a tree exactly. Split decomposition still writes them as such a sum, but it allows splits that no single tree has together, for example both $ab \mid cd$ and $ac \mid bd$. For each possible split, it measures how strongly the four-taxon comparisons favor it, and it keeps the split if the weakest comparison still favors it. Whatever cannot be explained by splits is left over as a rest. A large rest means that the data are noisy or that the splits miss most of the signal.

## The problem

The input is a symmetric matrix $d$ on the taxa $X = \{x_1, \ldots, x_n\}$ with zero diagonal, usually a [metric](/metric-space/). For a split $A \mid B$ of $X$ and $a, a' \in A$, $b, b' \in B$, let

$$\beta(a, a'; b, b') = \max\{d(a, b) + d(a', b'),\ d(a, b') + d(a', b),\ d(a, a') + d(b, b')\} - d(a, a') - d(b, b').$$

The isolation index is $\alpha(A \mid B) = \frac{1}{2} \min \beta(a, a'; b, b')$ over all such $a, a', b, b'$, where $a = a'$ and $b = b'$ are allowed. For four distinct taxa, $\beta$ is the amount by which the sum $d(a, a') + d(b, b')$ is smaller than the larger of the other two sums, as in the [four-point condition](/four-point-condition/). The output is the set of d-splits, those with $\alpha > 0$, and their indices.

## The algorithm

```pseudo id=main
SPLIT-DECOMPOSITION(d on x_1, ..., x_n)
L1  S ← {x_1 | x_2} with index d(x_1, x_2), if this is positive
L2  for k ← 3 to n do
L3      S' ← ∅
L4      candidates: X_{k−1} | {x_k}, and A ∪ {x_k} | B and A | B ∪ {x_k} for each A | B in S
L5      for each candidate, α ← min(the index of A | B on X_{k−1}, half the smallest β that uses x_k)
L6      add each candidate with α > 0 to S', with its index α
L7      S ← S'
L8  return S, the d-splits of X with their isolation indices
```

The key fact is in line L4. If $A \mid B$ is a d-split of $X_k$, remove $x_k$ from its side. Either the side becomes empty, and the split is $X_{k-1} \mid \{x_k\}$, or the rest is a split of $X_{k-1}$ whose index is at least as large, because its minimum runs over fewer terms. So every d-split of $X_k$ grows from a d-split of $X_{k-1}$, and the algorithm never has to try more than $2 \binom{k-1}{2} + 1$ candidates. Line L5 gets the new index without starting over: the terms of the new split are the old terms plus the terms that use $x_k$.

## Example

Take four taxa $a, b, c, d$ and the distances

| | a | b | c | d |
|---|---|---|---|---|
| a | 0 | 3 | 5 | 6 |
| b | 3 | 0 | 6 | 5 |
| c | 5 | 6 | 0 | 3 |
| d | 6 | 5 | 3 | 0 |

The three sums over pairs are $d(a, b) + d(c, d) = 6$, $d(a, c) + d(b, d) = 10$ and $d(a, d) + d(b, c) = 12$. The four-point condition fails, because the two largest sums differ, so $d$ is not a tree metric.

**Lines L1 to L7.** The algorithm adds the taxa in the order $a, b, c, d$.

| step | candidate | from | index | kept |
|---|---|---|---|---|
| $k = 2$ | $a \mid b$ | start | $d(a, b) = 3$ | yes |
| $k = 3$ | $ab \mid c$ | $\{c\}$ alone | 4 | yes |
| $k = 3$ | $ac \mid b$ | $a \mid b$ | 2 | yes |
| $k = 3$ | $a \mid bc$ | $a \mid b$ | 1 | yes |
| $k = 4$ | $abc \mid d$ | $\{d\}$ alone | 1 | yes |
| $k = 4$ | $abd \mid c$, $ab \mid cd$ | $ab \mid c$ | 1, 3 | yes, yes |
| $k = 4$ | $acd \mid b$, $ac \mid bd$ | $ac \mid b$ | 1, 1 | yes, yes |
| $k = 4$ | $ad \mid bc$, $a \mid bcd$ | $a \mid bc$ | 0, 1 | no, yes |

On three taxa, every split is a single taxon against two, and its index is the length of that taxon's branch in the tree for three taxa: for $c$ it is $\frac{1}{2}(5 + 6 - 3) = 4$. On four taxa, the index of $ab \mid cd$ comes from the term with $a, b$ against $c, d$: $\frac{1}{2}(\max\{10, 12, 6\} - 6) = 3$. The index of $ac \mid bd$ is $\frac{1}{2}(\max\{6, 12, 10\} - 10) = 1$, and the index of $ad \mid bc$ is $\frac{1}{2}(\max\{6, 10, 12\} - 12) = 0$.

**Result.** The d-splits are the four single taxa with index 1, $ab \mid cd$ with index 3, and $ac \mid bd$ with index 1. The sum of these split metrics gives back $d$ exactly, for example $d(a, d) = 1 + 1 + 3 + 1 = 6$, so the rest $d_0$ is zero. The splits $ab \mid cd$ and $ac \mid bd$ are incompatible, so no tree shows both, and the splits graph is a rectangle with sides 3 and 1 and a pendant edge at each corner.

**A five-taxon example.** The tests build $d$ from the circular splits $ab \mid cde$ of weight 3 and $bc \mid ade$ of weight 2, plus a branch of weight 1 at each taxon. The algorithm returns exactly these seven splits and weights. **A split-prime example.** For the graph distances of the complete bipartite graph $K_{3,2}$, with distance 1 between the parts and 2 inside a part, no split has a positive index, and the whole matrix is the rest $d_0$.

## Correctness

The proof rests on one restriction lemma. For a split $A \mid B$ of $X_k$ with $x_k \in A$ and $A \ne \{x_k\}$, the terms of its index are the terms of the index of $A \setminus \{x_k\} \mid B$ on $X_{k-1}$, together with the terms that use $x_k$. So the new index is the minimum of the old index and the new terms, which is line L5, and it is at most the old index. By induction on $k$, the list after step $k$ contains every d-split of $X_k$, because each of them grows from a d-split of $X_{k-1}$ or is the split of $x_k$ alone, and each candidate gets its exact index. Each split appears once, because a candidate determines the split it grew from. The full proof is in the proof file. That the d-splits are weakly compatible, that there are at most $\binom{n}{2}$ of them, and that the rest is split-prime are theorems of Bandelt and Dress, and the tests check them on random inputs.

## Complexity

At step $k$, the list holds at most $\binom{k-1}{2}$ d-splits of $X_{k-1}$, by the theorem of Bandelt and Dress, so there are at most $(k-1)(k-2) + 1$ candidates. The new terms of one candidate number at most $k^3$: the new taxon, one more taxon of its side and two taxa of the other side. Each term costs $O(1)$.

| part | cost |
|---|---|
| candidates at step $k$ | $O(k^2)$ |
| new terms per candidate | $O(k^3)$ |
| step $k$ | $O(k^5)$ |
| all steps | $O(n^6)$ |

The list holds $O(n^2)$ splits of $O(n)$ taxa each, which is $O(n^3)$ space. The rest $d_0$ costs $O(n^4)$ more to compute. A direct method that computes the index of every one of the $2^{n-1} - 1$ splits takes exponential time, which is what the tests use as a reference.

## Properties

- **Canonical.** The d-splits and their indices depend only on $d$, not on the order of the taxa or on any choice. The order only changes the intermediate lists.
- **Generalizes trees.** For a tree metric with positive branch lengths, the d-splits are exactly the splits of the tree, and the indices are the branch lengths.
- **Weakly compatible.** The d-splits never contain three splits $S_1, S_2, S_3$ and four taxa $t_0, \ldots, t_3$ such that each $S_i$ puts $t_0$ and $t_i$ on one side and the other two taxa on the other side. This bounds their number by $\binom{n}{2}$ and keeps the splits graph small.
- **Exact for weakly compatible sums.** If $d$ is a sum of split metrics of a weakly compatible system with positive weights, the method returns exactly these splits and weights. The tests check this for circular systems.
- **Conservative.** The index takes a minimum over all four-taxon comparisons, so one conflicting quartet can remove a split. On large or noisy data, many splits disappear into the rest.
- **Online.** The taxa can arrive one at a time. Each new taxon updates the list without a restart.

## Variants and improvements

- **[NeighborNet](/neighbor-net/)** builds a circular split system by agglomeration and fits weights by least squares. It keeps more signal than split decomposition on large data sets, where the isolation index tends to be small, and it is the usual method today.
- **Split decomposition of other inputs.** The same theory applies to any symmetric function, for example to distances from sequences, from gene contents or from genome rearrangements.
- **Faster implementations.** Practical programs, as in SplitsTree, use the same incremental scheme with careful bookkeeping and pruning. For tree metrics, every step keeps only $O(n)$ splits, and the cost drops accordingly.
- **Other weights.** Least squares weights for the d-splits fit the distances more closely than the isolation indices, at the cost of the canonical form.
- **Graph decomposition.** The name split decomposition is also used for an unrelated decomposition of graphs by Cunningham, which splits a graph along complete bipartite cuts. The two methods have different inputs and outputs.

## When to use it

Use split decomposition to see whether a distance matrix supports a tree, and where it does not. A result with only compatible splits says that a tree fits, and the incompatible splits show which groupings conflict, for example because of recombination or hybridization. It works best for small and well structured data sets, such as a few dozen closely related sequences. For hundreds of taxa, or for noisy distances, use [NeighborNet](/neighbor-net/), because split decomposition then tends to return a nearly star-like result with a large rest.

## Pitfalls

- **Missing the degenerate terms.** The minimum must include the terms with $a = a'$ or $b = b'$. Without them, the index of a split with one taxon on a side is not defined, and the result for three taxa is wrong.
- **Rounding.** The index is a difference of sums, and a tiny positive value from floating point rounding creates a false split. Use exact arithmetic or a tolerance.
- **Reading weights as branch lengths.** A d-split that is not in any tree has no branch. Its index is its weight in the decomposition, which is the length of its parallel edges in the splits graph.
- **Ignoring the rest.** The fraction of $d$ that is in $d_0$ tells how much of the data the splits explain. A good picture with a large rest can be misleading.
- **Confusion with the graph method.** Cunningham's split decomposition of graphs is a different method, despite the same name.

## Implementations

## History

Bandelt and Dress (1992) developed the theory of split decomposition in two papers, a mathematical one in Advances in Mathematics, with the canonical decomposition of a metric into weakly compatible splits and a split-prime rest, and one in Molecular Phylogenetics and Evolution that presented the method for distance data in biology. Huson's SplitsTree program (1998) made the method widely used, and it draws the d-splits as a splits graph, for which Dress and Huson (2004) later gave general construction algorithms. In the 2000s, NeighborNet (Bryant and Moulton 2004) replaced it for many uses, because it keeps more splits on large data sets.

## References
