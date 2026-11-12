---
tag: R9W3YJ
kind: algorithm
slug: annealed-importance-sampling
name: Annealed importance sampling
aliases:
- AIS
area: machine-learning/probabilistic-inference
level: research
summary: "Move samples from an easy distribution to a target through a chain of intermediate ones with MCMC, and weight them so that the mean weight estimates Z_T / Z_0."
model: real-ram
complexity:
  vars: {s: the number of runs, t: the number of intermediate distributions, c: the cost of one transition and one density evaluation, d: the size of one state}
  time: {worst: "O(s t c)"}
  space: {extra: "O(s + d)"}
properties: {deterministic: false, exact: false, online: false, recursive: false}
history:
  year: 2001
  people: [Radford M. Neal]
  note: "Neal described annealed importance sampling in a 1998 technical report and published it in Statistics and Computing in 2001. Jarzynski had found the same identity for nonequilibrium work in physics in 1997."
prereqs: [importance-sampling, markov-chain, partition-function]
see_also: [sequential-monte-carlo, simulated-annealing, parallel-tempering, likelihood-weighting, partition-function-computation, marginal-likelihood, effective-sample-size, evidence-lower-bound]
sources:
  - paper: doi:10.1023/A:1008923215028
    title: "Radford M. Neal, Annealed importance sampling, Statistics and Computing 11(2):125-139, 2001"
    locator: "the algorithm, the proof by importance sampling on the extended space with reversed kernels, the estimate of the ratio of normalizing constants, the geometric path, and the variance of the log weights as the number of intermediate distributions grows"
  - paper: doi:10.1103/PhysRevLett.78.2690
    title: "Christopher Jarzynski, Nonequilibrium equality for free energy differences, Physical Review Letters 78(14):2690-2693, 1997"
    locator: "the equality between the exponential average of the work over nonequilibrium paths and the free energy difference"
  - paper: "Pierre Del Moral, Arnaud Doucet and Ajay Jasra, Sequential Monte Carlo samplers, Journal of the Royal Statistical Society B 68(3):411-436, 2006"
    title: Del Moral, Doucet and Jasra 2006
    locator: "the framework of backward kernels on the extended space, with annealed importance sampling as the case without resampling"
  - paper: doi:10.1145/1390156.1390266
    title: "Ruslan Salakhutdinov and Iain Murray, On the quantitative analysis of deep belief networks, Proceedings of ICML 2008, pp. 872-879"
    locator: "AIS estimates of the partition function of restricted Boltzmann machines, and the test log likelihood of deep belief networks"
  - paper: "Roger B. Grosse, Zoubin Ghahramani and Ryan P. Adams, Sandwiching the marginal likelihood using bidirectional Monte Carlo, arXiv:1511.02543, 2015"
    title: Grosse, Ghahramani and Adams 2015
    locator: "forward AIS as a stochastic lower bound and reverse AIS from an exact posterior sample as a stochastic upper bound on the log marginal likelihood"
---

Annealed importance sampling (AIS) estimates the normalizing constant $Z_T$ of an unnormalized density $f_T$, and expectations under $p_T = f_T / Z_T$. It starts with exact draws from an easy distribution $p_0$ whose constant $Z_0$ is known. It then moves each draw through a chain of intermediate distributions $p_1, \ldots, p_{T-1}$ toward $p_T$, with one Markov chain step at each one. A weight records how much each step changed the density. The mean weight is an unbiased estimate of $Z_T / Z_0$. AIS is [importance sampling](/importance-sampling/) on the whole path, and it works where plain importance sampling from $p_0$ to $p_T$ fails because the two are too far apart.

## In plain words

You want the total mass of a complex distribution, and you can only sample a simple one. Importance sampling from the simple one to the complex one gives weights that are almost all zero and a few that are huge.

AIS makes the trip in many small steps. It builds a series of distributions that change slowly from the simple one to the complex one. Each sample starts in the simple distribution. At each step, it first records the ratio of the next density to the current density at its place, and then it takes one random step that suits the next distribution. The weight of the sample is the product of the ratios.

Each ratio is close to 1 because the steps are small, so the weights stay even. The average weight is the ratio of the two masses, with no bias.

## The problem

