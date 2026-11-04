---
tag: 94GGN6
kind: concept
slug: tilde-notation
name: Tilde notation
aliases:
- ~ notation
- leading-term approximation
area: foundations/asymptotic-analysis
level: core
summary: Writes f(n) ~ g(n) to mean f(n)/g(n) tends to 1, giving the leading term of an exact cost.
prereqs: [asymptotic-notation]
see_also: [asymptotic-equivalence, order-of-growth, doubling-hypothesis, stirling-approximation, logarithms, comparing-growth-by-limits]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.4, Analysis of Algorithms (tilde approximations and order of growth)
  - book: isbn:9780321905758
    title: Robert Sedgewick and Philippe Flajolet, An Introduction to the Analysis of Algorithms, second edition
    locator: Chapter 4, Asymptotic Approximations
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Chapter 9, Asymptotics
---

The tilde notation $f(n) \sim g(n)$ says that the ratio $f(n)/g(n)$ tends to 1 as $n$ grows. It keeps the leading term of a cost function together with its constant factor, and it drops the lower-order terms. Sedgewick and Wayne use it to state the cost of an algorithm, because it keeps the constant that [$\Theta$-notation](/asymptotic-notation/) throws away. As a mathematical relation it is [asymptotic equivalence](/asymptotic-equivalence/).

## In plain words

Suppose a program makes exactly 499500 comparisons on 1000 items, and the exact count is half of the number of items times one less than that number. Half the square of the number of items is 500000, which is wrong by only 0.1 percent. For a million items, the relative error is a thousand times smaller. So for large inputs you can say "about half the square of the input size", and you are right to within a fraction that shrinks to nothing.

Tilde notation is a short way to say this. It keeps the main term and its constant. Big-Theta keeps only the shape of the growth. It cannot see a factor of 2 between two algorithms that both grow like the square of the input size. Tilde notation shows this factor, so you can compare such algorithms and predict running times.

## The idea

### Definition

Let $f$ and $g$ be real functions on the positive integers, with $g(n) \ne 0$ for all large $n$. Then
$$f(n) \sim g(n) \iff \lim_{n \to \infty} \frac{f(n)}{g(n)} = 1.$$
Equivalently, $f(n) = g(n)\,(1 + \delta(n))$ with $\delta(n) \to 0$, or $f(n) = g(n) + o(g(n))$: the error is small compared with $g$, not small in absolute terms. In cost analysis $g$ is a simple function, usually $a\,n^b (\lg n)^c$, and $f$ is an exact count. The relation is an equivalence relation: it is reflexive, symmetric and transitive. The proofs are on the page of [asymptotic equivalence](/asymptotic-equivalence/).

### How to find the tilde form

Write the exact cost as a sum of terms, find the term $t(n)$ that every other term is $o$ of, and drop the others. This is correct by the following rule. If $f = t + e_1 + \cdots + e_k$ with $k$ fixed and $e_i = o(t)$ for each $i$, then $f/t = 1 + \sum_i e_i/t \to 1$, so $f \sim t$. For example, $n^2/2 - n/2 \sim n^2/2$, because $(n/2)/(n^2/2) = 1/n \to 0$. A polynomial with leading coefficient $a_k \ne 0$ is $\sim a_k n^k$.

When the exact cost is not known, two-sided bounds can still give the tilde form. If $\ell(n) \le f(n) \le u(n)$ and $\ell \sim u \sim t$ with $t > 0$, then $\ell/t \le f/t \le u/t$, and both outer ratios tend to 1. So $f \sim t$ by the squeeze rule.

### Difference from $\Theta$

If $f \sim g$ and $g$ is positive for all large $n$, as a cost function is, then $f = \Theta(g)$. *Proof.* The ratio tends to 1, so there is $n_0$ with $g(n) > 0$ and $\frac12 \le f(n)/g(n) \le 2$ for all $n \ge n_0$. Multiply by $g(n)$: $g(n)/2 \le f(n) \le 2g(n)$, which gives both bounds with $c = \frac12$ and $c = 2$. $\square$

The converse is false. We have $2n^2 = \Theta(n^2)$, but $2n^2 \not\sim n^2$, because the ratio tends to 2. The relation $f \sim g$ fixes the constant. The relation $f = \Theta(g)$ allows any constant, and it also allows $f/g$ to oscillate: $(2 + \sin n)\, n$ is $\Theta(n)$, but it is $\sim c\,n$ for no constant $c$, because the ratio $(2 + \sin n)/c$ has no limit.

