---
tag: HAH02Z
kind: algorithm
slug: wiedemann-algorithm
name: Wiedemann algorithm
aliases: [Wiedemann's method, Wiedemann's algorithm, scalar Wiedemann algorithm, Wiedemann solver]
area: algebra/exact-linear-algebra
level: research
summary: Solves sparse linear systems over finite fields using the minimal polynomial from a Krylov sequence.
solves: [linear-system-solving, minimal-polynomial-computation]
model: algebraic-computation-tree
complexity:
  vars: {n: the size of the matrix, w: the number of nonzero entries (at least n for a nonsingular matrix), q: the size of the finite field, b: the maximum binary length of an entry of an integer input}
  time: {expected: O(n w)}
  space: {extra: Θ(n)}
  field_operations: {expected: 6 n w + O(n^2)}
  bit_operations: {expected: O(n w log^2 q)}
properties: {deterministic: false, in_place: false, recursive: false}
prereqs: [black-box-matrix, matrix-minimal-polynomial, berlekamp-massey]
see_also: [block-wiedemann-algorithm, block-lanczos-algorithm, structured-gaussian-elimination, minimal-polynomial-computation, krylov-subspace, schwartz-zippel-lemma, sparse-matrix-vector-multiplication, index-calculus]
sources:
  - paper: doi:10.1109/TIT.1986.1057137
    title: Douglas H. Wiedemann, Solving sparse linear equations over finite fields, IEEE Transactions on Information Theory 32(1), 1986
    locator: pp. 54 to 62 (the Krylov sequence, its minimal polynomial by Berlekamp-Massey, the solver, and the determinant)
  - paper: doi:10.1007/3-540-54522-0_93
    title: Erich Kaltofen and B. David Saunders, On Wiedemann's method of solving sparse linear systems, Proceedings of AAECC-9, Lecture Notes in Computer Science 539, Springer, 1991
    locator: pp. 29 to 38 (preconditioners for singular and non-square systems, the rank, and probability bounds through the Schwartz-Zippel lemma)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jurgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Section 12.4, Wiedemann's algorithm and black box linear algebra; Section 12.3, Computing the minimal polynomial of a linearly recurrent sequence (Berlekamp-Massey through the extended Euclidean algorithm)
  - paper: doi:10.1109/TIT.1969.1054260
    title: James L. Massey, Shift-register synthesis and BCH decoding, IEEE Transactions on Information Theory 15(1), 1969
    locator: pp. 122 to 127 (the shortest linear recurrence of a finite sequence, and its uniqueness when the sequence has at least twice its length)
  - paper: doi:10.1090/S0025-5718-1994-1192970-7
    title: Don Coppersmith, Solving homogeneous linear equations over GF(2) via block Wiedemann algorithm, Mathematics of Computation 62(205), 1994
    locator: pp. 333 to 350 (the block version used for integer factorization)
---

The Wiedemann algorithm solves a linear system $A x = b$ over a finite field when $A$ is large and sparse, or more generally when $A$ is a [black box](/black-box-matrix/) that can only be multiplied by vectors. It never changes $A$. It projects the Krylov sequence $b, A b, A^2 b, \ldots$ to the scalars $s_i = u^T A^i b$ with a random vector $u$, finds the minimal polynomial $f$ of this scalar sequence with [Berlekamp-Massey](/berlekamp-massey/), and with high probability $f$ is the minimal polynomial of $b$ with respect to $A$, from which $x$ is a short combination of the Krylov vectors. The cost is about $3n$ products by $A$ and $O(n^2)$ further operations, with $\Theta(n)$ extra memory, so a matrix with $w$ nonzero entries costs $O(n w)$, against $O(n^3)$ for [elimination](/gaussian-elimination/), which also fills in the sparse matrix.

## In plain words

Multiplying a sparse table by a list of numbers is cheap, and it is all this method does with the table. Start from the right-hand side, multiply by the table again and again, and remember only one number per step: the dot product with a random list chosen at the start.

