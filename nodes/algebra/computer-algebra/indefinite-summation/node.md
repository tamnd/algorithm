---
tag: 4QG6DF
kind: problem
slug: indefinite-summation
name: Indefinite summation
aliases:
- closed-form summation
- indefinite sum
- antidifference problem
- symbolic summation
area: algebra/computer-algebra
level: core
summary: Given a summand, find a closed form for its partial sums, if one exists.
model: blum-shub-smale-machine
prereqs: [telescoping-sum, hypergeometric-term, finite-differences]
see_also: [gosper-algorithm, definite-summation, zeilberger-algorithm, creative-telescoping, petkovsek-hyper-algorithm, holonomic-function, integration-of-rational-functions, harmonic-series]
sources:
  - book: isbn:9781568810638
    title: Marko Petkovšek, Herbert S. Wilf and Doron Zeilberger, A = B, A K Peters, 1996
    locator: Chapter 5, Gosper's algorithm (the decision procedure for hypergeometric antidifferences, with examples of summable and nonsummable terms)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Chapter 23, Symbolic summation (polynomial summation, greatest factorial factorization, rational summation and Gosper's algorithm, with cost analyses)
  - book: isbn:9780201558029
    title: Ronald L. Graham, Donald E. Knuth and Oren Patashnik, Concrete Mathematics, second edition, Addison-Wesley, 1994
    locator: Section 2.6 (finite and infinite calculus, falling powers and antidifferences) and Section 5.7 (partial hypergeometric sums and Gosper's algorithm)
  - paper: doi:10.1073/pnas.75.1.40
    title: R. William Gosper, Jr., Decision procedure for indefinite hypergeometric summation, Proceedings of the National Academy of Sciences USA 75(1), 40-42, 1978
    locator: the algorithm and the claim that it decides existence
  - paper: doi:10.1145/322248.322255
    title: Michael Karr, Summation in finite terms, Journal of the ACM 28(2), 305-350, 1981
    locator: the theory of difference fields (Pi-Sigma fields) and the summation algorithm in them
---

Indefinite summation asks, for a sequence $f(k)$, for a sequence $F(k)$ in a given class with $F(k + 1) - F(k) = f(k)$. Such an $F$ is an *antidifference* of $f$, and then every partial sum telescopes: $\sum_{k=a}^{b-1} f(k) = F(b) - F(a)$. The problem is the discrete twin of [integration](/integration-of-rational-functions/), with the forward difference $\Delta F = F(k + 1) - F(k)$ in place of the derivative. Polynomials always have polynomial antidifferences, and rational functions are handled by Abramov's algorithm. For [hypergeometric terms](/hypergeometric-term/), [Gosper's algorithm](/gosper-algorithm/) decides whether a hypergeometric antidifference exists. Karr's algorithm extends this to nested sums and products.

## In plain words

You want a formula for $f(0) + f(1) + \cdots + f(n - 1)$ that does not need the dots. The trick is to find a function $F$ whose consecutive differences are the terms: then the sum collapses to the last value of $F$ minus the first. For some summands, like $k^2$ or $k \cdot k!$, such an $F$ exists in the same family of functions. For others, like $1/k$, it does not. The partial sums of $1/k$ are the harmonic numbers, and these are not a rational function of $n$. An algorithm for this problem must either find $F$ or prove that no $F$ of the chosen kind exists.

## Definition

Notation: $K$ is a field of characteristic $0$, $k$ is the summation variable, $E$ is the shift $E F(k) = F(k + 1)$, and $\Delta = E - 1$.

**General form.** A *difference field* is a field $\mathbb{F} \supseteq K(k)$ with an automorphism $\sigma$ that extends the shift. Given $f \in \mathbb{F}$, decide whether there is $g \in \mathbb{F}$ with $\sigma(g) - g = f$, and if so find one. The solution is unique up to adding a constant, an element fixed by $\sigma$.

**The usual classes.**

