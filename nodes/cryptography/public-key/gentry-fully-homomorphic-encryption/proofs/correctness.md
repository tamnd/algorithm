---
title: DGHV evaluation is correct while the noise stays below p/2, and recryption refreshes the noise
proves: [correctness]
status: full
---

Let $p$ be odd, and for an integer $z$ let $[z]_p$ be the unique integer in $(-p/2, p/2]$ congruent to $z$ modulo $p$. Say that an integer $c$ **encrypts** the bit $m$ **with noise** $\nu$ if $c = \nu + pk$ for some integer $k$ and $\nu \equiv m \pmod 2$.

**Lemma 1 (decryption).** If $c$ encrypts $m$ with noise $\nu$ and $|\nu| < p/2$, then DGHV-DECRYPT$(p, c) = m$.

*Proof.* $\nu \equiv c \pmod p$ and $\nu \in (-p/2, p/2)$, so $[c]_p = \nu$ by uniqueness, and $\nu \bmod 2 = m$. $\square$

**Lemma 2 (fresh ciphertexts).** A ciphertext from line L6 encrypts $m$ with a noise $\nu$ such that $|\nu| \le 1 + 2^{\rho' + 1} + (4\tau + 2) 2^{\rho}$.

*Proof.* Write $V = m + 2r + 2\sum_{i \in S} x_i$ and $c = V - j x_0$ with the integer $j$ that line L6 uses. Since $x_i = p q_i + r_i$, $c = \nu + pk$ with $\nu = m + 2r + 2\sum_{i \in S} r_i - j r_0$ and $k = 2\sum_{i \in S} q_i - j q_0$. Line L3 makes $r_0 = [x_0]_p$ even (for the parameters used, $|r_0| < 2^\rho < p/2$, so $r_0 = [x_0]_p$), so $\nu \equiv m \pmod 2$. For the size: $0 \le \sum_{i \in S} x_i \le \tau x_0$ for the nonnegative $x_i$ (and $\ge -\tau 2^\rho$ in general), and $|m + 2r| \le 2^{\rho'+1}$, so $-x_0 < V < (2\tau + 1) x_0$ and $|j| \le 2\tau + 1$. Hence $|\nu| \le 1 + 2(2^{\rho'} - 1) + 2\tau 2^\rho + (2\tau + 1) 2^\rho$, which gives the bound. $\square$

**Lemma 3 (gates).** If $c_1$ and $c_2$ encrypt $m_1$ and $m_2$ with noises $\nu_1$ and $\nu_2$, then $c_1 + c_2$ encrypts $m_1 \oplus m_2$ with noise $\nu_1 + \nu_2$, and $c_1 c_2$ encrypts $m_1 m_2$ with noise $\nu_1 \nu_2$.

*Proof.* $c_1 + c_2 = (\nu_1 + \nu_2) + p(k_1 + k_2)$ and $\nu_1 + \nu_2 \equiv m_1 + m_2 \equiv m_1 \oplus m_2 \pmod 2$. Also $c_1 c_2 = \nu_1 \nu_2 + p(\nu_1 k_2 + \nu_2 k_1 + p k_1 k_2)$ and $\nu_1 \nu_2 \equiv m_1 m_2 \pmod 2$. $\square$

**Theorem (correctness of evaluation).** Let $f$ be a circuit of XOR and AND gates. Give each input wire the bound $B$ of Lemma 2, an XOR gate the sum of the bounds of its inputs, and an AND gate their product. If the bound $B_f$ of the output wire is below $p/2$, then DGHV-DECRYPT$(p, \text{DGHV-EVAL}(f, c_1, \ldots, c_\ell)) = f(m_1, \ldots, m_\ell)$ for fresh ciphertexts $c_i$ of $m_i$.

*Proof.* By induction over the gates in topological order, using Lemma 3 and the triangle inequality, every wire carries an encryption of the right bit with noise of absolute value at most the bound of the wire. Lemma 1 applied to the output wire finishes the proof. $\blacksquare$

**The toy parameters.** With $\rho = 16$, $\rho' = 32$ and $\tau = 24$, $(4\tau + 2) 2^\rho = 98 \cdot 2^{16} < 2^{23}$, so $B < 2^{34}$. A balanced product of $2^d$ fresh ciphertexts has bound $B^{2^d} < 2^{34 \cdot 2^d}$. Since $p$ has $\eta = 192$ binary digits, $p/2 \ge 2^{190}$, and the theorem covers $d \le 2$ ($2^{136}$). For $d = 3$ the bound $2^{272}$ is far above $p$, and the theorem says nothing; the example on the page shows that decryption then really fails.

**Theorem (recryption).** Let DECRYPT be a circuit of XOR and AND gates that computes the decryption bit from the bits of the secret key and the bits of a ciphertext. Let $\langle sk \rangle$ be fresh encryptions of the key bits, and give the bit wires $\bar{c}_j$ the bound 1. If the bound of the output of DECRYPT under these input bounds is $B_D < p/2$, then for every $c$ that decrypts to $m$, RECRYPT$(pk, \langle sk \rangle, c)$ encrypts $m$ with noise at most $B_D$.

*Proof.* A bit $c_j \in \{0, 1\}$ is $c_j + p \cdot 0$, so it encrypts $c_j$ with noise $c_j$, of absolute value at most 1. By the induction of the previous theorem, the output of EVAL encrypts DECRYPT$(sk, c) = m$ with noise at most $B_D$. The bound $B_D$ depends only on the circuit DECRYPT and on the fresh noise bound of $\langle sk \rangle$, not on the noise of $c$. $\blacksquare$

The same argument with the circuit D of BOOTSTRAPPED-NAND shows that its output encrypts the NAND of the two input bits with noise at most $B_D$, so a circuit of NAND gates of any depth can be evaluated by applying BOOTSTRAPPED-NAND to each gate. Squashing is what makes $B_D < p/2$ possible for DGHV; this page does not prove the parameter conditions for it, which are in the paper.
