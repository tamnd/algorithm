---
title: Union by rank with path compression runs in O(m alpha(n)) time
proves: [statement]
status: full
---

This is the potential proof of CLRS, Section 19.4. We prove the bound $O(m\,\alpha(n))$ for $m$ operations of which $n$ are MAKE-SET. Tarjan's sharper bound $O(m\,\alpha(m, n))$ needs a finer argument, which is in his 1975 paper and in Tarjan and van Leeuwen (1984).

**Setup.** The operations are MAKE-SET, FIND and UNION on a [disjoint-set forest](/disjoint-set-forest/) with [union by rank](/union-by-rank/) and [path compression](/path-compression/). A UNION is two FINDs and one LINK of two different roots (or nothing, when the roots are equal). So a sequence of $m$ operations becomes a sequence of at most $3m$ operations MAKE-SET, FIND and LINK, and it is enough to prove the bound for these. MAKE-SET and LINK take $O(1)$ time, and a FIND on a path of $s$ nodes takes $O(s)$ time. Let $c$ be a constant such that these costs are at most $c$, $c$ and $cs$.

The number $n$ is the number of MAKE-SET operations in the whole sequence, and $\alpha(n)$ is fixed for the proof. The functions $A_k$ and $\alpha$ are those of the [inverse Ackermann function](/inverse-ackermann-function/) page: $A_0(j) = j + 1$, $A_k(j) = A_{k-1}^{(j+1)}(j)$, and $\alpha(n) = \min\{k : A_k(1) \ge n\}$. We use that $A_k(j) > j$, that $A_k$ is increasing in $j$, and that $A_{k+1}(j) > A_k(j)$.

**Rank facts.** From the [union by rank](/union-by-rank/) page: (i) $x.rank < x.p.rank$ for each non-root $x$; (ii) the rank of a node changes only while it is a root, and never falls; (iii) each rank is at most $\lfloor \lg n \rfloor \le n - 1$. We also need:

(iv) *For each node $x$, the rank of $x.p$ never falls over time.* The parent of $x$ changes in two ways. A LINK makes a root $x$ a child of $y$; from then on $x$ is a non-root. A FIND sets $x.p$ to the root $r$ of the path, and $r.rank \ge$ the old $x.p.rank$ by (i) along the path. Otherwise $x.p$ stays, and its rank does not fall by (ii).

**Level and iterate.** For a non-root $x$ with $x.rank \ge 1$, define

$$\mathrm{level}(x) = \max\{k \ge 0 : x.p.rank \ge A_k(x.rank)\}, \qquad \mathrm{iter}(x) = \max\{i \ge 1 : x.p.rank \ge A_{\mathrm{level}(x)}^{(i)}(x.rank)\}.$$

*Ranges.* $x.p.rank \ge x.rank + 1 = A_0(x.rank)$ by (i), so the set for the level contains 0. Also $A_{\alpha(n)}(x.rank) \ge A_{\alpha(n)}(1) \ge n > x.p.rank$ by (iii), so no $k \ge \alpha(n)$ is in the set, and $0 \le \mathrm{level}(x) < \alpha(n)$. For the iterate, $i = 1$ is in the set by the definition of the level. And $A_{\ell}^{(x.rank + 1)}(x.rank) = A_{\ell + 1}(x.rank) > x.p.rank$ for $\ell = \mathrm{level}(x)$, by the maximality of the level; the iterates of a point under $A_\ell$ increase, so $1 \le \mathrm{iter}(x) \le x.rank$.

**Potential.** After the $q$-th operation, give each node $x$ the potential

$$\phi_q(x) = \begin{cases} \alpha(n) \cdot x.rank & \text{if } x \text{ is a root or } x.rank = 0, \\ (\alpha(n) - \mathrm{level}(x)) \cdot x.rank - \mathrm{iter}(x) & \text{if } x \text{ is a non-root and } x.rank \ge 1, \end{cases}$$

and let $\Phi_q = c \sum_x \phi_q(x)$, over the nodes made so far. A non-root of rank 0 has potential 0. At the start $\Phi_0 = 0$.

**Lemma 1.** $0 \le \phi_q(x) \le \alpha(n) \cdot x.rank$ for each node $x$ and each $q$.

*Proof.* The root case and the rank 0 case are clear. For a non-root with $x.rank \ge 1$: $\mathrm{level}(x) \le \alpha(n) - 1$ and $\mathrm{iter}(x) \le x.rank$ give $\phi_q(x) \ge x.rank - x.rank = 0$. And $\mathrm{level}(x) \ge 0$ and $\mathrm{iter}(x) \ge 1$ give $\phi_q(x) \le \alpha(n) \cdot x.rank - 1$. $\square$

So $\Phi_q \ge 0 = \Phi_0$ for each $q$.

**Lemma 2.** Let $x$ be a non-root before the $q$-th operation, which is a LINK or a FIND. Then $\phi_q(x) \le \phi_{q-1}(x)$. If also $x.rank \ge 1$ and the operation changes $\mathrm{level}(x)$ or $\mathrm{iter}(x)$, then $\phi_q(x) \le \phi_{q-1}(x) - 1$.

