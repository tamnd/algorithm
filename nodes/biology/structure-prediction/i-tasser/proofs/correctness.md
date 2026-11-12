---
title: Replica exchange keeps the Boltzmann distributions, and SPICKER partitions the decoys
proves: [correctness]
status: full
---

We use the pseudocode of the page. The state space $\Omega$ is finite, $E : \Omega \to \mathbb{R}$, and $0 < T_1 < \cdots < T_R$. Write $\beta_r = 1/T_r$ and $\pi_r(x) = e^{-\beta_r E(x)} / Z_r$ with $Z_r = \sum_{y} e^{-\beta_r E(y)}$. The proposal $q(x, y)$ of a local move is symmetric: $q(x, y) = q(y, x)$. The joint state is $\mathbf{x} = (x_1, \ldots, x_R)$, and the target joint distribution is $\Pi(\mathbf{x}) = \prod_r \pi_r(x_r)$.

A Markov kernel $K$ satisfies *detailed balance* for a distribution $\mu$ if $\mu(u) K(u, v) = \mu(v) K(v, u)$ for all $u \ne v$. Summing over $u$ shows that then $\mu K = \mu$, so $\mu$ is stationary.

**Lemma 1 (the Metropolis move).** The kernel of line L9 for replica $r$, $K_r(x, y) = q(x, y) \min(1, e^{-\beta_r (E(y) - E(x))})$ for $y \ne x$, satisfies detailed balance for $\pi_r$.

*Proof.* For $x \ne y$,

$$\pi_r(x) K_r(x, y) = \frac{q(x, y)}{Z_r} \min\big(e^{-\beta_r E(x)}, e^{-\beta_r E(y)}\big),$$

because $e^{-\beta_r E(x)} \min(1, e^{-\beta_r(E(y) - E(x))}) = \min(e^{-\beta_r E(x)}, e^{-\beta_r E(y)})$. The right side is symmetric in $x$ and $y$, since $q$ is symmetric. $\square$

Moving replica $r$ alone, with the other replicas fixed, is a kernel on joint states that changes only coordinate $r$. Its detailed balance for $\Pi$ follows from Lemma 1, because $\Pi(\mathbf{x}) = \pi_r(x_r) \cdot \prod_{s \ne r} \pi_s(x_s)$ and the second factor is the same on both sides. So line L9, a product of such kernels, keeps $\Pi$ stationary.

**Lemma 2 (the swap move).** Let $\mathbf{x}'$ be $\mathbf{x}$ with the states of replicas $r$ and $r + 1$ exchanged, and let the swap be accepted with probability $\alpha(\mathbf{x}) = \min(1, e^{\Delta})$, $\Delta = (\beta_r - \beta_{r+1})(E(x_r) - E(x_{r+1}))$. Then $\Pi(\mathbf{x})\, \alpha(\mathbf{x}) = \Pi(\mathbf{x}')\, \alpha(\mathbf{x}')$.

*Proof.* Only the factors of replicas $r$ and $r + 1$ change, so

$$\frac{\Pi(\mathbf{x}')}{\Pi(\mathbf{x})} = \frac{e^{-\beta_r E(x_{r+1}) - \beta_{r+1} E(x_r)}}{e^{-\beta_r E(x_r) - \beta_{r+1} E(x_{r+1})}} = e^{(\beta_r - \beta_{r+1})(E(x_r) - E(x_{r+1}))} = e^{\Delta}.$$

For $\mathbf{x}'$ the exponent is $-\Delta$. If $\Delta \ge 0$, then $\alpha(\mathbf{x}) = 1$ and $\alpha(\mathbf{x}') = e^{-\Delta}$, and $\Pi(\mathbf{x}) \cdot 1 = \Pi(\mathbf{x}') e^{-\Delta}$. If $\Delta < 0$, the same holds with the roles exchanged. $\square$

Line L10 picks the pair $r$ uniformly at random, and the move from $\mathbf{x}'$ back to $\mathbf{x}$ uses the same pair with the same probability, so the swap kernel satisfies detailed balance for $\Pi$ by Lemma 2.

**Theorem 1.** $\Pi$ is a stationary distribution of one sweep, lines L9 and L10. If the chain of sweeps is irreducible and aperiodic on $\Omega^R$, then for every replica $r$ and every $x \in \Omega$, the fraction of sweeps in which replica $r$ is in state $x$ tends to $\pi_r(x)$ with probability 1.

*Proof.* Each part of a sweep keeps $\Pi$ stationary (Lemmas 1 and 2), and a composition of kernels that keep $\Pi$ stationary keeps it stationary. For a finite irreducible aperiodic chain, the stationary distribution is unique, and the ergodic theorem for Markov chains gives the convergence of the visit frequencies of joint states to $\Pi$. The marginal of $\Pi$ on coordinate $r$ is $\pi_r$. $\square$

Irreducibility needs the local moves to connect $\Omega$. Aperiodicity holds as soon as some move can be rejected or the proposal can stay, which is the case for any nonconstant $E$ with a Metropolis rule.

**Theorem 2 (SPICKER).** For any finite list of $d$ decoys, any distance with $\mathrm{dist}(x, x) = 0$, and any cutoff $\delta \ge 0$, lines L12 to L14 stop after at most $d$ rounds, the clusters are disjoint and cover all decoys, and the center $c$ of each round has the largest number of neighbours within $\delta$ among the decoys left in that round.

*Proof.* In each round the center is a neighbour of itself, since $\mathrm{dist}(c, c) = 0 \le \delta$, so each round removes at least one decoy, and there are at most $d$ rounds. A round outputs only decoys still in $D$ and removes them, so no decoy is in two clusters. The loop stops only when $D$ is empty, so every decoy is in some cluster. The maximality of the center is the choice of line L13. $\square$

The rule is greedy, so it does not maximize any global measure of the clustering. The page example shows a decoy that loses its only neighbour to an earlier cluster and ends alone.