- *Polynomial.* $f \in K[k]$. An antidifference always exists in $K[k]$, of degree $\deg f + 1$.
- *Rational.* $f \in K(k)$. Find $g \in K(k)$ with $\Delta g = f$, or prove there is none. In general, $f = \Delta g + h$ with $g$ rational and $h$ rational of minimal denominator, the discrete analogue of the rational and logarithmic parts of an integral.
- *Hypergeometric.* $f(k)$ is a [hypergeometric term](/hypergeometric-term/), so $f(k + 1)/f(k) \in K(k)$. Find a hypergeometric $F$ with $\Delta F = f$, or prove there is none. Gosper's key observation is that any such $F$ is $R(k) f(k)$ for a rational $R$, so the problem reduces to the linear difference equation $R(k + 1)\, f(k + 1)/f(k) - R(k) = 1$ for $R \in K(k)$.
- *Nested sums and products.* $f$ lies in a $\Pi\Sigma$ field, a tower of extensions of $K(k)$ by indefinite sums and products. Karr's algorithm decides summability in such towers.

## Variants

- **Definite summation.** Compute $\sum_k f(n, k)$ over all $k$ for which the summand is nonzero, as a function of $n$. Most famous binomial identities are definite sums whose indefinite version has no closed form. [Zeilberger's algorithm](/zeilberger-algorithm/) handles them by [creative telescoping](/creative-telescoping/): it finds a recurrence in $n$ for the definite sum, and [Petkovšek's algorithm Hyper](/petkovsek-hyper-algorithm/) then finds its hypergeometric solutions. See [definite summation](/definite-summation/).
- **Holonomic summation.** For [holonomic](/holonomic-function/) summands, which satisfy linear recurrences with polynomial coefficients, Abramov and van Hoeij and Chyzak give algorithms that find antidifferences satisfying recurrences of the same kind.
- **q-analogues.** Replace the shift $k \mapsto k + 1$ by $q^k \mapsto q^{k+1}$. Gosper's and Zeilberger's algorithms have q-versions.
- **Summation in finite terms with a given extension.** Allow the answer to use new symbols such as harmonic numbers $H_k$, and find the simplest such expression. This is the setting of Karr's theory and of Schneider's refinements.

## Examples

**A polynomial.** In falling powers $k^{\underline{m}} = k (k - 1) \cdots (k - m + 1)$, $\Delta k^{\underline{m+1}} = (m + 1) k^{\underline{m}}$, just as $(x^{m+1})' = (m + 1) x^m$. Since $k^2 = k^{\underline{2}} + k^{\underline{1}}$, an antidifference is $F(k) = k^{\underline{3}}/3 + k^{\underline{2}}/2$, and

$$\sum_{k=0}^{n-1} k^2 = F(n) - F(0) = \frac{(n - 1)\, n\, (2n - 1)}{6}.$$

**A rational function that telescopes.** $\Delta(-1/k) = -\frac{1}{k + 1} + \frac{1}{k} = \frac{1}{k (k + 1)}$, so $\sum_{k=1}^{n-1} \frac{1}{k (k + 1)} = 1 - \frac{1}{n}$.

**A rational function that does not.** $1/k$ has no rational antidifference. Suppose $g(k + 1) - g(k) = 1/k$ with $g = p/q$ in lowest terms. If $q$ is constant, the left side is a polynomial, which $1/k$ is not. Otherwise take a root $\alpha$ of $q$ and look at the roots of $q$ in $\alpha + \mathbb{Z}$. Let $\beta$ be the smallest of them and $\gamma = \beta + m$, $m \ge 0$, the largest. The point $\beta - 1$ is a pole of $g(k + 1)$ but not of $g(k)$, so it is a pole of $1/k$, and $\beta = 1$. The point $\gamma$ is a pole of $g(k)$ but not of $g(k + 1)$, so $\gamma = 0$. Then $m = \gamma - \beta = -1 < 0$, a contradiction. So the harmonic numbers $H_n = \sum_{k=1}^{n} 1/k$ are not a rational function of $n$.

**A hypergeometric term that is summable.** $\Delta k! = (k + 1)! - k! = k \cdot k!$, so $\sum_{k=0}^{n-1} k \cdot k! = n! - 1$. Here $R(k) = 1/k$ in Gosper's form $F = R f$. Also

