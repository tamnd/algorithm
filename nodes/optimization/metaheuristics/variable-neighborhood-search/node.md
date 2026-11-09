---
tag: WPXWMK
kind: algorithm
slug: variable-neighborhood-search
name: Variable neighborhood search
aliases:
- VNS
- variable neighbourhood search
- variable neighborhood descent
area: optimization/metaheuristics
level: advanced
summary: Systematically change the neighborhood structure when the search stagnates.
model: word-ram
complexity:
  vars: {K: the number of iterations, H: the time of one run of the local search, s: the size of one solution}
  time: {worst: O((K + 1) H)}
  space: {extra: O(s)}
properties: {deterministic: false, recursive: false}
prereqs: [local-search, neighborhood-structure, local-optimum, hill-climbing]
see_also: [iterated-local-search, neighborhood-structure, maximum-cut, large-neighborhood-search, hamming-distance, random-restart-hill-climbing, intensification-and-diversification, metaheuristic]
sources:
  - paper: doi:10.1016/S0305-0548(97)00031-2
    title: Nenad Mladenović and Pierre Hansen, Variable neighborhood search, Computers and Operations Research 24(11), 1997
    locator: pp. 1097 to 1100 (the original method, with shaking in nested neighborhoods)
  - paper: doi:10.1016/S0377-2217(00)00100-4
    title: Pierre Hansen and Nenad Mladenović, Variable neighborhood search, Principles and applications, European Journal of Operational Research 130(3), 2001
    locator: pp. 449 to 467 (basic VNS, variable neighborhood descent, reduced VNS, and the three facts behind the method)
  - book: isbn:9783319910857
    title: Michel Gendreau and Jean-Yves Potvin (editors), Handbook of Metaheuristics, third edition, Springer, 2019
    locator: Chapter 3, Variable Neighborhood Search, by Pierre Hansen, Nenad Mladenović, Jack Brimberg and José A. Moreno Pérez, from p. 57
  - book: isbn:9781558608726
    title: Holger H. Hoos and Thomas Stützle, Stochastic Local Search, Foundations and Applications, Morgan Kaufmann, 2004
    locator: Section 2.1, Iterative Improvement (Revisited), pp. 61 to 70 (variable neighbourhood descent), and Section 2.3, Hybrid SLS Methods, from p. 85
---

Variable neighborhood search (VNS) is a [metaheuristic](/metaheuristic/) that uses several [neighborhoods](/neighborhood-structure/) of different sizes, and changes the neighborhood when the search does not improve. From the current [local optimum](/local-optimum/) $x$ it jumps to a random solution in the $k$-th neighborhood of $x$ (the *shaking* step), runs a [local search](/local-search/), and moves to the result if it is better. After a success it goes back to the smallest neighborhood, $k = 1$; after a failure it tries the next larger one. Mladenović and Hansen introduced it in 1997. Its local search is often *variable neighborhood descent* (VND), which also cycles through neighborhoods and ends at a local optimum of all of them. VNS has no guarantee of reaching a global optimum.

## In plain words

A walker stands in a hollow. First the walker takes a short random hop and walks downhill again. If this leads to a lower hollow, the walker moves there and starts again with short hops. If not, the walker comes back and tries a longer hop, then a longer one, up to some limit.

The idea is that a lower hollow is often close, so try close first. Only when close tries fail, look further away. And a spot that is lowest among its close neighbors may not be lowest among the neighbors two steps away, so the descent itself also checks more than one kind of step.

## The problem

The input is a finite set $S$ of solutions, an objective $f : S \to \mathbb{R}$ to minimize, nested neighborhoods $N_1, \ldots, N_{k_{\max}}$ for shaking (for bit strings, $N_k(x)$ is the set of strings at [Hamming distance](/hamming-distance/) $k$ from $x$), a local search procedure, a start $x_0$ and a number of iterations $K$. The output is the best local minimum found. The aim is a global minimum, which VNS cannot prove it has found.

## The algorithm

```pseudo id=main
VNS(x0, f, N1..Nkmax, LOCAL-SEARCH, K)
L1  x ← LOCAL-SEARCH(x0)
L2  k ← 1
L3  for i ← 1 to K do
L4      y ← a random solution in N_k(x)                  ▷ shaking
L5      z ← LOCAL-SEARCH(y)
L6      if f(z) < f(x) then x ← z, k ← 1                 ▷ move, back to the first neighborhood
L7      else if k < kmax then k ← k + 1 else k ← 1        ▷ next neighborhood
L8  return x
```

Line L4 picks a random point in the $k$-th neighborhood of the current local minimum; a larger $k$ means a larger jump. Line L5 descends from it. Line L6 moves only to a strictly better local minimum, so $x$ is always the best one found. Line L7 tries a larger jump after a failure and starts again from $k = 1$ after $k_{\max}$.

The usual local search is **variable neighborhood descent** (VND) with neighborhoods $M_1, \ldots, M_m$, often different from the shaking ones: look for the best improving neighbor in $M_1$; if there is one, move and stay at $M_1$; if not, try $M_2$, and so on; stop when no $M_j$ has an improving neighbor. VND ends at a solution that is a local minimum of every $M_j$.

## Example

Take [Max-Cut](/maximum-cut/) on eight vertices with these twelve weighted edges, total weight 53: $\{0,1\}$:1, $\{0,2\}$:5, $\{0,4\}$:5, $\{0,5\}$:7, $\{0,6\}$:2, $\{1,3\}$:6, $\{1,5\}$:6, $\{2,7\}$:6, $\{3,4\}$:3, $\{3,6\}$:7, $\{4,6\}$:1, $\{5,6\}$:4. A solution is a string $x \in \{0,1\}^8$ that puts each vertex on a side, and $f(x)$ is the uncut weight, the weight of the edges with both ends on one side. The local search is VND with $M_1$ = single flips and $M_2$ = flips of two vertices. Shaking flips $k$ random vertices, $k_{\max} = 3$.

