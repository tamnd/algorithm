---
tag: P5EAGN
kind: theorem
slug: delsarte-lp-bound
name: Delsarte linear programming bound
aliases:
- LP bound
- Delsarte LP bound
- linear programming bound for codes
area: compression-and-coding/error-correcting-codes
level: research
summary: "The distance distribution of any code satisfies Krawtchouk inequalities, so a linear program bounds A_q(n, d). It gives the best known asymptotic bounds."
prereqs: [minimum-distance, linear-programming-problem, lp-duality]
see_also: [macwilliams-identity, hamming-bound, elias-bound, plotkin-bound, gilbert-varshamov-bound, simplex-method, bland-rule, golay-code]
sources:
  - paper: "P. Delsarte, Bounds for unrestricted codes, by linear programming, Philips Research Reports 27, 1972, pages 272 to 289"
    locator: the linear program on the distance distribution of a code that need not be linear
  - paper: "P. Delsarte, An algebraic approach to the association schemes of coding theory, Philips Research Reports Supplements 10, 1973"
    locator: the inequalities for the inner distribution of a subset of an association scheme, and the linear programming bound
  - paper: doi:10.1109/TIT.1977.1055688
    title: R. J. McEliece, E. R. Rodemich, H. Rumsey and L. R. Welch, New upper bounds on the rate of a code via the Delsarte-MacWilliams inequalities, IEEE Transactions on Information Theory 23(2), 1977
    locator: pp. 157 to 166 (the first and second asymptotic bounds from the linear program)
  - paper: doi:10.1109/tit.2005.851748
    title: A. Schrijver, New code upper bounds from the Terwilliger algebra and semidefinite programming, IEEE Transactions on Information Theory 51(8), 2005
    locator: pp. 2859 to 2866 (a semidefinite strengthening of the linear program)
  - book: isbn:9780521782807
    title: W. Cary Huffman and Vera Pless, Fundamentals of Error-Correcting Codes, Cambridge University Press, 2003
    locator: Chapter 2 (Krawtchouk polynomials and the linear programming upper bound)
  - url: https://aeb.win.tue.nl/codes/binary-1.html
    title: A. E. Brouwer, Table of general binary codes
    locator: the values of A(n, d) for n up to 24 compared with the bound on this page
---

The Delsarte linear programming bound (LP bound) is an upper bound on the size of a code obtained by solving a linear program. The variables are the distance distribution of the code: how many pairs of codewords lie at each distance. Delsarte proved that these numbers satisfy a family of linear inequalities built from Krawtchouk polynomials, for every code, linear or not. Maximizing the code size under these inequalities gives a bound that is exact for many small parameters, and its asymptotic analysis gives the best known upper bounds on the rate of binary codes.

## Statement

Notation. $C$ is a code of length $n$ over an alphabet of $q$ symbols, with $|C| = M$ words and minimum distance $d$. $A_q(n, d)$ is the largest such $M$. The *distance distribution* of $C$ is

$$A_i = \frac{1}{M} \, \#\{(x, y) \in C^2 : d(x, y) = i\}, \qquad i = 0, \dots, n,$$

so $A_0 = 1$, $A_1 = \dots = A_{d-1} = 0$, $A_i \ge 0$ and $\sum_i A_i = M$. The Krawtchouk polynomial of degree $k$ is

$$K_k(x) = \sum_{j=0}^{k} (-1)^j (q - 1)^{k - j} \binom{x}{j} \binom{n - x}{k - j}, \qquad k = 0, \dots, n .$$

**Theorem (Delsarte inequalities).** For every code $C$ and every $k = 0, \dots, n$,

$$\sum_{i=0}^{n} A_i K_k(i) \ge 0 .$$

For a linear code, $\frac{1}{M}\sum_i A_i K_k(i)$ is the number of words of weight $k$ in the dual code (the [MacWilliams identity](/macwilliams-identity/)).

**Theorem (LP bound).** $A_q(n, d) \le 1 + L$, where $L$ is the optimum of the linear program

$$\text{maximize } \sum_{i=d}^{n} A_i \quad \text{subject to} \quad \sum_{i=d}^{n} A_i K_k(i) \ge -\binom{n}{k}(q - 1)^k \ (k = 1, \dots, n), \quad A_i \ge 0 .$$

