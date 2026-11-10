---
title: The k-th smallest of d uniform values has a Beta law, so (k − 1)/v_k is unbiased for d and the intersection estimate is unbiased
proves: [correctness]
status: full
---

Let the stream have the set $D$ of $d$ distinct items, and let their scaled hash values $u(x)$, $x \in D$, be independent and uniform on $(0, 1)$. Then the values are distinct with probability 1. Write $v_1 < v_2 < \cdots < v_d$ for the sorted values.

**Lemma 1 (the state).** After lines L1 to L5, $T$ is the set of the $\min(k, d)$ smallest values of $\{u(x) : x \in D\}$. For two sets $A$ and $B$, the $k$ smallest values of $T_A \cup T_B$ are the $k$ smallest values of $A \cup B$.

*Proof.* By induction on the stream. The claim holds for the empty prefix. Let $T$ be the $\min(k, i)$ smallest values of the $i$ distinct items of a prefix, and let the next item have value $y$. If $y \in T$, the item is a repeat (values are distinct), the set is unchanged, and line L4 skips it. If $|T| = k$ and $y \ge \max(T)$, then $y$ is not among the $k$ smallest, and line L4 skips it. Otherwise $y$ is among the $k$ smallest of the new set, and line L5 inserts it and, if $|T| = k + 1$, removes the largest, which is the $(k+1)$-th smallest. A repeat whose value is not in $T$ was skipped before, and it is skipped again for the same reason.

For the merge, let $w$ be one of the $k$ smallest values of $A \cup B$, say $w = u(x)$ with $x \in A$. Fewer than $k$ values of $A$ are smaller than $w$, so $w \in T_A$. So the $k$ smallest of $A \cup B$ all lie in $T_A \cup T_B \subseteq \{u(x) : x \in A \cup B\}$, and they are the $k$ smallest of $T_A \cup T_B$. $\square$

**Lemma 2 (the law of $v_k$).** For $1 \le k \le d$, $v_k$ has density
$$f(v) = \frac{d!}{(k-1)!\,(d-k)!}\,v^{k-1}(1-v)^{d-k}, \qquad 0 < v < 1,$$
the Beta$(k, d-k+1)$ density.

*Proof.* $v_k \le v$ exactly when at least $k$ of the $d$ values are at most $v$. The number of such values is binomial with parameters $d$ and $v$, so
$$\Pr[v_k \le v] = \sum_{j=k}^{d}\binom{d}{j}v^j(1-v)^{d-j}.$$
Differentiate term by term. The term $j$ gives $\binom{d}{j}\big(j v^{j-1}(1-v)^{d-j} - (d-j)v^j(1-v)^{d-j-1}\big)$. With $a_j = \binom{d}{j}j\,v^{j-1}(1-v)^{d-j}$ and $b_j = \binom{d}{j}(d-j)v^j(1-v)^{d-j-1}$, we have $\binom{d}{j}(d-j) = \binom{d}{j+1}(j+1)$, so $b_j = a_{j+1}$, and $b_d = 0$. The sum telescopes to $a_k = \binom{d}{k}k\,v^{k-1}(1-v)^{d-k}$, and $\binom{d}{k}k = d!/((k-1)!(d-k)!)$. $\square$

We use the Beta integral $\int_0^1 v^{a-1}(1-v)^{b-1}\,dv = \frac{(a-1)!\,(b-1)!}{(a+b-1)!}$ for integers $a, b \ge 1$. It holds because Lemma 2 with $d = a + b - 1$ and $k = a$ gives a density, whose integral is 1.

**Theorem 3 (unbiased count).** Let $d \ge k$. For $k \ge 2$, $\mathbb{E}[(k-1)/v_k] = d$. For $k \ge 3$,
$$\mathrm{Var}\Big(\frac{k-1}{v_k}\Big) = \frac{d(d-k+1)}{k-2}.$$

*Proof.* Let $c = d!/((k-1)!(d-k)!)$. For $k \ge 2$,
$$\mathbb{E}\Big[\frac{1}{v_k}\Big] = c\int_0^1 v^{k-2}(1-v)^{d-k}\,dv = c\,\frac{(k-2)!\,(d-k)!}{(d-1)!} = \frac{d!}{(k-1)!\,(d-1)!}\,(k-2)! = \frac{d}{k-1}.$$
So $\mathbb{E}[(k-1)/v_k] = d$. For $k \ge 3$,
$$\mathbb{E}\Big[\frac{1}{v_k^2}\Big] = c\int_0^1 v^{k-3}(1-v)^{d-k}\,dv = c\,\frac{(k-3)!\,(d-k)!}{(d-2)!} = \frac{d(d-1)}{(k-1)(k-2)}.$$
Then
$$\mathrm{Var}\Big(\frac{k-1}{v_k}\Big) = (k-1)^2\Big(\frac{d(d-1)}{(k-1)(k-2)} - \frac{d^2}{(k-1)^2}\Big) = \frac{(k-1)d(d-1) - (k-2)d^2}{k-2} = \frac{d(d-k+1)}{k-2}. \qquad \square$$

