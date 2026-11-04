---
tag: S90GJ0
kind: theorem
slug: continuous-master-theorem
name: Continuous master theorem
aliases:
- Roura's continuous master theorem
area: foundations/recurrences
level: advanced
summary: A master theorem of Roura for full-history recurrences F(n) = t(n) + sum of w(n,k) F(k), whose weights follow a shape function, with exact leading constants.
prereqs: [master-theorem, recurrence-relation, quicksort-expected-running-time, tilde-notation, asymptotic-notation]
see_also: [akra-bazzi-theorem, divide-and-conquer-recurrence, quicksort, quickselect, point-quadtree, iteration-method, harmonic-series]
sources:
  - paper: doi:10.1145/375827.375837
    title: Salvador Roura, Improved master theorems for divide-and-conquer recurrences, Journal of the ACM 48(2), 170 to 205 (2001)
    locator: Section 3 (Definitions 3.1 and 3.2, Theorem 3.3), Section 7 (proof), Appendix B (examples)
  - book: isbn:9780321905758
    title: Robert Sedgewick and Philippe Flajolet, An Introduction to the Analysis of Algorithms, second edition
    locator: Chapter 1 (the analysis of quicksort) and Chapter 2, Recurrence Relations
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Section 2.2, Sums and Recurrences (the quicksort recurrence and summation factors)
---

The continuous master theorem of Roura gives the asymptotic solution, with its leading constant, of a full-history recurrence $F_n = t_n + \sum_{0 \le k < n} \omega_{n,k} F_k$ whose weights $\omega_{n,k}$ approach a continuous profile $\omega(z)$, called the shape function, as $n$ grows. Such recurrences arise when an algorithm splits its input at a random point, as quicksort, quickselect and searches in random trees do, so the sizes of the subproblems are not fixed. Like the [master theorem](/master-theorem/), it compares the toll function $t_n$ with a power $n^\alpha$ fixed by the weights, and it has three cases; unlike it, the answers are of the form $F_n \sim C\, t_n$ with an explicit $C$ in two of them.

## Statement

The statement is Theorem 3.3 of Roura (2001), with Definitions 3.1 and 3.2 of the same paper.

**Shape function.** A function $\omega : [0, 1] \to [0, \infty)$ is a *shape function* if $\int_0^1 \omega(z)\,dz$ exists and is at least 1, and there is some $\mu < 0$ such that $\int_0^1 \omega(z) z^\mu\,dz$ converges.

**Continuous recursive definition.** Let $N \ge 1$ be an integer, and let

$$F_n = b_n \quad (0 \le n < N), \qquad F_n = t_n + \sum_{0 \le k < n} \omega_{n,k} F_k \quad (n \ge N).$$

This is a *continuous recursive definition* of $F_n$ if there are a shape function $\omega$, a constant $0 < q \le 1$ and an integer-valued $M_n = \Theta(n^q)$ with the following property. Cut $[0, n)$ into the $M_n$ intervals $I_{n,j} = [\frac{j}{M_n} n, \frac{j+1}{M_n} n)$, and let

$$\varepsilon_{n,j} = \Bigg| \sum_{k \in I_{n,j}} \omega_{n,k} - \int_{j/M_n}^{(j+1)/M_n} \omega(z)\,dz \Bigg|.$$

Then $\sum_{0 \le j < M_n} \varepsilon_{n,j} = O(n^{-\rho})$ for some $\rho > 0$. Usually $M_n = n$ works, and then $\varepsilon_{n,k} = \big|\omega_{n,k} - \int_{k/n}^{(k+1)/n} \omega(z)\,dz\big|$.

**Theorem (Roura).** Let $F_n$ have a continuous recursive definition with shape function $\omega$, and let $t_n \sim B n^a (\ln n)^c\, \xi_n$, where $B > 0$, $a$ and $c$ are constants, and $\xi_n$ is either $\mu_n$ or $1/\mu_n$ for some *sublogarithmic* function $\mu_n$ (positive and non-decreasing for large $n$, with $(\log n)^\epsilon / \mu_n$ increasing for large $n$, for each $\epsilon > 0$). Let

$$\varphi(x) = \int_0^1 \omega(z) z^x\,dz, \qquad \mathcal H = 1 - \varphi(a).$$

