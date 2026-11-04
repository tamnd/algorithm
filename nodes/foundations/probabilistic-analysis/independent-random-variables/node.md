---
tag: RT78CZ
kind: concept
slug: independent-random-variables
name: Independent random variables
aliases:
- mutual independence
- pairwise independence
area: foundations/probabilistic-analysis
level: intro
summary: Random variables whose joint distribution factors; needed for variance of sums and Chernoff bounds.
prereqs: [random-variable, independence-of-events, expected-value]
see_also: [independence-of-events, independent-events, variance, chernoff-bound, chebyshev-inequality, k-wise-independent-hashing, pairwise-independence, moment-generating-function]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix C, Section C.3, Discrete random variables (independent random variables, expectation of a product, variance of a sum)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Section 2.1, Random Variables and Expectation; Section 15.1, Pairwise Independence (15.1.1 pairwise independent bits, 15.1.3 values modulo a prime); Section 15.2, Chebyshev's Inequality for Pairwise Independent Variables
  - book: isbn:9780521474658
    title: Rajeev Motwani and Prabhakar Raghavan, Randomized Algorithms
    locator: Chapter 3, Moments and Deviations, Section 3.4, Two-Point Sampling
  - book: isbn:9780471257080
    title: William Feller, An Introduction to Probability Theory and Its Applications, Volume 1, third edition
    locator: Chapter IX, Random Variables; Expectation (independent variables, products and sums)
---

Random variables are independent when their joint distribution is the product of their own distributions, so that the value of some of them gives no information about the values of the others. Independence of [random variables](/random-variable/) is [independence of events](/independence-of-events/) applied to all the events $\{X \in A\}$ that the variables define. It is the hypothesis behind the rule $\mathrm{E}[XY] = \mathrm{E}[X]\,\mathrm{E}[Y]$, behind the additivity of [variance](/variance/), and behind the [Chernoff bound](/chernoff-bound/). Weaker forms, pairwise and $k$-wise independence, are cheaper to produce and are enough for many algorithms.

## In plain words

Two random quantities are independent when knowing one tells you nothing about the other. The roll of one die and the roll of a second die are independent. The roll of a die and "is the roll even" are not: the second follows from the first.

Independence is a strong demand when there are many quantities. Pairwise independence only asks that each two of them say nothing about each other. Three random bits where the third is the exclusive or of the first two are pairwise independent, yet any two of them fix the third.

The difference matters for algorithms. Some proofs need only pairs to behave, and then a few truly random bits can be stretched into many usable ones. Other proofs, such as the strongest bounds on how far a sum strays from its mean, need full independence.

## The idea

### Definitions

Let $X_1, \ldots, X_n$ be discrete random variables on one [probability space](/probability-space/). They are mutually independent when, for all values $x_1, \ldots, x_n$,
$$ \Pr[X_1 = x_1, \ldots, X_n = x_n] = \prod_{i=1}^{n} \Pr[X_i = x_i]. $$
An equivalent form uses sets. The variables are mutually independent if and only if, for all sets of values $A_1, \ldots, A_n$,
$$ \Pr[X_1 \in A_1, \ldots, X_n \in A_n] = \prod_{i=1}^{n} \Pr[X_i \in A_i]. $$
*Proof of the equivalence.* Taking $A_i = \{x_i\}$ gives the first form from the second. For the other direction, the event on the left is the disjoint union of the events $\{X_1 = x_1, \ldots, X_n = x_n\}$ over $x_i \in A_i$, so its probability is $\sum_{x_1 \in A_1} \cdots \sum_{x_n \in A_n} \prod_i \Pr[X_i = x_i]$, and this sum of products factors as $\prod_i \sum_{x_i \in A_i} \Pr[X_i = x_i] = \prod_i \Pr[X_i \in A_i]$. $\square$

