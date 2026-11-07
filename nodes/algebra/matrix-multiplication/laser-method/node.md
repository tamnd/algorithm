---
tag: YHCGHF
kind: technique
slug: laser-method
name: Laser method
aliases:
- Coppersmith-Winograd laser method
- Strassen's laser method
area: algebra/matrix-multiplication
level: research
summary: Take a high power of a small tensor of low border rank, zero out blocks by type and by hashing into a 3-AP-free set until a direct sum of matrix products is left, then apply Schönhage's inequality.
prereqs: [schonhage-asymptotic-sum-inequality, border-rank, shannon-entropy]
see_also: [coppersmith-winograd-algorithm, matrix-multiplication-exponent, matrix-multiplication-tensor, multinomial-coefficient, universal-hashing, asymptotic-equipartition-property, stirling-approximation, tensor-rank]
sources:
  - paper: "Volker Strassen, Relative bilinear complexity and matrix multiplication, Journal für die reine und angewandte Mathematik 375/376 (1987)"
    locator: pp. 406 to 443 (the laser method, degenerations of tensor powers to direct sums of matrix products, and ω < 2.479)
  - paper: doi:10.1016/S0747-7171(08)80013-2
    title: Don Coppersmith and Shmuel Winograd, Matrix multiplication via arithmetic progressions, Journal of Symbolic Computation 9(3) (1990)
    locator: pp. 251 to 280 (the hashing into sets without three-term arithmetic progressions, the easy and complete constructions, and ω < 2.375477 from the square of the tensor)
  - paper: doi:10.4086/toc.gs.2013.005
    title: Markus Bläser, Fast Matrix Multiplication, Theory of Computing Graduate Surveys 5 (2013)
    locator: the sections on the laser method and on the Coppersmith and Winograd tensor (a full proof of the easy and complete bounds)
  - book: isbn:9783540605829
    title: Peter Bürgisser, Michael Clausen and M. Amin Shokrollahi, Algebraic Complexity Theory, Springer, Grundlehren der mathematischen Wissenschaften 315 (1997)
    locator: Chapter 15 (the laser method, tight sets and the proof of ω < 2.38)
  - paper: "Felix A. Behrend, On sets of integers which contain no three terms in arithmetical progression, Proceedings of the National Academy of Sciences of the USA 32(12) (1946)"
    locator: pp. 331 to 332 (subsets of 1..M of size M exp(−O(sqrt(log M))) with no three-term progression)
  - paper: doi:10.1145/2213977.2214056
    title: Virginia Vassilevska Williams, Multiplying matrices faster than Coppersmith-Winograd, STOC 2012
    locator: pp. 887 to 898 (the laser method on higher powers of the CW tensor, with values of blocks that are not matrix products)
  - paper: "Andris Ambainis, Yuval Filmus and François Le Gall, Fast matrix multiplication: limitations of the Coppersmith-Winograd method, 47th ACM Symposium on Theory of Computing (STOC 2015)"
    locator: the main theorem (the laser method on powers of the CW tensor in this form cannot give ω < 2.3078)
  - paper: "Ran Duan, Hongxun Wu and Renfei Zhou, Faster matrix multiplication via asymmetric hashing, 64th IEEE Symposium on Foundations of Computer Science (FOCS 2023), arXiv:2210.10173"
    locator: the main theorem and the asymmetric hashing step (ω < 2.371866)
---

