---
tag: RTM0C2
kind: theorem
slug: branching-process-extinction-theorem
name: Extinction probability of a branching process
aliases:
- branching process extinction theorem
area: biology/epidemic-and-ecological-models
level: core
summary: "If p_1 < 1, the extinction probability of a Galton-Watson process is the smallest root of f(s) = s in [0, 1], and it is 1 if and only if the mean offspring m is at most 1."
history:
  year: 1875
  people: [Henry William Watson, Francis Galton]
  note: Watson found the recursion for the generating function in 1875 but missed the root below 1 and concluded that every family dies out. Bienayme had stated the correct criterion earlier, and later authors gave full proofs.
prereqs: [galton-watson-process]
see_also: [galton-watson-process, birth-death-process, martingale, stochastic-sir-model, final-size-relation, basic-reproduction-number, fixed-point-iteration, epidemic-threshold]
sources:
  - book: "Theodore E. Harris, The Theory of Branching Processes, Springer, 1963"
    title: Harris 1963
    locator: Chapter I, the theorem on the probability of extinction of the Galton-Watson process
  - book: "Krishna B. Athreya and Peter E. Ney, Branching Processes, Springer, 1972"
    title: Athreya and Ney 1972
    locator: Chapter I, the extinction probability and the critical case
  - paper: "H. W. Watson and Francis Galton, On the probability of the extinction of families, Journal of the Anthropological Institute of Great Britain and Ireland 4, 1875, pages 138 to 144"
    title: Watson and Galton 1875
    locator: Watson's solution with the iterated generating function
  - paper: doi:10.1093/biomet/42.1-2.116
    title: "P. Whittle, The outcome of a stochastic epidemic, a note on Bailey's paper, Biometrika 42, 1955"
    locator: the bound on the probability of a minor outbreak through a comparison with birth-death processes
  - book: isbn:9780387950501
    title: Hakan Andersson and Tom Britton, Stochastic Epidemic Models and Their Statistical Analysis, Lecture Notes in Statistics 151, Springer, 2000
    locator: Chapter 3, the branching process approximation and the probability of a major outbreak
---

## Statement

Let $(Z_n)$ be a [Galton-Watson process](/galton-watson-process/) with $Z_0 = 1$ and offspring distribution $(p_k)_{k \ge 0}$. Let $f(s) = \sum_k p_k s^k$ be the probability generating function, and $m = \sum_k k p_k \in [0, \infty]$ the mean number of children. Let

$$q = P(Z_n = 0 \text{ for some } n)$$

be the probability of extinction.

**Theorem.** Assume $p_1 < 1$. Then:

1. $q$ is the smallest root of the equation $f(s) = s$ in $[0, 1]$.
2. $q = 1$ if and only if $m \le 1$.
3. $P(Z_n = 0) = f_n(0)$, where $f_n$ is $f$ composed with itself $n$ times, and $f_n(0)$ increases to $q$ as $n \to \infty$.

From $Z_0 = k$ the extinction probability is $q^k$.

## In plain words

Start with one individual. Each individual has a random number of children, all with the same law, and then dies. The line can die out, or it can grow without end. The chance that it dies out is the answer to one equation: the chance of extinction of the whole line must equal the chance that every child's own line dies out. That equation always has the answer "certain extinction", and it can have one smaller answer. The true chance is the smaller one. When the average number of children is at most one, there is no smaller answer, so the line dies out for sure, even when the average is exactly one. When the average is above one, the line survives with a positive chance. The only exception is when every individual has exactly one child, because then the line goes on forever.

## Proof

The generating function $f$ has three properties on $[0, 1]$ that the proof uses. It is continuous and nondecreasing, since all $p_k \ge 0$. It is convex, since $f''(s) = \sum_k k(k-1) p_k s^{k-2} \ge 0$. And $f(1) = 1$, $f(0) = p_0$.

**Step 1: the iteration.** Given $Z_1 = j$, the process is $j$ independent copies of the process that start at time 1, so $P(Z_{n+1} = 0 \mid Z_1 = j) = P(Z_n = 0)^j$. Let $q_n = P(Z_n = 0)$. Then

$$q_{n+1} = \sum_j p_j q_n^j = f(q_n), \qquad q_0 = 0,$$

