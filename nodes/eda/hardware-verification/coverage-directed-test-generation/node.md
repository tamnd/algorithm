---
tag: BA1EWQ
kind: technique
slug: coverage-directed-test-generation
name: Coverage-directed test generation
aliases:
- CDG
- Fine-Ziv coverage-directed generation
area: eda/hardware-verification
level: research
summary: Closes the loop between coverage and stimulus, for example by a Bayesian network that learns which generator settings hit which coverage holes, as in Fine and Ziv.
prereqs: [functional-coverage, constrained-random-stimulus-generation, bayesian-network]
see_also: [bayes-theorem, expectation-maximization, genetic-algorithm, multi-armed-bandit, thompson-sampling, geometric-distribution, bounded-model-checking, coverage-guided-fuzzing]
sources:
  - paper: doi:10.1145/775832.775907
    title: Shai Fine and Avi Ziv, Coverage directed test generation for functional verification using Bayesian networks, Proceedings of the 40th Design Automation Conference, 286 to 291, 2003
    locator: the Bayesian network whose inputs are the directives of the test generator and whose outputs are coverage events, its training on simulation runs, and its use to choose directives for uncovered events
  - paper: "Mark Braun, Shai Fine and Avi Ziv, Enhancing the efficiency of Bayesian network based coverage directed test generation, IEEE International High-Level Design Validation and Test Workshop (HLDVT), 75 to 80, 2004"
    title: M. Braun, S. Fine and A. Ziv, Enhancing the efficiency of Bayesian network based coverage directed test generation, Proceedings of the Ninth IEEE International High-Level Design Validation and Test Workshop, 75 to 80, 2004
    locator: the improvements of the Bayesian network method of Fine and Ziv (general locator)
  - paper: doi:10.1145/2071356.2071363
    title: Charalambos Ioannides and Kerstin I. Eder, Coverage-directed test generation automated by machine learning, a review, ACM Transactions on Design Automation of Electronic Systems 17(1), 2012
    locator: the survey of coverage-directed generation by Bayesian networks, genetic algorithms, genetic programming, Markov models and inductive logic programming (general locator)
---

Coverage-directed test generation (CDG) closes the loop between the [coverage](/functional-coverage/) report of a simulation regression and the settings of the random stimulus generator that drives it. Here a *test* means a simulation stimulus, a program or sequence of transactions for a design under verification; it is not a manufacturing test of a chip. A constrained random generator takes parameters, called *directives* by Fine and Ziv (weights, ranges, modes), and produces many stimuli from each setting. CDG learns from past runs which settings tend to hit which coverage events, and chooses settings that should hit the events no run has hit yet, the *coverage holes*. Fine and Ziv (2003) learn this relation with a [Bayesian network](/bayesian-network/); others use genetic algorithms, bandits or other learned models. The method is a heuristic: what can be proved is the arithmetic of one step, and how much it shortens closure is only measured.

## In plain words

A random generator makes test inputs for a chip design, and it has knobs: how long the bursts are, how often an interrupt comes, which instructions appear most. The team watches a list of situations that the tests should produce. Some situations are rare, and plain random runs almost never reach them.

Instead of turning the knobs by hand, the team records, for many past runs, the knob settings and the situations each run reached. A model learns from these records which settings make which situations likely. To reach a situation that no run has reached, the team asks the model for the most promising settings, runs with them, adds the new records, and asks again.

The model is only a guess. It cannot reach a situation that the design never allows, and it only chases the situations that someone listed.

## When it applies

- A *parametrized generator*. The stimulus comes from a random generator with a finite set of directives $D_1, \ldots, D_k$, each with a finite domain, and each setting $d$ gives a distribution over stimuli. [Constrained random stimulus generation](/constrained-random-stimulus-generation/) is the usual source.
- A *coverage model*. A finite set of events $E_1, \ldots, E_m$, such as bins of a [functional coverage](/functional-coverage/) model, and a monitor that reports which of them a run hit.
- *Many cheap runs*. The model learns from data, so it needs a few hundred or thousand runs over varied settings, and simulation must be cheap enough to give them.
- *Holes that the generator can reach*. Some setting must give the hole a probability that is not tiny. If the hole needs a sequence that no setting makes likely, a directed test or a formal witness from a [bounded model checker](/bounded-model-checking/) fits better. If the hole is unreachable in the design, no generator hits it, and the hole should be proved unreachable and removed.

