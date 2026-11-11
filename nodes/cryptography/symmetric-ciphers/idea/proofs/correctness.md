---
title: IDEA decryption with inverted subkeys inverts IDEA encryption
proves: [correctness]
status: full
---

Fix 52 subkeys. A state is a tuple $(x_1, x_2, x_3, x_4)$ of 16-bit words. Write $Z_r = (k_1, \ldots, k_4)$ for the first four subkeys of round $r$ (with $r = 9$ for the output step) and $(k_5, k_6)$ for the last two of round $r \le 8$.

**The operations are group operations.** XOR and $\boxplus$ are group operations on 16-bit words. For $\odot$: 65537 is prime, so the nonzero residues modulo 65537 form a group under multiplication. Line L9 maps the word $w \ne 0$ to the residue $w$ and the word 0 to the residue $2^{16}$, which is a bijection between 16-bit words and nonzero residues. So $\odot$ is a group operation on words, with identity 1, and every word $k$ has an inverse $k^{-1}$ with $k \odot k^{-1} = 1$.

**The steps.** Define these maps on states:

- The key step $T_{(k_1, k_2, k_3, k_4)}(x) = (x_1 \odot k_1, x_2 \boxplus k_2, x_3 \boxplus k_3, x_4 \odot k_4)$, which is line L3. Its inverse is $T_{(k_1^{-1}, -k_2, -k_3, k_4^{-1})}$, because each component is a group operation with a fixed element.
- The MA step $N_{(k_5, k_6)}(x) = (x_1 \oplus t_1, x_2 \oplus t_2, x_3 \oplus t_1, x_4 \oplus t_2)$, where $t_0 = k_5 \odot (x_1 \oplus x_3)$, $t_1 = k_6 \odot (t_0 \boxplus (x_2 \oplus x_4))$ and $t_2 = t_0 \boxplus t_1$. These are lines L4 to L7 without the exchange of the middle words.
- The exchange $s(x_1, x_2, x_3, x_4) = (x_1, x_3, x_2, x_4)$.

Line L7 is $s \circ N$: in the code's names, $X_2$ gets $c \oplus t_1$, the new third word, and $X_3$ gets $b \oplus t_2$.

**$N$ is its own inverse.** Let $y = N(x)$. Then $y_1 \oplus y_3 = x_1 \oplus t_1 \oplus x_3 \oplus t_1 = x_1 \oplus x_3$ and in the same way $y_2 \oplus y_4 = x_2 \oplus x_4$. Since $t_0$, $t_1$ and $t_2$ depend only on these two values and on $k_5, k_6$, the step $N(y)$ computes the same $t_1$ and $t_2$ and XORs them in again, which gives back $x$. No property of $\odot$ or $\boxplus$ is needed here.

**$s$ moves through a key step.** For all subkeys, $s \circ T_{(k_1, k_2, k_3, k_4)} = T_{(k_1, k_3, k_2, k_4)} \circ s$: both sides give $(x_1 \odot k_1, x_3 \boxplus k_3, x_2 \boxplus k_2, x_4 \odot k_4)$. Also $s \circ s$ is the identity.

**Encryption.** Line L8 is $T_{Z_9} \circ s$, because it reads $X_3$ before $X_2$. So

$$E = T_{Z_9} \circ s \circ (s \circ N_8 \circ T_{Z_8}) \circ \cdots \circ (s \circ N_1 \circ T_{Z_1}) = T_{Z_9} \circ N_8 \circ T_{Z_8} \circ s \circ N_7 \circ T_{Z_7} \circ \cdots \circ s \circ N_1 \circ T_{Z_1}.$$

**The inverse.** Every factor is a bijection, $N_r$ and $s$ are their own inverses, and $T_Z^{-1} = T_{\bar Z}$ with $\bar Z = (k_1^{-1}, -k_2, -k_3, k_4^{-1})$. So

$$E^{-1} = T_{\bar Z_1} \circ N_1 \circ s \circ T_{\bar Z_2} \circ N_2 \circ s \circ \cdots \circ s \circ T_{\bar Z_8} \circ N_8 \circ T_{\bar Z_9}.$$

Read this product from the right, in the order of application:

$$T_{\bar Z_9}, \; N_8, \; T_{\bar Z_8}, \; s, \; N_7, \; T_{\bar Z_7}, \; s, \; \ldots, \; T_{\bar Z_2}, \; s, \; N_1, \; T_{\bar Z_1}.$$

Let $\bar Z_r' = (k_1^{-1}, -k_3, -k_2, k_4^{-1})$ be $\bar Z_r$ with the middle words exchanged. By the rule above, "$T_{\bar Z_r}$, then $s$" equals "$s$, then $T_{\bar Z_r'}$". Doing this for every $r = 8, \ldots, 2$, the order of application becomes

$$T_{\bar Z_9}, \; N_8, \; s, \; T_{\bar Z_8'}, \; N_7, \; s, \; T_{\bar Z_7'}, \; \ldots, \; N_2, \; s, \; T_{\bar Z_2'}, \; N_1, \; T_{\bar Z_1}.$$

**Comparison.** Group these steps as $(T_{\bar Z_9}, N_8, s)$, $(T_{\bar Z_8'}, N_7, s)$, ..., $(T_{\bar Z_2'}, N_1, s)$, followed by $s$ and then $T_{\bar Z_1}$. The last group gets an $s$ that is cancelled by the added $s$, since $s \circ s$ is the identity. Each group is one round of IDEA-ENCRYPT, which is the key step, then $N$, then $s$. The final "$s$, then $T_{\bar Z_1}$" is line L8. So $E^{-1}$ is IDEA-ENCRYPT with these subkeys:

- round 1: $\bar Z_9$ and the $(k_5, k_6)$ of encryption round 8;
- round $r$ for $2 \le r \le 8$: $\bar Z_{10-r}'$ and the $(k_5, k_6)$ of encryption round $9 - r$;
- the output step: $\bar Z_1$.

These are the decryption subkeys of the page: inverses and negatives from encryption round $10 - r$, with $-k_2$ and $-k_3$ exchanged except in the first round and the output step. $\square$

**Termination.** The loop of line L1 runs 8 times. The key schedule appends 8 subkeys per pass of the loop of line L10, so it stops after 7 passes.