These numbers follow a hidden rule: from some point, each is a fixed combination of the previous ones. A classical method from coding theory, Berlekamp-Massey, finds the shortest such rule from twice as many numbers as the rule is long. That rule, with high probability, is also the rule obeyed by the vectors themselves, and rearranging it gives the solution directly. The random choice can be unlucky, so the answer is checked, and in the rare case of failure the method is run again with a new random list.

## The problem

**Notation.** $K = \mathbb{F}_q$ is a finite field, or any field with a finite sampling set $S \subseteq K$. $A$ is an $n \times n$ matrix over $K$, given as a black box $v \mapsto A v$, and $w$ is the number of its nonzero entries, so one product costs at most $2w$ field operations. For $b \in K^n$, the *Krylov space* is $\mathcal{K} = \operatorname{span}\{b, A b, A^2 b, \ldots\}$, its dimension $d$ is the degree of the minimal polynomial $\mu_{A,b}$ of $b$ (the monic $g$ of least degree with $g(A) b = 0$), and $\mu_{A,b}$ divides the [minimal polynomial](/matrix-minimal-polynomial/) of $A$. Costs are given in *field operations* (the algebraic computation tree model, plus random choices) and in *bit operations*, where an operation in $\mathbb{F}_p$ costs $O(\log^2 p)$. For integer input, $b$ also denotes the maximum binary length of the entries of $A$ and of the right-hand side.

**Input.** A black box for a nonsingular $A$ over $K$, a vector $b \in K^n$, and a source of random elements of $S$.

**Output.** The solution $x$ of $A x = b$, or a proof that $A$ is singular. The algorithm is Las Vegas: the output is always correct, and only the running time is random.

## The algorithm

```pseudo id=main
WIEDEMANN-SOLVE(A, b)              ▷ A is an n × n black box over K, nonsingular
L1  if b = 0 then return 0
L2  repeat
L3      choose u ∈ S^n uniformly at random
L4      s_i ← u^T A^i b for i = 0, …, 2n − 1           ▷ 2n − 1 products, one vector kept
L5      f ← BERLEKAMP-MASSEY(s_0, …, s_{2n−1}), monic, f = Σ_{j ≤ d} f_j x^j; if d = 0 then try again
L6      if f_0 = 0 then return "A is singular"
L7      x ← −(1/f_0) Σ_{j=1}^{d} f_j A^{j−1} b          ▷ by Horner, d − 1 products
L8  until A x = b
L9  return x
```

Line L4 computes the vectors $A^i b$ one after another and keeps only the current one and the scalar $s_i$. Line L5 returns the minimal polynomial of the scalar sequence; it is the monic polynomial of least degree $d$ with $\sum_j f_j s_{i+j} = 0$ for all $i$. Because the sequence satisfies the recurrence given by $\mu_{A,b}$, which has degree at most $n$, the $2n$ terms determine it. If $f = \mu_{A,b}$, then $0 = f(A) b = f_0 b + A \sum_{j \ge 1} f_j A^{j-1} b$, so the vector of line L7 solves the system; line L7 evaluates it as $y \leftarrow b$, then $y \leftarrow A y + f_j b$ for $j = d - 1, \ldots, 1$. If the projection was unlucky, $f$ is a proper divisor of $\mu_{A,b}$, the check on line L8 fails, and a new $u$ is drawn. If $f_0 = 0$, then $x$ divides $\mu_{A,b}$, which divides the minimal polynomial of $A$, so $0$ is an eigenvalue and $A$ is singular.

## Example

Over $\mathbb{F}_7$, let

$$A = \begin{pmatrix} 2 & 1 & 0 \\ 0 & 3 & 1 \\ 1 & 0 & 2 \end{pmatrix}, \qquad b = \begin{pmatrix} 3 \\ 4 \\ 3 \end{pmatrix}, \qquad u = e_1.$$

