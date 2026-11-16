---
tag: AV5YS6
kind: concept
slug: approximate-degree
name: Approximate degree
aliases:
- deg~(f)
area: complexity/communication-and-query-complexity
level: research
summary: "The least degree of a real polynomial that is within 1/3 of f on every input. It lower-bounds R(f) and 2Q(f), is Theta(sqrt n) for OR and Theta(n) for MAJORITY and PARITY."
prereqs: [query-complexity, minimax-approximation]
see_also: [polynomial-method, quantum-query-complexity, block-sensitivity, chebyshev-polynomials, minimax-approximation, majority-problem, parity-problem, sign-rank]
sources:
  - paper: doi:10.1007/BF01263419
    title: Noam Nisan and Mario Szegedy, On the degree of Boolean functions as real polynomials, Computational Complexity 4(4) (1994)
    locator: pp. 301 to 313 (approximate degree of OR is Theta(sqrt n); bs(f) at most 6 times the square of the approximate degree); conference version in STOC 1992, pp. 462 to 467
  - paper: doi:10.1145/129712.129758
    title: Ramamohan Paturi, On the degree of polynomials that approximate symmetric Boolean functions, 24th ACM Symposium on Theory of Computing (STOC 1992)
    locator: pp. 468 to 474 (approximate degree of every symmetric function)
  - paper: doi:10.1145/502090.502097
    title: Robert Beals, Harry Buhrman, Richard Cleve, Michele Mosca and Ronald de Wolf, Quantum lower bounds by polynomials, Journal of the ACM 48(4) (2001)
    locator: pp. 778 to 797 (Q(f) at least half the approximate degree; D(f) = O(Q(f)^6) for total f)
  - paper: doi:10.1016/S0304-3975(01)00144-X
    title: Harry Buhrman and Ronald de Wolf, Complexity measures and decision tree complexity, a survey, Theoretical Computer Science 288(1) (2002)
    locator: pp. 21 to 43; Section 4.3 (degree and symmetrization), Section 4.4 (approximate degree), Section 6.1 (symmetric functions)
  - paper: doi:10.1145/3406325.3451047
    title: Scott Aaronson, Shalev Ben-David, Robin Kothari, Shravas Rao and Avishay Tal, Degree vs. approximate degree and quantum implications of Huang's sensitivity theorem, 53rd ACM Symposium on Theory of Computing (STOC 2021)
    locator: pp. 1330 to 1342, main results (deg(f) = O(adeg(f)^2) and D(f) = O(Q(f)^4) for total f)
---

The approximate degree $\widetilde{\deg}(f)$ of a Boolean function $f$ is the least degree of a real polynomial that is within $1/3$ of $f$ on every input. It is the measure behind the [polynomial method](/polynomial-method/): the acceptance probability of a quantum algorithm with $T$ queries is a polynomial of degree at most $2T$, so $Q(f) \ge \widetilde{\deg}(f)/2$. It is $\Theta(\sqrt n)$ for OR, which gives the optimality of Grover search, and $\Theta(n)$ for MAJORITY and PARITY. This page defines the measure and computes it; the polynomial method page is the lower bound technique that uses it.

## In plain words

Write a Boolean rule as a formula that adds and multiplies the input bits. The exact formula can need high powers. Now allow a small error: the formula only has to land near the right answer, within one third, on every input. The approximate degree is the smallest power that such a formula needs. A quantum algorithm that looks at the input a few times produces an answer that is exactly such a formula with a small power, so a rule that needs a high power also needs many looks. For "is there a one?", the needed power grows like the square root of the number of bits. For "are most bits ones?", it grows in step with the number of bits.

## The idea

**Definition.** Every $f : \{0,1\}^n \to \{0,1\}$ has a unique multilinear polynomial that equals it on all inputs; its degree is $\deg(f)$. For $0 < \varepsilon < 1/2$,

$$\widetilde{\deg}_\varepsilon(f) = \min \{ \deg(p) : |p(x) - f(x)| \le \varepsilon \text{ for all } x \in \{0,1\}^n \},$$

and $\widetilde{\deg}(f) = \widetilde{\deg}_{1/3}(f)$. A polynomial $p$ can be taken multilinear, because $x_i^2 = x_i$ on $\{0,1\}$. Any other constant $\varepsilon$ changes the value by at most a constant factor: compose $p$ with a fixed univariate polynomial that pushes values near 0 closer to 0 and values near 1 closer to 1. For a partial function, the condition applies only on its domain, and $p$ may take any value elsewhere.

**Relations.** For every total $f$:

| relation | reason |
|---|---|
| $\widetilde{\deg}(f) \le \deg(f) \le D^{dt}(f)$ | a decision tree is a sum over its 1-leaves of products of $x_i$ and $1 - x_i$ |
| $\widetilde{\deg}(f) \le R(f)$ | the acceptance probability is an average of decision tree polynomials |
| $\widetilde{\deg}(f) \le 2 Q(f)$ | Beals et al.; see the [polynomial method](/polynomial-method/) |
| $\mathrm{bs}(f) \le 6 \, \widetilde{\deg}(f)^2$ | Nisan and Szegedy; see [block sensitivity](/block-sensitivity/) |
| $\deg(f) = O(\widetilde{\deg}(f)^2)$ | Aaronson, Ben-David, Kothari, Rao and Tal (2021) |

So for total functions the approximate degree is polynomially related to $D^{dt}$, $R$, $Q$ and $\mathrm{bs}$. With $D^{dt}(f) \le \mathrm{bs}(f)^3$ the table gives $D^{dt}(f) \le 216 \, \widetilde{\deg}(f)^6$, so $D^{dt}(f) = O(Q(f)^6)$, as Beals et al. proved; the 2021 paper improves this to $O(Q(f)^4)$. For partial functions there is no such relation.

**Symmetrization.** For symmetric $f$ the problem has one variable. Let $p$ approximate $f$ and average it over all permutations of the inputs. The average still approximates $f$, has degree at most $\deg(p)$, and is a combination of the sums $V_j(x) = \sum_{|S| = j} \prod_{i \in S} x_i$. Since $V_j(x) = \binom{|x|}{j}$, which is a polynomial of degree $j$ in $|x|$, the average equals $q(|x|)$ for a univariate $q$ with $\deg(q) \le \deg(p)$. This is the lemma of Minsky and Papert. So, for symmetric $f$ with values $f(0), \ldots, f(n)$ by weight,

$$\widetilde{\deg}(f) = \min \{ \deg(q) : |q(k) - f(k)| \le 1/3 \text{ for } k = 0, 1, \ldots, n \}.$$

This is a discrete [minimax approximation](/minimax-approximation/) problem on $n + 1$ points, which a linear program or the [Remez algorithm](/remez-algorithm/) solves exactly.

**Duality.** Since the definition is a linear program, [LP duality](/lp-duality/) gives a certificate for lower bounds: $\widetilde{\deg}_\varepsilon(f) > d$ if and only if there is a function $\psi : \{0,1\}^n \to \mathbb{R}$ with $\sum_x |\psi(x)| = 1$, $\sum_x \psi(x) f(x) > \varepsilon$, and $\sum_x \psi(x) p(x) = 0$ for every $p$ of degree at most $d$. Such a $\psi$ is called a dual polynomial. Most recent lower bounds, for compositions such as AND of ORs, build a dual polynomial explicitly.

**OR: the upper bound.** Let $T_d$ be the [Chebyshev polynomial](/chebyshev-polynomials/) of degree $d$, with $|T_d(t)| \le 1$ on $[-1, 1]$. On $[1, \infty)$ it is convex, with $T_d(1) = 1$ and $T_d'(1) = d^2$, so $T_d(1 + \delta) \ge 1 + d^2 \delta$. Put

$$q(k) = 1 - \frac{T_d\left(\frac{n - k}{n - 1}\right)}{T_d\left(\frac{n}{n - 1}\right)}.$$

Then $q(0) = 0$. For $k = 1, \ldots, n$ the argument lies in $[0, 1]$, so the fraction has absolute value at most $1 / T_d(n/(n-1)) \le 1/(1 + d^2/(n-1))$. With $d = \lceil \sqrt{2(n - 1)} \rceil$ this is at most $1/3$, so $q$ approximates OR with error $1/3$, and $\widetilde{\deg}(\mathrm{OR}_n) = O(\sqrt n)$.

**OR: the lower bound.** Let $q$ approximate OR with error $1/3$. Then $q(0) \le 1/3$ and $q(1) \ge 2/3$, so $q' \ge 1/3$ somewhere in $[0, 1]$, while $-1/3 \le q(k) \le 4/3$ at $k = 0, \ldots, n$. The lemma of Ehlich and Zeller and of Rivlin and Cheney, proved on the [polynomial method](/polynomial-method/) page, gives $\deg(q)^2 \ge (1/3) n / (1/3 + 5/3) = n/6$. So $\widetilde{\deg}(\mathrm{OR}_n) \ge \sqrt{n/6}$, and with the upper bound, $\Theta(\sqrt n)$. Since $\deg(\mathrm{OR}_n) = n$, this also shows that $\deg(f) = O(\widetilde{\deg}(f)^2)$ is tight.

