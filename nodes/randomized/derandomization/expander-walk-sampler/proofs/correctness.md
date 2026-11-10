---
title: The hitting property of expander walks and the expander mixing lemma
proves: [correctness]
status: full
---

We use the notation of the page. $G$ is a $d$-regular undirected multigraph on the vertex set $V$, $|V| = N$, with adjacency matrix $A$ and walk matrix $M = A/d$. $M$ is real and symmetric, so by the [spectral theorem](/spectral-theorem/) it has an orthonormal basis of eigenvectors with real eigenvalues $1 = \lambda_1 \ge \lambda_2 \ge \cdots \ge \lambda_N \ge -1$, and $\lambda = \max(|\lambda_2|, |\lambda_N|)$. The vector $\mathbf{1}$ has all entries 1, and $M\mathbf{1} = \mathbf{1}$ because $G$ is $d$-regular. $J = \frac{1}{N}\mathbf{1}\mathbf{1}^\top$ is the walk matrix of the complete graph with loops. $\|x\|$ is the Euclidean norm and $\|X\| = \max_{x \ne 0} \|Xx\|/\|x\|$ the operator norm. For a set $B \subseteq V$ of density $\mu = |B|/N$, $P$ is the diagonal matrix with $P_{vv} = 1$ for $v \in B$ and 0 otherwise.

**Lemma 1 (spectral bound on $\mathbf{1}^\perp$).** For every $x \perp \mathbf{1}$, $Mx \perp \mathbf{1}$ and $\|Mx\| \le \lambda \|x\|$.

*Proof.* We may take $\mathbf{1}/\sqrt{N}$ as the first vector of the orthonormal eigenbasis $u_1, \ldots, u_N$. Write $x = \sum_{i \ge 2} c_i u_i$. Then $Mx = \sum_{i \ge 2} \lambda_i c_i u_i$, which is orthogonal to $u_1$, and $\|Mx\|^2 = \sum_{i \ge 2} \lambda_i^2 c_i^2 \le \lambda^2 \|x\|^2$. $\square$

**Lemma 2 (decomposition).** $M = (1 - \lambda) J + \lambda E$ for a symmetric matrix $E$ with $\|E\| \le 1$.

*Proof.* If $\lambda = 0$, Lemma 1 gives $Mx = 0$ for $x \perp \mathbf{1}$, so $M = J$, and $E = 0$ works. Otherwise let $E = (M - (1 - \lambda)J)/\lambda$, which is symmetric. On $\mathbf{1}$: $M\mathbf{1} = J\mathbf{1} = \mathbf{1}$, so $E\mathbf{1} = \mathbf{1}$. On $x \perp \mathbf{1}$: $Jx = 0$, so $Ex = Mx/\lambda$, which is orthogonal to $\mathbf{1}$ with norm at most $\|x\|$ by Lemma 1. For a general $z = c\mathbf{1} + x$ with $x \perp \mathbf{1}$, the two parts of $Ez = c\mathbf{1} + Ex$ are orthogonal, so $\|Ez\|^2 = c^2 N + \|Ex\|^2 \le c^2 N + \|x\|^2 = \|z\|^2$. $\square$

**Lemma 3 (one step inside $B$).** $\|PMP\| \le \mu + \lambda(1 - \mu)$.

*Proof.* By Lemma 2 and the triangle inequality, $\|PMP\| \le (1 - \lambda)\|PJP\| + \lambda\|PEP\|$. Since $\|P\| \le 1$, $\|PEP\| \le \|E\| \le 1$. The matrix $PJP = \frac{1}{N}(P\mathbf{1})(P\mathbf{1})^\top$ has rank one, so its norm is $\frac{1}{N}\|P\mathbf{1}\|^2 = \frac{|B|}{N} = \mu$. So $\|PMP\| \le (1 - \lambda)\mu + \lambda = \mu + \lambda(1 - \mu)$. $\square$

**Theorem (hitting property).** Let $v_1$ be uniform on $V$ and let $v_{i+1}$ be a uniform random neighbour of $v_i$ (one of the $d$ edge slots of $v_i$, uniformly) for $i = 1, \ldots, t - 1$. Then

$$\Pr[v_1 \in B, \ldots, v_t \in B] \le \mu \big(\mu + \lambda(1 - \mu)\big)^{t-1}.$$

*Proof.* Let $\pi = \frac{1}{N}\mathbf{1}$ be the distribution of $v_1$. Let $q_i$ be the vector with $q_i(v) = \Pr[v_1, \ldots, v_i \in B,\ v_i = v]$. Then $q_1 = P\pi$, and $q_{i+1} = P M q_i$, because the walk moves from $v_i$ to $v_{i+1}$ with the transition probabilities $M_{v_{i+1} v_i}$ (symmetric), and $P$ removes the paths that leave $B$. Since $P^2 = P$, we get $q_t = (PMP)^{t-1} P\pi$, and the probability is

$$\mathbf{1}^\top q_t = (P\mathbf{1})^\top (PMP)^{t-1} (P\pi),$$

using $q_t = P q_t$. By Cauchy-Schwarz and Lemma 3,

