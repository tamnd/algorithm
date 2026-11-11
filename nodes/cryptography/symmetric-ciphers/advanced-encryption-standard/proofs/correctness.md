---
title: The AES inverse cipher inverts the cipher, and the AES-128 key expansion can be run backward
proves: [correctness]
status: full
---

We write SB, SR, MC and ARK$_t$ for SubBytes, ShiftRows, MixColumns and AddRoundKey with round key $t$, and ISB, ISR, IMC for the inverse steps. By lines L3 to L11,

$$E_K = \mathrm{ARK}_{N_r} \circ \mathrm{SR} \circ \mathrm{SB} \circ \prod_{t = N_r - 1}^{1} (\mathrm{ARK}_t \circ \mathrm{MC} \circ \mathrm{SR} \circ \mathrm{SB}) \circ \mathrm{ARK}_0,$$

where the product is a composition with $t = 1$ applied first.

**Lemma 1 (each step is a bijection with the stated inverse).**

1. ARK$_t$ is its own inverse, since $(s \oplus k) \oplus k = s$.
2. ISR rotates row $r$ right by $r$ places, which undoes the left rotation by $r$ places of SR.
3. The S-box is $S(a) = A \cdot \mathrm{inv}(a) \oplus \mathtt{63}$, where $\mathrm{inv}(a) = a^{254}$ is the field inverse for $a \ne 0$ and $\mathrm{inv}(0) = 0$. The map inv is its own inverse, so it is a bijection, and $A$ is invertible over GF(2), so the affine map is a bijection. So $S$ is a bijection, and ISB applies $S^{-1}$ to each byte.
4. MC multiplies each column, as a polynomial of degree at most 3 over GF($2^8$), by $a(x) = \mathtt{03}x^3 + \mathtt{01}x^2 + \mathtt{01}x + \mathtt{02}$ modulo $x^4 + 1$, and IMC multiplies by $a'(x) = \mathtt{0B}x^3 + \mathtt{0D}x^2 + \mathtt{09}x + \mathtt{0E}$. Since $x^4 \equiv 1$, the coefficient of $x^m$ in the product is $\bigoplus_{i + j \equiv m \pmod 4} a_i a'_j$. For $m = 0$, it is

$$\mathtt{02}\cdot\mathtt{0E} \oplus \mathtt{01}\cdot\mathtt{0B} \oplus \mathtt{01}\cdot\mathtt{0D} \oplus \mathtt{03}\cdot\mathtt{09} = \mathtt{1C} \oplus \mathtt{0B} \oplus \mathtt{0D} \oplus \mathtt{1B} = \mathtt{01}.$$

For $m = 1$, it is $\mathtt{02}\cdot\mathtt{09} \oplus \mathtt{01}\cdot\mathtt{0E} \oplus \mathtt{01}\cdot\mathtt{0B} \oplus \mathtt{03}\cdot\mathtt{0D} = \mathtt{12} \oplus \mathtt{0E} \oplus \mathtt{0B} \oplus \mathtt{17} = \mathtt{00}$. For $m = 2$, it is $\mathtt{02}\cdot\mathtt{0D} \oplus \mathtt{01}\cdot\mathtt{09} \oplus \mathtt{01}\cdot\mathtt{0E} \oplus \mathtt{03}\cdot\mathtt{0B} = \mathtt{1A} \oplus \mathtt{09} \oplus \mathtt{0E} \oplus \mathtt{1D} = \mathtt{00}$. For $m = 3$, it is $\mathtt{02}\cdot\mathtt{0B} \oplus \mathtt{01}\cdot\mathtt{0D} \oplus \mathtt{01}\cdot\mathtt{09} \oplus \mathtt{03}\cdot\mathtt{0E} = \mathtt{16} \oplus \mathtt{0D} \oplus \mathtt{09} \oplus \mathtt{12} = \mathtt{00}$. So $a(x) a'(x) \equiv 1$, and IMC $\circ$ MC and MC $\circ$ IMC are the identity, since multiplication modulo $x^4 + 1$ is commutative. $\square$

**Lemma 2.** ISB $\circ$ ISR $=$ ISR $\circ$ ISB.

*Proof.* ISB applies the same map to every byte, and ISR only moves bytes. $\square$

**Theorem 1.** For every key and block, the inverse cipher returns the input of the cipher.

*Proof.* By Lemma 1, the inverse of $E_K$ is the composition of the inverses of its steps in the reverse order:

$$E_K^{-1} = \mathrm{ARK}_0 \circ \prod_{t = 1}^{N_r - 1} (\mathrm{ISB} \circ \mathrm{ISR} \circ \mathrm{IMC} \circ \mathrm{ARK}_t) \circ \mathrm{ISB} \circ \mathrm{ISR} \circ \mathrm{ARK}_{N_r},$$

with $t = N_r - 1$ applied first. Group the steps applied in order: first ARK$_{N_r}$; then ISR, ISB, which by Lemma 2 is the same as ISR then ISB in either order; then ARK$_{N_r - 1}$, IMC; then ISR, ISB, ARK$_{N_r - 2}$, IMC; and so on, ending with ISR, ISB, ARK$_0$. This is the order of the inverse cipher of FIPS 197: ARK$_{N_r}$, then for $t = N_r - 1$ down to 1 the steps ISR, ISB, ARK$_t$, IMC, then ISR, ISB, ARK$_0$. $\square$

**Theorem 2.** For AES-128, the four words of any round key $t$ determine the cipher key.

*Proof.* With $N_k = 4$, line L18 gives $w[i] = w[i - 4] \oplus T_i(w[i - 1])$, where $T_i(v) = \mathrm{SubWord}(\mathrm{RotWord}(v)) \oplus \mathrm{Rcon}[i/4]$ if $4 \mid i$ and $T_i(v) = v$ otherwise. So $w[i - 4] = w[i] \oplus T_i(w[i - 1])$. Given $w[4t], \ldots, w[4t + 3]$ with $t \ge 1$, take $i = 4t + 3, 4t + 2, 4t + 1, 4t$ in this order. Each step uses $w[i]$ and $w[i - 1]$, which are known, since $w[i - 1]$ is either in the given round key or was found in the step before. This gives $w[4t - 4], \ldots, w[4t - 1]$, which is round key $t - 1$. By induction on $t$, round key 0, which is the cipher key, follows. $\blacksquare$

The test vectors of FIPS 197 Appendix C.1 to C.3, Appendix B and the round 1 states of Appendix C.1 check the implementation against the standard, and the tests check $D_K(E_K(x)) = x$ for random keys of all three sizes.
