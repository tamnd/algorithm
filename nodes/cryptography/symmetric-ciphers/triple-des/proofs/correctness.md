---
title: TDEA decryption inverts TDEA encryption, and the meet-in-the-middle attack finds the key pair
proves: [correctness]
status: full
---

Write $E_K$ and $D_K$ for DES encryption and decryption under the key $K$. The proof of correctness of [DES](/data-encryption-standard/) shows that $D_K(E_K(x)) = x$ for all $K$ and $x$. Since $E_K$ is a map from the finite set $\{0,1\}^{64}$ to itself with a left inverse, it is a bijection, so also $E_K(D_K(y)) = y$ for all $y$.

**Theorem 1.** For every key bundle $(K_1, K_2, K_3)$ and every block $x$, TDEA-DECRYPT$(K_1, K_2, K_3$, TDEA-ENCRYPT$(K_1, K_2, K_3, x)) = x$.

*Proof.* Lines L1 to L3 give $y = E_{K_3}(D_{K_2}(E_{K_1}(x)))$. Lines L4 to L6 then compute

$$D_{K_1}(E_{K_2}(D_{K_3}(y))) = D_{K_1}(E_{K_2}(D_{K_3}(E_{K_3}(D_{K_2}(E_{K_1}(x)))))).$$

The innermost pair $D_{K_3} \circ E_{K_3}$ is the identity, which leaves $D_{K_1}(E_{K_2}(D_{K_2}(E_{K_1}(x))))$. The pair $E_{K_2} \circ D_{K_2}$ is the identity, which leaves $D_{K_1}(E_{K_1}(x)) = x$. $\square$

**Theorem 2 (keying option 3).** If $K_1 = K_2 = K$, then TDEA-ENCRYPT$(K, K, K_3, x) = E_{K_3}(x)$. In particular, with three equal keys, TDEA is single DES.

*Proof.* Line L2 computes $D_K(E_K(x)) = x$, and line L3 returns $E_{K_3}(x)$. $\square$

**Theorem 3 (meet in the middle).** Let $E$ be any block cipher with keys in $\{0,1\}^k$, and let $y_j = E_{K_2}(E_{K_1}(x_j))$ for $j = 1, \ldots, s$. The attack stores $E_{k_1}(x_1)$ for every $k_1$, computes $D_{k_2}(y_1)$ for every $k_2$, and outputs each pair $(k_1, k_2)$ with $E_{k_1}(x_1) = D_{k_2}(y_1)$ that also satisfies $E_{k_2}(E_{k_1}(x_j)) = y_j$ for $j = 2, \ldots, s$. Its output contains $(K_1, K_2)$, and every pair it outputs agrees with all $s$ given pairs. It makes $2 \cdot 2^k$ calls for the table and the lookups, plus two calls for each test of a candidate on each further pair.

*Proof.* For $(k_1, k_2)$, the condition $E_{k_1}(x_1) = D_{k_2}(y_1)$ holds if and only if $E_{k_2}(E_{k_1}(x_1)) = y_1$, by applying the bijection $E_{k_2}$ to both sides. So the candidates after the first pair are exactly the key pairs that agree with $(x_1, y_1)$. The true pair agrees with every $(x_j, y_j)$ by the definition of $y_j$, so it is a candidate and passes every test, and it is output. A pair is output only if it passes the test on each pair $j \ge 2$, so every output agrees with all $s$ pairs. The table loop makes one call for each of the $2^k$ values of $k_1$, and the lookup loop makes one call for each of the $2^k$ values of $k_2$. $\blacksquare$

If $E_{k_2} \circ E_{k_1}$ behaves like a random permutation for each wrong pair, each of the $2^{2k} - 1$ wrong pairs agrees with one given pair with probability about $2^{-n}$, so about $2^{2k - n}$ candidates survive the first pair and about $2^{2k - sn}$ survive $s$ pairs. For DES, $2k - n = 48$, and $s = 2$ leaves about $2^{-16}$ false pairs on average.
