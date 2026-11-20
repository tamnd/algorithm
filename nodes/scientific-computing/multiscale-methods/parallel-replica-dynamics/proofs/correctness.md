---
title: Why the parallel stage gives the law of a serial escape
proves: [correctness]
status: full
---

We prove the claim for a discrete-time Markov chain, as in the implementation. The proof has an exact part, for replicas that start from the quasi-stationary distribution of the basin, and an approximate part, which is the error of the dephasing and decorrelation stages.

**Setting.** $(X_n)$ is a Markov chain with time step $h$. $W$ is the current basin, and $\tau = \min\{n \ge 1 : X_n \notin W\}$ is the exit step. A probability measure $\nu$ on $W$ is a *quasi-stationary distribution* (QSD) if, for $X_0 \sim \nu$, the law of $X_1$ given $\tau > 1$ is again $\nu$. Write $p = P_\nu(\tau = 1)$.

**Lemma 1 (exit from the QSD).** If $X_0 \sim \nu$, then for every $n \ge 1$ and every set $B$ outside $W$,
$$P_\nu(\tau = n,\ X_\tau \in B) = (1 - p)^{n-1}\, P_\nu(\tau = 1,\ X_1 \in B).$$
So $\tau$ is geometric with parameter $p$, and the exit point $X_\tau$ is independent of $\tau$.

*Proof.* By induction on $n$. The case $n = 1$ is trivial. For $n \ge 2$, by the Markov property at time 1,
$P_\nu(\tau = n, X_\tau \in B) = P_\nu(\tau > 1)\, P_{\mu}(\tau = n - 1, X_\tau \in B)$, where $\mu$ is the law of $X_1$ given $\tau > 1$. By the definition of the QSD, $\mu = \nu$, and $P_\nu(\tau > 1) = 1 - p$. The induction hypothesis gives the claim. The right side is a product of a function of $n$ and a function of $B$, which is the independence. $\square$

**Lemma 2 (the parallel stage).** Let $Y^1, \ldots, Y^m$ be independent copies of the chain, each started from $\nu$, with exit steps $\tau_1, \ldots, \tau_m$. Let $w = \min_j \tau_j$, let $J$ be the smallest $j$ with $\tau_j = w$, and let $N = m (w - 1) + J$. Then $N$ is geometric with parameter $p$, and $Y^J_w$ has the law of $X_\tau$ under $P_\nu$, independent of $N$. This is the content of lines L6 to L9.

*Proof.* Fix $n = m (w - 1) + j$ with $1 \le j \le m$. The event $\{N = n, Y^J_w \in B\}$ says: replicas $1, \ldots, j - 1$ have $\tau_i > w$, replica $j$ has $\tau_j = w$ and exits into $B$, and replicas $j + 1, \ldots, m$ have $\tau_i > w - 1$. By independence and Lemma 1, the probability is
$$(1-p)^{w (j-1)} \cdot (1-p)^{w-1} P_\nu(\tau = 1, X_1 \in B) \cdot (1-p)^{(w-1)(m-j)}.$$
The exponent of $1 - p$ is $w (j - 1) + (w - 1) + (w - 1)(m - j) = m (w - 1) + j - 1 = n - 1$. So the probability is $(1-p)^{n-1} P_\nu(\tau = 1, X_1 \in B)$, the same as Lemma 1 with $n$ in place of the serial exit step. $\square$

The proof shows why the accounting $m (w - 1) + j$ is exact: it orders the trials of the replicas as (step, replica) and counts the trials up to the first success, and independent geometric trials in any fixed order give a geometric count. The accounting $m w$ is not exact for discrete steps: it makes the time a multiple of $m$.

**Theorem.** Suppose that each dephased replica of line L5 has the law $\nu$, and that the trajectory at the end of the decorrelation stage of lines L3 and L4 has the law $\nu$. Then the clock increment and the next state of the parallel stage have the same joint law as the exit step and the exit point of one serial trajectory from the same point. Because the decorrelation stage is a serial run, the whole output (the times and the sequence of states) has the law of a serial run of the chain.

*Proof.* The decorrelation stage is the serial chain itself. At its end, by hypothesis the state has the law $\nu$, and by Lemma 1 the remaining serial exit is geometric with parameter $p$ and independent of the exit point. Lemma 2 gives the same joint law for the parallel stage. $\blacksquare$

**The exact case.** If the escape probability from each point of $W$ is the same number $p$ and the law of the exit point does not depend on the point, every probability measure on $W$ is a QSD with the same $p$, and the theorem holds with no approximation. This is the chain of the first two tests.

**What is approximate.** For a real dynamics the hypotheses hold only in the limit. Line L5 restarts a replica that leaves, so each dephased replica has the law of $X_{n_{\mathrm{corr}}}$ given $\tau > n_{\mathrm{corr}}$ for the chain started at the current point. If the chain killed outside $W$ is reversible with a spectral gap, this law converges to the QSD at the rate $(\lambda_2 / \lambda_1)^{n_{\mathrm{corr}}}$, where $\lambda_1 > |\lambda_2|$ are the two largest eigenvalues of the killed chain (Le Bris, Lelievre, Luskin and Perez 2012, in continuous time). The same holds for the end of the decorrelation stage. So the error in law of each transition is of order $(\lambda_2 / \lambda_1)^{n_{\mathrm{corr}}}$. For a deep basin the convergence is fast compared with the escape, and the error is small.

**What is not proved.** The theorem says nothing about the speedup. The elapsed time with $m$ processors is the decorrelation time, plus the longest dephasing, plus $w$ parallel steps, and only the last part is divided by $m$. The speedup of a run is a measurement.
