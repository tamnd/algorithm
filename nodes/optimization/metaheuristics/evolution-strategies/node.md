---
tag: ZYGTRG
kind: algorithm
slug: evolution-strategies
name: Evolution strategies
aliases:
- ES
- (mu,lambda)-ES
- (mu+lambda)-ES
- (1+1)-ES
- 1/5 success rule
area: optimization/metaheuristics
level: advanced
summary: Evolutionary methods on real vectors that add Gaussian noise to parents and adapt the noise size. The (1+1)-ES with the 1/5 rule converges linearly on the sphere.
solves: [global-optimization]
model: real-ram
complexity:
  vars: {k: the number of steps, n: the dimension, c: the cost of one value of the objective}
  time: {worst: O(k (n + c))}
  space: {extra: O(n)}
properties: {deterministic: false, iterative: true, anytime: true, population: false, comparison-based: true}
history:
  year: 1965
  people: [Ingo Rechenberg, Hans-Paul Schwefel, Peter Bienert]
  note: Rechenberg, Schwefel and Bienert started evolution strategies at the Technical University of Berlin in the 1960s. Rechenberg gave the 1/5 success rule in 1973.
prereqs: [black-box-optimization, mutation]
see_also: [cma-es, differential-evolution, genetic-algorithm, evolutionary-computation, derivative-free-optimization, fitness-function, linear-convergence-strongly-convex, condition-number]
sources:
  - paper: doi:10.1023/A:1015059928466
    title: Hans-Georg Beyer and Hans-Paul Schwefel, Evolution strategies, a comprehensive introduction, Natural Computing 1(1), 2002
    locator: pages 3 to 52 (the (mu/rho +, lambda) notation, the 1/5 success rule and self-adaptation)
  - book: isbn:9783540672975
    title: Hans-Georg Beyer, The Theory of Evolution Strategies, Springer, 2001
    locator: the chapter on the (1+1)-ES on the sphere model (the progress rate and the optimal normalized mutation strength)
  - paper: "Jens Jägersküpper, Algorithmic analysis of a basic evolutionary algorithm for continuous optimization, Theoretical Computer Science 379(3), 2007"
    title: Jens Jägersküpper, Algorithmic analysis of a basic evolutionary algorithm for continuous optimization
    locator: pages 329 to 347 (Theta(n) steps to halve the distance on the sphere with the 1/5 rule)
  - paper: "Youhei Akimoto, Anne Auger, Tobias Glasmachers and Daiki Morinaga, Global linear convergence of evolution strategies on more than smooth strongly convex functions, SIAM Journal on Optimization 32(2), 2022"
    title: Youhei Akimoto, Anne Auger, Tobias Glasmachers and Daiki Morinaga, Global linear convergence of evolution strategies on more than smooth strongly convex functions
    locator: the main theorem on the (1+1)-ES with success-based step-size adaptation
  - paper: "Olivier Teytaud and Sylvain Gelly, General lower bounds for evolutionary algorithms, Parallel Problem Solving from Nature PPSN IX, LNCS 4193, 2006"
    title: Olivier Teytaud and Sylvain Gelly, General lower bounds for evolutionary algorithms
    locator: pages 21 to 31 (lower bounds from the number of bits that comparisons give)
---

Evolution strategies (ES) are [evolutionary](/evolutionary-computation/) methods that minimize a function on $\mathbb{R}^n$. They make new points by adding Gaussian noise to parent points, keep the best ones, and change the size of the noise, the *step size*, while they run. Rechenberg and Schwefel started them in Berlin in the 1960s. The simplest member is the (1+1)-ES: one parent, one child per step, and the better of the two survives. With the 1/5 success rule, which makes the step size larger when more than one step in five succeeds and smaller otherwise, it converges linearly on the sphere: Jägersküpper proved that it needs $\Theta(n)$ steps to halve the distance to the optimum. The method only compares values of $f$, so it is unchanged when $f$ is replaced by a strictly increasing function of $f$. On a function with many [local minima](/local-optimum/), there is no guarantee that it finds the global one.

## In plain words

Stand on a hill in fog and look for the lowest point. Take a random step of about some length. If the new spot is not higher, stay there; if it is higher, go back.

Now also change the step length. If many steps work, you are far from the bottom, so make the steps longer. If almost no step works, you are too close for that length, so make them shorter. Rechenberg found that the best balance is when about one step in five works.

This simple rule makes the walker go down at a fixed rate, halving the distance to the bottom again and again, on a smooth round bowl. It only looks at which spot is lower, never at how much lower.

