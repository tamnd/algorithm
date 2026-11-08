---
title: MRG32k3a has state period (m1^3 - 1)(m2^3 - 1)/2 and returns values in (0, 1) computed exactly
proves: [correctness]
status: full
---

Write $m_1 = 2^{32} - 209$ and $m_2 = 2^{32} - 22853$; both are prime, which the tests check. Lines L1 and L2 of MRG32K3A-NEXT replace the first component state $X_{1} = (x_{1,n-3}, x_{1,n-2}, x_{1,n-1})$ by $A_1 X_1 \bmod m_1$, and lines L3 and L4 replace $X_2$ by $A_2 X_2 \bmod m_2$, where

$$A_1 = \begin{pmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ -810728 & 1403580 & 0 \end{pmatrix}, \qquad A_2 = \begin{pmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ -1370589 & 0 & 527612 \end{pmatrix}.$$

These are the companion matrices of the recurrences $x_{1,n} = (1403580\, x_{1,n-2} - 810728\, x_{1,n-3}) \bmod m_1$ and $x_{2,n} = (527612\, x_{2,n-1} - 1370589\, x_{2,n-3}) \bmod m_2$, with characteristic polynomials

$$P_1(z) = z^3 - 1403580\, z + 810728 \pmod{m_1}, \qquad P_2(z) = z^3 - 527612\, z^2 + 1370589 \pmod{m_2}.$$

A seed is valid when $X_1 \in \{0, \ldots, m_1 - 1\}^3$ and $X_2 \in \{0, \ldots, m_2 - 1\}^3$ and neither is the zero vector.

**Lemma 1 (component periods).** $P_1$ is primitive modulo $m_1$ and $P_2$ is primitive modulo $m_2$. Hence, from every valid seed, component $j$ is purely periodic with period exactly $\rho_j = m_j^3 - 1$.

*Proof.* Knuth's criterion (TAOCP Volume 2, Section 3.2.2) says that $z^k - a_1 z^{k-1} - \cdots - a_k$ is primitive modulo a prime $m$ if and only if (i) $(-1)^{k-1} a_k$ is a primitive root modulo $m$, (ii) $z^r \equiv (-1)^{k-1} a_k$ modulo the polynomial, with $r = (m^k - 1)/(m - 1)$, and (iii) $z^{r/q}$ is not congruent to a constant for each prime $q$ dividing $r$. Here $k = 3$, so $(-1)^{k-1} a_3 = a_3$, which is $-810728 \bmod m_1$ and $-1370589 \bmod m_2$. The tests check (i) with the prime factors of $m_j - 1$, found by trial division, and (ii) by exact square and multiply on polynomials modulo $P_j$. For (iii), the tests check that $r_j = m_j^2 + m_j + 1$ is prime, by the Miller-Rabin test with the first 13 prime bases, which is exact below $3.3 \cdot 10^{24}$; so the only prime is $q = r_j$, and $z^{r_j / r_j} = z$ is not a constant because $\deg P_j = 3 > 1$. So both polynomials are primitive.

For a primitive $P_j$, the ring $\mathrm{GF}(m_j)[A_j]$ is isomorphic to the field $\mathrm{GF}(m_j)[z]/(P_j)$ with $A_j \mapsto z$, so $A_j$ has order $m_j^3 - 1$ and every non-zero element of the ring is invertible. For a non-zero $X$ with period $\rho$, the element $A_j^\rho - I$ kills $X$, so it is not invertible, hence zero, and $m_j^3 - 1$ divides $\rho$. Since also $A_j^{m_j^3 - 1} = I$, $\rho = m_j^3 - 1$. This is the theorem of the [multiple recursive generator](/multiple-recursive-generator/) page. $\square$

**Lemma 2 (the pair).** From every valid seed, the pair $(X_1, X_2)$ is purely periodic with period

$$\rho = \operatorname{lcm}(m_1^3 - 1, m_2^3 - 1) = \frac{(m_1^3 - 1)(m_2^3 - 1)}{2}, \qquad 2^{190} < \rho < 2^{191}.$$

*Proof.* The two components evolve independently. The pair returns to its start after $t > 0$ steps if and only if both components do, that is, if and only if $\rho_1 \mid t$ and $\rho_2 \mid t$ by Lemma 1, that is, if and only if $\operatorname{lcm}(\rho_1, \rho_2) \mid t$. Pure periodicity follows because each step is a bijection of the state set. Finally $\operatorname{lcm}(\rho_1, \rho_2) = \rho_1 \rho_2 / \gcd(\rho_1, \rho_2)$, and the tests compute $\gcd(\rho_1, \rho_2) = 2$ and the bounds with exact integers. $\square$

The output $u_n$ is a function of the pair state, so the output sequence is periodic and its period divides $\rho$. This proof does not show that the output period equals $\rho$; L'Ecuyer (1999) gives $\rho$ as the period of the generator, which is the usual statement.

**Lemma 3 (exact arithmetic).** The reference implementation in IEEE double precision computes the same integers $p_1$ and $p_2$ as lines L1 and L3, and the same output value.

*Proof.* Every state value is an integer below $2^{32}$. Each product in L1 and L3 is below $1403580 \cdot m_1 < 0.67 \cdot 2^{53}$, and the difference of two such products lies strictly between $-2^{53}$ and $2^{53}$. Integers of absolute value at most $2^{53}$ are exact doubles, and the double sum, difference and product of exact doubles are exact when the exact result is such an integer, so the reference code forms the exact integer $a x - b y$. Its reduction modulo $m_j$ by $k = \lfloor p/m_j \rfloor$, computed with a rounded division and then corrected by one step if negative, again uses only integers below $2^{53}$, so it gives the exact residue. The final output is one rounded product of the exact integer $p_1 - p_2$ or $p_1 - p_2 + m_1$, below $2^{33}$, by the double constant $\mathit{norm}$, and Python floats are IEEE doubles with the same rounding. $\square$

**Lemma 4 (range).** Every output satisfies $\mathit{norm} \le u_n \le m_1 \cdot \mathit{norm}$, so $0 < u_n < 1$.

*Proof.* If $p_1 > p_2$ (line L5), then $1 \le p_1 - p_2 \le m_1 - 1$. Otherwise (line L6) $p_2 - p_1 \in [0, m_2 - 1]$, so $p_1 - p_2 + m_1 \in [m_1 - m_2 + 1, m_1]$, and $m_1 - m_2 + 1 = 22645 \ge 1$. In both cases the integer $q$ that is multiplied by $\mathit{norm}$ satisfies $1 \le q \le m_1$. Here $\mathit{norm} = 2.328306549295728 \cdot 10^{-10}$, a double close to $1/(m_1 + 1)$, and the rounded product $m_1 \cdot \mathit{norm}$ is $0.99999999976716\ldots < 1$, which the tests check; rounding is monotone, so every $q \cdot \mathit{norm}$ lies in $[\mathit{norm}, m_1 \cdot \mathit{norm}]$. $\square$

**Theorem.** For every valid seed, MRG32K3A-NEXT runs in a constant number of word operations, its state sequence is purely periodic with period $(m_1^3 - 1)(m_2^3 - 1)/2 \approx 2^{191}$, each output lies in $(0, 1)$, and the values agree with the published double-precision implementation. The state $2^e$ steps ahead is $(A_1^{2^e} X_1 \bmod m_1, A_2^{2^e} X_2 \bmod m_2)$, which the tests check for $e = 76$ and $e = 127$ against the matrices printed in RngStream.c.

*Proof.* Lemmas 2, 3 and 4. The jump formula holds because each step multiplies by $A_j$ modulo $m_j$, and matrix multiplication modulo $m_j$ is associative, so $2^e$ steps multiply by $A_j^{2^e}$, which $e$ squarings compute. $\blacksquare$
