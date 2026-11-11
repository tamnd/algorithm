---
title: Blowfish decryption inverts Blowfish encryption
proves: [correctness]
status: full
---

Fix any P-array $P_1, \ldots, P_{18}$ and any S-boxes, so that F of line L10 is a fixed function from 32-bit words to 32-bit words. F need not be a bijection. All words have 32 bits and $\oplus$ is XOR.

**A recurrence for encryption.** Let the input be $(L_0, R_0)$. Write $(L_i, R_i)$ for the values of $(x_L, x_R)$ after the swap of line L5 in round $i$, and let $a_i$ be the value of $x_L$ after line L3 in round $i$, so $a_i$ is the input of F in round $i$. Line L3 gives $a_i = L_{i-1} \oplus P_i$. Lines L4 and L5 give $L_i = R_{i-1} \oplus F(a_i)$ and $R_i = a_i$. Put $a_0 = R_0$ and $a_{17} = L_{16} \oplus P_{17}$.

*Claim.* For $1 \le i \le 16$,

$$a_{i+1} = a_{i-1} \oplus F(a_i) \oplus P_{i+1}. \tag{R}$$

*Proof.* For $i \le 16$, $a_{i+1} = L_i \oplus P_{i+1}$ (by line L3 in round $i+1$ when $i \le 15$, and by the definition of $a_{17}$ when $i = 16$). Then $L_i = R_{i-1} \oplus F(a_i)$. For $i = 1$, $R_0 = a_0$ by definition. For $i \ge 2$, $R_{i-1} = a_{i-1}$ by line L5 in round $i - 1$. So $a_{i+1} = a_{i-1} \oplus F(a_i) \oplus P_{i+1}$. $\square$

*The output.* After round 16, $(x_L, x_R) = (L_{16}, R_{16})$. Line L6 makes it $(R_{16}, L_{16})$. Line L7 makes $x_R = L_{16} \oplus P_{17} = a_{17}$, and line L8 makes $x_L = R_{16} \oplus P_{18} = a_{16} \oplus P_{18}$. So

$$E(L_0, R_0) = (a_{16} \oplus P_{18},\ a_{17}), \qquad a_0 = R_0,\ a_1 = L_0 \oplus P_1. \tag{O}$$

The same algebra holds for any 18 subkeys $Q_1, \ldots, Q_{18}$ in place of the $P_i$.

**Decryption.** BLOWFISH-DECRYPT runs the same code with $Q_i = P_{19-i}$. Let its input be the ciphertext $(C_L, C_R) = (a_{16} \oplus P_{18}, a_{17})$, and let $b_0, \ldots, b_{17}$ be its words, defined as above with $Q$. Then $b_0 = C_R = a_{17}$ and $b_1 = C_L \oplus Q_1 = a_{16} \oplus P_{18} \oplus P_{18} = a_{16}$.

*Claim.* $b_j = a_{17-j}$ for $0 \le j \le 17$.

*Proof.* By induction on $j$. The cases $j = 0$ and $j = 1$ are shown above. Let $1 \le j \le 16$ and assume the claim for $j - 1$ and $j$. Apply (R) to decryption:

$$b_{j+1} = b_{j-1} \oplus F(b_j) \oplus Q_{j+1} = a_{18-j} \oplus F(a_{17-j}) \oplus P_{18-j}.$$

Let $i = 17 - j$, so $1 \le i \le 16$. Equation (R) for encryption gives $a_{i+1} = a_{i-1} \oplus F(a_i) \oplus P_{i+1}$. XOR both sides with $F(a_i) \oplus P_{i+1}$ to get $a_{i-1} = a_{i+1} \oplus F(a_i) \oplus P_{i+1}$, that is $a_{16-j} = a_{18-j} \oplus F(a_{17-j}) \oplus P_{18-j}$. This is $b_{j+1}$, so $b_{j+1} = a_{17-(j+1)}$. $\square$

By (O) for decryption, the output is $(b_{16} \oplus Q_{18}, b_{17}) = (a_1 \oplus P_1, a_0) = (L_0, R_0)$. So $D(E(x)) = x$ for every block $x$. Because $E$ is a function from a finite set to itself with a left inverse, it is a bijection, and $D$ is its inverse.

**Key setup.** KEY-SETUP only replaces words of P and S with outputs of BLOWFISH-ENCRYPT. The proof above holds for any values of P and S, so it holds for the final P-array and S-boxes, whatever the key. The loop of line L15 runs over a fixed list of $9 + 512 = 521$ pairs, so the setup stops.
