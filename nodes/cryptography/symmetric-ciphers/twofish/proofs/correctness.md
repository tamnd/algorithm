---
title: Twofish decryption inverts Twofish encryption
proves: [correctness]
status: full
---

Fix a key, so that the subkeys $K_0, \ldots, K_{39}$ and the function $g$ are fixed. All words have 32 bits. $g$ is any function from words to words; we do not use that it is a bijection. Write $F_r(a, b) = (F_0, F_1)$ for the output of lines L6 to L10 in round $r$. It depends only on $a$, $b$ and $r$.

**One round.** Line L4 maps a state $(a, b, c, d)$ to

$$\Phi_r(a, b, c, d) = (\mathrm{ROR}(c \oplus F_0, 1),\ \mathrm{ROL}(d, 1) \oplus F_1,\ a,\ b), \qquad (F_0, F_1) = F_r(a, b).$$

Define

$$\Psi_r(a', b', c', d') = (c',\ d',\ \mathrm{ROL}(a', 1) \oplus G_0,\ \mathrm{ROR}(b' \oplus G_1, 1)), \qquad (G_0, G_1) = F_r(c', d').$$

*Claim.* $\Psi_r(\Phi_r(a, b, c, d)) = (a, b, c, d)$ for all words $a, b, c, d$.

*Proof.* Let $(a', b', c', d') = \Phi_r(a, b, c, d)$. Then $c' = a$ and $d' = b$, so $(G_0, G_1) = F_r(a, b) = (F_0, F_1)$. The first two outputs of $\Psi_r$ are $c' = a$ and $d' = b$. The third is $\mathrm{ROL}(\mathrm{ROR}(c \oplus F_0, 1), 1) \oplus F_0 = c \oplus F_0 \oplus F_0 = c$, because ROL by 1 undoes ROR by 1 on a 32-bit word. The fourth is $\mathrm{ROR}(\mathrm{ROL}(d, 1) \oplus F_1 \oplus F_1, 1) = \mathrm{ROR}(\mathrm{ROL}(d, 1), 1) = d$. $\square$

**The whole cipher.** Let $W_{\mathrm{in}}(a, b, c, d) = (a \oplus K_0, b \oplus K_1, c \oplus K_2, d \oplus K_3)$ be line L1 on the words of the block, and let $W_{\mathrm{out}}(a, b, c, d) = (c \oplus K_4, d \oplus K_5, a \oplus K_6, b \oplus K_7)$ be line L5. Then

$$E = W_{\mathrm{out}} \circ \Phi_{15} \circ \cdots \circ \Phi_0 \circ W_{\mathrm{in}}.$$

Each map has an inverse that we can write down. $W_{\mathrm{in}}^{-1}$ XORs the same words again. $W_{\mathrm{out}}^{-1}(u, v, w, z) = (w \oplus K_6, z \oplus K_7, u \oplus K_4, v \oplus K_5)$, which we check by substitution: applied to $W_{\mathrm{out}}(a, b, c, d)$ it gives $(a, b, c, d)$. By the claim, $\Psi_r$ is a left inverse of $\Phi_r$, and since $\Phi_r$ maps the finite set of states to itself, $\Phi_r$ is a bijection and $\Psi_r = \Phi_r^{-1}$. So

$$D = W_{\mathrm{in}}^{-1} \circ \Psi_0 \circ \Psi_1 \circ \cdots \circ \Psi_{15} \circ W_{\mathrm{out}}^{-1}$$

satisfies $D(E(x)) = x$ for every block $x$, by applying the inverse maps from the outside in. This $D$ is what TWOFISH-DECRYPT computes: it removes the output whitening, swaps the halves back, runs $\Psi_r$ for $r = 15$ down to 0, and removes the input whitening. $\square$

**The key schedule.** Lines L13 to L19 are a straight-line computation with a loop of exactly 20 steps, so they stop. The proof above holds for any subkeys and any $g$, so it holds for the ones the key schedule makes.
