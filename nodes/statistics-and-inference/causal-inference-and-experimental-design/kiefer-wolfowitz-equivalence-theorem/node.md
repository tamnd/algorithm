---
tag: VJG7NG
kind: theorem
slug: kiefer-wolfowitz-equivalence-theorem
name: Kiefer-Wolfowitz equivalence theorem
aliases:
- general equivalence theorem
area: statistics-and-inference/causal-inference-and-experimental-design
level: advanced
summary: A design is D-optimal if and only if it is G-optimal, minimizing the largest prediction variance, which then equals the number of parameters at the support points.
prereqs: [optimal-experimental-design, ordinary-least-squares, positive-definite-matrix, determinant, caratheodory-theorem]
see_also: [fedorov-exchange-algorithm, minimum-volume-enclosing-ellipsoid, khachiyans-algorithm, response-surface-methodology, fisher-information-matrix, convex-function, kkt-conditions, spectral-theorem]
sources:
  - paper: doi:10.4153/CJM-1960-030-4
    title: "J. Kiefer and J. Wolfowitz, The equivalence of two extremum problems, Canadian Journal of Mathematics 12, 1960, pp. 363 to 366"
    locator: The whole paper (D-optimality, G-optimality and the condition that the largest variance function equals the number of parameters are equivalent)
  - paper: doi:10.1111/j.2517-6161.1959.tb00338.x
    title: "J. Kiefer, Optimum experimental designs, Journal of the Royal Statistical Society, Series B 21(2), 1959, pp. 272 to 304"
    locator: The whole paper (approximate designs as probability measures and the optimality criteria for them)
  - paper: doi:10.1214/aos/1176342810
    title: "J. Kiefer, General equivalence theory for optimum designs (approximate theory), Annals of Statistics 2(5), 1974, pp. 849 to 879"
    locator: The whole paper (equivalence theorems for general concave criteria, including A- and E-optimality)
  - paper: doi:10.1214/aoms/1177697374
    title: "Corwin L. Atwood, Optimal and efficient designs of experiments, Annals of Mathematical Statistics 40(5), 1969, pp. 1570 to 1602"
    locator: The whole paper (the bound of the D-efficiency of a design by its G-efficiency; general locator)
  - book: isbn:9780898716047
    title: Friedrich Pukelsheim, Optimal Design of Experiments, SIAM Classics in Applied Mathematics 50, 2006 (reprint of the Wiley edition of 1993)
    locator: Chapter 7 (Section 7.14, the general equivalence theorem), Chapter 8 (optimal moment matrices and optimal designs) and Chapter 9 (Sections 9.2 to 9.4, the G-criterion, the bound for global optimality and the Kiefer-Wolfowitz theorem)
  - book: isbn:9780199296606
    title: A. C. Atkinson, A. N. Donev and R. D. Tobias, Optimum Experimental Designs, with SAS, Oxford University Press, 2007
    locator: Chapter 9 (optimum design theory and the general equivalence theorem) and Chapter 11 (D-optimum designs)
---

The Kiefer-Wolfowitz equivalence theorem says that two natural goals for a regression experiment give the same designs. The first goal, D-optimality, makes the confidence ellipsoid of the coefficients as small as possible. The second goal, G-optimality, makes the worst variance of a predicted mean over the design region as small as possible. For approximate designs (designs given as proportions of runs), a design meets one goal exactly when it meets the other, and exactly when its standardized prediction variance never exceeds $p$, the number of coefficients. The last condition is easy to check, so the theorem is both the test of optimality and the basis of the algorithms of [optimal experimental design](/optimal-experimental-design/).

## Statement

Let $\mathcal X$ be a compact set and $f : \mathcal X \to \mathbb R^p$ a continuous map whose $p$ coordinate functions are linearly independent on $\mathcal X$. The model is $y = f(x)^\top\theta + \varepsilon$ with uncorrelated errors of mean 0 and equal variance $\sigma^2$. An approximate design $\xi$ is a probability measure on $\mathcal X$ with finite support: weights $w_1, \dots, w_m > 0$ with sum 1 at points $x_1, \dots, x_m$. Its moment matrix and its standardized variance function are

