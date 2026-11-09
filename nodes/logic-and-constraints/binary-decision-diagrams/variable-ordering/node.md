---
tag: 3HNXB3
kind: problem
slug: variable-ordering
name: BDD variable ordering problem
aliases:
- variable order minimization
- BDD size minimization
- optimal variable order
- OBDD minimization
area: logic-and-constraints/binary-decision-diagrams
level: core
summary: Find the variable order with the smallest reduced ordered BDD. The size can change by an exponential factor with the order, and the decision version is NP-complete.
prereqs: [ordered-binary-decision-diagram, reduced-ordered-bdd, bdd-canonicity]
see_also: [variable-ordering-np-hardness, friedman-supowit-ordering, bdd-sifting, window-permutation-reordering, multiplier-bdd-lower-bound, hidden-weighted-bit-lower-bound, free-binary-decision-diagram, symbolic-model-checking]
sources:
  - book: isbn:9780898714586
    title: Ingo Wegener, Branching Programs and Binary Decision Diagrams, Theory and Applications, SIAM, 2000
    locator: Chapter 5, The variable-ordering problem; Chapter 4, The OBDD size of selected functions
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms Part 1, 2011
    locator: Section 7.1.4, Binary decision diagrams (the effect of the order, and reordering by swaps of adjacent levels)
  - paper: doi:10.1109/TC.1986.1676819
    title: Randal E. Bryant, Graph-based algorithms for Boolean function manipulation, IEEE Transactions on Computers C-35(8), 1986, pages 677 to 691
    locator: Section 3 (two orders for x1x2 + x3x4 + x5x6)
  - paper: doi:10.1109/12.537122
    title: Beate Bollig and Ingo Wegener, Improving the variable ordering of OBDDs is NP-complete, IEEE Transactions on Computers 45(9), 1996, pages 993 to 1002
    locator: main theorem (reduction from optimal linear arrangement)
  - paper: "Seiichiro Tani, Kiyoharu Hamaguchi and Shuzo Yajima, The complexity of the optimal variable ordering problems of shared binary decision diagrams, ISAAC 1993, Lecture Notes in Computer Science 762, pages 389 to 398"
    title: Tani, Hamaguchi and Yajima, The complexity of the optimal variable ordering problems of shared binary decision diagrams
    locator: main theorem (NP-completeness for shared OBDDs)
  - paper: doi:10.1006/inco.2001.3076
    title: Detlef Sieling, The nonapproximability of OBDD minimization, Information and Computation 172(2), 2002, pages 103 to 138
    locator: main theorem (no polynomial-time approximation within a constant factor unless P = NP)
  - paper: doi:10.1109/12.53586
    title: Steven J. Friedman and Kenneth J. Supowit, Finding the optimal variable ordering for binary decision diagrams, IEEE Transactions on Computers 39(5), 1990, pages 710 to 713
    locator: the dynamic program over subsets, O(n^2 3^n) time
  - paper: doi:10.1109/ICCAD.1993.580029
    title: Richard Rudell, Dynamic variable ordering for ordered binary decision diagrams, ICCAD 1993, pages 42 to 47
    locator: the sifting algorithm and the in-place swap of adjacent levels
---

The variable ordering problem asks for the variable order that makes the [reduced ordered BDD](/reduced-ordered-bdd/) of a function as small as possible. For one fixed order the reduced diagram is unique ([canonicity](/bdd-canonicity/)), but a different order gives a different diagram, and the two sizes can differ by an exponential factor. The decision version is [NP-complete](/np-complete/) ([Bollig and Wegener](/variable-ordering-np-hardness/)). An exact answer takes $O(n^2 3^n)$ time with the [Friedman-Supowit](/friedman-supowit-ordering/) dynamic program. BDD packages use heuristics, mainly [sifting](/bdd-sifting/) and [window permutation](/window-permutation-reordering/). These heuristics have no proved approximation ratio.

This page is the problem and an overview of the methods. The hardness theorem, the exact algorithm and the two heuristics each have their own page.

## In plain words

A BDD asks yes-or-no questions about the input bits, in one fixed sequence on each path. The sequence decides how much the diagram must remember at each step. If two bits work together, ask them one after the other, and the diagram can forget them at once. If you ask all the first bits of each pair first, the diagram must remember each answer until the partner bit comes. Then it needs a node for each combination of answers.

So the same function can need ten nodes with one sequence and thousands with another. The task is to find a good sequence. Trying every sequence is too slow, and no fast method is known that always finds the best one. Tools therefore start from a sequence that the structure of the circuit suggests. Then they improve it with local moves while they work.

## Definition

We use the notation of the BDD pages. The variables are $x_1, \ldots, x_n$, and an order is a permutation $\pi$ that lists them from the top level to the bottom level. For a [Boolean function](/boolean-function/) $f$, the reduced $\pi$-OBDD of $f$ is $G_\pi(f)$, and its size $|G_\pi(f)|$ counts the inner nodes and the sinks. For a list $F = (f_1, \ldots, f_m)$ of functions, the shared OBDD $G_\pi(F)$ has one root for each $f_j$ and shares equal subgraphs; its size is the number of distinct nodes.

