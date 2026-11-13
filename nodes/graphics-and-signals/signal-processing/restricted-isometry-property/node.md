---
tag: AMBGJ9
kind: definition
slug: restricted-isometry-property
name: Restricted isometry property
area: graphics-and-signals/signal-processing
level: research
summary: A matrix nearly keeps the length of every sparse vector. Small constants make basis pursuit recover sparse vectors exactly.
prereqs: [sparse-signal-recovery, eigenvalue]
see_also: [compressed-sensing, basis-pursuit, orthogonal-matching-pursuit, johnson-lindenstrauss-lemma, random-projection, concentration-of-measure, union-bound, condition-number]
sources:
  - paper: doi:10.1109/TIT.2005.858979
    title: Emmanuel J. Candès and Terence Tao, Decoding by linear programming, IEEE Transactions on Information Theory 51(12), 2005
    locator: pages 4203 to 4215 (the restricted isometry constants and their use for exact recovery by linear programming)
  - paper: doi:10.1016/j.crma.2008.03.014
    title: Emmanuel J. Candès, The restricted isometry property and its implications for compressed sensing, Comptes Rendus Mathématique 346(9-10), 2008
    locator: pages 589 to 592, Theorem 1.2 (exact recovery of every s-sparse vector by l1 minimization when the constant of order 2s is below the square root of 2 minus 1)
  - paper: doi:10.1007/s00365-007-9003-x
    title: Richard Baraniuk, Mark Davenport, Ronald DeVore and Michael Wakin, A simple proof of the restricted isometry property for random matrices, Constructive Approximation 28(3), 2008
    locator: pages 253 to 263 (random matrices with s log(n/s) rows have small constants, by a concentration inequality and a union bound as in the Johnson-Lindenstrauss lemma)
  - paper: doi:10.1109/TIT.2013.2290112
    title: Andreas M. Tillmann and Marc E. Pfetsch, The computational complexity of the restricted isometry property, the nullspace property, and related concepts in compressed sensing, IEEE Transactions on Information Theory 60(2), 2014
    locator: pages 1248 to 1259 (computing the restricted isometry constants and testing the null space property are NP-hard)
  - book: isbn:9780817649470
    title: Simon Foucart and Holger Rauhut, A Mathematical Introduction to Compressive Sensing, Birkhäuser, 2013
    locator: Chapter 5 (coherence), Chapter 6 (restricted isometry property) and Chapter 9 (random matrices)
---

A matrix $A \in \mathbb R^{m \times n}$ has the restricted isometry property of order $s$ when it nearly keeps the length of every vector with at most $s$ nonzero entries, and the restricted isometry constant $\delta_s$ measures how nearly. Candès and Tao (2005) defined these constants to give conditions under which [sparse signal recovery](/sparse-signal-recovery/) by linear programming is exact. Random matrices with about $s \log(n/s)$ rows have small constants with high probability, which is the base of [compressed sensing](/compressed-sensing/), but computing the constants of a given matrix is NP-hard.

## Definition

**Restricted isometry constant.** For an integer $s \ge 1$, $\delta_s = \delta_s(A)$ is the smallest $\delta \ge 0$ such that

$$(1 - \delta)\|x\|_2^2 \;\le\; \|Ax\|_2^2 \;\le\; (1 + \delta)\|x\|_2^2 \qquad \text{for every } x \text{ with } \|x\|_0 \le s.$$

$A$ has the restricted isometry property of order $s$ with constant $\delta$ if $\delta_s \le \delta$. The interesting case is $\delta < 1$, and the theorems below need $\delta$ well below $1$.

**Eigenvalue form.** For a set $S$ of column indices, let $A_S$ be the matrix of those columns and $G_S = A_S^{\mathsf T} A_S$ its Gram matrix. Then

$$\delta_s = \max_{|S| = s} \|G_S - I\|_2 = \max_{|S| = s} \max\big(\lambda_{\max}(G_S) - 1,\ 1 - \lambda_{\min}(G_S)\big).$$

*Proof.* An $s$-sparse $x$ has its support in some $S$ with $|S| = s$, and then $\|Ax\|_2^2 = x_S^{\mathsf T} G_S x_S$. The Rayleigh quotient of the symmetric matrix $G_S$ ranges over $[\lambda_{\min}(G_S), \lambda_{\max}(G_S)]$, so the two inequalities hold on $S$ exactly when $\delta \ge \lambda_{\max} - 1$ and $\delta \ge 1 - \lambda_{\min}$. Take the worst $S$. $\square$