$$M(\xi) = \sum_{i=1}^m w_i f(x_i)f(x_i)^\top, \qquad d(x, \xi) = f(x)^\top M(\xi)^{-1}f(x).$$

If $N$ runs are spread with $Nw_i$ runs at $x_i$, the [ordinary least squares](/ordinary-least-squares/) estimate $\hat\theta$ has covariance $\sigma^2M(\xi)^{-1}/N$, and the predicted mean at $x$ has variance $\sigma^2d(x, \xi)/N$. A design $\xi^*$ is D-optimal if it maximizes $\det M(\xi)$ over all designs, and G-optimal if it minimizes $\max_{x \in \mathcal X}d(x, \xi)$ over all designs with a nonsingular $M(\xi)$.

**Theorem (Kiefer and Wolfowitz, 1960).** For a design $\xi^*$ with nonsingular $M(\xi^*)$, these three statements are equivalent:

1. $\xi^*$ is D-optimal.
2. $\xi^*$ is G-optimal.
3. $\max_{x \in \mathcal X}d(x, \xi^*) = p$.

In addition, a D-optimal design exists; all D-optimal designs have the same moment matrix; $d(x_i, \xi^*) = p$ at every support point of a D-optimal design; and some D-optimal design has at most $p(p+1)/2$ support points.

## In plain words

You plan where to run an experiment so that a fitted curve is as good as possible. One plan makes the uncertainty about the curve's coefficients smallest overall. Another plan makes the worst uncertainty about the predicted curve, anywhere in the region, smallest. The theorem says the two plans are the same plan. It also gives a simple test: compute the prediction uncertainty everywhere. If it never goes above the number of coefficients, the plan is best, and at the chosen points it equals that number. If the uncertainty goes above that number somewhere, that place is where you should add runs, and that idea gives the standard search methods.

## Proof

Write $M = M(\xi)$ when the design is clear. Every $M(\xi)$ is symmetric and [positive semidefinite](/positive-definite-matrix/).

**Lemma 1 (the mean of $d$).** If $M(\xi)$ is nonsingular, then $\sum_i w_i d(x_i, \xi) = p$. So $\max_x d(x, \xi) \ge p$, and if $\max_x d(x, \xi) = p$, then $d(x_i, \xi) = p$ at every support point.

*Proof.* $\sum_i w_i f(x_i)^\top M^{-1}f(x_i) = \operatorname{tr}\bigl(M^{-1}\sum_i w_if(x_i)f(x_i)^\top\bigr) = \operatorname{tr}(M^{-1}M) = p$. A weighted mean with positive weights of numbers that are all at most $p$ equals $p$ only if every number equals $p$. $\square$

**Lemma 2 (derivative and concavity of $\log\det$).** Let $A$ be positive definite and $B$ positive semidefinite, both $p \times p$ and symmetric, and let $\varphi(\alpha) = \log\det\bigl((1 - \alpha)A + \alpha B\bigr)$ for $0 \le \alpha < 1$. Then $\varphi'(0) = \operatorname{tr}(A^{-1}B) - p$, and $\varphi$ is concave. It is strictly concave unless $B = A$.

*Proof.* Let $C = A^{-1/2}BA^{-1/2}$, with eigenvalues $\mu_1, \dots, \mu_p \ge 0$ by the [spectral theorem](/spectral-theorem/). Since $(1 - \alpha)A + \alpha B = A^{1/2}\bigl((1 - \alpha)I + \alpha C\bigr)A^{1/2}$,

$$\varphi(\alpha) = \log\det A + \sum_{j=1}^p\log(1 - \alpha + \alpha\mu_j),$$

