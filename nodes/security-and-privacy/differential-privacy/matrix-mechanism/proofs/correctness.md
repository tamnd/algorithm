---
title: The matrix mechanism is epsilon-DP and unbiased, with error 2 (Delta_A/epsilon)^2 trace(W (A^T A)^(-1) W^T)
proves: [correctness]
status: full
---

We use the pseudocode of the page. The data is a histogram $x \in \mathbb{N}^n$. Two histograms are neighbors if they differ by 1 in one cell: $x' = x \pm e_j$ (add/remove one record). The workload is an $m \times n$ matrix $W$ and the strategy is a $p \times n$ matrix $A$ of full column rank $n$. Let $\Delta_A = \max_j \sum_i |A_{ij}|$, $b = \Delta_A/\varepsilon$, and $A^+ = (A^\top A)^{-1} A^\top$. The noise $z = (z_1, \ldots, z_p)$ has independent $\mathrm{Lap}(b)$ entries.

**Claim 1 (privacy).** The output $W A^+ (A x + z)$ is $\varepsilon$-DP.

*Proof.* For neighbors $x' = x \pm e_j$, $A x' - A x = \pm A e_j$, the $j$-th column of $A$ up to sign. So $\|A x - A x'\|_1 = \sum_i |A_{ij}| \le \Delta_A$, and $\Delta_A$ is reached for the column with the largest $\ell_1$ norm. The density of $y = A x + z$ at a point $v \in \mathbb{R}^p$ is $\prod_i \frac{1}{2b} e^{-|v_i - (Ax)_i|/b}$. By the triangle inequality, for every $v$,

$$\frac{p_x(v)}{p_{x'}(v)} = \exp\Big(\frac{1}{b} \sum_i \big(|v_i - (Ax')_i| - |v_i - (Ax)_i|\big)\Big) \le \exp\Big(\frac{\|Ax - Ax'\|_1}{b}\Big) \le e^{\varepsilon}.$$

So $y$ is $\varepsilon$-DP. Lines L3 to L5 compute a fixed function of $y$ that does not look at $x$, so the output is $\varepsilon$-DP by post-processing. $\square$

**Claim 2 (unbiased).** $\mathbb{E}[W A^+ y] = W x$.

*Proof.* $A^+ A = (A^\top A)^{-1} A^\top A = I_n$, and $\mathbb{E}[z] = 0$. So $\mathbb{E}[A^+ y] = A^+ A x = x$, and $W$ is linear. $\square$

**Claim 3 (error).** The expected total squared error is

$$\mathbb{E}\,\|W A^+ y - W x\|_2^2 = 2 b^2 \operatorname{tr}\big(W (A^\top A)^{-1} W^\top\big) = \frac{2\Delta_A^2}{\varepsilon^2} \operatorname{tr}\big(W (A^\top A)^{-1} W^\top\big).$$

*Proof.* The error is $W A^+ z$ (Claim 2). The entries of $z$ are independent with mean 0 and variance $2b^2$, so $\mathbb{E}[z z^\top] = 2b^2 I_p$. Then

$$\mathbb{E}\,\|W A^+ z\|_2^2 = \operatorname{tr}\big(W A^+ \,\mathbb{E}[z z^\top]\, (A^+)^\top W^\top\big) = 2b^2 \operatorname{tr}\big(W A^+ (A^+)^\top W^\top\big),$$

and $A^+ (A^+)^\top = (A^\top A)^{-1} A^\top A (A^\top A)^{-1} = (A^\top A)^{-1}$. $\square$

**Claim 4 (least squares is the best linear reconstruction).** Among all matrices $B$ with $B A = W$, the choice $B = W A^+$ has the smallest expected total squared error $\mathbb{E}\|B z\|_2^2$.

*Proof.* Each such $B$ gives an unbiased estimate $B y$ of $W x$, with error $\mathbb{E}\|Bz\|^2 = 2b^2 \operatorname{tr}(B B^\top)$. Write $B = W A^+ + D$. Then $D A = B A - W A^+ A = 0$. So $D (A^+)^\top = D A (A^\top A)^{-1} = 0$, and

$$\operatorname{tr}(B B^\top) = \operatorname{tr}(W A^+ (A^+)^\top W^\top) + 2 \operatorname{tr}(W A^+ D^\top) + \operatorname{tr}(D D^\top).$$

The middle term is $2 \operatorname{tr}(D (A^+)^\top W^\top) = 0$, and the last term is at least 0, with equality only for $D = 0$. $\square$

This is the Gauss-Markov theorem for independent noise of equal variance. It says that, for a fixed strategy $A$, the only free choice left is $A$ itself.

**Cost.** Line L1 reads $A$ in $O(pn)$. Line L2 costs $O(pn)$ and $p$ Laplace draws. Line L3 forms $A^\top A$ in $O(pn^2)$, inverts it in $O(n^3)$ and multiplies by $A^\top$ in $O(pn^2)$. Line L4 costs $O(pn)$ and line L5 costs $O(mn)$. The space is $O(pn + mn)$ for the matrices. Lines L1 and L3 do not depend on the data, so for a fixed strategy they can be done one time and reused.
