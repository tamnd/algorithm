---
title: Honest BLS signatures verify, and each message has exactly one valid signature
proves: [correctness]
status: full
---

Let $G$ be a cyclic group of prime order $r$ with generator $g$, and let $e : G \times G \to G_T$ be bilinear ($e(u^a, v^b) = e(u, v)^{ab}$ for all $u, v \in G$ and integers $a, b$) and non-degenerate ($e(g, g) \ne 1$). Let $x \in [1, r-1]$ and $pk = g^x$.

**Lemma 1 (honest signatures verify).** For every message $m$, the output $\sigma$ of lines L2 and L3 passes lines L4 to L6.

*Proof.* Line L2 gives $h = H(m) \in G$, so $\sigma = h^x \in G$. Also $pk = g^x \in G$ and $pk \ne 1$, because $g$ has order $r$ and $0 < x < r$. So line L4 does not reject. Line L5 recomputes the same $h$. By bilinearity, $e(\sigma, g) = e(h^x, g^1) = e(h, g)^{x} = e(h^1, g^x) = e(h, pk)$, so line L6 returns true. $\square$

**Lemma 2 ($e(\cdot, g)$ is injective on $G$).** If $u, v \in G$ and $e(u, g) = e(v, g)$, then $u = v$.

*Proof.* Write $u = g^a$ and $v = g^b$. Then $e(g, g)^a = e(g, g)^b$, so $e(g, g)^{a - b} = 1$. The element $e(g, g)$ is not 1, and $e(g, g)^r = e(g^r, g) = e(1, g) = 1$, so its order divides the prime $r$ and is not 1; hence it is exactly $r$. So $r$ divides $a - b$, and $u = v$. $\square$

**Lemma 3 (uniqueness).** For a fixed $pk$ and $m$, the only $\sigma \in G$ that passes line L6 is $H(m)^x$.

*Proof.* Let $\sigma' \in G$ pass line L6, so $e(\sigma', g) = e(H(m), pk)$. By Lemma 1, $e(H(m)^x, g) = e(H(m), pk)$ too. By Lemma 2, $\sigma' = H(m)^x$. $\square$

**Lemma 4 (same-message aggregation).** Let $\sigma_i = H(m)^{x_i}$ be honest signatures under $pk_i = g^{x_i}$ for $i = 1, \dots, N$. Then $\sigma = \prod_i \sigma_i$ satisfies $e(\sigma, g) = e(H(m), \prod_i pk_i)$.

*Proof.* $\prod_i \sigma_i = H(m)^{\sum_i x_i}$ and $\prod_i pk_i = g^{\sum_i x_i}$, and Lemma 1 applies to the secret $\sum_i x_i \bmod r$ (if that sum is $0 \bmod r$ both sides are 1). $\blacksquare$

The same computation shows why rogue keys work: the check sees only the product of the keys, so any set of keys with product $g^\beta$ accepts $H(m)^\beta$.
