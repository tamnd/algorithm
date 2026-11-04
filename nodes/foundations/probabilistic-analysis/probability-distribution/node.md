---
tag: 6ESRF5
kind: definition
slug: probability-distribution
name: Probability distribution
area: foundations/probabilistic-analysis
level: intro
summary: A function assigning probabilities to the events of a sample space, satisfying nonnegativity, total probability one, and additivity for disjoint events.
prereqs: [probability-space]
see_also: [discrete-probability-distribution, probability-density-function, random-variable, uniform-distribution, binomial-distribution, geometric-distribution, poisson-distribution, total-variation-distance]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix C, Section C.2 (probability axioms, discrete and continuous uniform distributions) and Section C.3 (the probability density function of a random variable)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Section 1.2, Axioms of Probability, and Section 8.1.1, Probability Distributions in R
  - book: isbn:9780471257080
    title: William Feller, An Introduction to Probability Theory and Its Applications, Volume I, third edition
    locator: Chapter IX, Random Variables; Expectation (distributions of random variables)
---

A probability distribution is a function that gives a probability to each event of a sample space and satisfies the three axioms of a [probability space](/probability-space/): nonnegativity, total probability one, and additivity for disjoint events. The term has two common uses. CLRS calls the probability measure $\Pr$ of the space itself a probability distribution. The distribution of a [random variable](/random-variable/) $X$ is the measure $B \mapsto \Pr(X \in B)$ that $X$ carries to the real line, and it is the object that statements such as "$X$ is [binomial](/binomial-distribution/)" describe.

## Definition

**On a sample space.** Let $\Omega$ be a sample space with a $\sigma$-algebra $\mathcal{F}$ of events. A probability distribution on $\Omega$ is a function $\Pr : \mathcal{F} \to \mathbb{R}$ such that $\Pr(A) \ge 0$ for each event $A$, $\Pr(\Omega) = 1$, and $\Pr(\bigcup_i A_i) = \sum_i \Pr(A_i)$ for each finite or countable family of pairwise disjoint events. This is the same object as the probability measure of a [probability space](/probability-space/). CLRS states the axioms for a finite or countable $\Omega$ and pairwise disjoint events.

**Of a random variable.** Let $X$ be a real [random variable](/random-variable/) on $(\Omega, \mathcal{F}, \Pr)$. Its **distribution**, or **law**, is the function

$$P_X(B) = \Pr(X \in B) = \Pr(\{\omega \in \Omega : X(\omega) \in B\})$$

for each Borel set $B \subseteq \mathbb{R}$ (the Borel sets are the smallest $\sigma$-algebra that holds all intervals). $P_X$ is a probability distribution on $\mathbb{R}$. Proof: $P_X(B) \ge 0$ because it is a probability. $P_X(\mathbb{R}) = \Pr(\Omega) = 1$ because $X$ takes a real value at each outcome. If $B_1, B_2, \ldots$ are pairwise disjoint, then the sets $\{X \in B_i\}$ are pairwise disjoint (an outcome cannot map into two disjoint sets), and their union is $\{X \in \bigcup_i B_i\}$, so countable additivity of $\Pr$ gives countable additivity of $P_X$.

Two random variables $X$ and $Y$ are **equal in distribution**, written $X \overset{d}{=} Y$, when $P_X = P_Y$. They can live on different spaces.

**Cumulative distribution function.** The CDF of $X$ is $F_X(x) = \Pr(X \le x)$ for $x \in \mathbb{R}$. It has four properties:

1. $F_X$ is nondecreasing: for $x < y$, $\{X \le x\} \subseteq \{X \le y\}$, so monotonicity of $\Pr$ gives $F_X(x) \le F_X(y)$.
2. $\lim_{x \to -\infty} F_X(x) = 0$: the events $\{X \le -n\}$ decrease to $\emptyset$ as $n \to \infty$, so continuity of $\Pr$ gives $\Pr(X \le -n) \to 0$, and monotonicity extends this to all $x \to -\infty$.
3. $\lim_{x \to \infty} F_X(x) = 1$: the events $\{X \le n\}$ increase to $\Omega$, so $\Pr(X \le n) \to 1$.
4. $F_X$ is right-continuous: for $x_n \downarrow x$, the events $\{X \le x_n\}$ decrease to $\{X \le x\}$, so $F_X(x_n) \to F_X(x)$.

From these, for $a < b$: $\Pr(a < X \le b) = F_X(b) - F_X(a)$, because $\{X \le a\} \subseteq \{X \le b\}$. Also $\Pr(X = x) = F_X(x) - F_X(x^-)$, where $F_X(x^-)$ is the limit from the left: the events $\{x - 1/n < X \le x\}$ decrease to $\{X = x\}$. So $F_X$ jumps exactly at the values that $X$ takes with positive probability. A CDF fixes the whole distribution: two random variables with the same CDF are equal in distribution. For a discrete $X$ this follows from the jump formula, which gives each $\Pr(X = x)$. In general it is a standard result of measure theory, and this page uses it without proof.

**Kinds of distribution.**

