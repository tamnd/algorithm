---
title: The matching gives the largest one-to-one count, and properties of boundary precision and recall
proves: [correctness]
status: full
---

We use the notation of the page. $B$ is the set of machine boundary pixels and $G$ the set of human boundary pixels, both finite sets of integer points. For a tolerance $d \ge 0$ the graph $\Gamma_d$ has the left vertices $B$, the right vertices $G$, and an edge $(b, g)$ when $\lVert b - g \rVert \le d$ in the Euclidean norm. A matching is a set of edges with no shared end. The procedure BOUNDARY-F builds the edges in line L1, finds a matching $M$ in line L2 and returns $P = |M|/|B|$, $R = |M|/|G|$ and $F = 2PR/(P + R)$ in lines L3 and L4.

**Lemma 1 (the edges).** Line L1 lists exactly the edges of $\Gamma_d$.

*Proof.* If $\lVert (\Delta u, \Delta v) \rVert \le d$ for integers $\Delta u$ and $\Delta v$, then $|\Delta u| \le d$, so $|\Delta u| \le \lfloor d \rfloor$, and the same for $\Delta v$. So the scan of the offsets in $[-\lfloor d \rfloor, \lfloor d \rfloor]^2$ meets every edge, and the test $\Delta u^2 + \Delta v^2 \le d^2$ keeps exactly the edges. $\square$

**Lemma 2 (the matching is maximum).** After line L2, $M$ is a maximum matching of $\Gamma_d$.

*Proof.* Number the machine pixels $b_1, \ldots, b_n$ in the order of the loop, and let $\Gamma^{(k)}$ be the subgraph with left vertices $b_1, \ldots, b_k$ and all of $G$. We show by induction on $k$ that after the search from $b_k$, the matching $M$ is a maximum matching of $\Gamma^{(k)}$. For $k = 0$ the empty matching is maximum.

Step $k$. Let $M$ be maximum in $\Gamma^{(k-1)}$. One more vertex raises the size of a maximum matching by at most 1, so the maximum in $\Gamma^{(k)}$ is $|M|$ or $|M| + 1$. By Berge's theorem, it is $|M| + 1$ exactly when $\Gamma^{(k)}$ has an augmenting path for $M$: a path that alternates between edges outside and inside $M$ and joins a free left vertex to a free right vertex. Such a path has one left end and one right end. If it does not contain $b_k$, it lies in $\Gamma^{(k-1)}$, which is impossible since $M$ is maximum there. If it contains $b_k$, then $b_k$ is free and has degree at most 1 on the path, so $b_k$ is its left end.

The search from $b_k$ is a depth-first search in the directed graph that goes from a left vertex to a right vertex along an edge outside $M$, and from a matched right vertex to its partner along $M$. It marks each right vertex at most once, and it stops when it reaches a free right vertex. A depth-first search reaches every vertex that is reachable from its start, so it finds a free right vertex if and only if one is reachable from $b_k$, that is, if and only if an augmenting path from $b_k$ exists. A reachable vertex is reached along a simple path, and the search flips the edges of that path, which raises $|M|$ by 1 and keeps a matching. So after step $k$, $M$ is maximum in $\Gamma^{(k)}$. $\square$

**Theorem 1 (the scores).** Let $\nu = |M|$ be the size of a maximum matching of $\Gamma_d$, with $B$ and $G$ not empty.

1. $0 \le P \le 1$ and $0 \le R \le 1$, and $\nu$ does not depend on which maximum matching is found.
2. No assignment of machine pixels to distinct human pixels within distance $d$ has more than $\nu$ correct pixels. So $P$ and $R$ are the largest values that any one-to-one rule within the tolerance can give.
3. $F = 1$ if and only if $|B| = |G| = \nu$, that is, if $\Gamma_d$ has a perfect matching.
4. Swapping $B$ and $G$ swaps $P$ and $R$ and keeps $F$.
5. If $d \le d'$, then the $P$ and $R$ for $d'$ are at least those for $d$.

