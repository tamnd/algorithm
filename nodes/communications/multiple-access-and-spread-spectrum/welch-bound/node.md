---
tag: VC75JC
kind: theorem
slug: welch-bound
name: Welch bound
aliases:
- Welch bound on correlation
area: communications/multiple-access-and-spread-spectrum
level: advanced
summary: "Among K unit vectors in C^N, some two have squared inner product at least (K - N)/(N(K - 1)). So M sequences of length N and energy N have a correlation of at least N sqrt((M - 1)/(MN - 1))."
prereqs: [cross-correlation, autocorrelation]
see_also: [gold-sequences, kasami-sequences, zadoff-chu-sequence, maximal-length-sequence, code-division-multiple-access, ovsf-codes, multiuser-detection, barker-code]
sources:
  - paper: doi:10.1109/TIT.1974.1055219
    title: Lloyd R. Welch, Lower bounds on the maximum cross correlation of signals, IEEE Transactions on Information Theory 20(3), 1974
    locator: pp. 397 to 399 (the bound on the largest inner product of K unit vectors and its application to sets of sequences and their shifts)
  - paper: doi:10.1109/PROC.1980.11697
    title: Dilip V. Sarwate and Michael B. Pursley, Crosscorrelation properties of pseudorandom and related sequences, Proceedings of the IEEE 68(5), 1980
    locator: pp. 593 to 619 (the comparison of Gold and Kasami families with the Welch bound)
---

The Welch bound says that a set of many vectors in a space of small dimension cannot have all its inner products small. For $K$ unit vectors in $\mathbb{C}^N$, some pair has squared inner product at least $(K - N)/(N(K - 1))$. Applied to $M$ sequences of length $N$ and all their cyclic shifts, it gives the lower bound $N\sqrt{(M-1)/(MN-1)}$, about $\sqrt N$, on the largest periodic [cross-correlation](/cross-correlation/) or off-peak [autocorrelation](/autocorrelation/). It is the standard yardstick for the spreading-code families of CDMA, such as [Gold](/gold-sequences/) and [Kasami](/kasami-sequences/) sequences. Equality holds exactly for the sets that are both tight and equiangular. Welch proved the bound in 1974.

## Statement

**Theorem (Welch 1974).** Let $x_1, \ldots, x_K$ be vectors in $\mathbb{C}^N$ with $\|x_i\| = 1$, and let $c_{\max} = \max_{i \ne j} |\langle x_i, x_j \rangle|$, with $K \ge 2$. Then

$$c_{\max}^2 \;\ge\; \frac{K - N}{N(K - 1)}.$$

Equality holds if and only if (a) $\sum_i x_i x_i^H = (K/N) I_N$, so that the vectors form a tight frame, and (b) $|\langle x_i, x_j \rangle|$ is the same for all $i \ne j$.

**Sequence form.** Let $s_1, \ldots, s_M$ be complex sequences of period $N$ with energy $\sum_n |s_m[n]|^2 = N$, and let $\theta_{\max}$ be the largest $|\theta_{a,b}(\tau)| = |\sum_n s_a[n] \overline{s_b[(n + \tau) \bmod N]}|$ over all pairs $a, b$ and shifts $\tau$, except $a = b$ with $\tau = 0$. Then

$$\theta_{\max} \;\ge\; N \sqrt{\frac{M - 1}{MN - 1}}.$$

## In plain words

Two arrows that point in different directions overlap little. In a flat plane you can draw only two arrows that do not overlap at all. If you want more arrows, some of them must lean toward each other.

The bound says how much they must lean. With many arrows and few directions, at least one pair must overlap by a certain amount, however cleverly the arrows are placed.

For spreading codes, every code and every shifted copy of it is one arrow, and the overlap is the correlation between them. So a code family with many codes, or with long codes and many shifts, cannot have all its correlations near zero. The bound gives the floor, and a good code family comes close to it.

## Proof

Let $X$ be the $N \times K$ matrix with columns $x_1, \ldots, x_K$, and let $G = X^H X$ be the $K \times K$ Gram matrix, with entries $G_{ij} = \langle x_j, x_i \rangle$. Its diagonal entries are $1$, so $\operatorname{tr} G = K$. Its rank is at most $N$, and it is Hermitian and positive semidefinite, so it has at most $N$ nonzero eigenvalues $\lambda_1, \ldots, \lambda_r \ge 0$, with $r \le N$ and $\sum_k \lambda_k = K$.

The squared Frobenius norm is the sum of the squared eigenvalues. By the Cauchy-Schwarz inequality,

$$\|G\|_F^2 = \sum_{k=1}^{r} \lambda_k^2 \;\ge\; \frac{1}{r}\Big(\sum_{k=1}^{r} \lambda_k\Big)^2 = \frac{K^2}{r} \;\ge\; \frac{K^2}{N}.$$

On the other side, $\|G\|_F^2 = \sum_{i,j} |G_{ij}|^2 = K + \sum_{i \ne j} |\langle x_i, x_j\rangle|^2 \le K + K(K-1)\, c_{\max}^2$. Together,

$$K + K(K-1)\,c_{\max}^2 \;\ge\; \frac{K^2}{N}, \qquad\text{so}\qquad c_{\max}^2 \;\ge\; \frac{K^2/N - K}{K(K-1)} = \frac{K - N}{N(K-1)}.$$

