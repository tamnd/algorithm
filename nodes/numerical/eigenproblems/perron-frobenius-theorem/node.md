---
tag: 2TQ19R
kind: theorem
slug: perron-frobenius-theorem
name: Perron-Frobenius theorem
aliases:
- Perron-Frobenius
- Perron's theorem
- Perron-Frobenius theory of nonnegative matrices
area: numerical/eigenproblems
level: advanced
summary: An irreducible nonnegative matrix has its spectral radius as a simple eigenvalue with a positive eigenvector, its only nonnegative one. If the matrix is primitive, it strictly dominates.
prereqs: [eigenvalue, eigenvector, spectral-radius]
see_also: [power-iteration, pagerank, markov-chain, eigenvector-centrality, strongly-connected-graph, gershgorin-circle-theorem, nonsymmetric-eigenproblem, subspace-iteration]
sources:
  - book: isbn:9780521548236
    title: Roger A. Horn and Charles R. Johnson, Matrix Analysis, second edition, Cambridge University Press, 2013
    locator: Chapter 8, Positive and nonnegative matrices (Sections 8.2 on positive matrices, 8.3 on nonnegative matrices, 8.4 on irreducible matrices, 8.5 on primitive matrices)
  - book: isbn:9780898714548
    title: Carl D. Meyer, Matrix Analysis and Applied Linear Algebra, SIAM, 2000
    locator: Section 8.2 (positive matrices), Section 8.3 (nonnegative matrices, irreducibility and primitivity), Section 8.4 (stochastic matrices and Markov chains)
  - paper: "Oskar Perron, Zur Theorie der Matrices, Mathematische Annalen 64, 1907"
    title: Zur Theorie der Matrices
    locator: Math. Ann. 64 (1907), pp. 248 to 263
  - paper: "Georg Frobenius, Über Matrizen aus nicht negativen Elementen, Sitzungsberichte der Königlich Preussischen Akademie der Wissenschaften, 1912"
    title: Über Matrizen aus nicht negativen Elementen
    locator: Sitzungsber. Preuss. Akad. Wiss. Berlin (1912), pp. 456 to 477
  - paper: "Helmut Wielandt, Unzerlegbare, nicht negative Matrizen, Mathematische Zeitschrift 52, 1950"
    title: Unzerlegbare, nicht negative Matrizen
    locator: Math. Z. 52 (1950), pp. 642 to 648
---

The Perron-Frobenius theorem describes the dominant eigenvalue of a matrix with nonnegative entries. If $A \ge 0$ entrywise and $A$ is irreducible, meaning that its directed graph is [strongly connected](/strongly-connected-graph/), then the [spectral radius](/spectral-radius/) $r = \rho(A)$ is positive, it is a simple eigenvalue, and it has an eigenvector with all entries positive; no other eigenvalue has a nonnegative eigenvector. If moreover some power $A^k$ is entrywise positive (a primitive matrix), then every other eigenvalue has modulus strictly less than $r$. This is the reason [power iteration](/power-iteration/) converges for [PageRank](/pagerank/), for [Markov chains](/markov-chain/) and for [eigenvector centrality](/eigenvector-centrality/): the dominant eigenvector exists, is unique, is positive, and is separated from the rest of the spectrum.

## Statement

**Notation.** For real matrices and vectors, $A \ge 0$ means every entry is $\ge 0$ and $x > 0$ means every entry is $> 0$. $|x|$ is the entrywise absolute value. $\rho(A) = \max |\lambda_i|$ is the spectral radius. $A \in \mathbb R^{n \times n}$ is reducible if a permutation $P$ makes $P^T A P = \begin{pmatrix} B & C \\ 0 & D \end{pmatrix}$ with square $B$ and $D$ of positive order, and irreducible otherwise; for $n \ge 2$ this is the same as the strong connectivity of the graph with an edge $i \to j$ when $a_{ij} \ne 0$. We assume $n \ge 2$ for irreducible matrices, so that $A \ne 0$.

**Theorem (Perron 1907, Frobenius 1912).** Let $A \ge 0$ be irreducible and $r = \rho(A)$. Then

