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
see_also: [asymptotic-equivalence, order-of-growth, doubling-hypothesis, stirling-approximation, logarithms]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.4, Analysis of Algorithms (tilde notation)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 3, Characterizing Running Times (O, Omega and Theta)
  - book: isbn:9780201558029
    title: Graham, Knuth and Patashnik, Concrete Mathematics, second edition
    locator: Chapter 9, Asymptotics
---

The tilde notation $f(n) \sim g(n)$ says that the ratio $f(n)/g(n)$ tends to 1 as $n$ grows. It keeps the leading term of a function together with its constant factor, and drops the lower terms. Sedgewick and Wayne use it for the cost of an algorithm, because it keeps the constant that [$\Theta$-notation](/asymptotic-notation/) throws away.

## In plain words

Suppose a program makes exactly 499500 compares on 1000 items, and the exact count is half of the number of items times one less than that number. Half the square of the number of items gives 500000, which is wrong by 0.1 percent. For a million items, the relative error is a thousand times smaller. So for large inputs you can say "about half the square of the input size", and you are right to within a tiny fraction.

Tilde notation is a short way to say this. It tells you the main term and its constant. Big-Theta would say only that the cost grows like the square of the size. That hides a factor of 2 between two algorithms that both have cost $\Theta(n^2)$. Tilde notation shows this factor, so you can compare them.

## The idea

### Definition

Let $f$ and $g$ be functions from the positive integers to the reals, with $g(n) \ne 0$ for all large $n$. Then
$$f(n) \sim g(n) \iff \lim_{n \to \infty} \frac{f(n)}{g(n)} = 1.$$
Equivalently, $f(n) = g(n) + o(g(n))$: the difference is small compared with $g$. The relation $\sim$ is an equivalence relation on such functions (see [asymptotic equivalence](/asymptotic-equivalence/)). In particular, it is symmetric and transitive.

### Difference from $\Theta$

If $f \sim g$ and $g$ is positive for all large $n$, as a cost function is, then $f = \Theta(g)$. Proof: the ratio tends to 1, so there is $n_0$ with $g(n) > 0$ and $1/2 \le f(n)/g(n) \le 2$ for all $n \ge n_0$. Multiply by $g(n)$: $g(n)/2 \le f(n) \le 2g(n)$, which gives both bounds.

The converse is false. We have $2n^2 = \Theta(n^2)$, but $2n^2 \not\sim n^2$, because the ratio tends to 2. The relation $f \sim g$ fixes the constant. The relation $f = \Theta(g)$ allows any constant, and it also allows $f/g$ not to converge at all: $(2 + \sin n)\, n$ is $\Theta(n)$ but is $\sim c\,n$ for no $c$.

If $f(n) \sim a\, n^b$ for constants $a > 0$ and $b$, then the ratio $f(2n)/f(n)$ tends to $2^b$, which is what the [doubling hypothesis](/doubling-hypothesis/) measures. The tilde form also gives $a$. A $\Theta$ bound gives neither.

### Rules

If $f_1 \sim g_1$ and $f_2 \sim g_2$, then $f_1 f_2 \sim g_1 g_2$ and $f_1 / f_2 \sim g_1 / g_2$ (when $f_2, g_2$ are non-zero for large $n$), because limits of ratios multiply. If $f_1, f_2, g_1, g_2$ are all non-negative, then $f_1 + f_2 \sim g_1 + g_2$. Proof: let $r_i = f_i/g_i$. Then $(f_1+f_2)/(g_1+g_2) = (g_1 r_1 + g_2 r_2)/(g_1+g_2)$, a weighted mean of $r_1$ and $r_2$ with non-negative weights. It lies between $\min(r_1,r_2)$ and $\max(r_1,r_2)$, and both tend to 1.

These rules do not extend to subtraction. Take $f = n^2 + 2n$, $g = n^2 + n$ and $h = n^2$. Then $f \sim g$, but $f - h = 2n$ and $g - h = n$, so the ratio of the differences tends to 2 and $f - h \not\sim g - h$.