**Problem (OBDD minimization).** The input is a function $f$, given as a $\pi$-OBDD for some order $\pi$. The output is an order $\pi^*$ with

$$|G_{\pi^*}(f)| = \min_{\pi'} |G_{\pi'}(f)|.$$

**Decision version.** The input is a $\pi$-OBDD $G$ of $f$ and an integer $s$. The question is whether some order $\pi'$ gives $|G_{\pi'}(f)| \le s$.

The size of each level has a closed form, which all exact methods use. Let $S$ be the set of the first $k - 1$ variables of $\pi$, and let $x = \pi(k)$. Then

$$\#\{\text{nodes labeled } x\} = \#\{ f|_{a} : a \in \{0,1\}^S, \ f|_{a} \text{ depends on } x \}.$$

Here $f|_a$ is the [cofactor](/cofactor/) of $f$ by the assignment $a$ to the variables of $S$. The proof is short: each assignment $a$ leads from the root to the node of $f|_a$, and the reduced diagram has one node for each distinct subfunction ([canonicity](/bdd-canonicity/)). This number depends on the set $S$ and on $x$, but not on the order of the variables inside $S$ or below $x$. The number of $x$-nodes changes only when a variable crosses $x$. In particular, an exchange of two adjacent levels changes only the node counts of those two levels.

## Variants

- **Shared OBDDs.** Minimize the size of $G_\pi(F)$ for several functions at once. Tani, Hamaguchi and Yajima (1993) proved this version NP-complete.
- **Input as a truth table.** If $f$ is given as its table of $N = 2^n$ values, the Friedman-Supowit algorithm takes $O(n^2 3^n) = O(N^{\log_2 3} \log^2 N)$ time. This is polynomial in the input size, since $\log_2 3 \approx 1.585$. The hard case is a compact input, such as an OBDD or a circuit.
- **Input as a circuit or a CNF formula.** The OBDD for one order may already be exponential in the input size. Here the order is chosen before the BDD is built, from the structure of the circuit.
- **Approximation.** Find an order within a factor $c$ of the best. Sieling (2002) proved that for each constant $c > 1$ this is NP-hard.
- **Dynamic reordering.** In a BDD package the diagram changes during the computation. The package reorders in place, at chosen times, without a change of the node ids that the user holds.
- **Other diagrams.** The same problem exists for [ZDDs](/zero-suppressed-bdd/), [MDDs](/multi-valued-decision-diagram/) and [algebraic decision diagrams](/algebraic-decision-diagram/). [KFDDs](/kronecker-functional-decision-diagram/) also choose a decomposition type for each variable. [Free BDDs](/free-binary-decision-diagram/) allow a different order on each path.

## Examples

All numbers below were computed by a script with the [Friedman-Supowit](/friedman-supowit-ordering/) program, which gives the minimum and also the maximum over all $n!$ orders. Sizes include the sinks.

**Pairs.** Let $f_k = x_1 x_2 + x_3 x_4 + \cdots + x_{2k-1} x_{2k}$. This is Bryant's example (1986).

| $k$ | $n$ | order $x_1, x_2, \ldots, x_{2k}$ | order $x_1, x_3, \ldots, x_2, x_4, \ldots$ | min over all orders | max over all orders |
|---|---|---|---|---|---|
| 1 | 2 | 4 | 4 | 4 | 4 |
| 2 | 4 | 6 | 8 | 6 | 8 |
| 3 | 6 | 8 | 16 | 8 | 16 |
| 4 | 8 | 10 | 32 | 10 | 32 |
| 5 | 10 | 12 | 64 | 12 | 64 |

The first order gives $2k + 2$ nodes. The second order gives $2^{k+1}$ nodes. After $x_1, x_3, \ldots, x_{2k-1}$ are read, the rest of the function is the OR of the $x_{2j}$ with $x_{2j-1} = 1$. The $2^k$ answers give $2^k$ distinct subfunctions, so the level formula forces many nodes.

**Symmetric functions.** If $f(x)$ depends only on the number of ones in $x$, every order gives the same diagram up to the names of the variables. The subfunction after $k - 1$ levels depends only on the number of ones read so far, so each level has at most $k$ nodes, and the size is $O(n^2)$ for every order. Parity has $2n + 1$ nodes with each order.

**Middle bit of a product.** Let $\mathrm{MUL}_n$ be bit $n-1$ of the product of two $n$-bit numbers, with $2n$ variables. The [multiplier lower bound](/multiplier-bdd-lower-bound/) says that each order needs at least $2^{\lfloor n/8 \rfloor}$ nodes. The measured values for small $n$:

| $n$ | variables | min over all orders | max over all orders |
|---|---|---|---|
| 3 | 6 | 14 | 24 |
| 4 | 8 | 31 | 71 |
| 5 | 10 | 63 | 207 |
| 6 | 12 | 136 | 649 |
| 7 | 14 | 315 | 2019 |

The best order already gives a size that roughly doubles with each extra bit. For such a function, no ordering method can help much.