Taking $A_i$ equal to all values for each $i$ outside a set $T$ shows that each subfamily $\{X_i : i \in T\}$ is also mutually independent. The set form also says that the events $\{X_i \in A_i\}$ are mutually independent events, for every choice of the sets. For variables with densities the definition is the same with the set form, or with the joint density equal to the product of the densities.

The variables are $k$-wise independent when each subfamily of $k$ of them is mutually independent, and pairwise independent when they are 2-wise independent. Mutual independence implies $k$-wise independence for each $k$, and $k$-wise implies $j$-wise for $j < k$. The converses fail.

### Functions of independent variables

If $X_1, \ldots, X_n$ are mutually independent and $f_1, \ldots, f_n$ are functions, then $f_1(X_1), \ldots, f_n(X_n)$ are mutually independent.

*Proof.* For values $y_1, \ldots, y_n$, the event $\{f_i(X_i) = y_i\}$ is $\{X_i \in f_i^{-1}(y_i)\}$. Apply the set form with $A_i = f_i^{-1}(y_i)$. $\square$

The same argument shows that functions of disjoint groups of the variables are independent, for example $X_1 + X_2$ and $X_3 X_4$. This is the step that lets an analysis replace a variable by an indicator of it, such as $I\{X_i = 1\}$, and keep independence.

### Products and sums

**Expectation of a product.** If $X$ and $Y$ are independent and both have finite expectation, then $\mathrm{E}[XY] = \mathrm{E}[X]\,\mathrm{E}[Y]$.

*Proof.* By the definition of [expected value](/expected-value/) and independence,
$$ \mathrm{E}[XY] = \sum_{x}\sum_{y} x y \Pr[X = x, Y = y] = \sum_{x}\sum_{y} x y \Pr[X = x]\Pr[Y = y] = \Big(\sum_x x \Pr[X = x]\Big)\Big(\sum_y y \Pr[Y = y]\Big). $$
The double sum converges absolutely, since $\sum_x\sum_y |x||y|\Pr[X=x]\Pr[Y=y] = \mathrm{E}|X|\,\mathrm{E}|Y| < \infty$, so it may be summed in any order and factored. $\square$

By induction, mutually independent $X_1, \ldots, X_n$ with finite expectations satisfy $\mathrm{E}[X_1 \cdots X_n] = \prod_i \mathrm{E}[X_i]$: the variable $X_1 \cdots X_{n-1}$ is a function of the first $n-1$ variables, so it is independent of $X_n$. Applied to $e^{tX_i}$, this gives the product rule for [moment generating functions](/moment-generating-function/), $\mathrm{E}[e^{t(X_1 + \cdots + X_n)}] = \prod_i \mathrm{E}[e^{tX_i}]$, which is the first step of each Chernoff bound.

**Variance of a sum.** If $X_1, \ldots, X_n$ are pairwise independent with finite variances, then $\mathrm{Var}[X_1 + \cdots + X_n] = \sum_i \mathrm{Var}[X_i]$. The proof expands the square and uses $\mathrm{Cov}(X_i, X_j) = \mathrm{E}[X_i X_j] - \mathrm{E}[X_i]\mathrm{E}[X_j] = 0$ for $i \ne j$, which needs independence of the pair only. It is on the page [variance](/variance/). Mutual independence is not needed, and the algorithms below exploit this.

### Uncorrelated is not independent

The rule $\mathrm{E}[XY] = \mathrm{E}[X]\mathrm{E}[Y]$ does not imply independence. Let $X$ be uniform on $\{-1, 0, 1\}$ and $Y = X^2$. Then $\mathrm{E}[XY] = \mathrm{E}[X^3] = 0$ and $\mathrm{E}[X]\mathrm{E}[Y] = 0 \cdot \frac23 = 0$, so the variables are uncorrelated. But $Y$ is a function of $X$, and $\Pr[X = 0, Y = 1] = 0$ while $\Pr[X = 0]\Pr[Y = 1] = \frac13 \cdot \frac23 = \frac29$.

### Pairwise is not mutual

