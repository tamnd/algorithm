---
tag: JGRS6V
kind: algorithm
slug: bionj
name: BIONJ
area: biology/phylogenetics
level: research
summary: Neighbor-joining with a variance-weighted reduction step. The new distances are the weighted average that minimizes a model variance. Exact on tree metrics, O(n^3) time.
solves: [additive-tree-reconstruction]
model: word-ram
complexity:
  vars: {n: the number of taxa}
  time: {worst: "O(n^3)"}
  space: {extra: "O(n^2)"}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1997
  people: [Olivier Gascuel]
  note: Gascuel published BIONJ in Molecular Biology and Evolution in 1997, based on a simple model of the variances and covariances of distances estimated from sequences.
prereqs: [neighbor-joining, tree-metric]
see_also: [additive-tree-reconstruction, minimum-evolution, fitch-margoliash, least-squares-phylogeny, jukes-cantor-model]
sources:
  - paper: doi:10.1093/oxfordjournals.molbev.a025808
    title: Olivier Gascuel, BIONJ, an improved version of the NJ algorithm based on a simple model of sequence data, Molecular Biology and Evolution 14(7), 1997, pages 685 to 695
    locator: the variance model, the reduction formula with the weight lambda, and the simulations
  - paper: doi:10.1093/oxfordjournals.molbev.a040527
    title: James A. Studier and Karl J. Keppler, A note on the neighbor-joining algorithm of Saitou and Nei, Molecular Biology and Evolution 5(6), 1988, pages 729 to 731
    locator: the Q-criterion that BIONJ uses for selection
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, 2004
    locator: Chapter 11, Distance matrix methods
---

BIONJ is a variant of [neighbor-joining](/neighbor-joining/) for building an unrooted [phylogenetic tree](/phylogenetic-tree/) from a distance matrix of $n$ taxa. It selects the pair to join with the same $Q$-criterion, but it computes the distances from the new node as a weighted average $\lambda (D_{ik} - \delta_{iu}) + (1 - \lambda)(D_{jk} - \delta_{ju})$, where $\lambda$ minimizes the variance of the new distances under a simple model of sequence data. Like neighbor-joining it returns the true tree on a [tree metric](/tree-metric/), in $O(n^3)$ time. Olivier Gascuel published it in 1997.

## In plain words

Distances computed from sequences are noisy, and long distances are noisier than short ones. Neighbor-joining ignores this: when it merges two taxa into a new node, it takes the plain average of what the two taxa say about the distance from that node to each other taxon. BIONJ keeps a second table with an estimate of the noise in each distance. When it merges two taxa, it trusts the taxon whose distances are less noisy more, and it picks the weight that makes the new distances as reliable as possible. It also updates the noise table for the new node. The choice of which pair to merge does not change. When the distances come exactly from a tree, both taxa say the same thing, so the weight has no effect and BIONJ rebuilds the tree.

## The problem

The input is $n \ge 2$ taxa and a symmetric $n \times n$ matrix $D$ with zero diagonal, usually estimated from $m$ aligned sites under a substitution model. The output is an unrooted binary tree with the taxa as leaves and real edge lengths. The exact goal is [additive tree reconstruction](/additive-tree-reconstruction/); on other inputs BIONJ is a heuristic. It builds one tree with $n - 2$ greedy joins and does not search the $(2n-5)!!$ unrooted binary trees.

The variance model of Gascuel (1997) has two parts. The variance of an estimated distance $D_{ij}$ is proportional to $D_{ij}$, so the algorithm starts with $V = D$. For a pair $i, j$ that is joined at a node $p$, the covariance of $D_{ik}$ and $D_{jk}$ is the variance of the shared part of the two paths, from $p$ to $k$, which the model estimates by $\frac{1}{2}(V_{ik} + V_{jk} - V_{ij})$.

## The algorithm

