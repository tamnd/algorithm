---
tag: A1PFFF
kind: theorem
slug: abel-summation
name: Abel summation formula
aliases:
- summation by parts
- Abel's summation formula
area: sequences/prefix-sums-and-differences
level: advanced
summary: Writes sum a_k b_k as A(n)b(n) minus the sum of A(k)(b(k+1)-b(k)), where A is the prefix sum of a; the discrete integration-by-parts identity.
prereqs: [telescoping-sum, prefix-sums]
see_also: [discrete-antiderivative, finite-differences, indefinite-summation, euler-maclaurin-formula, harmonic-series, expected-value, range-update-range-query, prime-number-theorem]
sources:
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Section 2.6, Finite and infinite calculus (the rule of summation by parts, and its use on sums such as the sum of k 2^k and the sum of harmonic numbers)
  - book: isbn:9780387901633
    title: Tom M. Apostol, Introduction to Analytic Number Theory
    locator: Chapter 4, Theorem 4.2 (Abel's identity), and its use for the Chebyshev functions in the same chapter
  - paper: "N. H. Abel, Untersuchungen über die Reihe 1 + (m/1)x + (m(m-1)/(1.2))x^2 + ..., Journal für die reine und angewandte Mathematik 1, 1826, pages 311 to 339"
    locator: the lemma that bounds a sum of products by the largest partial sum times the first factor (Abel's inequality)
---

The Abel summation formula, also called summation by parts, rewrites a sum of products $\sum a_k b_k$ in terms of the [prefix sums](/prefix-sums/) $A_k = a_1 + \dots + a_k$ and the differences $b_{k+1} - b_k$. It is the discrete form of integration by parts, and its proof is one [telescoping sum](/telescoping-sum/). It turns a sum whose terms are hard to add into a sum whose terms are easy to add, it gives the convergence tests of Abel and Dirichlet, and its integral form, Abel's identity, is a basic tool of analytic number theory.

## Statement

Let $a_m, \dots, a_n$ and $b_m, \dots, b_n$ be numbers (real, complex, or elements of any commutative ring), with $m \le n$. Let $A_{m-1}, A_m, \dots, A_n$ be any sequence with $a_k = A_k - A_{k-1}$ for $m \le k \le n$. The usual choice is $A_{m-1} = 0$, so that $A_k = a_m + \dots + a_k$ is the prefix sum.

**Theorem (summation by parts).**

$$\sum_{k=m}^{n} a_k b_k = A_n b_n - A_{m-1} b_m - \sum_{k=m}^{n-1} A_k \,(b_{k+1} - b_k).$$

**Corollary (Abel's inequality).** If $b_m \ge b_{m+1} \ge \dots \ge b_n \ge 0$ and $|A_k| \le M$ for $m - 1 \le k \le n$, then

$$\Big|\sum_{k=m}^{n} a_k b_k\Big| \le 2 M b_m.$$

If also $A_{m-1} = 0$, the bound improves to $M b_m$.

**Theorem (Abel's identity, the integral form).** Let $a(1), a(2), \dots$ be numbers and let $A(t) = \sum_{1 \le k \le t} a(k)$ for real $t$, so $A(t) = 0$ when $t < 1$. Let $f$ have a continuous derivative on $[y, x]$, where $0 < y < x$. Then

$$\sum_{y < k \le x} a(k) f(k) = A(x) f(x) - A(y) f(y) - \int_y^x A(t) f'(t)\, dt.$$

This is Theorem 4.2 of Apostol.

## In plain words

Suppose you must add up many products, each made of a first factor and a second factor. Suppose the first factors are easy to add up in runs, and the second factors change slowly. Then you can trade the sum for a different one. Take the running totals of the first factors. Multiply each running total by how much the second factor changes at that point, and add these. Subtract this from the last running total times the last second factor.

The new sum is often much easier. If the second factor goes up by the same amount each time, the new sum has only running totals left. If the running totals stay small and the second factor shrinks steadily to zero, the new sum is small, and this is why some slowly shrinking sums with signs that change still add up to a finite number.

## Proof

**Summation by parts.** Replace each $a_k$ with $A_k - A_{k-1}$ and split the sum in two:

$$\sum_{k=m}^{n} a_k b_k = \sum_{k=m}^{n} A_k b_k - \sum_{k=m}^{n} A_{k-1} b_k = \sum_{k=m}^{n} A_k b_k - \sum_{k=m-1}^{n-1} A_k b_{k+1}.$$

The second step shifts the index of the second sum by one. Take the term $k = n$ out of the first sum and the term $k = m - 1$ out of the second sum. What is left in both sums runs over $m \le k \le n - 1$:

$$\sum_{k=m}^{n} a_k b_k = A_n b_n - A_{m-1} b_m + \sum_{k=m}^{n-1} A_k\,(b_k - b_{k+1}),$$

which is the theorem. $\square$

**Abel's inequality.** Apply the theorem. Since $b$ is nonincreasing, each $b_k - b_{k+1} \ge 0$, so

$$\Big|\sum_{k=m}^{n} a_k b_k\Big| \le M b_n + M b_m + M \sum_{k=m}^{n-1} (b_k - b_{k+1}) = M b_n + M b_m + M (b_m - b_n) = 2 M b_m.$$

The last sum telescopes. If $A_{m-1} = 0$, the term $M b_m$ for $A_{m-1} b_m$ is absent and the bound is $M b_n + M(b_m - b_n) = M b_m$. $\square$

**Abel's identity.** Let $p = \lfloor y \rfloor$ and $q = \lfloor x \rfloor$, so the integers $k$ with $y < k \le x$ are $p + 1, \dots, q$. The function $A$ is a step function: it is constant, equal to $A(k)$, on each interval $[k, k+1)$.

If $q = p$, the left side is $0$, and $A(t) = A(p)$ on all of $[y, x]$, so the right side is $A(p) f(x) - A(p) f(y) - A(p)\big(f(x) - f(y)\big) = 0$.

If $q \ge p + 1$, apply summation by parts with $m = p + 1$, $n = q$, $A_k = A(k)$ and $b_k = f(k)$:

$$\sum_{k=p+1}^{q} a(k) f(k) = A(q) f(q) - A(p) f(p+1) - \sum_{k=p+1}^{q-1} A(k) \big(f(k+1) - f(k)\big).$$

On $[k, k+1)$ the function $A$ equals $A(k)$, so $A(k)\big(f(k+1) - f(k)\big) = \int_k^{k+1} A(t) f'(t)\, dt$, and the last sum is $\int_{p+1}^{q} A(t) f'(t)\, dt$. In the same way, $A = A(q)$ on $[q, x]$ gives $A(q) f(q) = A(x) f(x) - \int_q^x A(t) f'(t)\, dt$, and $A = A(p)$ on $[y, p+1)$ gives $A(p) f(p+1) = A(y) f(y) + \int_y^{p+1} A(t) f'(t)\, dt$. Put the three parts in and join the three integrals into one over $[y, x]$. $\square$

## Consequences

**Closed forms for sums.** Take $a_k = 2^k$ and $b_k = k$ for $0 \le k \le n - 1$. Then $A_k = 2^{k+1} - 1$ and $b_{k+1} - b_k = 1$, so

$$\sum_{k=0}^{n-1} k\, 2^k = (n-1)(2^n - 1) - \sum_{k=0}^{n-2} (2^{k+1} - 1) = (n - 2)\, 2^n + 2.$$

For $n = 6$ both sides equal $258$. Take $a_k = 1$ and $b_k = H_k = 1 + 1/2 + \dots + 1/k$, the partial sums of the [harmonic series](/harmonic-series/). Then $A_k = k$ and $b_{k+1} - b_k = 1/(k+1)$, so

$$\sum_{k=1}^{n} H_k = n H_n - \sum_{k=1}^{n-1} \frac{k}{k+1} = (n + 1) H_n - n.$$

Concrete Mathematics, Section 2.6, does both sums this way in the language of [finite differences](/finite-differences/), where the rule reads $\sum u\, \Delta v = u v - \sum (E v)\, \Delta u$ and is the summation analogue of $\int u\, dv = uv - \int v\, du$.

**Weighted range sums from two prefix arrays.** With $b_k = k$ the formula gives $\sum_{k=1}^{n} k\, a_k = n A_n - \sum_{k=1}^{n-1} A_k$. So a sum weighted by the index needs only the prefix sums of $a$ and the prefix sums of those prefix sums. This is the identity behind the two-[Fenwick-tree](/fenwick-tree/) method for [range updates with range sums](/range-update-range-query/): there $a$ is the [difference array](/difference-array/) of the data, and the sum of a prefix of the data is $\sum_{k \le n} (n - k + 1)\, a_k$.

**Tail sums of expectations.** Let $X$ be a [random variable](/random-variable/) that takes values in $\{0, 1, \dots, n\}$. Take $a_k = \Pr[X = k]$ and $b_k = k$, and use the tails $T_k = \Pr[X \ge k]$ in place of prefix sums, with $a_k = T_k - T_{k+1}$. The same telescoping gives $\mathbb{E}[X] = \sum_{k=1}^{n} \Pr[X \ge k]$, a formula used often in the analysis of randomized algorithms; see [expected value](/expected-value/).

**Convergence tests.** If the partial sums of $\sum a_k$ are bounded and $b_k$ decreases to $0$, then Abel's inequality shows that the tails $\sum_{k=m}^{n} a_k b_k$ are at most $2 M b_m$, which tends to $0$, so $\sum a_k b_k$ converges. This is Dirichlet's test. With $a_k = (-1)^{k+1}$ it is the alternating series test, and with $a_k = \sin k$ it shows that $\sum (\sin k)/k$ converges. If instead $\sum a_k$ converges and $b_k$ is monotone and bounded, the same argument applied to the tails of $\sum a_k$ gives Abel's test.

**Analytic number theory.** Abel's identity with $a(k) = 1$ and $f(t) = 1/t$ gives $\sum_{k \le x} 1/k = \lfloor x \rfloor / x + \int_1^x \lfloor t \rfloor\, t^{-2}\, dt = \ln x + \gamma + O(1/x)$, where $\gamma$ is Euler's constant. With $a(p) = \ln p$ on primes $p$ and $f(t) = 1/\ln t$, it converts between the [prime-counting function](/prime-counting-function/) $\pi(x)$ and Chebyshev's function $\vartheta(x) = \sum_{p \le x} \ln p$, which is a standard step toward the [prime number theorem](/prime-number-theorem/). The [Euler-Maclaurin formula](/euler-maclaurin-formula/) can be seen as the same identity with $a(k) = 1$ pushed to more terms.

## Tightness

The identity is exact, so the questions of tightness are about the inequality and the hypotheses.

**The constant $2$ in Abel's inequality is the best.** Take $b$ constant, equal to $c > 0$, with $A_{m-1} = -M$, $a_m = 2M$ and $a_k = 0$ for $k > m$. Then $|A_k| \le M$ for all $k$, and $\sum_{k=m}^{n} a_k b_k = 2 M c = 2 M b_m$. In the same way, the bound $M b_m$ for $A_{m-1} = 0$ is reached by $a_m = M$ and $a_k = 0$ for $k > m$.

**Monotonicity is needed.** Dirichlet's test fails if $b_k \to 0$ but $b$ is not monotone. Take $a_k = (-1)^k$, whose partial sums are bounded by $1$, and $b_k = 1/k$ for even $k$ and $b_k = 0$ for odd $k$. Then $\sum a_k b_k = \sum_{j \ge 1} 1/(2j)$, which diverges. The proof breaks at the step that drops the absolute values from $b_k - b_{k+1}$.

**The boundary terms cannot be dropped.** For $a_k = 1$, $b_k = 1$ and $m = 1$, the left side is $n$, the sum of differences is $0$, and all of the value comes from $A_n b_n$.

**Smoothness in the integral form.** Abel's identity as stated needs $f'$ to exist and to be continuous, so that $f(k+1) - f(k) = \int_k^{k+1} f'$. In the language of Riemann-Stieltjes integrals the identity is integration by parts, $\int a\, df$ against the step function $A$, and it holds whenever $f$ has bounded variation and has no jump at the same point as $A$.

## History

Niels Henrik Abel used the identity in his 1826 paper on the binomial series in the first volume of Crelle's journal. There he proved the lemma now called Abel's inequality, and used it to prove that a power series that converges at a point of its circle of convergence is continuous there along the radius, the result now called Abel's theorem. Dirichlet used the same method for series with bounded partial sums, which gives the test that has his name. The integral form, with Stieltjes integrals or with a continuously differentiable $f$, became a standard tool of analytic number theory, where Apostol states it as Theorem 4.2. In the calculus of finite differences, summation by parts has been a basic rule since the eighteenth century, and Graham, Knuth and Patashnik give it as the partner of the rule that a sum of differences telescopes.

## References