## The template

**1. Collect data.** Run the generator with settings $d^{(1)}, \ldots, d^{(N)}$, chosen at random over the directive domains, one or more runs per setting. For each run record the setting and the vector $e \in \{0, 1\}^m$ of events that it hit.

**2. Fix the structure.** Write a network whose root nodes are the directives, whose leaf nodes are the coverage events, and whose inner nodes stand for intermediate quantities, such as the instruction mix or "the queue was full". The edges come from what the engineers know about the generator and the design; this is the part that needs expertise. The joint law factors as

$$ P(d, h, e) = \prod_{x} P(x \mid \mathrm{pa}(x)) $$

over all nodes $x$, where $\mathrm{pa}(x)$ are the parents of $x$ and $h$ are the inner nodes.

**3. Learn the tables.** Estimate each conditional table from the data. For observed nodes, count: with $n$ runs in which the parents of $x$ take the values $u$, and $k$ of them with $x = 1$, a smoothed estimate is $(k + 1)/(n + 2)$. For inner nodes that the monitor does not record, use [expectation maximization](/expectation-maximization/).

**4. Query.** For a hole $E_j$, compute $P(E_j = 1 \mid D = d)$ for candidate settings by exact inference in the network (for example [variable elimination](/variable-elimination/)) and pick

$$ d^\ast = \arg\max_d P(E_j = 1 \mid D = d). $$

For a set $H$ of holes, pick the $d$ that maximizes the expected number of new hits per run, $\sum_{j \in H} P(E_j = 1 \mid D = d)$. The two objectives can choose different settings.

**5. Run and repeat.** Simulate with $d^\ast$, add the runs to the data, update the tables, and query again. Stop when the holes are hit, or when the model gives every remaining hole a very small probability under every setting; such holes go to a directed test or to a formal tool.

**What can be proved about one step.**

