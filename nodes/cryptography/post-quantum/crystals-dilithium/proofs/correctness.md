---
title: ML-DSA verification accepts every signature that the signing loop returns
proves: [correctness]
status: full
---

Work in $R_q = \mathbb{Z}_q[X]/(X^{256}+1)$ with $q = 8380417$. For $a \in \mathbb{Z}_q$ let $a \bmod^\pm m$ be the representative of $a$ modulo $m$ in $(-m/2, m/2]$, and let $\|f\|_\infty$ be the largest absolute value of a coefficient of $f$ after reduction $\bmod^\pm q$. Let $\alpha = 2\gamma_2$; for both values of $\gamma_2$, $\alpha$ divides $q - 1$, and write $q - 1 = \alpha M$. The NTT is a ring isomorphism, so lines L3, L10 and L20 compute products in $R_q$.

**Definitions (FIPS 204, Section 7.4).** For $r \in \mathbb{Z}_q$ taken in $[0, q-1]$, Decompose sets $r_0 = r \bmod^\pm \alpha$; if $r - r_0 = q - 1$ it returns $(0, r_0 - 1)$, else it returns $((r - r_0)/\alpha, r_0)$. HighBits and LowBits are the two outputs. MakeHint$(z, r) = 1$ exactly when HighBits$(r) \ne$ HighBits$(r + z)$. UseHint$(h, r)$ with $(r_1, r_0) = $ Decompose$(r)$ returns $r_1$ if $h = 0$, $(r_1 + 1) \bmod M$ if $h = 1$ and $r_0 > 0$, and $(r_1 - 1) \bmod M$ if $h = 1$ and $r_0 \le 0$. All of them act coefficient by coefficient.

**Lemma 1 (the bands).** For $0 \le j < M$ let $B_j$ be the set of $r \in \mathbb{Z}_q$ with HighBits$(r) = j$. Then $B_0 = \{-\gamma_2, \dots, \gamma_2\}$ and $B_j = \{j\alpha + t : -\gamma_2 < t \le \gamma_2\}$ for $j \ge 1$, all modulo $q$. Each $B_j$ is a run of consecutive residues around the center $j\alpha$, with more than $\gamma_2$ elements on each side of the center counted with the center, the runs follow each other in the order $B_0, B_1, \dots, B_{M-1}$ around the circle, and $B_{M-1}$ is followed by $B_0$. For $r \in B_j$, LowBits$(r)$ is the offset $t$ of $r$ from $j\alpha$ in this run.

*Proof.* Take $r \in [0, q-1]$ and $r_0 = r \bmod^\pm \alpha \in (-\gamma_2, \gamma_2]$. In the normal case $r = r_1\alpha + r_0$ with $r_1 = (r - r_0)/\alpha$, and $0 \le r - r_0 < q - 1$, so $0 \le r_1 \le M - 1$; this gives $r \in B_{r_1}$ with offset $r_0$. The special case $r - r_0 = q - 1$ happens exactly for $r = q - 1 + r_0$ with $-\gamma_2 < r_0 \le 0$, that is for $r \in \{q - \gamma_2, \dots, q - 1\}$, and then the output $(0, r_0 - 1)$ puts $r \equiv r_0 - 1$ in $B_0$ with offset $r_0 - 1 \in [-\gamma_2, -1]$. The normal case with $r_1 = 0$ gives $r \in [0, \gamma_2]$. So $B_0 = \{-\gamma_2, \dots, \gamma_2\}$ modulo $q$. The top element of $B_{M-1}$ is $(M-1)\alpha + \gamma_2 = q - 1 - \gamma_2$, and the next residue $q - \gamma_2 \equiv -\gamma_2$ is the bottom element of $B_0$. The sizes are $2\gamma_2 + 1$ and $2\gamma_2$, and $2\gamma_2 + 1 + (M - 1) 2\gamma_2 = q$, so the runs cover $\mathbb{Z}_q$ once. $\square$

**Lemma 2 (UseHint).** Let $r, z \in \mathbb{Z}_q$ with $|z \bmod^\pm q| \le \gamma_2$, and let $h = $ MakeHint$(z, r)$. Then UseHint$(h, r) = $ HighBits$(r + z)$.