- **Discrete:** there is a finite or countable set $S$ with $\Pr(X \in S) = 1$. Then $F_X$ is a step function. See [discrete probability distribution](/discrete-probability-distribution/).
- **Continuous with a density:** there is a function $f \ge 0$ with $F_X(x) = \int_{-\infty}^x f(t)\,dt$ for all $x$. Then $F_X$ is continuous and $\Pr(X = x) = 0$ for each $x$. See [probability density function](/probability-density-function/).
- **Neither:** a mix of the two, or a continuous $F_X$ with no density.

## Examples and non-examples

**Comparisons of randomized quicksort.** Let $C$ be the number of key comparisons that [randomized quicksort](/randomized-quicksort/) makes on 4 distinct keys. The pivot choices give

| $c$ | 4 | 5 | 6 |
|---|---|---|---|
| $\Pr(C = c)$ | $1/2$ | $1/6$ | $1/3$ |
| $F_C(c)$ | $1/2$ | $2/3$ | $1$ |

A middle key as the first pivot (probability $1/2$) leaves subarrays of sizes 1 and 2, so $C = 3 + 1 = 4$. An end key as the first pivot leaves a subarray of size 3, which costs 2 or 3 more comparisons with probabilities $1/3$ and $2/3$, so $\Pr(C = 5) = \frac12 \cdot \frac13 = \frac16$ and $\Pr(C = 6) = \frac12 \cdot \frac23 = \frac13$. The distribution is the same for each input order of the 4 keys. Its mean is $29/6 \approx 4.83$, the value $2(n+1)H_n - 4n$ at $n = 4$ (see [expected value](/expected-value/)). The CDF is $0$ for $x < 4$, steps up at 4, 5 and 6, and is 1 from 6 on.

**The same law on two spaces.** The number of heads in two flips of a fair coin, and the number of keys out of 2 that hash to bucket 0 in a table with 2 buckets, both have the distribution $\Pr(0) = 1/4$, $\Pr(1) = 1/2$, $\Pr(2) = 1/4$. They are equal in distribution, although they are functions on different spaces.

**A mixed distribution from a retry timer.** A client sends a request and waits. With probability $0.9$ the reply comes at a time that is uniform on $[0, 1]$ milliseconds. With probability $0.1$ the request is lost, and the client gives up at the timeout of exactly 5 milliseconds. The wait $W$ has $F_W(x) = 0.9x$ on $[0, 1]$, $F_W(x) = 0.9$ on $[1, 5)$, and $F_W(x) = 1$ for $x \ge 5$. It is neither discrete (it has no countable support of full measure) nor continuous (it has an atom of $0.1$ at 5).

**Non-example: a function that is not right-continuous.** $G(x) = 0$ for $x \le 0$ and $G(x) = 1$ for $x > 0$ is nondecreasing with the right limits, but $G(0) = 0 \ne 1 = \lim_{x \downarrow 0} G(x)$. It is not the CDF of any random variable. The CDF of the constant 0 is $1$ at $x = 0$.

**Non-example: a function that is not additive.** On the subsets of $\{1, 2\}$, set $\mu(\emptyset) = 0$, $\mu(\{1\}) = \mu(\{2\}) = 0.6$, $\mu(\{1, 2\}) = 1$. It is nonnegative with total 1, but $\mu(\{1\}) + \mu(\{2\}) = 1.2 \ne 1$, so it is not a probability distribution.

### Pitfalls

- **The distributions of $X$ and $Y$ do not fix the distribution of $X + Y$.** Let $X$ be a fair bit. If $Y = X$, then $X + Y \in \{0, 2\}$ with probabilities $1/2$ each. If $Y$ is an independent fair bit, then $X + Y$ is 0, 1, 2 with probabilities $1/4$, $1/2$, $1/4$. In both cases $X$ and $Y$ have the same distributions. You need the joint distribution, or [independence](/independent-random-variables/), to find the law of a sum. [Linearity of expectation](/linearity-of-expectation/) is the exception: $\mathbb{E}[X + Y]$ needs only the two laws.
- **Equal in distribution is not equal.** If $X$ is a fair bit, then $1 - X$ has the same law, but $X \ne 1 - X$ at every outcome.
- **"Random" without a distribution means nothing.** "A random input" for [average-case analysis](/average-case-analysis/) must name a distribution, for example each of the $n!$ orders with probability $1/n!$.

## Related definitions

- A [discrete probability distribution](/discrete-probability-distribution/) is given by a probability mass function.
- A [probability density function](/probability-density-function/) gives a continuous distribution by integration.
- The joint distribution of $X_1, \ldots, X_n$ is the law of the vector $(X_1, \ldots, X_n)$ on $\mathbb{R}^n$. The law of each $X_i$ is a marginal of it.
- The [total variation distance](/total-variation-distance/) $\sup_B |P(B) - Q(B)|$ measures how far apart two distributions are. The [Poisson distribution](/poisson-distribution/) page uses it to bound the error of the Poisson limit of the binomial.
- Named families used in algorithms: [uniform](/uniform-distribution/), [Bernoulli](/bernoulli-trials/), [binomial](/binomial-distribution/), [geometric](/geometric-distribution/), [Poisson](/poisson-distribution/).

## References