and every term is defined for $0 \le \alpha < 1$. Then $\varphi'(0) = \sum_j(\mu_j - 1) = \operatorname{tr}C - p = \operatorname{tr}(A^{-1}B) - p$ and $\varphi''(\alpha) = -\sum_j(\mu_j - 1)^2/(1 - \alpha + \alpha\mu_j)^2 \le 0$, with equality only if all $\mu_j = 1$, that is $C = I$ and $B = A$. If $B$ is also positive definite, the same formula holds on $[0, 1]$. $\square$

The moment matrix is linear in the design: for designs $\xi$ and $\eta$ and the mixture $\xi_\alpha = (1 - \alpha)\xi + \alpha\eta$, $M(\xi_\alpha) = (1 - \alpha)M(\xi) + \alpha M(\eta)$. With $A = M(\xi)$ and $B = M(\eta)$, Lemma 2 gives the directional derivative

$$\frac{d}{d\alpha}\log\det M(\xi_\alpha)\Big|_{\alpha = 0} = \operatorname{tr}\bigl(M(\xi)^{-1}M(\eta)\bigr) - p = \sum_k v_k d(z_k, \xi) - p,$$

where $\eta$ has weights $v_k$ at points $z_k$. For the one-point design $\eta = \delta_x$ the derivative is $d(x, \xi) - p$.

**Lemma 3 (existence).** A D-optimal design exists, and its moment matrix is nonsingular.