| $i$ | $A^i b$ | $s_i = u^T A^i b$ |
|---|---|---|
| 0 | $(3, 4, 3)$ | 3 |
| 1 | $(3, 1, 2)$ | 3 |
| 2 | $(0, 5, 0)$ | 0 |
| 3 | $(5, 1, 0)$ | 5 |
| 4 | $(4, 3, 5)$ | 4 |
| 5 | $(4, 0, 0)$ | 4 |

Berlekamp-Massey on $(3, 3, 0, 5, 4, 4)$ returns $f = x^3 + 2x + 1$. Check: $s_3 + 2 s_1 + s_0 = 14$, $s_4 + 2 s_2 + s_1 = 7$ and $s_5 + 2 s_3 + s_2 = 14$, all $0$ modulo $7$. This is the characteristic polynomial $x^3 - 7x^2 + 16x - 13$ of $A$ reduced modulo $7$; it is irreducible over $\mathbb{F}_7$, so every nonzero $u$ works here, $342$ of the $343$ choices. Line L7 gives

$$x = -\tfrac{1}{1} (f_1 b + f_2 A b + A^2 b) = -\big(2 (3, 4, 3) + (0, 5, 0)\big) = -(6, 13, 6) \equiv (1, 1, 1),$$

and indeed $A (1, 1, 1)^T = (3, 4, 3)^T$.

**An unlucky projection.** Over $\mathbb{F}_5$, with $A = \operatorname{diag}(1, 2, 3)$, $b = (1, 1, 1)$ and $u = (1, 1, 0)$, the sequence is $s_i = 1 + 2^i$, whose minimal polynomial is $(x - 1)(x - 2) = x^2 + 2x + 2$, a proper divisor of $\mu_{A,b} = (x - 1)(x - 2)(x - 3)$. Line L7 gives $x = (1, 3, 0)$ and $A x = (1, 1, 0) \ne b$, so the check fails and another $u$ is drawn. Here a projection succeeds exactly when all three coordinates of $u$ are nonzero, for $64$ of the $125$ choices.

## Correctness

Three facts make the algorithm correct; the [full proof](proofs/correctness.md) gives the details. First, every polynomial $g$ with $g(A) b = 0$ annihilates the sequence $s$, so the minimal polynomial $F$ of the infinite sequence divides $\mu_{A,b}$ and has degree at most $d \le n$; and a sequence whose minimal polynomial has degree $e$ is determined, together with that polynomial, by its first $2e$ terms, so line L5 returns $F$. Second, if $F(0) = 0$ then $x \mid \mu_{A,b}$ and $A$ is singular, and if $F = \mu_{A,b}$ then line L7 solves the system; in all other cases the check on line L8 rejects the vector, so a returned $x$ is always a solution. Third, $F = \mu_{A,b}$ exactly when the $d \times d$ Hankel matrix $(s_{i+j})$ is nonsingular; its determinant is a nonzero polynomial of degree $d$ in the entries of $u$, so by the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/)

$$\Pr[\text{a try succeeds}] \ge 1 - \frac{d}{|S|} \ge 1 - \frac{n}{|S|}.$$

Over $\mathbb{F}_q$ with $S = \mathbb{F}_q$, the exact probability is $\prod_g (1 - q^{-\deg g})$ over the distinct irreducible factors $g$ of $\mu_{A,b}$, which is always positive, so the expected number of tries is finite even when $q$ is small. The test file checks both statements: by enumeration of all $u$ for three matrices over $\mathbb{F}_5$ (counts $64$, $124$ and $100$ out of $125$, against the bound $50$), and by sampling $400$ random sparse $8 \times 8$ systems over $\mathbb{F}_{101}$, where the bound allows at most $400 \cdot 8 / 101 \approx 32$ failed first tries on average and $10$ were observed.

## Complexity

**Field operations per try.** Line L4 does $2n - 1$ products by $A$ and $2n$ inner products of length $n$. Berlekamp-Massey on $2n$ terms costs $O(n^2)$ operations, about $2n^2$ multiplications in the worst case. Line L7 does $d - 1 \le n - 1$ products and $O(n d)$ vector operations, and line L8 one product. With products of at most $2w$ operations, a try costs at most $(3n - 1) \cdot 2w + O(n^2) = 6 n w + O(n^2)$ field operations, which is $O(n w)$ because $w \ge n$ for a nonsingular matrix.