*Proof.* The node $x$ stays a non-root, so its rank does not change, by (ii), and $\alpha(n)$ is fixed. If $x.rank = 0$, both potentials are 0. Else, by (iv), $x.p.rank$ does not fall, so $\mathrm{level}(x)$ does not fall. If the level stays the same, $\mathrm{iter}(x)$ does not fall, for the same reason, and if it grows, $\phi(x)$ falls by at least 1. If the level grows by $d \ge 1$, the term $(\alpha(n) - \mathrm{level}(x)) \cdot x.rank$ falls by $d \cdot x.rank \ge x.rank$, while $\mathrm{iter}(x)$ can fall by at most $x.rank - 1$, from at most $x.rank$ to at least 1. So $\phi(x)$ falls by at least 1. $\square$

**Amortized costs.** The amortized cost of operation $q$ is its actual cost plus $\Phi_q - \Phi_{q-1}$.

*MAKE-SET$(x)$.* The new node $x$ has potential 0, and no other node changes. The amortized cost is at most $c$.

*LINK$(x, y)$.* Let $x$ become the child of $y$ (the other case is symmetric). The nodes whose potential can change are $x$, $y$ and the children of $y$. A child of $y$ is a non-root, so by Lemma 2 its potential does not grow. Before the LINK, $x$ was a root with $\phi(x) = \alpha(n) \cdot x.rank$; after it, $\phi(x) \le \alpha(n) \cdot x.rank$ by Lemma 1, because the rank of $x$ does not change. The root $y$ keeps its status, and its rank grows by at most 1, so $\phi(y)$ grows by at most $\alpha(n)$. The amortized cost is at most $c + c\,\alpha(n)$.

*FIND$(x)$.* Let the path be $x = x_1, x_2, \ldots, x_s$, with $x_s$ the root. The actual cost is at most $cs$. Only the parents of $x_1, \ldots, x_{s-2}$ change, to $x_s$, so the nodes off the path keep their parents, their parents keep their ranks, and their potentials do not change. The root keeps its potential. By Lemma 2, no node of the path gains potential. We show that at least $\max(0, s - \alpha(n) - 2)$ nodes of the path lose at least 1.

Call a node $x_j$ with $j < s$ *good* if $x_j.rank \ge 1$ and there is an index $j < t < s$ with $\mathrm{level}(x_t) = \mathrm{level}(x_j)$, both levels taken before the FIND. Let $x_j$ be good, with $k = \mathrm{level}(x_j)$ and $i = \mathrm{iter}(x_j)$, and let $x_t$ be the later node with level $k$. Before the FIND:

$$x_j.p.rank \ge A_k^{(i)}(x_j.rank), \qquad x_t.rank \ge x_j.p.rank, \qquad x_t.p.rank \ge A_k(x_t.rank).$$

The first is the definition of the iterate, the second holds because $x_t$ is $x_{j+1} = x_j.p$ or a later node of the path and ranks increase along the path, and the third is the definition of the level of $x_t$. Since $A_k$ is increasing,

$$x_t.p.rank \ge A_k(x_t.rank) \ge A_k(x_j.p.rank) \ge A_k\big(A_k^{(i)}(x_j.rank)\big) = A_k^{(i+1)}(x_j.rank).$$

After the FIND, $x_j.p = x_s$, and $x_s.rank \ge x_t.p.rank$, because $x_t.p$ is $x_s$ or a node before it on the path. So after the FIND, $x_j.p.rank \ge A_k^{(i+1)}(x_j.rank)$. Then either $\mathrm{level}(x_j)$ has grown, or it is still $k$ and $\mathrm{iter}(x_j) \ge i + 1$. By Lemma 2, $\phi(x_j)$ falls by at least 1.

The nodes of the path that are not good are: the root $x_s$; the nodes of rank 0, of which there is at most one, $x_1$, because ranks increase strictly along the path; and, for each level $k$ from 0 to $\alpha(n) - 1$, the last node among $x_1, \ldots, x_{s-1}$ with level $k$, if there is one. That is at most $\alpha(n) + 2$ nodes. So at least $s - \alpha(n) - 2$ nodes are good, and $\Phi$ falls by at least $c\,(s - \alpha(n) - 2)$ when this is positive. The amortized cost is at most $cs - c\,(s - \alpha(n) - 2) = c\,(\alpha(n) + 2)$, and if $s \le \alpha(n) + 2$ it is at most $cs \le c\,(\alpha(n) + 2)$.

**Theorem.** A sequence of $m$ operations MAKE-SET, UNION and FIND, of which $n$ are MAKE-SET, on a disjoint-set forest with union by rank and path compression takes $O(m\,\alpha(n))$ time.

*Proof.* The sequence becomes at most $3m$ operations MAKE-SET, LINK and FIND, each of amortized cost at most $c\,(\alpha(n) + 2)$. The sum of the actual costs is the sum of the amortized costs minus $\Phi_{\text{end}} - \Phi_0$, and $\Phi_{\text{end}} \ge 0 = \Phi_0$ by Lemma 1. So the total time is at most $3m \cdot c\,(\alpha(n) + 2) = O(m\,\alpha(n))$. $\blacksquare$
