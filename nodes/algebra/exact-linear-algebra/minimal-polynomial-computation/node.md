---
tag: G1ZZY8
kind: problem
slug: minimal-polynomial-computation
name: Minimal polynomial computation
aliases: [computing the minimal polynomial of a matrix, matrix minimal polynomial computation]
area: algebra/exact-linear-algebra
level: advanced
summary: Compute the monic polynomial of least degree annihilating a matrix.
prereqs: [matrix-minimal-polynomial, gaussian-elimination]
see_also: [wiedemann-algorithm, berlekamp-massey, rational-canonical-form, characteristic-polynomial-computation, black-box-matrix, krylov-subspace, chinese-remainder-theorem, minimal-polynomial-algebraic-element]
sources:
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jurgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 12.3, Linearly recurrent sequences, and Section 12.4, Wiedemann's algorithm and black box linear algebra (the minimal polynomial of a matrix from the sequence u^T A^i v)
  - paper: doi:10.1109/TIT.1986.1057137
    title: Douglas H. Wiedemann, Solving sparse linear equations over finite fields, IEEE Transactions on Information Theory 32(1), 1986
    locator: pp. 54 to 62 (the minimal polynomial of a sparse matrix over a finite field from 2n terms of a projected Krylov sequence, and the probability of success)
  - paper: doi:10.1007/3-540-54522-0_93
    title: Erich Kaltofen and B. David Saunders, On Wiedemann's method of solving sparse linear systems, AAECC-9, Lecture Notes in Computer Science 539, 1991
    locator: pp. 29 to 38 (the probability that random projections preserve the minimal polynomial, through the Schwartz-Zippel lemma)
  - paper: "Mark Giesbrecht, Nearly optimal algorithms for canonical matrix forms, SIAM Journal on Computing 24(5), 1995"
    locator: pp. 948 to 969 (the minimal polynomial with the Frobenius form, in about as many field operations as matrix multiplication up to logarithmic factors, randomized)
  - paper: "Arne Storjohann, Deterministic computation of the Frobenius form, 42nd IEEE Symposium on Foundations of Computer Science (FOCS), 2001"
    locator: pp. 368 to 377 (the Frobenius form, and hence the minimal polynomial, in O(n^ω log n log log n) field operations)
---

Minimal polynomial computation asks, for an $n \times n$ matrix $A$ over a field $K$, for its [minimal polynomial](/matrix-minimal-polynomial/) $\mu_A$, the monic polynomial of least degree with $\mu_A(A) = 0$. For dense matrices it is a by-product of the [rational canonical form](/rational-canonical-form/), computable deterministically in $O(n^\omega \log n \log \log n)$ field operations. For sparse or black box matrices, the [Wiedemann algorithm](/wiedemann-algorithm/) finds it from $2n$ terms of the scalar sequence $u^T A^i v$ with [Berlekamp-Massey](/berlekamp-massey/), using only matrix-vector products; it is Monte Carlo and can return a proper divisor.

## In plain words

Raise a square table of numbers to the powers $0, 1, 2, \ldots$ and look for the first power that can be written as a combination of the earlier ones. The coefficients of that combination give the minimal polynomial, the shortest rule that the table obeys.

Doing this directly with whole tables is slow. A faster way follows one vector instead of the whole table, or even a single number per step: multiply a vector by the table again and again, read one coordinate, and find the shortest rule that this list of numbers obeys. With random choices, that rule is almost always the minimal polynomial.

## Definition

**Notation.** $K$ is a field and $A$ an $n \times n$ matrix over $K$. $\omega$ is the exponent of matrix multiplication. For an integer matrix, $b$ is the maximum binary length of an entry. For a vector $v$, $\mu_{A, v}$ is the monic generator of $\{f : f(A) v = 0\}$.

**Input.** $A$, given explicitly or as a [black box](/black-box-matrix/) $v \mapsto A v$.

**Output.** The monic polynomial $\mu_A \in K[x]$ of least degree with $\mu_A(A) = 0$.

**Characterizations used by the algorithms.**