If $f(n) \sim a\, n^b$ for constants $a > 0$ and $b$, then
$$\frac{f(2n)}{f(n)} = \frac{f(2n)}{a (2n)^b}\cdot\frac{a\,n^b}{f(n)}\cdot 2^b \to 2^b.$$
This is the ratio that the [doubling hypothesis](/doubling-hypothesis/) measures. A bound $f = \Theta(n^b)$ alone does not give this: for $f(n) = (2 + \sin n)\,n$ the ratio $f(2n)/f(n)$ has no limit.

### Rules

Let $f_1 \sim g_1$ and $f_2 \sim g_2$, with $g_1, g_2$ non-zero for all large $n$, and let $r_i = f_i/g_i$, so $r_i \to 1$.

- **Products and quotients.** $f_1 f_2 \sim g_1 g_2$, because the ratio is $r_1 r_2 \to 1$. Also $f_1/f_2 \sim g_1/g_2$, because $f_2 \ne 0$ for large $n$ (as $r_2 \to 1$) and the ratio is $r_1/r_2 \to 1$.
- **Sums of non-negative terms.** If $g_1, g_2 \ge 0$ for large $n$, then $f_1 + f_2 \sim g_1 + g_2$. *Proof.* Given $\varepsilon > 0$, for large $n$ we have $|f_i - g_i| \le \varepsilon\,g_i$ for $i = 1, 2$. Add the two inequalities: $|(f_1 + f_2) - (g_1 + g_2)| \le \varepsilon\,(g_1 + g_2)$. $\square$
- **Logarithms.** If $f \sim g$, $g > 0$ for large $n$ and $g(n) \to \infty$, then $\ln f \sim \ln g$, because $\ln f = \ln g + \ln(f/g) = \ln g + o(1)$ and $\ln g \to \infty$.
- **Substitution.** If $f \sim g$ and $h(n) \to \infty$ is integer-valued, then $f(h(n)) \sim g(h(n))$. For example, $f \sim a\,n^b$ gives $f(2n) \sim a\,2^b n^b$.

### What does not hold

- **Differences.** Take $f = n^2 + 2n$, $g = n^2 + n$ and $h = n^2$. Then $f \sim g$, but $f - h = 2n$ and $g - h = n$, so $f - h \not\sim g - h$. Never cancel leading terms between two tilde forms and keep the rest: the rest is exactly what $\sim$ throws away.
- **Sums with mixed signs.** $n^2 + n \sim n^2$ and $-n^2 \sim -n^2$, but the sums are $n$ and $0$.
- **Exponentials.** $n + 1 \sim n$, but $2^{n+1} = 2 \cdot 2^n \not\sim 2^n$. The converse of the logarithm rule fails for the same reason: $\ln 2^{n+1} \sim \ln 2^n$.
- **Absolute error.** $n^2/2 - n/2 \sim n^2/2$, but the difference $n/2$ grows without bound. The tilde controls the ratio only.
- **The base of a logarithm.** Inside $\Theta$ the base does not matter, but inside $\sim$ it does: $\lg n = \ln n/\ln 2$, so $\lg n \sim 1.4427\ln n$ and $\lg n \not\sim \ln n$.

### Pitfalls

- **Treating a tilde form as accurate at a given size.** The ratio tends to 1, but it may do so slowly. A lower-order term of relative size $1/\lg n$ is still 5 percent at $n = 10^6$, as the merge sort example below shows.
- **Reading $\sim$ as $\Theta$ or the reverse.** A tilde form needs the limit of the ratio. A proof that gives only $c_1 g \le f \le c_2 g$ with $c_1 < c_2$ proves $\Theta$, not $\sim$.
- **Counting the wrong operation.** A tilde form of a count of comparisons says nothing about the time of a step. It predicts time only when the counted operation dominates the time and costs about the same each time.
- **A tilde form without its case.** "$\sim n^2/2$ compares" for selection sort holds on every input, but "$\sim n^2/4$ compares" for insertion sort holds on average over random permutations only. State the case, as for any bound.

## Examples

**Selection sort.** On $n$ items, [selection sort](/selection-sort/) makes exactly $n(n-1)/2$ comparisons, on every input. So $C(n) \sim n^2/2$. For $n = 1000$ the exact count is $499\,500$ against $n^2/2 = 500\,000$, and for $n = 10^6$ the ratio is $0.999999$.

