---
title: The three-share AND is correct and non-complete, resists one glitch-extended probe, and is uniform with two fresh bits
proves: [correctness]
status: full
---

Let $x$ and $y$ be bits with uniform sharings: $x_1, x_2$ are independent uniform bits and $x_3 = x \oplus x_1 \oplus x_2$, and the same for $y$ with bits independent of those of $x$. Let $r_1, r_2$ be independent uniform bits, independent of the rest. Lines L1 to L3 compute

$$z_1 = x_2 y_2 \oplus x_2 y_3 \oplus x_3 y_2, \quad z_2 = x_3 y_3 \oplus x_1 y_3 \oplus x_3 y_1, \quad z_3 = x_1 y_1 \oplus x_1 y_2 \oplus x_2 y_1.$$

**Theorem 1 (correctness).** $z_1 \oplus z_2 \oplus z_3 = xy$, with or without line L4.

*Proof.* The nine terms are the products $x_i y_j$ for all $i, j \in \{1, 2, 3\}$, each once: $z_1$ has $(2,2), (2,3), (3,2)$, $z_2$ has $(3,3), (1,3), (3,1)$, and $z_3$ has $(1,1), (1,2), (2,1)$. Their XOR is $(x_1 \oplus x_2 \oplus x_3)(y_1 \oplus y_2 \oplus y_3) = xy$ by the distributive law over GF(2). Line L4 adds $r_1 \oplus r_2 \oplus (r_1 \oplus r_2) = 0$. $\square$

**Theorem 2 (non-completeness).** For each $i$, the function that computes $z_i$, with line L4 included, does not read $x_i$ or $y_i$.

*Proof.* By inspection of the terms above; line L4 adds only $r_1$, $r_2$ or both. $\square$

**Lemma 3.** For a uniform sharing $(x_1, x_2, x_3)$ of $x$, any two shares are independent uniform bits, whatever $x$ is.

*Proof.* $(x_1, x_2)$ is uniform by assumption. $x_3 = (x \oplus x_1) \oplus x_2$ with $x_2$ uniform and independent of $x_1$, so given $x_1$ the bit $x_3$ is uniform; hence $(x_1, x_3)$ is uniform. The case $(x_2, x_3)$ is the same with $x_1$ and $x_2$ exchanged. $\square$

**Theorem 4 (one glitch-extended probe).** Model a glitch on output share $i$ as a probe that sees all the inputs of the logic of $z_i$: $V_1 = (x_2, x_3, y_2, y_3, r_1)$, $V_2 = (x_1, x_3, y_1, y_3, r_2)$ and $V_3 = (x_1, x_2, y_1, y_2, r_1, r_2)$, without the $r$ when line L4 is not used. The distribution of each $V_i$ is the same for all four pairs $(x, y)$, and so is the distribution of every function of $V_i$, which includes every value that a glitch on $z_i$ can take.

*Proof.* By Lemma 3, the two shares of $x$ in $V_i$ are uniform and independent, and so are the two shares of $y$. The shares of $x$, the shares of $y$ and the bits $r$ are mutually independent. So $V_i$ is uniform on its range, whatever $(x, y)$ is. A function of a random variable whose law does not depend on $(x, y)$ also has a law that does not depend on $(x, y)$. $\square$

**Theorem 5 (uniformity with fresh bits).** With line L4, for each $(x, y)$, the output $(z_1, z_2, z_3)$ is uniform on the four sharings of $xy$.

*Proof.* Let $(w_1, w_2, w_3)$ be the output of lines L1 to L3, a random sharing of $xy$ by Theorem 1, independent of $(r_1, r_2)$. The output after line L4 is $(w_1 \oplus r_1, w_2 \oplus r_2, w_3 \oplus r_1 \oplus r_2)$. For fixed $w$, the map $(r_1, r_2) \mapsto (w_1 \oplus r_1, w_2 \oplus r_2)$ is a bijection onto $\{0, 1\}^2$, and the third share is fixed by the other two and by $xy$. So given $w$, the output is uniform on the four sharings of $xy$, and that law does not depend on $w$. $\square$

**Proposition 6 (no uniformity without fresh bits).** Without line L4, for $(x, y) = (1, 1)$ the sharing $(1, 1, 1)$ of $xy = 1$ has probability $\frac{1}{16}$, not $\frac14$, so the output is not uniform. The pair $(z_1, z_2)$ has a law for $(x, y) = (0, 0)$ that differs from its law for $(1, 1)$.

*Proof.* There are $4 \times 4 = 16$ equally likely pairs of input sharings. For $x = y = 1$, the output is $(1, 1, 1)$ only if $z_1 = z_2 = 1$. Listing the 16 cases gives exactly one, $x = (1, 1, 1)$ and $y = (1, 1, 1)$: then $z_1 = 1 \oplus 1 \oplus 1 = 1$ and likewise $z_2 = z_3 = 1$. For every other case at least one of $z_1, z_2$ is 0; the tests enumerate the cases and find the counts 5, 5, 5 and 1 for the sharings $(0,0,1)$, $(0,1,0)$, $(1,0,0)$ and $(1,1,1)$. For $(x, y) = (0, 0)$, the counts are 7, 3, 3 and 3 for $(0,0,0)$, $(0,1,1)$, $(1,0,1)$ and $(1,1,0)$. The pair $(z_1, z_2) = (1, 1)$ then has probability $\frac{3}{16}$ for $(0, 0)$ and $\frac{1}{16}$ for $(1, 1)$. $\blacksquare$

So lines L1 to L6 with the fresh bits give a correct and non-complete sharing that resists one glitch-extended probe for uniform input sharings, and whose output is a uniform sharing that the next stage can use with the same argument. The code computes the same expressions, and its tests enumerate all input sharings and random bits to confirm each statement.
