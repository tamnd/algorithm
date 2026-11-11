---
title: Kuznyechik decryption inverts Kuznyechik encryption
proves: [correctness]
status: full
---

Fix any round keys $K_1, \ldots, K_{10}$. The proof does not use the key schedule, so it holds for any keys. Write a block as $a_{15} \| \cdots \| a_0$ and let $l$ be the map of line L9. The only fact about $l$ that the proof needs is that the coefficient of $a_0$ is 1, so $l(a_{15}, \ldots, a_1, a_0) = m(a_{15}, \ldots, a_1) \oplus a_0$, where $m$ is the sum of the other 15 terms.

**$X[k]$ is an involution.** $(a \oplus k) \oplus k = a$.

**$S$ is a bijection.** $\pi$ is a permutation of the 256 bytes, so it has an inverse $\pi^{-1}$, and $S^{-1}$ applies $\pi^{-1}$ to each byte.

**$R$ is a bijection, with the inverse of the page.** Let $b = R(a) = l(a_{15}, \ldots, a_0) \| a_{15} \| \cdots \| a_1$, so $b_{15} = l(a_{15}, \ldots, a_0)$ and $b_{i-1} = a_i$ for $i = 1, \ldots, 15$. The page defines

$$R^{-1}(b) = b_{14} \| \cdots \| b_0 \| l(b_{14}, \ldots, b_0, b_{15}).$$

The first 15 bytes are $b_{14}, \ldots, b_0 = a_{15}, \ldots, a_1$, which are the first 15 bytes of $a$. The last byte is

$$l(a_{15}, \ldots, a_1, b_{15}) = m(a_{15}, \ldots, a_1) \oplus b_{15} = m(a_{15}, \ldots, a_1) \oplus m(a_{15}, \ldots, a_1) \oplus a_0 = a_0.$$

So $R^{-1}(R(a)) = a$ for every $a$. Since $R$ maps a finite set to itself and has a left inverse, it is a bijection, and $R^{-1}$ is its inverse. Then $L = R^{16}$ is a bijection with inverse $L^{-1} = (R^{-1})^{16}$.

**The whole cipher.** For $i = 1, \ldots, 9$, round $i$ is $\rho_i = L \circ S \circ X[K_i]$, a composition of bijections. Encryption is $E = X[K_{10}] \circ \rho_9 \circ \cdots \circ \rho_1$, a bijection. Its inverse is

$$E^{-1} = \rho_1^{-1} \circ \cdots \circ \rho_9^{-1} \circ X[K_{10}], \qquad \rho_i^{-1} = X[K_i] \circ S^{-1} \circ L^{-1}.$$

So decryption first XORs $K_{10}$, then for $i = 9$ down to 1 computes $S^{-1}(L^{-1}(a)) \oplus K_i$. This is the decryption of the page. $\square$

**The key schedule.** Line L13 is a Feistel round $F[C](a_1, a_0) = (LSX[C](a_1) \oplus a_0, a_1)$. Correctness of the cipher does not need the key schedule to be invertible, but it is: $F[C]$ is undone by $(b_1, b_0) \mapsto (b_0, LSX[C](b_0) \oplus b_1)$, so the key can be found from $K_1$ and $K_2$, which are the key itself.

**Termination.** The loops of lines L1, L6, L11 and L12 have fixed bounds, so each block and each key setup takes a fixed number of steps.
