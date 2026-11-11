---
title: The Feige-Fiat-Shamir scheme is complete, has soundness error 2^-k per round, and its secrets can be extracted
proves: [correctness]
status: full
---

Let $n = pq$ with $p, q$ distinct primes, $p \equiv q \equiv 3 \pmod 4$. Let $s_1, \ldots, s_k \in \mathbb{Z}_n^*$ and $v_j = (-1)^{b_j} s_j^{-2} \bmod n$. For $e \in \{0,1\}^k$ write $S_e = \prod_{e_j = 1} s_j$ and $V_e = \prod_{e_j = 1} v_j$. Line numbers refer to the pseudocode on the page.

**Lemma 1 (completeness).** An honest round is accepted.

*Proof.* Line L3 gives $x = (-1)^b r^2$ with $r \in \mathbb{Z}_n^*$, so $x \ne 0$ and line L6 does not reject. Line L5 gives $y = r S_e$. Then
$$y^2 V_e = r^2 \prod_{e_j = 1} s_j^2 \cdot \prod_{e_j = 1} (-1)^{b_j} s_j^{-2} = (-1)^{\sum_{e_j = 1} b_j} r^2 = \pm x,$$
so line L7 accepts. $\square$

**Lemma 2 (two answers give a secret).** Let $x \ne 0$ and let $(x, e, y)$ and $(x, e', y')$ be accepted, with $y' \in \mathbb{Z}_n^*$. Let $j$ be an index with $e_j = 1$ and $e'_j = 0$, and suppose $e$ and $e'$ agree elsewhere. Then $u = y / y' \bmod n$ satisfies $u^2 v_j = \pm 1$.

*Proof.* The two checks give $y^2 V_e = \pm x$ and $y'^2 V_{e'} = \pm x$. Here $V_e = V_{e'} v_j$. Since $y'$ and $V_{e'}$ are units, $x = \pm y'^2 V_{e'}$ is a unit too. Divide the first equation by the second: $(y/y')^2 v_j = \pm 1$. $\square$

For general $e \ne e'$ the same division gives $(y/y')^2 V_e / V_{e'} = \pm 1$, a square root of $\pm$ a known product of the $v_j^{\pm 1}$. The extractor in the code uses challenges that differ in one position, which a rewinding extractor can arrange by fixing the other positions.

**Lemma 3 (soundness error $2^{-k}$ per round).** Suppose a prover, with $x$ fixed, can answer two different challenges $e \ne e'$. Then it can compute some $u$ with $u^2 \prod_j v_j^{d_j} = \pm 1$ for the nonzero vector $d = e - e'$ with entries in $\{-1, 0, 1\}$. So a prover that knows no such root answers at most one challenge for each $x$, and passes a round with probability at most $2^{-k}$. The guessing prover, which picks $e^*$ and $y$ and sends $x = y^2 V_{e^*}$, passes with probability exactly $2^{-k}$.

*Proof.* The first part is the division of Lemma 2 with $u = y/y'$. For the guessing prover: if $e = e^*$, then $y^2 V_e = x$ and the round is accepted. If $e \ne e^*$ and the round were also accepted with the same $y$, then $y^2 V_e = \pm y^2 V_{e^*}$, so $V_e / V_{e^*} = \pm 1$. That is a relation $\prod_j v_j^{d_j} = \pm 1$ with $d \ne 0$, which holds only for special keys; for keys with no such relation, exactly one of the $2^k$ challenges is accepted. $\square$

**Lemma 4 (honest-verifier zero knowledge).** For each fixed $e$, the real pair $(x, y)$, with $r$ uniform in $\mathbb{Z}_n^*$ and $b$ a uniform bit, and the simulated pair $((-1)^b y^2 V_e, y)$, with $y$ uniform in $\mathbb{Z}_n^*$ and $b$ a uniform bit, have the same distribution.

*Proof.* In the real round $y = r S_e$, and $r \mapsto r S_e$ is a bijection of $\mathbb{Z}_n^*$, so $y$ is uniform and independent of $b$. Given $y$, the real $x = (-1)^b r^2 = (-1)^b y^2 S_e^{-2}$. Now $S_e^{-2} = \prod_{e_j = 1} s_j^{-2} = (-1)^{\beta} V_e$ with $\beta = \sum_{e_j = 1} b_j$, a constant. So $x = (-1)^{b + \beta} y^2 V_e$, and $b + \beta \bmod 2$ is a uniform bit independent of $y$. This is the simulated distribution. $\blacksquare$

**Remark (why the signs).** For a Blum integer, $-1$ has Jacobi symbol $+1$ but is not a square, and the units of Jacobi symbol $+1$ are exactly the numbers $\pm a^2$. With uniform $s_j$ and $b_j$, each $v_j$ is uniform over these units, and with a uniform $b$ so is $x$. So neither the public key nor the first message reveals whether a value is a square, a question that is believed hard without the factors ([quadratic residuosity](/quadratic-residuosity-problem/)).
