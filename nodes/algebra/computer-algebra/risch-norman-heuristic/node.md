---
tag: XPCGZH
kind: algorithm
slug: risch-norman-heuristic
name: Risch-Norman heuristic integration
aliases: [Norman's heuristic integrator, parallel Risch algorithm, parallel integration, Risch-Norman algorithm, poor man's integrator]
area: algebra/computer-algebra
level: advanced
summary: Heuristic symbolic integrator that is fast in practice but not complete.
solves: [symbolic-integration]
model: blum-shub-smale-machine
complexity:
  vars: {N: "the number of unknowns (coefficients of U and log constants)", E: "the number of monomials in the cleared equation", S: "the largest number of terms of a fixed polynomial in the cleared equation"}
  time: {worst: O(N S^2 + E N^2)}
  space: {extra: O(E N)}
properties: {deterministic: true, recursive: false, in_place: false}
prereqs: [risch-algorithm, hermite-reduction, liouville-theorem, gaussian-elimination]
see_also: [symbolic-integration, risch-algorithm, risch-structure-theorem, hermite-reduction, rothstein-trager, lazard-rioboo-trager, integration-of-rational-functions, liouville-theorem]
sources:
  - paper: "Arthur C. Norman and P. M. A. Moore, Implementing the new Risch integration algorithm, Proceedings of the 4th International Colloquium on Advanced Computing Methods in Theoretical Physics, Marseille, 1977"
    locator: the first description of the method (all generators treated at once, one linear system)
  - paper: doi:10.1093/comjnl/22.2.127
    title: S. J. Harrington, A new symbolic integration system in Reduce, The Computer Journal 22(2), 1979
    locator: pp. 127 to 131 (an implementation of the Norman method in Reduce)
  - paper: doi:10.1007/3-540-11607-9_17
    title: James H. Davenport, The parallel Risch algorithm (I), EUROCAM '82, Lecture Notes in Computer Science 144, Springer, 1982
    locator: pp. 144 to 157 (the name, the ansatz and the question of completeness)
  - paper: doi:10.1145/1089302.1089303
    title: James H. Davenport, On the parallel Risch algorithm (III), use of tangents, ACM SIGSAM Bulletin 16(3), 1982
    locator: pp. 3 to 6 (tan instead of complex exponentials)
  - paper: doi:10.1145/6187.6189
    title: James H. Davenport and Barry M. Trager, On the parallel Risch algorithm (II), ACM Transactions on Mathematical Software 11(4), 1985
    locator: pp. 356 to 362 (the denominator of the integral, special and normal factors)
  - paper: doi:10.1016/j.jsc.2007.04.003
    title: Manuel Bronstein, Structure theorems for parallel integration, Journal of Symbolic Computation 42(7), 2007
    locator: pp. 757 to 769 (the denominator and log-candidate theorems, the pmint implementation)
  - book: isbn:9783540214939
    title: Manuel Bronstein, Symbolic Integration I, Transcendental Functions, second edition, Springer, 2005
    locator: Chapter 3 (monomial extensions, normal and special polynomials) and Chapter 5 (the complete Risch algorithm for the transcendental case)
  - paper: doi:10.1016/S0747-7171(08)80027-2
    title: Manuel Bronstein, Integration of elementary functions, Journal of Symbolic Computation 9(2), 1990
    locator: pp. 117 to 173 (the recursive algorithm that the heuristic avoids)
---

The Risch-Norman heuristic, also called the parallel Risch algorithm, integrates a function from a tower of exponentials, logarithms and tangents with one guess and one linear system. It writes down the general shape of the answer: a rational function with a known denominator and an unknown numerator, plus logarithms of known arguments with unknown constant coefficients. It differentiates this guess and matches coefficients. The recursive [Risch algorithm](/risch-algorithm/) treats one extension at a time. This method treats all the generators at once. It is fast and easy to implement, and every answer it gives can be checked by differentiation. But if the guess is too small it fails, even when an elementary integral exists.

## In plain words

To find a function whose derivative is a given formula, first guess the shape of the answer. It will be a fraction whose bottom part we can predict from the bottom of the given formula, and whose top part is an unknown sum of products of the basic pieces, such as x, e^x or log x, each with an unknown number in front. We can also add logarithms of some predicted expressions, each with an unknown number in front.

