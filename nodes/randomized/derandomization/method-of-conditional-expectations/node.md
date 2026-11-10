---
tag: C5T3W4
kind: technique
slug: method-of-conditional-expectations
name: Method of conditional expectations
aliases:
- method of conditional probabilities
- conditional probabilities method
- derandomization by conditional expectations
area: randomized/derandomization
level: intro
summary: Fixes random choices one at a time, each time picking the value that keeps the conditional expectation of the objective at least as good.
prereqs: [linearity-of-expectation, conditional-expectation, probabilistic-method]
see_also: [pessimistic-estimators, sample-space-reduction, maximum-cut, max-sat, random-assignment-max-3-sat, k-wise-independence, randomized-rounding, greedy-algorithm]
sources:
  - book: isbn:9781119061953
    title: Noga Alon and Joel H. Spencer, The Probabilistic Method, fourth edition, Wiley, 2016
    locator: Chapter 16, Section 16.1 (the method of conditional probabilities)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition, Cambridge University Press, 2017
    locator: Chapter 6, Section 6.3 (derandomization using conditional expectations, for a large cut)
  - paper: doi:10.1561/0400000010
    title: Salil P. Vadhan, Pseudorandomness, Foundations and Trends in Theoretical Computer Science 7(1-3), 2012
    locator: Chapter 3, Section 3.4 (the method of conditional expectations, for MAX-CUT)
  - paper: doi:10.1016/0097-3165(73)90005-8
    title: Paul Erdős and John L. Selfridge, On a combinatorial game, Journal of Combinatorial Theory, Series A 14(3), 1973
    locator: pages 298 to 301 (the potential function argument for the Maker-Breaker game)
  - book: isbn:9780898713251
    title: Joel Spencer, Ten Lectures on the Probabilistic Method, second edition, SIAM, 1994
    locator: Lecture 4, Large deviations and nonprobabilistic algorithms (pages 29 to 35)
  - paper: doi:10.1016/0022-0000(88)90003-7
    title: Prabhakar Raghavan, Probabilistic construction of deterministic algorithms, approximating packing integer programs, Journal of Computer and System Sciences 37(2), 1988
    locator: pages 130 to 143 (conditional probabilities and pessimistic estimators)
  - paper: doi:10.1016/S0022-0000(74)80044-9
    title: David S. Johnson, Approximation algorithms for combinatorial problems, Journal of Computer and System Sciences 9(3), 1974
    locator: pages 256 to 278 (the greedy MAX-SAT algorithm with ratio 1 − 2^(−k) for clauses of at least k literals)
---

The method of conditional expectations turns a proof by the [probabilistic method](/probabilistic-method/) into a deterministic algorithm. If a random object $X = (X_1, \ldots, X_n)$ has $\mathrm{E}[f(X)] \ge \mu$, then some value of $X_1$ keeps the [conditional expectation](/conditional-expectation/) at least $\mu$, then some value of $X_2$ does the same, and so on, until every coordinate is fixed and $f(x) \ge \mu$ holds for the fixed object $x$. The method needs only one thing: a fast way to compute the conditional expectations. It gives a cut with at least half the edges for [maximum cut](/maximum-cut/) and an assignment that satisfies at least $7/8$ of the clauses of an exact 3-CNF formula for [MAX-SAT](/max-sat/).

## In plain words

A random choice is good on average. So among the possible values of the first coin, at least one value is as good as the average of the rest of the game. You do not need luck to find it: you compute, for each value of the first coin, how good the outcome is on average when the other coins are still random, and you keep the best value. Then you do the same for the second coin, and so on.

The average never goes down, because the current average is a mix of the averages after each choice, and the largest part of a mix is at least the mix. When all coins are fixed, nothing is random, and the result is at least the average you started with. The work is in computing those averages fast.

## When it applies

Use it when all of these hold:

- A randomized argument shows $\mathrm{E}[f(X)] \ge \mu$ (or $\mathrm{E}[g(X)] < 1$ for a count $g$ of bad events, to show that a good object exists).
- The random object is a sequence $X_1, \ldots, X_n$ of choices, each from a small set $S$ of values, in practice independent bits or values.
- For each prefix $x_1, \ldots, x_i$, the number $\mathrm{E}[f(X) \mid X_1 = x_1, \ldots, X_i = x_i]$ can be computed exactly in polynomial time. With [linearity of expectation](/linearity-of-expectation/), this is often a sum of simple terms, one for each edge or clause.

If the conditional expectation is hard to compute, but an upper bound on a failure probability is easy to compute and has the same averaging property, use [pessimistic estimators](/pessimistic-estimators/) instead. If the analysis uses only [k-wise independence](/k-wise-independence/), the other route is [sample space reduction](/sample-space-reduction/): try every point of a small sample space.

Notation. $\Pr$ and $\mathrm{E}$ are probability and expectation over the random choices. $n$ is the number of choices, $S$ the set of values of one choice, and $\mu = \mathrm{E}[f(X)]$.

## The template

