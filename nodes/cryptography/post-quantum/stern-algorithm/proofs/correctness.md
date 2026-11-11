---
title: Stern's algorithm returns only solutions, and a round succeeds with probability at least P
proves: [correctness, termination]
status: full
---

We use the notation of the page: $H \in \mathbb{F}_2^{r \times n}$ has rank $r = n - k$, $s \in \mathbb{F}_2^r$, $2p \le w$, and $\ell \le r$. In a round, $I$ is the set of $r$ positions, $J_1$ and $J_2$ are the disjoint halves of the complement, and $\Lambda$ is the set of the first $\ell$ pivot rows. $H_j$ is column $j$ of $H$.

**Lemma 1 (the elimination).** If $H_I$ is invertible, line L3 computes $H' = UH$ and $s' = Us$ for an invertible $U$ with $UH_I = \mathrm{Id}_r$, and row $i$ of $H'$ pivots on the $i$-th column of $I$. If $H_I$ is singular, line L4 detects it.

*Proof.* It is the Gauss-Jordan elimination of Prange's algorithm, with the same proof: row operations are left multiplications by invertible matrices, step $i$ makes the $i$-th column of $I$ the unit vector $u_i$, and a step fails to find a pivot exactly when the columns of $H_I$ are dependent. $\square$

**Lemma 2 (the candidates).** Let $H_I$ be invertible, and let $x \in \mathbb{F}_2^n$ with $\mathrm{supp}(x) \setminus I = A$. Then $Hx = s$ if and only if $x_I = s' + \sum_{j \in A} H'_j$.

*Proof.* $Hx = s$ if and only if $UHx = s'$, because $U$ is invertible. Since $H'_I = \mathrm{Id}_r$, $UHx = x_I + \sum_{j \in A} H'_j$. $\square$

**Lemma 3 (the collisions).** Lines L5 to L7 visit exactly the pairs $(A_1, A_2)$ with $A_1 \subseteq J_1$, $A_2 \subseteq J_2$, $|A_1| = |A_2| = p$, and $t|_\Lambda = 0$, where $t = s' + \sum_{j \in A_1 \cup A_2} H'_j$. They visit each such pair once, unless the round returns earlier.

*Proof.* Line L5 stores each $A_1$ under the key $a(A_1) = (s' + \sum_{j \in A_1} H'_j)|_\Lambda$. Line L6 visits each $A_2$ once, and line L7 visits the sets $A_1$ stored under $b(A_2) = (\sum_{j \in A_2} H'_j)|_\Lambda$, so it visits a pair exactly when $a(A_1) = b(A_2)$. Restriction to $\Lambda$ is linear, and $J_1 \cap J_2 = \emptyset$, so $t|_\Lambda = a(A_1) + b(A_2)$, which is zero exactly when $a(A_1) = b(A_2)$. $\square$

**Theorem 1 (soundness).** Each vector $e$ that STERN returns satisfies $He = s$ and $\mathrm{wt}(e) = w$.

*Proof.* A return happens only at line L10, in a round with $H_I$ invertible, for a pair $(A_1, A_2)$ with $|A_1| = |A_2| = p$ and $\mathrm{wt}(t) = w - 2p$. Line L10 sets $e_I = t$ and $e$ equal to 1 exactly on $A = A_1 \cup A_2$ outside $I$. So $\mathrm{supp}(e) \setminus I = A$ and Lemma 2 gives $He = s$. The sets $A_1$ and $A_2$ are disjoint and both are disjoint from $I$, so $\mathrm{wt}(e) = \mathrm{wt}(t) + |A_1| + |A_2| = w - 2p + 2p = w$. $\square$

**Theorem 2 (success of one round).** Let $e^\ast$ be a solution of weight $w$. If $H_I$ is invertible, $|\mathrm{supp}(e^\ast) \cap J_1| = |\mathrm{supp}(e^\ast) \cap J_2| = p$, and $e^\ast$ is zero on the $\ell$ columns of $I$ that the rows of $\Lambda$ pivot on, the round returns a solution. If the support of $e^\ast$ is a uniform random $w$-subset, independent of $H$ and of the random choices of the algorithm, each round with an invertible $H_I$ succeeds with probability at least

$$P = \frac{\binom{k_1}{p}\binom{k_2}{p}\binom{r-\ell}{w-2p}}{\binom{n}{w}} .$$

*Proof.* Let $A_1^\ast$ and $A_2^\ast$ be the parts of $\mathrm{supp}(e^\ast)$ in $J_1$ and $J_2$. By Lemma 2, $e^\ast_I = s' + \sum_{j \in A_1^\ast \cup A_2^\ast} H'_j$, which is the vector $t$ of the pair $(A_1^\ast, A_2^\ast)$. Row $i$ of $\Lambda$ pivots on a column $c_i$ of $I$, and the $i$-th entry of $e^\ast_I$ is $e^\ast_{c_i} = 0$ by assumption, so $t|_\Lambda = 0$. By Lemma 3 the round visits this pair unless it returns earlier. At this pair $\mathrm{wt}(t) = \mathrm{wt}(e^\ast) - 2p = w - 2p$, so line L9 passes. An earlier return is a solution by Theorem 1.

For the probability, fix $H$, $I$, $J_1$, $J_2$ and the window columns. The support of $e^\ast$ is independent of them. The number of $w$-subsets with exactly $p$ elements in $J_1$, exactly $p$ in $J_2$, and the other $w - 2p$ in the $r - \ell$ columns of $I$ outside the window is $\binom{k_1}{p}\binom{k_2}{p}\binom{r-\ell}{w-2p}$. Dividing by $\binom{n}{w}$ gives $P$. $\square$

**Theorem 3 (termination).** Assume $H$ has rank $r$, and there is a solution $e^\ast$ and a set $S_2 \subseteq \mathrm{supp}(e^\ast)$ of size $2p$ such that the columns on $S_1 = \mathrm{supp}(e^\ast) \setminus S_2$ are independent, the columns outside $S_2$ have rank $r$, $|S_1| \le r - \ell$, and $2p \le k$. Then STERN terminates with probability 1, and for fixed $H$, $s$ and $e^\ast$ the number of rounds with an invertible $H_I$ is geometric.

*Proof.* The independent columns on $S_1$ extend, inside the columns outside $S_2$, to a set $I_0$ of $r$ independent columns, because those columns have rank $r$. Then $S_2$ lies in the complement of $I_0$. Line L2 draws $I_0$ with positive probability, and the random order of the draw puts the $\ell$ window columns outside $S_1$ with positive probability, since $|S_1| \le r - \ell$. The random split of the complement puts exactly $p$ elements of $S_2$ in each half with positive probability. So each draw succeeds with some probability $q_0 > 0$ that depends only on $H$ and $e^\ast$, by Theorem 2. The draws are independent, so the probability that the first $N$ draws all fail is at most $(1 - q_0)^N$, which tends to 0. For fixed $H$, $s$ and $e^\ast$, the success of a round depends only on its own random choices, so the rounds with an invertible $H_I$ are independent trials with the same success probability, and their number up to the first success is geometric. $\blacksquare$

**Remark.** As for Prange, the mean number of rounds for a fixed error is $1/q$ for its own success probability $q$, and its average over the error is at least $1/P$ by Jensen's inequality. For random codes of the sizes in the tests, $q$ is close to $P$, and $1/P$ is the estimate that the page uses.
