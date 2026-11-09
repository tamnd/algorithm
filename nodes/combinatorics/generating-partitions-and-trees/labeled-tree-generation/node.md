---
tag: 2AZG8Y
kind: problem
slug: labeled-tree-generation
name: Labeled tree generation
aliases:
- Enumerating labeled trees
- Generating all trees on n labeled vertices
- Listing spanning trees of the complete graph
area: combinatorics/generating-partitions-and-trees
level: core
summary: Enumerate all trees on the vertex set {1..n}; there are n^(n-2) of them.
model: word-ram
complexity:
  vars: {n: the number of vertices, N: the number of labeled trees (n to the power n - 2)}
  time: {worst: Θ(n^2 + N)}
prereqs: [labeled-graph, cayley-formula, pruefer-code]
see_also: [pruefer-decoding, cayley-formula, prufer-sequence, spanning-tree-enumeration, uniform-spanning-tree-sampling, free-tree-generation, k-ary-gray-code, ranking-unranking]
sources:
  - url: https://cp-algorithms.com/graph/pruefer_code.html
    title: cp-algorithms, Prüfer code
    locator: the sections Restoring the tree using the Prüfer code in linear time, Bijection between trees and Prüfer codes, and Cayley's formula (including the count of trees with given degrees)
  - paper: doi:10.1137/S009753979225030X
    title: Sanjiv Kapoor and H. Ramesh, Algorithms for enumerating all spanning trees of undirected and weighted graphs, SIAM Journal on Computing 24(2) (1995), 247 to 265
    locator: the whole paper (O(N + V + E) time when only the change from one tree to the next is output)
  - url: https://page.math.tu-berlin.de/~felsner/SemWS17-18/Ruskey-Comb-Gen.pdf
    title: Frank Ruskey, Combinatorial Generation, working version, University of Victoria, 1995 to 2003
    locator: Section 2.10.2, Rooted Trees (Theorem 2.2, the n^(n-2) labelled free trees, with the bijection of Eğecioğlu and Remmel), and Exercise 26 of Chapter 2 (the Prüfer correspondence)
---