*Proof.* (1) $\nu \le \min(|B|, |G|)$. All maximum matchings have the same size. (2) Such an assignment is a matching of $\Gamma_d$. (3) $F$ is the harmonic mean of $P$ and $R$, which is 1 exactly when both are 1. (4) The graph is the same with the sides swapped. (5) $\Gamma_d$ is a subgraph of $\Gamma_{d'}$, so a matching of the first is a matching of the second. $\square$

The value of $F$ is not the score of a nearest-neighbor rule. If each machine pixel is called correct when some human pixel is within $d$, without the one-to-one rule, then a double line of machine pixels on both sides of a human line gets the precision 1. With the matching it gets $1/2$, as in the example of the page.

**Several humans.** BSDS-COUNTS takes human maps $G_1, \ldots, G_H$. For each one it finds a maximum matching $M_h$ in line L7. The precision is $|A| / |B|$ with $A$ the set of machine pixels matched in at least one $M_h$, and the recall is $\sum_h |M_h| / \sum_h |G_h|$.

**Proposition 2.** With several humans, $0 \le P, R \le 1$. The recall does not depend on the choice of the maximum matchings, but the precision can.

*Proof.* $A \subseteq B$ and $|M_h| \le |G_h|$ give the range. Each $|M_h|$ is the same for all maximum matchings. For the second claim, let $B = \{(0, 0), (2, 0)\}$, $G_1 = \{(1, 0)\}$ and $G_2 = \{(2, 0)\}$ with $d = 1$. The graph for $G_2$ has the edge from $(2, 0)$ only. For $G_1$, both machine pixels are at distance 1, and either one can be matched. If $(2, 0)$ is chosen for $G_1$, then $A = \{(2, 0)\}$ and $P = 1/2$; if $(0, 0)$ is chosen, then $A = B$ and $P = 1$. $\square$

A program must fix the rule that picks the matching. The rule of this page is the order of the loop of line L2. The reference BSDS code computes the matching in another way, and its precision can differ in such ties.

**Thresholds.** For a soft boundary map $s$ and a threshold $t$, let $B_t = \{x : s(x) \ge t\}$. ODS sums the four counts of every image at a common $t$ and takes the $t$ with the largest $F$ of the sums. OIS takes for each image the $t$ with the largest $F$ of that image and sums the counts at those thresholds.

**Proposition 3.** On a data set of one image, ODS equals OIS. On larger data sets OIS can be above ODS or below it.

*Proof.* With one image both choose the threshold that maximizes the $F$ of that image. With one human map per image the counts are $(c, b, c, g)$, where $c$ is the size of the matching, $b = |B_t|$ and $g = |G|$, and then $F = 2c/(b + g)$.

The example of the page has OIS 1 above ODS $4/5$. For the other direction take $d = 0.5$, so only equal pixels match, the thresholds 0.3, 0.6 and 0.9, and two images of one row of 6 pixels. Image 1 has $s = (0, 0.9, 0.3, 0.9, 0.6, 0.3)$ and human pixels at positions 0, 2 and 4. Image 2 has $s = (0.9, 0, 0.6, 0.9, 0.6, 0.3)$ and human pixels at positions 0, 3 and 5. The pairs $(c, b)$ at the three thresholds are $(2, 5)$, $(1, 3)$ and $(0, 2)$ for image 1, and $(3, 5)$, $(2, 4)$ and $(2, 2)$ for image 2, with $g = 3$ for both. The values of $F$ are $1/2$, $1/3$, $0$ for image 1 and $3/4$, $4/7$, $4/5$ for image 2, so OIS picks 0.3 for image 1 and 0.9 for image 2, each the unique best. The sums are $c = 4$, $b = 7$, $g = 6$, so OIS is $8/13$. At the common threshold 0.3 the sums are $c = 5$, $b = 10$, $g = 6$, with $F = 10/16 = 5/8 > 8/13$. So ODS is at least $5/8$, above OIS. $\square$

That OIS is above ODS on BSDS for the methods in the literature is a benchmark result, not a theorem.

**Cost.** Each machine pixel has at most $(2 \lfloor d \rfloor + 1)^2$ candidate neighbors, so line L1 takes $O(|B| d^2)$ time with a hash set of $G$. Each search of line L2 takes $O(|B| + |G| + E)$ time with $E = O(|B| d^2)$ edges, so line L2 takes $O(|B| (|B| + |G| + E))$ in the worst case. The [Hopcroft-Karp algorithm](/hopcroft-karp/) reduces this to $O(E \sqrt{|B| + |G|})$.
