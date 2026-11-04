---
tag: XZ91VA
kind: theorem
slug: fft-lower-bound
name: FFT linear circuit lower bound
aliases:
- Morgenstern DFT bound
- linear circuit lower bound for the DFT
area: foundations/lower-bounds
level: research
summary: A linear algorithm with constants of modulus at most 1 needs at least log2 |det A| additions to compute Ax, so the DFT of order n needs at least (n/2) log2 n additions.
prereqs: [discrete-fourier-transform, fast-fourier-transform, determinant]
see_also: [straight-line-program, roots-of-unity, matrix-vector-multiplication, horners-rule-optimality, lower-bound, optimality]
sources:
  - paper: doi:10.1145/321752.321761
    title: "J. Morgenstern, Note on a lower bound on the linear complexity of the fast Fourier transform, Journal of the ACM 20(2) (1973), 305-306"
    locator: the main theorem
  - book: isbn:9783540605829
    title: Peter Buergisser, Michael Clausen and M. Amin Shokrollahi, Algebraic Complexity Theory, Springer (1997)
    locator: Chapter 13, Linear Complexity
  - paper: doi:10.1090/S0025-5718-1965-0178586-1
    title: "J. W. Cooley and J. W. Tukey, An algorithm for the machine calculation of complex Fourier series, Mathematics of Computation 19(90) (1965), 297-301"
    locator: the whole paper (the radix-2 algorithm)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 30, Polynomials and the FFT (the DFT matrix, butterfly operations, the iterative FFT)
---

The FFT linear circuit lower bound, due to Morgenstern (1973), says that a *linear algorithm* whose constants have modulus at most $1$ needs at least $\log_2 |\det A|$ additions to compute $y = Ax$ for a square matrix $A$. For the [discrete Fourier transform](/discrete-fourier-transform/) of order $n$, $|\det F_n| = n^{n/2}$, so every such algorithm needs at least $\tfrac{n}{2}\log_2 n$ additions. The radix-2 [fast Fourier transform](/fast-fourier-transform/) uses $n \log_2 n$ additions of this kind, so it is optimal up to a factor of $2$ within the model. The bound depends on the limit on the constants, and no such bound is known without it.

## Statement

**Model.** Fix a real number $c > 0$. A *linear algorithm with constants bounded by $c$* has inputs $x_1, \ldots, x_n$ (complex numbers) and a sequence of steps

$$
z_k = \lambda_k u_k + \mu_k v_k \qquad (k = 1, \ldots, T),
$$

where $u_k, v_k$ are inputs or earlier values $z_j$ with $j < k$, and $\lambda_k, \mu_k \in \mathbb{C}$ satisfy $|\lambda_k| \le c$ and $|\mu_k| \le c$. Each value is a linear form in the inputs, and we identify it with its row vector of coefficients in $\mathbb{C}^n$; the input $x_i$ is the unit vector $e_i$. The algorithm *computes* $y = Ax$, for $A \in \mathbb{C}^{n \times n}$, if every row of $A$ is the vector of some input or some $z_k$. The cost is the number $T$ of steps. A step with $\lambda_k \ne 0$ and $\mu_k \ne 0$ is an *addition*; a step with one of them zero is a *scaling*.

**Theorem (Morgenstern).** Let $A \in \mathbb{C}^{n \times n}$.

1. If $c \ge \tfrac12$, every linear algorithm with constants bounded by $c$ that computes $Ax$ has $T \ge \log_{2c} |\det A|$ when $c > \tfrac12$, and it needs $|\det A| \le 1$ when $c = \tfrac12$.
2. If $c = 1$, the number of additions is at least $\log_2 |\det A|$, whatever the number of scalings.

**Corollary (DFT).** Let $\omega = e^{-2\pi i/n}$ and $F_n = (\omega^{jk})_{j,k=0}^{n-1}$. Then $|\det F_n| = n^{n/2}$, so a linear algorithm with constants of modulus at most $1$ that computes $F_n x$ makes at least

$$
\frac{n}{2} \log_2 n
$$

additions. If the real and imaginary parts are treated as $2n$ real inputs and the steps are real with constants in $[-1, 1]$, at least $n \log_2 n$ real additions are needed.

## In plain words

