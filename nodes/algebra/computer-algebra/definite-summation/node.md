---
tag: C47BYZ
kind: problem
slug: definite-summation
name: Definite summation
aliases:
- definite sums
- parametric summation
- symbolic definite summation
area: algebra/computer-algebra
level: advanced
summary: Find recurrences or closed forms for sums with parameters, such as binomial identities.
prereqs: [hypergeometric-term, indefinite-summation]
see_also: [zeilberger-algorithm, creative-telescoping, wz-method, gosper-algorithm, petkovsek-hyper-algorithm, holonomic-function, binomial-coefficient, telescoping-sum]
sources:
  - book: isbn:9781568810638
    title: Marko Petkovšek, Herbert S. Wilf and Doron Zeilberger, A = B, A K Peters, 1996
    locator: Chapter 4 (Sister Celine's method), Chapter 6 (Zeilberger's algorithm), Chapter 7 (the WZ phenomenon) and Chapter 8 (algorithm Hyper and closed forms)
  - book: isbn:9781107039032
    title: Joachim von zur Gathen and Jürgen Gerhard, Modern Computer Algebra, third edition, Cambridge University Press, 2013
    locator: Chapter 23 (symbolic summation, hypergeometric terms, Gosper's algorithm and the definite case)
  - paper: doi:10.1016/S0747-7171(08)80044-2
    title: Doron Zeilberger, The method of creative telescoping, Journal of Symbolic Computation 11(3), 195-204, 1991
    locator: the algorithm that finds a recurrence in n for a sum over k of a proper hypergeometric term
  - paper: doi:10.1007/BF02100618
    title: Herbert S. Wilf and Doron Zeilberger, An algorithmic proof theory for hypergeometric (ordinary and q) multisum/integral identities, Inventiones Mathematicae 108, 575-633, 1992
    locator: the fundamental theorem that proper hypergeometric terms satisfy recurrences of bounded order, which makes the methods terminate
  - paper: doi:10.1145/322248.322255
    title: Michael Karr, Summation in finite terms, Journal of the ACM 28(2), 305-350, 1981
    locator: the theory of difference fields (Pi-Sigma fields) for indefinite and definite summation beyond hypergeometric terms
---

Definite summation is the problem of evaluating a sum $S(n) = \sum_k F(n, k)$ over all integers $k$, or over bounds that depend on $n$, as a function of the parameter $n$. The typical summand is a hypergeometric term such as a product of binomial coefficients, and the typical goal is a closed form like $\sum_k \binom{n}{k}^2 = \binom{2n}{n}$ or, when none exists, a linear recurrence for $S(n)$ with polynomial coefficients. Unlike [indefinite summation](/indefinite-summation/), the sum often has a closed form even when its partial sums do not. Since Zeilberger's algorithm (1990, 1991) the problem is algorithmic for hypergeometric summands: a computer finds the recurrence, the certificate that proves it, and the closed form if there is one.

## In plain words

Many formulas in counting and probability are sums of binomial coefficients, and the classic question is whether such a sum has a short formula. Mathematicians used to look these up in tables or find them by clever tricks.

Here the computer does the job. It looks for an equation that links the sum for one value of the parameter to the sums for the next few values. That equation comes with a short proof that anyone can check by algebra. If the equation has a simple solution, that solution is the short formula. If it has none, the computer can prove that no short formula of that kind exists.

## Definition

Let $K$ be a field of characteristic 0, usually $\mathbb{Q}$ or $\mathbb{Q}(a, b, \ldots)$ for extra parameters. A term $F(n, k)$ is *hypergeometric* in both variables if $F(n+1, k)/F(n, k)$ and $F(n, k+1)/F(n, k)$ are rational functions in $K(n, k)$; it is *proper hypergeometric* if it has the form

$$F(n, k) = P(n, k) \frac{\prod_{i} (a_i n + b_i k + c_i)!}{\prod_{j} (u_j n + v_j k + w_j)!} \, z^k$$

with a polynomial $P$, integers $a_i, b_i, u_j, v_j$, and constants $c_i, w_j, z$ (see [hypergeometric term](/hypergeometric-term/)). The sum $S(n) = \sum_k F(n, k)$ has *natural boundaries* if, for each $n$, $F(n, k)$ is nonzero for only finitely many $k$; then the sum is over all $k \in \mathbb{Z}$.

**Input:** a proper hypergeometric $F(n, k)$ with natural boundaries, and possibly initial values.
**Output:** either a linear recurrence

$$\sum_{i=0}^{J} a_i(n) \, S(n + i) = 0, \qquad a_i \in K[n],$$

satisfied by $S$, or a closed form for $S(n)$: a linear combination of a fixed number of hypergeometric terms in $n$.

Costs are counted in operations in $K$, with the order $J$ of the recurrence and the degrees of the polynomials as parameters.

## Variants

- **Indefinite summation.** Find $T(k)$ with $T(k+1) - T(k) = F(k)$; decided for hypergeometric terms by [Gosper's algorithm](/gosper-algorithm/).
- **Recurrence form.** Find the recurrence only; this is what [creative telescoping](/creative-telescoping/) produces, and it is the usual endpoint when no closed form exists.
- **Closed form.** Find all hypergeometric solutions of the recurrence with [Petkovšek's algorithm Hyper](/petkovsek-hyper-algorithm/), then match initial values.
- **Proof form (WZ).** Given a conjectured identity $\sum_k F(n, k) = r(n)$, rewrite it as $\sum_k F(n, k)/r(n) = 1$ and find a WZ pair; see the [WZ method](/wz-method/).
- **q-analogues** with $q$-hypergeometric terms, and **multisums** $\sum_{k_1, \ldots, k_m} F(n, k_1, \ldots, k_m)$, both covered by the Wilf-Zeilberger theory.
- **Holonomic summands.** Sums and integrals of holonomic functions, handled by Chyzak's algorithm and by the holonomic systems approach of Zeilberger (1990); see [holonomic function](/holonomic-function/).
- **Difference fields.** Summands built from nested sums and products, such as harmonic numbers, in Karr's $\Pi\Sigma$ fields (1981) and Schneider's extensions.

## Examples

All values below were checked by a script in exact integer and rational arithmetic, for $n$ up to 40 or 50.

- $\sum_k \binom{n}{k} = 2^n$ and $\sum_k (-1)^k \binom{n}{k} = [n = 0]$.
- For $S(n) = \sum_k \binom{n}{k}^2$, Zeilberger's algorithm finds the first-order recurrence $(n+1) S(n+1) - 2(2n+1) S(n) = 0$. With $S(0) = 1$ this gives $S(n) = \binom{2n}{n}$. In WZ form, with $F(n, k) = \binom{n}{k}^2 / \binom{2n}{n}$, the function $G(n, k) = R(n, k) F(n, k)$ with
$$R(n, k) = -\frac{k^2 (3n + 3 - 2k)}{2 (2n + 1)(n + 1 - k)^2}$$
satisfies $F(n+1, k) - F(n, k) = G(n, k+1) - G(n, k)$, which proves that $\sum_k F(n, k)$ is constant, and so equals its value 1 at $n = 0$.
- The Apéry numbers $A(n) = \sum_k \binom{n}{k}^2 \binom{n+k}{k}^2$, which start $1, 5, 73, 1445, 33001$, satisfy
$$(n+1)^3 A(n+1) - (34n^3 + 51n^2 + 27n + 5) A(n) + n^3 A(n-1) = 0,$$
the recurrence in Apéry's proof that $\zeta(3)$ is irrational. Zeilberger's algorithm finds it; Hyper shows that it has no hypergeometric solution, so $A(n)$ has no closed form as a sum of a fixed number of hypergeometric terms.
- The Franel numbers $f(n) = \sum_k \binom{n}{k}^3$, which start $1, 2, 10, 56, 346, 2252$, satisfy $(n+1)^2 f(n+1) = (7n^2 + 7n + 2) f(n) + 8n^2 f(n-1)$, and also have no hypergeometric closed form.

## Known algorithms

- **Sister Celine's method** (Fasenmyer 1945). Look for a recurrence $\sum_{i, j} a_{ij}(n) F(n + i, k + j) = 0$ for the summand itself, by undetermined coefficients, then sum over $k$. It works for proper hypergeometric terms but is slow, since the number of unknowns grows with the square of the order.
- **Zeilberger's algorithm** (creative telescoping). Look for polynomials $a_0(n), \ldots, a_J(n)$ and a hypergeometric $G(n, k)$ with $\sum_i a_i(n) F(n + i, k) = G(n, k+1) - G(n, k)$, using a parametrized version of Gosper's algorithm for $J = 0, 1, 2, \ldots$. Summing over $k$ gives the recurrence. See [Zeilberger's algorithm](/zeilberger-algorithm/) and [creative telescoping](/creative-telescoping/).
- **Hyper** (Petkovšek 1992) finds every hypergeometric solution of a linear recurrence with polynomial coefficients, which decides whether a closed form exists. Extensions find d'Alembertian and Liouvillian solutions (Abramov and Petkovšek; Hendriks and Singer).
- **The WZ method** proves a given identity with a rational certificate $R(n, k)$, checkable by rational function arithmetic.
- **Karr's algorithm** and Schneider's Sigma package for nested sums; **Chyzak's algorithm** and the holonomic methods of Koutschan for holonomic summands.

## Bounds

- **Termination.** For a proper hypergeometric $F(n, k)$, a recurrence of the Sister Celine form exists with order bounded explicitly in terms of the integer coefficients $a_i, b_i, u_j, v_j$ (Wilf and Zeilberger 1992). Hence Zeilberger's algorithm, which finds a telescoper of minimal order, terminates. This is proved.
- **Order.** The recurrence found is not always of minimal order for $S(n)$: a telescoper of order $J$ for $F$ gives a recurrence for $S$, but $S$ can satisfy one of lower order. Sharper order bounds were given later by Apagodu and Zeilberger (2006).
- **Cost.** Each trial order $J$ solves a linear system whose size depends on a degree bound from Gosper's method; the worst-case cost is polynomial in the degree bound, which can be exponential in the bit size of the input because it comes from integer roots of a resultant. Observed performance is good for identities of the sizes found in tables.
- **Closed forms.** Hyper has worst-case cost exponential in the order of the recurrence, because it tries all combinations of factors of the leading and trailing coefficients; this is observed to be the bottleneck for high orders.

## Reductions

- **Definite to indefinite.** Creative telescoping reduces the definite sum to the parametrized indefinite problem $\sum_i a_i(n) F(n + i, k) = \Delta_k G$, solved with Gosper's algorithm. The natural boundaries make the telescoping sum $\sum_k \Delta_k G$ vanish; see [telescoping sum](/telescoping-sum/).
- **Closed form to recurrence solving.** A closed form exists if and only if the recurrence from Zeilberger's algorithm has suitable hypergeometric solutions, which Hyper decides.
- **Integrals.** The continuous analogue, definite integration of hyperexponential functions, reduces in the same way to Almkvist-Zeilberger telescoping.

## Applications

- **Combinatorial identities.** Proving or refuting the identities in tables of binomial sums, and finding new ones.
- **Special functions.** Recurrences and closed forms for hypergeometric series ${}_pF_q$ at special arguments, such as the Chu-Vandermonde and Saalschütz identities.
- **Number theory.** Recurrences like Apéry's, used in irrationality proofs.
- **Physics.** Sums from Feynman diagram calculations, reduced with Karr and Schneider's difference field methods.
- **Analysis of algorithms.** Exact evaluation of the sums that arise in the average-case analysis of algorithms.

## References
