---
tag: F1GKBX
kind: algorithm
slug: genetic-algorithm
name: Genetic algorithm
aliases:
- GA
- simple genetic algorithm
- canonical genetic algorithm
area: optimization/metaheuristics
level: intro
summary: Evolve a population of bit strings by selection, crossover and mutation. With elitism and a mutation rate in (0, 1) it finds an optimum with probability 1, but with no general time bound.
solves: [global-optimization]
model: real-ram
complexity:
  vars: {n: the length of a string, N: the population size, g: the number of generations, c: the cost of one fitness evaluation}
  time: {worst: O(g N (n + c))}
  space: {extra: O(N n)}
properties: {deterministic: false, iterative: true, anytime: true, population: true}
history:
  year: 1975
  people: [John H. Holland]
  note: Holland set out the genetic algorithm and the schema analysis in his 1975 book Adaptation in Natural and Artificial Systems. Goldberg's 1989 book made the method widely known.
prereqs: [roulette-wheel-selection, tournament-selection, crossover, mutation, elitism]
see_also: [schema-theorem, building-block-hypothesis, genetic-programming, memetic-algorithm, evolution-strategies, differential-evolution, premature-convergence, no-free-lunch-theorem]
sources:
  - book: isbn:9780262581110
    title: John H. Holland, Adaptation in Natural and Artificial Systems, MIT Press edition, 1992 (first edition University of Michigan Press, 1975)
    locator: Chapters 6 and 7 (the reproductive plans, crossover and mutation)
  - book: isbn:9780201157673
    title: David E. Goldberg, Genetic Algorithms in Search, Optimization, and Machine Learning, Addison-Wesley, 1989
    locator: Chapter 1 (the simple genetic algorithm and the worked example with f(x) = x^2) and Chapter 2 (schemata)
  - book: isbn:9780262133166
    title: Melanie Mitchell, An Introduction to Genetic Algorithms, MIT Press, 1996
    locator: Chapter 1 (the elements of a genetic algorithm) and Chapter 5 (implementation choices)
  - paper: doi:10.1109/72.265964
    title: Günter Rudolph, Convergence analysis of canonical genetic algorithms, IEEE Transactions on Neural Networks 5(1), 1994
    locator: pages 96 to 101 (the canonical algorithm does not converge to the optimum; the elitist variant does)
  - paper: doi:10.1016/S0304-3975(01)00182-7
    title: Stefan Droste, Thomas Jansen and Ingo Wegener, On the analysis of the (1+1) evolutionary algorithm, Theoretical Computer Science 276(1-2), 2002
    locator: pages 51 to 81 (expected time Θ(n log n) on linear functions, OneMax included)
  - book: doi:10.1007/978-3-662-44874-8
    title: A. E. Eiben and J. E. Smith, Introduction to Evolutionary Computing, second edition, Springer, 2015
    locator: Chapter 6, Popular evolutionary algorithm variants, Section 6.1, Genetic algorithms
---

A genetic algorithm (GA) is a [population-based](/population-based-search/) [metaheuristic](/metaheuristic/) that keeps a set of candidate solutions, coded as bit strings, and makes each new generation from the old one by [selection](/roulette-wheel-selection/), [crossover](/crossover/) and [mutation](/mutation/). Holland introduced it in 1975 as a model of adaptation, and it is the best known member of [evolutionary computation](/evolutionary-computation/). With a mutation rate strictly between 0 and 1 and [elitism](/elitism/), it finds an optimum of a finite problem with probability tending to 1, but this guarantee says nothing about the time. Proved runtime bounds exist only for special algorithms and functions, such as the $(1+1)$ EA on OneMax, which takes expected $\Theta(n \log n)$ evaluations.

## In plain words

You want a string of zeros and ones that gets a high score, and all you can do is score strings. Start with a few random strings. Then build a new group of the same size. Pick two parents, and prefer the ones with good scores. Cut both parents at the same point and swap the ends, so that each child has a piece of each parent. Then change a few random positions of each child. Put the children in the new group, and repeat.

Good pieces of strings tend to spread, because good parents have more children. The random changes bring in values that no string in the group has. Copy the best string into the next group unchanged, so the best score never gets worse. Stop after a fixed number of rounds and report the best string you saw.

## The problem

The input is a length $n$ and a fitness function $f : \{0,1\}^n \to \mathbb{R}$, given as a black box (see [fitness function](/fitness-function/) and [black-box optimization](/black-box-optimization/)). The goal is a string $x^*$ with $f(x^*) = f^* = \max_x f(x)$. This is [global optimization](/global-optimization/) over a finite set with $2^n$ points. The parameters are the population size $N$, the crossover probability $p_c$, the mutation rate $p_m$, the number $e$ of elite strings and the number of generations $G$. A problem in other variables needs a coding into bit strings first. To minimize a cost, maximize its negative, or a positive decreasing function of it when roulette selection needs $f \ge 0$.

