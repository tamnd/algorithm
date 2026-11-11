---
title: AOS ring signatures verify and hide the signer perfectly
proves: [correctness]
status: full
---

**Setting.** $G = \langle g \rangle$ has prime order $q$. The ring is $L = (y_0, \ldots, y_{n-1})$ with $y_i = g^{x_i}$, and member $s$ knows $x_s$. Write $H_L(t) = H(L, m, t) \in \mathbb{Z}_q$ and $T_i(e) = g^{z_i} y_i^{e}$. Indices are taken modulo $n$.

**Lemma 1 (the chain).** After lines L2 to L5, the values $e_0, \ldots, e_{n-1}$ satisfy $e_{i+1} = H_L(T_i(e_i))$ for every $i$, including $i = s$.

*Proof.* For $i \ne s$ this is line L4, which runs for $i = s+1, \ldots, s-1$ in order, each time using $e_i$ that line L2 or the step before has set. For $i = s$, line L5 sets $z_s = \alpha - x_s e_s$, so $T_s(e_s) = g^{\alpha - x_s e_s} \cdot g^{x_s e_s} = g^\alpha$, and line L2 set $e_{s+1} = H_L(g^\alpha)$. $\square$

**Theorem 2 (correctness).** For every ring, every member $s$ and every message, verify accepts the output of sign.

*Proof.* The verifier starts with $e = e_0$ and, in step $i$ (line L8), replaces $e$ by $H_L(T_i(e))$. By induction on $i$ and Lemma 1, after step $i$ it holds $e_{i+1}$. After step $n-1$ it holds $e_n = e_0$, so line L9 accepts. $\square$

**Theorem 3 (perfect anonymity).** Fix the ring, the message and the hash function. For a uniform $\alpha$ and uniform $z_i$ ($i \ne s$), the signature $(e_0, z_0, \ldots, z_{n-1})$ has the same distribution for every signer $s$. In fact, for every valid signature $\sigma$ and every member $j$ there is exactly one choice of coins with which member $j$ outputs $\sigma$.

*Proof.* Let $\sigma = (e_0, z_0, \ldots, z_{n-1})$ be valid, and let $e_1, \ldots, e_{n-1}$ be the values of the verifier's walk. Member $j$ outputs $\sigma$ if and only if its coins are $z_i$ for $i \ne j$ and $\alpha = z_j + x_j e_j$: with these coins line L2 gives $H_L(g^{\alpha}) = H_L(T_j(e_j)) = e_{j+1}$, line L4 then reproduces the walk, and line L5 gives back $z_j$. Conversely, the $z_i$ for $i \ne j$ are copied into $\sigma$, and $\alpha$ is fixed by line L5 once $e_j$ is fixed. So the map from member $j$'s coins $(\alpha, (z_i)_{i \ne j}) \in \mathbb{Z}_q^n$ to valid signatures is a bijection onto the set of valid signatures, for each $j$, and a uniform input gives the uniform distribution on that set. The set does not depend on $j$. $\square$

The anonymity holds even against an unbounded adversary who knows all secret keys, as long as each signer uses fresh uniform coins. The tests check the bijection: for a signature by member 2, `coins_for` computes the coins of each other member, and signing with them gives the same signature.

**Unforgeability.** Correctness says nothing about outsiders. Abe, Ohkubo and Suzuki prove that, in the random oracle model, a forger that does not know any $x_i$ can be turned into an algorithm for discrete logarithms in $G$, by rewinding at the query that closes the ring (the forking lemma).
