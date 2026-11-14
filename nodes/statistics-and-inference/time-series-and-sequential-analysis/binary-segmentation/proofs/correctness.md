---
title: The squared CUSUM contrast is the gain in fit of a cut, and the stack procedure computes the recursive binary segmentation
proves: [correctness]
status: full
---

Notation is that of the page. For $0 \le i < j \le n$, write $\bar x_{i,j}$ for the mean of $x_{i+1}, \ldots, x_j$ and $\mathrm{RSS}(i, j) = \sum_{l=i+1}^{j}(x_l - \bar x_{i,j})^2$, with $\mathrm{RSS}(i, i) = 0$.

**Lemma 1 (the contrast is the gain of a cut).** For $s < b < e$,
$$C(s, b, e)^2 = \mathrm{RSS}(s, e) - \mathrm{RSS}(s, b) - \mathrm{RSS}(b, e).$$

*Proof.* Let $n_1 = b - s$, $n_2 = e - b$, $N = n_1 + n_2$, $a = \bar x_{s,b}$, $c = \bar x_{b,e}$ and $\mu = \bar x_{s,e} = (n_1 a + n_2 c)/N$. For any numbers $y_1, \ldots, y_k$ with mean $\bar y$ and any $\mu$, $\sum(y_l - \mu)^2 = \sum(y_l - \bar y)^2 + k(\bar y - \mu)^2$, because the cross term $2(\bar y - \mu)\sum(y_l - \bar y)$ is 0. Apply this to the two parts and add:
$$\mathrm{RSS}(s, e) = \mathrm{RSS}(s, b) + \mathrm{RSS}(b, e) + n_1(a - \mu)^2 + n_2(c - \mu)^2.$$
Now $a - \mu = n_2(a - c)/N$ and $c - \mu = -n_1(a - c)/N$, so
$$n_1(a - \mu)^2 + n_2(c - \mu)^2 = \frac{n_1 n_2^2 + n_2 n_1^2}{N^2}(a - c)^2 = \frac{n_1 n_2}{N}(a - c)^2 = C(s, b, e)^2. \quad\square$$

**Corollary.** Line L4 returns a cut $b$ that minimizes $\mathrm{RSS}(s, b) + \mathrm{RSS}(b, e)$ over $s < b < e$, that is, the least squares fit of a model with one change in the segment. The contrast is nonnegative, so maximizing $C$ and maximizing $C^2$ give the same $b$.

**Lemma 2 (prefix sums).** With $P_0 = 0$ and $P_j = x_1 + \cdots + x_j$, $\bar x_{i,j} = (P_j - P_i)/(j - i)$. So each contrast costs $O(1)$ after $O(n)$ preprocessing, and line L4 costs $O(e - s)$.

*Proof.* $P_j - P_i = x_{i+1} + \cdots + x_j$. $\square$

**The recursive definition.** For $0 \le s < e \le n$ let $\beta(s, e)$ be the smallest maximizer of $C(s, \cdot, e)$ over $s < b < e$, and define
$$\mathrm{BS}(s, e) = \begin{cases}\emptyset & \text{if } e - s < 2 \text{ or } C(s, \beta(s, e), e) \le \zeta,\\ \{\beta(s, e)\} \cup \mathrm{BS}(s, \beta(s, e)) \cup \mathrm{BS}(\beta(s, e), e) & \text{otherwise.}\end{cases}$$
The definition is well founded, because both segments on the right are strictly shorter than $(s, e)$.

**Theorem.** The procedure stops after at most $2n - 1$ pops and returns $\mathrm{BS}(0, n)$ in increasing order.

*Proof.* Consider the multiset $\mathcal S$ of segments on the stack together with the set CP. We claim that the following holds before each test of line L2:
$$\mathrm{BS}(0, n) = CP \;\cup \bigcup_{(s, e) \in \mathcal S}\mathrm{BS}(s, e),$$
and that the sets on the right are pairwise disjoint. Also the segments in $\mathcal S$ are pairwise disjoint, they lie in $(0, n]$, and no element of CP lies strictly inside one of them.

Line L1 makes the claim true with $\mathcal S = \{(0, n)\}$ and $CP = \emptyset$. Suppose it holds and the loop pops $(s, e)$. If $e - s < 2$, or if $c \le \zeta$ at line L5, then $\mathrm{BS}(s, e) = \emptyset$ by definition and line L4 computed $b = \beta(s, e)$, so removing $(s, e)$ keeps the identity. Otherwise line L6 adds $b = \beta(s, e)$ to CP and pushes $(s, b)$ and $(b, e)$, which replaces $\mathrm{BS}(s, e)$ by $\{b\} \cup \mathrm{BS}(s, b) \cup \mathrm{BS}(b, e)$, which is the same set. The point $b$ lies strictly inside $(s, e)$, while $\mathrm{BS}(s, b)$ lies strictly inside $(s, b)$ and $\mathrm{BS}(b, e)$ strictly inside $(b, e)$, so disjointness is kept. The two new segments are disjoint and lie in the old one, so the segment facts are kept.

Termination: each split adds a new point of $\{1, \ldots, n-1\}$ to CP, and by disjointness no point is added twice, so there are at most $n - 1$ splits. Every pop either splits or not, and every segment except $(0, n)$ is pushed by a split, so the number of pops is at most $1 + 2(n - 1) = 2n - 1$. When the stack is empty the claim gives $CP = \mathrm{BS}(0, n)$, and line L7 sorts it. $\blacksquare$

**Running time.** The pops form a binary tree rooted at $(0, n)$ in which the children of a split segment are its two parts. The segments at one depth are disjoint, so by Lemma 2 the work at one depth is $O(n)$. A path from the root passes through split nodes only, except at its last node, so the depth is at most $m + 1$ when $m$ change points are found, and the total time is $O(n(m + 1))$.