**Equality.** The first inequality is an equality if and only if $r = N$ and all $N$ nonzero eigenvalues equal $K/N$. Since $G$ and $X X^H$ have the same nonzero eigenvalues, this means $X X^H = \sum_i x_i x_i^H = (K/N) I_N$. The second inequality is an equality if and only if every off-diagonal $|G_{ij}|$ equals $c_{\max}$. These are conditions (a) and (b).

**Sequence form.** For each sequence $s_m$ and shift $\tau$, let $x_{m,\tau} = N^{-1/2} (s_m[(n + \tau) \bmod N])_{n=0}^{N-1}$. These are $K = MN$ unit vectors in $\mathbb{C}^N$, and $\langle x_{a,0}, x_{b,\tau} \rangle = \theta_{a,b}(\tau) / N$. The inner product of two shifted vectors $x_{a,\sigma}$ and $x_{b,\tau}$ is $\theta_{a,b}(\tau - \sigma)/N$, and the pair of indices $(a, \sigma) \ne (b, \tau)$ is distinct exactly when $a \ne b$ or $\tau - \sigma \not\equiv 0$. So the largest inner product over distinct indices is $\theta_{\max}/N$, and the theorem gives

$$\frac{\theta_{\max}^2}{N^2} \;\ge\; \frac{MN - N}{N(MN - 1)} = \frac{M-1}{MN-1},$$

which is the sequence form. $\blacksquare$

## Consequences

- **Size of the floor.** For $M$ large compared with $1$, $N\sqrt{(M-1)/(MN-1)} \approx \sqrt N$. No family of many sequences of period $N$ has all its periodic correlations below about $\sqrt N$, a $1/\sqrt N$ fraction of the peak $N$.
- **Binary sequences.** For binary sequences of odd period $N$, every correlation is an odd integer. So $\theta_{\max}$ is at least the least odd integer at or above the bound. For $M = 2^{n/2}$ sequences of period $2^n - 1$ this integer is $1 + 2^{n/2}$, and the small [Kasami](/kasami-sequences/) set reaches it.
- **Code families against the bound.** For [Gold sequences](/gold-sequences/) of period $31$, the family has $33$ sequences, $\theta_{\max} = 9$, and the bound is $5.485$, a ratio of $1.64$. For the GPS family of period $1023$ with $1025$ sequences, $\theta_{\max} = 65$ against a bound of $31.97$, a ratio of $2.03$. For the small Kasami sets of period $15$, $63$ and $255$ the ratio is $1.48$, $1.21$ and $1.10$.
- **One sequence.** For $M = 1$ the bound is $0$. It is met by any sequence whose cyclic shifts are orthogonal, such as a [Zadoff-Chu sequence](/zadoff-chu-sequence/). An [m-sequence](/maximal-length-sequence/) has off-peak autocorrelation $-1$ and misses it by $1$.
- **Complex families.** For a prime $N$, the $N - 1$ Zadoff-Chu sequences have $\theta_{\max} = \sqrt N$. The bound is $2.4445$ for $N = 7$ against $\sqrt 7 = 2.6458$, and $28.9482$ for $N = 839$ against $28.9655$.
- **Total squared correlation.** The proof also shows $\sum_{i,j} |\langle x_i, x_j\rangle|^2 \ge K^2/N$, with equality for every tight frame. In synchronous [CDMA](/code-division-multiple-access/) with $K$ users of equal power and signatures of length $N < K$, the signature sets that meet this with equality are the ones that maximize the sum capacity.

## Tightness

- **Three vectors in $\mathbb{C}^2$.** For $K = 3$ and $N = 2$ the bound is $c_{\max}^2 \ge 1/4$. Three real unit vectors at the angles $0$, $120$ and $240$ degrees have pairwise inner products $-1/2$, so the bound holds with equality.
- **Four vectors in $\mathbb{C}^2$.** For $K = 4$ the bound is $1/3$. The vectors $(1, 0)$ and $(1/\sqrt 3, \sqrt{2/3}\,\omega^k)$ for $k = 0, 1, 2$, with $\omega = e^{j2\pi/3}$, have all six squared inner products equal to $1/3$, and $\sum_i x_i x_i^H = 2 I_2$. They meet the bound. No four real unit vectors in $\mathbb{R}^2$ do.
- **Sets that meet it.** Sets that satisfy (a) and (b) are called equiangular tight frames. They exist only for some pairs $(K, N)$; for complex vectors they need $K \le N^2$, and for real vectors $K \le N(N+1)/2$. For $K > N^2$ the bound is never met.
- **$K \le N$.** The right-hand side is $0$ or negative, and any orthonormal set meets $c_{\max} = 0$.
- **The sequence form is rarely met.** The shifts of $M$ sequences form $MN$ vectors in $\mathbb{C}^N$, which can be equiangular only if $MN \le N^2$. Even then, the shift structure restricts the possible sets, and the families on this page with $M \ge 2$ come close to the bound but do not meet it. For binary sequences the integer argument above gives a stronger floor.

## History

Lloyd Welch published the bound in 1974, in a short paper in the IEEE Transactions on Information Theory, as a lower bound on the largest cross-correlation of a set of signals, and applied it to sets of sequences with all their shifts. The paper also gives a family of stronger bounds for higher powers of the inner products. The bound became the reference for the families of spreading sequences: Sarwate and Pursley's 1980 survey compares the Gold and Kasami families with it. The sets that meet it with equality were later studied as equiangular tight frames, in frame theory, coding and quantum information.

## References
