---
tag: JJYQ7P
kind: theorem
slug: schonhage-asymptotic-sum-inequality
name: Schönhage's asymptotic sum inequality
aliases:
- Schönhage's theorem
- asymptotic sum inequality
- Schönhage's τ-theorem
- tau theorem
area: algebra/matrix-multiplication
level: research
summary: If a direct sum of products ⟨n_i,m_i,p_i⟩ has border rank at most r, then Σ (n_i m_i p_i)^(ω/3) ≤ r; many small independent products computed together bound ω.
prereqs: [border-rank, matrix-multiplication-tensor, matrix-multiplication-exponent]
see_also: [laser-method, coppersmith-winograd-algorithm, tensor-rank, bilinear-complexity, multinomial-coefficient, strassen-algorithm]
sources:
  - paper: doi:10.1137/0210032
    title: Arnold Schönhage, Partial and total matrix multiplication, SIAM Journal on Computing 10(3) (1981)
    locator: pp. 434 to 455 (the asymptotic sum inequality, the example ⟨k,1,k⟩ ⊕ ⟨1,(k−1)^2,1⟩ of border rank k^2 + 1, and ω < 2.522)
  - book: isbn:9783540605829
    title: Peter Bürgisser, Michael Clausen and M. Amin Shokrollahi, Algebraic Complexity Theory, Springer, Grundlehren der mathematischen Wissenschaften 315 (1997)
    locator: Chapter 15, Asymptotic complexity of matrix multiplication (the τ-theorem and its proof by tensor powers)
  - paper: doi:10.4086/toc.gs.2013.005
    title: Markus Bläser, Fast Matrix Multiplication, Theory of Computing Graduate Surveys 5 (2013)
    locator: the section on the asymptotic sum inequality (statement, proof and Schönhage's example)
  - paper: doi:10.1016/S0747-7171(08)80013-2
    title: Don Coppersmith and Shmuel Winograd, Matrix multiplication via arithmetic progressions, Journal of Symbolic Computation 9(3) (1990)
    locator: pp. 251 to 280 (the inequality as the final step after the laser method has found many independent products)
  - paper: "Volker Strassen, Relative bilinear complexity and matrix multiplication, Journal für die reine und angewandte Mathematik 375/376 (1987)"
    locator: pp. 406 to 443 (the laser method, which turns a tensor power into a direct sum of matrix products to which the inequality is applied)
---

Schönhage's asymptotic sum inequality says that an algorithm that computes several independent matrix products at once bounds the [exponent ω](/matrix-multiplication-exponent/), even when no single product in the sum is computed efficiently. If the direct sum $\bigoplus_{i=1}^{s} \langle n_i, m_i, p_i \rangle$ has [border rank](/border-rank/) at most $r$, then $\sum_i (n_i m_i p_i)^{\omega/3} \le r$. It is the step that turns every modern construction into a bound on ω: the [laser method](/laser-method/) and the [Coppersmith-Winograd algorithm](/coppersmith-winograd-algorithm/) find a large direct sum of matrix products inside a power of a small tensor, and this inequality converts it into the exponent. Schönhage proved it in 1981 and used it to show $\omega < 2.522$.

## Statement

Let $F$ be a field, let $\langle n, m, p \rangle$ be the [matrix multiplication tensor](/matrix-multiplication-tensor/) of the $n \times m$ by $m \times p$ product, and let $e \odot T = T \oplus \cdots \oplus T$ denote the direct sum of $e$ copies of $T$, on disjoint sets of variables. $\underline{R}$ is the border rank and $\omega = \omega(F)$.

**Theorem (asymptotic sum inequality).** Let $s \ge 1$ and $n_i, m_i, p_i \ge 1$ for $i = 1, \ldots, s$. If
$$\underline{R}\Big(\bigoplus_{i=1}^{s} \langle n_i, m_i, p_i \rangle\Big) \le r, \quad \text{then} \quad \sum_{i=1}^{s} (n_i m_i p_i)^{\omega/3} \le r.$$

Equivalently, if $\tau$ is the number with $\sum_i (n_i m_i p_i)^{\tau} = r$, then $\omega \le 3\tau$. For $s = 1$ it is the known bound $\omega \le 3 \log r / \log(nmp)$. The case of equal summands reads: $\underline{R}(e \odot \langle n, m, p \rangle) \le r$ implies $e \, (nmp)^{\omega/3} \le r$.

## In plain words

Suppose that one method computes several matrix products at the same time, with separate inputs and outputs for each, using $r$ multiplications in total. This may be cheaper than computing them one by one, because the method can share work between them.

The theorem says how much such a shared method is worth. Each product of size $n \times m$ by $m \times p$ is worth $(nmp)^{\omega/3}$ multiplications, which is what a best possible method for it alone would need for very large sizes. If the total worth exceeds $r$, the exponent ω must be smaller than assumed. So a cheap shared method proves that ω is small.

## Proof

All tensors of border rank at most $r$ are degenerations of the unit tensor $\langle r \rangle = r \odot \langle 1, 1, 1 \rangle$, and border rank does not grow under restrictions (in particular under the projection onto a direct summand), is submultiplicative under the Kronecker product $\otimes$, and is subadditive under $\oplus$. We use the fact, proved on the [border rank](/border-rank/) page, that $\underline{R}(\langle N, N, N \rangle) \le b$ implies $\omega \le \log b / \log N$. In this proof $\langle r \rangle$ with one argument always means the unit tensor.

**Step 1 (equal square summands).** *If $\underline{R}(e \odot \langle n, n, n \rangle) \le r$, then $e \, n^{\omega} \le r$.*

Let $a = \lceil r / e \rceil$. We show $\underline{R}(e \odot \langle n^k, n^k, n^k \rangle) \le a^k e$ for all $k \ge 1$ by induction. For $k = 1$, $r \le a e$. For the step, $e \odot \langle n^{k+1}, n^{k+1}, n^{k+1} \rangle = (e \odot \langle n, n, n \rangle) \otimes \langle n^k, n^k, n^k \rangle$. The first factor is a degeneration of the unit tensor $\langle r \rangle$, so the product is a degeneration of $\langle r \rangle \otimes \langle n^k, n^k, n^k \rangle = r \odot \langle n^k, n^k, n^k \rangle$. Since $r \le a e$, this is a restriction of $a \odot (e \odot \langle n^k, n^k, n^k \rangle)$, which by subadditivity and the induction hypothesis has border rank at most $a \cdot a^k e$.

A single copy is a restriction of $e$ copies, so $\underline{R}(\langle n^k, n^k, n^k \rangle) \le a^k e$ and $\omega \le (k \log a + \log e) / (k \log n)$ for every $k$. Letting $k \to \infty$ gives $n^{\omega} \le a = \lceil r/e \rceil$.

To remove the ceiling, apply this to the $N$-th Kronecker power: $\underline{R}(e^N \odot \langle n^N, n^N, n^N \rangle) \le r^N$, so $n^{N \omega} \le \lceil (r/e)^N \rceil \le (r/e)^N + 1$. Since $r \ge e$ (the $e$ copies have $e$ linearly independent outputs), taking $N$-th roots and $N \to \infty$ gives $n^{\omega} \le r / e$.

**Step 2 (equal rectangular summands).** *If $\underline{R}(e \odot \langle n, m, p \rangle) \le r$, then $e \, (nmp)^{\omega/3} \le r$.*

By the cyclic symmetry of matrix multiplication tensors, $e \odot \langle m, p, n \rangle$ and $e \odot \langle p, n, m \rangle$ also have border rank at most $r$. Their Kronecker product with $e \odot \langle n, m, p \rangle$ is $e^3 \odot \langle nmp, nmp, nmp \rangle$, since $\langle n, m, p \rangle \otimes \langle m, p, n \rangle \otimes \langle p, n, m \rangle = \langle nmp, nmp, nmp \rangle$ and $\odot$ distributes over $\otimes$. Its border rank is at most $r^3$, so Step 1 gives $e^3 (nmp)^{\omega} \le r^3$.

**Step 3 (the general sum).** Let $T = \bigoplus_{i=1}^{s} \langle n_i, m_i, p_i \rangle$ and $q_i = n_i m_i p_i$. The $N$-th Kronecker power expands by distributivity:
$$T^{\otimes N} = \bigoplus_{c} \binom{N}{c_1, \ldots, c_s} \odot \Big\langle \prod_i n_i^{c_i}, \prod_i m_i^{c_i}, \prod_i p_i^{c_i} \Big\rangle,$$
where $c = (c_1, \ldots, c_s)$ runs over the vectors of nonnegative integers with $\sum_i c_i = N$, and the [multinomial coefficient](/multinomial-coefficient/) counts the ordered choices of factors that give the same shape. Each part is a direct summand of $T^{\otimes N}$, so it has border rank at most $r^N$. Step 2 gives, for each $c$,
$$\binom{N}{c_1, \ldots, c_s} \prod_i q_i^{c_i \omega / 3} \le r^N.$$
There are $\binom{N + s - 1}{s - 1} \le (N + 1)^{s}$ vectors $c$. Summing over $c$ and using the multinomial theorem,
$$\Big(\sum_{i=1}^{s} q_i^{\omega/3}\Big)^N = \sum_c \binom{N}{c_1, \ldots, c_s} \prod_i q_i^{c_i \omega/3} \le (N+1)^{s} \, r^N.$$
Taking $N$-th roots, $\sum_i q_i^{\omega/3} \le (N + 1)^{s/N} r$, and $(N+1)^{s/N} \to 1$ as $N \to \infty$. $\square$

The proof never needs to know ω: it shows that each $\tau$ with $\sum_i q_i^{\tau} > r$ satisfies $\omega < 3\tau$, by building exact algorithms from ever larger powers.

## Consequences

- **Schönhage's example.** For $k \ge 2$, $\underline{R}(\langle k, 1, k \rangle \oplus \langle 1, (k-1)^2, 1 \rangle) \le k^2 + 1$, with the identity given on the [border rank](/border-rank/) page. The rank of each part alone is $k^2$ and $(k-1)^2$, so the sum is far cheaper than the parts. The theorem gives $k^{2\omega/3} + (k-1)^{2\omega/3} \le k^2 + 1$. Solving for the best $k$, computed by bisection:

  | $k$ | $r = k^2 + 1$ | bound on ω |
  |---|---|---|
  | 2 | 5 | 3 |
  | 3 | 10 | 2.5939 |
  | 4 | 17 | 2.5480 |
  | 5 | 26 | 2.5507 |
  | 6 | 37 | 2.5629 |

  So $k = 4$ gives $\omega < 2.548$. At $\omega = \log_2 7$ the left side for $k = 4$ is about $21.2 > 17$, which shows directly that Strassen's exponent is not optimal. Neither part alone gives anything: $\langle k, 1, k \rangle$ and $\langle 1, (k-1)^2, 1 \rangle$ each have $nmp$ at most $k^2$ and rank equal to $nmp$, which gives only $\omega \le 3$. Schönhage obtained $2.522$ from a more elaborate construction in the same paper.
- **Many copies.** $\underline{R}(e \odot \langle n, n, n \rangle) \le r$ gives $e \, n^{\omega} \le r$. So computing $e$ independent products with fewer than $e$ times the cost of one proves that the cost of one is below $n^{\omega}$ for some smaller exponent. This is how the laser method uses it: it finds $e$ disjoint copies of a matrix product in a power of a tensor.
- **The final step of the laser method.** In the [laser method](/laser-method/), Strassen (1987) and [Coppersmith and Winograd](/coppersmith-winograd-algorithm/) (1990) show that a power $T^{\otimes N}$ of a tensor of border rank $r$ degenerates to a direct sum of about $V^N$ copies of matrix products of a fixed size; the theorem then gives the bound on ω. All bounds since 1986 end this way.
- **Rectangular exponents.** The same proof gives versions for the rectangular exponents $\omega(a, b, c)$, which are used to bound the dual exponent α.

## Tightness

- **The constant in the conclusion.** For the unit tensor $\langle r \rangle = r \odot \langle 1, 1, 1 \rangle$ both sides equal $r$, so the inequality cannot be improved by a constant factor in general.
- **Only in the limit.** The theorem gives an algorithm with exponent $3\tau + \delta$ for each $\delta > 0$, built from tensor powers of growing order, and not one with exponent exactly $3\tau$. Coppersmith and Winograd (1982) showed that no single bilinear algorithm attains ω, so the infimum in the definition of ω is never a minimum. The algorithms obtained from the theorem are galactic: the powers and the interpolation needed to make them exact pay off only for astronomically large $n$.
- **Border rank is needed for the gain.** With rank instead of border rank the statement also holds, since $\underline{R} \le R$, but Schönhage's example loses its point: its gain comes from the strict subadditivity of border rank on this direct sum.
- **No converse.** A bound on ω does not imply that a given direct sum has small border rank. The inequality only goes from algorithms to bounds on ω.

## History

Pan's trilinear aggregation (1978) already computed several products together and gave $\omega < 2.795$. Bini, Capovani, Romani and Lotti (1979) introduced approximate algorithms and border rank. Schönhage (1981), in *Partial and total matrix multiplication*, combined both ideas: he proved the asymptotic sum inequality, gave the example with border rank $k^2 + 1$, and proved $\omega < 2.522$. Romani (1982) and Coppersmith and Winograd (1982) improved the bound with the same inequality to $2.517$ and $2.496$. Strassen's laser method (1986, published in 1987) and the Coppersmith and Winograd tensor (1990) found the large direct sums that all later records feed into this inequality.

## References