The input is a sequence of unnormalized densities $f_0, f_1, \ldots, f_T \ge 0$ on a state space $\mathcal{X}$, with the unknown constants $Z_j = \sum_x f_j(x)$ (an integral for a continuous space). The first one is easy: $Z_0$ is known, and exact draws from $p_0 = f_0 / Z_0$ are possible. For each $j \ge 1$, there is a Markov kernel $K_j$ that leaves $p_j$ invariant, such as a [Metropolis-Hastings](/metropolis-hastings/) or [Gibbs](/gibbs-sampling/) step. The task is to estimate $Z_T$, which is often a [partition function](/partition-function/) or a [marginal likelihood](/marginal-likelihood/), and expectations $\mathbb{E}_{p_T}[h]$.

The usual choice is the geometric path
$$f_j(x) = f_0(x)^{1 - \beta_j} f_T(x)^{\beta_j}, \qquad 0 = \beta_0 < \beta_1 < \cdots < \beta_T = 1,$$
where $\beta_j$ is an inverse temperature. For a posterior, $f_0$ is the prior and $f_T$ is the prior times the likelihood, so $f_j$ is the prior times the likelihood to the power $\beta_j$.

## The algorithm

```pseudo id=main
ANNEALED-IMPORTANCE-SAMPLING(f_0..f_T, K_1..K_T, s)
L1  for r ← 1 to s do
L2      x ← a draw from p_0 = f_0 / Z_0
L3      log w ← 0
L4      for j ← 1 to T do
L5          log w ← log w + log f_j(x) − log f_{j−1}(x)
L6          x ← a draw from K_j(x, ·), a kernel that leaves p_j invariant
L7      record the run: (log w_r, x_r) ← (log w, x)
L8  return Ẑ_T = Z_0 · (1/s) Σ_r w_r, and the weighted states (w_r, x_r) for expectations
```

Line L5 evaluates the ratio $f_j / f_{j-1}$ at the state *before* line L6 moves it. The runs are independent. For an expectation, use the self-normalized estimate $\sum_r w_r h(x_r) / \sum_r w_r$.

### Why it is importance sampling

Neal's view puts the whole run on an extended space. The proposal is the joint law of the path $(x_0, x_1, \ldots, x_{T-1})$ that lines L2 and L6 produce. The target is a path that starts at $x_{T-1} \sim p_T$ and runs backward through the reversed kernels $\tilde K_j(y, x) = K_j(x, y) \, p_j(x) / p_j(y)$. Its marginal on $x_{T-1}$ is exactly $p_T$. The ratio of the target and the proposal path densities, with all the kernel terms cancelled, is the product of line L5, divided by $Z_T / Z_0$. So the run is one draw of importance sampling on paths, and its weight has the mean $Z_T / Z_0$.

The weight also has a direct reading. With the geometric path, line L5 adds $(\beta_j - \beta_{j-1}) \big(\log f_T(x) - \log f_0(x)\big)$. The sum is a Riemann sum for the thermodynamic integration identity
$$\log \frac{Z_T}{Z_0} = \int_0^1 \mathbb{E}_{p_\beta}\big[\log f_T(x) - \log f_0(x)\big] \, d\beta,$$
but evaluated along one random path, and exponentiated before averaging.

## Example

**A three-state check.** Take the states $a, b, c$, with $f_0 = (1, 1, 1)$ and $f_T = (8, 1, 1)$, so $Z_0 = 3$ and $Z_T = 10$. Use $T = 2$ with the linear path $f_{1/2} = \tfrac12 f_0 + \tfrac12 f_T = (4.5, 1, 1)$. Each $K_j$ is Metropolis with a uniform proposal among the other two states. One run:

| step | state before | line L5 factor | weight | line L6 move |
|---|---|---|---|---|
| L2 | | | 1 | draw $x = a$ from $p_0$ |
| $j = 1$ | $a$ | $f_{1/2}(a) / f_0(a) = 4.5$ | 4.5 | under $f_{1/2}$, $a$ stays with probability $7/9$; say it stays |
| $j = 2$ | $a$ | $f_T(a) / f_{1/2}(a) = 8 / 4.5$ | 8 | the last move changes $x$, not $w$ |

