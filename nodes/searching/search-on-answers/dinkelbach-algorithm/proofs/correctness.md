---
title: Dinkelbach's algorithm returns an optimal ratio after finitely many and, for integer data, O(log U) iterations
proves: [correctness]
status: full
---

We use the pseudocode of the page. $X$ is a finite set, $N, D : X \to \mathbb{R}$ with $D > 0$ on $X$, $\lambda^* = \min_{x \in X} N(x)/D(x)$, and $F(\lambda) = \min_{x \in X} (N(x) - \lambda D(x))$. The oracle of line L4 returns a minimizer of $N - \lambda D$. Write $x_0, x_1, \ldots$ for the successive values of $x$, $\lambda_k = N(x_k)/D(x_k)$, $D_k = D(x_k)$, and $F_k = F(\lambda_k) = N(x_{k+1}) - \lambda_k D_{k+1}$, where $x_{k+1}$ is the point returned at line L4 in round $k$.

**Lemma 1 (Dinkelbach).** $F(\lambda) \ge 0$ if and only if $\lambda \le \lambda^*$, and $F(\lambda^*) = 0$.

*Proof.* $N(x) - \lambda D(x) = D(x)\big(N(x)/D(x) - \lambda\big)$ with $D(x) > 0$. If $\lambda \le \lambda^*$, each term is $\ge 0$, so $F(\lambda) \ge 0$. If $\lambda > \lambda^*$, an optimal $x^*$ gives a negative term, so $F(\lambda) < 0$. At $\lambda^*$ the optimal $x^*$ gives $0$. $\square$

**Claim 1 (correctness and finiteness).** The algorithm stops, and it returns $x_k$ with $\lambda_k = \lambda^*$.

*Proof.* In round $k$, $F_k \le N(x_k) - \lambda_k D_k = 0$, since $x_k$ is one of the candidates. If line L5 finds $F_k \ge 0$, then $F_k = 0 = F(\lambda_k)$, so $\lambda_k \le \lambda^*$ by Lemma 1. Also $\lambda_k \ge \lambda^*$ because it is the ratio of a feasible point. So $\lambda_k = \lambda^*$ and $x_k$ is optimal. Otherwise $F_k < 0$, that is $N(x_{k+1}) < \lambda_k D_{k+1}$, so $\lambda_{k+1} < \lambda_k$. The ratios strictly decrease, so no point of $X$ appears twice, and the algorithm stops after at most $|X|$ rounds. $\square$

**Lemma 2 (monotone denominators).** If $y$ minimizes $N - \mu D$ and $z$ minimizes $N - \nu D$ with $\mu < \nu$, then $D(y) \le D(z)$.

*Proof.* By the two minimalities, $N(y) - \mu D(y) \le N(z) - \mu D(z)$ and $N(z) - \nu D(z) \le N(y) - \nu D(y)$. Adding and cancelling $N(y) + N(z)$ gives $(\nu - \mu) D(y) \le (\nu - \mu) D(z)$. $\square$

For $k \ge 1$, $x_k$ minimizes at $\lambda_{k-1}$ and $x_{k+1}$ minimizes at $\lambda_k < \lambda_{k-1}$, so $D_{k+1} \le D_k$: the denominators do not increase from round 1 on.

**Claim 2 (the halving step).** For every round $k \ge 1$ in which the algorithm does not stop,

$$\frac{|F_k|}{|F_{k-1}|} + \frac{D_{k+1}}{D_k} \le 1.$$

*Proof.* Since $x_k$ minimizes $N - \lambda_{k-1} D$, its value is at most the value of $x_{k+1}$: $F_{k-1} = N(x_k) - \lambda_{k-1} D_k \le N(x_{k+1}) - \lambda_{k-1} D_{k+1}$. Hence

$$F_k = N(x_{k+1}) - \lambda_k D_{k+1} \ge F_{k-1} + (\lambda_{k-1} - \lambda_k) D_{k+1}.$$

From $F_{k-1} = N(x_k) - \lambda_{k-1} D_k = D_k(\lambda_k - \lambda_{k-1})$ we get $\lambda_{k-1} - \lambda_k = |F_{k-1}|/D_k$. With $F_k, F_{k-1} < 0$ the inequality reads $-|F_k| \ge -|F_{k-1}| + |F_{k-1}| D_{k+1}/D_k$, which is the claim after division by $|F_{k-1}|$. $\square$

So in each such round, $|F|$ drops to at most half, or $D$ drops to at most half, because both ratios cannot exceed $1/2$.

**Claim 3 (integer data).** If $N$ and $D$ take integer values with $|N(x)| \le U$ and $1 \le D(x) \le U$, with $U \ge 2$, the algorithm makes $O(\log U)$ rounds.

*Proof.* While the algorithm runs, $F_k = (N(x_{k+1}) D_k - N(x_k) D_{k+1})/D_k$ has a non-zero integer numerator, so $|F_k| \ge 1/D_k \ge 1/U$. Also $|F_k| \le |N(x_{k+1})| + |\lambda_k| D_{k+1} \le U + U \cdot U \le 2U^2$. So among the rounds $k \ge 1$, the value $|F_k|$ can halve at most $\lg(2U^2 \cdot U) = 1 + 3 \lg U$ times. By Lemma 2, $D_k$ is non-increasing from $k = 1$ and lies in $[1, U]$, so it can halve at most $\lg U$ times. By Claim 2, each round $k \ge 1$ before the last does one of the two. With the first round and the last round, the number of rounds is at most $4 \lg U + 3$. $\square$
