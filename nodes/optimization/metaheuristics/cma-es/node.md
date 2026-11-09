---
tag: BASB19
kind: algorithm
slug: cma-es
name: CMA-ES
aliases:
- covariance matrix adaptation evolution strategy
- CMA evolution strategy
area: optimization/metaheuristics
level: research
summary: Evolution strategy that samples from a Gaussian and learns its mean, step size and full covariance matrix from ranked samples. It is invariant under monotone changes of f and rotations.
solves: [global-optimization]
model: real-ram
complexity:
  vars: {g: the number of generations, n: the dimension, l: the population size, c: the cost of one value of the objective}
  time: {worst: O(g (l n^2 + l c + n^3))}
  space: {extra: O(n^2 + l n)}
properties: {deterministic: false, iterative: true, anytime: true, population: true, comparison-based: true}
history:
  year: 2001
  people: [Nikolaus Hansen, Andreas Ostermeier]
  note: Hansen and Ostermeier published CMA-ES in its standard form in 2001, after conference papers in 1996 and 1997. Hansen, Müller and Koumoutsakos added the rank-mu update in 2003.
prereqs: [evolution-strategies, covariance-matrix]
see_also: [evolution-strategies, cross-entropy-method, estimation-of-distribution-algorithm, natural-gradient-descent, differential-evolution, derivative-free-optimization, condition-number, quasi-newton-method]
sources:
  - paper: doi:10.1162/106365601750190398
    title: Nikolaus Hansen and Andreas Ostermeier, Completely derandomized self-adaptation in evolution strategies, Evolutionary Computation 9(2), 2001
    locator: pages 159 to 195 (the evolution path, the rank-one update, cumulative step-size adaptation and the invariance properties)
  - paper: doi:10.1162/106365603321828970
    title: Nikolaus Hansen, Sibylle D. Müller and Petros Koumoutsakos, Reducing the time complexity of the derandomized evolution strategy with covariance matrix adaptation (CMA-ES), Evolutionary Computation 11(1), 2003
    locator: pages 1 to 18 (the rank-mu update)
  - paper: "Nikolaus Hansen, The CMA evolution strategy, a tutorial, arXiv:1604.00772, 2016"
    title: Nikolaus Hansen, The CMA evolution strategy, a tutorial
    locator: the summary of the algorithm with its default parameters (Appendix A) and the section on invariance
  - paper: "Yann Ollivier, Ludovic Arnold, Anne Auger and Nikolaus Hansen, Information-geometric optimization algorithms, a unifying picture via invariance principles, Journal of Machine Learning Research 18, 2017"
    title: Yann Ollivier, Ludovic Arnold, Anne Auger and Nikolaus Hansen, Information-geometric optimization algorithms, a unifying picture via invariance principles
    locator: the section that recovers the rank-mu update of CMA-ES as a natural gradient step
  - paper: "Nikolaus Hansen and Stefan Kern, Evaluating the CMA evolution strategy on multimodal test functions, Parallel Problem Solving from Nature PPSN VIII, LNCS 3242, 2004"
    title: Nikolaus Hansen and Stefan Kern, Evaluating the CMA evolution strategy on multimodal test functions
    locator: pages 282 to 291 (larger populations on Rastrigin and other multimodal functions)
---

CMA-ES, the covariance matrix adaptation [evolution strategy](/evolution-strategies/), minimizes a function on $\mathbb{R}^n$ by sampling points from a Gaussian distribution $\mathcal{N}(m, \sigma^2 C)$ and moving the distribution toward the better samples. It learns three things from the ranks of the samples: the mean $m$, the step size $\sigma$, and a full [covariance matrix](/covariance-matrix/) $C$. On a convex quadratic, $C$ comes close to a multiple of the inverse of the Hessian, so the method then behaves as on the sphere, much as a [quasi-Newton method](/quasi-newton-method/) does with gradients. Hansen and Ostermeier published it in its standard form in 2001. The method only uses the order of the values, so it is invariant under strictly increasing transformations of $f$, and its updates are equivariant under rotations of the search space. There is no proof that the full method with its default parameters converges, even on convex quadratics, and on a multimodal function it can stop in a local minimum.