Then differentiate the guess with the usual rules and require it to equal the given formula. Each power product of the basic pieces gives one equation in the unknown numbers, and the equations are linear. Solve them exactly. If they have a solution, the guess with those numbers is an answer, and we can check it. If not, the guess was wrong, but a bigger guess could still work.

## The problem

**Notation.** $K$ is a field of characteristic $0$, here $K = \mathbb{Q}$. The integrand lies in $E = K(x, \theta_1, \ldots, \theta_m)$, where each $\theta_i$ is transcendental over the field before it and its derivative has the form $\theta_i' = N_i / d$ with $N_i \in K[x, \theta_1, \ldots, \theta_m]$ and one common $d \in K[x]$, $d \ne 0$. For example, $\theta = e^{a(x)}$ gives $N = a' \theta$, $\theta = \log b(x)$ gives $N / d = b' / b$, and $\theta = \tan x$ gives $N = 1 + \theta^2$. The constants of $E$ are $K$. The *scaled derivation* is
$$D = d\, \frac{\partial}{\partial x} + \sum_{i=1}^{m} N_i\, \frac{\partial}{\partial \theta_i},$$
so that $D p = d \cdot p'$ and $D$ maps polynomials to polynomials. A polynomial $q$ is *special* if $q \mid Dq$ and *normal* if $\gcd(q, Dq) = 1$. For example, $\theta = e^x$ is special, since $D\theta = \theta$, and $1 + \tan^2 x$ is special in the tangent tower.

**Input.** $f = P / Q$ with $P, Q \in K[x, \theta]$, where $Q = \prod_k q_k^{e_k}$ is given with pairwise coprime squarefree factors, plus an optional list of extra log candidates and an optional degree bound $\delta$.

**Output.** Either polynomials $U$, $B$ and pairs $(c_j, v_j)$ with $c_j \in K$ such that
$$\int f\, dx = \frac{U}{B} + \sum_j c_j \log v_j,$$
or FAIL. FAIL means that no answer of the guessed shape exists. It does not mean that $f$ has no elementary integral.

## The algorithm

```pseudo id=main
RISCH-NORMAN(P, Q, D, d, extra, δ)                 ▷ f = P/Q in K(x, θ_1..θ_m)
L1  B ← ∏ over normal q_k of q_k^(e_k − 1) · ∏ over special q_k of q_k^(e_k)
L2  V ← the nonconstant factors q_k of Q, then the extra candidates; W ← ∏ v over V
L3  if no δ is given: δ ← max(tdeg P − tdeg Q, 0) + tdeg B + 1
L4  U ← Σ u_μ x^μ0 θ^μ' over all exponents μ with |μ| ≤ δ, with unknowns u_μ
L5  columns: Q W (D(x^μ0 θ^μ') · B − x^μ0 θ^μ' · DB) for each μ, and Dv_j · B² Q W / v_j for each v_j
L6  right side: d P B² W
L7  solve Σ u_μ col_μ + Σ c_j col_j = right side over K, one equation per monomial; if no solution: return FAIL
L8  return U / B + Σ c_j log v_j with the solution, free unknowns set to 0
```

