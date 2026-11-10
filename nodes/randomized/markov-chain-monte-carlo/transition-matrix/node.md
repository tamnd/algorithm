---
tag: KQ3CBP
kind: definition
slug: transition-matrix
name: Transition matrix
aliases:
- stochastic matrix
- Markov kernel
area: randomized/markov-chain-monte-carlo
level: intro
summary: The matrix P of a Markov chain, with P(x, y) the probability to go from x to y in one step. Its entries are non-negative, each row sums to 1, and P^t gives the t-step probabilities.
prereqs: [markov-chain, matrix-power, probability-distribution]
see_also: [stationary-distribution, eigenvalue, spectral-radius, perron-frobenius-theorem, power-iteration, spectral-gap, adjacency-matrix, laplacian-matrix]
sources:
  - book: isbn:9781470429621
    title: David A. Levin and Yuval Peres, with Elizabeth L. Wilmer, Markov Chains and Mixing Times, second edition, American Mathematical Society, 2017
    locator: Section 1.1, Markov Chains (the two-state example, equations (1.6), (1.7) and (1.10)); Section 1.3, Irreducibility and Aperiodicity (the lazy version of a chain)
  - book: isbn:9780521633963
    title: J. R. Norris, Markov Chains, Cambridge University Press, 1997
    locator: Section 1.1, Definition and basic properties (n-step transition probabilities)
  - book: isbn:9780821807491
    title: Charles M. Grinstead and J. Laurie Snell, Introduction to Probability, second revised edition, American Mathematical Society, 1997
    locator: Section 11.1, Introduction (the n-step matrix P^n and the distribution uP^n after n steps)
---

A transition matrix, or stochastic matrix, is a square matrix $P$ with non-negative entries in which each row sums to 1. Row $x$ is a [probability distribution](/probability-distribution/) on the states: $P(x, y)$ is the probability that a [Markov chain](/markov-chain/) in state $x$ goes to state $y$ in one step. The page [Markov chain](/markov-chain/) is about the random process; this page is about the matrix and its algebra. Powers of $P$ give the $t$-step probabilities, a distribution $\mu$ (a row vector) evolves as $\mu P^t$, and a function $f$ (a column vector) evolves as $P^t f$.

## Definition

Let $\mathcal X$ be a finite set with $n$ elements. A *transition matrix* (or *row-stochastic matrix*) on $\mathcal X$ is a matrix $P \in \mathbb R^{\mathcal X \times \mathcal X}$ with
$$
P(x, y) \ge 0 \quad \text{for all } x, y, \qquad \sum_{y \in \mathcal X} P(x, y) = 1 \quad \text{for all } x.
$$
The second condition says $P\mathbf 1 = \mathbf 1$, where $\mathbf 1$ is the all-ones column vector.

**Conventions.** On these pages a distribution is a row vector and a function is a column vector. Some books use column-stochastic matrices and write $P\mu$; their matrix is the transpose of ours. On a general state space, $P$ is replaced by a *Markov kernel* $K(x, A)$: a probability measure $K(x, \cdot)$ for each $x$, measurable in $x$ for each set $A$. The pages of this group use finite state spaces.

**Four rules.** Let $(X_t)$ be a Markov chain with transition matrix $P$.

1. *$t$-step probabilities.* $\Pr[X_{s+t} = y \mid X_s = x] = P^t(x, y)$ when $\Pr[X_s = x] > 0$. In particular the *Chapman-Kolmogorov equations* $P^{s+t}(x, y) = \sum_z P^s(x, z)P^t(z, y)$ hold, because they are the rule for a matrix product.
2. *Distributions.* If $X_0 \sim \mu$, then $X_t \sim \mu P^t$.
3. *Functions.* For $f : \mathcal X \to \mathbb R$, $\mathbb E_x[f(X_t)] = (P^t f)(x)$.
4. *Products.* A product of transition matrices on the same set is a transition matrix. A convex combination of transition matrices is a transition matrix.

*Proof.* Rule 1 for $t = 1$ is the definition of a Markov chain. For the step from $t$ to $t + 1$, condition on $X_{s+t}$: by the Markov property, $\Pr[X_{s+t+1} = y \mid X_s = x] = \sum_z \Pr[X_{s+t} = z \mid X_s = x]\,P(z, y) = \sum_z P^t(x, z)P(z, y) = P^{t+1}(x, y)$. Rule 2 follows by summing rule 1 over $x$ with the weights $\mu(x)$. Rule 3 follows from rule 1 with $s = 0$: $\mathbb E_x f(X_t) = \sum_y P^t(x, y)f(y)$. For rule 4, the entries of $PQ$ are sums of products of non-negative numbers, and $PQ\mathbf 1 = P\mathbf 1 = \mathbf 1$. A convex combination keeps both conditions because they are linear and closed under convex combinations. $\square$

**Spectrum.** The number 1 is an [eigenvalue](/eigenvalue/) of $P$, with right [eigenvector](/eigenvector/) $\mathbf 1$. Each eigenvalue $\lambda$ of $P$ has $|\lambda| \le 1$, so the [spectral radius](/spectral-radius/) of $P$ is 1.