$$\sum_{j=0}^{k} (-1)^j \binom{n}{j} = (-1)^k \binom{n - 1}{k},$$

a hypergeometric antidifference in $j$.

**A hypergeometric term that is not.** Gosper's algorithm proves that the partial sums $\sum_{j=0}^{k} \binom{n}{j}$ have no hypergeometric closed form in $k$, although the full sum is $2^n$. This is the standard example of why definite summation needs separate methods (A = B, Chapter 5).

## Known algorithms

- **Polynomials.** Convert to the falling power basis, or solve for the coefficients of $F$ by linear algebra. This costs $O(d^2)$ operations in $K$ for $\deg f = d$ classically (von zur Gathen and Gerhard, Chapter 23, also give faster versions).
- **Rational functions.** Abramov's algorithm (1971, 1975) uses the *dispersion* of the denominator, the largest integer $h$ with $\gcd(q(k), q(k + h)) \ne 1$, found from the integer roots of the resultant $\operatorname{res}_k(q(k), q(k + h))$ in $h$. Paule's greatest factorial factorization (1995) is the discrete analogue of the [square-free factorization](/square-free-factorization/) and gives a discrete Hermite reduction.
- **Hypergeometric terms.** [Gosper's algorithm](/gosper-algorithm/) (1978) writes the ratio $f(k + 1)/f(k)$ in a normal form, bounds the degree of a polynomial unknown, and solves a linear system. It is a decision procedure: it either returns $F$ or proves that no hypergeometric antidifference exists.
- **Nested sums and products.** Karr's algorithm (1981) in $\Pi\Sigma$ fields, refined and implemented by Schneider in the Sigma package.
- **Holonomic sequences.** Algorithms of Abramov and van Hoeij, and Chyzak's algorithm for $\partial$-finite functions.

## Bounds

- **Existence.** Every polynomial has a polynomial antidifference. Rational and hypergeometric antidifferences exist only sometimes, and the algorithms above decide existence.
- **The dispersion can be large.** For $q(k) = k (k + N)$ the dispersion is $N$, which is exponential in the bit size of $N$. Any method that loops over all shifts up to the dispersion is therefore exponential in the input size for such inputs.
- **Gosper's degree bound.** The degree bound for the polynomial unknown in Gosper's algorithm can likewise depend on the value of an integer derived from the coefficients, not only on degrees. So the worst-case cost of Gosper's algorithm is polynomial in degrees and these integer values, but not polynomial in the bit size of the input. Von zur Gathen and Gerhard (Chapter 23) give the precise analysis.
- **Output size.** An antidifference can be much larger than the summand. For example, the polynomial antidifference of the single term $k^N$ has degree $N + 1$ and about $N/2$ nonzero terms, whose coefficients involve Bernoulli numbers.

## Reductions

- **To linear algebra.** Polynomial summation and the last step of Gosper's algorithm are linear systems over $K$.
- **To resultants and integer roots.** The dispersion reduces to finding the nonnegative integer roots of a [resultant](/resultant/).
- **From definite summation.** [Creative telescoping](/creative-telescoping/) reduces a definite sum to a parametrized indefinite summation problem: find $c_0, \ldots, c_r$ and $G$ with $\sum_i c_i(n) f(n + i, k) = \Delta_k G(n, k)$. [Zeilberger's algorithm](/zeilberger-algorithm/) solves it with a parametrized Gosper step.
- **Analogy with integration.** Abramov's rational summation mirrors Hermite reduction, and the harmonic numbers play the role that the logarithm plays in [rational integration](/integration-of-rational-functions/).

## Applications

- Closed forms in computer algebra systems, and proofs of combinatorial identities, as in A = B.
- The analysis of algorithms: sums such as $\sum k\, 2^k$ or $\sum \binom{n}{k} k$ in running-time analyses (Concrete Mathematics, Chapter 2 and Section 5.7).
- Symbolic summation in particle physics, where Schneider's methods evaluate large nested sums arising from Feynman integrals.

## References