Let $X$ and $Y$ be independent and uniform on $\{-1, +1\}$, and let $Z = XY$. Each pair is independent: for example $\Pr[X = a, Z = c] = \Pr[X = a, Y = ac] = \frac14$ for all signs $a, c$. But $XYZ = X^2 Y^2 = 1$, so $\mathrm{E}[XYZ] = 1$, while $\mathrm{E}[X]\mathrm{E}[Y]\mathrm{E}[Z] = 0$. This is the exclusive-or example of [independence of events](/independence-of-events/), written with signs instead of bits.

### Pitfalls

- **Using the product rule for a function of the same variable.** $\mathrm{E}[X^2] \ne \mathrm{E}[X]^2$ in general; $X$ is not independent of itself unless it is constant. The gap is the variance.
- **Treating zero covariance as independence.** It is enough for the variance of a sum, but not for a Chernoff bound or for $\Pr[X \in A, Y \in B] = \Pr[X \in A]\Pr[Y \in B]$.
- **Applying a Chernoff bound to pairwise independent variables.** The bound is false there, as the example below shows. With pairwise independence use the [Chebyshev inequality](/chebyshev-inequality/).
- **Independence that is lost by conditioning.** Two independent variables need not stay independent given their sum. If $X, Y$ are independent fair bits, then given $X + Y = 1$ the value of $X$ fixes $Y$.

## Examples

**Records in a random order.** In the [hiring problem](/hiring-problem/), candidates come in a uniformly random order, and $X_i$ is the indicator that candidate $i$ is better than candidates $1, \ldots, i-1$. The expectation $\mathrm{E}[X_i] = 1/i$ and its use are on the page [indicator random variable](/indicator-random-variable/). Here we show that $X_1, \ldots, X_n$ are mutually independent.

Let $R_i \in \{1, \ldots, i\}$ be the rank of candidate $i$ among the first $i$ candidates, with rank 1 for the best. The map from an order of the $n$ candidates to $(R_1, \ldots, R_n)$ is one to one: $R_n$ fixes which candidate is last, removing it leaves an order of $n-1$ candidates with ranks $R_1, \ldots, R_{n-1}$, and so on. The set of orders and the set of rank vectors $\{1\} \times \{1, 2\} \times \cdots \times \{1, \ldots, n\}$ both have $n!$ elements, so the map is a bijection. A uniform order therefore gives a uniform rank vector, and the uniform distribution on a product set makes the coordinates independent, each uniform on its own range. So $R_1, \ldots, R_n$ are mutually independent, and $X_i = I\{R_i = 1\}$ are mutually independent as functions of them. For $n = 4$, the probability that all four candidates are hired is $\frac{1}{24} = 1 \cdot \frac12 \cdot \frac13 \cdot \frac14$, and the probability that candidates 2 and 3 are both hired is $\frac16 = \frac12 \cdot \frac13$. By the variance rule above, the variance of the number of hires is $\sum_i \frac1i(1 - \frac1i)$.

**Many pairwise independent bits from few random bits.** Let $X_1, \ldots, X_b$ be independent fair bits. For each nonempty set $S \subseteq \{1, \ldots, b\}$, let $Y_S = \bigoplus_{i \in S} X_i$. This gives $2^b - 1$ bits: 7 bits from 3 random bits, and $1048575$ bits from 20.

*Each $Y_S$ is a fair bit.* Pick $j \in S$. For each fixed value of the other bits, $Y_S$ is $X_j$ or its complement, and both are fair.

*Each pair is independent.* Let $S \ne T$, and say $j \in S \setminus T$ (else swap the names). Fix all bits other than $X_j$. Then $Y_T$ is fixed, and $Y_S$ is still a fair bit. So given any value of $Y_T$, the bit $Y_S$ is fair, which gives $\Pr[Y_S = a, Y_T = c] = \frac14$.

The bits are not 3-wise independent: $Y_{\{1\}} \oplus Y_{\{2\}} = Y_{\{1,2\}}$.