1. If $\mathcal H > 0$, then $F_n \sim t_n/\mathcal H$.
2. If $\mathcal H = 0$:
   - if $c > -1$, then $F_n \sim t_n \ln n/\mathcal H'$, where $\mathcal H' = -(c + 1)\int_0^1 \omega(z) z^a \ln z\,dz$;
   - if $c = -1$, then $F_n = O(n^a \log^\epsilon n)$ for each $\epsilon > 0$, and $F_n = \Omega(n^a)$ if $F_n \ge 0$ for each $n$; if moreover $\mu_n = 1$, then $F_n \sim t_n \ln n \ln\ln n/\mathcal H''$, where $\mathcal H'' = -\int_0^1 \omega(z) z^a \ln z\,dz$;
   - if $c < -1$, then $F_n = O(n^a)$, and $F_n = \Theta(n^a)$ if $F_n \ge 0$ for each $n$.
3. If $\mathcal H < 0$ (including $\mathcal H = -\infty$), then $F_n = O(n^\alpha)$, and $F_n = \Theta(n^\alpha)$ if $F_n \ge 0$ for each $n$, where $\alpha$ is the unique solution of $\varphi(\alpha) = 1$.

The function $\varphi$ is strictly decreasing where it is finite, and $\varphi(0) = \int_0^1 \omega \ge 1$, so $\alpha \ge 0$ exists and is unique. The value $\alpha$ plays the role of $\log_b a$ in the master theorem: $\mathcal H > 0$ means $a > \alpha$ (the toll function dominates), $\mathcal H = 0$ means $a = \alpha$ (all levels tie), and $\mathcal H < 0$ means $a < \alpha$ (the leaves dominate). The case numbers are Roura's; his case 1 is case 3 of CLRS and the other way round.

CLRS, fourth edition, uses the name continuous master theorem for the real-valued form of the ordinary [master theorem](/master-theorem/). That theorem is a different result.

## In plain words

Some algorithms split their input at a random place. Quicksort is the classic one: the pivot can land anywhere, so a part can be tiny or almost the whole input. The cost of such an algorithm is an average over all the possible splits, and its formula mentions the costs of all smaller inputs at once.

The theorem says that only two things matter in the long run: how much work one call does by itself, and the overall profile of how the work of the calls spreads over the smaller sizes. From the profile you compute one critical rate of growth. If the work per call grows faster than this rate, the top call dominates, and the theorem even gives the constant factor. If it grows slower, the many small calls dominate. If the two rates match, an extra logarithmic factor appears.

## Proof

Roura's proof (Section 7 of his paper, with Sections 4 and 5) is long. Its structure is below, followed by a complete proof for the uniform shape function $\omega(z) = 2$, the shape of quicksort, where all three cases can be seen exactly.

### Where the constants come from

Suppose $F_k \approx C k^a$ and $t_n = B n^a$. The sum of the weights over an interval of $k$ approximates the integral of $\omega$, so

$$\sum_{k<n} \omega_{n,k} F_k \approx C n^a \sum_{k<n} \omega_{n,k} \left(\frac kn\right)^a \approx C n^a \int_0^1 \omega(z) z^a\,dz = C\varphi(a)\, n^a.$$

The recurrence then reads $C n^a \approx B n^a + C\varphi(a) n^a$, so $C = B/(1 - \varphi(a)) = B/\mathcal H$. This makes sense only if $\mathcal H > 0$, which is case 1. If $\mathcal H = 0$, the guess cancels, and the next guess $F_k \approx C k^a \ln k$ leaves the term $C n^a \int_0^1 \omega(z) z^a \ln z\,dz$, which gives $C = B/\mathcal H'$ when $c = 0$. If $\mathcal H < 0$, the guess $C k^\alpha$ with $\varphi(\alpha) = 1$ satisfies the homogeneous recurrence approximately, and the toll is too small to change the order.

### Structure of Roura's proof

1. **Canonical form.** Divide by $n^\alpha$: the function $C_n = F_n/n^\alpha$ satisfies a recurrence with weights $\omega_{n,k}(k/n)^\alpha$, whose shape function $\omega(z) z^\alpha$ has integral $\varphi(\alpha) = 1$. Roura calls a recurrence whose total weight tends to 1, at the rate $O(n^{-\rho})$, *canonical*.
2. **Core theorems (Section 4).** A canonical recurrence with non-negative base values and positive toll is $\Omega(1)$, and it is $O(1)$ when its toll is small enough. After the division by $n^\alpha$, these are the bounds of case 3.
3. **Flesh theorems (Section 5).** These treat canonical recurrences with larger tolls and give asymptotic equivalences for them.
4. **Assembly (Sections 6 and 7).** For the continuous case, Section 7 shows that $\varphi$ is continuous and strictly decreasing, that the canonical form is again a continuous recursive definition, and combines the core and flesh theorems into the cases of the theorem.