## The problem

The input is a function $f : \mathbb{R}^n \to \mathbb{R}$ that we can only evaluate, a start point $x_0$, a start step size $\sigma_0 > 0$ and a number of steps $K$. The goal is a point with a small value of $f$, the [global optimization](/global-optimization/) problem in the [black-box](/black-box-optimization/) setting. No gradient is used, so ES are [derivative-free](/derivative-free-optimization/) methods.

## The algorithm

The (1+1)-ES with the 1/5 success rule, in the per-step form that recent analyses such as Akimoto et al. use. The damping $D = \sqrt{n + 1}$ is one common choice of order $\sqrt n$. Here $\mathcal{N}(0, I)$ is a vector of $n$ independent standard normal numbers.

```pseudo id=main
ONE-PLUS-ONE-ES(f, x₀, σ₀, K)
L1  D ← √(n + 1);  x ← x₀;  σ ← σ₀
L2  for k ← 1 to K do
L3      y ← x + σ · 𝒩(0, I)
L4      if f(y) ≤ f(x) then             ▷ success
L5          x ← y
L6          σ ← σ · exp(1/D)
L7      else σ ← σ · exp(−1/(4D))
L8  return x
```

A success multiplies $\sigma$ by $e^{1/D}$ and a failure by $e^{-1/(4D)}$. Four failures cancel one success, so $\sigma$ stays the same exactly when one step in five succeeds. Rechenberg's original rule counts the successes over a window of steps and then multiplies or divides $\sigma$ by a constant. Both versions push the success rate toward $1/5$.

## Example

Minimize the sphere $f(x) = x_1^2 + x_2^2$ from $x_0 = (1, 1)$ with $\sigma_0 = 1$, so $D = \sqrt 3$, $e^{1/D} = 1.7813$ and $e^{-1/(4D)} = 0.8656$. With seed 0 the first 10 steps are:

| step | $f(x)$ | $\sigma$ | success |
|---|---|---|---|
| 1 | 2.0000 | 1.0000 | no |
| 2 | 2.0000 | 0.8656 | yes |
| 3 | 1.9137 | 1.5419 | no |
| 4 | 1.9137 | 1.3347 | yes |
| 5 to 7 | 0.4683 | 2.3774, 2.0579, 1.7813 | no |
| 8 | 0.4683 | 1.5419 | yes |
| 9, 10 | 0.3824 | 2.7466, 2.3774 | no |

After step 10, $x = (-0.2109, -0.5813)$, $f(x) = 0.3824$ and $\sigma = 2.0579$. There were 3 successes in 10 steps, and $\sigma_{10} = \exp((3 - 7/4)/\sqrt 3) = 2.0579$, as the formula in the proof gives.

**Linear convergence on the sphere.** Start at $x_0 = (1/\sqrt n, \dots, 1/\sqrt n)$, so $f(x_0) = 1$, with $\sigma_0 = 1$, and count the steps until $f(x) < 10^{-16}$, that is, until the distance to the optimum is below $10^{-8}$. Over 20 runs (seeds 0 to 19) for each $n$:

| $n$ | mean steps | min | max | rate $c = n \ln(10^8)/\text{mean}$ | fraction of successes |
|---|---|---|---|---|---|
| 2 | 294.7 | 248 | 351 | 0.125 | 0.119 |
| 5 | 619.8 | 524 | 726 | 0.149 | 0.141 |
| 10 | 1199.8 | 1020 | 1337 | 0.154 | 0.157 |
| 20 | 2198.4 | 1976 | 2368 | 0.168 | 0.166 |
| 40 | 4413.9 | 3972 | 4703 | 0.167 | 0.175 |

The number of steps grows linearly with $n$, and the distance falls by a factor of about $e^{-c/n}$ per step, so it halves in about $n \ln 2 / c \approx 4.1 n$ steps for $n = 40$. Beyer computes the best possible rate for the (1+1)-ES on the sphere as $n \to \infty$: the normalized progress $\varphi^*(s) = \frac{s}{\sqrt{2\pi}} e^{-s^2/8} - \frac{s^2}{2}\bigl(1 - \Phi(s/2)\bigr)$, with $s = \sigma n / \lVert x - x^* \rVert$, has its maximum $0.2025$ at $s = 1.224$, where the success probability is $1 - \Phi(0.612) = 0.270$. The measured rates are below this optimum, as they must be.

