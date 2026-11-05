---
title: Recursive contraction finds a minimum cut with probability Ω(1/log n) in O(n^2 log n) time
proves: [correctness, termination, complexity]
status: full
---

**Setting.** $G$ is an undirected graph on $n \ge 2$ vertices with weights $w \ge 0$, parallel edges summed, no self-loops. $\lambda$ is the weight of a minimum cut. A contracted graph $H$ has vertices that are disjoint groups of original vertices covering $V$, and $w_H(X, Y) = w(X, Y)$ for groups $X \ne Y$. A cut of $H$ is a union of groups, so it is a cut of $G$ with the same weight; hence $\lambda(H) \ge \lambda$. A cut $C$ of $G$ *survives* in $H$ if every group lies inside $C$ or inside $V \setminus C$; then $C$ is a cut of $H$.

**Lemma 1 (soundness).** Every pair $(k, S)$ returned is a cut of $G$ with weight exactly $k$; so the result is never below $\lambda$.

*Proof.* Line L6 returns a cut of the current graph with its weight, and a zero-weight return after $W = 0$ is a single group with no edge leaving it. Both are cuts of $G$ of the same weight. Lines L9 and L3 only choose among such pairs. $\square$

**Lemma 2 (one contraction).** If $H$ has $k \ge 3$ vertices, $W > 0$, and a minimum cut $C$ of $G$ survives in $H$, then one contraction of line L11 destroys $C$ with probability at most $2/k$.

*Proof.* The weighted degree of each vertex $X$ of $H$ is the weight of the cut $X$ of $G$, so it is at least $\lambda$. So $2W \ge k\lambda$. The edges of $H$ that cross $C$ have total weight $\lambda$, since $C$ survives, and the contraction picks one of them with probability $\lambda / W \le 2/k$. Contracting any other edge keeps every group on one side. $\square$

**Lemma 3 (contracting to $t$).** If $C$ survives in $H$ with $k$ vertices and $t \ge 2$, then CONTRACT$(H, t)$ keeps $C$ with probability at least $t(t-1) / (k(k-1))$. For $k \ge 7$ and $t = \lceil 1 + k/\sqrt2 \rceil$ this is at least $\frac12$, and $t < k$.

*Proof.* If $W = 0$ the call stops and $C$ survives. Otherwise, by Lemma 2 applied for $j = k, k - 1, \ldots, t + 1$ vertices, $C$ survives with probability at least $\prod_{j=t+1}^{k} (1 - 2/j) = \prod_{j=t+1}^{k} \frac{j - 2}{j} = \frac{t(t-1)}{k(k-1)}$. For the given $t$, $t - 1 \ge k/\sqrt2$ and $t \ge k/\sqrt2 + 1$, so $t(t-1) \ge k^2/2 + k/\sqrt2 \ge k(k-1)/2$. And $t < k$ for $k \ge 7$, since $1 + k/\sqrt2 \le k - 1$ when $k \ge 2/(1 - 1/\sqrt2) \approx 6.83$. $\square$

**Termination and depth.** By Lemma 3 each recursive call has fewer vertices than its parent, so the recursion ends. CONTRACT stops at exactly $t$ vertices unless it returns early, so a call at depth $j$ has at most $n_j$ vertices, where $n_0 = n$ and $n_{j+1} = \lceil 1 + n_j/\sqrt2 \rceil \le n_j/\sqrt2 + 2$. Let $c = 2/(1 - 1/\sqrt2) \approx 6.83$, so that $c = c/\sqrt2 + 2$. Then $n_{j+1} - c \le (n_j - c)/\sqrt2$, and so $n_j \le c + n/2^{j/2}$. A call at depth $j$ that recurses has at least 7 vertices, so $7 \le c + n/2^{j/2}$, which gives $2^{j} \le n^2/(7 - c)^2 \le 34\,n^2$. So the depth $D(n)$, the largest depth of a call, satisfies $2^{D(n)} \le 68\,n^2$ and $D(n) \le 2\log_2 n + 7 = O(\log n)$.

**Lemma 4 (success).** Let $p_D$ be the least probability, over all contracted graphs $H$ of recursion depth at most $D$ in which some minimum cut of $G$ survives, that RECURSIVE-CONTRACT$(H)$ returns a pair with $k = \lambda$. Then $p_D \ge 2/(D + 2)$.

*Proof.* By induction on $D$. For $D = 0$, line L6 finds a minimum cut of $H$, whose weight is $\lambda$ since $\lambda \le \lambda(H) \le w(C) = \lambda$; so $p_0 = 1$. Let $D \ge 1$, and let $C$ survive in $H$. Branch $i$ of line L8 succeeds if $C$ survives in $G_i$, with probability at least $\frac12$ by Lemma 3, and then, conditioned on any such $G_i$, the recursive call succeeds with probability at least $p_{D-1}$; if instead the call stopped with $W = 0$, it returns $0 = \lambda$. So a branch succeeds with probability at least $p_{D-1}/2$. The branches use independent random choices, so both fail with probability at most $(1 - p_{D-1}/2)^2$, and

$$p_D \ge 1 - \Bigl(1 - \frac{p_{D-1}}{2}\Bigr)^2 = p_{D-1} - \frac{p_{D-1}^2}{4}.$$

The map $f(p) = p - p^2/4$ is increasing on $[0, 2]$, so with $p_{D-1} \ge 2/(D + 1)$,

$$p_D \ge \frac{2}{D+1} - \frac{1}{(D+1)^2} = \frac{2D + 1}{(D+1)^2} \ge \frac{2}{D+2},$$

where the last step is $(2D + 1)(D + 2) = 2D^2 + 5D + 2 \ge 2D^2 + 4D + 2 = 2(D+1)^2$. $\square$

**Lemma 5 (time).** One run takes $O(n^2 \log n)$ time.

*Proof.* A call on $k$ vertices copies the matrix for each branch and makes at most $k$ contractions in each branch, each in $O(k)$ time, so it does $O(k^2)$ work besides its children; a call with $k \le 6$ does $O(1)$ work. There are at most $2^j$ calls at depth $j$, each with at most $n_j \le c + n/2^{j/2}$ vertices, so the work at depth $j$ is $O(2^j (c^2 + n^2/2^j)) = O(2^j + n^2)$. By the depth bound, $2^j \le 68\,n^2$ for every depth $j$ that occurs, so each depth costs $O(n^2)$, and the $D(n) + 1 = O(\log n)$ depths cost $O(n^2 \log n)$ in total. $\square$

**Theorem.** With $R$ runs, KARGER-STEIN returns $\lambda$ with probability at least $1 - (1 - 2/(D(n) + 2))^R \ge 1 - e^{-2R/(D(n) + 2)}$, and never a value below $\lambda$. With $R = \lceil c (D(n) + 2) \ln n / 2 \rceil = O(\log^2 n)$ the error is at most $n^{-c}$, and the time is $O(n^2 \log^3 n)$.

*Proof.* Soundness is Lemma 1. A minimum cut of $G$ survives in $G$ itself, so by Lemma 4 each run succeeds with probability at least $2/(D(n) + 2)$, independently of the other runs, and $(1 - x)^R \le e^{-xR}$. The time is $R$ times the bound of Lemma 5. $\blacksquare$