1. $r > 0$ and $r$ is an eigenvalue of $A$;
2. there is $v > 0$ with $A v = r v$, and $w > 0$ with $w^T A = r w^T$;
3. $r$ is an algebraically simple eigenvalue;
4. every nonnegative eigenvector of $A$ is a positive multiple of $v$;
5. (Collatz-Wielandt) $r = \max_{x \ge 0, x \ne 0} \min_{i: x_i > 0} (A x)_i / x_i = \min_{x > 0} \max_i (A x)_i / x_i$.

**Theorem (primitive matrices).** If $A \ge 0$ and $A^k > 0$ for some $k \ge 1$, then in addition $|\lambda| < r$ for every eigenvalue $\lambda \ne r$. In particular this holds for every positive matrix ($k = 1$).

**Theorem (period, stated without proof).** If $A \ge 0$ is irreducible and has exactly $h$ eigenvalues of modulus $r$, then they are $r e^{2\pi i k / h}$ for $k = 0, \dots, h - 1$, each simple, the whole spectrum is invariant under rotation by $2\pi/h$, and $h$ is the greatest common divisor of the lengths of the cycles of the graph of $A$ (HJ Section 8.4; Meyer Section 8.3). $A$ is primitive exactly when $h = 1$, and then $A^k > 0$ already for $k = (n-1)^2 + 1$ (Wielandt 1950).

**Theorem (general nonnegative matrices).** If $A \ge 0$ is reducible, $\rho(A)$ is still an eigenvalue with an eigenvector $x \ge 0$, $x \ne 0$, by continuity from $A + \epsilon \mathbf 1 \mathbf 1^T$; but $x$ may have zero entries, $\rho(A)$ may be $0$ or multiple, and it may have a Jordan block.

## In plain words

Think of a network where each link carries a nonnegative weight, and where every node can reach every other node by following links. Then there is one special growth rate, the largest, and one special way of spreading weight over the nodes that grows at exactly this rate. In that special spread, every node gets a positive share, and no other pattern with only nonnegative shares grows in a steady way. If the network is also mixed well enough that, after some number of steps, every node can reach every node, then repeating the network map from any positive start ends in that special spread.

## Proof

Let $A \ge 0$ be irreducible of order $n \ge 2$, and put $B = (I + A)^{n-1}$.

**Step 1: $B > 0$.** By the binomial theorem $B = \sum_{k=0}^{n-1} \binom{n-1}{k} A^k$, and $(A^k)_{ij} > 0$ exactly when the graph has a walk of length $k$ from $i$ to $j$, because all terms in the sum defining $(A^k)_{ij}$ are $\ge 0$. In a strongly connected graph on $n$ nodes, every $j \ne i$ is reached from $i$ by a path of length at most $n - 1$, and $(A^0)_{ii} = 1$. So every entry of $B$ is positive. Also $B$ commutes with $A$, and $B y > 0$ for every $y \ge 0$, $y \ne 0$.

**Step 2: the Collatz-Wielandt function attains its maximum.** For $x \ge 0$, $x \ne 0$, let $f(x) = \min_{i: x_i > 0} (A x)_i / x_i$, the largest $t$ with $A x \ge t x$. It is invariant under positive scaling, and it is bounded by the largest row sum of $A$. If $A x \ge t x$, then $A (B x) = B (A x) \ge t \, B x$ since $B \ge 0$, so $f(Bx) \ge f(x)$. Let $\Delta = \{x \ge 0 : \sum x_i = 1\}$. The set $K = \{B x / \sum_i (Bx)_i : x \in \Delta\}$ is compact and contains only positive vectors, and on positive vectors $f(x) = \min_i (A x)_i / x_i$ is continuous. So $f$ attains its maximum $r^*$ over $K$ at some $v \in K$, $v > 0$, and since $f(x) \le f(Bx)$ for every $x \in \Delta$, $r^* = \max_{x \ge 0, x \ne 0} f(x)$.