## In plain words

Think of a cloud of guesses around a center point. Each round, throw some random guesses from the cloud, sort them from best to worst, and move the center toward the best half.

Then reshape the cloud. If the good guesses lie along a long narrow valley, stretch the cloud along that valley and squeeze it across. If the last few moves all went in the same direction, make the cloud bigger, because the center is still far from the bottom. If the moves cancel each other out, make it smaller.

After a while the cloud has the same shape as the valley. The search then works as well on a long, thin, tilted valley as on a round bowl. It never needs the slope of the function, and only the order of the guesses counts, never their values.

## The problem

The input is a function $f : \mathbb{R}^n \to \mathbb{R}$ that we can only evaluate, a start mean $m_0$, a start step size $\sigma_0 > 0$ and a budget of evaluations. The goal is a point with a small value of $f$, the [global optimization](/global-optimization/) problem in the [black-box](/black-box-optimization/) setting. CMA-ES is a [derivative-free](/derivative-free-optimization/) method.

## The algorithm

The parameters depend only on $n$. The population size is $\lambda = 4 + \lfloor 3 \ln n \rfloor$ and $\mu = \lfloor \lambda/2 \rfloor$. The weights are $w_i \propto \ln(\mu + \tfrac12) - \ln i$ for $i = 1, \dots, \mu$, with $\sum w_i = 1$, and $\mu_{\mathrm{eff}} = 1/\sum w_i^2$. The learning rates $c_\sigma, d_\sigma, c_c, c_1, c_\mu$ follow the tutorial of Hansen, and $\chi_n = E\lVert \mathcal{N}(0, I) \rVert$. Write $C = B D^2 B^\top$ for the eigendecomposition, with $B$ orthogonal and $D$ diagonal, so $C^{1/2} = B D B^\top$ and $C^{-1/2} = B D^{-1} B^\top$.

```pseudo id=main
CMA-ES(f, m₀, σ₀, budget)
L1  m ← m₀; σ ← σ₀; C ← I; p_σ ← 0; p_c ← 0
L2  while the budget is not used up do
L3      for k ← 1 to λ: z_k ← 𝒩(0, I); y_k ← B D z_k; x_k ← m + σ y_k
L4      sort so that f(x_{1:λ}) ≤ … ≤ f(x_{λ:λ}); y_w ← Σᵢ₌₁^μ wᵢ y_{i:λ}
L5      m ← m + σ y_w
L6      p_σ ← (1 − c_σ) p_σ + √(c_σ(2 − c_σ) μ_eff) · C^(−1/2) y_w
L7      p_c ← (1 − c_c) p_c + h_σ √(c_c(2 − c_c) μ_eff) · y_w
L8      C ← (1 − c₁ − c_μ + δ) C + c₁ p_c p_cᵀ + c_μ Σᵢ₌₁^μ wᵢ y_{i:λ} y_{i:λ}ᵀ
L9      σ ← σ · exp((c_σ/d_σ)(‖p_σ‖/χ_n − 1))
L10     (B, D) ← eigendecomposition of C
L11 return the best point seen
```

Line L4 is the selection: the method keeps the $\mu$ best of the $\lambda$ samples and gives larger weights to better ranks. Line L5 moves the mean to the weighted mean of the selected points. The *evolution paths* $p_\sigma$ and $p_c$ in lines L6 and L7 are sums of recent steps that decay with the rates $c_\sigma$ and $c_c$. In line L8, the term with $p_c p_c^\top$ is the *rank-one update*, which stretches $C$ along the path that the mean has followed, and the sum is the *rank-$\mu$ update*, which fits $C$ to the selected steps of this generation. Line L9 is *cumulative step-size adaptation*: under random selection, $C^{-1/2} y_w$ has the distribution $\mathcal{N}(0, I/\mu_{\mathrm{eff}})$, the factors in L6 make $p_\sigma$ distributed as $\mathcal{N}(0, I)$, and $\sigma$ grows when $p_\sigma$ is longer than $\chi_n$, that is, when successive steps point the same way. The flag $h_\sigma \in \{0, 1\}$ stops the update of $p_c$ while $\lVert p_\sigma \rVert$ is very large, and $\delta = (1 - h_\sigma) c_1 c_c (2 - c_c)$ corrects for that.