**Basic facts.**

1. $\delta_1 \le \delta_2 \le \cdots$, since a vector with $s$ nonzero entries also has at most $s + 1$.
2. $\delta_1 = 0$ if and only if every column has norm $1$.
3. For $s \le n$, $\delta_s < 1$ if and only if every $s$ columns of $A$ are linearly independent. So $\delta_{2s} < 1$ says that $\operatorname{spark}(A) > 2s$, and each $s$-sparse vector is the only $s$-sparse solution of its measurements.
4. For columns of norm $1$, $\delta_2 = \mu$, the mutual coherence $\mu = \max_{i \ne j} |\langle a_i, a_j \rangle|$. The Gram matrix of two columns is $\begin{pmatrix} 1 & c \\ c & 1 \end{pmatrix}$ with eigenvalues $1 \pm c$.
5. For columns of norm $1$, $\delta_s \le (s - 1)\mu$. Each row of $G_S - I$ has $s - 1$ entries of size at most $\mu$, so by the Gershgorin disc theorem every eigenvalue of $G_S - I$ has size at most $(s - 1)\mu$.
6. On a support of size $s$, the [condition number](/condition-number/) of $A_S$ is at most $\sqrt{(1 + \delta_s)/(1 - \delta_s)}$. Least squares on a correct support is then well conditioned.

**Recovery theorem.** (Candès 2008, Theorem 1.2.) If $\delta_{2s} < \sqrt 2 - 1$, then for every $s$-sparse $x_0$, the vector $x_0$ is the unique solution of [basis pursuit](/basis-pursuit/), minimize $\|x\|_1$ subject to $Ax = Ax_0$. The same paper gives a stable version for noisy measurements and for vectors that are only close to sparse. Later work raised the threshold; Foucart and Rauhut (2013, Chapter 6) survey the constants.

**Random matrices.** (Baraniuk, Davenport, DeVore and Wakin 2008.) Let the entries of $A$ be independent normal with mean $0$ and variance $1/m$, or independent signs $\pm 1/\sqrt m$. For each $\delta \in (0, 1)$ there are constants $c_1, c_2 > 0$ such that if $m \ge c_1 s \log(n/s)$, then $\delta_s \le \delta$ with probability at least $1 - 2e^{-c_2 m}$. The proof shows that $\|Ax\|_2^2$ is close to $\|x\|_2^2$ for one fixed $x$ with probability exponentially close to $1$, which is the concentration step of the [Johnson-Lindenstrauss lemma](/johnson-lindenstrauss-lemma/), and then takes a [union bound](/union-bound/) over a finite net of each $s$-dimensional coordinate subspace and over all $\binom ns$ subspaces.

**Complexity.** The eigenvalue form computes $\delta_s$ by $\binom ns$ symmetric eigenvalue problems of size $s$. Tillmann and Pfetsch (2014) showed that computing $\delta_s$ is NP-hard, so no method is known that is fast for every matrix. In practice the property is proved for random families, not checked for one matrix.

## Examples and non-examples

**The identity.** For $A = I_n$, $\|Ax\|_2 = \|x\|_2$ for every $x$, so $\delta_s = 0$ for all $s$. It is an isometry, but it does not compress: $m = n$.

**The tetrahedron.** Let

$$A = \frac{1}{\sqrt 3}\begin{pmatrix} 1 & 1 & -1 & -1 \\ 1 & -1 & 1 & -1 \\ 1 & -1 & -1 & 1 \end{pmatrix}.$$

The columns have norm $1$ and every two have inner product $-\tfrac13$. So for $|S| = k$, $G_S = \tfrac43 I - \tfrac13 J$, where $J$ is the all-ones matrix, with eigenvalues $\tfrac43 - \tfrac k3$ (on the all-ones vector) and $\tfrac43$ (on the vectors whose entries sum to $0$). This gives

| order $s$ | $\lambda_{\min}(G_S)$ | $\lambda_{\max}(G_S)$ | $\delta_s$ |
|---|---|---|---|
| 1 | $1$ | $1$ | $0$ |
| 2 | $\tfrac23$ | $\tfrac43$ | $\tfrac13$ |
| 3 | $\tfrac13$ | $\tfrac43$ | $\tfrac23$ |
| 4 | $0$ | $\tfrac43$ | $1$ |