**Expected cost.** Tries are independent and each succeeds with probability at least $1 - n/|S|$, so the expected number of tries is at most $1 / (1 - n/|S|)$, which is at most $2$ when $|S| \ge 2n$. So the expected cost is $O(n w)$ field operations; this is proved. In practice almost every first try succeeds once $|S|$ is much larger than $n$; the count above shows that the bound is far from tight, an observation. When $q < 2n$, either accept more tries, or take $u$ in an extension field $\mathbb{F}_{q^k}$ with $q^k \ge 2n$, which multiplies the cost by a factor polynomial in $k = O(\log n)$.

**Bit operations over $\mathbb{F}_p$.** Each field operation costs $O(\log^2 p)$, so the expected total is $O(n w \log^2 p)$. No number grows: every intermediate value is an element of $\mathbb{F}_p$.

**Over $\mathbb{Z}$ or $\mathbb{Q}$.** Run directly over $\mathbb{Q}$, the scalars $s_i$ for $i < 2n$ have up to $2n (b + \log_2 n) + O(b)$ binary digits, since $|s_i| \le \|u\| \, (n 2^b)^i \, \|b\|$, and Berlekamp-Massey over $\mathbb{Q}$ creates fractions of similar size; this bound is proved, but the method is then slower than elimination. Instead, solve modulo primes of $\ell = \Theta(\log (n b))$ digits and reconstruct. By [Cramer's rule](/cramers-rule/) and the [Hadamard bound](/hadamard-bound/), $x = \operatorname{adj}(A) b / \det A$ has numerators and denominator of at most $n (b + \tfrac12 \log_2 n) + \log_2 n$ digits, so $O(n (b + \log n) / \ell)$ primes suffice for rational reconstruction, and the expected total is $O(n^2 w (b + \log n) \log (n b) + n^3 (b + \log n)^2)$ bit operations, the second term for the Chinese remainder and rational reconstruction steps with schoolbook arithmetic. Bad primes, those dividing $\det A$, are detected by line L6 and skipped.

**Space.** $u$, the current Krylov vector, $y$ and the $2n$ scalars: $\Theta(n)$ field elements beyond the black box. This is the main advantage over elimination on a sparse matrix, which may need $\Theta(n^2)$ memory after fill-in.

## Properties

- **Las Vegas.** The answer is checked, so it is always correct; only the number of tries is random.
- **Black box.** $A$ is used only through products $v \mapsto A v$, so structured matrices (Toeplitz, sparse, products of sparse matrices, matrices given by a formula) are handled with the cost of their products.
- **No fill-in and $\Theta(n)$ memory.** $A$ is never modified.
- **By-products.** The polynomial $f$ is the minimal polynomial of $b$; with a random $b$ as well, it is the minimal polynomial of $A$ with probability at least $1 - 2 \deg \mu_A / |S|$, which gives a Monte Carlo [minimal polynomial computation](/minimal-polynomial-computation/).
- **Sequential.** The products $A^i b$ form a chain of $2n$ dependent steps, so the scalar algorithm parallelizes only inside each product; the block version removes this limit.

## Variants and improvements

- **Wiedemann's continuation.** Instead of discarding an unlucky $f$, Wiedemann's original paper uses it: with $b' = f(A) b$, the remaining factor of $\mu_{A,b}$ is the minimal polynomial of $b'$, found by a second projection, and the two partial results combine. This reduces the expected work when $q$ is small.
- **Determinant.** With a random diagonal preconditioner $D$, the minimal polynomial of $A D$ equals its characteristic polynomial with high probability, so $\det A = \pm f(0) / \det D$ from one minimal polynomial computation (Wiedemann, 1986; the diagonal preconditioner is analyzed by Chen, Eberly, Kaltofen, Saunders, Turner and Villard, 2002).
- **Singular and non-square systems, rank.** Kaltofen and Saunders (1991) precondition $A$ by random Toeplitz and triangular Toeplitz matrices so that its leading $r \times r$ minor is nonzero for $r = \operatorname{rank} A$; this gives the rank, random solutions of consistent singular systems and nullspace vectors in the same cost. See [rank computation](/rank-computation/) and [nullspace computation](/nullspace-computation/).
- **Block Wiedemann.** Coppersmith (1994) projects with blocks of $m$ vectors on both sides and replaces Berlekamp-Massey by a matrix version; the $m$ chains of products run in parallel and over $\mathbb{F}_2$ each product handles $m$ bits at once with word operations. See the [block Wiedemann algorithm](/block-wiedemann-algorithm/).
- **Lanczos methods.** The [block Lanczos algorithm](/block-lanczos-algorithm/) reaches the same cost with a different Krylov recurrence, and is the main competitor over $\mathbb{F}_2$.
- **Early termination.** If the Berlekamp-Massey output has not changed for several more terms, stop computing the sequence; this saves work when $\deg \mu_{A,b}$ is much less than $n$, at the price of a small chance of a wrong $f$, which line L8 still catches.
- **Fast minimal polynomial.** Computing $f$ with the fast extended Euclidean algorithm costs $O(M(n) \log n)$ instead of $O(n^2)$, which matters when $w$ is close to $n$.

## When to use it

Use it for large sparse systems over a finite field when elimination would fill in or run out of memory: the linear algebra step of the [index calculus](/index-calculus/) method for discrete logarithms and of factoring algorithms (in the block version), sparse systems from combinatorics and coding theory, and structured matrices with fast products. It is often combined with [structured Gaussian elimination](/structured-gaussian-elimination/), which first shrinks the matrix while keeping it sparse. For dense matrices, or for $n$ up to a few thousand, elimination modulo $p$ is faster and simpler; over $\mathbb{F}_2$ at very large sizes, the block versions are used instead of the scalar one.

## Pitfalls

- **Too few terms.** Berlekamp-Massey needs $2n$ terms, or $2 \deg \mu_{A,b}$; with fewer, the shortest recurrence of the prefix need not be the minimal polynomial of the whole sequence.
- **Trusting $f$ without the check.** An unlucky $u$ silently gives a proper divisor of $\mu_{A,b}$ and a wrong $x$. The check $A x = b$ costs one product and must stay.
- **Small fields.** Over $\mathbb{F}_2$, a single try succeeds with probability exactly $\prod_g (1 - 2^{-\deg g})$, for example at most $\tfrac12$ whenever $x + 1$ divides $\mu_{A,b}$, and the Schwartz-Zippel bound $1 - n/2$ says nothing. Use many tries, an extension field, or the block version.
- **Singular matrices.** The scalar method is a solver for nonsingular $A$. If $b$ is outside the range of $A$, then $\mu_{A,b}(0) = 0$ and a lucky try reports singularity; but for a consistent singular system it may also stop with $f_0 = 0$ although solutions exist. Use the preconditioned variants of Kaltofen and Saunders for singular systems.
- **Storing the Krylov vectors.** Keeping all $A^i b$ costs $\Theta(n^2)$ memory and throws away the main advantage; recompute them on line L7 instead.

## Implementations

## History

Douglas Wiedemann published the method in 1986, motivated by the sparse systems of discrete logarithm and factoring algorithms. It joined Lanczos and conjugate gradient methods adapted to finite fields by LaMacchia and Odlyzko and others, and it used Berlekamp's and Massey's algorithm for linear recurrences from the decoding of BCH codes (Berlekamp, 1968; Massey, 1969). Kaltofen and Saunders (1991) added the preconditioners for singular systems and the rank, which made Wiedemann's method the foundation of black box linear algebra, as in the LinBox library. Coppersmith (1994) introduced the block version, which together with block Lanczos became the standard linear algebra step of the number field sieve.

## References