*Proof.* $P\mathbf 1 = \mathbf 1$ is the row-sum condition. If $Pv = \lambda v$ with $v \ne 0$ (complex entries allowed), choose $x$ with $|v(x)|$ largest. Then $|\lambda|\,|v(x)| = |\sum_y P(x, y)v(y)| \le \sum_y P(x, y)|v(y)| \le |v(x)|$, so $|\lambda| \le 1$. $\square$

A left eigenvector for the eigenvalue 1 with non-negative entries that sum to 1 is a [stationary distribution](/stationary-distribution/). That page proves that one exists for each $P$, and that it is unique when $P$ is [irreducible](/irreducibility/). The [Perron-Frobenius theorem](/perron-frobenius-theorem/) gives more for irreducible non-negative matrices. The gap between 1 and the other eigenvalues controls the speed of convergence; see [spectral gap](/spectral-gap/).

**The lazy version.** For a transition matrix $P$, the *lazy* matrix is $P_L = \tfrac12(I + P)$. The chain stays put with probability at least $1/2$ and otherwise takes a step of $P$. By rule 4, $P_L$ is a transition matrix. It has the same stationary distributions as $P$, because $\mu P_L = \mu$ if and only if $\mu P = \mu$. Its eigenvalues are $(1 + \lambda)/2$ for the eigenvalues $\lambda$ of $P$, so they all lie in $[0, 1]$ when $P$ has real eigenvalues. Laziness removes periodic behavior; see [aperiodicity](/aperiodicity/).

## Examples and non-examples

**The Land of Oz.** With the states rain, nice, snow (see [Markov chain](/markov-chain/)),
$$
P = \begin{pmatrix} 1/2 & 1/4 & 1/4 \\ 1/2 & 0 & 1/2 \\ 1/4 & 1/4 & 1/2 \end{pmatrix}, \qquad
P^2 = \begin{pmatrix} 7/16 & 3/16 & 3/8 \\ 3/8 & 1/4 & 3/8 \\ 3/8 & 3/16 & 7/16 \end{pmatrix}.
$$
For example, $P^2(N, N) = \sum_z P(N, z)P(z, N) = \tfrac12 \cdot \tfrac14 + 0 + \tfrac12 \cdot \tfrac14 = \tfrac14$: a nice day comes two days after a nice day with probability $1/4$. The eigenvalues of $P$ are $1$, $1/4$ and $-1/4$.

**Two states.** For $0 < a + b < 2$,
$$
P = \begin{pmatrix} 1 - a & a \\ b & 1 - b \end{pmatrix}, \qquad
P^t = \frac{1}{a + b}\begin{pmatrix} b & a \\ b & a \end{pmatrix} + \frac{(1 - a - b)^t}{a + b}\begin{pmatrix} a & -a \\ -b & b \end{pmatrix}.
$$
The formula is true for $t = 0$. Multiplying the first matrix by $P$ does not change it, and multiplying the second matrix by $P$ multiplies it by $1 - a - b$, so the formula is true for all $t$. The eigenvalues are 1 and $1 - a - b$. Each row of $P^t$ tends to $(b, a)/(a + b)$, and the error falls by the factor $|1 - a - b|$ at each step.

**Random walk on a graph.** For a graph with [adjacency matrix](/adjacency-matrix/) $A$ and diagonal degree matrix $D$, the simple random walk has $P = D^{-1}A$. The normalized [Laplacian matrix](/laplacian-matrix/) $I - D^{-1/2}AD^{-1/2}$ is similar to $I - P$, so the two have the same eigenvalues.

**Doubly stochastic matrices.** If the columns also sum to 1, then the uniform distribution is stationary: $(\mathbf 1^\top/n)P = \mathbf 1^\top/n$. Card shuffles have this form; see [card shuffling](/card-shuffling/).

**A permutation matrix.** The matrix of the cycle $0 \to 1 \to 2 \to 0$ is a transition matrix. Its powers repeat with period 3 and never converge. Its eigenvalues are the three cube roots of unity, all of modulus 1.

**Non-examples.** A matrix with a negative entry is not a transition matrix. A *substochastic* matrix, with row sums at most 1, describes a chain that can be killed; it becomes a transition matrix if an extra absorbing "cemetery" state takes the missing mass. The matrix $\begin{pmatrix} 1/2 & 1/2 \\ 1/3 & 1/3 \end{pmatrix}$ is not stochastic, and its second row is not a distribution.

## Related definitions

- [Markov chain](/markov-chain/): the random process that a transition matrix and an initial distribution define.
- [Stationary distribution](/stationary-distribution/): a probability row vector $\pi$ with $\pi P = \pi$.
- [Irreducibility](/irreducibility/) and [aperiodicity](/aperiodicity/): properties of the pattern of non-zero entries of $P$.
- [Detailed balance](/detailed-balance/): $\pi(x)P(x, y) = \pi(y)P(y, x)$. Then $P$ is self-adjoint for the inner product weighted by $\pi$, and its eigenvalues are real; see [spectral gap](/spectral-gap/).
- [Matrix power](/matrix-power/) and [matrix exponentiation](/matrix-exponentiation/): ways to compute $P^t$. [Power iteration](/power-iteration/) computes $\pi$ as the limit of $\mu P^t$ for an irreducible aperiodic $P$.

## References