A run that starts at $b$ gets the factor $1$ at $j = 1$, then moves to $a$ or $c$ with probability $1/2$ each, and ends with the weight $16/9$ or $1$. The exact mean is easiest to see through $m_j(x) = \mathbb{E}[w_j [x_j = x]]$. It starts at $(1/3, 1/3, 1/3)$. The factor of $j = 1$ makes it $(3/2, 1/3, 1/3)$, which is $f_{1/2} / 3$, and $K_1$ leaves it unchanged because $K_1$ leaves $f_{1/2}$ invariant. The factor of $j = 2$ makes it $(8/3, 1/3, 1/3) = f_T / 3$. The mean weight is $10/3$, and $Z_0 \cdot 10/3 = 10 = Z_T$.

If both kernels left $f_0$ invariant instead, the second step would no longer find $m_1 \propto f_{1/2}$, and the exact mean weight would be $131/54 \approx 2.43$, not $10/3$. The invariance of $K_j$ for $p_j$ is what makes the estimate unbiased.

**An Ising chain.** The target is an open chain of 16 spins $x_i \in \{-1, 1\}$ with $f_T(x) = \exp\big(2 \sum_i x_i x_{i+1}\big)$, so $\log Z_T = \log 2 + 15 \log(2 \cosh 2) = 30.9654$. The start $p_0$ is uniform, with $Z_0 = 2^{16}$. The path is geometric with equal steps $\beta_j = j / T$, and each $K_j$ is one Gibbs sweep at $\beta_j$. With $s = 1000$ runs and the seed 1:

| $T$ | $\hat Z_T / Z_T$ | variance of $\log w$ | effective sample size |
|---|---|---|---|
| 1 | 0.0198 | 59.68 | 2.8 |
| 10 | 1.7435 | 7.69 | 6.1 |
| 100 | 0.9701 | 0.92 | 452.8 |

With $T = 1$, AIS is plain importance sampling from the uniform distribution. The aligned states that carry most of $Z_T$ are almost never drawn, so the estimate is far too low, and the [effective sample size](/effective-sample-size/) shows it. With $T = 100$ the variance of $\log w$ is about 65 times smaller, and the estimate is within 3 percent.

## Correctness

Let $m_j(y) = \mathbb{E}[w_j [x_j = y]]$, where $w_j$ and $x_j$ are the weight and the state after step $j$. By induction, $m_j = f_j / Z_0$. The base case is $m_0 = f_0 / Z_0$ because $x_0 \sim p_0$ and $w_0 = 1$. In the step, line L5 multiplies $m_{j-1} = f_{j-1} / Z_0$ by $f_j / f_{j-1}$, which gives $f_j / Z_0$, and line L6 applies $K_j$, which leaves $f_j$ unchanged. The step needs the support condition $f_j(x) > 0 \Rightarrow f_{j-1}(x) > 0$. Summing $m_T$ over the states gives $\mathbb{E}[w_T] = Z_T / Z_0$, so $\hat Z_T$ is unbiased for every $s$. The same identity gives $\mathbb{E}[w_T h(x_T)] = (Z_T / Z_0) \mathbb{E}_{p_T}[h]$, so the self-normalized estimate converges almost surely by the strong law of large numbers. By Jensen's inequality, $\mathbb{E}[\log \hat Z_T] \le \log Z_T$, and by Markov's inequality, $P(\log \hat Z_T > \log Z_T + b) \le e^{-b}$. The full proof is in the proofs file.

## Complexity

- **Time.** Each run evaluates two log densities and makes one transition at each of the $T$ steps. With $c$ the cost of one transition and one evaluation, $s$ runs cost $O(s t c)$, where $t = T$. For the Ising chain, one Gibbs sweep and one energy cost $O(n)$, so the total is $O(s T n)$.
- **Space.** $O(d)$ for the current state and $O(s)$ for the weights, or $O(s d)$ when the final states are kept for expectations.
- **Number of steps.** Neal shows that, when the kernels bring each state close to $p_j$ and the path is smooth, the variance of $\log w$ falls like $1/T$. The table of the example shows this from $T = 10$ to $T = 100$. So a longer path can replace a much larger number of runs.
- **Parallel.** The $s$ runs are independent and can run in parallel.

## Properties

- **Unbiased for the ratio of constants.** $\mathbb{E}[\hat Z_T] = Z_T$ for every $s$ and every $T$, if each $K_j$ leaves $p_j$ invariant.
- **Stochastic lower bound on $\log Z_T$.** The log of the estimate is biased low. It exceeds $\log Z_T$ by $b$ with probability at most $e^{-b}$.
- **No mixing needed for correctness.** The kernels need only leave $p_j$ invariant. They need not be reversible or mix. Bad mixing increases the variance; it never adds bias to $\hat Z_T$.
- **The final states are weighted, not exact.** A final state $x_T$ alone is not a draw from $p_T$. Only the pairs $(w, x_T)$ estimate expectations under $p_T$.
- **No burn-in.** Each run starts from an exact draw of $p_0$, so there is no burn-in and no need to diagnose convergence of a chain.