```pseudo id=main
CONDITIONAL-EXPECTATIONS(f, n, S)       ▷ X_1, …, X_n random, values in S
L1  for i ← 1 to n do
L2      best ← −∞
L3      for each v in S do
L4          e ← E[f(X) | X_1 = x_1, …, X_{i−1} = x_{i−1}, X_i = v]
L5          if e > best then best ← e, x_i ← v
L6  return x = (x_1, …, x_n)
```

**Claim.** Let $X_1, \ldots, X_n$ have any joint distribution on $S^n$ with $S$ finite, let $f$ be real valued, and let line L4 range over the values $v$ with $\Pr[X_i = v \mid X_1 = x_1, \ldots, X_{i-1} = x_{i-1}] > 0$. Then the returned $x$ has $f(x) \ge \mathrm{E}[f(X)]$.

*Proof.* Write $g_i = \mathrm{E}[f(X) \mid X_1 = x_1, \ldots, X_i = x_i]$ for the prefix chosen by the end of step $i$, so $g_0 = \mathrm{E}[f(X)]$. By the law of total expectation,

$$g_{i-1} = \sum_{v} \Pr[X_i = v \mid X_1 = x_1, \ldots, X_{i-1} = x_{i-1}] \cdot \mathrm{E}[f(X) \mid X_1 = x_1, \ldots, X_{i-1} = x_{i-1}, X_i = v].$$

The weights are nonnegative and sum to 1, so the largest term $\mathrm{E}[\cdot \mid \ldots, X_i = v]$ is at least $g_{i-1}$. Line L5 keeps a value $v$ with the largest term, so $g_i \ge g_{i-1}$. By induction, $g_n \ge g_0$. After step $n$ every coordinate is fixed, so $g_n = f(x)$. $\square$

The chosen value of line L5 never has conditional probability 0 when the coordinates are independent and each value of $S$ has positive probability, which is the usual case. Any value with $e \ge g_{i-1}$ can replace the best one; the proof uses only $g_i \ge g_{i-1}$.

**Cost.** The loop does $n |S|$ evaluations of line L4. If one evaluation costs $C$, the total time is $O(n |S| C)$. Often the change of the conditional expectation from one step to the next is local, and an incremental update makes the total time linear in the size of the input.

## Classic examples

### Maximum cut with at least half the edges

Let $G = (V, E)$ have $n$ vertices and $m$ edges. Put each vertex on side 0 or side 1 with an independent fair coin. An edge is cut with probability $1/2$, so $\mathrm{E}[\text{cut}] = m/2$. Given the sides of some vertices,

$$\mathrm{E}[\text{cut} \mid \text{fixed sides}] = (\text{cut edges with both ends fixed}) + \tfrac{1}{2} (\text{edges with an end not fixed}).$$

When vertex $v$ gets its side, only the edges from $v$ to already fixed neighbours change their term, from $1/2$ to 0 or 1. So the rule of line L5 is: put $v$ on the side opposite to the majority of its fixed neighbours. This is the greedy algorithm, and the claim proves that it cuts at least $m/2$ edges. Since no cut has more than $m$ edges, this is a [2-approximation](/approximation-ratio/) for [maximum cut](/maximum-cut/). It runs in $O(n + m)$ time.

Trace on the graph with vertices 0 to 4 and the 7 edges 01, 02, 12, 13, 23, 24, 34, with ties broken toward side 0:

| step | vertex | E if side 0 | E if side 1 | choice |
|---|---|---|---|---|
| 1 | 0 | 7/2 | 7/2 | 0 |
| 2 | 1 | 3 | 4 | 1 |
| 3 | 2 | 4 | 4 | 0 |
| 4 | 3 | 4 | 4 | 0 |
| 5 | 4 | 3 | 5 | 1 |

The result is the cut $\{1, 4\}$ against $\{0, 2, 3\}$, with 5 cut edges: 01, 12, 13, 24 and 34. The start value was $7/2$, and 5 is also the maximum for this graph.

### MAX-3SAT with at least 7/8 of the clauses

Let $\varphi$ have $m$ clauses, each with exactly 3 literals on 3 different variables. Set each variable true with an independent fair coin, as in [the random assignment algorithm](/random-assignment-max-3-sat/). A clause fails only when all 3 literals are false, with probability $1/8$, so $\mathrm{E}[\text{satisfied}] = 7m/8$. Given a partial assignment, a clause contributes

$$\begin{cases} 1 & \text{if a fixed literal is true,} \\ 1 - 2^{-r} & \text{otherwise, where } r \text{ is the number of its literals not yet fixed.} \end{cases}$$

(If $r = 0$ and no literal is true, the term is 0.) The claim gives an assignment with at least $7m/8$ satisfied clauses. Each clause has an integer count, so at least $\lceil 7m/8 \rceil$ are satisfied. For a formula with clauses of any length $k_j \ge 1$ on distinct variables, the same steps give at least $\sum_j (1 - 2^{-k_j}) \ge m/2$ satisfied clauses. Johnson (1974) gave a greedy algorithm with this guarantee, the ratio $1 - 2^{-k}$ when each clause has at least $k$ literals.