The fraction of successes is below $1/5$ because $\sigma$ must shrink with the distance. By Claim 2 of the proof, $\ln(\sigma_K/\sigma_0) = (S - (K - S)/4)/D$ after $S$ successes in $K$ steps. If $\sigma$ falls at the same rate $c/n$ per step as the distance, this gives $S/K = 1/5 - \frac{4}{5} D c / n$, which is $0.159$ for $n = 10$ and $0.179$ for $n = 40$, close to the measured $0.157$ and $0.175$.

**A badly scaled function.** On the ellipsoid $f(x) = \sum_{i=1}^{n} 10^{6(i-1)/(n-1)} x_i^2$ with $n = 10$, whose [condition number](/condition-number/) is $10^6$, from $x_0 = (1, \dots, 1)$ with $f(x_0) = 1274605$ and $\sigma_0 = 1$, the value after 20000 steps was between 56.6 and 158.8 over seeds 0 to 4. On the sphere with the same start and budget it was below $10^{-271}$ for all 5 seeds. The step size adapts to the steep directions, and progress along the flat ones is very slow. This is the problem that [CMA-ES](/cma-es/) solves.

## Correctness

The proofs are below. They cover what holds for every $f$, and the one convergence result that holds for every $f$ is for a variant with a fixed step size.

1. **Elitism.** $f(x)$ never increases, and after each step $f(x)$ is the smallest value of $f$ seen so far. So the returned point is the best point evaluated.
2. **The step size is a function of the number of successes.** After $S$ successes in $K$ steps, $\sigma_K = \sigma_0 \exp\bigl((S - (K - S)/4)/D\bigr)$. So $\sigma_K = \sigma_0$ if and only if $S = K/5$.
3. **Invariance.** With the same random numbers, the run on $g \circ f$ with $g$ strictly increasing gives exactly the same points as on $f$. The run on $f(x - c)$ from $x_0 + c$ gives the points shifted by $c$. The run on $f(x/a)$ with $a > 0$ from $a x_0$ with step size $a \sigma_0$ gives the points multiplied by $a$. For an orthogonal matrix $Q$, the run on $f(Q^\top x)$ from $Q x_0$ has the same distribution as $Q$ times the run on $f$.
4. **A lower bound for every comparison-based method.** If the optimum of the sphere is uniform in the unit ball, any method that learns one bit per step needs at least $n \log_2(1/\varepsilon) - 1$ steps to be within $\varepsilon$ of it with probability $1/2$.
5. **Fixed step size.** If $\sigma$ is held fixed, $f$ is continuous, its minimum $f^*$ is attained and the level set $\{f \le f(x_0)\}$ is bounded, then for every $\varepsilon > 0$, $P(f(x_K) \ge f^* + \varepsilon) \le (1 - p)^K$ for some $p > 0$. This is a guarantee in the limit only, with a $p$ that can be tiny.

Two results need more than the space here.

- **Jägersküpper (2007).** On the sphere, the (1+1)-ES with the 1/5 rule (in the window form, with a window of $n$ steps) reduces the distance to the optimum by a factor $1/2$ in $\Theta(n)$ steps, with a probability that tends to 1 exponentially fast in $n$, once $\sigma$ is adapted to the distance. So $b$ halvings take $\Theta(b n)$ steps. Claim 4 shows that this is the best order for any method that learns one bit per step.
- **Akimoto, Auger, Glasmachers and Morinaga (2022).** For $f = g \circ h$, where $h$ is strongly convex with a Lipschitz gradient and $g$ is strictly increasing, the (1+1)-ES with this success-based rule converges linearly: the expected number of steps to come within $\varepsilon$ of the optimum is $O(\log(1/\varepsilon))$, with a constant that depends on $n$ and on the ratio of the Lipschitz constant to the strong convexity constant, and grows with that ratio. This explains the slow progress on the ellipsoid above.

With the 1/5 rule, $\sigma$ goes to 0 at a linear rate, so the method converges to a local minimum on a multimodal function. Claim 5 does not apply, and no result says which local minimum it reaches.

## Complexity

One step draws $n$ normal numbers, forms $y$ in $O(n)$ and evaluates $f$ once, so $K$ steps cost $O(K(n + c))$, where $c$ is the cost of $f$. The extra space is $O(n)$. On the sphere, reaching distance $\varepsilon$ from distance 1 takes $\Theta(n \log(1/\varepsilon))$ steps by the theorem of Jägersküpper and the lower bound of Claim 4. On an ill-conditioned quadratic, the number of steps also grows with the condition number.

