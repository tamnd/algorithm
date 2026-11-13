---
tag: THR7VX
kind: problem
slug: burnt-pancake-problem
name: Burnt pancake problem
aliases:
- Burnt pancake sorting
area: games-and-search/puzzles
level: advanced
summary: "Sort a stack of pancakes, each burnt on one side, by flips of a top part of the stack so that all burnt sides end down; the worst case g(n) satisfies 3n/2 <= g(n) <= 2n - 2 for n >= 10."
prereqs: [pancake-sorting, breadth-first-search]
see_also: [pancake-sorting, pancake-sort, sorting-by-reversals, breakpoint-distance, np-hard, symmetric-group, implicit-graph, state-space]
sources:
  - paper: doi:10.1016/0012-365X(79)90068-2
    title: "William H. Gates and Christos H. Papadimitriou, Bounds for sorting by prefix reversal, Discrete Mathematics 27(1), 1979"
    locator: "pp. 47-57; the burnt problem and the bounds 3n/2 - 1 <= g(n) <= 2n + 3"
  - paper: doi:10.1016/0166-218X(94)00009-3
    title: "David S. Cohen and Manuel Blum, On the problem of sorting burnt pancakes, Discrete Applied Mathematics 61(2), 1995"
    locator: "pp. 105-120; 3n/2 <= g(n) <= 2n - 2 for n >= 10, and the conjecture that -I_n is the hardest stack"
  - paper: doi:10.1016/j.tcs.2010.11.028
    title: "Josef Cibulka, On average and highest number of flips in pancake sorting, Theoretical Computer Science 412(8-10), 2011"
    locator: "pp. 822-834; the bounds on the flips for -I_n, the average case, and g(15) = 25"
  - paper: doi:10.1016/j.tcs.2010.11.004
    title: "Anthony Labarre and Josef Cibulka, Polynomial-time sortable stacks of burnt pancakes, Theoretical Computer Science 412(8-10), 2011"
    locator: "pp. 695-702"
  - paper: "Laurent Bulteau, Guillaume Fertin and Irena Rusu, Pancake flipping is hard, Journal of Computer and System Sciences 81(8), 2015"
    locator: "pp. 1556-1574; NP-hardness of the unburnt problem, with the burnt problem left open"
  - url: "https://oeis.org/A078941"
    locator: "OEIS A078941, the burnt pancake numbers g(n), with A078942 for the stack -I_n"
---

The burnt pancake problem asks for the fewest flips that sort a stack of $n$ pancakes of different sizes, each burnt on one side, into order with every burnt side down; a flip turns over the top part of the stack. It is the signed version of [pancake sorting](/pancake-sorting/): a stack is a signed permutation, and a flip reverses a prefix and changes the signs in it. The worst case $g(n)$ satisfies $3n/2 \le g(n) \le 2n - 2$ for $n \ge 10$ (Cohen and Blum 1995), and OEIS A078941 lists its exact values for $n \le 17$. The unburnt problem is [NP-hard](/np-hard/), but the complexity of a shortest burnt sort was still open when that hardness proof appeared in 2015.

## In plain words

You have a stack of pancakes of different sizes, and each pancake has a burnt side. You want the stack ordered from small on top to large at the bottom, with every burnt side facing down. Your only tool is a spatula: you slide it under any pancake and flip everything above it in one go. That reverses the order of those pancakes and also turns each of them over. So each pancake has to reach the right place and face the right way. The question is how many flips you need for the worst stack. A simple method uses about three flips per pancake. Cleverer methods need about two, and some stacks need at least one and a half per pancake.

## Definition

**Stacks.** A stack of $n$ burnt pancakes is a signed permutation $\pi = (\pi_1, \dots, \pi_n)$, listed from the top: each of $1, \dots, n$ occurs once as $+k$ (burnt side down) or $-k$ (burnt side up). There are $2^n n!$ stacks. The goal is the identity $I_n = (1, 2, \dots, n)$, and $-I_n = (-1, -2, \dots, -n)$ is the sorted stack with every pancake upside down.

