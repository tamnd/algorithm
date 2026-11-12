---
tag: D5Z0XF
kind: definition
slug: expander-codes
name: Expander codes
area: compression-and-coding/error-correcting-codes
level: research
summary: Codes defined on a Tanner graph in which every small set of bits has many neighbor checks. A simple flipping decoder then corrects a constant fraction of errors in linear time.
history:
  year: 1996
  people: [Michael Sipser, Daniel A. Spielman, Gilles Zémor, R. Michael Tanner]
  note: Tanner built codes on graphs in 1981. Sipser and Spielman in 1996 proved that vertex expansion gives linear-time decoding of a constant fraction of errors, and Zémor in 2001 gave a simpler construction and decoder on the double cover of a spectral expander.
prereqs: [ldpc-code, tanner-graph, bipartite-graph]
see_also: [bit-flipping-decoding, minimum-distance, product-codes, gilbert-varshamov-bound, probabilistic-method, spectral-gap, halver, expander-walk-sampler]
sources:
  - paper: "M. Sipser and D. A. Spielman, Expander codes, IEEE Transactions on Information Theory 42(6), 1996, pages 1710 to 1722"
    title: Expander codes
    locator: The codes of an expanding bipartite graph, the bound on their distance, and the sequential and parallel flipping decoders that correct a constant fraction of errors when the expansion is greater than 3/4 of the degree
  - paper: "G. Zémor, On expander codes, IEEE Transactions on Information Theory 47(2), 2001, pages 835 to 837"
    title: On expander codes
    locator: Codes on the edges of a bipartite spectral expander with a small code at each vertex, and the decoder that alternates between the two sides
  - paper: doi:10.1109/TIT.1981.1056404
    title: R. M. Tanner, A recursive approach to low complexity codes, IEEE Transactions on Information Theory 27(5), 1981, pages 533 to 547
    locator: Codes defined by a bipartite graph of digits and subcodes, and a lower bound on their distance from the girth of the graph
  - paper: "D. A. Spielman, Linear-time encodable and decodable error-correcting codes, IEEE Transactions on Information Theory 42(6), 1996, pages 1723 to 1731"
    title: Linear-time encodable and decodable error-correcting codes
    locator: Asymptotically good codes built from expander codes with both encoding and decoding in linear time
---

Expander codes are binary linear codes defined on a [Tanner graph](/tanner-graph/) that is a good expander: every small set of variable nodes has many check node neighbors, close to the largest number the degrees allow. Sipser and Spielman showed in 1996 that this one property gives two results at once. The code has a minimum distance that grows linearly with the length, and a simple flipping decoder, a form of [bit-flipping decoding](/bit-flipping-decoding/), corrects every error pattern up to a constant fraction of the length in linear time. With parity checks at the check nodes an expander code is an [LDPC code](/ldpc-code/) whose graph has a proven expansion. With a small code at each node instead of a parity check, as in Tanner's graphs, Zémor gave a simpler form on the double cover of a spectral expander. Expander codes were among the first asymptotically good codes with a decoder in linear time.

## Definition

**Biregular graph.** Let $G$ be a [bipartite graph](/bipartite-graph/) with $n$ variable nodes, each of degree $c$, and $m$ check nodes, each of degree $d$, so $n c = m d$. For a set $S$ of variable nodes, $N(S)$ is the set of check nodes with at least one neighbor in $S$.

**Vertex expansion.** $G$ is an $(A, \delta)$ *expander* when every set $S$ of variable nodes with $|S| \le A$ has

$$|N(S)| \ge \delta c |S|.$$

Since $S$ has $c|S|$ edges, $\delta \le 1$ always. Families of interest have $A = \alpha n$ for a constant $\alpha > 0$ and $\delta$ fixed as $n$ grows.

**Expander code.** The code $C(G)$ is the set of words $x \in \{0, 1\}^n$ such that at each check node the bits of its neighbors add to 0 mod 2. It is the code of the [parity-check matrix](/parity-check-matrix/) whose Tanner graph is $G$. The $m$ checks give rate at least $1 - m/n = 1 - c/d$. In the general form of Sipser and Spielman, each check node requires its $d$ bits to form a word of a fixed code $C_0$ of length $d$, not only to have even parity.

**Unique neighbors.** A check in $N(S)$ is a *unique neighbor* of $S$ if exactly one of its neighbors is in $S$. If $|N(S)| \ge \delta c |S|$, the number $U$ of unique neighbors is at least $(2\delta - 1) c |S|$: each check in $N(S)$ that is not unique takes at least two of the $c|S|$ edges, so $c|S| \ge U + 2(|N(S)| - U)$, and $U \ge 2|N(S)| - c|S|$.

