---
title: Correctness of the Pohlig-Hellman algorithm
proves: [correctness, termination, minimality]
status: full
---

Let $G$ be a finite abelian group, $g, h \in G$, and $N = \prod_{(l, e) \in F} l^e$ a multiple of $\operatorname{ord}(g)$, with each $l$ prime.

**Lemma 1 (exact order).** After lines L1 to L3, $r = \operatorname{ord}(g)$.

*Proof.* Let $o = \operatorname{ord}(g)$. Throughout, $o \mid r$: this holds for $r = N$, and $r$ is replaced by $r/l$ only if $g^{r/l} = 1$, that is, only if $o \mid r/l$. When the loop for $l$ ends, either $l \nmid r$, or $g^{r/l} \ne 1$, so $o \nmid r/l$. In both cases the exponent of $l$ in $r$ equals the exponent of $l$ in $o$: it is at least that, since $o \mid r$, and if it were larger then $o \mid r/l$. Later rounds only remove other primes, so they keep this exponent and keep $o \mid r$. At the end every prime has the same exponent in $r$ and in $o$, and $r \mid N$ has no other primes, so $r = o$. $\square$

**Lemma 2 (membership in a cyclic group).** If $G$ is cyclic, then $h \in \langle g \rangle$ if and only if $h^r = 1$.

*Proof.* If $h = g^x$ then $h^r = (g^r)^x = 1$. A cyclic group has exactly one subgroup of each order dividing $\#G$, and the elements $y$ with $y^r = 1$ form a subgroup of order $r$ (in a cyclic group of order $M$ with generator $c$, $c^t$ satisfies $c^{tr} = 1$ exactly when $M/\gcd(M, r) \mid t$, which gives $\gcd(M, r) = r$ elements, as $r \mid M$). This subgroup contains $\langle g \rangle$, of order $r$, so the two are equal. $\square$

So if line L4 returns NONE, then $h \notin \langle g \rangle$, in any group. For the rest of the proof, suppose first that $h = g^{x^*}$, where $x^*$ is the least non-negative solution; then $0 \le x^* < r$.

**Lemma 3 (projection).** Let $l^f \parallel r$ and $c = r/l^f$. Then $g_l = g^c$ has order $l^f$, $h_l = h^c = g_l^{x^*}$, and for an integer $y$, $g_l^y = h_l$ if and only if $y \equiv x^* \pmod{l^f}$.

*Proof.* $g$ has order $r$, so $g^c$ has order $r/\gcd(r, c) = l^f$. Then $h_l = (g^{x^*})^c = g_l^{x^*}$, and $g_l^y = g_l^{x^*}$ holds exactly when $l^f \mid y - x^*$. $\square$

**Lemma 4 (digits).** Write $x^* \bmod l^f = \sum_{k=0}^{f-1} d_k l^k$ with $0 \le d_k < l$. Before round $k$ of lines L11 to L15, $x_l = \sum_{t < k} d_t l^t$. In round $k$, baby-step giant-step returns $d = d_k$.

*Proof.* By induction on $k$; for $k = 0$, $x_l = 0$ by line L10. Assume the claim before round $k$. By Lemma 3, $h_l g_l^{-x_l} = g_l^{y}$ with $y \equiv x^* - x_l \pmod{l^f}$, and $y \equiv \sum_{t \ge k} d_t l^t \pmod{l^f}$. Raising to $l^{f-1-k}$ gives $g_l^{y l^{f-1-k}}$, and

$$y \, l^{f-1-k} \equiv d_k l^{f-1} + l^{f} \textstyle\sum_{t > k} d_t l^{t-k-1} \equiv d_k l^{f-1} \pmod{l^f}.$$

So $\delta = g_l^{d_k l^{f-1}} = \gamma^{d_k}$, with $\gamma = g_l^{l^{f-1}}$ of order $l$. Baby-step giant-step with the bound $l \ge \operatorname{ord}(\gamma)$ returns the least $d \ge 0$ with $\gamma^d = \delta$, which is $d_k$ since $0 \le d_k < l = \operatorname{ord}(\gamma)$. Line L15 then gives $x_l = \sum_{t \le k} d_t l^t$. $\square$

**Correctness for $h \in \langle g \rangle$.** By Lemma 2 and the first direction of its proof, line L4 does not return. By Lemma 4, line L14 never returns, and after the loop for $l$, $x_l = x^* \bmod l^f$. The moduli $l^f$ for the distinct primes $l \mid r$ are pairwise coprime with product $r$, so line L17 returns the unique $x \in [0, r)$ with $x \equiv x^* \pmod{l^f}$ for all $l$, by the Chinese remainder theorem. Since $0 \le x^* < r$, $x = x^*$. Line L18 finds $g^x = h$, and line L19 returns the least solution.

**Correctness for $h \notin \langle g \rangle$.** Any value that reaches line L19 has passed the test of line L18, so $g^x = h$ and $h \in \langle g \rangle$. Hence for $h \notin \langle g \rangle$ the algorithm returns NONE at line L4, L14 or L18. If $G$ is cyclic, Lemma 2 shows that line L4 already returns NONE.

**Termination.** The loop of lines L2 and L3 divides $r$ by $l$ at each round and so runs at most $e$ rounds for each $(l, e)$. The digit loop runs $f$ rounds per prime, and baby-step giant-step terminates. So the algorithm stops after finitely many group operations, bounded as in the Complexity section. $\blacksquare$