## Variants and improvements

- **Plain importance sampling.** With $T = 1$, or with kernels that do not move, the weight is $f_T(x_0) / f_0(x_0)$, and AIS is [importance sampling](/importance-sampling/).
- **Sequential Monte Carlo samplers.** Del Moral, Doucet and Jasra put AIS in a general framework with backward kernels. Adding [resampling](/resampling/) when the effective sample size drops gives an SMC sampler; AIS is the case without resampling. See [sequential Monte Carlo](/sequential-monte-carlo/).
- **Other paths and schedules.** Besides the geometric path, the linear path $(1 - \beta) f_0 + \beta f_T$ and paths through moments are used. The spacing of $\beta_j$ can be adapted so that each step changes the weights by the same amount.
- **Better kernels.** [Hamiltonian Monte Carlo](/hamiltonian-monte-carlo/) steps work well on continuous spaces, where they make each intermediate step mix faster.
- **Bidirectional Monte Carlo.** On simulated data, an exact posterior sample is available. Running AIS in reverse from it gives a stochastic *upper* bound on $\log Z_T$, which, with the forward lower bound, sandwiches the true value (Grosse, Ghahramani and Adams).
- **Related schemes.** [Simulated annealing](/simulated-annealing/) uses the same sequence of temperatures to find a maximum, and keeps no weights. [Parallel tempering](/parallel-tempering/) runs all the temperatures at once as one MCMC chain. Neal's tempered transitions use a heat and cool cycle as one Metropolis move.

## When to use it

Use AIS to estimate a normalizing constant or a [marginal likelihood](/marginal-likelihood/) when exact [partition function computation](/partition-function-computation/) is infeasible and MCMC steps for the intermediate distributions are available. It is a standard way to evaluate the test log likelihood of energy models such as restricted Boltzmann machines (Salakhutdinov and Murray), and of latent variable models such as the [variational autoencoder](/variational-autoencoder/), where the [evidence lower bound](/evidence-lower-bound/) gives only a bound. When posterior samples are the only goal, a single long MCMC chain is often cheaper. When the target has well separated modes, resampling as in SMC, or parallel tempering, can help more.

## Pitfalls

- **Weight after the move.** Line L5 must use the state before the move of line L6. Swapping the two gives a biased estimate.
- **Kernels for the wrong distribution.** Each $K_j$ must leave $p_j$ invariant, at its own temperature. A kernel for $p_T$ or $p_0$ at every step gives a biased estimate, as the three-state example shows.
- **Too few steps.** With too few intermediate distributions, a few runs carry all the weight, and the estimate of $\log Z_T$ is typically much too low. Because the estimate of $Z_T$ is unbiased but skewed, most runs of the whole procedure underestimate it, and an occasional run overestimates it by a lot. Report the effective sample size and the variance of $\log w$.
- **Reading the log estimate as unbiased.** $\log \hat Z_T$ is a lower bound in expectation. Comparing two models by their AIS log estimates favours the model whose AIS runs mix better.
- **Underflow.** Keep $\log w$, and average with the log-sum-exp trick, as line L8 of the implementation does.
- **Support.** An intermediate density that is zero where a later one is positive loses mass and biases the estimate down.

## Implementations

## History

Jarzynski (1997) proved in nonequilibrium statistical physics that the exponential average of the work done while a system is driven from one state to another equals the exponential of the free energy difference. Neal (technical report 1998, journal paper 2001) found the same construction independently for statistics. He combined [simulated annealing](/simulated-annealing/) with importance sampling, gave the extended space proof, and used it for Bayesian marginal likelihoods; the log weight is the negative of the work in Jarzynski's identity, measured in units of $kT$. Del Moral, Doucet and Jasra (2006) placed AIS inside the framework of [sequential Monte Carlo](/sequential-monte-carlo/) samplers. Salakhutdinov and Murray (2008) made AIS the standard tool to estimate the partition function of restricted Boltzmann machines, and Grosse, Ghahramani and Adams (2015) added the reverse runs that give upper bounds.

## References
