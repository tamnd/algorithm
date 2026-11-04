---
tag: 2N4TKH
kind: theorem
slug: markov-inequality
name: Markov's inequality
aliases:
- Markov inequality
area: foundations/probabilistic-analysis
level: intro
summary: For a nonnegative random variable X and a > 0, P(X >= a) <= E[X]/a; the first tail bound, and the base of Chebyshev and Chernoff.
prereqs: [random-variable, expected-value, indicator-random-variable]
see_also: [chebyshev-inequality, chernoff-bound, union-bound, high-probability-bounds, las-vegas-algorithm, monte-carlo-algorithm, moment-generating-function, concentration-of-measure]
sources:
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: Chapter 3, Moments and Deviations, Section 3.1, Markov's Inequality
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms, Cambridge University Press, 1995
    locator: Section 3.2, The Markov and Chebyshev Inequalities (Theorem 3.2, and Exercises 3.2 and 3.3 on tightness and the form with a function h); Section 1.2, Las Vegas and Monte Carlo
  - book: isbn:9780521884273
    title: Devdatt P. Dubhashi and Alessandro Panconesi, Concentration of Measure for the Analysis of Randomized Algorithms, Cambridge University Press, 2009
    locator: Chapter 1, Chernoff-Hoeffding Bounds, Section 1.3, The Chernoff Bound (Markov's inequality applied to an exponential)
  - url: "https://en.wikipedia.org/wiki/Markov%27s_inequality"
    locator: lead section (the name, and the earlier appearance in the work of Chebyshev)
---

Markov's inequality says that a [random variable](/random-variable/) $X$ that is never negative satisfies $\Pr(X \ge a) \le \mathbb{E}[X]/a$ for each $a > 0$. It needs only the [expected value](/expected-value/), so it applies to almost anything, and it is the weakest of the standard tail bounds. Applied to $(X - \mathbb{E}X)^2$ it gives [Chebyshev's inequality](/chebyshev-inequality/), and applied to $e^{sX}$ it gives the [Chernoff bound](/chernoff-bound/). In the analysis of algorithms it turns a bound on the expected running time into a bound on the probability of a long run, which converts a [Las Vegas algorithm](/las-vegas-algorithm/) into a [Monte Carlo algorithm](/monte-carlo-algorithm/).

## Statement

**Theorem (Markov).** Let $X$ be a random variable with $X \ge 0$ (with probability 1), and let $a > 0$. Then
$$ \Pr(X \ge a) \le \frac{\mathbb{E}[X]}{a}. $$
If $\mathbb{E}[X] = \infty$ the bound says nothing, and it holds trivially. When $0 < \mathbb{E}[X] < \infty$, the substitution $a = t\,\mathbb{E}[X]$ gives the equivalent form $\Pr(X \ge t\,\mathbb{E}[X]) \le 1/t$ for each $t > 0$.

**Corollary (Markov with a function).** Let $X$ be any real random variable, let $f : \mathbb{R} \to [0, \infty)$ be nondecreasing, and let $a$ be a real number with $f(a) > 0$. Then
$$ \Pr(X \ge a) \le \frac{\mathbb{E}[f(X)]}{f(a)}. $$
Here $X$ may take negative values. Only $f$ must be nonnegative.

**Corollary (reverse Markov).** Let $X \le b$ with probability 1, and let $a < b$. Then
$$ \Pr(X > a) \ge \frac{\mathbb{E}[X] - a}{b - a}. $$

**Equality.** For $0 < \mathbb{E}[X] < \infty$, equality holds in the theorem exactly when $X \in \{0, a\}$ with probability 1. For each $\mu$ with $0 < \mu \le a$ there is such an $X$ with $\mathbb{E}[X] = \mu$, so no bound that uses only the mean and nonnegativity can be smaller.

## In plain words

Suppose the average salary in a company is one thousand. Then at most half of the staff can earn two thousand or more, because those people alone would already push the average to one thousand. At most a tenth can earn ten thousand or more. Nobody can earn less than nothing, and that is the only fact the argument needs besides the average.

For algorithms, the salary is the running time of a randomized program. If the program takes one second on average, then the chance that it takes ten seconds or more is at most one in ten. The bound is crude: for most programs the true chance is far smaller. But it needs no knowledge of how the time is spread out, so you can always use it, and stronger bounds are built on top of it.

## Proof

**The theorem.** Let $I$ be the [indicator random variable](/indicator-random-variable/) of the event $\{X \ge a\}$: $I = 1$ when $X \ge a$ and $I = 0$ otherwise.

1. *Pointwise inequality.* We show $a I \le X$ for each outcome. If $X \ge a$, then $aI = a \le X$. If $X < a$, then $aI = 0 \le X$, by the hypothesis $X \ge 0$. This is the only place where the hypothesis is used.
2. *Take expectations.* Expectation is monotone: $Y \le Z$ pointwise implies $\mathbb{E}[Y] \le \mathbb{E}[Z]$ when both exist (for nonnegative variables, with the value $\infty$ allowed). So $a\,\mathbb{E}[I] \le \mathbb{E}[X]$.
3. *Read off the probability.* $\mathbb{E}[I] = \Pr(X \ge a)$. Divide by $a > 0$. $\square$