**Distance.** If $\delta > 1/2$, every nonzero codeword has weight greater than $A$. *Proof.* Let $S$ be the support of a codeword with $|S| \le A$. Every check in $N(S)$ has an even, so nonzero at least two, number of neighbors in $S$, so there is no unique neighbor, and $U = 0$. But $U \ge (2\delta - 1) c|S| > 0$ if $S$ is not empty. $\square$

**Theorem (Sipser and Spielman).** Let $G$ be an $(A, \delta)$ expander with $3/4 < \delta < 1$. Then the sequential flipping decoder below, given a codeword with at most $(2\delta - 1) A$ bits flipped, returns that codeword after at most $c$ times as many flips as there are errors.

The decoder flips, one at a time, any variable that has more unsatisfied than satisfied checks among its $c$ checks, and keeps the counts up to date after each flip.

```pseudo id=main
EXPANDER-FLIP-DECODE(G, r)
L1  w ← r
L2  for each check i: s_i ← parity of the bits of w at the neighbors of i      ▷ 1 means unsatisfied
L3  for each variable j: b_j ← |{ i ∈ N(j) : s_i = 1 }|; put j in a queue Q if 2 b_j > c
    while Q is not empty do
        take j from Q
L4      if 2 b_j ≤ c then skip j                                      ▷ it changed since it was queued
L5      w_j ← 1 − w_j
L6      for each check i of j: s_i ← 1 − s_i
L7          for each variable k of i: update b_k by ±1, and put k in Q if 2 b_k > c
L8  return w
```

*Proof of the theorem.* Let $S$ be the set of positions where $w$ differs from the sent codeword, $s = |S|$, and $u$ the number of unsatisfied checks. At the start $s = s_0 \le (2\delta - 1) A$ and $u = u_0 \le c s_0$, since only the checks in $N(S)$ can be unsatisfied.

1. *Each flip lowers $u$.* A flipped variable has $b > c/2$ unsatisfied checks and $c - b$ satisfied ones. The flip turns them around, so $u$ changes by $c - 2b \le -1$. So there are at most $u_0 \le c s_0$ flips, and the decoder stops.
2. *While $0 < s \le A$, some variable can be flipped.* Every unique neighbor of $S$ sees exactly one error, so it is unsatisfied, and $u \ge U \ge (2\delta - 1) c s > c s / 2$, because $\delta > 3/4$. Every unsatisfied check is in $N(S)$, so the sum over $j \in S$ of the unsatisfied checks of $j$ is at least $u > c s / 2$, and some $j \in S$ has more than $c/2$.
3. *$s$ stays below $A$.* Each flip changes $s$ by 1, and $s_0 \le (2\delta - 1) A < A$ because $\delta < 1$. If $s$ ever reached $A$, it would be after at least one flip, so $u < u_0 \le c s_0 \le (2\delta - 1) c A$. But at that moment the bound of step 2 gives $u \ge (2\delta - 1) c A$, which is a contradiction.
4. *At the stop, $s = 0$.* The decoder stops when no variable has more than $c/2$ unsatisfied checks. By steps 2 and 3 this cannot happen with $0 < s \le A$, so $s = 0$. $\blacksquare$

The bound $\delta < 1$ matters. Every graph without double edges is a $(1, 1)$ expander, and the formula would then promise one corrected error. But if two variables have the same checks, an error at one of them gives both the full count $c$, and the decoder may flip the other one and stop at a wrong codeword. For $A \ge 2$, $\delta = 1$ would mean that no two variables share a check, so the bound loses nothing of interest.

**Linear time.** Each flip costs $O(c d)$ work in lines L6 and L7, and there are at most $c s_0$ flips. The setup of lines L1 to L3 costs $O(n c)$. So the decoder runs in $O(n c + c^2 d s_0)$ time, linear in $n$ for fixed degrees. Sipser and Spielman also gave a parallel form that flips all such variables at once and needs $O(\log n)$ rounds.

**Zémor's form.** Let $H$ be a $\Delta$-regular graph with $n$ vertices, and let $G$ be its double cover: a bipartite graph with two copies of the vertices, left and right, and an edge for each edge of $H$ in each direction. The bits are the $n \Delta$ edges of $G$. Each vertex requires its $\Delta$ edges to form a word of a fixed linear code $C_0$ of length $\Delta$, rate $r_0$ and relative distance $\delta_0$. The rate is at least $2 r_0 - 1$. The decoder decodes $C_0$ at all left vertices in parallel, then at all right vertices, and so on. Zémor proved that when the second largest eigenvalue $\lambda$ of $H$ is small compared with $\Delta$, the decoder corrects every error pattern of weight up to about $\delta_0^2 / 4$ times the length, in a number of rounds logarithmic in $n$. The proof uses the [spectral gap](/spectral-gap/) of $H$ instead of vertex expansion.