## Properties

- **Comparison-based.** Only the outcome of $f(y) \le f(x)$ is used. So the method is invariant under strictly increasing transformations of $f$, and it is robust to the scale of $f$.
- **Invariant under translation, uniform scaling and rotation** of the search space, with the matching change of $x_0$ and $\sigma_0$ (Claim 3).
- **Not invariant under scaling of single coordinates.** The mutation is isotropic, so a badly scaled problem is slow. CMA-ES learns a covariance matrix to remove this.
- **Elitist.** The current point is always the best point seen.
- **No gradient.** It works on functions that are not differentiable, and on noisy functions with care.
- **Anytime.** $x$ is valid at each step.

## Variants and improvements

- **The $(\mu, \lambda)$-ES and the $(\mu + \lambda)$-ES.** Keep $\mu$ parents, make $\lambda$ children, and select the $\mu$ best either from the children only (comma) or from parents and children (plus). The comma version forgets the parents, which helps on noisy or changing functions and lets the step size grow again.
- **Recombination.** The $(\mu/\mu, \lambda)$-ES moves to the mean of the $\mu$ best children, with equal or decreasing weights. The mean reduces the effect of the noise in the bad directions.
- **Self-adaptation.** Each child carries its own step size, mutated by a log-normal factor $\sigma' = \sigma e^{\tau \mathcal{N}(0,1)}$ with $\tau \approx 1/\sqrt{2n}$, and selection keeps the step sizes of the good children. Schwefel also adapted one step size per coordinate and rotation angles.
- **Cumulative step-size adaptation.** Compare the length of the sum of recent steps with its expected length under random selection, and change $\sigma$ when the steps are longer or shorter than that. This is the rule in [CMA-ES](/cma-es/).
- **Covariance matrix adaptation.** [CMA-ES](/cma-es/) samples from $\mathcal{N}(m, \sigma^2 C)$ and learns $C$, which makes the method invariant under all linear changes of coordinates.
- **Natural evolution strategies.** They follow the [natural gradient](/natural-gradient-descent/) of the expected value of $f$ over the search distribution.

## When to use it

Use an ES for continuous problems of small to medium dimension where gradients are not available or not useful: simulation models, noisy measurements, functions with kinks. The (1+1)-ES is a good first method because it has almost no parameters. For badly scaled or non-separable problems, use CMA-ES. For smooth problems where gradients are cheap, a [quasi-Newton method](/quasi-newton-method/) is usually much faster. For multimodal problems, use restarts with a larger population and do not expect a guarantee.

## Pitfalls

- **Expecting a global optimum.** With the 1/5 rule the step size goes to 0, so the run settles in one basin.
- **The start step size.** A $\sigma_0$ far too small makes the method a slow local search until $\sigma$ grows, and on a multimodal function it fixes the basin early. A rule of thumb is about a third of the width of the region where the optimum can be.
- **Success with or without equality.** With $f(y) < f(x)$, a run on a plateau never succeeds and $\sigma$ shrinks to 0. With $f(y) \le f(x)$, as here, the walk can drift across the plateau.
- **Constants of the 1/5 rule.** A factor that changes $\sigma$ too fast makes the step size noisy, and one that changes it too slowly wastes steps. Only the ratio $1/4$ of the two exponents fixes the target rate $1/5$; the damping $D$ sets the speed.
- **Bad scaling.** The isotropic mutation is very slow on ill-conditioned problems, as the ellipsoid example shows. Rescale the variables or use CMA-ES.
- **Noise.** With a noisy $f$, an elitist method can keep a point that was lucky once. Use a comma strategy or evaluate the parent again.

## Implementations

## History

Ingo Rechenberg, Hans-Paul Schwefel and Peter Bienert started evolution strategies at the Technical University of Berlin in the mid 1960s, first on physical experiments such as the shape of a plate in a wind tunnel. Rechenberg's 1973 book gave the theory of the (1+1)-ES on the sphere and on a corridor model and the 1/5 success rule. Schwefel introduced the $(\mu, \lambda)$ and $(\mu + \lambda)$ strategies and self-adaptation in the 1970s. Beyer developed the theory of progress rates in the 1990s. Jägersküpper gave the first proofs of the running time with the 1/5 rule in 2003 and 2007, and Akimoto, Auger, Glasmachers and Morinaga proved global linear convergence on a large class of functions in 2022. Hansen and Ostermeier added cumulative step-size and covariance matrix adaptation, which led to [CMA-ES](/cma-es/).

## References