so $q_n = f_n(0)$. Since 0 is absorbing, the events $\{Z_n = 0\}$ increase with $n$, and their union is the event of extinction. So $q_n$ is nondecreasing and $q_n \to q$ by the continuity of probability. As $f$ is continuous, $q = \lim q_{n+1} = \lim f(q_n) = f(q)$. So $q$ is a root of $f(s) = s$ in $[0, 1]$.

**Step 2: $q$ is the smallest root.** Let $s \in [0, 1]$ with $f(s) = s$. Then $q_0 = 0 \le s$. If $q_n \le s$, then $q_{n+1} = f(q_n) \le f(s) = s$, because $f$ is nondecreasing. So $q_n \le s$ for all $n$, and $q \le s$. This proves parts 1 and 3.

**Step 3: when the smallest root is 1.** Let $g(s) = f(s) - s$, so $g(1) = 0$ and $g(0) = p_0 \ge 0$.

*Case $p_0 + p_1 = 1$.* No individual has more than one child. Then $f(s) = p_0 + p_1 s$ and $m = p_1 < 1$. The equation $p_0 + p_1 s = s$ has the only root $s = p_0 / (1 - p_1) = 1$. So $q = 1$, and $m \le 1$, as the theorem says.

*Case $p_k > 0$ for some $k \ge 2$.* Then $f''(s) > 0$ on $(0, 1)$, so $f'$ is strictly increasing there and $g$ is strictly convex on $[0, 1]$.

- If $m \le 1$: for $s \in [0, 1)$, $f'(s) < \lim_{t \uparrow 1} f'(t) = m \le 1$, so $g'(s) < 0$. So $g$ is strictly decreasing on $[0, 1]$, and $g(s) > g(1) = 0$ for every $s < 1$. The only root in $[0, 1]$ is 1, and $q = 1$.
- If $m > 1$ (the case $m = \infty$ included): the difference quotient $(f(1) - f(s))/(1 - s)$ tends to $m > 1$ as $s \uparrow 1$, so $f(s) < s$ for $s$ close to 1, that is, $g(s) < 0$. Since $g(0) \ge 0$ and $g$ is continuous, $g$ has a root in $[0, 1)$. By step 2, $q$ is at most this root, so $q < 1$.

This proves part 2. For $Z_0 = k$, the $k$ lines are independent, and the whole population dies out exactly when each line dies out, which has probability $q^k$. $\square$

## Consequences

**Speed of the iteration.** Line L4 of the procedure on the [Galton-Watson page](/galton-watson-process/) is the [fixed-point iteration](/fixed-point-iteration/) $q_{n+1} = f(q_n)$. In the supercritical case, convexity gives $q - q_{n+1} = f(q) - f(q_n) \le f'(q)(q - q_n)$, and $f'(q) < 1$, because $g$ crosses zero from above at $q$. So the error falls at least as fast as $f'(q)^n q$. For Poisson(2) offspring, $f'(q) = m q = 0.406376$, and the iterates are $q_1 = 0.135335$, $q_2 = 0.177403$, $q_5 = 0.201525$, $q_{10} = 0.203169$, $q_{20} = 0.203188$. In the subcritical case, $1 - q_n = P(Z_n > 0) \le E[Z_n] = m^n$. In the critical case the iteration is slow: $1 - q_n \sim 2/(n \sigma^2)$ when $\sigma^2 < \infty$, so for Poisson(1) offspring $q_{1000} = 0.998008$.

**Poisson offspring and the final size.** For Poisson($R_0$) offspring, $f(s) = e^{R_0(s - 1)}$. With $z = 1 - q$, the equation $q = f(q)$ becomes $z = 1 - e^{-R_0 z}$, the [final size relation](/final-size-relation/) of the deterministic SIR model. So the probability of a major outbreak equals the final attack fraction. The values are $q = 0.417188$ for $R_0 = 1.5$, $q = 0.203188$ for $R_0 = 2$ and $q = 0.059520$ for $R_0 = 3$.