**Markov with a function.** Since $f$ is nondecreasing, $X \ge a$ implies $f(X) \ge f(a)$. So $\{X \ge a\} \subseteq \{f(X) \ge f(a)\}$. The variable $f(X)$ is nonnegative and $f(a) > 0$, so the theorem applied to $f(X)$ and the level $f(a)$ gives
$$ \Pr(X \ge a) \le \Pr(f(X) \ge f(a)) \le \frac{\mathbb{E}[f(X)]}{f(a)}. \qquad \square $$

**Reverse Markov.** The variable $Y = b - X$ is nonnegative by the hypothesis $X \le b$, and $b - a > 0$. The theorem gives $\Pr(X \le a) = \Pr(Y \ge b - a) \le (b - \mathbb{E}[X])/(b - a)$. Take complements: $\Pr(X > a) \ge 1 - (b - \mathbb{E}[X])/(b - a) = (\mathbb{E}[X] - a)/(b - a)$. $\square$

**Equality.** Let $0 < \mathbb{E}[X] < \infty$. By step 2, equality holds exactly when $\mathbb{E}[X - aI] = 0$. The variable $X - aI$ is nonnegative by step 1, and a nonnegative variable has mean 0 exactly when it is 0 with probability 1. So equality holds exactly when $X = aI$ with probability 1, that is, when $X$ takes only the values 0 and $a$. Given $0 < \mu \le a$, the variable with $\Pr(X = a) = \mu/a$ and $\Pr(X = 0) = 1 - \mu/a$ has mean $\mu$ and $\Pr(X \ge a) = \mu/a$. $\square$

## Consequences

