---
title: GOST 28147-89 decryption inverts encryption
proves: [correctness]
status: full
---

Fix any S-boxes, so that $g(k, a)$ of lines L4 to L6 is a fixed function of two 32-bit words. The proof does not need $g$ to be invertible in $a$. All words have 32 bits and $\oplus$ is XOR. For a key word $k$, write

$$G[k](a_1, a_0) = (a_0,\ g(k, a_0) \oplus a_1), \qquad G^*[k](a_1, a_0) = (g(k, a_0) \oplus a_1,\ a_0),$$

as in RFC 8891. Line L2 applies $G[K_i]$ and line L3 applies $G^*[K_{32}]$. Let $\sigma(a_1, a_0) = (a_0, a_1)$ be the swap of the halves. Then $G[k] = \sigma \circ G^*[k]$.

**$G^*[k]$ is an involution.** Apply it twice: $G^*[k](g(k, a_0) \oplus a_1, a_0) = (g(k, a_0) \oplus g(k, a_0) \oplus a_1, a_0) = (a_1, a_0)$, because the right half $a_0$ does not change, so the second call of $g$ gets the same input. So $G^*[k]^{-1} = G^*[k]$. Also $\sigma^{-1} = \sigma$.

**Encryption.** With round keys $K_1, \ldots, K_{32}$, encryption is

$$E = G^*[K_{32}] \circ G[K_{31}] \circ \cdots \circ G[K_1] = G^*[K_{32}] \circ \sigma \circ G^*[K_{31}] \circ \sigma \circ \cdots \circ \sigma \circ G^*[K_1].$$

Each factor is a bijection, so $E$ is a bijection. Its inverse is the product of the inverses in reverse order:

$$E^{-1} = G^*[K_1] \circ \sigma \circ G^*[K_2] \circ \sigma \circ \cdots \circ \sigma \circ G^*[K_{32}].$$

**Decryption.** The page runs the same procedure with the keys $K_{32}, \ldots, K_1$. That procedure computes

$$G^*[K_1] \circ G[K_2] \circ \cdots \circ G[K_{32}] = G^*[K_1] \circ \sigma \circ G^*[K_2] \circ \sigma \circ \cdots \circ \sigma \circ G^*[K_{32}],$$

which is $E^{-1}$ term by term. So decryption of the encryption of any block gives the block back. $\square$

**The reflection property.** Let $k_1, \ldots, k_8$ be the key words, and write $H = G[k_8] \circ \cdots \circ G[k_1]$ for rounds 17 to 24 and $H' = G^*[k_8] \circ G[k_7] \circ \cdots \circ G[k_1]$, so $H = \sigma \circ H'$. Rounds 25 to 32 compute $L = G^*[k_1] \circ G[k_2] \circ \cdots \circ G[k_8]$, which is $H'^{-1}$ by the argument above. If $y$ is the state after round 16 and $x = H(y)$ has equal halves, then $\sigma(x) = x$, so $H'(y) = \sigma(H(y)) = x$ and $L(x) = H'^{-1}(x) = y$. So the ciphertext is the state after round 16. This is the property that the page uses in its Properties section.

**Termination.** The loop of line L1 runs 31 times, and lines L4 to L6 do a fixed amount of work, so each block takes a fixed number of steps.