- $\deg \mu_A$ is the least $d$ with $A^d \in \operatorname{span}(I, A, \ldots, A^{d - 1})$.
- $\mu_A = \operatorname{lcm}(\mu_{A, v_1}, \ldots, \mu_{A, v_n})$ for any basis $v_1, \ldots, v_n$ of $K^n$.
- For vectors $u$, $v$, the scalar sequence $a_i = u^T A^i v$ is linearly recurrent, and its minimal polynomial divides $\mu_{A, v}$, which divides $\mu_A$.

## Variants

- **Monte Carlo black box.** Return a divisor of $\mu_A$ that equals $\mu_A$ with a stated probability. This is what the Wiedemann approach gives; a check $f(A) w = 0$ for random $w$ detects most failures.
- **Minimal polynomial of a vector.** Compute $\mu_{A, v}$, the generator of the Krylov subspace of $v$; see [Krylov subspace](/krylov-subspace/).
- **Over $\mathbb{Z}$ or $\mathbb{Q}$.** $\mu_A \in \mathbb{Z}[x]$ for an integer matrix, and it can be computed modulo several primes and reconstructed with the [Chinese remainder theorem](/chinese-remainder-theorem/).
- **Degree only, or nonderogatory test.** Decide whether $\mu_A = \chi_A$, which holds for most matrices over large fields.
- **Minimal polynomial of a sequence.** Given $a_0, a_1, \ldots, a_{2d - 1}$ of a sequence with a recurrence of order at most $d$, find its minimal recurrence; this is the [Berlekamp-Massey](/berlekamp-massey/) problem.
- **Minimal polynomial of an algebraic element.** For $\alpha$ in a finite extension of $K$, the [minimal polynomial](/minimal-polynomial-algebraic-element/) of $\alpha$ is the minimal polynomial of the matrix of multiplication by $\alpha$.

## Examples

**From powers.** For $A = \begin{pmatrix} 2 & 1 & 0 \\ 0 & 2 & 0 \\ 0 & 0 & 2 \end{pmatrix}$, $A \ne 2 I$, so $\deg \mu_A \ge 2$, and $A^2 = \begin{pmatrix} 4 & 4 & 0 \\ 0 & 4 & 0 \\ 0 & 0 & 4 \end{pmatrix} = 4 A - 4 I$. So $\mu_A = x^2 - 4 x + 4 = (x - 2)^2$, while $\chi_A = (x - 2)^3$.

**From a scalar sequence.** For $A = \operatorname{diag}(1, 3)$ and $u = v = (1, 1)$, $a_i = u^T A^i v = 1 + 3^i$, which gives $2, 4, 10, 28, \ldots$. Berlekamp-Massey on the first $2n = 4$ terms finds $a_{i+2} = 4 a_{i+1} - 3 a_i$ (indeed $10 = 16 - 6$ and $28 = 40 - 12$), so the sequence has minimal polynomial $x^2 - 4 x + 3 = \mu_A$.

**A bad projection.** With $u = (1, 0)$ and the same $v$, $a_i = 1$ for all $i$, whose minimal polynomial is $x - 1$, a proper divisor of $\mu_A$. Wiedemann's method avoids this with random $u$ and $v$ and, if needed, takes the lcm over a few tries.

**Edge cases.** For $n = 0$, $\mu = 1$; for the zero matrix of size $n \ge 1$, $\mu = x$; for a $1 \times 1$ matrix $(a)$, $\mu = x - a$.

## Known algorithms

- **Linear algebra on the powers.** Vectorize $I, A, A^2, \ldots$ and find the first dependence by elimination. Simple but $O(n^4)$ or worse, because each power is a matrix product and the vectors have length $n^2$.
- **Krylov subspaces with lcm.** Compute $\mu_{A, v}$ for the unit vectors $v = e_1, \ldots, e_n$ by elimination on Krylov matrices, sharing the work across vectors, and take the lcm. Careful versions build a Krylov basis of $K^n$ step by step and run in $O(n^3)$ field operations.
- **Through the Frobenius form.** $\mu_A$ is the last invariant factor: deterministic in $O(n^\omega \log n \log \log n)$ field operations (Storjohann, 2001), and randomized (Las Vegas) algorithms of Giesbrecht (1995) use about $n^\omega$ operations up to logarithmic factors.
- **Wiedemann's method** (1986). Choose random $u$, $v$, compute $a_i = u^T A^i v$ for $i < 2n$ with $2n$ black box products, and find the minimal polynomial of the sequence with Berlekamp-Massey in $O(n^2)$ field operations. Repeating with new $u$, $v$ and taking the lcm raises the probability of success. See the [Wiedemann algorithm](/wiedemann-algorithm/).
- **Block Wiedemann.** Use blocks of $s$ vectors and a matrix Berlekamp-Massey algorithm, for parallelism and for small fields; see [block Wiedemann](/block-wiedemann-algorithm/).
- **Multimodular over $\mathbb{Z}$.** Compute $\mu_A \bmod p$ for several primes, discard primes where the degree is smaller, and reconstruct the integer coefficients, which are bounded through the factor bounds of $\chi_A$.

