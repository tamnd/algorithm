---
title: The Newton form built from the divided-difference table interpolates the data
proves: [correctness, termination]
status: full
---

**Setting.** The nodes are $z_0, \ldots, z_n$, with equal nodes adjacent. For a node value $v$ let $\mu_S(v)$ be the number of times $v$ occurs in a block $S = (z_i, \ldots, z_{i+k})$ of consecutive nodes. The data are numbers $D(v, r)$ for each node value $v$ and $0 \le r < \mu(v)$, where $\mu(v)$ is the multiplicity of $v$ in the full list; $D(v, 0)$ is the value $y$ and $D(v, r)$ plays the role of $f^{(r)}(v)$. A polynomial $P$ *matches the data on $S$* when $P^{(r)}(v) = D(v, r)$ for each $v$ in $S$ and each $0 \le r < \mu_S(v)$. For distinct nodes this is $P(z_j) = y_j$ for $z_j \in S$. The divided difference $f[z_i, \ldots, z_{i+k}]$ is defined by the recurrence of the page: by $D(z_i, k)/k!$ if $z_i = z_{i+k}$, and by the quotient of differences otherwise.

**Lemma 1 (uniqueness).** If $P, Q \in \mathcal{P}_k$ both match the data on a block $S$ of $k + 1$ nodes, then $P = Q$.

*Proof.* $G = P - Q$ has $G^{(r)}(v) = 0$ for $r < \mu_S(v)$, so $(x - v)^{\mu_S(v)}$ divides $G$ for each $v$ in $S$. These factors are coprime, so their product, of degree $\sum_v \mu_S(v) = k + 1$, divides $G$. As $\deg G \le k$, $G = 0$. $\square$

**Lemma 2 (existence and leading coefficient).** For each block $S = (z_i, \ldots, z_{i+k})$ there is a polynomial $P_S \in \mathcal{P}_k$ that matches the data on $S$, and the coefficient of $x^k$ in $P_S$ is $f[z_i, \ldots, z_{i+k}]$.

*Proof.* By induction on $k$. For $k = 0$, $P_S = D(z_i, 0)$, of leading coefficient $f[z_i]$.

Let $k \ge 1$ and assume the claim for blocks of $k$ nodes. *Case 1: $z_i = z_{i+k}$.* Because equal nodes are adjacent, all nodes of $S$ equal $v = z_i$ and $\mu_S(v) = k + 1$. The Taylor polynomial $P_S(x) = \sum_{r=0}^{k} D(v, r)(x - v)^r / r!$ has $P_S^{(r)}(v) = D(v, r)$ for $r \le k$ and leading coefficient $D(v, k)/k! = f[z_i, \ldots, z_{i+k}]$.

*Case 2: $z_i \ne z_{i+k}$.* Let $Q$ match the data on $(z_i, \ldots, z_{i+k-1})$ and $R$ on $(z_{i+1}, \ldots, z_{i+k})$; they exist by the induction hypothesis, with leading coefficients $f[z_i, \ldots, z_{i+k-1}]$ and $f[z_{i+1}, \ldots, z_{i+k}]$. Put
$$P(x) = \frac{(x - z_i) R(x) - (x - z_{i+k}) Q(x)}{z_{i+k} - z_i}.$$
Then $P \in \mathcal{P}_k$, and its coefficient of $x^k$ is $(f[z_{i+1}, \ldots, z_{i+k}] - f[z_i, \ldots, z_{i+k-1}])/(z_{i+k} - z_i) = f[z_i, \ldots, z_{i+k}]$. By the Leibniz rule, for each $v$ and $r$,
$$(z_{i+k} - z_i)\, P^{(r)}(v) = (v - z_i) R^{(r)}(v) + r R^{(r-1)}(v) - (v - z_{i+k}) Q^{(r)}(v) - r Q^{(r-1)}(v),$$
where the terms with $r - 1$ are absent for $r = 0$. Fix $v$ in $S$ and $r < \mu_S(v)$.

- If $v \ne z_i$ and $v \ne z_{i+k}$, then $\mu_S(v)$ is also the multiplicity of $v$ in both smaller blocks, so $Q^{(s)}(v) = R^{(s)}(v) = D(v, s)$ for $s \le r$. The right side is $((v - z_i) - (v - z_{i+k})) D(v, r) = (z_{i+k} - z_i) D(v, r)$.
- If $v = z_i$, the block of $Q$ holds $v$ with multiplicity $\mu_S(v)$ and the block of $R$ with multiplicity $\mu_S(v) - 1$. The term $(v - z_i) R^{(r)}(v)$ is 0. Since $r - 1 < \mu_S(v) - 1$, $R^{(r-1)}(v) = D(v, r-1) = Q^{(r-1)}(v)$, so the two terms with $r$ cancel. The right side is $(z_{i+k} - z_i) Q^{(r)}(v) = (z_{i+k} - z_i) D(v, r)$.
- If $v = z_{i+k}$, the same argument with $Q$ and $R$ exchanged gives $(z_{i+k} - z_i) R^{(r)}(v) = (z_{i+k} - z_i) D(v, r)$.