**Pairwise independent values modulo a prime.** Let $p$ be a prime and $A, B$ independent and uniform on $\mathbb{Z}_p$. Define $Y_i = (A + iB) \bmod p$ for $i = 0, \ldots, p-1$. For $i \ne j$ the map $(A, B) \mapsto (Y_i, Y_j)$ is linear with determinant $j - i \not\equiv 0 \pmod p$, so it is a bijection of $\mathbb{Z}_p^2$. Hence $(Y_i, Y_j)$ is uniform on $\mathbb{Z}_p^2$, and the $Y_i$ are pairwise independent and uniform. The same idea with a random polynomial of degree $k - 1$ gives $k$-wise independence, the basis of [$k$-wise independent hashing](/k-wise-independent-hashing/).

**Two-point sampling.** A test uses a random seed from $\mathbb{Z}_p$, and on a "yes" instance at least a fraction $q \ge \frac12$ of the seeds give the right answer "yes". Independent runs with $t$ seeds cost $t \lg p$ random bits and fail with probability at most $2^{-t}$. Instead, take the $t$ seeds $Y_1, \ldots, Y_t$ of the previous example, with $t < p$, from only two random values. Let $W$ count the good seeds. It is a sum of $t$ pairwise independent indicators of probability $q$, so $\mathrm{E}[W] = tq$ and $\mathrm{Var}[W] = tq(1 - q)$. All runs fail only if $W = 0$, and by Chebyshev
$$ \Pr[W = 0] \le \Pr\big[|W - tq| \ge tq\big] \le \frac{tq(1-q)}{(tq)^2} = \frac{1-q}{tq} \le \frac1t. $$
For $t = 100$ the error is at most $0.01$ with $2 \lg p$ random bits, against $2^{-100}$ with $100 \lg p$ bits. This trade of error for random bits is in Motwani and Raghavan, Section 3.4.

**Why the Chernoff bound needs mutual independence.** Take the $2^b - 1$ pairwise independent bits $Y_S$ above. All of them are 0 exactly when $X_1 = \cdots = X_b = 0$, which has probability $2^{-b}$. For $b = 10$ this is $2^{-10} = 0.00098$. For 1023 mutually independent fair bits, the probability that all are 0 is $2^{-1023}$, about $1.1 \times 10^{-308}$. The sum has mean $\mu = 511.5$, and the Chernoff bound $\Pr[\text{sum} \le (1 - \delta)\mu] \le e^{-\delta^2\mu/2}$ for $0 < \delta < 1$ gives, with $\delta = \frac12$, $\Pr[\text{sum} \le \mu/2] \le e^{-63.94} \approx 1.7 \times 10^{-28}$. For the pairwise independent bits, $\Pr[\text{sum} \le \mu/2] \ge \Pr[\text{sum} = 0] = 2^{-10}$, far above this bound, so the Chernoff bound does not hold for them.

## Where it is used

- **Variance and concentration.** The additivity of variance for pairwise independent terms gives Chebyshev bounds on counts, as in two-point sampling and in the [weak law of large numbers](/law-of-large-numbers/). Mutual independence gives the [Chernoff](/chernoff-bound/) and [Hoeffding](/hoeffding-inequality/) bounds.
- **Hashing.** [Universal hash families](/universal-hash-family/) and [$k$-wise independent hashing](/k-wise-independent-hashing/) provide limited independence of hash values at low cost. Chaining with a 2-universal family needs only a bound on the collision probability of each pair of keys; other schemes, such as linear probing, need a higher degree of independence.
- **Derandomization.** A small sample space with pairwise independence, as above, can be searched in full, which turns some randomized algorithms into deterministic ones, see [sample space reduction](/sample-space-reduction/) and [small-bias sample spaces](/small-bias-sample-space/).
- **Records and permutations.** The independence of the relative ranks in a [random permutation](/random-permutation/) gives the exact variance of the number of hires in the hiring problem and of the number of left-to-right maxima.

## References