Logarithms keep the relation in one direction. If $f \sim g$, $g$ is positive and $g(n) \to \infty$, then $\ln f \sim \ln g$, because $\ln f = \ln g + \ln(f/g) = \ln g + o(1)$. The converse is false: $\ln 2^{n+1} \sim \ln 2^n$, but $2^{n+1} \not\sim 2^n$.

### What $\sim$ does not tell you

The tilde keeps the ratio, not the difference. $n^2/2 - n/2 \sim n^2/2$, but the difference between them is $n/2$, which grows. Also, $\sim$ is sensitive to the base of a logarithm, unlike $\Theta$: $\lg n \sim \ln n / \ln 2$, and $\lg n \not\sim \ln n$. And $2^{n+1} \not\sim 2^n$, since the ratio is 2. Convergence of the ratio can also be slow, so a tilde form can be a poor guide for moderate $n$ (see the examples).

## Examples

Each exact count below was checked by computer.

- **Selection sort.** On $n$ items, [selection sort](/selection-sort/) makes exactly $n(n-1)/2$ compares, for every input. So $C(n) \sim n^2/2$. For $n = 1000$ the exact count is 499500 and $n^2/2 = 500000$. For $n = 10^6$, the ratio is $0.999999$.
- **Merge sort.** For top-down [merge sort](/merge-sort/) with the recurrence $C(n) = C(\lceil n/2 \rceil) + C(\lfloor n/2 \rfloor) + n - 1$ (the merge makes at most $n - 1$ compares), the worst-case count is $n \lceil \lg n \rceil - 2^{\lceil \lg n \rceil} + 1$. For $n = 1000$ this is 8977, and for $n = 10^6$ it is 18951425. The leading term gives $C(n) \sim n \lg n$. The ratio $C(n) / (n \lg n)$ is 0.90 at $n = 10^3$ and 0.95 at $n = 10^6$: it tends to 1, but slowly, because the lower term $-\Theta(n)$ is only a $1/\lg n$ fraction of the leading term. The word "worst case" and the recurrence matter: a different merge or a different split gives a different count.
- **Quicksort.** [Quicksort](/quicksort/) with a uniformly random pivot makes $2(n+1)H_n - 4n$ compares in expectation, where $H_n$ is the $n$th [harmonic number](/harmonic-series/) and $H_n \sim \ln n$. So the expected count is $\sim 2 n \ln n \approx 1.386\, n \lg n$. The ratio of the exact count to $2n \ln n$ is 0.85 at $n = 10^4$ and 0.90 at $n = 10^6$.
- **Binary search.** On a sorted array of $n$ items, [binary search](/binary-search/) makes at most $\lfloor \lg n \rfloor + 1$ probes, which is $\sim \lg n$.
- **Stirling's formula.** $n! \sim \sqrt{2\pi n}\,(n/e)^n$ (see [Stirling's approximation](/stirling-approximation/)). Here the tilde keeps a constant that $\Theta$ cannot state. The weaker statement $\ln n! \sim n \ln n$ is also true, and it is enough for the sorting lower bound.
- **Not an example.** $T(n) = 3n^2 + n \lg n$ has $T(n) \sim 3n^2$, but $T(n) \not\sim n^2$. Both are $\Theta(n^2)$.

## Where it is used

- **Comparing two algorithms of the same order.** Selection sort ($\sim n^2/2$ compares) and [insertion sort](/insertion-sort/) on random input (about $n^2/4$ compares) are both $\Theta(n^2)$, but the tilde form shows a factor of 2 in compares. Merge sort and quicksort are both $\Theta(n \log n)$, and the tilde form shows that random-pivot quicksort makes about 39 percent more compares on average than merge sort makes in the worst case.
- **Predicting running time.** If the cost is $\sim a\,n^b$, then $a$ can be measured from a timing at one size, and the time at a larger size can be predicted. See the [doubling hypothesis](/doubling-hypothesis/) and [order of growth](/order-of-growth/).
- **Use $\Theta$ instead** when the constant depends on the machine, the language or the cost of one step, or when you want only the shape of the growth. Use $\sim$ when the quantity is a count of an exact operation, such as compares or array accesses, that does not depend on the machine.

## References