The laser method is the technique behind every upper bound on the [exponent ω](/matrix-multiplication-exponent/) since 1986. It starts with a small tensor $T$ of low [border rank](/border-rank/) whose pieces are matrix products, but which is not itself a direct sum of them, because the pieces share variables. In a high Kronecker power $T^{\otimes N}$ it sets most variable blocks to zero, first by their type and then by a random hash into a set without three-term arithmetic progressions, until what is left is a direct sum of many independent matrix products. [Schönhage's asymptotic sum inequality](/schonhage-asymptotic-sum-inequality/) then turns the count and the size of these products into a bound on ω. Strassen introduced it in 1986 and got $\omega < 2.479$; Coppersmith and Winograd added the hashing and their tensor in 1990 and got $\omega < 2.376$. The resulting algorithms are galactic.

## In plain words

Some small computations do several matrix products at once, cheaply, but the products overlap: they share inputs. Overlapping products are no good for a bound on ω, which needs separate products.

Take many copies of the small computation and combine them into one huge computation. Its pieces overlap in a very regular way. Now throw away inputs, by setting them to zero, chosen so that the pieces that survive no longer overlap. A clever random choice keeps almost as many pieces as there are input blocks. The pieces that survive are separate matrix products, all computed by the huge computation, and Schönhage's inequality says what that is worth.

## When it applies

The method needs a tensor $T$ over a field $F$ with three properties.

- **Low border rank.** $\underline{R}(T) \le r$, with $r$ close to the dimensions of $T$. Then $\underline{R}(T^{\otimes N}) \le r^N$.
- **A block structure.** The variables split as $X = \bigoplus_{I} X_I$, $Y = \bigoplus_{J} Y_J$, $Z = \bigoplus_{K} Z_K$, and $T = \sum_{(I, J, K) \in S} T_{IJK}$, where $T_{IJK}$ uses only $X_I$, $Y_J$ and $Z_K$ and is (isomorphic to) a matrix product $\langle n_b, m_b, p_b \rangle$, or more generally has a known value $V_b$. Write $b = (I, J, K)$ for an element of the support $S$.
- **Tightness.** There is an integer $c$ with $I + J + K = c$ for all $(I, J, K) \in S$, with the block indices read as integers. This makes the hashing step work. A support with this property is called tight.

The method then gives, for each probability distribution $P$ on $S$ that is determined by its three marginals $P_X$, $P_Y$, $P_Z$:

$$\log_2 r \;\ge\; \min\{H(P_X), H(P_Y), H(P_Z)\} + \sum_{b \in S} P(b) \cdot \frac{\omega}{3} \log_2 (n_b m_b p_b),$$

where $H$ is the [Shannon entropy](/shannon-entropy/). Solving for ω and optimizing over $P$ gives the bound. When $P$ is not determined by its marginals, a penalty term $H(P') - H(P)$ for the worst competing distribution $P'$ with the same marginals is subtracted on the right.

## The template

```pseudo id=main
LASER-METHOD(T, S, P, N)                ▷ T of border rank r with tight block support S
L1  T_N ← T^{⊗N}, of border rank at most r^N
L2  view T_N as a sum over block triples (I, J, K) ∈ S^N, with I = (I_1, …, I_N)
L3  zero out each X-block I whose type is not P_X; the same for Y with P_Y and Z with P_Z
L4  choose a prime M and a set B ⊆ Z_M with no three-term progression, |B| = M^(1−o(1))
L5  choose w_0, w_1, …, w_N uniformly at random in Z_M
L6  h_X(I) ← w_0 + Σ_t w_t I_t ;  h_Z(K) ← w_0 + Σ_t w_t K_t ;  h_Y(J) ← w_0 + 2^(−1) Σ_t w_t (c − J_t)
L7  zero out each block whose hash is not in B
L8  for each pair of surviving triples that share a block, zero out that block
L9  the surviving triples are disjoint: T_N has degenerated to a direct sum of e matrix products
L10 apply the asymptotic sum inequality to the direct sum, with border rank at most r^N
```

**Why each step is sound.**

- *Zeroing out is free.* Setting a block of variables to zero is a restriction, so it does not raise border rank. After L3 and L7, every triple that contains a zeroed block is gone; the others are unchanged.
- *Types (L3).* The type of a sequence $I$ is the vector of frequencies of its entries. If $P$ is determined by its marginals, then every triple $(I, J, K) \in S^N$ whose three blocks have types $P_X$, $P_Y$, $P_Z$ has joint type $P$. So after L3 every surviving triple is a Kronecker product of the same multiset of blocks, and each is a matrix product $\langle \prod_t n_{b_t}, \prod_t m_{b_t}, \prod_t p_{b_t} \rangle$ of the same size, with $nmp = \prod_b (n_b m_b p_b)^{N P(b)}$.
- *The hash (L6).* For every triple in the support, $I_t + J_t + K_t = c$ for each $t$, so $h_X(I) + h_Z(K) = 2 w_0 + \sum_t w_t (c - J_t) = 2 h_Y(J)$. The three hash values of a triple form a three-term progression in $\mathbb{Z}_M$. If all three lie in $B$, which has no nontrivial progression, they are equal. So after L7, a triple survives only when its three blocks have the same hash, and two triples that share a block live in the same hash class.
- *Counting (L8).* Let $n_X$ be the number of X-blocks of type $P_X$, about $2^{N H(P_X)}$ by [Stirling's approximation](/stirling-approximation/), and in the symmetric case let each block lie in $d$ triples of joint type $P$, so there are $n_X d$ triples and at most $3 n_X d^2 / 2$ pairs of triples that share a block. Coppersmith and Winograd show that the hash values are independent enough that a fixed triple survives L7 with probability $|B| / M^2$, and a fixed pair of triples that share a block survives with probability at most $|B| / M^3$. Zeroing out a shared block in L8 removes at most two triples per such pair. With $M$ about $6d$, the expected number of disjoint triples left is at least $n_X d |B| / M^2 - 3 n_X d^2 |B| / M^3 = n_X |B| / (12 M)$. By Behrend's construction $|B| \ge M e^{-O(\sqrt{\log M})}$, so this is $2^{N H(P_X) - o(N)}$.
- *The bound (L10).* With $e = 2^{N H(P_X) - o(N)}$ disjoint copies of a product with $nmp$ as above, the asymptotic sum inequality gives $e \, (nmp)^{\omega/3} \le r^N$. Take logarithms, divide by $N$ and let $N \to \infty$. This gives the inequality of the previous section. If the three marginal entropies differ, the smallest one limits the count.

## Classic examples

1. **The easy Coppersmith-Winograd tensor.** For $q \ge 1$, $T = \sum_{i=1}^{q} (x_0 y_i z_i + x_i y_0 z_i + x_i y_i z_0)$, with blocks $X_0 = \{x_0\}$, $X_1 = \{x_1, \ldots, x_q\}$ and the same for $Y$ and $Z$. The support is $\{(0, 1, 1), (1, 0, 1), (1, 1, 0)\}$, tight with $c = 2$, and each block is a product with $nmp = q$, for example $x_0 y_i z_i$ is $\langle 1, 1, q \rangle$. Its border rank is at most $q + 2$. With $P$ uniform, $P_X = (1/3, 2/3)$ and $H(P_X) = \log_2 3 - 2/3$. The inequality reads $q^{\omega/3} \le (q+2) \cdot 2^{2/3} / 3$, that is
$$\omega \le \log_q \frac{4 (q+2)^3}{27}.$$
At $q = 8$ this is $\log_8 4000 \approx 2.4036$, the best integer value of $q$.
2. **The complete Coppersmith-Winograd tensor.** Adding $x_0 y_0 z_{q+1} + x_0 y_{q+1} z_0 + x_{q+1} y_0 z_0$ keeps the border rank at $q + 2$ and adds the blocks $(0, 0, 2)$, $(0, 2, 0)$, $(2, 0, 0)$, each $\langle 1, 1, 1 \rangle$. Put weight $\alpha$ on each of the three old blocks and $1/3 - \alpha$ on each new one. The marginals are $(2/3 - \alpha, 2\alpha, 1/3 - \alpha)$, and they determine $P$. The inequality gives
$$\omega \le \frac{\log_2(q+2) - H(2/3 - \alpha, 2\alpha, 1/3 - \alpha)}{\alpha \log_2 q},$$
which a script minimized over $\alpha$ on a grid of step $10^{-5}$: the best is $q = 6$, $\alpha \approx 0.3173$, $\omega < 2.3872$. The details are on the [Coppersmith-Winograd algorithm](/coppersmith-winograd-algorithm/) page.
3. **The square of the tensor.** Coppersmith and Winograd applied the method to $T^{\otimes 2}$ with a coarser block structure, in which some blocks are not matrix products and get values computed by the method itself. This gave $\omega < 2.375477$. Stothers, Vassilevska Williams and Le Gall did the same for the powers $4$, $8$, $16$ and $32$, which gave the bounds near $2.3729$ in the table on the [exponent](/matrix-multiplication-exponent/) page.
4. **A toy run.** For the easy tensor and $N = 9$, the support of $T^{\otimes 9}$ restricted to the uniform type has $1680$ triples on $84$ X-blocks. A run of the template with $M = 29$ and the progression-free set $B = \{0, 1, 3, 4, 9, 10, 12, 13\}$ in $\mathbb{Z}_{29}$, with the best of $40$ random seeds, kept $42$ triples after L7 and $4$ disjoint triples after L8. The script checked that the three hashes of each support triple form a progression mod $29$ and that the $4$ triples left are disjoint and no other support triple uses only their blocks. For $N = 3$ an exhaustive search shows that at most $2$ of the $6$ triples can be kept. Such small sizes lose most of the blocks: the $2^{-o(N)}$ losses only become negligible for very large $N$.

## Variations

- **Strassen's original form.** Strassen (1986, published 1987) used powers of the tensor $\sum_{i=1}^{q} (x_0 y_i z_i + x_i y_0 z_i)$, of border rank $q + 1$ since $\sum_i (x_0 + \varepsilon x_i)(y_0 + \varepsilon y_i) z_i - x_0 y_0 \sum_i z_i$ equals $\varepsilon$ times it up to $O(\varepsilon^2)$, and degenerations without the hashing step, and obtained $\omega < 2.479$. The hashing with progression-free sets is due to Coppersmith and Winograd.
- **Values of non-matrix blocks.** In powers of the CW tensor, merged blocks are not matrix products. Their value $V_\tau$ is bounded by applying the method to them recursively, which is the computational core of the analyses since 2010.
- **Refined laser method.** Alman and Vassilevska Williams (2021) avoided some of the losses of zeroing out by allowing triples that share blocks in a controlled way, and got $\omega < 2.3728596$.
- **Asymmetric hashing.** Duan, Wu and Zhou (2023) let the X, Y and Z sides be treated differently in the hashing, which lifts the restriction behind the barrier below, and got $\omega < 2.371866$. Later papers refined this to $2.371552$ and $2.371339$.
- **Rectangular products.** The same method with unequal treatment of the three sides bounds $\omega(1, k, 1)$ and the dual exponent α.

## Pitfalls

- **Border rank, not rank.** The bound uses $\underline{R}(T)$, and the final algorithm must be made exact by the interpolation of the [border rank](/border-rank/) page, which multiplies the cost by a polynomial in $N$. This is harmless for the exponent but adds to the galactic constants.
- **Marginals that do not determine $P$.** If other joint types share the marginals of $P$, the surviving triples are a mixture, and the count must subtract the extra entropy. Forgetting the penalty overstates the gain.
- **Wrap-around.** The set $B$ must have no three-term progression modulo $M$, not only in the integers. A Behrend set inside $[0, M/2)$ works for odd $M$, since then $u + w = 2v$ in $\mathbb{Z}_M$ implies it in $\mathbb{Z}$.
- **The hash on $Y$.** With $I + J + K = c$, the correct hash for $Y$ uses $c - J_t$ and the inverse of $2$, so $M$ must be odd. Using the same linear form on all three sides breaks the progression property.
- **Small $N$ tells little.** The toy run keeps $4$ of $84$ blocks. The bounds are limits as $N \to \infty$ and say nothing useful about any concrete size.
- **Barriers.** Ambainis, Filmus and Le Gall (2015) proved that the method in the form used up to 2014, applied to any power of the CW tensor, cannot give $\omega < 2.3078$. Later results of Alman and Vassilevska Williams extended such limits. These are limits of the method, not of ω.

## Exercises

1. Check that for the easy CW tensor with uniform $P$ the marginal entropy is $\log_2 3 - 2/3$, and derive $\omega \le \log_q (4(q+2)^3/27)$. Show that $q = 8$ is the best integer.
2. Show that if the easy CW tensor with $q = 2$ had border rank $3$ instead of at most $4$, the same calculation would give $\omega = 2$. (Coppersmith and Winograd made this observation; a flattening shows that the border rank is at least $3$.)
3. For the complete CW tensor, show that the six numbers $P(b)$ are determined by the three marginals.
4. Prove that $h_X(I) + h_Z(K) = 2 h_Y(J)$ for every triple of $S^N$, and that for two distinct X-blocks the pair of hash values is uniform on $\mathbb{Z}_M^2$.
5. Show that zeroing out cannot raise border rank, and that after L3 every surviving triple is the same matrix product up to a permutation of indices.

## References
