---
title: A5/1 decrypts correctly, and each majority clock moves at least two registers
proves: [correctness]
status: full
---

Write $\sigma = (R_1, R_2, R_3)$ for the state, with $R_1$, $R_2$, $R_3$ integers of 19, 22 and 23 bits.

**Lemma 1 (registers keep their lengths).** After each line of the page, $0 \le R_j < 2^{L_j}$ for $L = (19, 22, 23)$.

*Proof.* Line L1 sets each register to 0. Line L8 shifts left, cuts the result to $L_j$ bits and sets bit 0 to a single bit $t$, so the result is below $2^{L_j}$. Lines L2 and L3 XOR one bit into bit 0, which does not change the length. Lines L4, L5 and L7 only call line L8. By induction the claim holds. $\square$

**Lemma 2 (determinism).** The keystream $z_1, \ldots, z_n$ is a function of $(K, f, n)$ only.

*Proof.* Line L1 sets a fixed state. Lines L2 and L3 apply fixed maps that depend only on the bits of $K$ and $f$. Line L6 computes $m$ from $\sigma$, and line L7 applies line L8 to the registers chosen by $\sigma$ and $m$, so each majority clock is a fixed function of $\sigma$. Line L5 reads three fixed bits of $\sigma$. By induction on the number of clocks, each state and each $z_t$ is a function of $(K, f)$. $\square$

**Theorem 1 (correctness).** For each key, frame number and message $m$ of $n$ bits, the receiver recovers $m$ from $c = m \oplus z$.

*Proof.* By Lemma 2 the receiver computes the same $z$, and $(m_t \oplus z_t) \oplus z_t = m_t$ for each bit, since $z_t \oplus z_t = 0$. $\blacksquare$

**Lemma 3 (at least two registers move).** In each call of line L7, at least two registers move. If the three clocking bits are independent and uniform, each register moves with probability 3/4.

*Proof.* Let $b_1, b_2, b_3$ be the clocking bits and $m$ their majority. The bits take two values, so by the pigeonhole principle at least two of them are equal, and by the definition of the majority at least two of them equal $m$. Line L7 moves exactly the registers with $b_j = m$. For the second claim, $R_1$ does not move if and only if $b_2 = b_3 \ne b_1$, which is 2 of the 8 equally likely triples. So $R_1$ moves with probability $6/8 = 3/4$, and the same count holds for $R_2$ and $R_3$. $\square$

**Remark.** These are functional facts. The majority clock is not injective on the $2^{64}$ states, so some states have no predecessor and others have several. For example, take $R_3'$ with bit 10 equal to 0 and bit 9 equal to 1, let $R_3 = \mathrm{STEP}(R_3')$, whose bit 10 is 1, and take $R_1, R_2$ with clocking bits 0. Then $(R_1, R_2, R_3')$ moves all three registers and $(R_1, R_2, R_3)$ moves only $R_1$ and $R_2$, and both give $(\mathrm{STEP}(R_1), \mathrm{STEP}(R_2), R_3)$. The security claims of A5/1 do not hold: the attacks named on the page recover the state in practice.
