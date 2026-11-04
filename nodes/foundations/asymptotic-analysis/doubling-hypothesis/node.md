---
tag: KVJZJ3
kind: technique
slug: doubling-hypothesis
name: Doubling hypothesis
aliases:
- doubling test
- doubling ratio
area: foundations/asymptotic-analysis
level: core
summary: Estimates the exponent of a power-law running time by comparing timings at input sizes n and 2n.
prereqs: [tilde-notation, order-of-growth, logarithms]
see_also: [empirical-analysis-of-algorithms, asymptotic-notation, common-growth-rates, comparing-growth-by-limits, stirling-approximation]
sources:
  - url: "https://algs4.cs.princeton.edu/14analysis/"
    locator: Section 1.4, Analysis of Algorithms (booksite, doubling ratio experiments)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 1.4, Analysis of Algorithms (the doubling ratio experiment and the power-law hypothesis)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 3, Characterizing Running Times (the difference between Theta and an exact leading term)
---

The doubling hypothesis is a technique that estimates the exponent $b$ in a running time $T(n) \sim a\,n^b$ from measurements. You run the program on inputs of size $n_0, 2n_0, 4n_0, \ldots$, and compute the ratio $T(2n)/T(n)$ at each size. If the hypothesis is right, the ratios tend to $2^b$, so $\lg(T(2n)/T(n))$ tends to $b$. Sedgewick and Wayne use it in Section 1.4 to predict the running time of a program on a larger input.

## In plain words

Suppose the running time of a program is about a constant times the input size raised to some power. Run the program on an input, then on one twice as large. If the second run takes twice as long, the power is 1. If it takes four times as long, the power is 2. If it takes eight times as long, the power is 3. In general, the power is how many times you must double 1 to reach the ratio, even a fractional number of times. A ratio of 2.8 means 1.5.

You can do this with a stopwatch. Double the input again and again, and watch the ratio of the times. When the ratio stops changing, you read the power from it. Then estimate the constant, and predict the time for an input too large to test. The ratios show when the simple form fails.

## When it applies

- The program has a running time or an operation count that you can measure at a series of sizes, each twice the previous one.
- You expect, or want to test, that the cost is $\sim a\,n^b$ for constants $a > 0$ and $b$, possibly with a logarithmic factor.
- You want a prediction for a larger size, or a check of a bound that you proved. Compare the measured exponent with the exponent of the proved bound.
- It does not apply to a cost that is exponential in $n$ or that jumps in steps: the ratios then do not settle.

## The template

**The hypothesis and its limit.** Assume $T(n) \sim a\,n^b$ with $a > 0$ and $b$ real, that is $T(n)/(a n^b) \to 1$ (see [tilde notation](/tilde-notation/)). Then
$$ \frac{T(2n)}{T(n)} \;\to\; 2^{b}, \qquad\text{so}\qquad \lg\frac{T(2n)}{T(n)} \to b. $$
*Proof.* Write the ratio as
$$ \frac{T(2n)}{T(n)} = \frac{T(2n)}{a(2n)^b}\cdot\frac{a\,n^b}{T(n)}\cdot\frac{a(2n)^b}{a\,n^b}. $$
The first factor tends to 1 because $T \sim a n^b$ at the point $2n$, the second tends to 1, and the third is $2^b$. $\square$

The hypothesis is about $\sim$, not about $\Theta$. If only $T(n) = \Theta(n^b)$ with $T > 0$, then for all large $n$ the ratio $T(2n)/T(n)$ stays between two positive constants, and it need not converge. For $T(n) = (2 + \sin n)\,n$ we have $T = \Theta(n)$, but the ratio does not settle at $2$.

**With a logarithmic factor.** If $T(n) \sim a\,n^b\lg n$, then $T(2n)/T(n) \to 2^b$, because $\lg(2n)/\lg n = 1 + 1/\lg n \to 1$. For the exact form $T(n) = a\,n^b\lg n$, the ratio is $2^b(1 + 1/\lg n)$, which is above $2^b$ and tends to it slowly. See the pitfalls.

**The steps.**

