---
title: ARIA decryption is encryption with transformed round keys
proves: [correctness]
status: full
---

Fix round keys $ek_1, \ldots, ek_{n+1}$ with $n$ even. The proof holds for any values, so it does not depend on the key schedule. For a 128-bit value $k$, write $X_k(x) = x \oplus k$. Write $S_1 = SL_1$, $S_2 = SL_2$, and $A$ for the diffusion layer.

**Three facts.**

1. $S_2 \circ S_1$ is the identity. $SL_1$ applies $SB_1, SB_2, SB_3, SB_4$ to the bytes in positions $0, 1, 2, 3 \pmod 4$, and $SL_2$ applies $SB_3, SB_4, SB_1, SB_2$ to the same positions. Since $SB_3 = SB_1^{-1}$ and $SB_4 = SB_2^{-1}$, each byte position gets an S-box followed by its inverse. In the same way $S_1 \circ S_2$ is the identity.
2. $A \circ A$ is the identity. This is a property of the fixed 16 by 16 binary matrix of $A$, which the test file checks on random inputs and which follows from the matrix product over the two-element field.
3. $A$ is linear over XOR: $A(x \oplus k) = A(x) \oplus A(k)$. So $A \circ X_k = X_{A(k)} \circ A$.

**Encryption.** Lines L1 to L4 apply, in this order,

$$X_{ek_1}, S_1, A, \; X_{ek_2}, S_2, A, \; X_{ek_3}, S_1, A, \; \ldots, \; X_{ek_{n-1}}, S_1, A, \; X_{ek_n}, S_2, X_{ek_{n+1}}.$$

The S-box layer after $X_{ek_r}$ is $S_1$ for odd $r$ and $S_2$ for even $r$. This holds for $r = n$ too, because $n$ is even and line L4 uses $S_2$.

**The inverse.** Each step is a bijection: $X_k$ and $A$ are their own inverses, and $S_1, S_2$ are inverses of each other. So $E^{-1}$ applies the inverses in reverse order:

$$X_{ek_{n+1}}, S_1, X_{ek_n}, A, S_2, X_{ek_{n-1}}, A, S_1, X_{ek_{n-2}}, \ldots, A, S_1, X_{ek_2}, A, S_2, X_{ek_1}.$$

Here the layer between $X_{ek_{r+1}}$ and $X_{ek_r}$ is the inverse of the layer after $X_{ek_r}$ in encryption: $S_2$ for odd $r$ and $S_1$ for even $r$.

**Moving the keys.** By fact 3, each pair "$X_{ek_r}$, then $A$" with $2 \le r \le n$ can be replaced by "$A$, then $X_{A(ek_r)}$". This gives

$$X_{ek_{n+1}}, S_1, A, \; X_{A(ek_n)}, S_2, A, \; X_{A(ek_{n-1})}, S_1, A, \; \ldots, \; X_{A(ek_3)}, S_1, A, \; X_{A(ek_2)}, S_2, X_{ek_1}.$$

**Comparison.** Set $dk_1 = ek_{n+1}$, $dk_j = A(ek_{n+2-j})$ for $2 \le j \le n$, and $dk_{n+1} = ek_1$. The key $dk_j$ with $2 \le j \le n$ is $A(ek_r)$ with $r = n + 2 - j$, and it is followed by the layer for $r - 1 = n + 1 - j$, which is $S_2$ if $n + 1 - j$ is odd and $S_1$ if it is even. Since $n$ is even, $n + 1 - j$ is odd exactly when $j$ is even. So $dk_j$ is followed by $S_1$ for odd $j$ and by $S_2$ for even $j$, which is the rule of encryption. The key $dk_1$ is followed by $S_1$ and the key $dk_n$ is followed by $S_2$ and then $X_{dk_{n+1}}$ with no $A$, as in line L4. So the sequence above is ARIA-ENCRYPT with the round keys $dk_1, \ldots, dk_{n+1}$, and decryption with these keys computes $E^{-1}$. $\square$

**Why $n$ must be even.** If $n$ were odd, the layer after $X_{dk_1}$ in $E^{-1}$ would be $S_2$, while ARIA-ENCRYPT uses $S_1$ in round 1. All three key sizes give an even $n$: 12, 14 or 16.

**Termination.** The loop of line L1 runs $n - 1$ times, and each step does a fixed amount of work.