**Geometric offspring and the stochastic SIR model.** In the early phase of the [stochastic SIR model](/stochastic-sir-model/), a case infects others at rate $\beta$ for an exponential time with rate $\gamma$. The number of people that it infects is geometric, with $f(s) = 1/(1 + R_0 - R_0 s)$ and $R_0 = \beta / \gamma$. The roots of $f(s) = s$ are $1$ and $1/R_0$. So $q = 1/R_0$ for $R_0 > 1$. With $i$ initial cases, the probability of a minor outbreak is about $(1/R_0)^i$, and $1 - (1/R_0)^i$ is the probability of a major outbreak. Whittle (1955) gave this result for the general stochastic epidemic through a comparison with [birth-death processes](/birth-death-process/). For $R_0 = 2$, one case gives a major outbreak with probability $1/2$ under geometric offspring and $0.797$ under Poisson offspring. The geometric law is a Poisson law with a random mean, so it is more spread out. Such spread makes extinction more likely at the same mean, because $s^k$ is convex in $k$ and so $f(s)$ grows when the offspring law spreads out.

**A martingale.** Since $E[q^{Z_{n+1}} \mid Z_n] = f(q)^{Z_n} = q^{Z_n}$, the process $q^{Z_n}$ is a bounded [martingale](/martingale/). It converges almost surely, and its limit is 1 on extinction and 0 on survival (when $q < 1$). So $E[q^{Z_n}] = q$ for every $n$, and on survival $Z_n \to \infty$.

**Extinction or explosion.** If $p_1 < 1$, the process does not stay in a bounded set of positive values forever. If $p_0 > 0$, each visit to a state $k \ge 1$ ends in extinction at the next step with probability $p_0^k$, so each such state is visited only finitely often. If $p_0 = 0$, the process never decreases, and it increases at each step with a probability of at least $1 - p_1 > 0$. So with probability 1, either $Z_n = 0$ eventually or $Z_n \to \infty$.

**The epidemic threshold.** Part 2 is the stochastic form of the [epidemic threshold](/epidemic-threshold/): a major outbreak has positive probability if and only if the mean number of secondary cases per case, the [basic reproduction number](/basic-reproduction-number/), is above 1.

## Tightness

- **The condition $p_1 < 1$ is needed.** If $p_1 = 1$, then $f(s) = s$, every point of $[0, 1]$ is a root, $m = 1$ and $q = 0$. Part 1 still holds (0 is the smallest root), but part 2 fails.
- **"Smallest" is needed.** The value $s = 1$ is always a root. When $m > 1$ there are exactly two roots in $[0, 1]$, and $q$ is the one below 1. Watson (1875) chose the wrong root. The iteration must start at 0: started at 1, it stays at 1.
- **"At most 1" includes the critical case.** For $m = 1$ the line dies out with probability 1, even though $E[Z_n] = 1$ for every $n$. The mean stays at 1 because the rare surviving lines are large: given $Z_n > 0$, $E[Z_n \mid Z_n > 0] = 1/P(Z_n > 0)$, which grows like $n \sigma^2 / 2$.
- **No moment condition beyond the mean.** The proof uses only the mean. The theorem holds for $m = \infty$, where $q < 1$.
- **The example with two roots.** For $p_0 = 1/4$, $p_1 = 1/4$, $p_2 = 1/2$, the roots are $1/2$ and $1$, and $m = 5/4$. The exact values $f_n(0) = 0.25, 0.34375, 0.39502, \ldots$ increase to $q = 1/2$, not to 1.
- **The assumptions of the model matter.** If the offspring law changes with the generation or depends on the population size, as it does when susceptibles run out, the theorem does not apply as stated. In an epidemic, $q$ is the probability of a minor outbreak only in the limit of a large population.

## History

Galton posed the problem of the extinction of surnames as a public question, and Watson's solution appeared in their joint paper of 1875 ([Watson and Galton](#references)). Watson set up the recursion $q_{n+1} = f(q_n)$ correctly, but he concluded that $q = 1$ in every case, because he did not see the second root below 1. Bienayme had stated the correct criterion in 1845, and his note was found again in the twentieth century. Complete proofs came in the 1920s and 1930s, and the result took its modern form in the books of [Harris](#references) and of [Athreya and Ney](#references). In epidemic theory, Whittle (1955) used the comparison with branching processes to bound the probability of a minor outbreak.

## References