1. Fix a generator of inputs of size $n$. State what kind of input it makes: random, sorted, worst case.
2. Choose a start size $n_0$ that is large enough for the run to be measured well, and run sizes $n_0, 2n_0, 4n_0, \ldots$.
3. For each size, record $T(n)$. It can be seconds or a count of operations. A count is exact and has no noise.
4. For each $n = 2^i n_0$ with $i \ge 1$, compute the ratio $R(n) = T(n)/T(n/2)$ and $\lg R(n)$. Here the ratio is labeled by the larger size. Some examples below label it by the smaller size, as $T(2n)/T(n)$, and each of them says so.
5. Look for convergence. If $\lg R(n)$ settles near a value $b$, round it to a plausible exponent, and say how far the ratios are from the limit.
6. Estimate $a$ from the largest size: $a \approx T(N)/N^b$.
7. Predict: $T(n) \approx a\,n^b$ for a larger $n$. Check the prediction with one more run if you can.

The same steps as pseudocode, with the two holes `Generate` (makes an input of size $n$) and `Measure` (runs the program and returns a time or a count):

```
DoublingTest(Generate, Measure, n0, k):
    T[0] = Measure(Generate(n0))
    for i = 1 to k:
        n = n0 * 2^i
        T[i] = Measure(Generate(n))
        R[i] = T[i] / T[i-1]
        print n, R[i], lg R[i]
    b = lg R[k]    // then round b to a plausible exponent, such as 2 or 3/2
    a = T[k] / (n0 * 2^k)^b
    return b, a
```

## Classic examples

All the numbers below are exact counts, so there is no noise.

**Three nested loops.** A brute-force check of all triples of $n$ numbers, as in the simplest algorithm for [3SUM](/3sum/), visits $\binom n3 = n(n-1)(n-2)/6$ triples. The exact ratio is $\binom{2n}3 / \binom n3 = (8n-4)/(n-2)$, which is above 8 for each $n > 2$ and converges to 8:

| $n$ | $T(n) = \binom n3$ | $T(n)/T(n/2)$ | $\lg$ of the ratio |
| --- | --- | --- | --- |
| 250 | 2 573 000 | | |
| 500 | 20 708 500 | 8.048 | 3.0087 |
| 1000 | 166 167 000 | 8.024 | 3.0043 |
| 2000 | 1 331 334 000 | 8.012 | 3.0022 |
| 4000 | 10 658 668 000 | 8.006 | 3.0011 |
| 8000 | 85 301 336 000 | 8.003 | 3.0005 |

Round the exponent to $b = 3$. The constant is $a \approx T(8000)/8000^3 = 0.16660$, and the exact leading constant is $1/6 = 0.16667$. The prediction $a\,n^3$ for $n = 16\,000$ is $6.8241 \times 10^{11}$, and the exact count is $6.8254 \times 10^{11}$.

**[Selection sort](/selection-sort/).** The count of compares is $n(n-1)/2$. The ratio at $n = 1000$ (that is, $T(2000)/T(1000)$) is $4.002$, and at $n = 10^6$ it is $4.000002$. So $b = 2$ and $a = 1/2$.

**A logarithmic factor.** [Merge sort](/merge-sort/) on $n = 2^m$ keys makes $n\lg n - n + 1$ compares in the worst case. The ratio $T(2n)/T(n)$ and its binary logarithm are:

| $n$ | $T(2n)/T(n)$ | $\lg$ of the ratio |
| --- | --- | --- |
| $2^{8}$ | 2.285 | 1.192 |
| $2^{10}$ | 2.222 | 1.152 |
| $2^{16}$ | 2.133 | 1.093 |
| $2^{20}$ | 2.105 | 1.074 |
| $2^{30}$ | 2.069 | 1.049 |

The ratio tends to 2, so the limit exponent is $b = 1$, but at $n = 2^{20}$ it is still 5 percent above 2. An experimenter who stops at $n = 2^{20}$ and fits a power law gets $b \approx 1.07$. This is the effect of the factor $\lg n$. A factor $\lg n$ makes the fitted exponent a little above the true power of $n$, and the fitted exponent falls only slowly as $n$ grows. Lower-order terms can push the ratio either way: $5n^2 + 40n$ gives ratios below 4, and $\binom n3$ gives ratios above 8. Their effect fades like $1/n$, while the effect of $\lg n$ fades like $1/\lg n$. That slow decline is the signal of a logarithmic factor.

## Variations

**Other ratios.** Multiply the size by any factor $r > 1$. If $T \sim a n^b$ then $T(rn)/T(n) \to r^b$ and $b = \log_r$ of the limit. Doubling is common because the sizes are easy to generate and because $\lg$ is easy to compute.

**Log-log regression.** Plot $\lg T$ against $\lg n$ for all sizes. If $T \sim a n^b$, the points lie near a line of slope $b$ and intercept $\lg a$. A fit over all sizes uses all the data, but the small sizes, where the lower terms are large, bias it. So fit the line by least squares on the larger sizes only. See [empirical analysis of algorithms](/empirical-analysis-of-algorithms/).