**Hidden weighted bit.** The [HWB lower bound](/hidden-weighted-bit-lower-bound/) gives another function with exponential size for every order. Its measured minimum grows from 82 nodes at $n = 10$ to 224 nodes at $n = 14$. HWB has small [free BDDs](/free-binary-decision-diagram/), so the order constraint itself causes the blow-up.

## Known algorithms

**Exact methods.**

- **All orders.** Build the diagram for each of the $n!$ orders. This is only possible for very small $n$.
- **[Friedman-Supowit](/friedman-supowit-ordering/) (1990).** A dynamic program over the subsets of variables, like the [Held-Karp algorithm](/held-karp-algorithm/). It uses the level formula: the cost of a level depends only on the set of variables below it. It takes $O(n^2 3^n)$ time and exponential space.
- **Branch and bound.** Later exact methods prune the subset lattice with lower bounds on the size of the remaining levels, in the style of [best-first branch and bound](/best-first-branch-and-bound/). They solve larger cases in practice, but the worst case stays exponential.

**Static heuristics.** Choose the order before the BDD is built, from the structure of a circuit. Typical rules order the inputs by a depth-first walk from the outputs, so that inputs that meet in a gate are close in the order. Malik et al. (1988) and Fujita, Fujisawa and Kawato (1988) gave early rules of this kind.

**Dynamic heuristics.** Improve the order of an existing BDD by exchanges of adjacent levels. An exchange rewrites only the nodes of the two levels, so it is cheap.

- **[Window permutation](/window-permutation-reordering/)** (Fujita, Matsunaga and Kakuda 1991; Ishiura, Sawada and Yajima 1991). Try all orders of a window of 2, 3 or 4 adjacent levels, keep the best one, and slide the window.
- **[Sifting](/bdd-sifting/)** (Rudell 1993). Move one variable through all levels, put it at the best position, and repeat for each variable. This is the default reordering of most BDD packages.
- Variants of sifting move groups of variables together, and general [local search](/local-search/) such as [simulated annealing](/simulated-annealing/) has also been tried.

None of the heuristics has a proved approximation ratio, and by Sieling's theorem no polynomial-time method can have a constant ratio unless P = NP. Their quality is known only from measurements. For example, on 200 random functions of 8 variables (each an OR of 3 to 6 random products of two variables, seed 5), sifting reached the optimum in 193 cases, windows of 3 levels in 137 cases, and windows of 2 levels in 90 cases.

## Bounds

- **Upper bound for every function.** Every function of $n$ variables has a reduced OBDD with $O(2^n / n)$ nodes for every order (see [reduced ordered BDD](/reduced-ordered-bdd/)).
- **Best against worst order.** The ratio can be exponential: $2k + 2$ against $2^{k+1}$ for the pairs function above.
- **Functions that are hard for every order.** The middle bit of multiplication needs $2^{\lfloor n/8 \rfloor}$ nodes for each order (Bryant 1991), and the hidden weighted bit needs $2^{n/5 - 1}$ nodes (Bollig, Löbbing, Sauerhoff and Wegener 1999). For these functions the problem is not the order.
- **Hardness.** The decision version is NP-complete for a single OBDD (Bollig and Wegener 1996) and for shared OBDDs (Tani, Hamaguchi and Yajima 1993). For each constant $c > 1$, it is NP-hard to find an order within a factor $c$ of the best (Sieling 2002).
- **Exact time.** $O(n^2 3^n)$ (Friedman and Supowit 1990). This is far below the $n!$ orders, but it is still exponential.

## Reductions

- **From optimal linear arrangement.** Bollig and Wegener reduce the optimal linear arrangement problem on graphs to the decision version. The proof is on the [NP-hardness page](/variable-ordering-np-hardness/).
- **To a shortest path in the subset lattice.** The level formula turns the problem into a shortest path from the empty set to the full set in the lattice of subsets, where adding $x$ to a set $J$ costs the number of $x$-nodes directly above $J$. Friedman-Supowit is dynamic programming on this graph, and the branch and bound methods are best-first search on it.
- **Membership in NP.** The certificate is the order $\pi'$. To check it, rebuild the diagram bottom-up in a manager with the order $\pi'$: each node $v$ of $G$ with variable $x$ becomes $\mathrm{ITE}(x, h_1, h_0)$ of the results $h_1$ and $h_0$ of its children. The function of $v$ is a restriction of $f$, and a restriction never has a larger $\pi'$-OBDD than $f$. So each intermediate result has at most $s$ nodes if the answer is yes, and the check stops with no as soon as a result passes $s$ nodes. This takes time polynomial in $|G|$ and $s$.

## Applications

- **[Symbolic model checking](/symbolic-model-checking/) and [symbolic reachability](/symbolic-reachability/).** The transition relation and the state sets are BDDs. The order decides whether the computation fits in memory. Current and next state variables are usually interleaved.
- **[Equivalence checking](/boolean-equivalence-checking/) of circuits.** The BDDs of two circuits are built with the same order and compared.
- **[Model counting](/model-counting/)** and the knowledge compilation of constraints. The count is linear in the BDD size, so a good order makes the count fast.
- **Logic synthesis.** The BDD size with a good order is a measure of the complexity of a function.

## References
