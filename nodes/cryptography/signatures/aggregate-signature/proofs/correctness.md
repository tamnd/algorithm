---
title: Honest BGLS aggregates verify, and the distinct message rule is what blocks the rogue key cancellation
proves: [correctness]
status: full
---

Let $G$ be a cyclic group of prime order $r$ with generator $g$, and let $e : G \times G \to G_T$ be bilinear ($e(u^a, v^b) = e(u, v)^{ab}$) and non-degenerate ($e(g, g) \ne 1$). Signer $i$ has $x_i \in [1, r - 1]$ and $pk_i = g^{x_i}$, and its BLS signature on $m_i$ is $\sigma_i = H(m_i)^{x_i}$.

**Lemma 1 (aggregation is a homomorphism of the check).** For any $u_1, \dots, u_N \in G$, $e(\prod_i u_i, g) = \prod_i e(u_i, g)$.

*Proof.* By induction on $N$. For $N = 1$ there is nothing to show. Bilinearity in the first argument gives $e(u v, g) = e(u, g)\, e(v, g)$ for all $u, v \in G$ (write $u = g^a$, $v = g^b$; then $e(g^{a+b}, g) = e(g, g)^{a+b}$). Apply this with $u = \prod_{i < N} u_i$ and $v = u_N$. $\square$

**Lemma 2 (honest aggregates verify).** If the messages $m_1, \dots, m_N$ are distinct and $\sigma = \prod_i \sigma_i$ is the output of line L1, then lines L2 to L4 return true.

*Proof.* Line L2 passes because the messages are distinct. Each $\sigma_i$ and each $pk_i$ is in $G$, and $G$ is closed under the group operation, so $\sigma \in G$ and line L3 passes. By Lemma 1 and bilinearity,

$$e(\sigma, g) = \prod_i e(H(m_i)^{x_i}, g) = \prod_i e(H(m_i), g)^{x_i} = \prod_i e(H(m_i), g^{x_i}) = \prod_i e(H(m_i), pk_i),$$

so line L4 returns true. $\square$

**Lemma 3 (equal messages see only the product of keys).** If $m_1 = \dots = m_N = m$, the right side of line L4 equals $e(H(m), \prod_i pk_i)$.

*Proof.* Bilinearity in the second argument gives $\prod_i e(H(m), pk_i) = e(H(m), \prod_i pk_i)$, by the same induction as Lemma 1. $\square$

**Consequence (the rogue key).** Let $pk_1$ be honest, and let the adversary pick $\beta$ and announce $pk_2 = g^\beta \cdot pk_1^{-1}$. Then $pk_1 pk_2 = g^\beta$, and by Lemma 3 with $N = 2$ and the same message $m$, the value $\sigma = H(m)^\beta$ satisfies the equation of line L4: $e(H(m)^\beta, g) = e(H(m), g^\beta)$. The adversary knows $\beta$ but not the secret of $pk_1$, so without line L2 it has an aggregate "signed" by $pk_1$ that $pk_1$ never made. Line L2 rejects this input because the two messages are equal. With distinct messages, Lemma 3 does not apply, the hashes $H(m_1)$ and $H(m_2)$ are independent, and the BGLS reduction to co-CDH in the random oracle model shows that no adversary does better with a chosen key than with an honest one, up to the loss stated in that paper.

**Remark (splitting zero).** Lemma 1 shows that the check depends on $\sigma$ only through the product. If $\sigma_1' = \sigma_1 \delta$ and $\sigma_2' = \sigma_2 \delta^{-1}$ for any $\delta \in G$, the products are the same, so the wrong pair aggregates to a valid aggregate. Correctness is for the aggregate as a whole, not for each part. $\blacksquare$