For $n = 10$ the defaults are $\lambda = 10$, $\mu = 5$, $w = (0.456, 0.271, 0.162, 0.085, 0.026)$, $\mu_{\mathrm{eff}} = 3.17$, $c_\sigma = 0.284$, $d_\sigma = 1.284$, $c_c = 0.295$, $c_1 = 0.0153$ and $c_\mu = 0.0202$.

## Example

**A tilted valley.** Take $f(x) = \tfrac12 (x_1 + x_2)^2 + 50 (x_1 - x_2)^2$ on $\mathbb{R}^2$. Its Hessian has the eigenvalue 1 along $(1, 1)$ and 100 along $(1, -1)$, so the level sets are long ellipses at $45°$. Start at $m_0 = (1, 1)$ with $\sigma_0 = 0.5$. Here $\lambda = 6$ and $\mu = 3$. With seed 0, the best value, $\sigma$, the condition number of $C$ (the ratio of its largest to its smallest eigenvalue) and the angle of the main axis of $C$ were:

| generation | best $f$ | $\sigma$ | condition of $C$ | angle of the main axis |
|---|---|---|---|---|
| 1 | $2.0$ | $0.450$ | 1.2 | $17.4°$ |
| 10 | $2.9 \cdot 10^{-1}$ | $0.215$ | 3.0 | $46.5°$ |
| 20 | $2.1 \cdot 10^{-3}$ | $0.220$ | 26.2 | $44.0°$ |
| 40 | $2.4 \cdot 10^{-8}$ | $7.3 \cdot 10^{-3}$ | 60.9 | $46.4°$ |
| 80 | $2.0 \cdot 10^{-14}$ | $5.1 \cdot 10^{-5}$ | 186.5 | $48.2°$ |
| 121 | $3.5 \cdot 10^{-21}$ | $3.1 \cdot 10^{-7}$ | 191.4 | $45.8°$ |

After 727 evaluations, $f < 10^{-20}$. The main axis of $C$ turned to the flat direction $(1, 1)$ at $45°$ within 10 generations, and the condition of $C$ grew toward the condition 100 of the inverse Hessian and then moved around it. Over 20 runs (seeds 0 to 19), the number of evaluations to reach $10^{-20}$ was 712.9 on average (637 to 811) for this tilted valley and 715.0 (625 to 925) for the same valley along the axes, $\tfrac12 x_1^2 + 50 x_2^2$ from $(\sqrt 2, 0)$. By the rotation invariance below, the two have the same distribution.

**Learning the inverse Hessian.** On the ellipsoid $f(x) = \sum_{i=1}^{10} 10^{6(i-1)/9} x_i^2$, the eigenvalues of the Hessian are in the ratios $1, 4.6, 21.5, 100, \dots, 10^6$. In the run with seed 0 from $m_0 = (1, \dots, 1)$ and $\sigma_0 = 1$, at the end, the eigenvalues of $C$ divided by the smallest were $1, 5.2, 21.2, 127.4, 430.8, 1797, 7537, 46861, 194793$ and $812413$: close to the ratios of the inverse Hessian.

**Evaluations to reach $f < 10^{-10}$** for $n = 10$, over 10 runs (seeds 0 to 9), all of which reached the target within the budget of 60000:

| function | start | mean | min | max |
|---|---|---|---|---|
| sphere | $m_0 = (1, \dots, 1)$, $\sigma_0 = 1$ | 1615 | 1501 | 1771 |
| ellipsoid, condition $10^6$ | $m_0 = (1, \dots, 1)$, $\sigma_0 = 1$ | 6061 | 5891 | 6371 |
| Rosenbrock, $\sum_{i=1}^{9} 100(x_{i+1} - x_i^2)^2 + (1 - x_i)^2$ | $m_0 = 0$, $\sigma_0 = 0.5$ | 6416 | 5721 | 7271 |

The ellipsoid with condition $10^6$ takes about 4 times as many evaluations as the sphere. Most of them are spent while $C$ is being learned.