$$\mathbf{1}^\top q_t \le \|P\mathbf{1}\| \cdot \|PMP\|^{t-1} \cdot \|P\pi\| = \sqrt{\mu N} \cdot \big(\mu + \lambda(1 - \mu)\big)^{t-1} \cdot \frac{\sqrt{\mu N}}{N} = \mu\big(\mu + \lambda(1 - \mu)\big)^{t-1}. \quad \square$$

**Corollary (correctness of EXPANDER-WALK-AMPLIFY).** Let $\mathcal{A}$ be an RP algorithm with $m$ random bits, and let $G$ have $N = 2^m$ vertices, one for each random string.

1. If the input $w$ is not in the language, the algorithm rejects with probability 1.
2. If $w$ is in the language, it rejects with probability at most $\frac{1}{2}\big(\frac{1 + \lambda}{2}\big)^{t-1}$.

*Proof.* (1) Line L6 accepts only if $\mathcal{A}(w, v_i)$ accepts for some $i$, and $\mathcal{A}$ never accepts an input outside the language. (2) Let $B$ be the set of random strings on which $\mathcal{A}$ rejects $w$. It does not depend on the walk, and $\mu = |B|/N \le 1/2$. The algorithm rejects exactly when $v_1, \ldots, v_t \in B$. By the theorem, this has probability at most $\mu(\mu + \lambda(1 - \mu))^{t-1}$. The function $\mu \mapsto \mu(\mu + \lambda(1 - \mu))^{t-1}$ is nondecreasing on $[0, 1]$, since both factors are nonnegative and nondecreasing ($\mu + \lambda(1 - \mu) = \lambda + (1 - \lambda)\mu$). So its value at $\mu \le 1/2$ is at most its value at $1/2$, which is $\frac{1}{2}\big(\frac{1 + \lambda}{2}\big)^{t-1}$. $\square$

For a target error $2^{-k}$ with $k \ge 1$, it is enough that $(t - 1)\log_2\frac{2}{1 + \lambda} \ge k - 1$. For $\lambda \le 1/2$ the factor is at most $3/4$, so $t - 1 \ge (k - 1)/\log_2(4/3) \approx 2.41(k - 1)$ suffices.

**Theorem (expander mixing lemma).** For all sets $S, T \subseteq V$, let $e(S, T) = \mathbf{1}_S^\top A \mathbf{1}_T$, the number of pairs $(u, v)$ with $u \in S$, $v \in T$ and $uv$ an edge, counted with multiplicity. Then

$$\left| e(S, T) - \frac{d|S||T|}{N} \right| \le \lambda d \sqrt{|S|\Big(1 - \frac{|S|}{N}\Big)|T|\Big(1 - \frac{|T|}{N}\Big)} \le \lambda d \sqrt{|S||T|}.$$

*Proof.* Write $\mathbf{1}_S = \sigma\mathbf{1} + x$ with $\sigma = |S|/N$ and $x \perp \mathbf{1}$, and $\mathbf{1}_T = \tau\mathbf{1} + y$ with $\tau = |T|/N$ and $y \perp \mathbf{1}$. Then $\|x\|^2 = \|\mathbf{1}_S\|^2 - \sigma^2 N = |S|(1 - \sigma)$, and in the same way $\|y\|^2 = |T|(1 - \tau)$. Expand, with $A\mathbf{1} = d\mathbf{1}$ and $A$ symmetric:

$$\mathbf{1}_S^\top A \mathbf{1}_T = \sigma\tau\,\mathbf{1}^\top A\mathbf{1} + \sigma\,\mathbf{1}^\top A y + \tau\, x^\top A\mathbf{1} + x^\top A y = \sigma\tau d N + 0 + 0 + x^\top A y,$$

since $\mathbf{1}^\top A y = d\,\mathbf{1}^\top y = 0$ and $x^\top A \mathbf{1} = d\, x^\top \mathbf{1} = 0$. The first term is $d|S||T|/N$. By Cauchy-Schwarz and Lemma 1, $|x^\top A y| = d|x^\top M y| \le d\|x\|\|My\| \le \lambda d \|x\|\|y\|$. $\square$

**Corollary (expansion of small sets).** If $T$ is the set of vertices with no neighbour in $S$, then $e(S, T) = 0$, and the mixing lemma gives $\sigma\tau \le \lambda^2(1 - \sigma)(1 - \tau)$. So every set $S$ of density $\sigma$ has neighbours in all but a fraction $\tau \le \lambda^2(1 - \sigma)/(\sigma + \lambda^2(1 - \sigma)) < \lambda^2/\sigma$ of the vertices. This is the property used on the page [disperser](/disperser/).

*Proof.* From $\sigma\tau d N \le \lambda d N \sqrt{\sigma(1 - \sigma)\tau(1 - \tau)}$, square and divide by $\sigma\tau$ (the case $\tau = 0$ is trivial): $\sigma\tau \le \lambda^2(1 - \sigma)(1 - \tau)$. Solve for $\tau$: $\tau(\sigma + \lambda^2(1 - \sigma)) \le \lambda^2(1 - \sigma)$. $\square$