The error terms $\varepsilon_{n,j}$ control how far the discrete weights are from the shape function, and the hypothesis $\sum_j \varepsilon_{n,j} = O(n^{-\rho})$ makes their total effect a lower-order term. Roura also states, as an open problem (Conjecture 7.1), whether the condition on $\int \omega(z) z^\mu\,dz$ for some $\mu < 0$ follows from the convergence of $\int \omega$; it holds when $\omega$ is bounded near 0, with any $\mu \in (-1, 0)$.

### A complete proof for the uniform shape

Let $F_0$ be given, $F_n = t_n + \frac{2}{n}\sum_{k<n} F_k$ for $n \ge 1$, and $t_n = n^a$ with $a > -1$. Here $\omega_{n,k} = 2/n = \int_{k/n}^{(k+1)/n} 2\,dz$, so $\varepsilon_{n,k} = 0$, $\omega(z) = 2$, and $\varphi(x) = 2/(x + 1)$ for $x > -1$. Then $\varphi(\alpha) = 1$ gives $\alpha = 1$.

*Reduction to first order.* Multiply the recurrence by $n$, write it for $n - 1$, and subtract. With $d_n = n t_n - (n-1) t_{n-1}$ (and $d_1 = t_1$):

$$nF_n = (n+1)F_{n-1} + d_n \quad (n \ge 1).$$

Divide by $n(n + 1)$; the sum [telescopes](/telescoping-sum/), as in the [iteration method](/iteration-method/):

$$F_n = (n+1)\Big(F_0 + \sum_{k=1}^{n}\frac{d_k}{k(k+1)}\Big).$$

By the mean value theorem, $d_k = k^{a+1} - (k-1)^{a+1} = (a+1)\eta^a$ for some $\eta \in (k - 1, k)$, so $d_k = (a+1) k^a (1 + O(1/k))$ for $k \ge 2$, and $d_k/(k(k+1)) = (a+1)k^{a-2}(1 + O(1/k))$.

- **$a > 1$ (case 1).** The sum is $\sim (a+1) n^{a-1}/(a-1)$, so $F_n \sim \frac{a+1}{a-1} n^a$. The theorem gives $\mathcal H = 1 - \frac{2}{a+1} = \frac{a-1}{a+1}$ and $t_n/\mathcal H = \frac{a+1}{a-1} n^a$, the same.
- **$a = 1$ (case 2, $c = 0$).** $d_k = 2k - 1$, the sum is $2\ln n + O(1)$, and $F_n \sim 2n\ln n$. The theorem gives $\mathcal H' = -\int_0^1 2z\ln z\,dz = \frac12$ and $t_n \ln n/\mathcal H' = 2n\ln n$.
- **$-1 < a < 1$ (case 3).** The terms are $O(k^{a-2})$, a convergent series, so $F_n = (n + 1)(L + o(1))$ with $L = F_0 + \sum_{k \ge 1} d_k/(k(k+1))$, and $F_n = O(n) = O(n^\alpha)$. If $a \ge 0$ and $F_0 \ge 0$, each $d_k > 0$, so $L \ge d_1/2 = \frac12$ and $F_n = \Theta(n)$.

This proves the theorem for $\omega = 2$ and $t_n = n^a$. $\blacksquare$

## Consequences

### Quicksort

The expected number of comparisons $Q_n = n + 1 + \frac2n\sum_{k<n} Q_k$, $Q_0 = 0$, has $\omega(z) = 2$, $a = 1$, $c = 0$, so $\mathcal H = 1 - \varphi(1) = 0$ and $\mathcal H' = \frac12$. The theorem gives $Q_n \sim 2n\ln n \approx 1.386\, n\lg n$. The exact solution is $Q_n = 2(n+1)H_n - 2n$, with $H_n$ the [harmonic number](/harmonic-series/); see [quicksort expected running time](/quicksort-expected-running-time/). Convergence of the ratio is slow: $Q_n/(2n\ln n)$ is about $0.940$ at $n = 10^3$ and $0.974$ at $n = 10^7$, because the second term of $Q_n$ is of order $n$.

### Quickselect