**Step 3: $v$ is an eigenvector and $r^* = \rho(A)$.** We have $A v - r^* v \ge 0$. If it is not zero, Step 1 gives $B(A v - r^* v) > 0$, so $A (Bv) > r^* B v$ in every entry, and $f(Bv) > r^*$, a contradiction. So $A v = r^* v$ with $v > 0$. If $r^* = 0$, then $A v = 0$ with $v > 0$ forces $A = 0$, which is reducible for $n \ge 2$; so $r^* > 0$. For any eigenvalue $\lambda$ with $A y = \lambda y$, $y \ne 0$, the triangle inequality gives $|\lambda| |y| = |A y| \le A |y|$, so $f(|y|) \ge |\lambda|$ and $|\lambda| \le r^*$. Hence $r^* = \rho(A) = r$, proving items 1 and the first half of 2. The matrix $A^T$ is irreducible too, which gives $w > 0$.

**Step 4: geometric simplicity.** Let $A z = r z$ with $z \ne 0$. Since $A$ and $r$ are real, the real and imaginary parts of $z$ are in the null space of $A - rI$, so it suffices to treat a real $z$. Suppose $z$ is not a multiple of $v$. Replacing $z$ by $-z$ if needed, some entry of $z$ is positive; let $c = \min_{i: z_i > 0} v_i / z_i > 0$. Then $y = v - c z \ge 0$ (entries with $z_i \le 0$ are at least $v_i > 0$), $y$ is zero at the index of the minimum, $y \ne 0$ because $z$ is not a multiple of $v$, and $A y = r y$. But then $y = B y / (1 + r)^{n-1} > 0$ by Step 1, a contradiction. So the eigenspace of $r$ is spanned by $v$.

**Step 5: algebraic simplicity.** If $r$ were not algebraically simple, then, its eigenspace being one-dimensional, there would be a Jordan chain: a vector $z$ with $(A - r I) z = v$. Multiplying by $w^T$ gives $0 = w^T (A - r I) z = w^T v > 0$, a contradiction. This proves item 3.

**Step 6: nonnegative eigenvectors.** If $A x = \mu x$ with $x \ge 0$, $x \ne 0$, then $\mu w^T x = w^T A x = r w^T x$ and $w^T x > 0$, so $\mu = r$, and by Step 4 $x$ is a multiple of $v$, positive because $x \ge 0$. This is item 4.

**Step 7: Collatz-Wielandt.** The max form is Step 2 and Step 3. For the min form, if $x > 0$ and $A x \le t x$, then $r w^T x = w^T A x \le t w^T x$, so $t \ge r$; and $x = v$ gives $t = r$. This is item 5.

**Step 8: primitive matrices.** First let $A > 0$. If $A y = \lambda y$ with $|\lambda| = r$, then $r |y| \le A |y|$, so $f(|y|) \ge r$, and the argument of Step 3 gives $A |y| = r |y|$. Hence $|\sum_j a_{ij} y_j| = \sum_j a_{ij} |y_j|$ for each $i$, and since all $a_{ij} > 0$ this equality in the triangle inequality forces all $y_j$ to have the same argument: $y = e^{i\phi} |y|$. Then $\lambda y = A y = e^{i\phi} A|y| = r y$, so $\lambda = r$. Now let $A^k > 0$. If $\lambda \ne r$ is an eigenvalue with $|\lambda| = r$ and eigenvector $y$, then $A^k y = \lambda^k y$ with $|\lambda^k| = r^k = \rho(A^k)$, so $\lambda^k = r^k$ by the positive case, and $y$ is a multiple of the Perron vector of $A^k$. That vector is $v$, since $A^k v = r^k v$ and the eigenspace of $r^k$ for $A^k$ is one-dimensional by Step 4 applied to the irreducible matrix $A^k$. So $\lambda v = A v = r v$ and $\lambda = r$, a contradiction. $\blacksquare$

## Consequences

