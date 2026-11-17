---
title: Pooled size factors are exact when more than half of the genes do not change, and the weak equations make the linear system uniquely solvable
proves: [correctness]
status: full
---

We prove that pooling and deconvolution recover the true size factors, up to one common constant, in exact arithmetic when the counts of more than half of the genes are proportional to the size factors (Theorem 2). We show when the pool equations alone have more than one solution (Lemma 3), and that the weak equations of line L7 always make the solution unique (Lemma 4). With clusters, the same holds when the condition holds inside each cluster and between each cluster and the reference (Theorem 5). That real counts satisfy these conditions is a modelling assumption, and with Poisson noise the factors have an error that the tests measure but the proof does not bound.

**Setting.** Counts $Y_{gj} \ge 0$ for genes $g = 1, \dots, G$ and cells $j = 1, \dots, n$, with library sizes $t_j = \sum_g Y_{gj} > 0$. Line L1 sets $Z_{gj} = Y_{gj}/t_j$ and line L2 sets $U_g = \frac1n\sum_j Z_{gj}$. For a pool $S$, line L5 sets $f_S = \operatorname{median}\{V_g/U_g : U_g > 0\}$ with $V_g = \sum_{j \in S} Z_{gj}$. Lines L6 to L8 minimize
$$F(x) = \sum_S \Big(\sum_{j \in S} x_j - f_S\Big)^2 + \varepsilon\sum_j (x_j - e_j)^2,$$
where $e_j = \operatorname{median}\{Z_{gj}/U_g : U_g > 0\}$ is the single-cell estimate and $\varepsilon = 10^{-6}$. Line L9 returns $\hat\theta_j = x_j t_j$, and line L11 divides by the mean.

**Model.** There are true factors $\theta_j > 0$ and a set $N$ of genes, the non-DE genes, with $Y_{gj} = \theta_j\lambda_g$ for $g \in N$, $\lambda_g > 0$. The other genes may have any counts. Let $P = \{g : U_g > 0\}$, so $N \subseteq P$, and assume $|N| > |P|/2$.

**Lemma 1 (ratios of the non-DE genes).** Let $x_j = \theta_j/t_j$ and $\bar x = \frac1n\sum_j x_j$. For $g \in N$ and every pool $S$, $V_g/U_g = \sum_{j \in S}x_j/\bar x$, and $Z_{gj}/U_g = x_j/\bar x$.

*Proof.* For $g \in N$, $Z_{gj} = \theta_j\lambda_g/t_j = x_j\lambda_g$, so $U_g = \lambda_g\bar x$ and $V_g = \lambda_g\sum_{j \in S}x_j$. Divide. $\square$

The ratios do not depend on $g$. This is why the method divides by the library size before pooling: the library size of a cell is not proportional to $\theta_j$ when other genes change, but $x_j$ absorbs it, and line L9 multiplies it back.

**Theorem 2 (exact recovery).** Under the model, the minimizer of $F$ is $x^\ast_j = x_j/\bar x$, and the returned factors are $\theta_j/\bar\theta$, with $\bar\theta$ the mean of the true factors.

*Proof.* By Lemma 1, more than half of the values in each median of line L5 equal $\sum_{j \in S}x_j/\bar x$. When more than half of a list of values equal $c$, the median is $c$; the proof of this fact is in the proof of [median-of-ratios normalization](/median-of-ratios-normalization/). So $f_S = \sum_{j \in S}x^\ast_j$ for every pool, and in the same way $e_j = x^\ast_j$. Then $F(x^\ast) = 0$, and $F \ge 0$, so $x^\ast$ is a minimizer. It is the only one by Lemma 4. Line L9 gives $\hat\theta_j = x^\ast_j t_j = \theta_j/\bar x$, and dividing by the mean gives $\theta_j/\bar\theta$. $\square$

**Lemma 3 (the pool equations alone).** Let the pools be all windows of $w$ consecutive positions on a ring of $n$ cells, for each $w$ in a set $W$, and let $A$ be the matrix of these equations. Then $A$ has a nonzero null vector if and only if there is an integer $k$, $0 < k < n$, such that $n$ divides $kw$ for every $w \in W$. Then $v_p = \cos(2\pi kp/n)$, on ring positions $p$, is such a vector.

*Proof.* For one $w$, the pool matrix $C_w$ has a row for each start $s$ with ones at positions $s, \dots, s + w - 1$ modulo $n$. It is a circulant matrix, so the vectors $\phi_k(p) = \omega^{kp}$ with $\omega = e^{2\pi i/n}$ are its eigenvectors, with eigenvalues $\mu_w(k) = \sum_{i=0}^{w-1}\omega^{ki}$. For $k = 0$, $\mu_w(0) = w > 0$. For $0 < k < n$, $\omega^k \ne 1$ and $\mu_w(k) = (\omega^{kw} - 1)/(\omega^k - 1)$, which is 0 if and only if $\omega^{kw} = 1$, that is, $n$ divides $kw$. Now $A^\ast A = \sum_{w \in W} C_w^\ast C_w$ has the same eigenvectors with eigenvalues $\sum_w|\mu_w(k)|^2$. This sum is 0 if and only if every $\mu_w(k) = 0$, and $A$ has a nonzero null vector if and only if $A^\ast A$ has the eigenvalue 0. When $\mu_w(k) = 0$ for all $w$, $C_w\phi_k = 0$, and since $C_w$ is real, the real part $v$ of $\phi_k$ also satisfies $C_wv = 0$. $\square$