```pseudo id=main
BIONJ(D, n)
L1  A ← {1, ..., n}; V ← D; r ← n
L2  while r > 2 do
L3      for each i ∈ A do R_i ← Σ_{k ∈ A} D_ik
L4      (i, j) ← a pair of A that minimizes Q(i, j) = (r − 2) D_ij − R_i − R_j
L5      create a new node u; δ_iu ← D_ij / 2 + (R_i − R_j) / (2(r − 2)); δ_ju ← D_ij − δ_iu
L6      add the edges (i, u) of length δ_iu and (j, u) of length δ_ju
L7      λ ← 1/2 if V_ij = 0, else 1/2 + Σ_{k ∈ A \ {i, j}} (V_jk − V_ik) / (2(r − 2) V_ij), clipped to [0, 1]
L8      for each k ∈ A \ {i, j} do D_uk ← D_ku ← λ (D_ik − δ_iu) + (1 − λ)(D_jk − δ_ju)
L9                                 V_uk ← V_ku ← λ V_ik + (1 − λ) V_jk − λ (1 − λ) V_ij
L10     A ← (A \ {i, j}) ∪ {u}; r ← r − 1
L11 let A = {a, b}; add the edge (a, b) of length D_ab
L12 return the edges
```

Lines L3 to L6 are neighbor-joining. Line L7 is the new step. Each of $D_{ik} - \delta_{iu}$ and $D_{jk} - \delta_{ju}$ estimates the distance from $u$ to $k$, and line L8 mixes them. With $\lambda = 1/2$, line L8 is $(D_{ik} + D_{jk} - D_{ij})/2$, the reduction of neighbor-joining. When the distances from $j$ have larger variances than those from $i$, the sum in line L7 is positive and $\lambda > 1/2$, so $i$ gets more weight. Line L9 stores the model variance of the new distances.

## Example

The five taxa A to E have this matrix, which is not a tree metric.

| | A | B | C | D | E |
|---|---|---|---|---|---|
| A | 0 | 9 | 11 | 10 | 9 |
| B | 9 | 0 | 3 | 8 | 9 |
| C | 11 | 3 | 0 | 11 | 7 |
| D | 10 | 8 | 11 | 0 | 10 |
| E | 9 | 9 | 7 | 10 | 0 |

**Pass 1, $r = 5$.** The row sums are $R = (39, 29, 32, 39, 35)$, and the smallest $Q$ is $Q(B, C) = 3 \cdot 3 - 29 - 32 = -52$; the next is $Q(A, D) = -48$. Both methods join B and C into $u_1$ with $\delta_B = 3/2 + (29 - 32)/6 = 1$ and $\delta_C = 2$. Now they differ. With $V = D$, the sum in line L7 is $(11 - 9) + (11 - 8) + (7 - 9) = 3$ over $k = $ A, D, E, so $\lambda = 1/2 + 3/(2 \cdot 3 \cdot 3) = 2/3$. B gets the larger weight, because its distances to A, D and E are shorter.

| new entry | to A | to D | to E | variance sum |
|---|---|---|---|---|
| NJ, $\lambda = 1/2$: $D_{u_1 k}$ | 17/2 | 8 | 13/2 | 101/4 |
| BIONJ, $\lambda = 2/3$: $D_{u_1 k}$ | 25/3 | 23/3 | 7 | 25 |

The last column is the sum of the three model variances, $\sum_k V_{u_1 k}$; BIONJ makes it smaller, as it must. For example $D_{u_1 A} = \frac{2}{3}(9 - 1) + \frac{1}{3}(11 - 2) = 25/3$ and $V_{u_1 A} = \frac{2}{3} \cdot 9 + \frac{1}{3} \cdot 11 - \frac{2}{9} \cdot 3 = 9$.

**Pass 2, $r = 4$.** On the neighbor-joining matrix, the smallest $Q$ is $-71/2$, for A with D (and for E with $u_1$, the other side of the same split). On the BIONJ matrix, the smallest $Q$ is $-106/3$, for A with E (and for D with $u_1$). So the final trees differ: neighbor-joining returns `((B,C),E,(A,D));` and BIONJ returns `((B,C),D,(A,E));`. A small change in one row of the reduced matrix changes the topology.