**A multimodal function.** On Rastrigin's function $f(x) = 10n + \sum_i (x_i^2 - 10 \cos 2\pi x_i)$ with $n = 5$, from $m_0 = (3, \dots, 3)$ with $\sigma_0 = 2$ and 20000 evaluations, the global minimum ($f < 10^{-8}$) was found in 0 of 20 runs (seeds 0 to 19) with the default $\lambda = 8$, in 6 of 20 with $\lambda = 50$ and in 16 of 20 with $\lambda = 200$. The other runs stopped in a local minimum.

## Correctness

The proofs are below. They cover the structure of the method, not its convergence.

1. **$C$ stays symmetric positive definite.** If $c_1 + c_\mu < 1$, which holds for the default parameters, then every $C$ is symmetric positive definite. So $C^{1/2}$ and $C^{-1/2}$ exist, and the sampling in L3 is well defined.
2. **Under random selection, the paths are standard.** If the order of the $\lambda$ samples does not depend on $f$, then $C^{-1/2} y_w \sim \mathcal{N}(0, I/\mu_{\mathrm{eff}})$, and if $p_\sigma \sim \mathcal{N}(0, I)$ before L6, it is again $\mathcal{N}(0, I)$ after. So $\ln \sigma$ has the drift $\frac{c_\sigma}{d_\sigma}\bigl(E\lVert p_\sigma\rVert/\chi_n - 1\bigr) = 0$ in that stationary state, and $\sigma$ changes only because of selection.
3. **Invariance under increasing transformations of $f$.** With the same random numbers, the runs on $f$ and on $g \circ f$, with $g$ strictly increasing, are identical.
4. **Invariance under translation and orthogonal maps.** The run on $f(x - c)$ from $m_0 + c$ is the run on $f$ shifted by $c$. For an orthogonal $Q$, the run on $f(Q^\top x)$ from $Q m_0$ has the same distribution as the run on $f$ mapped by $Q$, with $C$ mapped to $Q C Q^\top$.

Hansen and Ostermeier also describe invariance under every invertible linear map $A$, when $C_0$ is set to $A A^\top$. For the updates of $m$, $p_c$ and $C$ this follows by the computation of Claim 4 with $A$ in place of $Q$. The path $p_\sigma$ uses the symmetric root $C^{-1/2}$, and for a general $A$ the matrix $C^{-1/2} A$ equals $C'^{-1/2}$ only up to an orthogonal factor that can change from one generation to the next. So the exact statement we prove for $\sigma$ is for orthogonal maps.

What is not proved:

- **Convergence.** To our knowledge there is no proof that CMA-ES with its default parameters converges to a minimum on all convex quadratics, nor a proof of its rate. There are proofs for simpler strategies, such as the linear convergence of the (1+1)-ES with the 1/5 rule (see [evolution strategies](/evolution-strategies/)), and for variants of CMA-ES with changed step-size rules.
- **Global optima.** On a multimodal function, the step size goes to 0 near one local minimum, as on Rastrigin above. No result says which one.
- **The natural-gradient view.** Ollivier, Arnold, Auger and Hansen showed that the rank-$\mu$ update of $m$ and $C$ is a step of [natural gradient descent](/natural-gradient-descent/) on the expected rank-based weight over the Gaussian family. This explains the update, but it is not a proof that the method converges.

## Complexity

One generation draws $\lambda n$ normal numbers and computes $y_k = B D z_k$ in $O(\lambda n^2)$, evaluates $f$ $\lambda$ times, updates $C$ in $O(\mu n^2)$, and computes the eigendecomposition in $O(n^3)$. So $g$ generations cost $O(g(\lambda n^2 + \lambda c + n^3))$. Implementations update $B$ and $D$ only every $\Theta(n/\lambda)$ generations or so, which brings the cost of the algebra to $O(n^2)$ per evaluation. The space is $O(n^2 + \lambda n)$. With $n$ in the thousands, the $n^2$ entries of $C$ are the limit, and variants with diagonal or low-rank $C$ are used. The default $\lambda$ grows only as $\ln n$, so the learning rate $c_\mu$ of order $1/n^2$ means that learning a full $C$ takes on the order of $n^2$ evaluations.

