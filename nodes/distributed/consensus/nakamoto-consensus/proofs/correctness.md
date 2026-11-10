---
title: The probability that an attacker reverses a block z deep
proves: [correctness]
status: full
---

This proof covers the double-spend bound of the Bitcoin white paper. It does not prove the common prefix, chain quality and chain growth properties, which need a different argument (Garay, Kiayias and Leonardos, 2015).

**Model.** All blocks have the same target. Each new block anywhere in the network is the attacker's with probability $q$ and an honest miner's with probability $p = 1 - q$, independently of all other blocks. This holds if the attacker controls a share $q$ of the hash power and every hash succeeds with the same small probability, since the next successful hash is then the attacker's with probability $q$. The attacker's *deficit* is the number of blocks by which the honest chain is ahead of the attacker's private chain. An honest block raises it by 1, and an attacker's block lowers it by 1. The attacker *catches up* when the deficit reaches 0; then it can publish a chain at least as long, and in the paper's model this counts as success.

**Lemma 1 (gambler's ruin with two barriers).** Let $0 \le z \le N$, and let $a_z$ be the probability that the deficit, started at $z$, reaches 0 before it reaches $N$. Let $r = q/p$. Then

$$a_z = \frac{r^z - r^N}{1 - r^N} \quad (r \ne 1), \qquad a_z = 1 - \frac{z}{N} \quad (r = 1).$$

*Proof.* The walk reaches 0 or $N$ with probability 1, since from any state it gets to $N$ within $N$ steps with probability at least $p^N > 0$. Conditioning on the first block gives, for $0 < z < N$,

$$a_z = p\, a_{z+1} + q\, a_{z-1}, \qquad a_0 = 1, \quad a_N = 0.$$

The characteristic equation $p x^2 - x + q = 0$ has the roots $1$ and $q/p = r$, because $p + q = 1$. If $r \ne 1$, every solution of the recurrence is $a_z = A + B r^z$; the boundary conditions give $A + B = 1$ and $A + B r^N = 0$, so $B = 1/(1 - r^N)$ and $A = -r^N/(1 - r^N)$, which is the formula. If $r = 1$, the roots coincide and $a_z = A + Bz$, with $A = 1$ and $B = -1/N$. A recurrence of second order with two boundary values has one solution, so these are the probabilities. $\square$

**Lemma 2 (catch-up from $z$ behind).** The probability $q_z$ that the deficit, started at $z \ge 0$, ever reaches 0 is $1$ if $p \le q$ and $(q/p)^z$ if $p > q$.

*Proof.* Let $E_N$ be the event that the deficit reaches 0 before $N$. The event "the deficit ever reaches 0" is the union of the $E_N$ over $N > z$: if it reaches 0 at some finite step, the largest deficit before that step is some finite $M$, and the event $E_{M+1}$ holds. The events grow with $N$, so by continuity of probability $q_z = \lim_{N \to \infty} a_z$. If $p > q$ then $r < 1$, $r^N \to 0$ and $a_z \to r^z$. If $p < q$ then $r > 1$, and dividing by $r^N$ gives $a_z = (r^{z-N} - 1)/(r^{-N} - 1) \to 1$. If $p = q$ then $a_z = 1 - z/N \to 1$. $\square$

**Theorem (the white paper's formula).** Suppose the attacker starts mining a private chain when the payment is sent, and the merchant waits until the honest chain has $z$ blocks after the payment's block. If the attacker's progress $k$ at that moment is Poisson with mean $\lambda = z q/p$, then the attacker eventually catches up with probability

$$P(q, z) = 1 - \sum_{k=0}^{z} \frac{\lambda^k e^{-\lambda}}{k!}\left(1 - (q/p)^{z-k}\right) \qquad (p > q).$$

*Proof.* Given $k$, the deficit is $z - k$. If $k \ge z$, the attacker has already caught up, and the success probability is 1. If $k < z$, by the independence of later blocks and Lemma 2, it is $(q/p)^{z-k}$. Summing over $k$ with weights $\pi_k = \lambda^k e^{-\lambda}/k!$:

$$P = \sum_{k > z} \pi_k + \sum_{k=0}^{z} \pi_k (q/p)^{z-k} = 1 - \sum_{k=0}^{z} \pi_k + \sum_{k=0}^{z} \pi_k (q/p)^{z-k},$$

which is the formula. The term $k = z$ is zero, since $(q/p)^0 = 1$. $\square$

**Why the mean is $z q/p$.** While the honest miners find $z$ blocks, each block is honest with probability $p$, so the number $k$ of attacker blocks before the $z$-th honest one has the negative binomial law $\Pr[k] = \binom{k+z-1}{k} p^z q^k$, with mean $z q/p$. The white paper replaces it by a Poisson law with the same mean. Using the exact law in the proof above gives

$$P_{\text{exact}}(q, z) = 1 - \sum_{k=0}^{z} \binom{k+z-1}{k} p^z q^k \left(1 - (q/p)^{z-k}\right),$$

which differs from $P$ by a small factor; for $q = 0.1$ and $z = 1$ it is $0.9 \cdot \frac{1}{9} + 0.1 = 0.2$, against $0.2045873$. The tests check both formulas against seeded simulations of their models.

**Exponential decay.** For $p > q$, $P(q, z) \le \Pr[k \ge z/2] + (q/p)^{z/2}$, by splitting on whether $k$ is below $z/2$. The mean of $k$ is $zq/p$, which is less than $z/2$ when $q < 1/3$, so a [Chernoff bound](/chernoff-bound/) makes the first term exponentially small in $z$; for $1/3 \le q < 1/2$, split at $z(q/p + 1)/2$ instead, which lies strictly between the mean and $z$. Either way $P(q, z)$ falls exponentially in $z$.

**What the model leaves out.** Network delay, which lets honest miners waste work on forks; changes in difficulty; an attacker that prepares blocks before the payment; and attacks on the incentives, such as selfish mining. The bounds of Garay, Kiayias and Leonardos cover the first and the adversary's full freedom in a synchronous model, at the cost of a margin on the honest majority.