- *Expected new hits.* If a run with setting $d$ hits $E_j$ with probability $p_j(d)$, the expected number of holes of $H$ that the run hits is $\sum_{j \in H} p_j(d)$, by [linearity of expectation](/linearity-of-expectation/) over the indicators of the events; no independence between events is needed.
- *Waiting time.* Runs with a fixed setting are independent, so the number of runs until $E_j$ is first hit has a [geometric distribution](/geometric-distribution/) with mean $1/p_j(d)$.
- *Two forms of the query.* The query can also ask for the setting that is most probable given that the hole is hit, $\arg\max_d P(D = d \mid E_j = 1)$. By [Bayes' theorem](/bayes-theorem/), $P(D = d \mid E_j = 1) = P(E_j = 1 \mid D = d) \, P(D = d) / P(E_j = 1)$. So the two forms choose the same setting when the prior $P(D = d)$ is uniform over the candidates, and they can differ when it is not.

These facts are about the true probabilities $p_j(d)$. The network gives estimates of them, and how close the estimates are depends on the data and on the structure. That the loop closes coverage faster than plain random runs is a measured result of the papers, not a theorem.

## Classic examples

**A FIFO with two knobs.** A generator has the directives $D_1$ = burst length in $\{\text{short}, \text{long}\}$ and $D_2$ = read rate in $\{\text{slow}, \text{fast}\}$. The event $F$ is "the FIFO became full in the run". Forty runs per setting, 160 in all, gave these counts.

| setting | runs | runs with $F$ | smoothed estimate |
|---|---|---|---|
| short, slow | 40 | 2 | 3/42 |
| short, fast | 40 | 0 | 1/42 |
| long, slow | 40 | 14 | 15/42 |
| long, fast | 40 | 3 | 4/42 |

The query picks (long, slow). With settings drawn uniformly, the observed hit rate per run is $19/160 \approx 0.12$, so the expected wait for a hit is about $160/19 \approx 8.4$ runs. With (long, slow) the observed rate is $14/40 = 0.35$, a wait of about $2.9$ runs. The training prior was uniform, so the posterior form gives the same choice: $P(D = d \mid F = 1)$ is proportional to the counts $2, 0, 14, 3$.

**A hole, reached through structure.** Add a third directive $D_3$ = flush rate in $\{\text{low}, \text{high}\}$, drawn at random in each run, and the event $L$ = "the run issued a flush". The coverage task $G$ = "the run filled the FIFO and issued a flush" was never hit. In the network, $F$ has parents $D_1, D_2$; $L$ has parent $D_3$; and $G$ is the AND of $F$ and $L$. The structure says that $F$ and $L$ are independent given the directives, so

$$ P(G = 1 \mid d) = P(F = 1 \mid d_1, d_2) \; P(L = 1 \mid d_3). $$

If the runs gave $P(L = 1 \mid \text{high}) = 1/2$, the model predicts $15/42 \cdot 1/2 \approx 0.18$ for (long, slow, high), the best setting, although $G$ has no hit in the data. This is how a network can rank settings for a hole: the hole shares parents with events that were hit. The prediction rests on the independence that the structure assumes; if a flush empties the FIFO, the assumption is wrong and the runs will show it.

**Fine and Ziv (2003).** The first network-based CDG, for the generator of stimuli of a processor design. The directives are the inputs of the network, the coverage events its outputs, and the inner nodes encode knowledge of the design. The network is trained on simulation runs and queried for directives that hit uncovered events. Braun, Fine and Ziv (2004) improved its efficiency.

## Variations

- **Genetic algorithms.** Treat a setting of the directives as a genome, its fitness as the coverage that its runs add, and evolve a population with a [genetic algorithm](/genetic-algorithm/). No structure needs to be written, and many more runs are needed. The review of Ioannides and Eder surveys this family, with genetic programming and other learned models.
- **Bandits.** With a fixed list of candidate settings and the reward "new events hit by the run", the choice of setting is a [multi-armed bandit](/multi-armed-bandit/); [Thompson sampling](/thompson-sampling/) keeps a posterior per setting and balances trying new settings against using the best one. The reward changes as holes are filled, which the basic bandit model does not allow.
- **Formal help.** For a hole that random settings miss, a [bounded model checker](/bounded-model-checking/) given the event as a cover goal returns a trace, or a proof that the event cannot happen within the bound. The trace can be replayed as a directed test, or used to tune the constraints.
- **Software analogues.** [Coverage-guided fuzzing](/coverage-guided-fuzzing/) closes the same loop for programs, but changes the inputs themselves, not the parameters of a generator.

## Pitfalls

- **Settings that never vary.** If a directive kept one value in all training runs, the data say nothing about its other values, and the network cannot rank them. Draw the training settings at random over the domains; because the directives are set by the engineer and not observed, the learned dependence of events on directives is causal.
- **A non-uniform prior.** The query $\arg\max_d P(D = d \mid E_j = 1)$ favors settings that were tried often. If in the FIFO example the setting (long, fast) had run 400 times with 30 hits, a rate of $0.075$, the posterior would prefer it ($30$ of the $46$ hits) over (long, slow) with a rate of $0.35$. Ask for $\arg\max_d P(E_j = 1 \mid D = d)$, or divide by the prior.
- **Zero counts.** A table with $k = 0$ estimates the probability as 0 and the setting is never tried again. Smooth the estimates.
- **One setting for everything.** Running only $d^\ast$ hits the target hole and stops exploring the rest of the stimulus space, where bugs that no event describes may be. Keep a share of runs at random settings.
- **The model is the limit.** CDG fills holes of the coverage model. A situation that no event describes is never a target, and a hit is still not a check: the response must be judged by checkers or [assertions](/assertion-based-verification/).
- **Unreachable holes.** An event that the design cannot produce stays at probability near 0 under every setting, and the loop runs forever unless it stops on a threshold and sends the hole to a formal tool.

## Exercises

1. In the FIFO example, a second event $E'$ has the hit counts $10, 30, 1, 4$ for the four settings in the order of the table. Which single setting maximizes the expected number of hits of $\{F, E'\}$ per run, using the observed rates?
2. Prove that the expected number of runs with a fixed setting until $E_j$ is first hit is $1/p_j(d)$, and that the probability that $r$ runs miss it is $(1 - p_j(d))^r$.
3. Show that $\arg\max_d P(D = d \mid E = 1)$ and $\arg\max_d P(E = 1 \mid D = d)$ agree for every event when $P(D = d)$ is uniform, and give a two-setting example where they differ otherwise.
4. In the hole example, suppose a flush always empties the FIFO before it can be full in the same run. Which edge is missing from the network, and what does the model predict for $G$ after it is added?
5. A setting has 0 hits in 50 runs. Compare the raw estimate, the smoothed estimate $(k+1)/(n+2)$, and the upper end of a one-sided 95 percent bound $1 - 0.05^{1/50}$.

## References
