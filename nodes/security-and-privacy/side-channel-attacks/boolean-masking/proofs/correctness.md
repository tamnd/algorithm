---
title: The masked S-box lookup is correct and secure against one probe, and the three-share linear map is secure against two probes
proves: [correctness]
status: full
---

Let $S$ be a permutation of $\{0, 1\}^w$, let $p$ be public and $k$ secret, and let $m_{in}$ and $m_{out}$ be independent and uniform on $\{0, 1\}^w$. The wires of MASKED-SBOX are $m_{in}$ and $m_{out}$ (line L1), $a = p \oplus m_{in}$ (L2), $x' = a \oplus k$ (L3), the table entries $T[u] = S(u \oplus m_{in}) \oplus m_{out}$ for every $u$ (L4) and $y' = T[x']$ (L5). A set of wires is secure if its joint distribution is the same for every $k$.

**Lemma 1.** If $m$ is uniform on $\{0, 1\}^w$ and independent of a random variable $Z$, then for every function $f$, the value $f(Z) \oplus m$ is uniform and independent of $Z$.

*Proof.* For each value $z$ of $Z$, the map $m \mapsto f(z) \oplus m$ is a bijection of $\{0, 1\}^w$, so given $Z = z$ the value $f(z) \oplus m$ is uniform. The conditional law does not depend on $z$, so it is also the law without the condition, and the two are independent. $\square$

**Theorem 1 (correctness).** Line L6 returns $(y', m_{out})$ with $y' \oplus m_{out} = S(p \oplus k)$ for all values of the masks.

*Proof.* $x' = p \oplus m_{in} \oplus k$, so $x' \oplus m_{in} = p \oplus k$. Then $y' = T[x'] = S(x' \oplus m_{in}) \oplus m_{out} = S(p \oplus k) \oplus m_{out}$. $\square$

**Theorem 2 (one probe).** Every single wire is secure.

*Proof.* The wires $m_{in}$, $m_{out}$ and $a = p \oplus m_{in}$ do not depend on $k$. The entry $T[u]$ is a function of $m_{in}$ and $m_{out}$ only, so it does not depend on $k$ either. By Lemma 1 with $m = m_{in}$ and $Z = k$, the wire $x' = (p \oplus k) \oplus m_{in}$ is uniform for every $k$. By Lemma 1 with $m = m_{out}$ and $Z = (k, m_{in})$, the wire $y' = S(p \oplus k) \oplus m_{out}$ is uniform for every $k$. $\square$

**Proposition 3 (two probes).** The pairs $(m_{in}, x')$, $(a, x')$ and $(m_{out}, y')$ are not secure if $S$ is not constant on the key space, which holds for a permutation. The pairs $(y', T[u])$ and $(x', T[u])$ are secure for every $u$.

*Proof.* $m_{in} \oplus x' = p \oplus k$, $a \oplus x' = k$ and $m_{out} \oplus y' = S(p \oplus k)$; each pair determines a value that takes different values for different keys, so the joint law depends on $k$. For $(y', T[u])$: write $y' = S(p \oplus k) \oplus m_{out}$ and $T[u] = S(u \oplus m_{in}) \oplus m_{out}$. Then $(y', T[u])$ is a bijective image of $(y', y' \oplus T[u]) = (S(p \oplus k) \oplus m_{out}, S(p \oplus k) \oplus S(u \oplus m_{in}))$. Since $S$ is a permutation and $m_{in}$ is uniform, $S(u \oplus m_{in})$ is uniform and independent of $m_{out}$; by Lemma 1 the second component is uniform for every $k$ and independent of $m_{out}$, and then by Lemma 1 again the first component is uniform and independent of the second. So the pair is uniform on $(\{0, 1\}^w)^2$ for every $k$. For $(x', T[u])$: $T[u]$ contains $m_{out}$, which appears in no other wire of the pair, so by Lemma 1 the pair is $(x', \text{a uniform value independent of } x')$, and $x'$ is uniform for every $k$ by Theorem 2. $\square$

The tests check all 210 pairs of the 21 wires for the PRESENT S-box and $p = \texttt{3}$ and find exactly the three pairs above.

**Proposition 4 (second-order leakage).** For a uniform $m \in \{0, 1\}^4$ and every $x$, $\mathrm{E}[\mathrm{HW}(x \oplus m)] = 2$ and $\mathrm{E}[(\mathrm{HW}(x \oplus m) - 2)(\mathrm{HW}(m) - 2)] = 1 - \mathrm{HW}(x)/2$.

*Proof.* By Lemma 1, $x \oplus m$ is uniform, and each of its 4 bits is 1 with probability $\frac12$. Write $u_q = m_q - \frac12$ for the bits $m_q$ of $m$. A bit of $x$ equal to 1 flips the bit of $m$, so $(x \oplus m)_q - \frac12 = (1 - 2x_q) u_q$. The $u_q$ are independent with mean 0 and $\mathrm{E}[u_q^2] = \frac14$, so the expectation of the product of $\sum_q (1 - 2x_q) u_q$ and $\sum_r u_r$ is $\frac14 \sum_q (1 - 2x_q) = 1 - \mathrm{HW}(x)/2$. $\square$

**Lemma 5.** Let $k_1$ and $k_2$ be independent and uniform on $\{0, 1\}^w$ and $k_3 = k \oplus k_1 \oplus k_2$. Then any two of $k_1, k_2, k_3$ are independent and uniform, for every $k$.

*Proof.* For $(k_1, k_2)$ this is the assumption. For $(k_1, k_3)$: $k_3 = (k \oplus k_1) \oplus k_2$ with $k_2$ uniform and independent of $k_1$, so by Lemma 1 $k_3$ is uniform and independent of $k_1$. The pair $(k_2, k_3)$ is the same with $k_1$ and $k_2$ exchanged. $\square$

**Theorem 6 (three shares, linear map).** Let $L$ be a GF(2)-linear map. The wires $k_1, k_2, k_3$, $x_1 = k_1 \oplus p$, $y_1 = L(x_1)$, $y_2 = L(k_2)$ and $y_3 = L(k_3)$ satisfy $y_1 \oplus y_2 \oplus y_3 = L(p \oplus k)$, and every set of at most two wires is secure.

*Proof.* By linearity, $y_1 \oplus y_2 \oplus y_3 = L(k_1 \oplus p \oplus k_2 \oplus k_3) = L(p \oplus k)$. Each wire is a function of one share and the public $p$: $k_1$, $x_1$ and $y_1$ of $k_1$, the wires $k_2$ and $y_2$ of $k_2$, and $k_3$ and $y_3$ of $k_3$. So a set of at most two wires is a function of at most two shares, and by Lemma 5 those shares have a law that does not depend on $k$. A function of them also has a law that does not depend on $k$. $\blacksquare$

The bound is tight: the three wires $k_1, k_2, k_3$ give $k$. The code applies the same operations, and its tests enumerate all masks to confirm Theorems 1, 2 and 6 and Proposition 3 for the stated S-box and map.
