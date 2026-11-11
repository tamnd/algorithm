---
title: The Lee-Brickell algorithm returns only solutions, and a round succeeds with probability at least P_p
proves: [correctness, termination]
status: full
---

We use the notation of the page: $H \in \mathbb{F}_2^{r \times n}$ has rank $r = n - k$, $s \in \mathbb{F}_2^r$, $0 \le p \le w$, and $I$ is the set of $r$ positions drawn in line L2, with complement $J$. For a column index $j$, $H_j$ is column $j$ of $H$.

**Lemma 1 (the elimination).** If $H_I$ is invertible, line L3 computes $H' = UH$ and $s' = Us$ for an invertible $U$ with $UH_I = \mathrm{Id}_r$, where row $i$ of $H'$ pivots on the $i$-th column of $I$. If $H_I$ is singular, line L4 detects it.

*Proof.* This is the same Gauss-Jordan elimination as in Prange's algorithm, and the proof is the same: each row swap and row addition is a left multiplication by an invertible matrix, step $i$ makes the $i$-th column of $I$ the unit vector $u_i$ and keeps the earlier pivot columns, and a step finds no pivot exactly when the columns of $H_I$ are dependent. $\square$

**Lemma 2 (the candidates).** Let $H_I$ be invertible, and let $x \in \mathbb{F}_2^n$ with $\mathrm{supp}(x) \cap J = A$. Then $Hx = s$ if and only if $x_I = s' + \sum_{j \in A} H'_j$, where $x_I$ is read in the pivot order of $I$.

*Proof.* $U$ is invertible, so $Hx = s$ if and only if $UHx = s'$. Split $x$ into its part on $I$ and its part on $J$: $UHx = H'_I x_I + \sum_{j \in A} H'_j = x_I + \sum_{j \in A} H'_j$, because $H'_I = \mathrm{Id}_r$. So $UHx = s'$ if and only if $x_I = s' + \sum_{j \in A} H'_j$. $\square$

**Theorem 1 (soundness).** Each vector $e$ that LEE-BRICKELL returns satisfies $He = s$ and $\mathrm{wt}(e) = w$.

*Proof.* A return happens only at line L9, in a round with $H_I$ invertible (Lemma 1), for a set $A \subseteq J$ with $\mathrm{wt}(t) = w - |A|$, where $t = s' + \sum_{j \in A} H'_j$. Line L8 sets $e_I = t$, $e_j = 1$ for $j \in A$, and $e = 0$ on $J \setminus A$. So $\mathrm{supp}(e) \cap J = A$ and $e_I = t$, and Lemma 2 gives $He = s$. The sets $I$ and $A$ are disjoint, so $\mathrm{wt}(e) = \mathrm{wt}(t) + |A| = w$. $\square$

**Theorem 2 (success of one round).** Let $e^\ast$ be a solution, $He^\ast = s$ and $\mathrm{wt}(e^\ast) = w$. If $H_I$ is invertible and $|\mathrm{supp}(e^\ast) \cap J| \le p$, the round returns a solution. Now let the support of $e^\ast$ be a uniform random $w$-subset of the positions, independent of $H$ and of the random choices of the algorithm. Then each round with an invertible $H_I$ succeeds with probability at least

$$P_p = \frac{\sum_{i=0}^{p} \binom{k}{i}\binom{r}{w-i}}{\binom{n}{w}},$$

with equality when $e^\ast$ is the only solution of weight $w$.

*Proof.* Let $A^\ast = \mathrm{supp}(e^\ast) \cap J$, with $|A^\ast| \le p$. Line L5 runs over all subsets of $J$ of size at most $p$, so it reaches $A^\ast$ unless the round returns earlier, and an earlier return is a solution by Theorem 1. At $A = A^\ast$, Lemma 2 applied to $e^\ast$ gives $e^\ast_I = s' + \sum_{j \in A^\ast} H'_j = t$, so $\mathrm{wt}(t) = w - |A^\ast|$, line L7 passes, and the round returns.

For the probability, fix $H$ and a set $I$ with $H_I$ invertible; $I$ depends only on the random choices of the algorithm, and $\mathrm{supp}(e^\ast)$ is independent of it. The number of $w$-subsets of the positions that have exactly $i$ elements in $J$ (of size $k$) and $w - i$ in $I$ (of size $r$) is $\binom{k}{i}\binom{r}{w-i}$. Summing over $i \le p$ and dividing by $\binom{n}{w}$ gives the probability $P_p$ that $|A^\ast| \le p$, and in that event the round succeeds. If $e^\ast$ is the only solution of weight $w$, a round can succeed only by returning $e^\ast$, and by Lemma 2 the candidate for a set $A$ equals $e^\ast$ only if $A = A^\ast$, which line L5 visits only when $|A^\ast| \le p$. So the probability is exactly $P_p$. $\square$

**Theorem 3 (termination).** Assume $H$ has rank $r$, and the instance has a solution $e^\ast$ whose support columns are linearly independent (this needs $w \le r$). Then LEE-BRICKELL terminates with probability 1. For fixed $H$, $s$ and $e^\ast$, the number of rounds with an invertible $H_I$ is geometric with mean $1/q$, where $q$ is the probability that one such round succeeds; averaged over a uniform support of $e^\ast$, $q$ is at least $P_p$.

*Proof.* The independent columns on $\mathrm{supp}(e^\ast)$ extend to $r$ independent columns, because $H$ has rank $r$. Call that set $I_0$. Each draw of line L2 equals $I_0$ with probability $1/\binom{n}{r} > 0$, and then $\mathrm{supp}(e^\ast) \cap J = \emptyset$, so the round succeeds by Theorem 2. The draws are independent, so the probability that the first $N$ draws all miss $I_0$ is at most $(1 - 1/\binom{n}{r})^N$, which tends to 0. With $H$, $s$ and $e^\ast$ fixed, the success of a round depends only on its own draw, so the rounds with an invertible $H_I$ are independent trials with the same success probability $q$, and their number up to the first success is geometric with mean $1/q$. The average of $q$ over the support of $e^\ast$ is the probability in Theorem 2, which is at least $P_p$. $\blacksquare$

**Remark.** By Jensen's inequality the average of $1/q$ is at least $1/P_p$. For random codes of the sizes in the tests, $q$ is close to $P_p$ for almost every error, and $1/P_p$ is the standard estimate that the page uses.