## Examples and non-examples

**An array graph.** For the prime $p = 7$ and $c = 6$, take the variables $(b, x)$ with $0 \le b, x < 7$ and the checks $(a, r)$ with $0 \le a < 6$, $0 \le r < 7$; check $(a, r)$ holds the variables with $x = r + a b \bmod 7$. This gives $n = 49$ variables of degree 6 and 42 checks of degree 7. Two variables share at most one check, because at most one line $x = r + a b$ goes through two points. The code has dimension 12, so rate $12/49$, above the bound $1 - 6/7 = 1/7$ because the checks are dependent.

The implementation measures the expansion by brute force over all sets of up to 4 variables. The least neighbor counts are 6 for one variable, 11 for two (they share a check), 15 for three and 18 for four, so the ratio $|N(S)| / (c |S|)$ falls from $1$ to $11/12$, $5/6$ and $3/4$. So $G$ is a $(3, 5/6)$ expander, and the theorem guarantees the correction of $\lfloor (2 \cdot 5/6 - 1) \cdot 3 \rfloor = 2$ errors. With $A = 4$ the ratio is $3/4$, which is not above $3/4$, so the theorem gives nothing more. Since $3/4 > 1/2$, the distance result still says that no nonzero codeword has weight at most 4.

The tests check the unique neighbor step directly: every set $S$ of 1, 2 or 3 variables has a member with more than 3 of its 6 checks in odd parity with $S$. They decode every error pattern of weight 0, 1 and 2 on random codewords, with at most $6 w$ flips. Past the guarantee, all of 300 random patterns of weight 3 still decode, and 132 of 300 of weight 4. The same construction with $c = 5$ guarantees only one error.

This graph is far too small for the asymptotic theorem to matter in practice; it shows how the definitions fit together on a case that can be checked by hand and by brute force.

**Random graphs.** Sipser and Spielman showed with the [probabilistic method](/probabilistic-method/) that for a large enough $c$, a random $(c, d)$-biregular graph is, with high probability, an $(\alpha n, \delta)$ expander with $\delta > 3/4$ for some constant $\alpha > 0$. So good expander codes exist, with distance and decoding radius linear in $n$. Explicit graphs with such vertex expansion came later, from the lossless expanders of Capalbo, Reingold, Vadhan and Wigderson in 2002.

**Non-example: equal columns.** If two variables have the same set of checks, the set $S$ of both has $|N(S)| = c = c|S|/2$, so $\delta \le 1/2$ for $A \ge 2$, and indeed the word with ones at those two positions is a codeword of weight 2.

**Non-example: column weight 2.** If $c = 2$, each variable is an edge between two checks, and a set of variables that forms a cycle in that graph of checks has exactly as many neighbors as members, $|N(S)| = |S| = c|S|/2$. Such a cycle is a codeword. A graph with bounded degree has cycles of length $O(\log n)$, so these codes have distance $O(\log n)$ and are never expander codes with linear $A$ and $\delta > 1/2$.

**Non-example: a Tanner graph with good girth only.** Large girth gives expansion only for small sets: a graph of girth $g$ makes every set of fewer than about $g/2$ variables look like a tree, but it says nothing about sets of linear size. An LDPC code with large girth need not have a linear decoding radius for flipping.

## Related definitions

- **LDPC codes.** Expander codes with parity checks are LDPC codes, and belief propagation also works on them. The expander theorem gives a guarantee for every error pattern up to a radius, while density evolution gives the typical behavior of [belief propagation decoding](/belief-propagation-decoding/) and is usually much better in practice.
- **Bit flipping.** The decoder of the theorem is the sequential form of Gallager's bit flipping, with the threshold "more than half of the checks". The parallel largest count form of [bit-flipping decoding](/bit-flipping-decoding/) has no such guarantee in general.
- **Product codes.** Zémor's codes on a complete bipartite graph are the [product codes](/product-codes/) of $C_0$ with itself, and his decoder is the usual row and column decoder. The expander graph replaces the complete graph, which keeps the degree fixed as the length grows.
- **Spectral and vertex expansion.** A $\Delta$-regular graph with a large [spectral gap](/spectral-gap/) has good edge expansion, but spectral bounds alone cannot certify vertex expansion above half the degree. This is why Sipser and Spielman needed random graphs for the flipping decoder, and why Zémor's form, which needs only spectral expansion, is explicit.
- **Distance bounds.** The distance of good expander codes is linear in $n$, but below the [Gilbert-Varshamov bound](/gilbert-varshamov-bound/). Later work of Barg and Zémor and of Guruswami and Indyk used expander codes for codes with good rates and linear-time decoding.

## References
