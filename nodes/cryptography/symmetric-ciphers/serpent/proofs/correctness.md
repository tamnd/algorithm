---
title: Serpent decryption inverts Serpent encryption
proves: [correctness]
status: full
---

Fix a key, so that the round keys $\hat K_0, \ldots, \hat K_{32}$ are fixed. A state is a tuple $X = (X_0, X_1, X_2, X_3)$ of 32-bit words. We show that each step of SERPENT-ENCRYPT is a bijection on states and give its inverse. Then the decryption, which applies the inverses in reverse order, inverts encryption.

**Key XOR.** $X \mapsto X \oplus \hat K_i$ is its own inverse, because $(X \oplus \hat K_i) \oplus \hat K_i = X$.

**S-box layer.** For a permutation $S$ of $\{0, \ldots, 15\}$, line L5 maps $X$ to $Y$, where for each column $j \in \{0, \ldots, 31\}$, the column value $c_j(X) = \sum_{t=0}^{3} 2^t \cdot \mathrm{bit}_j(X_t)$ is replaced: $c_j(Y) = S(c_j(X))$. A state is fixed by its 32 column values, and the columns do not interact. Define $\hat S^{-1}$ the same way with $S^{-1}$. Then $c_j(\hat S^{-1}(\hat S(X))) = S^{-1}(S(c_j(X))) = c_j(X)$ for every $j$, so $\hat S^{-1} \circ \hat S$ is the identity.

**LT.** LT is a sequence of ten elementary steps (two in each of lines L9 to L13). Each step is of one of two types:

1. $X_a \leftarrow \mathrm{ROL}(X_a, s)$. Its inverse is $X_a \leftarrow \mathrm{ROR}(X_a, s)$, since a rotation by $s$ places to the left and then to the right gives back each bit.
2. $X_a \leftarrow X_a \oplus g(X_{\ne a})$, where $g$ depends only on words other than $X_a$. For example, in line L10, $X_1 \leftarrow X_1 \oplus X_0 \oplus X_2$ and $X_3 \leftarrow X_3 \oplus X_2 \oplus (X_0 \ll 3)$, and in line L12, $X_0 \leftarrow X_0 \oplus X_1 \oplus X_3$ and $X_2 \leftarrow X_2 \oplus X_3 \oplus (X_1 \ll 7)$. The step does not change the words $g$ reads, so applying the same step again XORs the same value $g(X_{\ne a})$ a second time and restores $X_a$.

In each line the two steps change different words, and the second step of a line does not read the word the first step changed (line L10: the step on $X_3$ reads $X_2$ and $X_0$, not $X_1$; line L12: the step on $X_2$ reads $X_3$ and $X_1$, not $X_0$). So the inverse of LT is the list of inverse steps in reverse order, which is the function lt_inv of the code. A composition of bijections is a bijection, so LT is a bijection.

**The cipher.** Write $A_i(X) = X \oplus \hat K_i$, $B_i = \hat S_{i \bmod 8}$ and $L$ = LT. Lines L3 to L7 compute

$$E = A_{32} \circ B_{31} \circ A_{31} \circ L \circ B_{30} \circ A_{30} \circ \cdots \circ L \circ B_0 \circ A_0.$$

Each factor is a bijection with the inverse given above, so $E$ is a bijection and

$$E^{-1} = A_0 \circ B_0^{-1} \circ L^{-1} \circ A_1 \circ \cdots \circ L^{-1} \circ A_{31} \circ B_{31}^{-1} \circ A_{32}.$$

This is what decryption computes: for $i = 31$ down to 0, it undoes the last step of round $i$ (the XOR with $\hat K_{32}$ when $i = 31$, else $L^{-1}$), then $B_i^{-1}$, then $A_i$. $\square$

**The key schedule.** Lines L15 to L18 run a loop of exactly 132 steps and 33 S-box layers, so they stop. The proof holds for any round keys.

**Bitslice and standard forms.** The paper also describes Serpent with an initial permutation IP, S-boxes on groups of 4 consecutive bits, and a final permutation FP $= \mathrm{IP}^{-1}$. IP moves bit $4j + t$ of the block to bit $j$ of word $X_t$, so it turns groups of 4 consecutive bits into bit columns. The two forms compute the same function (Section 3 of the paper); the test vectors, which are given for the standard form, check this for our code.