**Paturi's theorem.** For symmetric $f$, let $\Gamma(f) = \min \{ |2k - n + 1| : f(k) \ne f(k + 1) \}$, which is small when $f$ changes value near the middle weight. Then $\widetilde{\deg}(f) = \Theta(\sqrt{n (n - \Gamma(f))})$. OR changes at weight 0, so $\Gamma = n - 1$ and the bound is $\Theta(\sqrt n)$. MAJORITY and PARITY change near the middle, so the bound is $\Theta(n)$. For PARITY the exact value is $n$, by a count of sign changes; see the [parity problem](/parity-problem/).

**Error near 1/2.** As $\varepsilon \to 1/2$, the measure becomes the **threshold degree**: the least degree of a polynomial whose sign equals $(-1)^{f(x)+1}$ on every input. MAJORITY has threshold degree 1, from $|x| - n/2$, but approximate degree $\Theta(n)$. PARITY has threshold degree $n$. The threshold degree is related to [sign rank](/sign-rank/) in communication complexity.

## Examples

**Exact values.** The values below come from an exact rational minimax computation on the symmetric values, checked against an exhaustive search for small $n$.

| $n$ | 2 | 4 | 10 | 11 | 16 | 25 | 36 | 49 | 64 | 100 |
|---|---|---|---|---|---|---|---|---|---|---|
| $\widetilde{\deg}(\mathrm{OR}_n)$ | 1 | 2 | 2 | 3 | 3 | 4 | 4 | 5 | 6 | 7 |
| $\sqrt{n/6}$, lower bound | 0.58 | 0.82 | 1.29 | 1.35 | 1.63 | 2.04 | 2.45 | 2.86 | 3.27 | 4.08 |
| $\lceil \sqrt{2(n-1)} \rceil$, Chebyshev | 2 | 3 | 5 | 5 | 6 | 7 | 9 | 10 | 12 | 15 |

For $n = 1, \ldots, 12$ the values are $1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 3, 3$. For $n$ from 16 to 100 the true value is between $0.67 \sqrt n$ and $0.8 \sqrt n$, well inside the two bounds. The Chebyshev construction has error at most $1/3$ by the proof; on the points $k = 0, \ldots, n$ its actual error is $0.18$ for $n = 4$, $0.22$ for $n = 16$ and $0.23$ for $n = 100$, so a smaller degree is enough.

**Two bits.** For $\mathrm{OR}_2$, the polynomial $\tfrac{2}{3}(x_1 + x_2)$ gives $0$, $2/3$ and $4/3$ at weights 0, 1 and 2, so it has error $1/3$, and $\widetilde{\deg}(\mathrm{OR}_2) = 1$ while $\deg(\mathrm{OR}_2) = 2$. The best linear approximation has error exactly $1/4$; a constant has error $1/2$.

**The best error at each degree.** For $\mathrm{OR}_4$ the least errors are $0.375$ with degree 1 and $0.1667$ with degree 2. For $\mathrm{OR}_{10}$, degree 2 reaches error exactly $1/3$, and degree 1 only $0.45$. For MAJORITY, see the table on the [majority problem](/majority-problem/) page: the values grow about as $n/4$, from 3 at $n = 6$ to 21 at $n = 80$.

**PARITY.** For every $n$ checked, from 1 to 12, the least error with degree $n - 1$ is exactly $1/2$, the error of the constant $1/2$. So no polynomial of degree below $n$ helps at all.

## Where it is used

- **Quantum query lower bounds.** $Q(f) \ge \widetilde{\deg}(f)/2$ gives $Q(\mathrm{OR}_n) = \Omega(\sqrt n)$, so [Grover search](/grover-search/) is optimal (see [Grover optimality](/grover-optimality/)), and $Q = \Theta(n)$ for MAJORITY. For partial functions it also gives the lower bounds for collision and [element distinctness](/element-distinctness/); see the [polynomial method](/polynomial-method/).
- **Classical query complexity.** $\widetilde{\deg}(f) \le R(f)$ and $\mathrm{bs}(f) \le 6 \, \widetilde{\deg}(f)^2$ place it among the polynomially related measures of [query complexity](/query-complexity/).
- **Communication complexity.** Lower bounds on the approximate degree of $f$ lift to lower bounds on the randomized and quantum [communication complexity](/communication-complexity/) of matrices built from $f$, and threshold degree lifts to [sign rank](/sign-rank/).
- **Learning.** A class of functions whose members all have approximate degree at most $d$ can be learned from examples by fitting a polynomial of degree $d$, which has at most $\sum_{j \le d} \binom{n}{j}$ coefficients; this links approximate degree to [PAC learning](/pac-learning/).

## References
