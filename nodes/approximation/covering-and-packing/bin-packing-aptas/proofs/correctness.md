---
title: The asymptotic scheme uses at most (1 + eps) OPT + 1 bins
proves: [correctness]
status: full
---

We use the pseudocode of the page with $0 < \varepsilon \le 1$ and $\delta = \varepsilon / 2 \le \frac12$. The input $I$ has sizes in $(0, 1]$. The large items are the items with size at least $\delta$; there are $n'$ of them, and they form the list $I_L$. The small items have size less than $\delta$. We write $\mathrm{OPT}(X)$ for the least number of bins for a list $X$, and $\mathrm{OPT} = \mathrm{OPT}(I)$.

For two lists $X$ and $Y$, we say $X$ *is dominated by* $Y$ if there is an injective map $\phi$ from the items of $X$ to the items of $Y$ with $s_x \le s_{\phi(x)}$ for each $x$. If $X$ is dominated by $Y$, then $\mathrm{OPT}(X) \le \mathrm{OPT}(Y)$: take an optimal packing of $Y$, put each $x$ where $\phi(x)$ is, and drop the items of $Y$ that are not images. No load grows.

**Lemma 1 (the large items alone).** Lines L1 to L5 return a packing of $I_L$ with at most $(1 + \delta)\,\mathrm{OPT}(I_L)$ bins.

*Proof.* If $K = \lfloor \delta^2 n' \rfloor = 0$, line L2 packs $I_L$ optimally, and the claim holds. Let $K \ge 1$. Line L3 sorts $I_L$ by decreasing size and cuts it into groups $G_1, G_2, \ldots, G_g$ of $K$ consecutive items each, except that $G_g$ may have fewer. Line L4 rounds each item of $G_h$, $h \ge 2$, up to the largest size in $G_h$, and $J$ is the list of rounded items.

*$J$ is dominated by $I_L$.* Map the $t$-th item of $G_h$ to the $t$-th item of $G_{h-1}$, for $h \ge 2$. This is injective because $|G_h| \le K = |G_{h-1}|$. The rounded size of an item of $G_h$ is the largest size in $G_h$, which is at most the smallest size in $G_{h-1}$, because the list is sorted. So $\mathrm{OPT}(J) \le \mathrm{OPT}(I_L)$.

*The packing.* Line L5 takes an optimal packing of $J$, puts each original item where its rounded copy is, which does not make any load larger, and adds one bin for each of the $K$ items of $G_1$. This packs all of $I_L$ in $\mathrm{OPT}(J) + K$ bins.

*The cost of $G_1$.* Each large item has size at least $\delta$, so $\delta n' \le S(I_L) \le \mathrm{OPT}(I_L)$, and $K \le \delta^2 n' \le \delta\,\mathrm{OPT}(I_L)$.

So the packing has at most $\mathrm{OPT}(I_L) + \delta\,\mathrm{OPT}(I_L)$ bins. $\square$

**Lemma 2 (adding the small items).** Let $P$ be a packing of $I_L$ in $p$ bins. Line L6 extends it to a packing of $I$ with at most $\max\bigl(p,\ \frac{S}{1 - \delta} + 1\bigr)$ bins, where $S$ is the total size of $I$.

*Proof.* Line L6 is first fit on the small items, started with the bins of $P$, so the packing stays feasible. If line L6 opens no new bin, the count is $p$. Otherwise consider the moment the last new bin opens. Its item has size less than $\delta$ and fits into no earlier bin, so each other bin has load more than $1 - \delta$ at that moment, and loads only grow. So with $q$ bins at the end, $S > (q - 1)(1 - \delta)$, that is, $q < \frac{S}{1-\delta} + 1$. $\square$

**Theorem.** The scheme returns a packing of $I$ with at most $(1 + \varepsilon)\,\mathrm{OPT} + 1$ bins.

*Proof.* Feasibility follows from Lemma 1 and Lemma 2. By Lemma 1, $p \le (1 + \delta)\,\mathrm{OPT}(I_L) \le (1 + \delta)\,\mathrm{OPT}$, because $I_L$ is a sub-list of $I$. Since $0 < \delta \le \frac12$, we have $\frac{1}{1 - \delta} \le 1 + 2\delta$, because $(1 - \delta)(1 + 2\delta) = 1 + \delta(1 - 2\delta) \ge 1$. So $\frac{S}{1-\delta} + 1 \le (1 + 2\delta) S + 1 \le (1 + 2\delta)\,\mathrm{OPT} + 1$. By Lemma 2, the number of bins is at most

$$\max\bigl((1+\delta)\,\mathrm{OPT},\ (1 + 2\delta)\,\mathrm{OPT} + 1\bigr) = (1 + 2\delta)\,\mathrm{OPT} + 1 = (1 + \varepsilon)\,\mathrm{OPT} + 1. \qquad \blacksquare$$

**Lemma 3 (running time).** For a fixed $\varepsilon$, the scheme runs in time polynomial in $n$.

*Proof.* Each bin holds at most $\lfloor 1/\delta \rfloor$ large items. If $K = 0$, then $n' < 1/\delta^2$, a constant, and the exact packing in line L2 takes constant time. If $K \ge 1$, then $K \ge \delta^2 n' / 2$ (because $\lfloor x \rfloor \ge x/2$ for $x \ge 1$), so $J$ has at most $g - 1 \le n'/K \le 2/\delta^2$ distinct sizes. Call this number $d$. A bin of $J$ is a *configuration*: a vector of $d$ counts with total size at most 1 and at most $1/\delta$ items, so there are at most $(1/\delta + 1)^d$ configurations, a constant. The dynamic program over the vectors of remaining counts has at most $(n + 1)^d$ states and tries each configuration in each state, so it takes $O\bigl((n+1)^d (1/\delta + 1)^d\bigr)$ steps, which is $n^{O(1/\varepsilon^2)}$. Sorting, grouping and first fit take $O(n^2)$ steps or less. $\square$

The exponent of $n$ grows with $1/\varepsilon$, so this is an asymptotic polynomial-time approximation scheme, and not an asymptotic fully polynomial one. Replacing the exact dynamic program by the configuration LP and rounding its basic solution gives a running time that is polynomial in $n$ and $1/\varepsilon$, at the cost of a larger additive term; see [Karmarkar and Karp](/karmarkar-karp-bin-packing/).