## Bounds

**Algebraic model.** The best deterministic bound is $O(n^\omega \log n \log \log n)$ field operations, through the Frobenius form. The only proved lower bound is the trivial $\Omega(n^2)$.

**Verification.** Checking that a candidate $f$ of degree $d$ satisfies $f(A) = 0$ costs $O(\sqrt{d})$ matrix products by the Paterson-Stockmeyer method, so $O(n^{\omega + 1/2})$ field operations, more than computing $\mu_A$ itself. Checking $f(A) w = 0$ for one random vector $w$ costs only $d$ matrix-vector products; it proves only $\mu_{A, w} \mid f$, and that equality $\mu_{A, w} = \mu_A$ holds with high probability.

**Probability for Wiedemann's method.** If $u$ and $v$ have entries chosen uniformly from a finite set $S \subseteq K$, the sequence $u^T A^i v$ has minimal polynomial $\mu_A$ with probability at least $1 - 2 \deg \mu_A / |S|$. The proof applies the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/) twice: once to a $d \times d$ minor of the Krylov matrix of $v$, and once to the $d \times d$ Hankel matrix of the sequence, both polynomials of degree $d = \deg \mu_A$ in the random entries. Over a small field such as $\mathbb{F}_2$ this bound is useless, and Wiedemann (1986) gives a separate bound for $\mathbb{F}_q$; repeated trials or a field extension are used there.

**Bit sizes over $\mathbb{Z}$.** $\mu_A$ is a monic divisor of $\chi_A$ in $\mathbb{Z}[x]$, whose coefficients have $O(n (b + \log n))$ binary digits by the Hadamard bound on principal minors, and Mignotte's bound transfers this to $\mu_A$ with $O(n)$ more digits. So the reconstruction needs primes whose product has $O(n (b + \log n))$ binary digits, that is $O(n (b + \log n) / w)$ primes of word length $w$.

## Reductions

- **From the Frobenius form.** $\mu_A$ is its last invariant factor.
- **To sequence problems.** With projections, the matrix problem becomes the minimal polynomial of a scalar sequence, solved by Berlekamp-Massey or by a [Pade approximation](/pade-approximation/) of the generating function $\sum_i a_i x^i$.
- **To it: linear systems.** For nonsingular $A$, $\mu_A(0) \ne 0$, and $\mu_A = x^d + \cdots + c_0$ gives $A^{-1} b = -c_0^{-1} (A^{d-1} b + \cdots + c_1 b)$, which is how Wiedemann solves sparse systems.
- **To it: diagonalizability and eigenvalues.** $A$ is diagonalizable over $K$ if and only if $\mu_A$ splits into distinct linear factors, which can be tested with a gcd of $\mu_A$ and its derivative and a root search.

## Applications

- **Sparse linear algebra.** Solving, determinant and rank of large sparse matrices over finite fields, in integer factoring, discrete logarithms and coding theory; see [linear system modulo 2](/linear-system-modulo-2/).
- **Matrix functions and powers.** Computing $f(A)$ or $A^N$ by reduction modulo $\mu_A$, which has lower degree than $\chi_A$.
- **Algebraic numbers and field arithmetic.** The minimal polynomial of an element of a number field or finite field is the minimal polynomial of a multiplication matrix.
- **Testing and verification.** Deciding whether a matrix is nilpotent, idempotent, or of finite order, which are statements about $\mu_A$.

## References
