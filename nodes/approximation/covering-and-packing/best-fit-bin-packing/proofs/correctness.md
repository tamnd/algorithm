---
title: Best fit is feasible and uses at most 2 OPT - 1 bins; sketch of the 1.7 bound
proves: [correctness]
status: full
---

We use the pseudocode of the page. The input is a list $s_1, \ldots, s_n$ with $0 < s_i \le 1$, $S = \sum_i s_i$, the bins are $B_1, \ldots, B_k$ in the order in which line L4 opens them, and $\ell(B)$ is the final load of bin $B$. We write $\mathrm{BF} = k$. The proof of the factor 2 is full. The proof of the factor 1.7 is a sketch with a citation.

**Lemma 1 (feasibility).** Best fit returns a partition of the items into bins, and each bin has load at most 1.

*Proof.* Line L3 picks only a bin with $\mathrm{load}[j] + s_i \le 1$, or a new bin with load 0, and $s_i \le 1$. Line L5 puts item $i$ into exactly one bin. So after each pass each load is at most 1. $\square$

**Lemma 2 (new bins).** Let item $x$ be the first item of bin $B_j$, and let $e \ne j$ be a bin that was open when $x$ came. Then $s_x > 1 - \ell(B_e)$.

*Proof.* Line L4 opens a new bin only when no open bin has room, so $s_x$ was more than the free space of $B_e$ at that time. Loads only grow, so that free space is at least $1 - \ell(B_e)$. $\square$

Only the first item of a bin has this property. A later item of $B_j$ may fit into an earlier bin. For example, on the list $(0.3, 0.8, 0.2)$ best fit puts $0.2$ into the bin of $0.8$, although the bin of $0.3$ has free space $0.7$. This is why the proof for [first fit](/first-fit-bin-packing/) does not carry over directly.

**Theorem 1.** If $k \ge 2$, then $S > k/2$. Hence $\mathrm{BF} \le 2\lceil S \rceil - 1 \le 2\,\mathrm{OPT} - 1$ for $n \ge 1$.

*Proof.* Suppose two bins $B_e$, $B_j$ with $e < j$ have load at most $\frac12$. The first item $x$ of $B_j$ has $s_x \le \ell(B_j) \le \frac12$, and $B_e$ was open when $x$ came, so Lemma 2 gives $s_x > 1 - \ell(B_e) \ge \frac12$, a contradiction. So at most one bin has load at most $\frac12$.

If no bin has load at most $\frac12$, then $S > k/2$. Otherwise let $B_e$ be the bin with load at most $\frac12$ and let $B_j$ be any other bin. If $e < j$, apply Lemma 2 to the first item of $B_j$ and to $B_e$: $\ell(B_j) > 1 - \ell(B_e)$. If $j < e$, apply Lemma 2 to the first item of $B_e$ and to $B_j$: $\ell(B_e) > 1 - \ell(B_j)$. In both cases $\ell(B_e) + \ell(B_j) > 1$. The other $k - 2$ bins hold more than $\frac12$ each, so $S > 1 + \frac{k-2}{2} = \frac{k}{2}$.

So $k < 2S \le 2 \lceil S \rceil$, and $k \le 2\lceil S\rceil - 1$. For $k = 1$ the bound holds because $\lceil S \rceil \ge 1$. The size bound $\lceil S \rceil \le \mathrm{OPT}$ ends the proof. $\square$

This proof uses only the rule "open a new bin only if no open bin has room". So the bound holds for each *any fit* algorithm, which includes first fit, best fit and worst fit.

**Theorem 2 (sketch).** $\mathrm{BF} \le \lfloor 1.7\,\mathrm{OPT} \rfloor$ for every list.

*Sketch.* The proof of Dósa and Sgall (ICALP 2014) uses the weight function of the first fit proof, $w(a) = \frac65 a + v(a)$, with the bonus $v(a)$ equal to 0 up to $\frac16$, to $\frac35(a - \frac16)$ on $(\frac16, \frac13]$, to $\frac1{10}$ on $(\frac13, \frac12]$ and to $\frac25$ above $\frac12$.

1. Each set of total size at most 1 has weight at most $\frac{17}{10}$, with the same proof as for first fit. So the total weight is at most $1.7\,\mathrm{OPT}$.
2. Each bin with an item larger than $\frac12$, or with load at least $\frac56$, or with two items larger than $\frac13$ has weight at least 1, with the same proof as for first fit.
3. The rest is different. For first fit, each item of a later bin is larger than the free space of each earlier bin, and the deficits of the light bins telescope. For best fit this property holds only for the first item of each bin (Lemma 2). Dósa and Sgall replace it by an argument that uses the best fit rule itself: an item goes into the fullest bin with room. With this, they show that the total weight is at least the number of bins minus a correction, and the correction is small enough to give $\lfloor 1.7\,\mathrm{OPT} \rfloor$.

The details are in the cited paper. An earlier, shorter argument of Johnson, Demers, Ullman, Garey and Graham (1974) gives the asymptotic bound $1.7\,\mathrm{OPT} + O(1)$ for best fit.

**A family with ratio 5/3.** On $6m$ items of size $\frac17 + \varepsilon$, then $6m$ of size $\frac13 + \varepsilon$, then $6m$ of size $\frac12 + \varepsilon$, best fit uses $m + 3m + 6m = 10m$ bins: the bins of the first kind have free space $\frac17 - 6\varepsilon$, too small for any later item, and the bins of the second kind have free space $\frac13 - 2\varepsilon$, too small for the items of the third kind. One item of each kind per bin gives $6m$ bins, and the $6m$ items larger than $\frac12$ need $6m$ bins, so $\mathrm{OPT} = 6m$ and $\mathrm{BF} = \frac53\,\mathrm{OPT}$.