So $P^{(r)}(v) = D(v, r)$ in all cases, and $P_S = P$ works. $\square$

**Lemma 3 (Newton form).** Let $p_k = P_{(z_0, \ldots, z_k)}$ and $\omega_k(x) = \prod_{l=0}^{k-1} (x - z_l)$. Then $p_n = \sum_{k=0}^{n} f[z_0, \ldots, z_k]\, \omega_k$.

*Proof.* For $k \ge 1$, $G = p_k - p_{k-1}$ lies in $\mathcal{P}_k$ and matches the zero data on $(z_0, \ldots, z_{k-1})$, since both terms match the same data there. As in Lemma 1, $\omega_k$, of degree $k$, divides $G$, so $G = \alpha \omega_k$ for a constant $\alpha$. Comparing the coefficients of $x^k$, $\alpha$ is the leading coefficient of $p_k$ (as $\deg p_{k-1} < k$), which is $f[z_0, \ldots, z_k]$ by Lemma 2. Summing $p_k - p_{k-1}$ from $k = 1$ to $n$ and adding $p_0 = f[z_0]$ gives the formula. $\square$

**Theorem.** NEWTON-COEFFICIENTS returns $c$ with $c[k] = f[z_0, \ldots, z_k]$ for $0 \le k \le n$, so by Lemma 3 the Newton form with these coefficients is the unique $p_n \in \mathcal{P}_n$ that matches the data. NEWTON-EVALUATE$(z, c, t)$ returns $\sum_{k=0}^{n} c[k]\, \omega_k(t)$. Both terminate after a fixed number of steps.

*Proof of the coefficient claim.* We use this invariant at the test of line L2, for $k = 1, \ldots, n + 1$:

> **(T)** $c[i] = f[z_{i-k+1}, \ldots, z_i]$ for $k - 1 \le i \le n$, and $c[i] = f[z_0, \ldots, z_i]$ for $0 \le i < k - 1$.

*Initialization.* For $k = 1$ line L1 gives $c[i] = y[i] = f[z_i]$ for all $i$, which is (T).

*Maintenance.* Assume (T) for $k \le n$. Pass $k$ visits $i = n, n - 1, \ldots, k$ in that order. When it visits $i$, the entries $c[i]$ and $c[i - 1]$ have not been changed in this pass, because the earlier visits wrote only to indices above $i$. As $i - 1 \ge k - 1$, (T) gives $c[i] = f[z_{i-k+1}, \ldots, z_i]$ and $c[i-1] = f[z_{i-k}, \ldots, z_{i-1}]$. If $z[i] = z[i-k]$, then all of $z_{i-k}, \ldots, z_i$ are equal (equal nodes are adjacent) and line L4 writes $D(z_i, k)/k! = f[z_{i-k}, \ldots, z_i]$. Otherwise line L5 writes $(f[z_{i-k+1}, \ldots, z_i] - f[z_{i-k}, \ldots, z_{i-1}])/(z_i - z_{i-k}) = f[z_{i-k}, \ldots, z_i]$. After the pass, $c[i] = f[z_{i-k}, \ldots, z_i]$ for $k \le i \le n$, which is the first part of (T) for $k + 1$. The entries with $i \le k - 1$ are unchanged; for $i = k - 1$ the old value is $f[z_0, \ldots, z_{k-1}]$, and for $i < k - 1$ it is $f[z_0, \ldots, z_i]$. This is the second part of (T) for $k + 1$.

*Termination.* The loops of lines L2 and L3 are counted loops with $n$ and $n - k + 1$ steps, so the procedure stops after $n(n+1)/2$ updates. At the exit $k = n + 1$, and (T) says $c[i] = f[z_0, \ldots, z_i]$ for all $0 \le i \le n$.

*Proof of the evaluation claim.* Let $q_k = \sum_{j=k}^{n} c[j] \prod_{l=k}^{j-1} (t - z_l)$. Before the loop of line L8, $p = c[n] = q_n$. If $p = q_{k+1}$ before the step with index $k$, line L9 gives $p = q_{k+1}(t - z_k) + c[k] = \sum_{j=k+1}^{n} c[j] \prod_{l=k}^{j-1}(t - z_l) + c[k] = q_k$. The loop runs $n$ times and ends with $p = q_0 = \sum_{j=0}^{n} c[j]\, \omega_j(t)$. $\blacksquare$

**Adding a node.** If $b_k = f[z_{n-k}, \ldots, z_n]$ for $k = 0, \ldots, n$ and $z_{n+1}$ differs from all nodes, the recurrence of the divided differences gives $b'_k = f[z_{n+1-k}, \ldots, z_{n+1}] = (b'_{k-1} - b_{k-1})/(z_{n+1} - z_{n+1-k})$ with $b'_0 = y_{n+1}$, and Lemma 3 for $n + 1$ nodes shows that the old coefficients stay and the new one is $b'_{n+1}$.