The expected number of comparisons to select an element of random rank with [quickselect](/quickselect/) satisfies $S_n = n + 1 + \frac{2}{n^2}\sum_{k<n} k S_k$, Roura's example (9). Here $\int_{k/n}^{(k+1)/n} 2z\,dz = \frac{2k}{n^2} + \frac{1}{n^2}$, so $\omega(z) = 2z$ with $\varepsilon_{n,k} = 1/n^2$ and $\sum_k \varepsilon_{n,k} = 1/n$. Then $\varphi(x) = 2/(x + 2)$, $\mathcal H = 1 - \varphi(1) = \frac13 > 0$, and $S_n \sim 3n$. The ratio $S_n/n$ is $2.977$ at $n = 10^3$ and $2.9998$ at $n = 2 \cdot 10^5$.

### Partial match in a random quadtree

Roura's example (5) is $Q_n = 1 + \frac{4}{n(n+1)}\sum_{k<n}(n - k)Q_k$, $Q_0 = 0$, for a partial-match search in a random [point quadtree](/point-quadtree/). Its shape function is $\omega(z) = 4(1 - z)$, with $\int_0^1 \omega = 2$, and $\varphi(x) = 4\big(\frac{1}{x+1} - \frac{1}{x+2}\big)$. Here $a = 0$ and $\mathcal H = 1 - \varphi(0) = -1 < 0$, so $Q_n = \Theta(n^\alpha)$ with $\varphi(\alpha) = 1$, that is $\alpha^2 + 3\alpha - 2 = 0$ and $\alpha = (\sqrt{17} - 3)/2 \approx 0.56155$. The ratio $Q_n/n^\alpha$ is about $1.575$ at $n = 10^3$ and $1.594$ at $n = 2 \cdot 10^5$. The theorem gives the order, not the constant, in this case.

### Grouped weights

The weights need not fit $\omega$ one by one. For $F_n = n + \frac4n \sum_{k<n,\ k \text{ even}} F_k$, each single weight is $4/n$ or 0, while $\int_{k/n}^{(k+1)/n} 2\,dz = 2/n$, so with $M_n = n$ the errors add up to about 2, which is not $O(n^{-\rho})$. With $M_n = \lfloor\sqrt n\rfloor$ groups, each group of about $\sqrt n$ consecutive $k$ has weight within $O(1/n)$ of the integral, and the errors add up to $O(n^{-1/2})$. So $\omega(z) = 2$, $\mathcal H = 0$, $\mathcal H' = \frac12$, and $F_n \sim 2n\ln n$, as for quicksort. Numerically, $F_n/n - 2\ln n$ tends to about $-3.23$.

## Tightness

- **Fixed split sizes are not covered.** For $F_n = t_n + F_{\lfloor n/2 \rfloor}$, all the weight of the sum sits on one $k$. No integrable $\omega$ has a mass of 1 on an interval of length tending to 0, so this is not a continuous recursive definition. Roura's Discrete Master Theorem (his Theorem 2.3) handles it, with $\varphi$ replaced by a finite sum $\sum_d w_d z_d^x$.
- **Fewer than one call.** The definition asks for $\int_0^1 \omega \ge 1$. With $\int_0^1 \omega < 1$, as in $F_n = n + \frac1{2n}\sum_{k<n} F_k$, there is no $\alpha \ge 0$ with $\varphi(\alpha) = 1$, and the theorem does not apply.
- **The $c = -1$ case is weaker.** In case 2 with $c = -1$ and a sublogarithmic factor, the theorem gives only $O(n^a \log^\epsilon n)$ and $\Omega(n^a)$, not an equivalence.
- **Case 3 has no constant.** When $\mathcal H < 0$, the leading constant depends on all values of $F_k$, the small ones included, as for the quadtree example, and the theorem gives only $\Theta(n^\alpha)$. Roura gives an example, with fixed split sizes, of a recurrence of order $\Theta(1)$ whose values fluctuate periodically and do not converge.
- **Sign conditions.** The $\Theta$ and $\Omega$ conclusions need $F_n \ge 0$. The $O$ conclusions hold without it.

## History

Roura introduced the theorem and its name in his 2001 paper in the Journal of the ACM, together with a Discrete Master Theorem for recurrences whose subproblems have fixed fractions of the size, with floors and ceilings allowed. Both theorems give exact leading constants. The quicksort recurrence itself had been solved exactly long before, by reduction to a first-order recurrence, as in Concrete Mathematics, Section 2.2, and Sedgewick and Flajolet. The theorem gives the leading term of such recurrences without an exact solution, and it applies when no exact solution is known, as for the partial-match search in quadtrees.

## References
