---
title: The powering construction has bias at most (n − 1)/2^m
proves: [correctness]
status: full
---

We use the notation of the page. $F = \mathrm{GF}(2^m)$ is the field of polynomials over $\mathrm{GF}(2)$ of degree less than $m$, with product modulo an irreducible polynomial of degree $m$. We identify each element of $F$ with its vector of $m$ coefficients. The seed $(x, y)$ is uniform on $F \times F$, and $b_0, \ldots, b_{n-1}$ is the output of SMALL-BIAS-GENERATOR.

**Lemma 1 (loop invariant).** At the start of iteration $i$ of line L4, $z = x^i$, with the convention $x^0 = 1$ for every $x$. So $b_i = \langle x^i, y \rangle$ for each $i$.

*Proof.* Line L3 sets $z = 1 = x^0$. Line L6 replaces $z = x^i$ by $z \cdot x = x^{i+1}$. Line L5 then computes $b_i = \langle z, y \rangle = \langle x^i, y \rangle$. $\square$

**Lemma 2 (linearity).** For $u, v, y \in F$, $\langle u + v, y \rangle = \langle u, y \rangle \oplus \langle v, y \rangle$.

*Proof.* The sum in $F$ adds coefficient vectors modulo 2, and $\langle \cdot, y \rangle = \bigoplus_j (\cdot)_j y_j$ is linear over $\mathrm{GF}(2)$ in its first argument. $\square$

**Lemma 3 (a fixed nonzero vector).** If $w \in F$ is not 0 and $y$ is uniform on $F$, then $\langle w, y \rangle$ is 0 and 1 with probability $1/2$ each.

*Proof.* Pick a coordinate $j$ with $w_j = 1$. Flipping $y_j$ is a bijection of $F$ that changes $\langle w, y \rangle$, so it pairs the $y$ with value 0 with the $y$ with value 1. $\square$

**Theorem.** For every nonempty $S \subseteq \{0, \ldots, n-1\}$,

$$\mathrm{E}_{x, y}\Big[(-1)^{\bigoplus_{i \in S} b_i}\Big] = \frac{r_S}{2^m}, \qquad 0 \le r_S \le n - 1,$$

where $r_S$ is the number of roots in $F$ of $p_S(t) = \sum_{i \in S} t^i$. So the bias of every nonempty parity is at most $(n-1)/2^m$, and the output space is $\varepsilon$-biased when $2^m \ge (n-1)/\varepsilon$.

*Proof.* By Lemma 1 and Lemma 2, applied $|S| - 1$ times,

$$\bigoplus_{i \in S} b_i = \bigoplus_{i \in S} \langle x^i, y \rangle = \Big\langle \sum_{i \in S} x^i, y \Big\rangle = \langle p_S(x), y \rangle.$$

Condition on $x$. Since $x$ and $y$ are independent, $y$ is still uniform.

- If $p_S(x) \ne 0$, Lemma 3 gives $\mathrm{E}_y[(-1)^{\langle p_S(x), y \rangle}] = 0$.
- If $p_S(x) = 0$, then $\langle 0, y \rangle = 0$ for every $y$, and $\mathrm{E}_y[(-1)^0] = 1$.

Averaging over the $2^m$ values of $x$ gives $\mathrm{E}[(-1)^{\text{parity}}] = r_S/2^m$.

It remains to bound $r_S$. The coefficients of $p_S$ are in $\{0, 1\} \subseteq F$, and the coefficient of $t^i$ is 1 exactly for $i \in S$. Since $S$ is nonempty, $p_S$ is not the zero polynomial, and its degree is $\max S \le n - 1$. A nonzero polynomial of degree $d$ over a field has at most $d$ roots, because each root $\alpha$ splits off a factor $t - \alpha$ and $F[t]$ has no zero divisors. So $r_S \le n - 1$. (For $S = \{0\}$, $p_S = 1$ has no root and the bit $b_0 = \langle 1, y \rangle$ is unbiased.) $\square$

**Corollary (seed length).** With $m = \lceil \log_2((n-1)/\varepsilon) \rceil$ for $n \ge 2$, $(n - 1)/2^m \le \varepsilon$, and the seed has $2m \le 2\log_2((n-1)/\varepsilon) + 2$ bits.

*Proof.* $2^m \ge (n-1)/\varepsilon$ by the choice of $m$, and $m < \log_2((n-1)/\varepsilon) + 1$. $\square$

**Remark (the irreducible modulus is needed).** The root bound uses that $F$ is a field. With the reducible modulus $t^2 + t$ and $m = 2$, the ring has 4 elements, each equal to its own square. Then $p_S(X) = X + X^2$ for $S = \{1, 2\}$ vanishes at all 4 elements, although its degree is 2, and the parity $b_1 \oplus b_2$ is always 0, with bias 1.