**Chebyshev and Chernoff.** With $f(x) = x^2$ applied to $|X - \mathbb{E}X|$, the corollary gives $\Pr(|X - \mathbb{E}X| \ge a) \le \mathrm{Var}(X)/a^2$, which is [Chebyshev's inequality](/chebyshev-inequality/). With $f(x) = e^{sx}$ for $s > 0$ it gives $\Pr(X \ge a) \le e^{-sa}\,\mathbb{E}[e^{sX}]$ for each $s > 0$. Minimizing over $s$ is the [moment generating function](/moment-generating-function/) method behind the [Chernoff bound](/chernoff-bound/) and the [Hoeffding inequality](/hoeffding-inequality/). With $f(x) = |x|^k$ it gives the moment bound $\Pr(|X| \ge a) \le \mathbb{E}|X|^k / a^k$. Each of these bounds is Markov's inequality applied to a better variable.

**From Las Vegas to Monte Carlo.** Let $A$ be a [Las Vegas algorithm](/las-vegas-algorithm/): its answer is always correct, and on each input $I$ its running time $T$ is random with $\mathbb{E}[T] \le \tau(I)$. Build algorithm $B$: run $A$ for at most $c\,\tau(I)$ steps, for a constant $c > 1$; if $A$ has not stopped, stop it and output "fail". Then $B$ always runs in at most $c\,\tau(I)$ steps, and by Markov's inequality applied to $T \ge 0$,
$$ \Pr(B \text{ fails}) = \Pr(T > c\,\tau(I)) \le \Pr(T \ge c\,\tau(I)) \le \frac{1}{c}. $$
So $B$ is a [Monte Carlo algorithm](/monte-carlo-algorithm/) whose only error is a detected "fail". If $B$ restarts $A$ up to $k$ times with fresh random bits, the runs are independent, and all $k$ fail with probability at most $c^{-k}$. For a total budget of $\beta\,\tau(I)$ steps, $k = \beta/c$ runs give the failure bound $c^{-\beta/c} = \exp(-\beta\,(\ln c)/c)$. The function $(\ln c)/c$ is largest at $c = e$, where it is $1/e = 0.3679$, against $0.3466$ at $c = 2$ and at $c = 4$. With the budget $\beta = 20$:

| time limit per run | runs | bound on the failure probability |
| --- | --- | --- |
| $2\tau$ | 10 | $2^{-10} = 0.000977$ |
| $4\tau$ | 5 | $4^{-5} = 0.000977$ |
| $10\tau$ | 2 | $10^{-2} = 0.01$ |
| $20\tau$ | 1 | $0.05$ |

Many short runs beat one long run, because Markov's bound for a single run falls only like $1/c$, while independent restarts multiply. The Markov bound needs no knowledge of the distribution of $T$. The trade between expected bounds and bounds that hold [with high probability](/high-probability-bounds/) is the subject of that page.

**Averaging arguments.** The reverse form turns a mean into a fraction. Suppose a randomized test is correct with probability at least 0.9 on average over its random seeds, so that the success probability $X$ of a random seed is in $[0, 1]$ with $\mathbb{E}[X] \ge 0.9$. Then $\Pr(X > 0.8) \ge (0.9 - 0.8)/(1 - 0.8) = 0.5$: at least half of the seeds succeed with probability above 0.8.

**How it compares with the truth.** The table shows two variables with mean 2 and mean 50. The first is the number of fair coin flips up to and including the first head, a [geometric](/geometric-distribution/) variable with $\Pr(T \ge a) = 2^{-(a-1)}$. The second is the number of heads in 100 fair flips, a [binomial](/binomial-distribution/) variable, with its exact tail sum.

| variable | $a$ | Markov bound $\mathbb{E}[X]/a$ | exact $\Pr(X \ge a)$ |
| --- | --- | --- | --- |
| geometric, mean 2 | 4 | 0.5 | 0.125 |
| geometric, mean 2 | 8 | 0.25 | 0.0078 |
| geometric, mean 2 | 32 | 0.0625 | $4.66 \times 10^{-10}$ |
| binomial, $n = 100$, mean 50 | 60 | 0.833 | 0.0284 |
| binomial, $n = 100$, mean 50 | 75 | 0.667 | $2.82 \times 10^{-7}$ |
| binomial, $n = 100$, mean 50 | 100 | 0.5 | $7.89 \times 10^{-31}$ |

The bound falls like $1/a$, and the true tails fall exponentially. For the binomial, Markov cannot even say that 100 heads in 100 flips is unlikely. Chebyshev uses the variance and gives $0.04$ for $\Pr(X \ge 75)$ (see [Chebyshev's inequality](/chebyshev-inequality/)), and Chernoff uses independence and gives an exponentially small bound (see [binomial tail bounds](/binomial-tail-bounds/)).

## Tightness

Markov's inequality is the best possible bound from the two facts it uses. For each $a > 0$ and each mean $\mu$ with $0 < \mu \le a$, the two-point variable with $\Pr(X = a) = \mu/a$ and $\Pr(X = 0) = 1 - \mu/a$ attains it, as proved above. For $\mu > a$ the bound exceeds 1, and the best true statement is $\Pr(X \ge a) \le 1$, attained by the constant $X = \mu$. The extremal variable puts all its mass at 0 and at $a$, which is unusual for the running time of an algorithm. This is why the bound is weak in practice.

The strict form is never attained with a positive mean. If $0 < \mathbb{E}[X] < \infty$, then $\Pr(X > a) < \mathbb{E}[X]/a$. Proof: $a\,1[X > a] \le X$ pointwise, with strict inequality on $\{X > a\}$ and on $\{0 < X \le a\}$. One of these two sets has positive probability, because $\mathbb{E}[X] > 0$. So the expectations differ.

### Pitfalls

- **The variable must be nonnegative.** Let $X = -1$ or $X = 1$ with probability $\frac12$ each. Then $\mathbb{E}[X] = 0$ but $\Pr(X \ge 1) = \frac12$. If $X \ge m$ for a known constant $m$, apply the theorem to $X - m$: $\Pr(X \ge a) \le (\mathbb{E}[X] - m)/(a - m)$ for $a > m$.
- **Only one tail.** Markov bounds the upper tail. It says nothing about $\Pr(X \le a)$ for $a$ below the mean. For that you need an upper bound $b$ on $X$ and the reverse form above, or information about the variance.
- **A bound at or below the mean is empty.** For $a \le \mathbb{E}[X]$ the bound is at least 1.
- **The function must be nondecreasing.** The corollary $\Pr(X \ge a) \le \mathbb{E}[f(X)]/f(a)$ can fail for $f(x) = x^2$, which decreases on the negative numbers: for $X = 0$ and $a = -1$ the left side is 1 and the right side is 0. Apply $f(x) = x^2$ to the nonnegative variable $|X - \mu|$, as in Chebyshev's inequality.
- **Expected time does not give a high-probability time.** From $\mathbb{E}[T] = \tau$ alone, the best statement is $\Pr(T \ge c\tau) \le 1/c$. To get a failure probability of $1/n$ this way you need the limit $n\tau$. Restarts with a limit of $2\tau$ give $1/n$ after $\lceil \lg n \rceil$ runs, at a total cost of $2\tau\lceil \lg n \rceil$, but only because the runs are independent.
- **Restarts need fresh randomness.** The bound $c^{-k}$ for $k$ restarts multiplies probabilities, so it needs the runs to be independent. A restart that reuses the same random seed repeats the same run.

## History

The inequality is named after Andrey Markov. It appeared earlier in the work of his teacher Pafnuty Chebyshev, and many texts in analysis call it Chebyshev's inequality. In the analysis of randomized algorithms it is the first tool of Motwani and Raghavan, Chapter 3, and of Mitzenmacher and Upfal, Chapter 3, where it serves as the base for the bounds of Chebyshev and Chernoff.

## References