- **Power iteration.** For a primitive $A$ and any start $x_0 \ge 0$, $x_0 \ne 0$, [power iteration](/power-iteration/) converges to $v / \|v\|$ at the rate $|\lambda_2| / r < 1$, since $w^T x_0 > 0$ guarantees a component along $v$.
- **Markov chains.** A row-stochastic matrix $P$ has $\rho(P) = 1$ with right eigenvector $\mathbf 1$. If the chain is irreducible, the stationary distribution $\pi > 0$ with $\pi^T P = \pi^T$ exists and is unique; if it is also aperiodic ($h = 1$), $\mu_0^T P^k \to \pi^T$ for every initial distribution ([Markov chain](/markov-chain/)). [PageRank](/pagerank/) adds a positive teleportation term so that the Google matrix is positive.
- **Bounds on $r$.** The Collatz-Wielandt formula gives $\min_i (A x)_i / x_i \le r \le \max_i (A x)_i / x_i$ for every $x > 0$; with $x = \mathbf 1$, $r$ lies between the smallest and the largest row sums.
- **Monotonicity.** If $0 \le A \le C$ entrywise, then $\rho(A) \le \rho(C)$, with strict inequality when $C$ is irreducible and $A \ne C$.
- **Applications.** Leslie population models (the growth rate and the stable age distribution), input-output economics (Leontief: $(I - A)^{-1} \ge 0$ exists when $\rho(A) < 1$), [eigenvector centrality](/eigenvector-centrality/), the convergence of the Jacobi and Gauss-Seidel iterations for M-matrices, and the growth rate of the number of walks in a graph.

**Example.** $A = \begin{pmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ 1 & 1 & 0 \end{pmatrix}$ is irreducible (the cycle $1 \to 2 \to 3 \to 1$) and has the cycles of lengths 3 and 2 ($2 \to 3 \to 2$), whose greatest common divisor is 1, so it is primitive. Its characteristic polynomial is $t^3 - t - 1$, with the real root $r = 1.324718$ (the plastic number) and a complex pair of modulus $r^{-1/2} = 0.868837$. The Perron vector is $(1, r, r^2)$, normalized to $(0.245122, 0.324718, 0.430160)$, and the left vector is $(1/r, r, 1)$. With $x = \mathbf 1$, $A x = (1, 1, 2)$, so the Collatz-Wielandt bounds give $1 \le r \le 2$. The first power with all entries positive is $A^5 = \begin{pmatrix} 1 & 1 & 1 \\ 1 & 2 & 1 \\ 1 & 2 & 2 \end{pmatrix}$, and $5 = (n-1)^2 + 1$, so this matrix attains Wielandt's bound. Power iteration on it converges at the rate $0.868837 / 1.324718 = 0.6559$ per step.

## Tightness

- **Irreducibility is needed for positivity and simplicity.** $\begin{pmatrix} 1 & 1 \\ 0 & 1 \end{pmatrix}$ is reducible; $\rho = 1$ has the eigenvector $(1, 0)^T$ with a zero entry and a Jordan block of size 2. $I_2$ has $\rho = 1$ double, with nonnegative eigenvectors $e_1$ and $e_2$ that are not multiples.
- **Primitivity is needed for strict dominance.** The cyclic permutation $\begin{pmatrix} 0 & 1 & 0 \\ 0 & 0 & 1 \\ 1 & 0 & 0 \end{pmatrix}$ is irreducible with period $h = 3$; its eigenvalues are the three cube roots of unity, all of modulus $\rho = 1$, and power iteration cycles instead of converging.
- **Nonnegativity is needed.** $\begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}$ has no real eigenvalue at all, and $\begin{pmatrix} 1 & 0 \\ 0 & -2 \end{pmatrix}$ has its dominant eigenvalue negative.
- **Wielandt's exponent is sharp.** The example above needs exactly $(n-1)^2 + 1$ powers; the matrices with a Hamiltonian cycle plus one chord of this shape attain the bound for every $n$.

## History

Oskar Perron proved the theorem for positive matrices in 1907, in work on continued fractions. Georg Frobenius extended it to irreducible nonnegative matrices in 1908, 1909 and 1912, introducing irreducibility and the cyclic structure of the peripheral spectrum. Lothar Collatz (1942) gave the min-max characterization, and Helmut Wielandt (1950) gave the short proof through the function $f$ used above, together with the bound $(n-1)^2 + 1$ on the exponent of a primitive matrix. Markov's work on chains (1906 to 1908) used the stochastic case independently.

## References