For binary codes with $d$ even one may also set $A_i = 0$ for odd $i$.

**Theorem (dual form).** Let $f(x) = 1 + \sum_{k=1}^{n} f_k K_k(x)$ with all $f_k \ge 0$ and $f(i) \le 0$ for $i = d, \dots, n$. Then $A_q(n, d) \le f(0)$. By [LP duality](/lp-duality/), the best such $f$ gives exactly $1 + L$.

**Asymptotic form (binary).** McEliece, Rodemich, Rumsey and Welch (1977) derived from the linear program that every family of binary codes with relative distance $\delta < 1/2$ has rate

$$R \le h\left(\tfrac12 - \sqrt{\delta(1 - \delta)}\right) + o(1),$$

where $h$ is the binary entropy function. This is the first MRRW bound. They also proved a second, stronger bound for small $\delta$.

## In plain words

Instead of counting balls, look at the list of distances between all pairs of codewords. Not every list of numbers can come from a code: a hidden symmetry of the Hamming space forces certain weighted sums of these numbers to be at least zero. So the code size is at most the best value of a linear program whose unknowns are the counts of each distance. A computer solves it exactly for short codes, and any feasible solution of the dual program is a short certificate of the bound.

## Proof

*Characters.* Identify the alphabet with $\mathbb{Z}_q$ and let $\omega = e^{2\pi i/q}$. For $z \in \mathbb{Z}_q^n$ let $\chi_z(u) = \omega^{z \cdot u}$. If $u$ has weight $w$, then

$$\sum_{\mathrm{wt}(z) = k} \chi_z(u) = K_k(w).$$

To see this, sum over the support $S$ of $z$, $|S| = k$. A position $j \in S$ with $u_j \ne 0$ contributes $\sum_{a \ne 0} \omega^{a u_j} = -1$, and a position with $u_j = 0$ contributes $q - 1$. If $S$ meets the support of $u$ in $j$ positions, the product is $(-1)^j (q - 1)^{k - j}$, and there are $\binom{w}{j}\binom{n - w}{k - j}$ such sets.

*Delsarte inequalities.* By the identity,

$$M \sum_i A_i K_k(i) = \sum_{x, y \in C} K_k(d(x, y)) = \sum_{\mathrm{wt}(z) = k} \sum_{x, y \in C} \chi_z(x - y) = \sum_{\mathrm{wt}(z) = k} \Big| \sum_{x \in C} \chi_z(x) \Big|^2 \ge 0 .$$

*LP bound.* The distance distribution of $C$ satisfies $A_0 = 1$, $A_i = 0$ for $0 < i < d$, $A_i \ge 0$, and the inequalities. Since $K_k(0) = \binom{n}{k}(q - 1)^k$, the inequality for $k$ reads $\sum_{i \ge d} A_i K_k(i) \ge -K_k(0)$. So $(A_d, \dots, A_n)$ is feasible and $M - 1 = \sum_{i \ge d} A_i \le L$. For binary codes with $d$ even, puncture $C$ in one position and add an overall parity bit. The new code has the same size, minimum distance at least $d$ and only even distances, so the restriction to even $i$ is valid for a code of size $A_2(n, d)$.

*Dual form.* Let $B_k = \sum_i A_i K_k(i) \ge 0$. Then

$$M = \sum_i A_i \le \sum_i A_i + \sum_{k \ge 1} f_k B_k = \sum_i A_i f(i) = f(0) + \sum_{i \ge d} A_i f(i) \le f(0).$$

The linear program in the statement and the program "minimize $f(0)$ over such $f$" are a primal and dual pair, so by strong duality their optima agree. $\blacksquare$

The proof of the MRRW bound chooses an explicit polynomial $f$ built from Christoffel-Darboux kernels of Krawtchouk polynomials and estimates their zeros. It is long, and the page does not reproduce it.

## Consequences