## Properties

- **Comparison-based.** Only the ranks of the values are used (Claim 3). The method is not affected by the scale of $f$, by an offset, or by a monotone change such as $\ln f$.
- **Equivariant under rotations, reflections and translations** (Claim 4), and under uniform scaling with $\sigma_0$ scaled. It does not depend on the choice of the coordinate system, unlike methods that treat each coordinate on its own.
- **Learns the scaling.** After the adaptation phase, $C$ approximates a multiple of the inverse Hessian on a convex quadratic, as the examples show.
- **Few parameters.** The user sets $m_0$, $\sigma_0$ and the budget. The defaults of the other parameters work on a wide range of problems.
- **Not elitist.** The mean can move to a worse point, which helps with noise.
- **Anytime.** The best point seen is valid at each generation.

## Variants and improvements

- **Restarts with a larger population.** IPOP-CMA-ES (Auger and Hansen, 2005) restarts the method with $\lambda$ doubled each time it stops. On multimodal functions with a global structure, such as Rastrigin, a larger population finds the global minimum more often, as the measurement above shows. BIPOP-CMA-ES alternates large and small populations.
- **The (1+1)-CMA-ES.** One parent and one child, with the 1/5 rule for $\sigma$ and a rank-one update of a Cholesky factor of $C$.
- **Active CMA-ES.** It also uses the worst samples, with negative weights, to shrink $C$ in bad directions. It needs care to keep $C$ positive definite.
- **Separable and low-rank variants.** sep-CMA-ES learns only the diagonal of $C$, and other variants learn a low-rank $C$, so that they scale to large $n$.
- **Constraints and noise.** Bounds are usually handled by a penalty or by repairing samples, and noise by more evaluations or a larger $\lambda$.
- **Related methods.** The [cross-entropy method](/cross-entropy-method/) and [estimation of distribution algorithms](/estimation-of-distribution-algorithm/) also fit a distribution to good samples, but they refit it from scratch each time and have no evolution paths. Natural evolution strategies follow the natural gradient directly.

## When to use it

Use CMA-ES for continuous problems with about 2 to a few hundred variables, when gradients are not available or not reliable, and when the problem may be badly scaled, non-separable or rugged. It is a standard choice in this setting and does well on benchmarks of black-box optimization. For multimodal problems, use it with restarts and growing populations. For smooth problems with cheap gradients, a [quasi-Newton method](/quasi-newton-method/) is usually faster. For very cheap functions in very high dimension, the $O(n^2)$ cost per sample can dominate.

## Pitfalls

- **A bad start step size.** $\sigma_0$ should be about a third of the width of the region that holds the optimum. Too small, and the method finds the nearest local minimum.
- **Stopping too early or too late.** Use the standard stopping rules, such as a range of recent best values below a tolerance, or $\sigma$ times the largest eigenvalue root below a tolerance, and restart.
- **A non-symmetric $C$.** Rounding can make $C$ slightly asymmetric if the two halves are computed separately. Compute one half and copy it, as the implementation here does, or symmetrize $C$ before the eigendecomposition.
- **Variables with very different units.** The method learns the scaling, but it wastes evaluations doing so. Rescale the variables to similar ranges when you know them.
- **Bounds.** CMA-ES has no built-in bounds. Clipping the samples biases the update of $C$. A penalty on the distance to the box, or sampling again, is better.
- **Expecting a global optimum.** The default population is small and can stop in a local minimum. Use restarts.

## Implementations

## History

Hansen and Ostermeier introduced the derandomized adaptation of the mutation distribution in the mid 1990s, and published CMA-ES with the evolution path, the rank-one update and cumulative step-size adaptation in Evolutionary Computation in 2001. Hansen, Müller and Koumoutsakos added the rank-$\mu$ update in 2003, which made the method work with large populations. Auger and Hansen proposed the restart strategy IPOP-CMA-ES in 2005. Akimoto, Nagata, Ono and Kobayashi in 2010 and Ollivier, Arnold, Auger and Hansen in 2017 explained the update as a natural gradient step. Hansen keeps a tutorial with the current default parameters.

## References