*Proof.* If $h = 0$, then HighBits$(r + z) = $ HighBits$(r) = r_1$, which is what UseHint returns. Let $h = 1$, and let $r \in B_{r_1}$ with offset $r_0$ (Lemma 1). Moving from $r$ by $z$ steps on the circle changes the offset to $r_0 + z$ as long as it stays in the run. The bottom offset of a run is $-\gamma_2$ or $-\gamma_2 + 1$ and the top offset is $\gamma_2$, so leaving the run downward needs $r_0 + z \le -\gamma_2$ and leaving it upward needs $r_0 + z > \gamma_2$. If $r_0 > 0$, the first is impossible because $r_0 + z \ge 1 - \gamma_2$, so $r + z$ left upward. It cannot pass the whole next run, which has at least $2\gamma_2$ elements, because $r_0 + z \le 2\gamma_2$, so $r + z \in B_{(r_1 + 1) \bmod M}$. If $r_0 \le 0$, leaving upward needs $z > \gamma_2$, which is impossible, so $r + z$ left downward, and since $r_0 + z \ge -2\gamma_2$ it lands in $B_{(r_1 - 1) \bmod M}$. These are the two values that UseHint returns. $\square$

**Lemma 3 (stable high bits).** If $|s \bmod^\pm q| \le \beta$ and $|\mathrm{LowBits}(r)| < \gamma_2 - \beta$, then HighBits$(r + s) = $ HighBits$(r)$.

*Proof.* Let $r \in B_{r_1}$ with offset $r_0$, $|r_0| < \gamma_2 - \beta$. The offset of $r + s$ is $r_0 + s$ with $|r_0 + s| < \gamma_2$, which is inside the run $B_{r_1}$ by Lemma 1. Apply this to each coefficient. $\square$

**Lemma 4 (what the verifier computes).** Let $t = A s_1 + s_2$ and $t = t_1 2^d + t_0$ from lines L3 and L4. For $z = y + c s_1$ and $w = A y$, line L20 computes $w'_{approx} = w - c s_2 + c t_0$.

*Proof.* Power2Round gives $t \equiv t_1 2^d + t_0$. So $A z - c t_1 2^d = A y + c A s_1 - c (t - t_0) = A y + c A s_1 - c A s_1 - c s_2 + c t_0$. $R_q$ is commutative, so $c A s_1 = A (c s_1)$. $\square$

**Theorem.** Let $(pk, sk)$ come from lines L1 to L6 (through line L23), and let $\sigma = (\tilde c, z, h)$ be returned at line L16 for the message $M'$ (through line L24 with the same context). Then lines L17 to L22 (through line L25) return true.

*Proof.* Line L19 recomputes $\mu$: $tr = H(pk, 64)$ by line L5, and $M'$ is the same byte string because lines L24 and L25 build it in the same way, so $\mu$ equals the value of line L7. SampleInBall is deterministic, so the verifier gets the same $c$. The decoders invert the encoders on the values that signing writes: $z$ has coefficients in $(-(\gamma_1 - \beta), \gamma_1 - \beta)$ and $h$ has at most $\omega$ ones (line L15), so line L17 recovers $(\tilde c, z, h)$, and line L18 passes by line L13. Every coefficient of $c$ is in $\{-1, 0, 1\}$ with $\tau$ nonzero, so $\|c s_2\|_\infty \le \tau \eta = \beta$.

Let $r = w - c s_2$. By Lemma 4, $w'_{approx} = r + c t_0$. Line L14 sets $h = $ MakeHint$(-c t_0, r + c t_0)$, and line L15 ensures $\|c t_0\|_\infty < \gamma_2$, so Lemma 2 with the value $r + c t_0$ and the shift $-c t_0$ gives UseHint$(h, w'_{approx}) = $ HighBits$(r)$. By line L13, $\|\mathrm{LowBits}(r)\|_\infty < \gamma_2 - \beta$, so Lemma 3 with $s = c s_2$ gives HighBits$(r) = $ HighBits$(r + c s_2) = $ HighBits$(w) = w_1$. So line L21 gets $w_1' = w_1$, and line L22 computes $H(\mu \| \mathrm{w1Encode}(w_1), \lambda/4) = \tilde c$ by line L11. $\blacksquare$

**Termination.** The proof is exact for every returned signature; the only random part is how many iterations the loop needs. Each iteration uses a fresh $\kappa$, so ExpandMask gives a new mask, and the acceptance probability of one iteration is a constant (about $1/4.25$ for ML-DSA-44 by FIPS 204, Table 1) under the usual heuristic that the hash outputs behave as random. The number of iterations is then geometric, with expected value the inverse of that constant.
