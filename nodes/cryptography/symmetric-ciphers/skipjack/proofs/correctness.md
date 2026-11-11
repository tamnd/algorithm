---
title: Skipjack decryption inverts Skipjack encryption
proves: [correctness]
status: full
---

Fix any key $cv_0, \ldots, cv_9$ and any table $F$ of 256 bytes. $F$ need not be a permutation. All words have 16 bits and $\oplus$ is XOR. For a step $k$, write $c = k + 1$ for the counter.

**$G_k$ is a bijection.** Write $\kappa_i = cv_{(4k + i) \bmod 10}$ for $i = 0, 1, 2, 3$. Lines L7 to L10 compute, from $(g_1, g_2)$, the bytes $g_{j+2} = F[g_{j+1} \oplus \kappa_{j-1}] \oplus g_j$ for $j = 1, 2, 3, 4$, and the output is $(g_5, g_6)$. Each line is a Feistel round: from $(g_j, g_{j+1})$ it makes $(g_{j+1}, g_{j+2})$. Given $(g_{j+1}, g_{j+2})$, the old byte is

$$g_j = F[g_{j+1} \oplus \kappa_{j-1}] \oplus g_{j+2},$$

because $x \oplus y \oplus y = x$. So, from $(g_5, g_6)$, apply this for $j = 4, 3, 2, 1$ to find $g_4, g_3, g_2, g_1$. This is $G_k^{-1}$. It uses $F$ only in the forward direction.

**Rule A is a bijection.** Let $(a, b, d, e)$ be the output of line L3 on input $(w_1, w_2, w_3, w_4)$. Then $a = G_k(w_1) \oplus w_4 \oplus c$, $b = G_k(w_1)$, $d = w_2$ and $e = w_3$. From the output:

- $w_1 = G_k^{-1}(b)$,
- $w_2 = d$ and $w_3 = e$,
- $w_4 = a \oplus G_k(w_1) \oplus c = a \oplus b \oplus c$.

So the input is a function of the output, and the inverse of rule A is $(a, b, d, e) \mapsto (G_k^{-1}(b), d, e, a \oplus b \oplus c)$, as on the page.

**Rule B is a bijection.** Let $(a, b, d, e)$ be the output of line L5 on input $(w_1, w_2, w_3, w_4)$. Then $a = w_4$, $b = G_k(w_1)$, $d = w_1 \oplus w_2 \oplus c$ and $e = w_3$. From the output:

- $w_1 = G_k^{-1}(b)$,
- $w_2 = d \oplus w_1 \oplus c$,
- $w_3 = e$ and $w_4 = a$.

So the inverse of rule B is $(a, b, d, e) \mapsto (x, x \oplus d \oplus c, e, a)$ with $x = G_k^{-1}(b)$, as on the page.

**The whole cipher.** Encryption is the composition $S_{31} \circ \cdots \circ S_1 \circ S_0$, where $S_k$ is step $k + 1$, rule A or rule B with $G_k$ and counter $k + 1$. Each $S_k$ is a bijection, so the composition is a bijection, and its inverse is $S_0^{-1} \circ S_1^{-1} \circ \cdots \circ S_{31}^{-1}$. Decryption on the page applies $S_{31}^{-1}$ first and $S_0^{-1}$ last, with the same rule, key bytes and counter for each $k$. So decryption of the encryption of any block gives the block back. $\square$

**Termination.** The loop of line L1 runs 32 times, and each step runs lines L7 to L10 once, so encryption and decryption do a fixed amount of work for each block.