*Proof.* The set $\mathcal M = \{M(\xi)\}$ is the [convex hull](/convex-hull/) of the compact set $S = \{f(x)f(x)^\top : x \in \mathcal X\}$ in the space of symmetric matrices, which has dimension $k = p(p+1)/2$. By [Carathéodory's theorem](/caratheodory-theorem/) every point of the hull is a convex combination of $k + 1$ points of $S$, so $\mathcal M$ is the image of the compact set $S^{k+1} \times \Delta_k$, with $\Delta_k$ the set of weight vectors of length $k + 1$, under a continuous map, and is compact. The [determinant](/determinant/) is continuous, so it attains its maximum on $\mathcal M$. The vectors $f(x)$ span $\mathbb R^p$: otherwise some $c \ne 0$ has $c^\top f(x) = 0$ for all $x$, which contradicts linear independence. Take $p$ points with independent $f(x_i)$ and equal weights; their moment matrix is nonsingular, so the maximum of $\det$ is positive. $\square$

**(1) implies (3).** Let $\xi^*$ be D-optimal and $x \in \mathcal X$. For $0 \le \alpha < 1$, $(1 - \alpha)\xi^* + \alpha\delta_x$ is a design, so $\log\det M$ along this segment is largest at $\alpha = 0$, and its derivative there is at most 0. That derivative is $d(x, \xi^*) - p$. So $d(x, \xi^*) \le p$ for every $x$, and by Lemma 1 the maximum is exactly $p$.

**(3) implies (1).** Let $\max_x d(x, \xi^*) = p$ and let $\eta$ be any design. If $M(\eta)$ is singular, $\det M(\eta) = 0 < \det M(\xi^*)$. Otherwise $\varphi(\alpha) = \log\det M\bigl((1 - \alpha)\xi^* + \alpha\eta\bigr)$ is concave on $[0, 1]$ by Lemma 2, so it lies below its tangent at 0:

$$\log\det M(\eta) = \varphi(1) \le \varphi(0) + \varphi'(0) = \log\det M(\xi^*) + \sum_k v_k d(z_k, \xi^*) - p \le \log\det M(\xi^*).$$

**(2) and (3) are equivalent.** By Lemma 3 a D-optimal design $\xi_D$ exists, and by (1) implies (3) it has $\max_x d(x, \xi_D) = p$. By Lemma 1, $\max_x d(x, \xi) \ge p$ for every design. So the smallest possible value of $\max_x d(x, \xi)$ is exactly $p$, and a design is G-optimal if and only if its maximum equals $p$, which is (3).

**The other claims.** If $\xi_1$ and $\xi_2$ are D-optimal with $M_1 \ne M_2$, the mixture with $\alpha = 1/2$ has, by strict concavity in Lemma 2, $\log\det M > \frac12\log\det M_1 + \frac12\log\det M_2 = \log\det M_1$, which contradicts optimality. So the optimal moment matrix $M^*$ is unique. Lemma 1 with (3) gives $d(x_i, \xi^*) = p$ at the support points.

For the support size, $M^*$ is on the boundary of $\mathcal M$: if it were an interior point, $M^* + \epsilon I$ would lie in $\mathcal M$ for small $\epsilon > 0$ and have a larger determinant. By the supporting hyperplane theorem there is a nonzero linear function $L$ on symmetric matrices with $L(M) \le L(M^*)$ for all $M \in \mathcal M$. If $M^* = \sum_i w_if(x_i)f(x_i)^\top$, then $L(M^*)$ is a weighted mean of the values $L(f(x_i)f(x_i)^\top) \le L(M^*)$, so all of them equal $L(M^*)$. So $M^*$ is in the convex hull of the points of $S$ in the hyperplane $\{L = L(M^*)\}$, whose dimension is $k - 1$. Carathéodory's theorem in this hyperplane writes $M^*$ as a convex combination of at most $k = p(p+1)/2$ points of $S$, and that combination is a D-optimal design. $\square$

## Consequences

**Two worked examples.** The theorem turns a guess into a proof.

- Straight line on $[-1, 1]$: $f(x) = (1, x)$, $p = 2$, and $\xi$ puts weight $1/2$ at $-1$ and at $1$. Then $M(\xi) = I$ and $d(x, \xi) = 1 + x^2 \le 2$, with equality exactly at $\pm 1$. So $\xi$ is D-optimal and G-optimal, with $\det M = 1$.
- Quadratic on $[-1, 1]$: $f(x) = (1, x, x^2)$, $p = 3$, and $\xi$ puts weight $1/3$ at $-1$, $0$ and $1$. Then

$$M(\xi) = \begin{pmatrix} 1 & 0 & 2/3 \\ 0 & 2/3 & 0 \\ 2/3 & 0 & 2/3 \end{pmatrix}, \qquad M(\xi)^{-1} = \begin{pmatrix} 3 & 0 & -3 \\ 0 & 3/2 & 0 \\ -3 & 0 & 9/2 \end{pmatrix},$$

and $d(x, \xi) = 3 - \frac92x^2 + \frac92x^4 = 3 - \frac92x^2(1 - x^2)$. This is at most 3 on $[-1, 1]$, equals 3 exactly at $-1$, $0$ and $1$, and has its smallest value $15/8$ at $x^2 = 1/2$. So $\xi$ is D-optimal with $\det M = 4/27$, and three support points, the fewest possible for $p = 3$.

**An efficiency bound.** For any design $\xi$ with nonsingular $M(\xi)$ and the optimal $M^*$,

$$\Bigl(\frac{\det M(\xi)}{\det M^*}\Bigr)^{1/p} \ge \frac{p}{\max_x d(x, \xi)}.$$

*Proof.* The eigenvalues $\lambda_j$ of $M(\xi)^{-1}M^*$ are positive, their product is $\det M^*/\det M(\xi)$, and their sum is $\operatorname{tr}(M(\xi)^{-1}M^*) = \sum_iw_i^*d(x_i^*, \xi) \le \max_xd(x, \xi)$. The inequality of arithmetic and geometric means gives $(\prod_j\lambda_j)^{1/p} \le \max_xd(x, \xi)/p$. $\square$ So one pass over $\mathcal X$ that computes $d$ gives a certificate of how far a design is from the optimum without knowing $M^*$. For the quadratic model, weights $1/4, 1/2, 1/4$ at $-1, 0, 1$ have D-efficiency $(27/32)^{1/3} \approx 0.945$ and $\max d = 4$, so the bound gives $0.75$; five equal weights at $-1, -\frac12, 0, \frac12, 1$ have D-efficiency $(189/320)^{1/3} \approx 0.839$ and $\max d = 31/7$, so the bound gives $21/31 \approx 0.677$.

**Algorithms.** The derivative $d(x, \xi) - p$ says which point to add. Adding weight at the point where $d$ is largest is the vertex direction method of Wynn (1970) and Fedorov (1972), the same update as [Khachiyan's algorithm](/khachiyans-algorithm/) for the [minimum volume enclosing ellipsoid](/minimum-volume-enclosing-ellipsoid/), whose dual is the D-optimal design problem over the points $f(x)$. For exact designs the [Fedorov exchange algorithm](/fedorov-exchange-algorithm/) swaps a point of low $d$ for a point of high $d$.

**General criteria.** The same proof works for any concave criterion $\Phi$ of $M$ with a directional derivative: $\xi^*$ maximizes $\Phi$ if and only if the derivative toward every one-point design is at most 0. This is the general equivalence theorem of Kiefer (1974). For A-optimality, $\Phi(M) = -\operatorname{tr}M^{-1}$, the condition is $f(x)^\top M^{-2}f(x) \le \operatorname{tr}M^{-1}$ for all $x$; for the quadratic model, the weights $1/4, 1/2, 1/4$ at $-1, 0, 1$ give $\operatorname{tr}M^{-1} = 8$ and $f(x)^\top M^{-2}f(x) = 8 - 20x^2(1 - x^2) \le 8$, so that design is A-optimal.

**Rotatable second-order designs.** In [response surface methodology](/response-surface-methodology/), the theorem explains why designs that spread runs over the corners, the axes and the center of the region predict well everywhere: G-optimality and D-optimality ask for the same thing.

## Tightness

- **Exact designs.** The theorem is about approximate designs. For $N$ runs, $N w_i$ must be integers, and then D-optimality and G-optimality can differ. Take the straight line, $N = 3$ runs, and the candidates $-1, -\frac34, \dots, 1$. An exhaustive check over all 165 multisets gives the D-optimal exact designs $\{-1, -1, 1\}$ and $\{-1, 1, 1\}$, with $\det X^\top X = 8$ and largest prediction variance $\sigma^2$, while the G-optimal exact design is $\{-1, 0, 1\}$, with $\det X^\top X = 6$ and largest prediction variance $\frac56\sigma^2$. For the empirical design $\xi$ of $N$ runs, $d(x, \xi) = N f(x)^\top(X^\top X)^{-1}f(x)$, and neither design reaches $\max_x d(x, \xi) = p = 2$: the values are 3 and 2.5.
- **Equal variances.** With error variance $\sigma^2/\lambda(x)$ the theorem holds after replacing $f(x)$ by $\sqrt{\lambda(x)}f(x)$. Without that change, a design that is D-optimal for the weighted model is not G-optimal for the unweighted prediction variance.
- **The bound $p(p+1)/2$.** It is the general Carathéodory count. It is not reached in the two examples, where $p$ points suffice, and for polynomial regression of degree $p - 1$ on an interval the D-optimal design has exactly $p$ support points. Fewer than $p$ points are never enough, since then $M$ has rank less than $p$.
- **Compactness and continuity.** Without them a D-optimal design need not exist. With $f(x) = (1, x)$ on the open interval $(-1, 1)$, every design has $\det M < 1$ while designs near $\pm 1$ come as close to 1 as wanted.
- **Partial interest.** If only $s < p$ linear combinations of $\theta$ matter, D-optimality for those $s$ combinations ($D_s$-optimality) and minimax variance of predictions differ in general, and the right-hand side $p$ becomes $s$ in the corresponding equivalence theorem.

## History

Kirstine Smith (1918) found designs that minimize the largest prediction variance for polynomial regression on an interval, an early G-optimal design. Kiefer (1959) set out the approximate theory, in which a design is a probability measure, and named the criteria by letters. Kiefer and Wolfowitz (1960) proved that the D-criterion and the G-criterion have the same optimal designs, with the value $p$. Wynn (1970) and Fedorov (1972) turned the derivative into algorithms. Atwood (1969) related the efficiencies, and Kiefer (1974) extended the equivalence to general concave criteria. Pukelsheim (1993) gives the modern account through moment matrices and duality.

## References