For $k = 2$ the integral for $\mathbb{E}[1/v_2^2]$ diverges at 0, so the variance is infinite. The same computation gives $\mathbb{E}[k/v_k] = dk/(k-1)$, so $k/v_k$ overestimates $d$ by the factor $k/(k-1)$.

**Corollary 4 (exact below $k$).** If $d < k$, line L6 returns $d$.

*Proof.* By Lemma 1, $T$ holds all $d$ distinct values, so $|T| = d < k$. $\square$

**Corollary 5 (error bound).** For $d \ge k \ge 3$ and $\varepsilon > 0$, $\Pr\big[|\hat d - d| > \varepsilon d\big] < \frac{1}{(k-2)\varepsilon^2}$.

*Proof.* By [Chebyshev's inequality](/chebyshev-inequality/) and Theorem 3, the probability is at most $\frac{d(d-k+1)}{(k-2)\varepsilon^2 d^2}$, and $(d-k+1)/d < 1$. $\square$

**Lemma 6 (the sample is uniform).** Let $d \ge k$ and let $S$ be the set of the items with the $k$ smallest values. Then $S$ is a uniform random $k$-subset of $D$, and $S$ is independent of $v_k$.

*Proof.* The values are independent and identically distributed, so their joint law does not change when the items are permuted. Fix a $k$-subset $R$ and a permutation $\pi$ of $D$ that maps $R$ to another $k$-subset $\pi(R)$. The event $\{S = R, v_k \le t\}$ is mapped by $\pi$ to $\{S = \pi(R), v_k \le t\}$, so the two events have the same probability. So $\Pr[S = R, v_k \le t] = \Pr[v_k \le t]/\binom{d}{k}$ for every $R$ and $t$, which is the claim. $\square$

**Theorem 7 (unbiased intersection and Jaccard).** Let $A$ and $B$ be sets with $|A \cup B| \ge k \ge 2$, and let the values of the items of $A \cup B$ be independent and uniform. Let $L$ be the $k$ smallest values of $T_A \cup T_B$, let $v_k = \max L$, and let $K$ be the number of values of $L$ whose items are in $A \cap B$. Then
$$\mathbb{E}\Big[\frac{K}{k}\Big] = \frac{|A \cap B|}{|A \cup B|}, \qquad \mathbb{E}\Big[\frac{K}{k}\cdot\frac{k-1}{v_k}\Big] = |A \cap B|.$$

*Proof.* By Lemma 1, $L$ holds the $k$ smallest values of $A \cup B$, so its items are the set $S$ of Lemma 6 for $D = A \cup B$. A value of $L$ whose item is in $A \cap B$ is in both $T_A$ and $T_B$ by the argument of Lemma 1, and a value of $L$ in both sketches belongs to an item of both sets, because the values are distinct. So $K = |S \cap A \cap B|$. Write $\mathbf{1}_x$ for the [indicator](/indicator-random-variable/) that $x \in S$. By Lemma 6, $\Pr[x \in S \mid v_k] = k/|A \cup B|$ for each $x$, so
$$\mathbb{E}[K \mid v_k] = \sum_{x \in A \cap B}\Pr[x \in S \mid v_k] = \frac{k\,|A \cap B|}{|A \cup B|}.$$
Taking expectations gives the first claim. For the second, condition on $v_k$ and then use Theorem 3 for $D = A \cup B$:
$$\mathbb{E}\Big[\frac{K}{k}\cdot\frac{k-1}{v_k}\Big] = \mathbb{E}\Big[\frac{|A \cap B|}{|A \cup B|}\cdot\frac{k-1}{v_k}\Big] = \frac{|A \cap B|}{|A \cup B|}\cdot|A \cup B| = |A \cap B|. \qquad \square$$

**Expected number of heap changes.** Let the distinct items arrive in some order. The $i$-th distinct item enters $T$ exactly when its value is among the $k$ smallest of the first $i$ values. By symmetry this has probability $\min(1, k/i)$, so the expected number of insertions is $k + \sum_{i=k+1}^{d} k/i = k(1 + H_d - H_k)$, where $H_j$ is the $j$-th harmonic number.

**What is cited.** The analysis above assumes an ideal hash. Bar-Yossef, Jayram, Kumar, Sivakumar and Trevisan (RANDOM 2002) prove that the estimate from the $t$ smallest values, with $t = O(1/\varepsilon^2)$ and a pairwise independent hash, is within a factor $1 \pm \varepsilon$ of $d$ with constant probability. That result is cited and not proved here. $\blacksquare$