**A model with a logarithm.** Test the form $T \sim a\,n^b\lg n$ by dividing: if $T(n)/(n^b\lg n)$ settles at a constant, the form fits. Compare it with the fit of the pure power law, and use the one that gives a constant ratio.

**Detecting exponential growth.** For $T(n) = c^n$ the ratio $T(2n)/T(n) = c^n$ grows without bound. A ratio that keeps growing at each doubling is a sign that the cost is not a power law.

## Pitfalls

- **A logarithmic factor looks like a larger exponent.** For $T \sim a n \lg n$ the ratio at $n = 1000$ is $2.2007$, which suggests $b = 1.14$, and at $n = 10^6$ it is $2.1003$ ($b = 1.07$). At $n = 10^9$ it is still $2.067$. If the exponent is close to an integer but a little above it, and it falls slowly, suspect a factor $\lg n$.
- **Small sizes.** The lower terms are large for small $n$. For $\binom n3$ the ratio at $n = 10$ (comparing 20 and 10) is $9.5$, which gives $\lg 9.5 = 3.25$. Start at a size where the ratio is already stable, and do not trust the first rows.
- **Caches and memory.** When the data no longer fits in a cache level, the time per operation jumps, and the ratio jumps above $2^b$ at that doubling. The running time then follows different constants on different ranges of $n$, so no single power law fits across the boundary. Use an operation count as well as a timing, see [empirical analysis of algorithms](/empirical-analysis-of-algorithms/).
- **Noise and the clock.** A run that takes a few milliseconds is dominated by timer resolution, the operating system and, in a managed language, JIT compilation and garbage collection. Make the smallest run last long enough, repeat each run, and take the median or the minimum.
- **Ratios converge slowly or not at all.** A ratio that has not converged is not an estimate of $2^b$. The sequence of ratios must settle before you round. If the cost oscillates, for example with the parity of $n$ or with powers of two, doubling may land on the same phase every time and hide the oscillation.
- **One kind of input.** The hypothesis is about the time on the input family that you generated. A random input gives the average case, and it can differ from the worst case, as with quicksort on sorted input.
- **A test is not a proof.** A finite series of ratios does not show that $T \sim a n^b$. It supports the hypothesis, and it can refute it. A bound proved from the algorithm is still needed.
- **$\Theta$ is not enough to predict.** A $\Theta(n^2)$ bound allows ratios anywhere between two constants. The prediction of a time at a larger size needs $\sim$ and the estimate of the constant $a$.

## Exercises

1. A program has $T(n) = 5n^2 + 40n$ steps. Compute $T(2n)/T(n)$ for $n = 10$, $100$ and $1000$.
2. Measurements give $T(1000) = 3.1$ s, $T(2000) = 6.4$ s and $T(4000) = 13.2$ s. Estimate $b$, then estimate the time at $n = 32\,000$ assuming $b = 1$.
3. For $T(n) = n\lg n$, find the least $n = 2^m$ for which $T(2n)/T(n) < 2.05$.
4. Show that $T(n) = 2^n$ has $T(2n)/T(n)$ unbounded, so no $b$ fits.
5. A count gives $T(n)/T(n/2) = 2.83$ at several doublings in a row. Estimate $b$ and name a plausible form of $T$.

<details>
<summary>Hints and answers</summary>

1. $T(10) = 900$, $T(20) = 2800$, ratio $3.111$. $T(100) = 54\,000$, $T(200) = 208\,000$, ratio $3.852$. $T(1000) = 5\,040\,000$, $T(2000) = 20\,080\,000$, ratio $3.984$. They tend to 4, so $b = 2$.
2. The ratios are $6.4/3.1 = 2.06$ and $13.2/6.4 = 2.06$. So $\lg 2.06 \approx 1.04$, and $b \approx 1$. With $b = 1$ and $a \approx 13.2/4000 = 0.0033$, the prediction for $n = 32\,000$ is about $105.6$ s. The data are made up for the exercise.
3. The ratio is $2(m+1)/m$, which is below $2.05$ when $m > 40$. So the least is $m = 41$, $n = 2^{41}$.
4. $T(2n)/T(n) = 2^{2n}/2^n = 2^n \to \infty$.
5. $\lg 2.83 = 1.501$, so $b = 3/2$ and $T(n) \sim a\,n^{3/2}$. A form such as $n\sqrt n$ is plausible, for example the cost of a loop over $n$ items with a scan of $\sqrt n$ items inside.

</details>

## References
