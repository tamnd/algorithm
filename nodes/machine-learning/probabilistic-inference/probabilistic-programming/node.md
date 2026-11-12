---
tag: KGYEAS
kind: concept
slug: probabilistic-programming
name: Probabilistic programming
aliases:
- probabilistic programming languages
- PPL
area: machine-learning/probabilistic-inference
level: advanced
summary: "Write a generative model as a program with random choices and observations, and let a generic engine such as enumeration, importance sampling or MCMC on traces infer the posterior."
history:
  year: 2008
  people: [Noah D. Goodman, Vikash K. Mansinghka, Daniel M. Roy, Keith Bonawitz, Joshua B. Tenenbaum]
  note: "Church (2008) made a universal programming language, a Lisp with random choices and conditioning, into a modelling language with generic MCMC inference. BUGS had earlier given a language for graphical models with Gibbs sampling."
prereqs: [bayesian-inference, likelihood-weighting, metropolis-hastings]
see_also: [ancestral-sampling, bayesian-network, importance-sampling, sequential-monte-carlo, hamiltonian-monte-carlo, no-u-turn-sampler, black-box-variational-inference, automatic-differentiation]
sources:
  - paper: "Noah D. Goodman, Vikash K. Mansinghka, Daniel M. Roy, Keith Bonawitz and Joshua B. Tenenbaum, Church: a language for generative models, Proceedings of UAI 2008, pp. 220-229"
    title: Goodman, Mansinghka, Roy, Bonawitz and Tenenbaum 2008
    locator: "the language with random primitives, query by conditioning, stochastic memoization, and MCMC on the execution traces"
  - paper: "David Wingate, Andreas Stuhlmüller and Noah D. Goodman, Lightweight implementations of probabilistic programming languages via transformational compilation, Proceedings of AISTATS 2011, PMLR 15:770-778"
    title: Wingate, Stuhlmüller and Goodman 2011
    locator: "structural addresses for random choices, and single-site Metropolis-Hastings on traces with the correction for fresh and stale choices"
  - paper: doi:10.18637/jss.v076.i01
    title: "Bob Carpenter and others, Stan: a probabilistic programming language, Journal of Statistical Software 76(1):1-32, 2017"
    locator: "the language with typed blocks for data, parameters and model, the log density with automatic differentiation, and inference by the no-U-turn sampler, optimization and variational inference"
  - paper: "Eli Bingham and others, Pyro: deep universal probabilistic programming, Journal of Machine Learning Research 20(28):1-6, 2019"
    title: Bingham and others 2019
    locator: "a universal language embedded in Python with named sample sites, guide programs as variational families, and stochastic variational inference"
  - paper: "Jan-Willem van de Meent, Brooks Paige, Hongseok Yang and Frank Wood, An introduction to probabilistic programming, arXiv:1809.10756, 2018"
    title: van de Meent, Paige, Yang and Wood 2018
    locator: "first order and higher order languages, the density of a program, likelihood weighting, Metropolis-Hastings, sequential Monte Carlo and variational inference for programs"
---

## In plain words

A probabilistic program is a normal program that can also roll dice and that can be told what was observed. Running it once tells one random story of how the data could have come about. The program is the model.

The question is always the same: given what was observed, which stories are likely? A probabilistic programming system answers it with a general engine that works for any program. The engine does not need to know what the program models. It only runs the program many times, controls the dice, and scores each run by how well it explains the observations.

So the modeller writes the model and does not write the inference code. The cost is speed. A general engine is usually slower than an algorithm made for one model, and some engines work only for some kinds of program.

## The idea

**Two new statements.** Take a deterministic programming language and add two statements:

- `sample(address, d)` draws a value from the distribution `d` and returns it. The address names this random choice, so that the same choice can be found in another run.
- `observe(d, y)` states that the value `y` was observed from the distribution `d`. It does not change the run; it multiplies the score of the run by the likelihood $d(y)$. A hard constraint `condition(test)` is the case where the likelihood is 1 or 0.