## The algorithm

SELECT is [tournament selection](/tournament-selection/) of size $k$ or [roulette wheel selection](/roulette-wheel-selection/). CROSSOVER is one-point [crossover](/crossover/) with a uniform cut point in $\{1, \ldots, n-1\}$. MUTATE flips each bit independently with probability $p_m$.

```pseudo id=main
GENETIC-ALGORITHM(f, n, N, p_c, p_m, e, G)
L1  P ← N strings drawn uniformly from {0,1}^n
L2  best ← a string of P with the largest f
L3  for t ← 1 to G do
L4      Q ← the e strings of P with the largest f       ▷ elitism, 0 ≤ e < N
L5      while |Q| < N do
L6          a ← SELECT(P), b ← SELECT(P)
L7          with probability p_c: (a, b) ← CROSSOVER(a, b)
L8          a ← MUTATE(a, p_m), b ← MUTATE(b, p_m)
L9          add a to Q, and add b to Q if |Q| < N
L10     P ← Q
L11     if the largest f in P exceeds f(best) then best ← a string of P with the largest f
L12 return best
```

Lines L4 to L9 make one generation. The elite strings of line L4 skip selection, crossover and mutation. The other places are filled by pairs of children of selected parents. Selection uses only the fitness values, and the variation steps of lines L7 and L8 use only the strings, so the method never looks inside $f$. The variable $best$ is the best string that the run has put in a population. The code below also stops early when $f(best)$ reaches a known target.

## Example

Maximize $f(x) = x^2$, where $x$ is the 5-bit string read as a binary number. This is the example of Goldberg's Chapter 1. Take $N = 4$, roulette selection, $p_c = 1$, $e = 0$, and assume that no bit flips in this generation.

| string | $x$ | $f(x)$ | share $f/\sum f$ | interval of the wheel |
|---|---|---|---|---|
| 01101 | 13 | 169 | 0.1444 | [0, 0.1444) |
| 11000 | 24 | 576 | 0.4923 | [0.1444, 0.6368) |
| 01000 | 8 | 64 | 0.0547 | [0.6368, 0.6915) |
| 10011 | 19 | 361 | 0.3085 | [0.6915, 1) |

The sum is 1170 and the mean is 292.5. Four spins with $u = 0.10, 0.40, 0.55, 0.85$ select 01101, 11000, 11000 and 10011. The string 01000 gets no child, and 11000 gets two.

| pair | cut | children | $f$ of the children |
|---|---|---|---|
| 01101, 11000 | 4 | 01100, 11001 | 144, 625 |
| 11000, 10011 | 2 | 11011, 10000 | 729, 256 |

The new mean is 438.5 and the new maximum is 729, against 292.5 and 576 before. The maximum $f^* = 961$ at 11111 is not yet in the population. The schema 1**** had 2 strings and now has 3. The [schema theorem](/schema-theorem/) page computes the exact expected count, 3.20 for $p_m = 0.001$.

## Correctness

A GA cannot certify that a string is optimal, so its correctness is a set of invariants and one limit statement. Line L4 and the test $|Q| < N$ keep $N$ strings of length $n$ in each population. Lines L2 and L11 keep $best$ equal to a best string seen so far. With $e \ge 1$, line L4 copies a best string of $P$ into $Q$, so the largest fitness of the population never decreases. If $0 < p_m < 1$, each mutated child equals any fixed string $y$ with probability at least $\delta = \min(p_m, 1 - p_m)^n > 0$, whatever its parents are. So the probability that no optimal string has appeared after $t$ generations is at most $(1 - \delta)^t$, which tends to 0. The full proof is below. Rudolph (1994) showed that the population of the GA without elitism does not converge to the optimum in the same sense: it is an irreducible Markov chain, so it loses an optimal string again with positive probability.

The bound $(1 - \delta)^t$ is a convergence statement, not a useful time bound. For $p_m = 1/n$ it gives $\delta = n^{-n}$, so it only says that the expected time is at most of the order of $n^n$ generations, which is far more than the $2^n$ evaluations of a full enumeration.

## Complexity

One generation selects $N$ parents, makes $N$ children with $O(n)$ work each for crossover and mutation, and evaluates $N$ new strings. Tournament selection costs $O(k)$ per parent. A roulette wheel costs $O(N)$ per spin with a linear scan, or $O(\log N)$ with a binary search on the prefix sums. So one generation costs $O(N(n + c))$ time with tournaments, and $G$ generations cost $O(G N (n + c))$. The two populations take $O(N n)$ space.

