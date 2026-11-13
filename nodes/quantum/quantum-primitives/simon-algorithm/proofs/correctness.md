---
title: Simon's algorithm returns the hidden string and stops with probability 1
proves: [correctness]
status: full
---

We write $N = 2^n$, $y \cdot s = \sum_j y_j s_j \bmod 2$ and $s^\perp = \{y : y \cdot s = 0\}$. The input register is qubits $0$ to $n - 1$ and the output register is qubits $n$ to $n + m - 1$. The promise is $f(x) = f(x') \iff x' \in \{x, x \oplus s\}$.

**Lemma 1 (one run).** Lines L3 to L7 give an outcome $y$ with
$$\Pr[y] = \begin{cases} 2/N & \text{if } s \ne 0 \text{ and } y \cdot s = 0, \\ 0 & \text{if } s \ne 0 \text{ and } y \cdot s = 1, \\ 1/N & \text{if } s = 0. \end{cases}$$

*Proof.* Line L3 gives $|0\rangle|0\rangle$. Line L4 gives $N^{-1/2} \sum_x |x\rangle|0\rangle$, and line L5 gives $N^{-1/2} \sum_x |x\rangle |f(x)\rangle$. By the identity $H^{\otimes n} |x\rangle = N^{-1/2} \sum_y (-1)^{x \cdot y} |y\rangle$, line L6 gives
$$\frac{1}{N} \sum_y |y\rangle \otimes \sum_x (-1)^{x \cdot y} |f(x)\rangle = \frac{1}{N} \sum_y |y\rangle \otimes \sum_{v} c_{y,v} |v\rangle, \qquad c_{y,v} = \sum_{x : f(x) = v} (-1)^{x \cdot y}.$$
So $\Pr[y] = N^{-2} \sum_v |c_{y,v}|^2$, where $v$ runs over the labels that $f$ takes.

If $s = 0$, each label $v$ has one preimage, so $|c_{y,v}| = 1$ and there are $N$ labels: $\Pr[y] = N/N^2 = 1/N$.

If $s \ne 0$, each label $v$ has two preimages $x_v$ and $x_v \oplus s$, and there are $N/2$ labels. Then $c_{y,v} = (-1)^{x_v \cdot y}(1 + (-1)^{s \cdot y})$, which is $\pm 2$ if $y \cdot s = 0$ and $0$ if $y \cdot s = 1$. So $\Pr[y] = N^{-2} \cdot (N/2) \cdot 4 = 2/N$ for $y \in s^\perp$, and $0$ otherwise. Since $|s^\perp| = N/2$, this is the uniform distribution on $s^\perp$. $\square$

**Lemma 2 (the system).** Every equation in $E$ holds for $s$. If $E$ has rank $n - 1$, its solution set is $\{0, s'\}$ for one string $s' \ne 0$, and if $s \ne 0$ then $s' = s$.

*Proof.* By Lemma 1, if $s \ne 0$ each sample $y$ has $y \cdot s = 0$, and if $s = 0$ every equation $y \cdot 0 = 0$ holds. The solution set of a homogeneous system over GF(2) of rank $n - 1$ in $n$ unknowns is a subspace of dimension $1$, so it has the form $\{0, s'\}$ with $s' \ne 0$. If $s \ne 0$, then $s$ is a nonzero solution, so $s = s'$. $\square$

**Lemma 3 (the loop ends).** With probability $1$ the loop of line L2 ends, and the expected number of runs is $\sum_{j=1}^{n-1} 1/(1 - 2^{-j})$ if $s \ne 0$, and $\sum_{j=2}^{n} 1/(1 - 2^{-j})$ if $s = 0$.

*Proof.* Let $V = s^\perp$ (dimension $d = n - 1$) if $s \ne 0$, and $V = \{0,1\}^n$ (dimension $d = n$) if $s = 0$. By Lemma 1 each sample is uniform on $V$ and independent of the earlier ones, because each run starts from a fresh $|0\rangle$. When the rows of $E$ span a subspace $W \subseteq V$ of dimension $r$, a new sample is outside $W$ with probability $1 - 2^{r - d}$, and exactly then the rank becomes $r + 1$. While $r < n - 1 \le d$, this probability is at least $1/2$. So the number of runs at rank $r$ is geometric with mean $1/(1 - 2^{r-d})$, and it is finite with probability $1$. Summing over $r = 0, \ldots, n - 2$ gives the two formulas, with $j = d - r$. $\square$

**Theorem.** SIMON$(U_f, f, n, m)$ stops with probability $1$ and returns $s$.

*Proof.* By Lemma 3 the loop ends, and then $E$ has rank $n - 1$. By Lemma 2, line L9 finds the unique nonzero solution $s'$.

If $s \ne 0$, Lemma 2 gives $s' = s$. By the promise $f(0) = f(0 \oplus s) = f(s')$, so line L10 returns $s' = s$.

If $s = 0$, $f$ is one-to-one by the promise, and $s' \ne 0$, so $f(0) \ne f(s')$. Line L10 returns $0 = s$. $\blacksquare$

**The bound on the mean.** For $s \ne 0$,
$$\sum_{j=1}^{n-1} \frac{1}{1 - 2^{-j}} = \sum_{j=1}^{n-1} \Big(1 + \frac{1}{2^j - 1}\Big) < n - 1 + \sum_{j \ge 1} \frac{1}{2^j - 1} = n - 1 + 1.60669\ldots,$$
and the sum for $s = 0$ is smaller term by term after a shift of the index. With the two classical queries of line L10, the expected number of queries is less than $n + 2.61$.

**The tail.** Let $k$ samples be uniform on $V$ of dimension $d$. They fail to span $V$ only if they all lie in some hyperplane of $V$. There are $2^d - 1$ hyperplanes, each holds a sample with probability $1/2$, so by the union bound the failure probability is at most $(2^d - 1)/2^k < 2^{d - k}$. The exact value is $1 - \prod_{i=0}^{d-1}(1 - 2^{i-k})$ for $k \ge d$, from counting the $k$-tuples that span.
