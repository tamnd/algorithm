---
title: The product formula is exact, the modified Metropolis step keeps the conditional law invariant, and subset simulation stops
proves: [correctness, termination]
status: full
---

Let $\varphi$ be the standard normal density on $\mathbb{R}$ and $\pi(u) = \prod_{k=1}^{d} \varphi(u_k)$ the standard normal density on $\mathbb{R}^d$. For a threshold $b$ put $F = \{u : g(u) \le b\}$ with $\mathbb{P}[U \in F] > 0$, and let $\pi_F(u) = \pi(u) \mathbf{1}_F(u) / \mathbb{P}[U \in F]$ be the conditional density.

**Lemma 1 (product formula).** If $F_m \subseteq F_{m-1} \subseteq \cdots \subseteq F_1$ and $\mathbb{P}[F_j] > 0$ for all $j$, then $\mathbb{P}[F_m] = \mathbb{P}[F_1] \prod_{j=2}^{m} \mathbb{P}[F_j \mid F_{j-1}]$.

*Proof.* Since $F_j \subseteq F_{j-1}$, $F_j \cap F_{j-1} = F_j$, so $\mathbb{P}[F_j \mid F_{j-1}] = \mathbb{P}[F_j] / \mathbb{P}[F_{j-1}]$. The product telescopes to $\mathbb{P}[F_m]$. $\square$

The sets of the algorithm are nested because the thresholds decrease: $b_{j+1}$ is a quantile of samples that all satisfy $g \le b_j$ (Lemma 3), so $b_{j+1} \le b_j$.

**Lemma 2 (the one coordinate kernel).** Fix $w > 0$. The kernel $q$ on $\mathbb{R}$ that proposes $\xi = x + \text{Uniform}(-w, w)$, accepts with probability $\min(1, \varphi(\xi)/\varphi(x))$, and otherwise stays at $x$, satisfies detailed balance for $\varphi$: for measurable sets $A, B \subseteq \mathbb{R}$, $\int_A \varphi(x) q(x, B)\, dx = \int_B \varphi(y) q(y, A)\, dy$.

*Proof.* The proposal density $s(x, \xi) = \mathbf{1}[|\xi - x| < w] / (2w)$ is symmetric. For $x \neq y$ the moving part of the kernel has density $s(x, y) \min(1, \varphi(y)/\varphi(x))$, and $\varphi(x) s(x, y) \min(1, \varphi(y)/\varphi(x)) = s(x, y) \min(\varphi(x), \varphi(y))$, which is symmetric in $x$ and $y$. The part that stays at $x$ contributes $\int_{A \cap B} \varphi(x) r(x)\, dx$ to both sides, where $r(x)$ is the rejection probability. $\square$

**Lemma 3 (the modified Metropolis step).** Let $K$ be the kernel of MM-STEP: apply the kernel of Lemma 2 to each coordinate independently to get a candidate $c$, then move to $c$ if $c \in F$ and stay otherwise. Then $K$ satisfies detailed balance for $\pi_F$, so $\pi_F$ is stationary for $K$. Every state of a chain started in $F$ lies in $F$.

*Proof.* The candidate kernel $Q(u, dc) = \prod_k q(u_k, dc_k)$ is a product of kernels that are reversible for $\varphi$, so $Q$ is reversible for $\pi$: for product sets $A = \prod A_k$ and $B = \prod B_k$, $\int_A \pi(u) Q(u, B)\, du = \prod_k \int_{A_k} \varphi q(\cdot, B_k) = \prod_k \int_{B_k} \varphi q(\cdot, A_k) = \int_B \pi(c) Q(c, A)\, dc$, and product sets determine the measures. Now $K(u, B) = Q(u, B \cap F) + \mathbf{1}_B(u) Q(u, F^c)$. For measurable $A, B \subseteq F$,

$$\int_A \pi_F(u) K(u, B)\, du = \frac{1}{\mathbb{P}[F]} \Big( \int_A \pi(u) Q(u, B)\, du + \int_{A \cap B} \pi(u) Q(u, F^c)\, du \Big),$$

since $B \cap F = B$. The first term is symmetric in $A$ and $B$ by the reversibility of $Q$, and the second is symmetric because it depends only on $A \cap B$. So $K$ is reversible for $\pi_F$ on $F$, and integrating over $B = F$ gives stationarity. A move goes only to a candidate in $F$, so a chain that starts in $F$ stays in $F$. $\square$

**Corollary.** If a seed $u$ has law $\pi_F$, then every state of its chain has law $\pi_F$, by induction with Lemma 3. The states of one chain are dependent, but each one has the correct marginal law. So the fraction of chain states with $g \le b'$ estimates $\mathbb{P}[g(U) \le b' \mid U \in F]$, with an error that depends on the correlation of the chain.

In the algorithm, the seeds of level $j + 1$ are the samples of level $j$ with $g \le b_j$. If the samples of level $j$ have law $\pi_{F_{j-1}}$ and $b_j$ were fixed in advance, each such seed would have law $\pi_{F_j}$, and the corollary would apply. Because $b_j$ is a sample quantile of the same samples, this holds only approximately; that is the source of the $O(1/N)$ bias that Au and Beck describe, which is not proved here.

**Theorem.** SUBSET-SIMULATION stops after at most max_levels levels and at most $N + (N - p_0 N) \cdot \text{max\_levels}$ calls of $g$. When it returns, the thresholds are nonincreasing, the last threshold is 0, and the estimate is the product of the recorded factors. With fixed nested thresholds, the product of the exact factors is $\mathbb{P}[g(U) \le 0]$, and each chain state of level $j + 1$ has the law $\pi_{F_j}$ when its seed does.

*Proof.* Each level does finitely many steps: a sort, and $p_0 N$ chains of $1/p_0 - 1$ steps, each with at most one call of $g$. The loop runs at most max_levels times, then returns or raises an error. Level 1 makes $N$ calls and each later level at most $N - p_0 N$. The thresholds are nonincreasing as shown after Lemma 1; the returned factors are $p_0$ for each recorded level and the failure fraction for the last. The product statement is Lemma 1, and the law of the chain states is the corollary of Lemma 3. $\blacksquare$

The theorem does not bound the error of one run. The c.o.v. formula of Au and Beck needs the correlation factors of the chains and an assumption that the chains mix over all of $F_j$. If $F_j$ has parts that no seed reaches, the chains never sample them, and the estimate is too small.