**Insertion sort on random input.** Let [insertion sort](/insertion-sort/) compare the key with each element that it passes, and stop at the left end without a comparison. On a uniformly random permutation of $n$ distinct keys, the key in position $i$ (for $i = 2, \ldots, n$) passes $(i-1)/2$ larger elements on average, and it makes one more comparison unless it is the smallest of the first $i$, which has probability $1/i$. By [linearity of expectation](/linearity-of-expectation/) the expected count is
$$\sum_{i=2}^{n}\left(\frac{i-1}{2} + 1 - \frac1i\right) = \frac{n(n-1)}{4} + n - H_n \sim \frac{n^2}{4},$$
where $H_n$ is the $n$-th [harmonic number](/harmonic-series/). The formula matches an exhaustive count over all permutations for $n \le 7$. For $n = 1000$ it gives $250\,742.5$, which is $1.003$ times $n^2/4$. Both sorts are $\Theta(n^2)$, and the tilde forms show the factor of 2 between them.

**Merge sort.** Top-down [merge sort](/merge-sort/) makes at most $C(n) = n c - 2^c + 1$ comparisons in the worst case, where $c = \lceil \lg n \rceil$. We show $n\lg n - n + 1 \le C(n) \le n\lg n$ for each $n \ge 1$, so $C(n) \sim n\lg n$ by the squeeze rule. *Proof.* For $n = 1$ all three are 0. For $n \ge 2$ write $n = 2^c\theta$ with $\frac12 < \theta \le 1$, so $c - \lg n = -\lg\theta$ and $2^c = n/\theta$. Then $C(n) - (n\lg n - n + 1) = n\,h(\theta)$ with $h(\theta) = 1 - \lg\theta - 1/\theta$. We have $h(\frac12) = h(1) = 0$ and $h''(\theta) = \theta^{-2}(1/\ln 2 - 2/\theta) < 0$ on $(\frac12, 1]$, so $h$ is concave and $h \ge 0$ there. This is the lower bound. Also $C(n) - n\lg n = n\,(h(\theta) - 1) + 1$. The maximum of $h$ is at $\theta = \ln 2$, where $h = 0.0861\ldots$, so $C(n) - n\lg n \le -0.913\,n + 1 < 0$. $\square$ The convergence is slow: $C(n)/(n\lg n)$ is $0.753$ at $n = 10$, $0.901$ at $n = 1000$ and $0.951$ at $n = 10^6$, where $C(n) = 18\,951\,425$.

**Quicksort.** [Quicksort](/quicksort/) with a uniformly random pivot, where partitioning $m$ keys costs $m - 1$ comparisons, makes $2(n+1)H_n - 4n$ comparisons in expectation (see [expected running time of quicksort](/quicksort-expected-running-time/)). Since $H_n \sim \ln n$, the products and sums rules give $2(n+1)H_n \sim 2n\ln n$, and $4n = o(n\ln n)$, so the expected count is $\sim 2n\ln n = (2\ln 2)\,n\lg n \approx 1.386\,n\lg n$. The ratio of the exact count to $2n\ln n$ is $0.795$ at $n = 10^3$, $0.846$ at $n = 10^4$ and $0.897$ at $n = 10^6$.

**Stirling's formula.** $n! \sim \sqrt{2\pi n}\,(n/e)^n$ (see [Stirling's approximation](/stirling-approximation/)). Here the tilde keeps the constant $\sqrt{2\pi}$. A $\Theta$ statement would keep only the shape $\sqrt n\,(n/e)^n$. By the logarithm rule, $\ln n! \sim n\ln n$, which is enough for the sorting lower bound.

**Non-example.** $T(n) = 3n^2 + n\lg n$ has $T(n) \sim 3n^2$, but $T(n) \not\sim n^2$, although both statements $T = \Theta(n^2)$ and $3n^2 = \Theta(n^2)$ are true. The ratio $T(n)/(3n^2)$ is $1.111$ at $n = 10$ and $1.003$ at $n = 1000$.

## Where it is used

- **Comparing algorithms of the same order.** Selection sort ($\sim n^2/2$ comparisons on every input) and insertion sort ($\sim n^2/4$ on average) differ by a factor of 2. Quicksort with a random pivot ($\sim 1.386\,n\lg n$ on average) and merge sort ($\le n\lg n$ in the worst case) differ by about 39 percent in the limit. At $n = 10^6$ the ratio of the two exact formulas is only $1.31$, because the lower-order terms differ.
- **Predicting running time.** If the time is $\sim a\,n^b$, measure the time at two sizes to estimate $b$ and $a$, and predict the time at a larger size. This is the [doubling hypothesis](/doubling-hypothesis/), and it needs the tilde form, not only a $\Theta$ bound.
- **Exact analysis.** Counts of comparisons, exchanges and array accesses are stated with their leading constant. The [order of growth](/order-of-growth/) is the coarser class that remains when the constant is dropped.
- **Use $\Theta$ instead** when the constant depends on the machine, the language or the cost of one step, or when only the shape of the growth matters. Use $\sim$ when the quantity is an exact count of an operation that does not depend on the machine.

## References
