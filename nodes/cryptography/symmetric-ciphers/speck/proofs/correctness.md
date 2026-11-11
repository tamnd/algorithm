---
title: SPECK decryption inverts encryption
proves: [correctness]
status: full
---

Words have $n$ bits, $+$ and $-$ are modulo $2^n$, and $\ggg r$, $\lll r$ are rotations, with $(w \ggg r) \lll r = w$ and $(w \lll r) \ggg r = w$. For a round key $k$, lines L3 and L4 compute the map
$$R_k(x, y) = (x', y'), \qquad x' = ((x \ggg \alpha) + y) \oplus k, \qquad y' = (y \lll \beta) \oplus x',$$
and lines L8 and L9 compute
$$R_k^{*}(x', y') = (x, y), \qquad y = (x' \oplus y') \ggg \beta, \qquad x = ((x' \oplus k) - y) \lll \alpha.$$

**Lemma 1.** $R_k^{*}(R_k(x, y)) = (x, y)$ for all $x, y, k$.

*Proof.* Let $(x', y') = R_k(x, y)$. Line L8 computes $(x' \oplus y') \ggg \beta = (x' \oplus (y \lll \beta) \oplus x') \ggg \beta = (y \lll \beta) \ggg \beta = y$. Line L9 then computes $((x' \oplus k) - y) \lll \alpha = (((x \ggg \alpha) + y) - y) \lll \alpha = (x \ggg \alpha) \lll \alpha = x$, since XOR with $k$ twice cancels and addition modulo $2^n$ is a group operation. $\square$

**Lemma 2.** Both procedures compute the same round keys $k_0, \ldots, k_{T-1}$, because lines L1 and L6 call the same deterministic KEY-SCHEDULE on the same key. $\square$

**Theorem.** For each parameter set, key and block $v$, SPECK-DECRYPT(SPECK-ENCRYPT$(v)) = v$, and SPECK-ENCRYPT is a permutation of $\{0,1\}^{2n}$.

*Proof.* By Lemma 2, encryption is $E = R_{k_{T-1}} \circ \cdots \circ R_{k_0}$ and decryption is $D = R^{*}_{k_0} \circ \cdots \circ R^{*}_{k_{T-1}}$. In $D \circ E$, the innermost pair $R^{*}_{k_{T-1}} \circ R_{k_{T-1}}$ is the identity by Lemma 1. Removing it leaves the same form with $T - 1$ rounds, and induction on $T$ gives $D \circ E = \mathrm{id}$. A map of a finite set to itself with a left inverse is a bijection. $\blacksquare$

The key schedule is the round map with the counter as key: with $(\ell_i, k_i)$ in place of $(x, y)$ and $i$ in place of $k$, $R_i$ gives $x' = ((\ell_i \ggg \alpha) + k_i) \oplus i = \ell_{i+m-1}$ and $y' = (k_i \lll \beta) \oplus \ell_{i+m-1} = k_{i+1}$. The test `test_key_schedule_is_the_round_function` checks this for SPECK128/128.
