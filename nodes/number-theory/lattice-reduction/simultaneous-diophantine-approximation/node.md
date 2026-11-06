---
tag: CNMNW8
kind: problem
slug: simultaneous-diophantine-approximation
name: Simultaneous Diophantine approximation
aliases:
- simultaneous rational approximation
- SDA
- good simultaneous approximation
area: number-theory/lattice-reduction
level: advanced
summary: Find a common small-denominator rational approximation to several reals at once.
prereqs: [continued-fraction, lattice-basis, lll-approximation-guarantee]
see_also: [integer-relation-problem, continued-fraction-convergents, lll-algorithm, shortest-vector-problem, closest-vector-problem, minkowski-theorem, frank-tardos-algorithm, merkle-hellman-knapsack]
sources:
  - paper: "A. K. Lenstra, H. W. Lenstra Jr. and L. Lovász, Factoring polynomials with rational coefficients, Mathematische Annalen 261 (1982)"
    locator: pages 515 to 534 (Section 1, the corollary that finds a common denominator at most 2^(n(n+1)/4) epsilon^(-n) with all errors at most epsilon)
  - paper: "J. C. Lagarias, The computational complexity of simultaneous Diophantine approximation problems, SIAM Journal on Computing 14(1) (1985)"
    locator: pages 196 to 209 (NP-completeness of the good simultaneous approximation problem in the sup norm, and the analysis of LLL for it)
  - paper: "A. Frank and É. Tardos, An application of simultaneous Diophantine approximation in combinatorial optimization, Combinatorica 7(1) (1987)"
    locator: pages 49 to 65 (rounding the weights of a linear objective to small integers, which makes algorithms strongly polynomial)
  - book: isbn:9780471982326
    title: Alexander Schrijver, Theory of Linear and Integer Programming, Wiley, 1986
    locator: Chapter 6, Diophantine approximation and basis reduction (Dirichlet's theorem, continued fractions, and simultaneous approximation by basis reduction)
---

Simultaneous Diophantine approximation asks, for real numbers $\alpha_1, \ldots, \alpha_n$, for one integer $q \ge 1$ such that every $q \alpha_i$ is close to an integer $p_i$: then the fractions $p_1 / q, \ldots, p_n / q$ share the denominator $q$ and approximate all the $\alpha_i$ at once. Dirichlet's theorem guarantees $q \le \varepsilon^{-n}$ with all errors $|q \alpha_i - p_i|$ below $\varepsilon$. For $n = 1$ [continued fractions](/continued-fraction-convergents/) find the best $q$ quickly, but for general $n$ the problem is NP-hard (Lagarias, 1985), and the [LLL algorithm](/lll-algorithm/) finds a $q$ that is larger than Dirichlet's bound by a factor $2^{n(n+1)/4}$ in polynomial time.

## In plain words

Several numbers are given, say the lengths of a few gears. We look for one whole number that, multiplied by each of them, lands almost exactly on a whole number every time. Then all the numbers are, up to small errors, fractions with that same bottom part.

With one number this is the classic job of continued fractions, and it is easy. With several numbers at once it is hard: each number pulls the choice in a different direction, and checking all candidates up to a limit takes as long as the limit is large. A pigeonhole argument shows that a fairly good candidate always exists. Lattice reduction finds a candidate that is not the best, but is good enough for many uses in optimization and in breaking codes.

## Definition

**Notation.** As on all pages of this area: lattice bases are written as rows $b_1, \ldots, b_k$, with Gram-Schmidt vectors $b_i^*$, first minimum $\lambda_1$, determinant $\det(L)$ and LLL parameter $\delta$. On this page $n$ is the number of reals, so the lattice used below has rank $k = n + 1$. For a real $x$, $\|x\|_{\mathbb{Z}} = \min_{p \in \mathbb{Z}} |x - p|$ is the distance to the nearest integer. The inputs are rationals, written in binary.

**Good simultaneous approximation (decision).** *Input:* rationals $\alpha_1, \ldots, \alpha_n$, an integer $N \ge 1$ and a rational $\varepsilon > 0$. *Question:* is there an integer $q$ with $1 \le q \le N$ and

$$\max_{1 \le i \le n} \|q \alpha_i\|_{\mathbb{Z}} \le \varepsilon \, ?$$

**Search version.** Output such a $q$ and the integers $p_i$ nearest to $q \alpha_i$, or report that none exists.

**Optimization version.** Given $\alpha$ and $N$, find $q \in \{1, \ldots, N\}$ that minimizes $\max_i \|q \alpha_i\|_{\mathbb{Z}}$.

Since $N$ is given in binary, trying every $q \le N$ takes time exponential in the input size.

## Variants

- **Euclidean version.** Measure the errors by $\big( \sum_i (q \alpha_i - p_i)^2 \big)^{1/2}$ instead of their maximum. This is the version that lattice reduction handles directly, and it differs from the sup norm by at most a factor $\sqrt n$.
- **Best approximations.** A denominator $q$ is a *best simultaneous approximation* if $\max_i \|q \alpha_i\|_{\mathbb{Z}} < \max_i \|q' \alpha_i\|_{\mathbb{Z}}$ for every $q' < q$. For $n = 1$ these are exactly the denominators of the continued fraction convergents of $\alpha_1$ (Lagrange).
- **Inhomogeneous version (Kronecker).** Given also targets $\beta_i$, make every $q \alpha_i - \beta_i$ close to an integer. This is a [closest vector problem](/closest-vector-problem/) in the same lattice.
- **Small linear forms.** The dual question: find integers $q_1, \ldots, q_n$, not all zero and bounded in size, such that $q_1 \alpha_1 + \cdots + q_n \alpha_n$ is close to an integer. When the linear form is exactly 0 this is the [integer relation problem](/integer-relation-problem/). Khintchine's transference principle relates how well the two questions can be solved for the same $\alpha$.

## Examples

- **Rational inputs.** If all $\alpha_i$ have the common denominator $D$, then $q = D$ gives errors 0. Example: $\alpha = (1/3, 2/3)$ with $q = 3$, $p = (1, 2)$.
- **One number.** For $\alpha_1 = \sqrt 2$ the convergents are $1/1, 3/2, 7/5, 17/12, 41/29, \ldots$, and $\|29 \sqrt 2\|_{\mathbb{Z}} \approx 0.0122$, against Dirichlet's guarantee $1/29$.
- **Two numbers.** For $\alpha = (\sqrt 2, \sqrt 3)$, the best simultaneous approximations up to $q = 200000$ begin with $q = 1, 3, 7, 22, 34, 41, 1183, 1463, 2646, 4109, \ldots$ (computed by checking every $q$). The denominator $q = 41$ gives $41 \sqrt 2 \approx 57.983$ and $41 \sqrt 3 \approx 71.014$, so $58/41$ and $71/41$ approximate both numbers with errors at most $0.0173 / 41$. The least $q$ with both errors $\|q \alpha_i\|_{\mathbb{Z}}$ at most $1/100$ is $q = 1463$, with $p = (2069, 2534)$.
- **What LLL finds.** With $\varepsilon = 1/100$ and the lattice of the next section, LLL with $\delta = 3/4$ returns $q = 4109$, $p = (5811, 7117)$, with both errors about $0.0035$. That is within the proved bound $q \le 30000$ for this construction, but almost three times the least admissible $q$. With $\varepsilon = 1/10$ it returns $q = 41$, which is the least admissible one.

## Known algorithms

All bounds below are proved unless marked otherwise; time is polynomial or not in the input size, the total number of binary digits of $\alpha$, $N$ and $\varepsilon$.

- **Brute force.** Check $q = 1, \ldots, N$: $O(N n)$ arithmetic operations, exponential in the size of $N$.
- **$n = 1$: continued fractions.** The convergents of $\alpha_1$, computed by the [Euclidean algorithm](/euclidean-algorithm/), list all best approximations, so the optimization version is solved exactly in polynomial time.
- **Fixed $n$: integer programming.** The conditions $1 \le q \le N$ and $|q \alpha_i - p_i| \le \varepsilon$ are linear in the $n + 1$ unknowns $q, p_1, \ldots, p_n$. So the decision version is an integer program in fixed dimension, solved in polynomial time by [Lenstra's algorithm](/lenstra-algorithm/) for each fixed $n$; the running time grows faster than exponentially in $n$.
- **LLL (proved approximation).** Let $c > 0$ be a rational with $c \le 2^{-n(n+1)/4} \varepsilon^{n+1}$, and take the rank $n + 1$ lattice with rows
  $$b_i = e_i \ (1 \le i \le n), \qquad b_{n+1} = (\alpha_1, \ldots, \alpha_n, c).$$
  Its vectors are $q b_{n+1} - \sum_i p_i b_i = (q \alpha_1 - p_1, \ldots, q \alpha_n - p_n, q c)$, and $\det(L) = c$. The first vector of an LLL-reduced basis with $\delta = 3/4$ has length at most $2^{n/4} \det(L)^{1/(n+1)} \le \varepsilon$ by the [LLL guarantee](/lll-approximation-guarantee/). Its $q$ is not 0, because a vector with $q = 0$ is a nonzero integer vector, of length at least $1 > \varepsilon$ (take $\varepsilon < 1$). After a sign change $q \ge 1$, every $|q \alpha_i - p_i| \le \varepsilon$, and $q c \le \varepsilon$ gives $q \le 2^{n(n+1)/4} \varepsilon^{-n}$. This runs in polynomial time. The example above used $c = \varepsilon^3 / 3$ for $n = 2$, giving the bound $3 / \varepsilon^2 = 30000$.
- **Stronger reduction.** [BKZ](/bkz-algorithm/) or an exact [SVP](/shortest-vector-problem/) solver on the same lattice improves the factor $2^{n(n+1)/4}$, at a cost exponential in the block size or in $n$. Exact SVP solves the weighted Euclidean version exactly, not the sup norm version with a hard bound $N$.

## Bounds

- **Dirichlet's theorem (existence).** For every real $\alpha \in \mathbb{R}^n$ and integer $Q \ge 1$ there is $q$ with $1 \le q \le Q^n$ and $\max_i \|q \alpha_i\|_{\mathbb{Z}} < 1/Q$. *Proof.* The $Q^n + 1$ points of fractional parts $(\{q \alpha_1\}, \ldots, \{q \alpha_n\})$ for $q = 0, 1, \ldots, Q^n$ lie in $[0, 1)^n$, which splits into $Q^n$ half-open cubes of side $1/Q$. Two of them, for $q_1 < q_2$, fall in the same cube, and $q = q_2 - q_1$ works. $\square$ [Minkowski's theorem](/minkowski-theorem/) gives the same result for every real $N \ge 1$: some $q \le N$ has all errors at most $N^{-1/n}$.
- **The exponent $1/n$ is best possible.** There are badly approximable vectors, for which $\max_i \|q \alpha_i\|_{\mathbb{Z}} \ge C q^{-1/n}$ for all $q \ge 1$ with a constant $C > 0$; for example $(\alpha_1, \ldots, \alpha_n)$ when $1, \alpha_1, \ldots, \alpha_n$ is a basis of a real number field of degree $n + 1$ (Perron).
- **NP-completeness.** Lagarias (1985) proved that the good simultaneous approximation problem in the sup norm, with $n$ part of the input, is NP-complete. So there is no polynomial-time algorithm unless P = NP, while the problem is polynomial for each fixed $n$.
- **Hardness of approximation.** Rössner and Seifert (1996) extended the hardness to approximate versions that relax $N$ or $\varepsilon$ by factors that grow almost polynomially in $n$.
- **What is achievable.** LLL relaxes the denominator bound by $2^{n(n+1)/4}$ at a fixed error, which is exponential in $n$ but enough for most applications, where $n$ is small or the instance has a planted solution much better than Dirichlet's bound.

## Reductions

- **To SVP.** The lattice above turns the Euclidean version into a shortest vector problem in rank $n + 1$; any $\gamma$-approximate SVP algorithm then gives errors and denominator within factors governed by $\gamma$. Lagarias analyzed this reduction for the LLL factor.
- **To CVP.** The inhomogeneous version, with the target $(\beta_1, \ldots, \beta_n, 0)$ in the same lattice, is a [closest vector problem](/closest-vector-problem/).
- **From NP-complete problems.** Lagarias's NP-hardness proof is a polynomial-time reduction from an NP-complete integer problem to the decision version with $n$ growing.
- **Planted solutions.** When some $q$ is much better than Dirichlet's bound predicts, the corresponding lattice vector is much shorter than the others, which is an instance of [unique SVP](/unique-svp/); this is why lattice reduction finds such hidden denominators reliably.

## Applications

- **Strongly polynomial algorithms.** Frank and Tardos (1987) replace the weights of a linear objective by small integers, found by simultaneous approximation with LLL, that order all relevant $0/1$ vectors in the same way. This makes many combinatorial optimization algorithms strongly polynomial; see the [Frank-Tardos algorithm](/frank-tardos-algorithm/).
- **Rounding in the ellipsoid method.** Grötschel, Lovász and Schrijver use simultaneous approximation to round the points produced by the [ellipsoid method](/ellipsoid-method/) to rational vectors with a small common denominator.
- **Knapsack cryptanalysis.** In the [Merkle-Hellman knapsack](/merkle-hellman-knapsack/) system, the secret multiplier makes the public weights divided by the modulus unusually well approximable with a common denominator. Lagarias (1983) explained Shamir's attack on the system in these terms.
- **Approximate common divisors.** Given $x_i = p r_i + s_i$ with small noise $s_i$, the ratios $x_i / x_0$ are close to $r_i / r_0$, so $r_0$ is an unusually good common denominator; lattice reduction on the lattice above recovers it and then $p$. This attack sets parameter limits for schemes built on the approximate common divisor problem.
- **Recovering rational vectors.** A vector known only numerically, whose entries are fractions with a small common denominator, is recovered from enough correct digits by the same method.

## References