Labeled tree generation is the problem of listing every tree on the vertex set $[n] = \{1, \ldots, n\}$ exactly once, where two trees are different when their edge sets are different. By [Cayley's formula](/cayley-formula/) there are $N = n^{n-2}$ of them for $n \ge 2$. The [Prüfer code](/pruefer-code/) maps them one to one onto the sequences $[n]^{n-2}$, so an odometer over the sequences plus [Prüfer decoding](/pruefer-decoding/) lists all trees in $O(n)$ time per tree. Methods that list the spanning trees of the complete graph $K_n$ and output only the exchange of one edge between consecutive trees reach $O(1)$ amortized time per tree.

## In plain words

Number the dots from 1 to $n$, and connect them with lines so that every dot is reached and there is no loop. You want every such drawing once. Unlike for unlabeled trees, a path 1-2-3 and a path 2-1-3 count as two different trees, because the dots carry names.

The easy way uses the Prüfer code: every list of $n - 2$ numbers from 1 to $n$ is the code of exactly one tree, and every tree has a code. So count through all the lists, like an odometer, and turn each list into its tree.

## Definition

A *labeled tree* on $[n]$ is a connected graph with vertex set $[n]$ and $n - 1$ edges. Let $\mathcal{T}_n$ be the set of these trees, so $|\mathcal{T}_1| = 1$ and $|\mathcal{T}_n| = n^{n-2}$ for $n \ge 2$.

**Input:** an integer $n \ge 1$.

**Output:** a sequence that contains each tree of $\mathcal{T}_n$ exactly once.

**Cost model.** The [word RAM](/word-ram/). In the *full output* model, each tree is written as $n - 1$ edges, or as a code of $n - 2$ numbers, so $\Theta(nN)$ time is necessary. In the *change output* model, the algorithm writes the first tree in full and then, for each next tree, only the edges that leave and enter; this is the model in which $O(1)$ amortized time per tree is possible.

## Variants

- **Code.** The Prüfer code in $[n]^{n-2}$; the parent array of the tree rooted at $n$; an edge list; an adjacency structure.
- **Order.** Lexicographic order of the Prüfer codes, a [Gray code](/gray-code/) of the codes such as the [reflected $n$-ary Gray code](/k-ary-gray-code/), or an order in which consecutive trees differ by one edge exchange.
- **Restricted trees.** Trees with a given degree sequence $d_1, \ldots, d_n$ correspond to codes in which $v$ occurs $d_v - 1$ times, so there are $\frac{(n-2)!}{\prod_v (d_v - 1)!}$ of them, and listing the [permutations of the multiset](/multiset-permutations/) lists them. Trees with $k$ leaves correspond to codes with exactly $n - k$ distinct letters.
- **Rooted trees and forests.** Rooted labeled trees on $[n]$ number $n^{n-1}$, and rooted forests on $[n]$ number $(n + 1)^{n-1}$, by adding a new vertex $n + 1$ joined to every root.
- **Spanning trees of a given graph.** Listing the trees on $[n]$ is listing the spanning trees of $K_n$. For other graphs this is the [spanning tree enumeration](/spanning-tree-enumeration/) problem.
- **Random and direct access.** A uniform random code, decoded, gives a [uniform random tree](/uniform-spanning-tree-sampling/) on $[n]$. Reading the code as a number in base $n$ gives [ranking and unranking](/ranking-unranking/).

## Examples

For $n = 4$ there are $4^2 = 16$ trees. Twelve are paths, one for each order of the 4 vertices up to reversal, $4!/2 = 12$; four are stars, one for each choice of the center. The stars have the codes $(c, c)$ for the center $c$. The paths have the codes $(x, y)$ with $x \ne y$, whose inner vertices are $x$ and $y$.

For $n = 5$ there are $5^3 = 125$ trees: 60 paths, 5 stars, and 60 trees with degrees $3, 2, 1, 1, 1$. In terms of the code, a path has 3 distinct letters, the third shape has 2, and a star has 1.

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| $n^{n-2}$ | 1 | 1 | 3 | 16 | 125 | 1296 | 16807 | 262144 | 4782969 | 100000000 |

So a full listing is practical up to about $n = 10$.

## Known algorithms

| method | order | total time | worst step |
|---|---|---|---|
| all $(n-1)$-subsets of the edges of $K_n$, test each | any | $O\big(\binom{n(n-1)/2}{n-1}\, n\big)$ | large |
| odometer over $[n]^{n-2}$ + [Prüfer decoding](/pruefer-decoding/) | lexicographic in the code | $\Theta(nN)$ | $O(n)$ |
| [spanning tree enumeration](/spanning-tree-enumeration/) on $K_n$ (Gabow and Myers) | depth-first | $O(n^2 + nN)$ | polynomial |
| spanning tree enumeration on $K_n$ with change output (Kapoor and Ramesh) | edge exchanges | $O(n^2 + N)$ | polynomial |

- **Subset testing.** Most $(n-1)$-subsets of the $\binom{n}{2}$ edges are not trees: for $n = 6$ there are $\binom{15}{5} = 3003$ subsets and only 1296 trees, and the fraction falls quickly as $n$ grows. This method is not [output-sensitive](/output-sensitive-generation/).
- **Prüfer odometer.** Step the code like an odometer in base $n$ and decode each code in $\Theta(n)$ time. This is simple and optimal in the full output model. Consecutive codes differ in one letter at the end most of the time, but the decoded trees can differ in many edges, so the decoding cannot be reused cheaply.
- **Spanning tree methods.** The general methods for spanning trees of a graph with $n$ vertices and $m$ edges, run on $K_n$ with $m = \binom{n}{2}$, give $O(n^2 + nN)$ in the full output model and $O(n^2 + N)$ in the change output model.

## Bounds

- Any method visits $N = n^{n-2}$ trees, so $\Omega(N)$ time is necessary. In the change output model the methods above meet it, up to the $O(n^2)$ start.
- In the full output model, the output has $\Theta(nN)$ numbers, and the Prüfer odometer meets this bound.
- $N = n^{n-2}$ grows faster than any exponential $c^n$, so only small $n$ are practical: $10^8$ trees for $n = 10$.

## Reductions

- **To sequences.** The Prüfer bijection reduces the problem to listing $[n]^{n-2}$, plus decoding. Any order on sequences, such as an $n$-ary Gray code, gives an order on trees.
- **To spanning trees.** Labeled trees on $[n]$ are the spanning trees of $K_n$, so every [spanning tree enumeration](/spanning-tree-enumeration/) algorithm solves this problem.
- **To unlabeled trees.** Each unlabeled free tree with automorphism group $A$ appears $n!/|A|$ times among the labeled trees. Listing unlabeled trees first ([free tree generation](/free-tree-generation/)) and then all labelings of each, up to its automorphisms, is another route, but the Prüfer route is much simpler.

## Applications

- Exhaustive tests of graph algorithms on every tree with a small number of labeled vertices, where the labels matter, for example for tie-breaking rules.
- Uniform random labeled trees as test inputs and as models in statistics and in phylogenetics.
- Proofs and checks of counting formulas for trees with degree, leaf or root constraints.

## References
