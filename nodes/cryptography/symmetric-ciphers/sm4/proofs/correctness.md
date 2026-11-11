---
title: SM4 decryption inverts SM4 encryption
proves: [correctness]
status: full
---

Fix any round keys $rk_0, \ldots, rk_{31}$ and any function $T$ from words to words. The proof does not need $T$ to be invertible and does not use the key schedule. All words have 32 bits and $\oplus$ is XOR.

**Encryption.** Line L2 defines $X_4, \ldots, X_{35}$ from $X_0, \ldots, X_3$ by

$$X_{i+4} = X_i \oplus T(X_{i+1} \oplus X_{i+2} \oplus X_{i+3} \oplus rk_i), \qquad i = 0, \ldots, 31. \tag{1}$$

XOR both sides with the value of $T$. This gives

$$X_i = X_{i+4} \oplus T(X_{i+1} \oplus X_{i+2} \oplus X_{i+3} \oplus rk_i). \tag{2}$$

**Decryption.** Decryption runs lines L1 to L3 on the ciphertext $(X_{35}, X_{34}, X_{33}, X_{32})$ with round keys $rk'_j = rk_{31-j}$. Call its words $Y_0, Y_1, \ldots$. So $Y_0 = X_{35}$, $Y_1 = X_{34}$, $Y_2 = X_{33}$, $Y_3 = X_{32}$, and

$$Y_{j+4} = Y_j \oplus T(Y_{j+1} \oplus Y_{j+2} \oplus Y_{j+3} \oplus rk_{31-j}).$$

*Claim.* $Y_j = X_{35-j}$ for $j = 0, \ldots, 35$.

*Proof by induction on $j$.* The claim holds for $j = 0, 1, 2, 3$ by the definition of the input. Let $j \ge 0$ and assume the claim for $j, j+1, j+2, j+3$. Put $i = 31 - j$, so $35 - j = i + 4$, $34 - j = i + 3$, $33 - j = i + 2$ and $32 - j = i + 1$. Then

$$Y_{j+4} = X_{i+4} \oplus T(X_{i+3} \oplus X_{i+2} \oplus X_{i+1} \oplus rk_i).$$

XOR is commutative, so the argument of $T$ is the same as in (2), and by (2) $Y_{j+4} = X_i = X_{31-j} = X_{35-(j+4)}$. $\square$

So $Y_{32}, Y_{33}, Y_{34}, Y_{35} = X_3, X_2, X_1, X_0$, and line L3 of decryption outputs $(Y_{35}, Y_{34}, Y_{33}, Y_{32}) = (X_0, X_1, X_2, X_3)$, the plaintext. So decryption inverts encryption for every key, and encryption is a bijection on blocks. $\square$

**Termination.** The loops of lines L1 and L7 run 32 times each with a fixed amount of work, so each block and each key setup takes a fixed number of steps.