**The meaning of a program.** One run makes a *trace* $x$: the random choices, each with its address and value, in the order of execution. Let $p_i(x_i \mid \ldots)$ be the probability of the $i$-th choice given the run so far, and $\ell_k$ the likelihood at the $k$-th observe statement. The program defines the unnormalized density
$$P(x) = \prod_{i} p_i(x_i \mid \ldots) \prod_{k} \ell_k(y_k \mid \ldots),$$
the posterior $P(x \mid \text{obs}) = P(x) / Z$ on traces, with the evidence $Z = \sum_x P(x)$, and through the return value a posterior on answers. Running the program forward without the observe statements is [ancestral sampling](/ancestral-sampling/) from the prior.

**More than a graphical model.** A [Bayesian network](/bayesian-network/) is a program without branches: a fixed list of choices. A program can branch on a random value, loop a random number of times or recurse, so the number of choices and their addresses can differ from run to run. Languages that allow this are called universal or higher order (Church, Anglican, WebPPL, Pyro, Gen). Languages that fix a finite set of variables in advance are first order (BUGS, Stan). The extra freedom makes models of unknown size easy to write, such as a scene with an unknown number of objects, a grammar, or a [Dirichlet process](/dirichlet-process/) mixture, but it rules out engines that need a fixed set of variables.

**Generic engines.** Each engine needs only some operations on the program:

| engine | what it does with the program | needs |
|---|---|---|
| enumeration | runs it once for every path of choices, by replaying prefixes | finite discrete choices; the cost grows with the number of traces |
| [likelihood weighting](/likelihood-weighting/) | runs it with every choice from the prior; the weight is the product of the likelihoods | only the ability to run it; the weights spread out when the evidence is unlikely |
| [sequential Monte Carlo](/sequential-monte-carlo/) | runs many copies together and resamples them at each observe statement | the ability to pause runs at observe statements |
| lightweight Metropolis-Hastings | changes one choice of a trace and runs the program again, reusing the other choices by address | addresses that match between runs |
| [Hamiltonian Monte Carlo](/hamiltonian-monte-carlo/), as in Stan | moves all the continuous variables along the gradient of $\log P$ | a fixed set of continuous variables, and [automatic differentiation](/automatic-differentiation/) |
| variational inference, as in Pyro | fits a second program, the guide, as the approximate posterior by stochastic gradients of the [evidence lower bound](/evidence-lower-bound/) | a guide with the same addresses, and gradients |

**Lightweight Metropolis-Hastings.** Wingate, Stuhlmüller and Goodman showed that MCMC on traces needs nothing more than addresses. One step from the trace $x$:

```pseudo
LMH-STEP(program, x)
    a ← an address chosen uniformly from the |x| choices of x
    v ← a new value for a, drawn from the distribution of a in x
    x' ← run the program; at a use v, at an address that x has use the value in x,
          and at a new address draw from the prior
    F ← the prior probability of v and of the new ("fresh") choices of x'
    R ← the prior probability of the old value of a and of the choices of x that x' did not use ("stale")
    accept x' with the probability min(1, P(x') · |x| · R / (P(x) · |x'| · F)), else keep x
```

The factors $|x|, |x'|, F, R$ are the proposal probabilities in the two directions. They matter because the move can change the number of choices. With them, the step satisfies detailed balance with respect to $P(x \mid \text{obs})$, as for any [Metropolis-Hastings](/metropolis-hastings/) kernel. A reused value is scored in $P(x')$ under its new distribution, so a value that the new run makes impossible is rejected.

## Examples

**A trick coin.** A coin is a trick coin with probability $1/10$. A trick coin shows heads with the probability $4/5$ or $1$, each with probability $1/2$; a normal coin with $1/2$. Three heads are observed. In the embedded language of the implementation:

```python
def trick_coin(ctx):
    trick = ctx.sample("trick", flip(Fraction(1, 10)))
    if trick:
        p = ctx.sample("bias", uniform_draw([Fraction(4, 5), Fraction(1)]))
    else:
        p = Fraction(1, 2)
    for _ in range(3):
        ctx.observe(flip(p), True)
    return trick
```

The choice `bias` exists only in some runs. Enumeration finds three traces:

| trace | prior | likelihood | $P(x)$ |
|---|---|---|---|
| trick, bias $4/5$ | $1/20$ | $64/125$ | $16/625$ |
| trick, bias $1$ | $1/20$ | $1$ | $1/20$ |
| not trick | $9/10$ | $1/8$ | $9/80$ |

So $Z = 1881/10000$ and $P(\text{trick} \mid \text{HHH}) = (16/625 + 1/20) / Z = 84/209 \approx 0.4019$. Likelihood weighting with $10000$ runs and the seed 1 gives $0.4046$, and the mean weight $0.1885$ estimates $Z = 0.1881$.

One lightweight MH move from the trace "not trick" has $|x| = 1$, so it picks `trick`. With probability $9/10$ it draws "not trick" again and nothing changes. With probability $1/10$ it draws "trick"; the run then reaches the new address `bias` and draws it fresh, say $4/5$. Then $F = (1/10)(1/2)$, $R = 9/10$, $|x'| = 2$, and
$$\frac{P(x') \, |x| \, R}{P(x) \, |x'| \, F} = \frac{(16/625) \cdot 1 \cdot (9/10)}{(9/80) \cdot 2 \cdot (1/20)} = \frac{256}{125} > 1,$$
so the move is accepted. The reverse move is accepted with the probability $125/256$. A chain of $10000$ steps with $1000$ discarded and the seed 1 gives $0.3888$; its draws are correlated, so it is less accurate than the same number of independent weighted runs here. The tests check that the exact transition matrix of this step satisfies detailed balance, and that the plain rule $\min(1, P(x') / P(x))$, without the four factors, does not leave the posterior invariant.

**A random number of choices.** Flip a coin with $P(\text{heads}) = 1/3$ until heads, at most four times, and condition on at least two flips. The program has a loop with a random exit, so its traces have two, three or four choices (a trace with one flip violates the condition). The posterior of the number of flips is $1/3, 2/9, 4/9$ for $2, 3, 4$, and the evidence is $Z = 2/3$. A graphical model of this program would need four variables with "not used" values; the program needs none.

**A Bayesian network.** The sprinkler network of the [likelihood weighting](/likelihood-weighting/) page, written as a program with `observe` for $C = 1$ and $W = 1$, gives the same answer by enumeration: $P(R = 1 \mid e) = 202/207$ and $Z = 1863/5000$. Likelihood weighting on the program is exactly likelihood weighting on the network, because the `observe` statements are where the network has its evidence.

## Where it is used

- **Statistics.** Stan is widely used in applied statistics for hierarchical regression models and similar models with continuous parameters. Its main engine is the [no-U-turn sampler](/no-u-turn-sampler/), a form of Hamiltonian Monte Carlo, with gradients from automatic differentiation.
- **Machine learning.** Pyro and NumPyro combine probabilistic programs with neural networks, for example to write a [variational autoencoder](/variational-autoencoder/) as a model program and a guide program. Their main engine is [black box](/black-box-variational-inference/) and [stochastic variational inference](/stochastic-variational-inference/).
- **Cognitive science.** Church and its successor WebPPL are used to write models of human reasoning as programs, where conditioning on a program is the model of a mind that reasons about what it sees.
- **Graphical models with message passing.** Some systems, such as Infer.NET, compile a program into a factor graph and run message passing such as [expectation propagation](/expectation-propagation/) or [belief propagation](/belief-propagation/).
- **Teaching and checking.** Exact enumeration on small discrete programs, as in the examples above, gives reference answers to check the approximate engines.

## References
