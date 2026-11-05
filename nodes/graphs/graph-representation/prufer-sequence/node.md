---
tag: QT2985
kind: concept
slug: prufer-sequence
name: Prüfer sequence
aliases:
- Prufer code
area: graphs/graph-representation
level: core
summary: Bijective encoding of labelled trees on n vertices as sequences of length n−2.
prereqs: [tree, labeled-graph, degree]
see_also: [pruefer-code, cayley-formula, free-tree-properties, matrix-tree-theorem, counting-spanning-trees, uniform-spanning-tree-sampling, parent-pointer-tree]
sources:
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 2.2 (Spanning trees and enumeration), the Prüfer code, its inverse, and Cayley's formula with the count of trees with given degrees
  - paper: Heinz Prüfer, Neuer Beweis eines Satzes über Permutationen, Archiv der Mathematik und Physik, series 3, volume 27, 1918
    locator: pages 142 to 144, the original encoding of labeled trees by sequences
  - paper: Arthur Cayley, A theorem on trees, Quarterly Journal of Pure and Applied Mathematics 23, 1889
    locator: pages 376 to 378, the statement that there are n^(n-2) trees on n labeled vertices
---

The Prüfer sequence of a [tree](/tree/) on the [labeled](/labeled-graph/) vertex set $\{1, \ldots, n\}$, for $n \ge 2$, is the sequence of $n - 2$ labels that you get by removing the leaf with the smallest label $n - 2$ times and writing down its neighbour each time. The map from trees to sequences is a bijection onto $\{1, \ldots, n\}^{n-2}$, so it proves [Cayley's formula](/cayley-formula/): there are exactly $n^{n-2}$ labeled trees on $n$ vertices. Each vertex $v$ appears $d(v) - 1$ times in the sequence, where $d(v)$ is its [degree](/degree/). Both the encoding and the decoding run in $O(n)$ time.

## In plain words

Take a tree whose dots carry the numbers 1 to the number of dots. Find the leaf with the smallest number, write down the number of the dot it hangs from, and erase the leaf. Do this again and again until only two dots are left. The list of numbers you wrote down is the code of the tree.

The code is shorter than a list of the edges, and it has no rules: any list of the right length, using any numbers in the range, is the code of exactly one tree. You can rebuild the tree from it. A dot that hangs many leaves shows up many times, and a leaf never shows up at all. This makes the code a simple way to count trees, to store them, and to pick a random tree fairly.

## The idea

Fix $n \ge 2$ and let $T$ be a tree with the vertex set $[n] = \{1, \ldots, n\}$. The labels give a [total order](/total-order/) on the vertices, which is what makes "the smallest leaf" well defined.

**Encoding.** Set $T_1 = T$. For $i = 1, \ldots, n - 2$: let $\ell_i$ be the leaf of $T_i$ with the smallest label, let $a_i$ be its unique neighbour, and let $T_{i+1} = T_i - \ell_i$. The Prüfer sequence is $P(T) = (a_1, \ldots, a_{n-2})$. Each $T_i$ is a tree with $n - i + 1 \ge 3$ vertices for $i \le n - 2$, so it has at least two leaves and $\ell_i$ exists. At the end, $T_{n-1}$ is a single edge. For $n = 2$ the sequence is empty.

**Decoding.** Given $(a_1, \ldots, a_{n-2}) \in [n]^{n-2}$, set $d(v) = 1 + |\{i : a_i = v\}|$ for each $v$. For $i = 1, \ldots, n - 2$: let $\ell_i$ be the smallest $v$ with $d(v) = 1$, add the edge $\{\ell_i, a_i\}$, set $d(\ell_i) \leftarrow 0$ and $d(a_i) \leftarrow d(a_i) - 1$. At the end, exactly two vertices have $d = 1$; add the edge between them.

**Lemma 1 (degrees).** In $P(T)$, each vertex $v$ appears exactly $d_T(v) - 1$ times. *Proof.* The vertex $v$ is written once for each neighbour of $v$ that is removed while $v$ is still in the tree. If $v$ is removed, at step $i$, it is a leaf of $T_i$, so $d_T(v) - 1$ of its neighbours were removed before it, and none after. If $v$ is one of the two vertices of $T_{n-1}$, then it has exactly one neighbour left in $T_{n-1}$, so again $d_T(v) - 1$ of its neighbours were removed. In both cases $v$ was written $d_T(v) - 1$ times. $\square$

So the leaves of $T$ are exactly the vertices that do not occur in $P(T)$, and the first removed leaf $\ell_1$ is the smallest label that does not occur in $(a_1, \ldots, a_{n-2})$.

**Theorem (Prüfer).** For each $n \ge 2$, $P$ is a bijection from the labeled trees on $[n]$ to $[n]^{n-2}$, and decoding is its inverse.

*Proof.* We prove a slightly more general claim by induction on $n$: for each set $S$ of $n \ge 2$ integers, $P$ is a bijection from the trees on $S$ to $S^{n-2}$, and decoding inverts it. For $n = 2$ there is one tree on $S$ and one sequence, the empty one. Let $n \ge 3$.

*Injective.* Let $T$ and $T'$ be trees on $S$ with $P(T) = P(T') = (a_1, \ldots, a_{n-2})$. By Lemma 1 the leaves of both are the elements of $S$ that do not occur in the sequence, so both remove the same first leaf $\ell_1$, and both attach it to $a_1$. Then $T - \ell_1$ and $T' - \ell_1$ are trees on $S \setminus \{\ell_1\}$ with the same sequence $(a_2, \ldots, a_{n-2})$, so they are equal by induction, and $T = T'$.