The sizes $20, 40, 60, 80, 100$ of the paper are all multiples of 20, and 20 is one of them, so the condition is that $n$ divides $20k$ for some $0 < k < n$. This holds if and only if $\gcd(n, 20) > 1$, with $k = n/\gcd(n, 20)$: for every even $n$ and every multiple of 5. For $n = 100$, $k = 5$. For $n = 101$ no $k$ works. On such a null vector the pool equations cannot tell the factors apart: adding $c\,v$ to $x$ changes no pool sum.

**Lemma 4 (uniqueness).** For every $\varepsilon > 0$, $F$ has exactly one minimizer, the solution of $(A^\top A + \varepsilon I)x = A^\top f + \varepsilon e$.

*Proof.* $F$ is a quadratic with Hessian $2(A^\top A + \varepsilon I)$. For $y \ne 0$, $y^\top(A^\top A + \varepsilon I)y = \|Ay\|^2 + \varepsilon\|y\|^2 > 0$, so the Hessian is positive definite, $F$ is strictly convex, and its only stationary point, the solution of the normal equations, is its minimizer. $\square$

When $A$ has full column rank, the weak equations move the solution by $O(\varepsilon)$ in general, and not at all in the setting of Theorem 2. When $A$ has a null space, the weak equations fix the component of $x$ in it to that of the single-cell estimates. In floating point the normal matrix then has a condition number of order $\|A\|^2/\varepsilon$, so rounding errors grow by that factor; the tests use a tolerance of $10^{-5}$ for this reason.

**Theorem 5 (clusters).** Suppose the cells are split into clusters, the model holds inside each cluster with its own non-DE set, and line L10 scales cluster $c$ by $\tau_c = \operatorname{median}_g P_{cg}/P_{rg}$ over genes positive in both, where $P_{cg}$ is the mean of $Y_{gj}/\hat\theta_j$ over the cells of $c$ and $r$ is the reference cluster. If more than half of these genes have $Y_{gj} = \theta_j\lambda_g$ in both clusters, then the final factors are $\theta_j/\bar\theta$ for all cells.

*Proof.* By Theorem 2 applied to cluster $c$ alone, $\hat\theta_j = \theta_j/\kappa_c$ for $j \in c$, with a constant $\kappa_c > 0$. For a gene with $Y_{gj} = \theta_j\lambda_g$ in both clusters, $Y_{gj}/\hat\theta_j = \kappa_c\lambda_g$, so $P_{cg} = \kappa_c\lambda_g$ and $P_{cg}/P_{rg} = \kappa_c/\kappa_r$. More than half of the ratios equal this, so $\tau_c = \kappa_c/\kappa_r$, and $\tau_c\hat\theta_j = \theta_j/\kappa_r$ for every cell of every cluster. Line L11 divides by the mean, which gives $\theta_j/\bar\theta$. $\square$

So with clusters the non-DE condition is needed inside each cluster and between each cluster and the reference, not over all cells at once.

**What the lines compute.** Lines L1 and L2 compute $Z$ and $U$. Line L3 builds the ring, and line L4 the windows; each cell is in $w$ windows of size $w$, so in $\sum_{w \in W}w$ pools. Line L5 computes $f_S$, skipping genes with $U_g = 0$. Lines L6 to L8 build $A^\top A + \varepsilon I$ and $A^\top f + \varepsilon e$ directly and solve by Gaussian elimination with partial pivoting. Line L9 multiplies by $t_j$, line L10 is Theorem 5, and line L11 scales to mean 1. Theorem 2 does not use the ring order: it holds for any set of pools. The ring order matters only for noise, because it puts cells of similar size in one pool.

**Complexity.** With $q = |W|$ pool sizes and $w_{max}$ the largest, line L5 takes $O(Gw)$ per pool plus a median, so $O(qn(Gw_{max} + G\log G))$ in all. Building the normal matrix takes $O(qnw_{max}^2)$, and solving it $O(n^3)$. scran solves the sparse system instead, which is much faster for many cells.

**What the tests check.** The test file checks Theorem 2 with 0, 20 and 45 percent of changed genes, that the library size is wrong on such data, Theorem 5 with two clusters, and the page example with its singular pools of size 2. It compares the floating point solution with an exact rational solution of the same normal equations. It checks Lemma 3 with the null vector for $n = 100$ and the divisibility condition for $n = 100$ and $n = 101$, and that each cell is in 300 pools with the default sizes. A simulation with Poisson counts, more than half of them 0, measures that the pooled factors have a smaller error and a smaller composition bias than the library size, and that most single-cell medians are 0. These are measurements, not theorems.