## Correctness

Two facts hold. First, on the leaf metric of a binary tree with positive edge lengths, BIONJ returns that tree with its edge lengths, for every $\lambda$. The selection in lines L3 to L5 is that of neighbor-joining, so the joined pair is a cherry with common neighbor $p$, and both $D_{ik} - \delta_{iu}$ and $D_{jk} - \delta_{ju}$ equal the distance from $p$ to $k$; any average of two equal numbers is that number, so the reduced matrix is the leaf metric of the smaller tree, and induction finishes the proof. Second, the variance sum is a convex quadratic in $\lambda$ with leading coefficient $(r - 2) V_{ij}$, and the formula of line L7 is its minimum, clipped to $[0, 1]$. The full proof is in the proof file.

## Complexity

The model is the word RAM with unit-cost arithmetic on the entries. Lines L3 and L4 take $O(r^2)$ time per pass, as in neighbor-joining. Line L7 takes $O(r)$ time, and lines L8 and L9 take $O(r)$ time. Summed over $r = n, \ldots, 3$, the time is $O(n^3)$ in the worst case. The two matrices $D$ and $V$ take $O(n^2)$ space; this is about twice the memory of neighbor-joining.

## Properties

- **Same selection, different reduction.** BIONJ changes only lines L7 to L9. With $\lambda = 1/2$ at every step it is neighbor-joining.
- **Exact on tree metrics.** It returns the tree for every choice of $\lambda$, so the weight never hurts on perfect data.
- **Weight in range.** The clip to $[0, 1]$ keeps the new distance between the two estimates, so a large error in one row cannot push it outside them.
- **Better accuracy on simulated data.** In the simulations of Gascuel (1997), BIONJ recovered the true topology more often than neighbor-joining, with the largest gains for trees with large distances and unequal rates.
- **Unrooted output, possibly negative lengths.** As with neighbor-joining, the output is unrooted, and on non-additive input line L5 can give a negative edge length.

## Variants and improvements

- **Other variance models.** The model $V = D$ fits distances whose variance grows linearly. A program can start from other estimates of the variances, for example from a substitution model, and keep lines L7 to L9.
- **Weighbor** (Bruno, Socci and Halpern 2000) uses a likelihood-based model also in the selection step, not only in the reduction.
- **As a starting tree.** Programs such as FastME and PhyML build a BIONJ tree first and then improve it with [nearest neighbor interchanges](/nearest-neighbor-interchange/) or [subtree prune and regraft](/subtree-prune-and-regraft/) moves under [minimum evolution](/minimum-evolution/) or [maximum likelihood](/maximum-likelihood-phylogeny/).

## When to use it

Use BIONJ in place of neighbor-joining when the distances come from sequences and some of them are long, because it uses the same time and almost the same code. It is a good starting tree for a likelihood or minimum evolution search. On distances that are not estimates from sequences, such as a matrix of exact path lengths or of costs, the variance model has no meaning, and plain neighbor-joining is just as good.

## Pitfalls

- **Dividing by zero.** When $V_{ij} = 0$ the formula of line L7 is undefined. Use $\lambda = 1/2$, as line L7 does.
- **Forgetting the clip.** Without the clip $\lambda$ can be negative or larger than 1, and the new distance is no longer a weighted average of the two estimates.
- **Updating $V$ with the wrong formula.** $V_{uk}$ has the term $-\lambda(1 - \lambda) V_{ij}$ for the covariance. Without it the variances grow with each join, and later weights are wrong.
- **Changing the selection.** BIONJ uses the $Q$-criterion of $D$, not of $V$. A version that selects on the variances is a different method with no exactness proof.

## Implementations

## History

Gascuel (1997) introduced BIONJ. He kept the selection of Saitou and Nei, in the form of Studier and Keppler (1988), and changed the reduction step using a first-order model of the variances and covariances of evolutionary distances. Later work on [minimum evolution](/minimum-evolution/) by Desper and Gascuel used BIONJ trees as starting points for tree search.

## References