**Exact values for short codes.** The implementation solves the linear program exactly with the [simplex method](/simplex-method/) over rational numbers, using [Bland's rule](/bland-rule/) so that it cannot cycle. The constraints are of the form $-\sum_i A_i K_k(i) \le K_k(0)$ with a nonnegative right side, so the origin is a feasible start. It also reads off the optimal dual polynomial and checks the dual conditions, which certifies the bound. The table compares the result with the values of $A_2(n, d)$ from Brouwer's table and with the [Hamming bound](/hamming-bound/):

| $n$ | $d$ | LP optimum $1 + L$ | LP bound | $A_2(n, d)$ | Hamming bound |
|---|---|---|---|---|---|
| 8 | 6 | 3 | 3 | 2 | 6 |
| 9 | 4 | 128/5 | 25 | 20 | 51 |
| 10 | 4 | 128/3 | 42 | 40 | 93 |
| 11 | 4 | 256/3 | 85 | 72 | 170 |
| 12 | 4 | 512/3 | 170 | 144 | 315 |
| 12 | 6 | 24 | 24 | 24 | 51 |
| 12 | 8 | 4 | 4 | 4 | 13 |
| 17 | 4 | 32768/9 | 3640 | 3072 to 3276 | 7281 |
| 20 | 6 | 149504/63 | 2373 | 2048 to 2279 | 4969 |
| 23 | 7 | 4096 | 4096 | 4096 | 4096 |
| 24 | 8 | 4096 | 4096 | 4096 | 7216 |

For every $n \le 12$ and every $d$ the tests check that the LP bound is at least the tabulated value, and that the dual polynomial proves the same number. At $(24, 8)$ the LP bound gives 4096, which the extended [Golay code](/golay-code/) meets, while the Hamming bound gives 7216.

**Where it is weak.** At $(8, 6)$ the LP bound is 3 but the true value is 2. The binary [Plotkin bound](/plotkin-bound/) gets 2 because it uses the parity of $M$, an integer fact that a linear program cannot see. At $(17, 4)$ and $(20, 6)$ the best known upper bounds are lower than the LP bound. Schrijver (2005) strengthened the method with semidefinite programming over triples of codewords, which improves the bound for several small parameters.

**Asymptotic bounds.** For binary codes the first MRRW bound is below the [Elias bound](/elias-bound/) for $\delta$ above about 0.15:

| $\delta$ | 0.05 | 0.10 | 0.20 | 0.30 | 0.40 | 0.45 |
|---|---|---|---|---|---|---|
| Elias | 0.8279 | 0.7019 | 0.4920 | 0.3117 | 0.1495 | 0.0734 |
| MRRW (first) | 0.8582 | 0.7219 | 0.4690 | 0.2502 | 0.0815 | 0.0253 |
| GV (lower bound) | 0.7136 | 0.5310 | 0.2781 | 0.1187 | 0.0290 | 0.0072 |

Near $\delta = 1/2$, writing $\delta = 1/2 - \varepsilon$, the first MRRW bound is of order $\varepsilon^2 \log(1/\varepsilon)$, and the [Gilbert-Varshamov bound](/gilbert-varshamov-bound/) is of order $\varepsilon^2$. The gap between them is still open.

**Other spaces.** The same method works in any association scheme: for constant weight codes with Hahn polynomials, and for spherical codes and designs with Gegenbauer polynomials. Delsarte's 1973 thesis set up this general frame.

## Tightness

For a perfect code, the LP bound is never above the Hamming bound, so it is met: the tests find 16 at $(7, 3)$, 2048 at $(15, 3)$ and 4096 at $(23, 7)$. For the extended Golay code it gives 4096 at $(24, 8)$, and the optimal solution that the implementation finds is the distance distribution $A_8 = 759$, $A_{12} = 2576$, $A_{16} = 759$, $A_{24} = 1$ of that code. The bound is not exact in general, as the cases at $(8, 6)$, $(9, 4)$ and $(12, 4)$ show. Asymptotically, the gap between the MRRW bounds and the GV bound is open, and stronger methods such as semidefinite programs have not closed it.

## History

MacWilliams (1963) proved the identity that relates the weight distribution of a linear code to that of its dual. Delsarte saw that the transformed numbers are nonnegative even for nonlinear codes, and turned this into a linear program (1972). His 1973 thesis placed it in the theory of association schemes. McEliece, Rodemich, Rumsey and Welch (1977) analysed the program asymptotically and obtained the best known upper bounds on the rate of binary codes. Schrijver (2005) introduced the semidefinite extension.

## References