Line L1 predicts the denominator. In the transcendental case a normal factor of multiplicity $e$ in $Q$ occurs at most $e - 1$ times in the denominator of the rational part of the integral, as in [Hermite reduction](/hermite-reduction/). A special factor can stay with its full multiplicity: $\int e^{-x}\, dx = -1/\theta$ has $\theta$ in the denominator. Line L2 picks the log candidates, following [Liouville's theorem](/liouville-theorem/): the logarithms in an elementary integral have arguments that divide the denominator, together with some special polynomials, such as $1 + \tan^2 x$, that the caller must supply. Lines L5 and L6 come from differentiating the guess: $d (U / B)' = (DU \cdot B - U \cdot DB) / B^2$ and $d (\log v)' = Dv / v$, and multiplying through by $d B^2 Q W$ clears all denominators. The equation is linear in the unknowns, so line L7 is [Gaussian elimination](/gaussian-elimination/) over $K$.

## Example

Take $f = x e^{x^2}$. The tower is $\theta = e^{x^2}$ with $d = 1$, $N = 2x\theta$, so $D = \partial_x + 2x\theta\, \partial_\theta$. Here $Q = 1$, so $B = 1$ and there are no log candidates. Take $\delta = 2$:
$$U = u_{00} + u_{10} x + u_{01} \theta + u_{20} x^2 + u_{11} x\theta + u_{02} \theta^2.$$
Then
$$DU = u_{10} + 2u_{20} x + 2u_{01} x\theta + u_{11} (\theta + 2x^2\theta) + 4u_{02} x\theta^2.$$
Matching with $x\theta$ gives $u_{10} = 0$, $u_{20} = 0$, $u_{11} = 0$, $u_{02} = 0$ and $2u_{01} = 1$, while $u_{00}$ is free. With $u_{00} = 0$ the answer is $U = \theta / 2$, that is, $\int x e^{x^2}\, dx = e^{x^2} / 2$.

Take $f = \log x$. The tower is $\theta = \log x$ with $d = x$ and $N = 1$, so $D = x\partial_x + \partial_\theta$. The equation is $DU = x\theta$. With $\delta = 2$, the images are $D x = x$, $D\theta = 1$, $D x^2 = 2x^2$, $D(x\theta) = x\theta + x$ and $D\theta^2 = 2\theta$. Matching gives $u_{11} = 1$, $u_{10} + u_{11} = 0$, and all other unknowns $0$ except the free constant. So $\int \log x\, dx = x\log x - x$.

Take $f = \tan x$ with $\theta = \tan x$, $N = 1 + \theta^2$, and the extra candidate $v = 1 + \theta^2$. Since $Dv = 2\theta(1 + \theta^2)$, the column of $c$ is $2\theta$ times $B^2 Q = 1$, and the solution is $U = 0$ and $c = 1/2$: $\int \tan x\, dx = \frac{1}{2} \log(1 + \tan^2 x)$.

Two failures. For $f = e^{x^2}$, the coefficient of $\theta$ in $DU = \theta$ requires a polynomial $p(x)$ with $p' + 2xp = 1$. This is impossible, because for $p \ne 0$ the left side has degree $\deg p + 1 \ge 1$. So the method fails for every $\delta$, and here the Risch algorithm shows that no elementary integral exists. For $f = 1 / (x^2 - 2)$, the only candidate is $x^2 - 2$, and $c\, (2x) / (x^2 - 2)$ never equals $f$. The answer $\frac{1}{2\sqrt 2} \log \frac{x - \sqrt 2}{x + \sqrt 2}$ needs logarithms of factors over $\mathbb{Q}(\sqrt 2)$, so the method fails although the integral is elementary. All these results are checked in the tests.

## Correctness

The method is *sound*: if it returns an answer, the derivative of the answer is $f$. Multiplying the derivative of the guess by $d B^2 Q W$, which is nonzero, gives exactly the linear system of L5 to L7, and exact elimination finds a solution whenever one exists. So FAIL also has a precise meaning: there are no constants that make the guess work for this $B$, this candidate list and this bound $\delta$. The proof is in the proof file. The method is *not complete*: an elementary integral can need a larger $\delta$, other log arguments, or constants outside $K$. Whether there is a choice of $B$, candidates and degree bound that is always enough is an open question in general. Davenport (1982) gave the first discussion, and Bronstein (2007) proved denominator and candidate theorems that cover many cases.

## Complexity

The cost model is operations in $K$. Let $N$ be the number of unknowns: $\binom{\delta + m + 1}{m + 1}$ coefficients of $U$ plus one constant for each candidate. Let $E$ be the number of distinct monomials in the cleared equation, and $S$ the largest number of terms of a fixed polynomial in it (such as $Q W$, $B$ or $B^2 Q W / v_j$). Building one column multiplies polynomials with at most $S$ terms, so all columns cost $O(N S^2)$. Gauss-Jordan elimination on an $E \times N$ system costs $O(E N^2)$, or $O(E N \min(E, N))$. So the total is $O(N S^2 + E N^2)$ operations, and the matrix takes $O(E N)$ space. These bounds are proved for the procedure.

$N$ grows like $\delta^{m+1}$, so the method is polynomial for a fixed tower height and degree bound, but large towers give large systems. Over $\mathbb{Q}$ the bit cost also depends on coefficient growth in elimination. Fraction-free (Bareiss) elimination keeps it polynomial in the input size. In practice the systems are sparse and solve fast. The heuristic is observed to succeed on most integrals met in practice, which is why systems use it before or instead of the full Risch algorithm. There is no proved bound on how often it succeeds.

## Properties

- Sound: every returned answer is an antiderivative and can be checked by differentiation.
- Not complete: FAIL does not prove that no elementary integral exists.
- Deterministic and not recursive: one linear system, no recursion over the tower.
- The answer is not unique: $U$ is determined up to adding a constant multiple of $B$, and the logarithm of a special factor, such as $\log e^x = x$, can trade places with a term of $U$.
- It works for exponentials, logarithms, tangents and other monomials with $\theta' \in K(x)[\theta]$, all treated in the same way.

## Variants and improvements

- **Bronstein's pmint.** Bronstein's "poor man's integrator" (2005, described in the 2007 paper) works for any tower given by derivatives. It computes $B$ from the squarefree factors of the denominator and their derivatives, adds factors of the leading coefficients and special polynomials as log candidates, and solves the system. It handles many integrals that are not elementary in the sense of the Risch algorithm, such as integrals with special functions in the integrand.
- **Tangents instead of complex exponentials.** Davenport (1982, part III) uses $\tan$ and $\tanh$ to keep trigonometric integrals real. The candidate $1 + \tan^2 x$ is then special and must be supplied.
- **Algebraic constants.** If the system has no solution over $K$, systems can factor the candidates over an extension, or run the [Rothstein-Trager](/rothstein-trager/) or [Lazard-Rioboo-Trager](/lazard-rioboo-trager/) method on the logarithmic part.
- **Larger degree bounds.** Retrying with a larger $\delta$, or with powers of the special factors, recovers integrals that the first guess missed, at a cost that grows quickly with $\delta$.
- **The full algorithm.** The recursive [Risch algorithm](/risch-algorithm/) is complete for elementary towers. It is harder to implement, and it can be slower when the tower is tall.

## When to use it

Use it as the first try in a symbolic integrator, in particular for integrands that mix several exponentials, logarithms and tangents, where the recursive algorithm must order the tower and recurse many times. Use it when an answer that can be checked matters more than a proof of non-integrability. If it fails, and you need to know whether an elementary integral exists, run the full [Risch algorithm](/risch-algorithm/). For rational functions, use [Hermite reduction](/hermite-reduction/) and the [Rothstein-Trager](/rothstein-trager/) method, which are complete and cheaper.

## Pitfalls

- Reading FAIL as "not elementary". Only the full Risch algorithm proves that.
- Forgetting the special log candidates. Without $1 + \tan^2 x$ the method cannot find $\int \tan x\, dx$, since this factor never occurs in the denominator.
- Treating a special factor as normal. Then L1 lowers its exponent, and integrals such as $\int e^{-x}\, dx = -e^{-x}$ are lost.
- A degree bound that is too small. Integrals such as $\int x e^x\, dx = (x - 1) e^x$ need $\delta \ge 2$, and the default bound can be too small for integrands whose numerator cancels.
- A tower that is not transcendental. If $\theta_2 = e^{2x}$ is added next to $\theta_1 = e^x$, the generators are algebraically dependent, the coefficient matching is not valid, and the method can miss answers or give answers with relations hidden in them. Use a [structure theorem](/risch-structure-theorem/) to check the tower first.
- Coefficient growth. Over $\mathbb{Q}$ the linear system can have large entries. Use fraction-free elimination or modular methods for large systems.

## Implementations

## History

Risch (1969, 1970) gave the complete decision procedure for elementary transcendental integrands, which works one extension at a time. Arthur Norman and P. M. A. Moore proposed in 1977 to treat all generators at once with a single ansatz, and implemented it for Reduce. Harrington (1979) described a Reduce integrator built on this idea. Davenport named it the parallel Risch algorithm and studied its completeness in a series of papers from 1982 to 1985, part II with Trager on the denominator and part III on tangents. The heuristic is used in Reduce and, as a first try, in Maple. Bronstein revived it as pmint, a short Maple program, and proved structure theorems for the denominator and the log candidates in a paper that appeared in 2007, after his death. Whether some form of the parallel method is complete remains open.

## References