From the start 00000000, with $f = 53$, VND makes four single flips, with $f$ going $53 \to 33 \to 17 \to 11 \to 8$, and stops at 10010101 with $f = 8$: no single flip and no double flip improves it. With the random generator `random.Random(1)` of the Python code:

| $i$ | $k$ | shaken $y$ | $f(y)$ | local min $z$ | $f(z)$ | move |
|---|---|---|---|---|---|---|
| 1 | 1 | 10110101 | 19 | 10010101 | 8 | no |
| 2 | 2 | 11110101 | 32 | 10010101 | 8 | no |
| 3 | 3 | 11000111 | 23 | 11000011 | 6 | yes |
| 4 | 1 | | | 11000011 | 6 | no |

Shakes with $k = 1$ and $k = 2$ fall back into the same local minimum. The shake with $k = 3$ lands in another basin, and VND reaches 11000011 with $f = 6$, which cuts 47 of the 53. Enumeration of all 256 strings shows that 6 is the optimum.

The example also shows why VND uses two neighborhoods. Up to swapping the two sides, this instance has three local minima for single flips, with $f$ = 6, 8 and 11, but only two that are also local minima for double flips, with $f$ = 6 and 8. The single-flip local minimum 11100010 with $f = 11$ has the double-flip neighbor 11000011 with $f = 6$.

## Correctness

VNS has no optimality guarantee, so "correct" means the following. VND stops, because each move lowers $f$ and $S$ is finite, and it ends at a local minimum of every neighborhood it uses: it stops only after it has tested all of them on the same solution. VNS stops after $K + 1$ runs of the local search; its current solution never gets worse, it is always a local minimum of all the descent neighborhoods, and it is the best local minimum returned during the run. The index $k$ follows the rule of lines L6 and L7. The [full proof](proofs/correctness.md) gives all steps.

Hansen and Mladenović base the method on three facts. A local minimum of one neighborhood need not be a local minimum of another. A global minimum is a local minimum of every neighborhood. And for many problems, local minima of different neighborhoods are close to each other. The first two are proved in one line each; the third is an observation about real instances, not a theorem.

## Complexity

Each iteration costs one shake and one run of the local search, so the time is $O((K + 1) H)$, where $H$ bounds the time of one run of the local search; a shake by $k$ flips costs $O(k)$ and is dominated. For VND with single and double flips on $n$ vertices, a full scan costs $O(n)$ and $O(n^2)$ evaluations of the change of $f$. The number of moves of a descent has no polynomial bound in general, as for [hill climbing](/hill-climbing/). The extra space is a constant number of solutions, $O(s)$.

## Properties

- **Systematic change of neighborhood.** The jump size grows after each failure and resets after each success, so the search stays near the current local minimum while it can improve there, and looks further away only when it cannot.
- **Few parameters.** Basic VNS needs the shaking neighborhoods, $k_{\max}$ and the local search.
- **Descent-only moves.** Basic VNS moves only to a better local minimum, so the current solution is the best one found.
- **Randomized.** The shaking step is random. VND alone is deterministic.
- **No general guarantee.** The result is a local minimum of the descent neighborhoods, not proved global.

## Variants and improvements

- **Variable neighborhood descent.** The deterministic descent through several neighborhoods, used alone or as the local search inside VNS.
- **Reduced VNS.** Skip the local search: shake and accept if the shaken solution is better. Useful when the descent is very expensive.
- **Skewed VNS.** Accept a slightly worse local minimum if it is far from the current one, which helps on landscapes where good local minima are far apart.
- **General VNS.** VNS whose local search is VND, as in this page.
- **Relation to iterated local search.** Basic VNS is an [iterated local search](/iterated-local-search/) whose kick size changes by the rule of lines L6 and L7.
- **Larger neighborhoods.** [Large neighborhood search](/large-neighborhood-search/) uses one very large neighborhood explored by an exact or greedy repair, not a sequence of growing ones.

## When to use it

Use VNS when the problem has a natural family of neighborhoods of growing size, such as flipping $k$ bits, moving $k$ customers or changing $k$ edges, and a cheap local search for the smaller ones. It has few parameters, which makes it easy to apply to a new problem. The Handbook chapter reports many uses on location, clustering and routing problems. On the 10-vertex Max-Cut instance of the [random restart](/random-restart-hill-climbing/) page (optimum 25), single flips have eight local minima with $f$ = 25, 26 and 30, but the four strings that are local minima of both single and double flips all have $f = 25$, so VND alone from 0000000000 finds the optimum. On such an instance the second neighborhood, not the shaking, does the work.

## Pitfalls

- **Neighborhoods that are not nested.** Shaking assumes that $N_{k+1}$ jumps further than $N_k$. If not, the order of the neighborhoods has no meaning.
- **A $k_{\max}$ that is too large.** A shake by close to $n$ flips is a random restart. In Max-Cut, flipping all $n$ vertices gives the same cut, so $k = n$ wastes the iteration.
- **Comparing with the shaken solution.** Line L6 compares the local minimum $z$ with $x$, not the shaken $y$; $y$ is almost always worse.
- **VND that stops too early.** VND must go back to $M_1$ after each move. If it continues with $M_2$, the result is not always a local minimum of $M_1$.

## Implementations

## History

Mladenović and Hansen introduced variable neighborhood search in 1997, and Hansen and Mladenović gave a full account in 2001, with basic, reduced, skewed and general VNS and variable neighborhood descent. The chapter by Hansen, Mladenović, Brimberg and Moreno Pérez in the Handbook of Metaheuristics reviews later variants and uses.

## References