**Flips.** For $1 \le i \le n$, the flip $\rho_i$ maps
$$(\pi_1, \dots, \pi_i, \pi_{i+1}, \dots, \pi_n) \mapsto (-\pi_i, \dots, -\pi_1, \pi_{i+1}, \dots, \pi_n).$$
Unlike in the unburnt problem, $\rho_1$ is not trivial: it turns the top pancake over.

**Problem.** Given $\pi$, find the least number $d(\pi)$ of flips that turn it into $I_n$, and such a sequence. The *burnt pancake number* is $g(n) = \max_\pi d(\pi)$.

**The burnt pancake graph.** Every flip is its own inverse, so the flips generate the group of signed permutations, of order $2^n n!$, and its Cayley graph with the $n$ flips as generators is an undirected $n$-regular graph. Then $d(\pi)$ is the distance from $\pi$ to $I_n$, and $g(n)$ is the diameter of this graph, since the graph is vertex-transitive.

## Variants

- **Unburnt pancakes.** Without signs this is [pancake sorting](/pancake-sorting/), whose worst case is between $15n/14$ and $18n/11 + O(1)$ and whose decision version is NP-hard; the simple method is [pancake sort](/pancake-sort/).
- **The stack $-I_n$.** Cohen and Blum conjectured that $-I_n$ is always the hardest stack. Cibulka showed $\lfloor (3n + 3)/2 \rfloor \le d(-I_n) \le \lfloor (3n + 3)/2 \rfloor + 2$ for $n \ge 2$, and that the conjecture fails at $n = 15$, where $d(-I_{15}) = 24$ but $g(15) = 25$.
- **Average case.** Cibulka gives a method that uses about $7n/4$ flips on average and shows that every method needs $n + \Omega(n/\log n)$ flips on average.
- **Arbitrary reversals.** If any segment, not only a top part, may be reversed with its signs changed, the problem becomes sorting signed permutations by reversals, which [is solvable in polynomial time](/sorting-by-reversals/). Only the prefix version is open.
- **Easy classes.** Labarre and Cibulka sort the stacks of a class called simple permutations optimally in polynomial time and prove a new lower bound.

## Examples

**Two pancakes, both burnt side up.** The stack $(-1, -2)$ needs 4 flips, the most for $n = 2$:

| flip | stack after it |
|---|---|
| | $(-1, -2)$ |
| $\rho_2$ | $(2, 1)$ |
| $\rho_1$ | $(-2, 1)$ |
| $\rho_2$ | $(-1, 2)$ |
| $\rho_1$ | $(1, 2)$ |

**Exact values from a full search.**

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| stacks $2^n n!$ | 2 | 8 | 48 | 384 | 3840 | 46,080 | 645,120 |
| $g(n)$ | 1 | 4 | 6 | 8 | 10 | 12 | 14 |
| $d(-I_n)$ | 1 | 4 | 6 | 8 | 10 | 12 | 14 |
| stacks at distance $g(n)$ | 1 | 1 | 2 | 3 | 4 | 1 | 1 |
| average $d(\pi)$ | 0.5 | 2.0 | 3.44 | 4.80 | 6.12 | 7.40 | 8.65 |

For $n = 3$ the two hardest stacks are $(-1, -2, -3)$ and $(1, -2, -3)$. OEIS A078941 continues the sequence $g(n)$ with 15, 17, 18, 19, 21, 22, 23, 25, 26, 28 for $n = 8, \dots, 17$. So $g(n) = 2n$ for $2 \le n \le 7$, and the bound $2n - 2$ fails for $n = 8$ and $9$; it needs $n \ge 10$.

## Known algorithms