Think of each intermediate result of the algorithm as a row of numbers: how much of each input it contains. Collect all rows computed so far and look at the largest "volume" that any choice of input-many rows can span. At the start, with only the inputs, this volume is one.

One step adds two earlier rows, each scaled by a number of size at most one. The volume can then at most double, because the new row is a mix of two old rows. Scaling a row by a small number never makes the volume larger.

At the end the outputs are among the rows, so the volume is at least the volume of the output matrix. If this volume is huge, many doublings were needed. The Fourier matrix has a very large volume, which forces about half of the input size times its logarithm many additions.

## Proof

**Potential.** For $k = 0, \ldots, T$ let $R_k = \{e_1, \ldots, e_n, z_1, \ldots, z_k\}$ be the set of vectors known after $k$ steps. Let $D_k$ be the largest value of $|\det M|$ over all $n \times n$ matrices $M$ whose $n$ rows all belong to $R_k$ (a row may be used more than once).

*Start.* The rows of $M$ are unit vectors. If two rows are equal, $\det M = 0$; otherwise $M$ is a permutation matrix and $|\det M| = 1$. So $D_0 = 1$.

*One step.* Let $M$ have rows in $R_k$. If no row is $z_k$, then $|\det M| \le D_{k-1}$. If $z_k$ appears twice, $\det M = 0$. If it appears once, in row $r$, the determinant is linear in row $r$, so

$$
\det M = \lambda_k \det M_u + \mu_k \det M_v ,
$$

where $M_u$ and $M_v$ are $M$ with row $r$ replaced by $u_k$ and $v_k$. Their rows lie in $R_{k-1}$, so

$$
|\det M| \le (|\lambda_k| + |\mu_k|)\, D_{k-1}.
$$

Hence $D_k \le \max(1, |\lambda_k| + |\mu_k|)\, D_{k-1}$.

*End.* Every row of $A$ is in $R_T$, so $A$ itself is one of the matrices in the definition of $D_T$, and $|\det A| \le D_T$.

*Part 1.* For each step, $\max(1, |\lambda_k| + |\mu_k|) \le \max(1, 2c) = 2c$ when $c \ge \tfrac12$. So $|\det A| \le D_T \le (2c)^T$. If $c > \tfrac12$, take logarithms to base $2c > 1$. If $c = \tfrac12$, the bound says $|\det A| \le 1$.

*Part 2.* Let $c = 1$. A scaling has $|\lambda_k| + |\mu_k| \le 1$, so it does not increase $D$. An addition has $|\lambda_k| + |\mu_k| \le 2$. So $|\det A| \le D_T \le 2^{a}$, where $a$ is the number of additions, and $a \ge \log_2 |\det A|$. $\blacksquare$

*Proof of the corollary.* The $(j, l)$ entry of $F_n F_n^{*}$ is $\sum_{k=0}^{n-1} \omega^{(j-l)k}$. It is $n$ if $j = l$, and $0$ otherwise, since it is a geometric sum of the $n$-th root of unity $\omega^{j-l} \ne 1$ over a full period. So $F_n F_n^* = nI$ and $|\det F_n|^2 = \det(F_n F_n^*) = n^n$, which gives $|\det F_n| = n^{n/2}$ and $\log_2 |\det F_n| = \tfrac{n}{2}\log_2 n$.

For the real version, write $F_n = P + iQ$ with real $P, Q$. On the vector of real and imaginary parts, the transform acts by the real $2n \times 2n$ matrix $G = \begin{pmatrix} P & -Q \\ Q & P \end{pmatrix}$. With the complex matrix $U = \frac{1}{\sqrt 2}\begin{pmatrix} I & iI \\ iI & I \end{pmatrix}$ one checks $U G U^{-1} = \begin{pmatrix} P - iQ & 0 \\ 0 & P + iQ \end{pmatrix}$, so $\det G = \overline{\det F_n} \cdot \det F_n = n^n$. Part 2 with $2n$ inputs gives at least $\log_2 n^n = n \log_2 n$ real additions. $\square$

## Consequences