Here $\mu = \tfrac13$, and the Gershgorin bound $(s - 1)\mu$ is tight for $s = 2, 3, 4$. Since $\delta_2 = \tfrac13 < \sqrt 2 - 1$, the recovery theorem applies with $s = 1$: basis pursuit recovers every $1$-sparse vector from its three measurements. For $s = 2$, $\delta_4 = 1$, and indeed the four columns sum to zero, so $(1, 1, 0, 0)$ and $(0, 0, -1, -1)$ have the same measurements.

**Coherence against restricted isometry.** Let $A = [\,I_{16} \mid \tfrac14 H\,]$, where $H$ is the $16 \times 16$ Sylvester [Hadamard matrix](/walsh-hadamard-transform/). The columns have norm $1$, and $\mu = \tfrac14$, so $\delta_2 = \tfrac14$ and $\delta_4 \le \tfrac34$. The recovery theorem needs $\delta_{2s} < \sqrt 2 - 1 \approx 0.414$, and these bounds give it only for $s = 1$. The coherence condition $\mu < 1/(2s - 1)$ of [orthogonal matching pursuit](/orthogonal-matching-pursuit/) and basis pursuit holds for $s = 2$. Bounds on $\delta_s$ from the coherence grow linearly in $s$, so they cannot show recovery for $s$ much larger than $\sqrt m$.

**Non-example: sufficient, not necessary.** Let $A = [\,e_1, e_2, e_3, w\,]$ with $w = \tfrac1{11}(6, 6, 7)$, a unit vector. The Gram matrix has the eigenvalues $1, 1, 0, 2$, so $\delta_4 = 1$, and $\delta_2 = \mu = \tfrac7{11}$. No order meets the recovery theorem for $s = 2$, or even for $s = 1$. Still, basis pursuit recovers $x_0 = e_1 + e_2$ from $y = (1, 1, 0)$: every solution of $Ax = y$ is $(1 - \tfrac6{11}t, 1 - \tfrac6{11}t, -\tfrac7{11}t, t)$, whose $\ell_1$ norm is $2 + \tfrac{30}{11}|t|$ for $t < 0$, $2 + \tfrac6{11}t$ for $0 < t \le \tfrac{11}6$, and $\tfrac{30}{11}t - 2 > 2$ for larger $t$. So $t = 0$ is the unique minimizer. The property is a uniform condition on all sparse vectors at once, and a single vector can be recovered without it.

**Non-example: a scaled identity.** For $A = 2 I_n$, $\|Ax\|_2^2 = 4\|x\|_2^2$, so $\delta_1 = 3$. The matrix is perfectly conditioned, but the property also asks for the right scale. Divide the columns by their norms before measuring the constants.

## Related definitions

- **Mutual coherence.** $\mu(A)$, the largest absolute inner product of two distinct normalized columns. It is cheap to compute, and $\delta_2 = \mu$. The Welch bound $\mu \ge \sqrt{(n - m)/(m(n - 1))}$ limits it from below, which is why coherence alone gives recovery only for $s$ of order $\sqrt m$.
- **Spark.** The least number of dependent columns. $\delta_{2s} < 1$ is the same as $\operatorname{spark}(A) > 2s$.
- **Null space property.** $A$ has the null space property of order $s$ if $\|v_S\|_1 < \|v_{S^c}\|_1$ for every nonzero $v$ with $Av = 0$ and every $|S| \le s$. Basis pursuit recovers every $s$-sparse vector exactly if and only if it holds. A small $\delta_{2s}$ implies it, but not the other way round. Testing it is also NP-hard (Tillmann and Pfetsch 2014).
- **[Johnson-Lindenstrauss lemma](/johnson-lindenstrauss-lemma/).** A random linear map nearly keeps the distances among a fixed finite set of points. The restricted isometry property asks the same for the infinite union of all $s$-dimensional coordinate subspaces, and the proof above reduces it to a finite set by a net.
- **Restricted eigenvalue condition.** A weaker, one-sided condition on $\|Ax\|_2$ for vectors near sparse directions, used for error bounds of the [lasso](/lasso-regression/).
- **Condition number.** The property says that every $s$-column submatrix is well conditioned, with the same bound for all of them.

## References
