---
title: Prange's algorithm returns only solutions, and a round succeeds with probability C(n-k, w)/C(n, w)
proves: [correctness, termination]
status: full
---

We use the notation of the page: $H \in \mathbb{F}_2^{r \times n}$ has rank $r = n - k$, $s \in \mathbb{F}_2^r$, and $0 \le w \le r$. For a set $I = \{I_1, \ldots, I_r\}$ of positions, $H_I$ is the $r \times r$ matrix of the columns of $H$ in $I$, in this order.

**Lemma 1 (the elimination).** If $H_I$ is invertible, lines L3 and L5 compute $H' = UH$ and $s' = Us$ for an invertible $U$ with $UH_I = \mathrm{Id}_r$. If $H_I$ is singular, line L4 detects it.

*Proof.* Gauss-Jordan elimination applies a sequence of row swaps and row additions to the augmented matrix $[H \mid s]$. Each of them is a left multiplication by an invertible elementary matrix, so after any number of steps the matrix is $[UH \mid Us]$ for an invertible $U$. The elimination handles the columns $I_1, \ldots, I_r$ in order. Before step $i$, rows $1$ to $i-1$ have their pivots in columns $I_1$ to $I_{i-1}$, and these columns are zero in every other row. Step $i$ looks for a row $j \ge i$ with a 1 in column $I_i$. If it finds one, it swaps it to position $i$ and adds it to every other row with a 1 in column $I_i$. Row $i$ has a 0 in columns $I_1, \ldots, I_{i-1}$, so the additions keep those columns as unit vectors, and column $I_i$ becomes the unit vector $u_i$. After step $r$, $(UH)_I = \mathrm{Id}_r$. If no row $j \ge i$ has a 1 in column $I_i$, then in the current matrix column $I_i$ is a combination of the unit vectors $u_1, \ldots, u_{i-1}$, which are columns $I_1, \ldots, I_{i-1}$. So the columns of $(UH)_I$ are linearly dependent, and since $U$ is invertible, so are the columns of $H_I$: $H_I$ is singular. Conversely, if $H_I$ is singular, the columns of $(UH)_I$ are dependent at every step, so they can never become $\mathrm{Id}_r$, and some step finds no pivot. $\square$

**Lemma 2 (the candidate).** Let $H_I$ be invertible, and let $x \in \mathbb{F}_2^n$ be zero outside $I$. Then $Hx = s$ if and only if $x_I = s'$.

*Proof.* $U$ is invertible, so $Hx = s$ if and only if $UHx = Us = s'$. Since $x$ is zero outside $I$, $UHx = (UH)_I\, x_I = \mathrm{Id}_r\, x_I = x_I$. $\square$

**Theorem 1 (soundness).** Each vector that PRANGE returns satisfies $He = s$ and $\mathrm{wt}(e) = w$.

*Proof.* A return happens only at line L8, after a round in which $H_I$ is invertible (Lemma 1, line L4) and $\mathrm{wt}(s') = w$ (line L6). Line L7 sets $e_I = s'$ and $e = 0$ outside $I$. By Lemma 2, $He = s$. The weight of $e$ is the weight of $e_I = s'$, which is $w$. $\square$

**Theorem 2 (success of one round).** Let $e^\ast$ be a solution, $He^\ast = s$ and $\mathrm{wt}(e^\ast) = w$. If $\mathrm{supp}(e^\ast) \subseteq I$ and $H_I$ is invertible, the round returns $e^\ast$. Now let the support of $e^\ast$ be a uniform random $w$-subset of the positions, independent of $H$ and of the random choices of the algorithm. Then for each round in which $H_I$ is invertible, the probability of success is at least

$$P = \frac{\binom{n-k}{w}}{\binom{n}{w}},$$

with equality when $e^\ast$ is the only solution of weight $w$.

*Proof.* If $\mathrm{supp}(e^\ast) \subseteq I$, then $e^\ast$ is zero outside $I$, and Lemma 2 gives $s' = e^\ast_I$. So $\mathrm{wt}(s') = \mathrm{wt}(e^\ast) = w$, line L6 passes, and line L7 rebuilds $e^\ast$.

For the probability, fix $H$. Line L2 draws $I$ uniformly among the $\binom{n}{r}$ subsets of size $r$, and the event "$H_I$ is invertible" depends only on $H$ and $I$. The support of $e^\ast$ is independent of both. So, conditioned on any fixed $I$ with $H_I$ invertible, the probability that the uniform $w$-subset $\mathrm{supp}(e^\ast)$ lies inside the fixed $r$-set $I$ is the number of $w$-subsets of $I$ divided by the number of all $w$-subsets: $\binom{r}{w}/\binom{n}{w} = P$. In that event the round succeeds, so the probability of success is at least $P$. If $e^\ast$ is the only solution of weight $w$, a round can succeed only by returning $e^\ast$ (Theorem 1), and by Lemma 2 it returns $e^\ast$ only if $\mathrm{supp}(e^\ast) \subseteq I$. So the probability is exactly $P$. $\square$

**Theorem 3 (termination).** Assume $H$ has rank $r$, the instance has a solution $e^\ast$ whose support columns are linearly independent, and $w \le r$. Then PRANGE terminates with probability 1. For fixed $H$, $s$ and $e^\ast$, let $p$ be the probability that one round with an invertible $H_I$ succeeds. Then the number of such rounds is geometric with mean $1/p$, and under the hypotheses of Theorem 2 the average of $p$ over the support of $e^\ast$ is at least $P$.

*Proof.* The columns of $H$ on $\mathrm{supp}(e^\ast)$ are independent, and $H$ has rank $r$, so they extend to a set $I_0$ of $r$ independent columns with $\mathrm{supp}(e^\ast) \subseteq I_0$. Line L2 draws $I_0$ with probability $q_0 = 1/\binom{n}{r} > 0$ in each draw, and then the round returns by Theorem 2. The draws are independent, so the probability that the first $N$ draws all miss $I_0$ is at most $(1 - q_0)^N$, which tends to 0. So the algorithm stops with probability 1. With $H$, $s$ and $e^\ast$ fixed, the rounds use fresh independent draws of $I$, and the success of a round depends only on its own $I$. So the rounds with an invertible $H_I$ are independent trials with the same success probability $p$, and the number of them up to the first success is geometric with mean $1/p$. The average of $p$ over the uniform support of $e^\ast$ is the probability of success of one round in Theorem 2, which is at least $P$. $\blacksquare$

**Remark.** By Jensen's inequality the average of $1/p$ is at least $1/P$, not at most. For random codes of the sizes in the tests, $p$ is close to $P$ for almost every error, and $1/P$ is the standard estimate of the number of rounds that the literature and the page use.
