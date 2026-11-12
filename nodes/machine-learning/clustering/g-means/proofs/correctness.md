---
title: G-means stops, never exceeds k_max, returns a Lloyd fixed point, and applies the Anderson-Darling test correctly
proves: [correctness]
status: full
---

**Lemma 1 (the children).** If $Y \sim \mathcal{N}(0, \lambda)$ with $\lambda > 0$, then $\mathbb{E}[Y \mid Y > 0] = \sqrt{2\lambda/\pi}$.

*Proof.* With the density $\varphi_\lambda(y) = (2\pi\lambda)^{-1/2} e^{-y^2/(2\lambda)}$,
$$\mathbb{E}[Y \mid Y > 0] = 2\int_0^\infty y\,\varphi_\lambda(y)\,dy = \frac{2}{\sqrt{2\pi\lambda}}\Big[-\lambda e^{-y^2/(2\lambda)}\Big]_0^\infty = \frac{2\lambda}{\sqrt{2\pi\lambda}} = \sqrt{\frac{2\lambda}{\pi}} . \qquad \square$$

So for a Gaussian cluster with main eigenvector $s$ and eigenvalue $\lambda$, the starting points $c \pm s\sqrt{2\lambda/\pi}$ of line L5 are the means of the two halves cut by the hyperplane through $c$ orthogonal to $s$. They are only starting points: line L5 then runs 2-means.

**Lemma 2 (the form of the statistic).** For sorted values $0 < z_{(1)} \le \cdots \le z_{(n)} < 1$,
$$\sum_{i=1}^n (2i - 1)\big[\ln z_{(i)} + \ln(1 - z_{(n+1-i)})\big] = \sum_{i=1}^n \big[(2i - 1)\ln z_{(i)} + (2(n - i) + 1)\ln(1 - z_{(i)})\big].$$
So the function `anderson_darling` computes the usual Anderson-Darling statistic $A^2$, times Stephens' factor $1 + 4/n - 25/n^2$.

*Proof.* The first parts agree term by term. In the second part of the left side, put $j = n + 1 - i$. Then $2i - 1 = 2(n + 1 - j) - 1 = 2(n - j) + 1$, and the sum becomes $\sum_j (2(n - j) + 1)\ln(1 - z_{(j)})$. $\square$

**Lemma 3 (invariance).** Let $y_i = \langle x_i, v\rangle / \|v\|^2$. For any $a \ne 0$ and $b$, the statistic of the values $a y_i + b$ equals the statistic of the values $y_i$. In particular it does not depend on the length or the sign of $v$.

*Proof.* Standardization with the sample mean and the sample standard deviation maps $a y_i + b$ to $\operatorname{sign}(a)$ times the standardized $y_i$. If $a > 0$, the values $z_{(i)}$ are the same. If $a < 0$, the symmetry $\Phi(-u) = 1 - \Phi(u)$ maps the sorted list $z_{(1)}, \ldots, z_{(n)}$ to $1 - z_{(n)}, \ldots, 1 - z_{(1)}$, so $z_{(i)}$ becomes $1 - z_{(n+1-i)}$ and $1 - z_{(n+1-i)}$ becomes $z_{(i)}$. Each term of the sum in Lemma 2 (left side) stays the same. Replacing $v$ by $\mu v$ with $\mu \ne 0$ multiplies every $y_i$ by $1/\mu$. $\square$

**Theorem.** Assume $k_{\max} \ge 1$. G-means stops after at most $k_{\max}$ passes of lines L2 to L9. It never holds more than $k_{\max}$ centers. When it returns, each returned center with at least one point is the mean of its points, and each point is with a nearest center.

*Proof.* Let $K$ be the number of centers at line L2. In the loop of line L3, let $N$ be the number of centers already written into the new list. A center $j$ is tested only if $N + (K - j) < k_{\max}$, where $K - j$ counts center $j$ and the centers after it. Keeping center $j$ leaves $N + (K - j)$ unchanged, after the step to $j + 1$; a split adds one. So the quantity $N + (K - j)$ starts at $K \le k_{\max}$, grows by one only when it is below $k_{\max}$, and so stays at most $k_{\max}$. At the end of the loop it is the new number of centers, which is therefore at most $k_{\max}$.

If no center is replaced, line L9 returns. Otherwise the number of centers grows by at least one. It starts at 1 and never exceeds $k_{\max}$, so there are at most $k_{\max}$ passes. Each pass runs Lloyd's algorithm, which stops by the correctness of [k-means](/k-means/), and finitely many 2-means runs, which stop for the same reason.

At the return, the centers and the labels are the output of the Lloyd run of line L2 in the same pass, and the loop changed neither. That run stopped because the labels did not change, so each point is with a nearest center (ties go to the current center), and each center with points is the mean of its points, which was computed from these same labels. (The implementation also stops a Lloyd run after 300 iterations as a safety cap; this last claim is for a run that converged before the cap.) $\square$

**Remark (what is not claimed).** The theorem says nothing about whether the returned $k$ is the true number of clusters. Each test has false alarm rate about $\alpha$ only under the null hypothesis that the projected values are a normal sample, and the projection depends on the data through the 2-means run, so even this holds only approximately.
