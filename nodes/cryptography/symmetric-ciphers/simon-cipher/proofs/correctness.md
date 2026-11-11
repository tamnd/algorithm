---
title: SIMON decryption inverts encryption
proves: [correctness]
status: full
---

Let $n$ be the word size and let $f$ be any function from $n$-bit words to $n$-bit words; for SIMON, $f(x) = (S^1 x \wedge S^8 x) \oplus S^2 x$. For a round key $k$, let
$$R_k(x, y) = (y \oplus f(x) \oplus k,\; x), \qquad R_k^{*}(x', y') = (y',\; x' \oplus f(y') \oplus k).$$
Line L3 applies $R_{k_i}$ and line L7 applies $R_{k_i}^{*}$.

**Lemma 1.** $R_k^{*}(R_k(x, y)) = (x, y)$ for all $x, y, k$.

*Proof.* Let $(x', y') = R_k(x, y)$, so $x' = y \oplus f(x) \oplus k$ and $y' = x$. Then $R_k^{*}(x', y') = (y', x' \oplus f(y') \oplus k) = (x, y \oplus f(x) \oplus k \oplus f(x) \oplus k) = (x, y)$, because $a \oplus a = 0$. $\square$

The lemma uses nothing about $f$. This is the general fact that a [Feistel network](/feistel-network/) round is invertible for each round function.

**Lemma 2.** Both procedures compute the same round keys $k_0, \ldots, k_{T-1}$.

*Proof.* Lines L1 and L5 call the same KEY-SCHEDULE on the same key, and the schedule is a deterministic function of the key and the fixed constants $c$ and $z_j$. $\square$

**Theorem.** For each parameter set, key and block $v$, SIMON-DECRYPT(SIMON-ENCRYPT$(v)) = v$, and SIMON-ENCRYPT is a permutation of $\{0,1\}^{2n}$.

*Proof.* By Lemma 2, encryption is $E = R_{k_{T-1}} \circ \cdots \circ R_{k_0}$ and decryption is $D = R^{*}_{k_0} \circ \cdots \circ R^{*}_{k_{T-1}}$. In $D \circ E$ the innermost pair is $R^{*}_{k_{T-1}} \circ R_{k_{T-1}}$, which is the identity by Lemma 1. Removing it leaves the same form with $T - 1$ rounds, and induction on $T$ gives $D \circ E = \mathrm{id}$. So $E$ has a left inverse on a finite set, and it is a bijection. $\blacksquare$
