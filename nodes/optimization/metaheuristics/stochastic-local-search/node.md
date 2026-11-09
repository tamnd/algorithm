---
tag: ZKRFPQ
kind: concept
slug: stochastic-local-search
name: Stochastic local search
aliases:
- SLS
area: optimization/metaheuristics
level: advanced
summary: Local search whose moves or acceptance decisions are randomized.
prereqs: [local-search, neighborhood-structure, randomized-algorithm]
see_also: [walksat, simulated-annealing, iterated-local-search, random-restart-hill-climbing, las-vegas-algorithm, geometric-distribution, fitness-landscape, metaheuristic]
sources:
  - book: isbn:9781558608726
    title: Holger H. Hoos and Thomas Stützle, Stochastic Local Search, Foundations and Applications, Morgan Kaufmann, 2004
    locator: Section 1.5, Stochastic Local Search, from p. 37 (the formal definition); Chapter 2, SLS Methods, from p. 61; Section 4.1, from p. 149 (run-time distributions, probabilistic approximate completeness, with details from p. 155); Section 6.3, WalkSAT, from p. 273
  - paper: "Uwe Schöning, A probabilistic algorithm for k-SAT and constraint satisfaction problems, Proceedings of the 40th Annual Symposium on Foundations of Computer Science, IEEE, 1999"
    locator: pp. 410 to 414 (random walk with restarts for k-SAT and its bound)
  - book: isbn:9783319910857
    title: Michel Gendreau and Jean-Yves Potvin (editors), Handbook of Metaheuristics, third edition, Springer, 2019
    locator: Chapter 5, Iterated Local Search, from p. 129, and Chapter 7, Multi-start Methods, pp. 221 to 243
---

Stochastic local search (SLS) is the family of [local search](/local-search/) methods that make random decisions: where to start, which neighbor to try, or whether to accept a move. The standard formal framework is the one of Hoos and Stützle's 2004 book. Random choices let a search leave [local optima](/local-optimum/) and cross plateaus without a fixed rule that could cycle, and they make the run time a random variable. [WalkSAT](/walksat/), [simulated annealing](/simulated-annealing/), [iterated local search](/iterated-local-search/), [late acceptance hill climbing](/late-acceptance-hill-climbing/) and [random-restart hill climbing](/random-restart-hill-climbing/) are SLS methods. For a few of them a bound on the expected time is proved, as for Schöning's random walk for $k$-SAT; for most, the guarantees are only that the success probability grows with time, if that.

## In plain words

A plain local search always does the same thing from the same start, so it always gets stuck in the same place. A stochastic local search rolls dice. It may start somewhere random, pick a random neighbor, or sometimes take a step that makes things a little worse.

Because of the dice, two runs can end in different places and take different times. So you do not ask how long one run takes, but how the time is spread over many runs, and how likely a run is to succeed within a given time.

## The idea

Hoos and Stützle define an SLS algorithm for a problem instance by:

- a search space $S$ and a set $S' \subseteq S$ of solutions, the goal;
- a [neighborhood](/neighborhood-structure/) relation $N$ on $S$;
- a finite set $M$ of memory states, which holds what the method remembers, such as a temperature, a [tabu list](/tabu-list/) or nothing at all;
- an initialization function, which gives a probability distribution over the start pairs in $S \times M$;
- a step function, which maps the current pair $(x, m)$ to a probability distribution over pairs $(y, m')$ with $y \in N(x)$;
- a termination predicate, which gives for each pair the probability of stopping there.

Methods that also use constructions, kicks or populations fit this frame by a suitable choice of the search space and of the memory.

Two properties describe what an SLS algorithm can do on a solvable instance.

- **Probabilistic approximate completeness (PAC).** The probability of having found a solution within $t$ steps tends to 1 as $t \to \infty$, from every start. A method is *essentially incomplete* if this limit is below 1, for example because it can get stuck in a region it never leaves. Hoos and Stützle analyze which SAT methods are PAC; adding a small probability of a random walk step is a common way to make a method PAC.
- **The run-time distribution (RTD).** The distribution of the number of steps to a solution over independent runs. It is the natural object to measure and compare, rather than a mean alone.

Some exact facts follow from the random choices.

- **Restarts.** If one independent run succeeds with probability $p$, then $R$ runs all fail with probability $(1 - p)^R$, and the number of runs until the first success has a [geometric distribution](/geometric-distribution/) with mean $1/p$.
- **Exponential run times.** If the run time $T$ has an exponential distribution, then $P(T > s + t \mid T > s) = P(T > t)$: a run that has failed so far is as good as a fresh one, and a restart neither helps nor hurts. Restarts can help when the run time has a heavier tail than an exponential distribution.
- **Las Vegas behavior.** A method that stops only when it finds a solution and checks it, such as WalkSAT on a satisfiable formula, is a [Las Vegas algorithm](/las-vegas-algorithm/): its answer is always right, and only its time is random.

## Examples

- **Uniform random walk.** Move to a uniform random neighbor at each step. It is PAC on any connected neighborhood graph, but usually slow.
- **Randomized iterative improvement.** With probability $w_p$, take a random neighbor; otherwise make one step of iterative improvement. Hoos and Stützle use this as a simple SLS method.
- **WalkSAT.** Pick an unsatisfied clause at random and flip one of its variables, with a noise parameter that sets how often the choice is random.
- **Schöning's random walk.** For $k$-SAT with $n$ variables: start from a uniform random assignment, and $3n$ times pick an unsatisfied clause and flip a uniform random variable of it; restart if no solution is found. Schöning proved that one try finds a solution of a satisfiable formula with probability at least about $(2(k-1)/k)^{-n}$, up to a polynomial factor, so the expected time is $O((2(k-1)/k)^n \cdot \mathrm{poly}(n))$, which for 3-SAT is $O(1.334^n)$ up to the polynomial factor. On one planted 3-SAT instance with $n = 12$ variables and 50 clauses (generated with Python `random.Random(42)`, 12 satisfying assignments), 64% of 20000 tries (with `random.Random(1)`) succeeded, far above the worst-case bound $(3/4)^{12} \approx 0.03$.
- **Simulated annealing.** Pick a random neighbor and accept a worse one with a probability that depends on a temperature; the temperature is the memory state.
- **Iterated local search and GRASP.** Random kicks or random greedy constructions, followed by a deterministic descent.

## Where it is used

SLS methods are standard for [SAT](/sat/) and [MAX-SAT](/max-sat/), the [traveling salesman problem](/traveling-salesman-problem/), scheduling, and constraint problems, often as the best known practical method for large instances. Because their run times are random, studies of SLS methods report run-time distributions, success rates within a time limit, and the number of independent runs, with the seeds used. The analysis of the [fitness landscape](/fitness-landscape/) explains much of their behavior. On satisfiable instances an SLS method can find a solution and prove it by checking, but on unsatisfiable instances it cannot prove that no solution exists, which is why complete methods are still needed.

## References