The number of generations needed to reach an optimum has no general bound beyond the convergence argument above, and the [no free lunch theorem](/no-free-lunch-theorem/) shows that no such bound can hold over all functions. The tight results that exist are for simple algorithms on simple functions:

- **The (1+1) EA on OneMax.** Keep one string $x$. Flip each bit with probability $1/n$ to get $y$, and keep $y$ if $f(y) \ge f(x)$. On OneMax, $f(x) = \sum_i x_i$, the expected number of iterations is $\Theta(n \log n)$. The upper bound $e n H_n \le e n (\ln n + 1)$ comes from the fitness levels, and the lower bound from the zeros that must each be flipped at least once. Droste, Jansen and Wegener (2002) proved $\Theta(n \log n)$ for every linear function with nonzero weights. The proof for OneMax is in the complexity proof below.
- **Crossover.** For some functions a GA with crossover is provably faster than any mutation-only algorithm of this kind, and for others it is slower. The [building block hypothesis](/building-block-hypothesis/) page gives the main results.

## Properties

- **Randomized and anytime.** Each run is random, and $best$ is a valid answer at any time.
- **Black box.** It uses $f$ only through evaluations, and selection uses only comparisons or ratios of the values.
- **Population-based.** It keeps $N$ strings. Selection makes the population lose diversity, and mutation adds it back. When the loss wins, the run stalls in a [premature convergence](/premature-convergence/).
- **Not invariant to scaling with roulette.** Adding a constant to $f$ changes roulette probabilities. Tournament selection uses only the order of the values, so it is invariant under any increasing transformation of $f$.

## Variants and improvements

- **Steady state GA.** Make one or two children per step and let them replace the worst strings. The [memetic algorithm](/memetic-algorithm/) page uses this form.
- **Other codings.** Real-valued genes with blend or simulated binary crossover, and permutations with order crossover, for problems such as the [traveling salesman problem](/traveling-salesman-problem/). The [crossover](/crossover/) page lists them.
- **Other selection schemes.** Rank selection, truncation selection and stochastic universal sampling. See [roulette wheel selection](/roulette-wheel-selection/) and [tournament selection](/tournament-selection/).
- **Hybrids.** Add a [local search](/local-search/) to each child to get a [memetic algorithm](/memetic-algorithm/).
- **Trees instead of strings.** [Genetic programming](/genetic-programming/) evolves programs with the same loop.
- **Model-based variants.** An [estimation of distribution algorithm](/estimation-of-distribution-algorithm/) replaces crossover and mutation by sampling from a probability model fitted to the selected strings.

## When to use it

Use a GA when $f$ is a black box, the solutions have a natural coding as strings, and a good solution found in the time you have is enough. When the problem has structure that an exact method can use, such as a linear program, a matroid or a small integer program, use the exact method. When a simple [local search](/local-search/) or [simulated annealing](/simulated-annealing/) with a good neighborhood works, it is often easier to tune than a GA. No metaheuristic is better than another over all problems, by the [no free lunch theorem](/no-free-lunch-theorem/), so compare methods on instances of your own problem.

## Pitfalls

- **Negative fitness with roulette.** Line L6 with a roulette wheel needs $f \ge 0$ and $\sum f > 0$. With a negative value the probabilities are not defined. Shift or rank the values, or use tournaments.
- **No elitism.** With $e = 0$ in line L4, the best string of a generation can be lost. Return $best$ (line L12), not the best of the last population, and use $e \ge 1$ when the best of the population must not get worse.
- **Mutation rate 0.** With $p_m = 0$ in line L8, a position where all strings hold the same bit never changes again, and the optimum may become unreachable. Use $p_m > 0$, usually about $1/n$.
- **Reading the schema theorem as a speed guarantee.** The schema theorem is an inequality about one generation in expectation. It does not show that a GA finds good strings fast.
- **Comparing on a few runs.** A GA is random. Report the number of runs, the seeds and the spread of the results, not one run.

## Implementations

## History

Holland developed the genetic algorithm at the University of Michigan in the 1960s and published it, with the schema analysis, in his 1975 book. De Jong's 1975 thesis, supervised by Holland, studied the method on a set of test functions. Goldberg's 1989 book made the method widely known and gave the form with roulette selection, one-point crossover and bit-flip mutation that is now called the simple genetic algorithm. Rudolph (1994) gave the Markov chain analysis of convergence with and without elitism. Rigorous runtime analysis started in the 1990s with simple algorithms such as the $(1+1)$ EA, and Droste, Jansen and Wegener (2002) gave the $\Theta(n \log n)$ bound for linear functions.

## References