- **The FFT is optimal up to a factor of 2 in this model.** The radix-2 FFT for $n = 2^k$ performs $\tfrac{n}{2}\log_2 n$ butterflies $(u, v) \mapsto (u + \omega^j v,\ u - \omega^j v)$. Each output of a butterfly is one step $1 \cdot u \pm \omega^j \cdot v$ with constants of modulus $1$, so the FFT is a linear algorithm with $c = 1$ and $n \log_2 n$ additions. The bound is $\tfrac{n}{2}\log_2 n$.
- **Real arithmetic.** In real arithmetic a butterfly with a general twiddle factor takes $6$ real steps with constants in $[-1, 1]$: $2$ for the product $\omega^j v$ (real part $a\cos\theta - b\sin\theta$, imaginary part $a\sin\theta + b\cos\theta$) and $4$ for the two complex sums. So the radix-2 FFT uses at most $3n\log_2 n$ real steps, against the lower bound $n \log_2 n$.
- **Other matrices.** The theorem applies to any square matrix with a large determinant. For example, a Hadamard matrix $H$ of order $n$ (entries $\pm 1$, $HH^{T} = nI$) also has $|\det H| = n^{n/2}$, so the Walsh-Hadamard transform needs $\tfrac{n}{2}\log_2 n$ additions with constants bounded by $1$, and the fast Walsh-Hadamard transform uses $n\log_2 n$.

### Worked example

| $n$ | $\lvert\det F_n\rvert = n^{n/2}$ | bound $\tfrac{n}{2}\log_2 n$ | radix-2 FFT additions $n \log_2 n$ |
|---|---|---|---|
| 2 | 2 | 1 | 2 |
| 4 | 16 | 4 | 8 |
| 8 | 4096 | 12 | 24 |
| 16 | $2^{32}$ | 32 | 64 |
| 1024 | $2^{5120}$ | 5120 | 10240 |

For $n = 2$, $F_2 = \begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}$ has determinant $-2$. The bound asks for one addition, and indeed $x_0 + x_1$ and $x_0 - x_1$ cannot both be inputs or scalings. The FFT uses two. For the real version with $n = 4$, the $8 \times 8$ real matrix has determinant $4^4 = 256$, so at least $8$ real additions are needed.

### Pitfalls

- **The constants must be bounded.** The proof uses $|\lambda_k| + |\mu_k| \le 2c$. Without a bound, one scaling can multiply the potential by any amount. For $n = 1$ and $A = (2^k)$, a linear algorithm with $c = 1$ needs $k$ additions (by the theorem, and $z = u + u$ repeated $k$ times reaches it), but with unbounded constants a single step $z = 2^k x_1$ suffices. For general linear algorithms with unbounded constants, proving a lower bound of order $n \log n$ for the DFT, or any superlinear bound for an explicit matrix, is a well-known open problem.
- **Normalization matters.** The unitary DFT $\tfrac{1}{\sqrt n}F_n$ has $|\det| = 1$, and the theorem gives no bound for it. The $\tfrac{n}{2}\log_2 n$ bound is for the unnormalized matrix with constants of modulus at most $1$. A different bound $c$ also changes the number: the bound is $\log_{2c}|\det A|$, not $\log_2$.
- **Linear algorithms only.** The model has no multiplication of two values that depend on the input, no division and no branching. An algorithm outside this model is not covered.
- **Count of operations.** The theorem counts additions, each with its two scalings. It does not count the multiplications by constants separately, and it says nothing about the number of multiplications, which can be much smaller than the number of additions.
- **Complex versus real.** One complex step costs several real operations. The complex bound $\tfrac{n}{2}\log_2 n$ and the real bound $n \log_2 n$ are about different models and must not be mixed.

## Tightness

For $n$ a power of $2$, the radix-2 FFT meets the bound up to a factor of exactly $2$: $n\log_2 n$ additions against $\tfrac{n}{2}\log_2 n$. For $n = 2$ the bound is $1$ and the optimum is $2$, since $x_0 + x_1$ and $x_0 - x_1$ each need their own addition step. So the theorem does not determine the exact optimum. The order $n \log n$ is tight for the model.

## History

Cooley and Tukey (1965) published the radix-2 FFT, which computes the DFT with $O(n \log n)$ operations. Morgenstern (1973) proved, in a two-page note in the Journal of the ACM, that linear algorithms with bounded constants need $\Omega(n \log n)$ additions for the DFT, by the determinant argument on this page. Buergisser, Clausen and Shokrollahi treat this and other results on linear complexity in Chapter 13 of their book.

## References
