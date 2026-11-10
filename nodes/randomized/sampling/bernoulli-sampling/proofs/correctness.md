---
title: Geometric skips give exactly the law of Bernoulli sampling
proves: [correctness, termination, time.expected]
status: full
---

Let $0 < p < 1$ and $q = 1 - p$. Bernoulli sampling with rate $p$ on positions $0, \ldots, n-1$ is the random set $S$ with

$$\Pr[S = A] = p^{|A|} q^{\,n - |A|} \quad \text{for each } A \subseteq \{0, \ldots, n-1\}. \tag{B}$$

This is the same as saying that the events $\{i \in S\}$ are independent, each with probability $p$: the product of the $n$ factors $p$ or $q$ is (B).

**Lemma 1 (GEOMETRIC).** If $U$ is uniform on $(0, 1]$, then $G = \lfloor \ln U / \ln q \rfloor$ satisfies $\Pr[G = g] = q^g p$ for each integer $g \ge 0$.

*Proof.* Since $\ln U \le 0$ and $\ln q < 0$, the ratio is at least 0, so $G \ge 0$. For an integer $g \ge 0$, $G \ge g$ holds if and only if $\ln U / \ln q \ge g$, that is $\ln U \le g \ln q$ (we multiplied by the negative number $\ln q$), that is $U \le q^g$. So $\Pr[G \ge g] = q^g$, and $\Pr[G = g] = q^g - q^{g+1} = q^g p$. $\square$

**Theorem.** Let the calls of line L3 return independent values $G_1, G_2, \ldots$, each with $\Pr[G_j = g] = q^g p$. Then BERNOULLI-SAMPLE stops with probability 1, and the set $S$ that it returns satisfies (B).

*Proof.* Termination. Each call gives $G_j \ge 0$, so line L4 raises $i$ by at least 1. After at most $n + 1$ calls, $i \ge n$, and line L5 returns. So the loop stops after at most $n + 1$ iterations on every run, not only with probability 1.

The law. Write $i_0 = -1$ and $i_j = i_{j-1} + G_j + 1$. Line L6 adds $i_j$ to $S$ while $i_j < n$, and line L5 stops at the first $j$ with $i_j \ge n$. So $S = \{i_1, \ldots, i_k\}$, where $k$ is the number of $j$ with $i_j < n$. The values $i_j$ strictly increase, so the run is determined by the set $S$ and the last step.

Fix $A = \{a_1 < a_2 < \cdots < a_k\} \subseteq \{0, \ldots, n-1\}$, and write $a_0 = -1$. The event $S = A$ happens if and only if $G_j = a_j - a_{j-1} - 1$ for $j = 1, \ldots, k$, and then $G_{k+1} \ge n - 1 - a_k$, so that $i_{k+1} = a_k + G_{k+1} + 1 \ge n$. Each $a_j - a_{j-1} - 1 \ge 0$, so these are legal values. By independence,

$$\Pr[S = A] = \prod_{j=1}^{k} q^{a_j - a_{j-1} - 1} p \cdot \Pr[G_{k+1} \ge n - 1 - a_k] = p^k\, q^{\sum_{j=1}^{k} (a_j - a_{j-1} - 1)} \cdot q^{\,n - 1 - a_k}.$$

Here we used $\Pr[G \ge g] = q^g$ from the proof of Lemma 1, with $g = n - 1 - a_k \ge 0$. The sum telescopes: $\sum_{j=1}^{k} (a_j - a_{j-1} - 1) = a_k - a_0 - k = a_k + 1 - k$. So the exponent of $q$ is $(a_k + 1 - k) + (n - 1 - a_k) = n - k$, and $\Pr[S = A] = p^k q^{n-k}$, which is (B). The case $k = 0$ is the same computation with an empty product: $S = \emptyset$ exactly when $G_1 \ge n$, with probability $q^n$. $\square$

**Expected time.** The loop runs $|S| + 1$ times: once for each kept position and once for the step that stops. So the expected number of iterations is $\mathbb{E}|S| + 1 = np + 1$, by linearity of expectation over the $n$ positions. Each iteration takes $O(1)$ time with one uniform real. $\blacksquare$

**The direct method.** For a rational $p = a/b$, BERNOULLI-SAMPLE-DIRECT keeps position $i$ when an independent uniform integer $t_i \in \{0, \ldots, b-1\}$ is below $a$. This has probability exactly $a/b$, and the $n$ tests use independent draws, so the events $\{i \in S\}$ are independent with probability $p$ each. That is (B), with no rounding.

**Floating point.** Lemma 1 needs a uniform real and exact logarithms. In floating point, $U$ lies on a grid (multiples of $2^{-53}$ for the usual generators) and the logarithms round. So each skip has the law of Lemma 1 only up to errors of the order of the grid spacing and of the rounding near the integer boundaries of the floor. In particular $U \ge 2^{-53}$, so $G \le 53 \ln 2 / (-\ln q)$: longer skips, which have probability about $2^{-53}$, never occur.
