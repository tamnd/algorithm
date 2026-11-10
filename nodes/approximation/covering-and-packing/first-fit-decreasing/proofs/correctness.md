---
title: First fit decreasing is feasible and uses at most 3/2 OPT bins; the 11/9 bound
proves: [correctness]
status: full
---

We use the pseudocode of the page. The input is a list of sizes in $(0, 1]$, line L1 sorts it as $s_1 \ge s_2 \ge \cdots \ge s_n$, the bins are $B_1, \ldots, B_k$ in the order in which line L5 opens them, and $\ell(B)$ is the final load of $B$. We write $\mathrm{FFD} = k$ and $S = \sum_i s_i$. The proofs of feasibility and of the factor $\frac32$ are full. The proof of the bound $\frac{11}{9}\mathrm{OPT} + \frac69$ is a sketch with a citation.

**Lemma 1 (feasibility).** First fit decreasing returns a partition of the items into bins, and each bin has load at most 1.

*Proof.* Line L1 only reorders the items. Lines L3 to L6 are [first fit](/first-fit-bin-packing/) on the sorted list, which puts each item into exactly one bin and never makes a load larger than 1. $\square$

**Lemma 2 (first fit property).** If item $x$ is in $B_t$ and $e < t$, then $s_x > 1 - \ell(B_e)$.

*Proof.* $B_e$ was open when $x$ came, first fit did not choose it, and loads only grow. $\square$

**Theorem 1.** $\mathrm{FFD} \le \frac32\,\mathrm{OPT}$ for every list.

*Proof.* Let $j = \lceil 2k/3 \rceil$. It is enough to show $\mathrm{OPT} \ge j$, because then $\mathrm{OPT} \ge \frac{2k}{3}$. If $j = 1$ this is clear, so let $j \ge 2$.

*Case 1: $B_j$ has an item larger than $\frac12$.* Call it $x$. If $B_j$ had an item before $x$, that item would be at least $s_x$ by the order, and the two items would have total more than 1. So $x$ is the first item of $B_j$. The first items of $B_1, \ldots, B_{j-1}$ came before $x$, so they are also larger than $\frac12$. So there are $j$ items larger than $\frac12$, no two of them fit into one bin, and $\mathrm{OPT} \ge j$.

*Case 2: each item of $B_j$ is at most $\frac12$.* The first item of $B_j$ is at most $\frac12$, and each item of $B_j, \ldots, B_k$ comes after it in the sorted order, so each of these items is at most $\frac12$. Each bin $B_t$ with $j \le t < k$ has at least two items: if $B_t$ had one item, its load would be at most $\frac12$, and the first item of $B_{t+1}$, of size at most $\frac12$, would have fit into $B_t$, which contradicts Lemma 2. So the bins $B_j, \ldots, B_k$ hold at least $2(k - j) + 1$ items. From $j \le \frac{2k + 2}{3}$ we get $2k \ge 3j - 2$, and so

$$2(k - j) + 1 \ge (3j - 2) - 2j + 1 = j - 1.$$

Choose $j - 1$ distinct items $x_1, \ldots, x_{j-1}$ from the bins $B_j, \ldots, B_k$. By Lemma 2, $\ell(B_e) + s_{x_e} > 1$ for each $e \le j - 1$. These sums use disjoint items, so $S > j - 1$, and the size bound gives $\mathrm{OPT} \ge \lceil S \rceil \ge j$. $\blacksquare$

**Tightness of Theorem 1.** With capacity 8, the sizes $(4, 3, 3, 2, 2, 2)$ fit into two bins $\{4, 2, 2\}$ and $\{3, 3, 2\}$. First fit decreasing packs $[4\ 3]$, $[3\ 2\ 2]$, $[2]$ and uses 3 bins, which is $\frac32\,\mathrm{OPT}$. Since no polynomial-time algorithm has absolute ratio less than $\frac32$ unless P = NP (see [the hardness theorem](/bin-packing-np-hardness/)), first fit decreasing has the best absolute ratio that a polynomial-time algorithm can have, unless P = NP.

**Theorem 2 (sketch).** $\mathrm{FFD} \le \frac{11}{9}\,\mathrm{OPT} + \frac69$ for every list, and this is tight.

*Sketch.* The proof of Dósa, Li, Han and Tuza (2013) is a minimal counterexample argument. Take a list with the least number of items that breaks the bound.

1. *The last item opens the last bin.* Remove the items that come after the first item of $B_k$. The packing of the earlier items does not change, so first fit decreasing still uses $k$ bins, and $\mathrm{OPT}$ does not grow. So in a minimal counterexample the smallest item, of size $s_n$, is alone in $B_k$, and by Lemma 2 each earlier bin has load more than $1 - s_n$.
2. *Small last items are easy.* If $s_n \le \frac16$, then $S > \frac56(k - 1)$, so $k < \frac65\,\mathrm{OPT} + 1$, which is below $\frac{11}{9}\mathrm{OPT} + \frac69$ once $\mathrm{OPT}$ is large. So the main case has all items larger than a constant fraction of the bin, and each bin holds only a few items.
3. *Weights.* Each item gets a weight that depends on its size relative to $s_n$. The weights are chosen so that each optimal bin has weight at most $\frac{11}{9}$, while the bins of first fit decreasing have total weight at least $k - \frac69$. The case analysis over the possible contents of the bins of first fit decreasing is long, and it is the bulk of the paper.

Johnson (1973) first proved $\frac{11}{9}\mathrm{OPT} + 4$. Dósa (2007) announced the constant $\frac69$, and the full proof is in the 2013 paper.

**Tight lists.** Let $\varepsilon = \frac1{100}$ and use four sizes: $a = \frac12 + \varepsilon$, $b = \frac14 + 2\varepsilon$, $c = \frac14 + \varepsilon$, $d = \frac14 - 2\varepsilon$.

*Asymptotic ratio $\frac{11}{9}$.* Take $6m$ items each of $a$, $b$, $c$ and $12m$ items of $d$. The sorted order is $a, b, c, d$. First fit decreasing gives each $a$ its own bin and adds one $b$ to each (load $\frac34 + 3\varepsilon$; a second $b$ does not fit). No $c$ fits into these bins, so the $c$ items go three to a bin, in $2m$ bins (load $\frac34 + 3\varepsilon$). No $d$ fits into any of these bins, since $\frac34 + 3\varepsilon + d > 1$, so the $d$ items go four to a bin, in $3m$ bins. That is $11m$ bins. The bins $\{a, c, d\}$, with load exactly 1, and $\{b, b, d, d\}$, with load exactly 1, give $6m + 3m = 9m$ bins, and $S = 9m$, so $\mathrm{OPT} = 9m$.

*The additive constant.* Take $N = 6m + 4$ items each of $a$, $b$, $c$ and $2N$ items of $d$. As before, the $a$ and $b$ items fill $N$ bins. The $c$ items fill $2m + 1$ bins with three items and one bin with one item. That last bin takes three $d$ items (load $1 - 5\varepsilon$), and the other $12m + 5$ items $d$ go four to a bin into $3m + 2$ bins. So $\mathrm{FFD} = (6m + 4) + (2m + 2) + (3m + 2) = 11m + 8$. The packing with bins $\{a, c, d\}$ and $\{b, b, d, d\}$ uses $N + \frac{N}{2} = 9m + 6$ bins, and $S = 9m + 6$, so $\mathrm{OPT} = 9m + 6$. So $\mathrm{FFD} = \frac{11}{9}\,\mathrm{OPT} + \frac69$ for each $\mathrm{OPT} \equiv 6 \pmod 9$.