- **Simple method, at most $3n - 2$ flips.** For $k = n, n - 1, \dots, 1$, if pancake $k$ is not already at position $k$ with its burnt side down, flip it to the top (one flip unless it is there), turn it burnt side up with $\rho_1$ if needed, and flip the top $k$ pancakes, which puts it at position $k$ burnt side down. The last pancake needs at most one flip, so the total is at most $3(n - 1) + 1$, and some stacks need all of them under this method.
- **Cohen and Blum.** Their algorithm uses at most $2n - 2$ flips for $n \ge 10$.
- **Exact search.** A [breadth-first search](/breadth-first-search/) of the [implicit graph](/implicit-graph/) from $I_n$ gives $d(\pi)$ for all $2^n n!$ stacks at once, because flips are involutions. With stacks stored as tuples it costs $O(2^n n! \cdot n^2)$ time, and a hash table of all stacks fits in memory up to about $n = 8$. Larger $n$ need disk-based search or a search from one stack at a time.
- **Heuristic search.** Put a pancake $n + 1$ below the stack and call a pair of neighbours $(\pi_i, \pi_{i+1})$ a breakpoint when $\pi_{i+1} \ne \pi_i + 1$. A flip $\rho_i$ maps a pair $(a, b)$ inside the flipped part to $(-b, -a)$, and $b = a + 1$ exactly when $-a = -b + 1$, so only the pair at the cut can change. So each flip changes the number of breakpoints by at most 1, and $d(\pi) \ge$ the number of breakpoints. This is an admissible heuristic for IDA* or A*, as in the [breakpoint distance](/breakpoint-distance/) of the unburnt problem.

## Bounds

- **Lower bound.** $g(n) \ge 3n/2$ for $n \ge 2$ (Cohen and Blum), improving $3n/2 - 1$ of Gates and Papadimitriou. The breakpoint count alone gives only $g(n) \ge n$, since $-I_n$ has $n$ breakpoints.
- **Upper bound.** $g(n) \le 2n - 2$ for $n \ge 10$ (Cohen and Blum), improving $2n + 3$ of Gates and Papadimitriou. The simple method gives $3n - 2$.
- **The stack $-I_n$.** $\lfloor (3n + 3)/2 \rfloor \le d(-I_n) \le \lfloor (3n + 3)/2 \rfloor + 2$ for $n \ge 2$ (Cibulka), with equality on the left when $n \equiv 3 \pmod 4$ and $n \ne 7, 11$.
- **Relation to the unburnt problem.** Forgetting the signs maps any burnt solution of a stack with all signs $+$ to an unburnt solution, so the unburnt distance of a permutation is at most its burnt distance, and the unburnt pancake number is at most $g(n)$.
- **Complexity.** Bulteau, Fertin and Rusu proved the unburnt problem NP-hard in 2015 and noted that the complexity of the burnt problem was still open. A polynomial algorithm is known only for special classes, such as the simple permutations of Labarre and Cibulka.

## Reductions

- **From unburnt pancakes.** The [pancake sorting](/pancake-sorting/) page gives the reduction that places each pancake burnt side down.
- **Group distance.** The problem asks for a shortest word in the generators $\rho_1, \dots, \rho_n$ for an element of the group of signed permutations, the same shape as the distance problems of the [Rubik's cube](/rubiks-cube-problem/) and the [sliding tile puzzle](/sliding-tile-puzzle/) in their [state spaces](/state-space/).
- **To unrestricted reversals.** Allowing all segment reversals relaxes the problem, so the signed reversal distance of [sorting by reversals](/sorting-by-reversals/) is a lower bound on $d(\pi)$, and it is computable in linear time.

## Applications

- Genome rearrangement: a stack models a chromosome whose genes have an order and a strand, and a flip models a reversal at one end.
- Interconnection networks: the burnt pancake graph has $2^n n!$ vertices but degree only $n$ and diameter at most $2n - 2$ for $n \ge 10$, the kind of trade-off a network topology needs.
- A test domain for heuristic search, with exact values known for small $n$ and a simple admissible heuristic.

## References