*Surjective, and decoding is the inverse.* Let $(a_1, \ldots, a_{n-2}) \in S^{n-2}$. Some element of $S$ does not occur in it, since $|S| = n > n - 2$; let $\ell_1$ be the smallest one, which is the first leaf the decoder picks. The element $\ell_1$ does not occur in $(a_2, \ldots, a_{n-2})$, and $a_1 \ne \ell_1$, so $(a_2, \ldots, a_{n-2}) \in (S \setminus \{\ell_1\})^{n-3}$. By induction, it is the sequence of a tree $T'$ on $S \setminus \{\ell_1\}$, and the decoder, which from step 2 on runs on exactly these counts, builds $T'$. Let $T = T' + \{\ell_1, a_1\}$, a tree on $S$ because $a_1 \in S \setminus \{\ell_1\}$ is a vertex of $T'$ and $\ell_1$ is new. In $T$, the leaves are the elements that do not occur in the sequence (Lemma 1 applied to $T'$, plus $\ell_1$, plus the change of $a_1$), so the smallest leaf of $T$ is $\ell_1$ and its neighbour is $a_1$. Hence $P(T) = (a_1, a_2, \ldots, a_{n-2})$, and $T$ is the output of the decoder. $\square$

**Cayley's formula.** The bijection gives $|\{\text{trees on } [n]\}| = n^{n-2}$ for $n \ge 2$. By Lemma 1 it also counts the trees with given degrees: for $d_1, \ldots, d_n \ge 1$ with $\sum_v d_v = 2n - 2$, the number of trees with $d_T(v) = d_v$ for each $v$ is the number of sequences in which each $v$ occurs $d_v - 1$ times,

$$\binom{n - 2}{d_1 - 1, \ldots, d_n - 1} = \frac{(n-2)!}{\prod_{v=1}^{n} (d_v - 1)!}.$$

**Linear time.** A heap of the current leaves gives $O(n \log n)$ time. A linear method keeps a pointer $p$ to the smallest leaf index found so far. After it removes the leaf $\ell$ with neighbour $a$, if $a$ has become a leaf and $a < p$, then $a$ is the next leaf to remove, because every leaf below $p$ was already removed; otherwise the pointer moves up to the next index with degree 1. The pointer only moves up, so the scan costs $O(n)$ in total, and each step does $O(1)$ other work. The tree must be given with its neighbours, for example as an [adjacency list](/adjacency-list/) or as a [parent array](/parent-pointer-tree/) rooted at $n$, since the vertex $n$ is never removed (it is never the smallest leaf while another leaf exists). The decoder runs in $O(n)$ time with the same pointer.

## Examples

Take the tree on $[8]$ with the edges $15, 25, 45, 34, 46, 67, 68$.

| step $i$ | leaves of $T_i$ | smallest leaf $\ell_i$ | neighbour $a_i$ |
|---|---|---|---|
| 1 | 1, 2, 3, 7, 8 | 1 | 5 |
| 2 | 2, 3, 7, 8 | 2 | 5 |
| 3 | 3, 5, 7, 8 | 3 | 4 |
| 4 | 5, 7, 8 | 5 | 4 |
| 5 | 4, 7, 8 | 4 | 6 |
| 6 | 7, 8 | 7 | 6 |

The two vertices left are 6 and 8. So $P(T) = (5, 5, 4, 4, 6, 6)$. The vertices 4, 5 and 6 have degree 3 and occur twice each; the leaves 1, 2, 3, 7, 8 do not occur.

To decode $(5, 5, 4, 4, 6, 6)$ with $n = 8$, start from $d = (1, 1, 1, 3, 3, 3, 1, 1)$ for the vertices 1 to 8. The smallest vertex with $d = 1$ is 1, so add $15$; then 2, so add $25$; then 3, so add $34$. Now $d(5) = 1$ and 5 is the smallest, so add $54$; then $d(4) = 1$, so add $46$; then 7, so add $76$. The vertices 6 and 8 are left with $d = 1$, so add $68$. The seven edges are those of $T$.

**Counts.** For $n = 2, 3, 4, 5, 6$ there are $1, 3, 16, 125, 1296$ labeled trees, which is $n^{n-2}$. For $n = 4$, the 16 trees are 4 stars (the sequences $(v, v)$) and 12 paths (the sequences $(u, v)$ with $u \ne v$). A path on $[4]$ has the two inner vertices of degree 2, and the formula gives $\frac{2!}{1!\,1!} = 2$ paths for each choice of the two inner vertices, so $\binom{4}{2} \cdot 2 = 12$.

**Labels matter.** The sequence encodes a labeled tree, not a shape. The paths $1\text{-}2\text{-}3\text{-}4$ and $2\text{-}1\text{-}3\text{-}4$ are isomorphic, but their sequences are $(2, 3)$ and $(1, 3)$. On 4 vertices there are 16 labeled trees and only 2 shapes, the path and the star.

**Not a tree.** The encoding is defined only for trees. A graph with a cycle and no leaf, such as the cycle $C_n$, stops at the first step. A [spanning forest](/spanning-forest/) with two or more components runs out of leaves in one component and then removes vertices that are not leaves of the whole, so the decoder does not give it back.

## Where it is used

- **Counting.** It gives a bijective proof of [Cayley's formula](/cayley-formula/), the number of spanning trees of $K_n$, which the [matrix-tree theorem](/matrix-tree-theorem/) proves by a determinant, and the count of trees with a given degree sequence.
- **Random trees.** A uniform random sequence in $[n]^{n-2}$, decoded, is a uniform random labeled tree in $O(n)$ time. For [uniform spanning trees](/uniform-spanning-tree-sampling/) of a general graph, other methods are needed.
- **Storage and enumeration.** A labeled tree fits in $n - 2$ numbers, against $n - 1$ edges of 2 numbers each, and the trees on $[n]$ can be listed by listing the sequences in lexicographic order.
- **Genetic algorithms on trees.** Search methods that change a tree by a small edit can work on its sequence, where each edit gives a valid tree. A change of one entry can change many edges, so this code has poor locality.

## References