Trace with 4 variables and 8 clauses, ties broken toward false:

$C_1 = x_1 \lor x_2 \lor x_3$, $C_2 = \lnot x_1 \lor x_2 \lor x_4$, $C_3 = \lnot x_1 \lor \lnot x_3 \lor \lnot x_4$, $C_4 = \lnot x_2 \lor x_3 \lor \lnot x_4$, $C_5 = x_1 \lor \lnot x_2 \lor x_4$, $C_6 = x_1 \lor \lnot x_3 \lor x_4$, $C_7 = \lnot x_2 \lor \lnot x_3 \lor x_4$, $C_8 = \lnot x_1 \lor \lnot x_2 \lor x_3$.

| step | variable | E if false | E if true | choice |
|---|---|---|---|---|
| start | | | | E = 7 |
| 1 | $x_1$ | 7 | 7 | false |
| 2 | $x_2$ | 29/4 | 27/4 | false |
| 3 | $x_3$ | 7 | 15/2 | true |
| 4 | $x_4$ | 7 | 8 | true |

The value after step 1 is 7, after step 2 it is $29/4$, after step 3 it is $15/2$, and the final assignment satisfies all 8 clauses. The values never go down, as the claim says.

### The Erdős-Selfridge game

Erdős and Selfridge (1973) used the same averaging for a game. Two players take turns to claim vertices of a hypergraph. Maker wins by claiming all vertices of some edge. Their potential, the sum of $2^{-r}$ over the edges that Breaker has not touched, with $r$ the number of unclaimed vertices of the edge, is the expected number of edges that Maker would fill if the free vertices were shared at random. Breaker plays so that this potential never grows. When every edge has $k$ vertices and there are fewer than $2^{k-1}$ edges, Breaker, who moves second, wins. This is an early use of the expectation as a potential that guides a deterministic strategy.

### Other uses

- **Set balancing and packing.** Raghavan (1988) derandomized randomized rounding of packing integer programs. The failure probability there is not computable exactly, so he used an upper bound with the same averaging property. See [pessimistic estimators](/pessimistic-estimators/).
- **Balancing games.** Spencer (Lecture 4 of the 1994 edition) uses the same potentials to turn large deviation bounds into deterministic strategies and algorithms.

## Variations

- **Conditional probabilities.** Take $f$ to be the indicator of a bad event, or a sum of such indicators, and keep the conditional value *below* 1 instead of above $\mu$. At the end the value is an integer below 1, so it is 0 and no bad event happens. This is the form in Alon and Spencer.
- **Pessimistic estimators.** Replace the exact conditional value by an upper bound $U$ on it that can be computed and that cannot increase under the best choice. See [pessimistic estimators](/pessimistic-estimators/).
- **Conditional expectations over a small space.** If the analysis needs only pairwise or [k-wise independence](/k-wise-independence/), the choices can be the seed bits of a small sample space. There are $O(\log n)$ seed bits in place of $n$ choices, and each step can test its values in parallel. Luby (1986) and others used this for parallel algorithms. See [sample space reduction](/sample-space-reduction/).
- **Weights.** For weighted maximum cut or weighted MAX-SAT, use the weighted sum as $f$. The proof does not change.

## Pitfalls

- **The result is not optimal.** The method guarantees the expectation, not the optimum. On the path with edges 03, 34, 45, 52, 21, processed in the order 0 to 5 with ties toward side 0, the greedy cut has 4 edges, but the path is bipartite and has a cut of all 5 edges.
- **The conditional expectation must be exact.** An estimate by sampling, or a rounded value, can choose a value with a smaller conditional expectation, and then the claim fails. Use integers (scale MAX-3SAT terms by 8) or exact fractions; floating point ties are a common source of wrong choices.
- **Repeated variables change the expectation.** The bound $7/8$ needs 3 literals on 3 different variables. The clause $x \lor x \lor y$ is satisfied with probability $3/4$, and $x \lor \lnot x \lor y$ always. Compute each term from the clause as it is.
- **Dependent choices.** If the $X_i$ are not independent, the conditional distribution of $X_i$ depends on the prefix, and line L4 must use it. A value with conditional probability 0 must not be chosen, because its conditional expectation is not defined.
- **Hard conditional expectations.** For a property such as "every row sum is small", the exact conditional probability is a sum over exponentially many completions. Do not try to compute it; use a pessimistic estimator.

## Exercises

1. Show that the greedy cut algorithm of this page, run on a graph where every vertex has odd degree, cuts strictly more than $m/2$ edges.
2. Give a formula with clauses of exactly 3 literals on distinct variables in which no assignment satisfies more than $\lceil 7m/8 \rceil$ clauses. (Hint: all 8 sign patterns on the same 3 variables.)
3. Apply the method to the bound that a graph with $m$ edges has a bipartite subgraph with at least $m/2$ edges, but with three sides instead of two, and find the guarantee for a 3-cut.
4. A $k$-uniform hypergraph has fewer than $2^{k-1}$ edges. Use conditional expectations to 2-colour its vertices in polynomial time so that no edge has one colour.

## References
