---
tag: XVSXFR
kind: algorithm
slug: land-doig-algorithm
name: Land-Doig algorithm
aliases:
- Land-Doig branch and bound
area: techniques/branch-and-bound
level: advanced
summary: Original branch-and-bound for integer linear programs, using LP relaxations as bounds and branching on fractional variables.
solves: [mixed-integer-programming]
model: real-ram
complexity:
  vars: {N: the number of nodes of the search tree, L: the time to solve one linear program}
  time: {worst: O(N (L + log N))}
  space: {extra: O(N)}
properties: {deterministic: true, recursive: false}
prereqs: [linear-programming-problem, lp-relaxation, best-first-branch-and-bound]
see_also: [simplex-method, branching-rule, bounding-function, mixed-integer-programming, binary-integer-programming, branch-and-cut, cutting-plane-method-integer-programming, dual-simplex-method]
sources:
  - paper: doi:10.2307/1910129
    title: A. H. Land and A. G. Doig, An automatic method of solving discrete programming problems, Econometrica 28(3), 1960
    locator: pp. 497 to 520
  - paper: doi:10.1093/comjnl/8.3.250
    title: R. J. Dakin, A tree-search algorithm for mixed integer programming problems, The Computer Journal 8(3), 1965
    locator: pp. 250 to 255
  - book: isbn:9780471283669
    title: Laurence A. Wolsey, Integer Programming
    locator: Chapter 7, Branch and Bound (LP-based branch and bound)
  - paper: doi:10.1287/opre.11.6.972
    title: John D. C. Little, Katta G. Murty, Dura W. Sweeney and Caroline Karel, An algorithm for the traveling salesman problem, Operations Research 11(6), 1963
    locator: pp. 972 to 989
  - paper: doi:10.1007/bf01580225
    title: Robert G. Jeroslow, Trivial integer programs unsolvable by branch-and-bound, Mathematical Programming 6(1), 1974
    locator: pp. 105 to 109
---

The Land-Doig algorithm solves integer linear programs by solving a tree of linear programs. Each node fixes some integer variables to integer values, and the optimum of its [LP relaxation](/lp-relaxation/) is an upper bound for all integer solutions in it. A node whose LP solution is integral is a candidate [incumbent](/incumbent-solution/); a node whose LP value is not above the incumbent is discarded; any other node is split on a variable with a fractional value. Land and Doig published it in 1960, and it is the origin of LP-based branch and bound, the method at the core of every modern solver for [mixed integer programming](/mixed-integer-programming/).

## In plain words

You want the best whole-number answer to a problem with linear rules, such as how many trucks of each type to buy. First drop the rule "whole numbers only" and solve the easier problem. Its answer is at least as good as any whole-number answer, so it is a limit.

If this answer is already in whole numbers, you are done. If a variable has the value 3.4, any whole-number answer has it at 3 or 4 or further away. So you try "fix it to 3" and "fix it to 4", each as a new easier problem. You also keep in mind "2" and "5" for later. Each new problem gives its own limit, and you always work next on the problem with the best limit. You stop when no waiting problem can beat the best whole-number answer you have.

## The problem

Maximize $c^\top x$ subject to $A x \le b$ and $x \ge 0$, with $x_j \in \mathbb{Z}$ for $j \in I$, where $I$ is a set of indices. With $I$ equal to all indices, it is a pure integer program; otherwise it is mixed. The page assumes that the feasible set of the LP relaxation, $P = \{x \ge 0 : A x \le b\}$, is bounded, so that every variable has a finite range. For a set $F$ of fixings $x_j = k$, write $\mathrm{LP}(F)$ for the linear program with these equations added, and $\bar{x}(F)$ and $v(F)$ for an optimal solution and its value.

## The algorithm

A live node is a tuple $(F, \bar{x}, v, sib)$: the fixings, the LP solution and value, and a note $sib = (F', j, k, s)$ that says which sibling to make next: the node $F' \cup \{x_j = k\}$, where $s = \pm 1$ is the direction away from the LP value of the parent. The procedure MAKE$(F, sib)$ solves LP$(F)$ and, if it is feasible with $v(F) > z$, inserts the node into a max-priority queue $H$ with key $v(F)$.

```pseudo id=main
LAND-DOIG(c, A, b, I)
L1  z ← −∞; best ← NIL
L2  MAKE(∅, NIL)                                    ▷ the root: the LP relaxation itself
L3  while H is not empty do
L4      (F, x̄, v, sib) ← EXTRACT-MAX(H)              ▷ the live node with the best LP value
L5      if v ≤ z then break                          ▷ no live node can beat z
L6      if sib = (F′, j, k, s) ≠ NIL then
L7          MAKE(F′ ∪ {x_j = k}, (F′, j, k + s, s))  ▷ the next value of x_j, one step further away
L8      if x̄_j is an integer for every j ∈ I then
L9          if v > z then z ← v; best ← x̄; continue
L10     choose j ∈ I with x̄_j fractional; let f ← ⌊x̄_j⌋
L11     MAKE(F ∪ {x_j = f}, (F, j, f − 1, −1)); MAKE(F ∪ {x_j = f + 1}, (F, j, f + 2, +1))
L12 return (z, best)
```

Line L11 makes only the two values of $x_j$ next to the LP value. The other values, $f - 1, f - 2, \ldots$ and $f + 2, f + 3, \ldots$, are made one at a time at line L7, when their neighbor nearer to $\bar{x}_j$ is taken from the queue. This keeps the tree small and is safe because the LP value can only fall as the fixed value moves away from $\bar{x}_j$ (see Correctness).

## Example

Maximize $5 x_1 + 4 x_2$ subject to $6 x_1 + 4 x_2 \le 24$, $x_1 + 2 x_2 \le 6$, $x_1, x_2 \ge 0$ and integer.

| step | LP solved | solution | value | result |
|---|---|---|---|---|
| 1 | root | $(3, \frac{3}{2})$ | 21 | inserted |
| 2 | $x_2 = 1$ | $(\frac{10}{3}, 1)$ | $\frac{62}{3}$ | inserted, next sibling $x_2 = 0$ |
| 3 | $x_2 = 2$ | $(2, 2)$ | 18 | inserted, next sibling $x_2 = 3$ |
| 4 | $x_2 = 0$ | $(4, 0)$ | 20 | made when $x_2 = 1$ is taken; inserted |
| 5 | $x_2 = 1, x_1 = 3$ | $(3, 1)$ | 19 | inserted |
| 6 | $x_2 = 1, x_1 = 4$ | none | | infeasible |
| 7 | $x_2 = -1$ | none | | infeasible; made when $x_2 = 0$ is taken |

The root is taken first and split on $x_2 = \frac{3}{2}$ (steps 2 and 3). The node $x_2 = 1$, with value $\frac{62}{3}$, is taken next: it makes its sibling $x_2 = 0$ (step 4) and splits on $x_1 = \frac{10}{3}$ (steps 5 and 6). The node $x_2 = 0$, value 20, is taken next; its LP solution $(4, 0)$ is integral, so $z = 20$. The next node in the queue has value $19 \le 20$, so the search stops. The node $x_2 = 2$, value 18, is never processed, and $x_2 = 3$ is never made.

The optimum is $x = (4, 0)$ with value 20, after 7 linear programs. The rounded root solution $(3, 1)$ has value 19 and $(3, 2)$ is infeasible: rounding the LP optimum does not give the integer optimum, and the optimum $(4, 0)$ comes from a sibling made late, at line L7.

## Correctness

Fix a node with fixings $F$ and LP solution $\bar{x}$, and a fractional $\bar{x}_j$. Let $\varphi(k) = v(F \cup \{x_j = k\})$, with $\varphi(k) = -\infty$ when that program is infeasible. The feasible set of LP$(F)$ is convex, so the set of $k$ with $\varphi(k) > -\infty$ is an interval that contains $\bar{x}_j$, and $\varphi$ is concave on it: a convex combination of optimal points for $k_1$ and $k_2$ is feasible for the same combination of $k_1$ and $k_2$. The maximum of $\varphi$ is at $\bar{x}_j$. So $\varphi$ does not increase as $k$ moves away from $\bar{x}_j$: $\varphi(f - 1) \le \varphi(f)$, $\varphi(f + 2) \le \varphi(f + 1)$, and so on. Each integer solution of the node has $x_j = k$ for one integer $k$, so it lies in exactly one child $F \cup \{x_j = k\}$.

The algorithm keeps this invariant: every integer solution with value above $z$ lies in a live node, or in a child $F \cup \{x_j = k\}$ not made yet whose nearer neighbor $F \cup \{x_j = k \mp 1\}$ is live. A child that is not inserted because it is infeasible or has value at most $z$ takes all the further values with it, by the monotone property. When the loop stops, every live node has value at most $z$, and so has every child not yet made. The search ends because $P$ is bounded, so each $x_j$ has finitely many integer values, each set of fixings is made at most once, and a set of fixings has at most $|I|$ elements. The [proof](proofs/correctness.md) gives the details.

## Complexity

Each node costs one linear program and $O(\log N)$ for the queue, so the time is $O(N (L + \log N))$, where $N$ is the number of nodes and $L$ the time of one LP. Linear programs are solved in polynomial time by interior point methods, and in practice by the [simplex method](/simplex-method/), warm-started from the parent's basis with the [dual simplex method](/dual-simplex-method/).

The number of nodes can be exponential. Integer programming is NP-hard, so this is expected, but even very easy instances can be bad. Jeroslow (1974) gave the program $2 x_1 + 2 x_2 + \cdots + 2 x_n = n$ with $n$ odd and $x \in \{0, 1\}^n$, which has no solution because the left side is even. Every LP-based branch and bound that branches on single variables, with any node order, needs a number of nodes exponential in $n$ to prove this, because the LP stays feasible as long as at most $(n-1)/2$ variables are fixed to each of 0 and 1. With the code of this page, the number of linear programs solved is 15, 57, 207 and 753 for $n = 3, 5, 7, 9$.

The memory is the live nodes, $O(N)$ in the worst case, as in [best-first branch and bound](/best-first-branch-and-bound/).

## Properties

- **Exact.** It returns an optimal solution, or reports that there is none, when $P$ is bounded.
- **Best-first.** The node order is by LP value. As for [best-first branch and bound](/best-first-branch-and-bound/), every node it splits has LP value at least the optimum: an optimal solution lies in a live node, or in a sibling not made yet whose bound is at most that of a live node.
- **Gap.** At any time, $\max(z, \max_H v)$ is an upper bound on the optimum, and $z$ a lower bound.
- **Mixed problems.** Continuous variables are never fixed; they stay in the LP.

## Variants and improvements

- **Dakin's dichotomy.** Dakin (1965) replaced the fixings by the two bounds $x_j \le \lfloor \bar{x}_j \rfloor$ and $x_j \ge \lceil \bar{x}_j \rceil$. Two children cover all values, so no siblings need to be made later. This is the [branching rule](/branching-rule/) of modern solvers.
- **Depth-first and hybrid node order.** Depth-first order finds incumbents earlier and uses less memory, and the child LP can start from the parent's basis.
- **Choice of variable.** [Strong branching](/strong-branching/), [pseudocost branching](/pseudocost-branching/) and [reliability branching](/reliability-branching/) choose $j$ at line L10.
- **Cuts.** Adding cutting planes at nodes gives [branch and cut](/branch-and-cut/); adding columns gives [branch and price](/branch-and-price/).

## When to use it

Use LP-based branch and bound for integer and mixed integer linear programs whose LP relaxation is a good bound. In practice, use a solver that implements the modern form, with Dakin branching, cuts, presolve and heuristics. The original scheme with sibling values is useful when the integer variables have wide ranges and one wants a node for each value.

## Pitfalls

- **Rounding errors.** In floating point, $\bar{x}_j = 2.9999999$ is integral for practical purposes. Use a tolerance, or exact arithmetic for small problems as in the code here.
- **Unbounded relaxations.** If $P$ is unbounded, an LP can be unbounded, or a chain of siblings at line L7 can go on forever. Bound the variables first.
- **Rounding the LP solution.** Rounding $\bar{x}$ to the nearest integers can be infeasible or far from optimal, as in the example.
- **Forgetting the siblings.** With fixings to values, making only the two values next to $\bar{x}_j$ and never their further neighbors loses solutions, such as $x_2 = 0$ in the example.

## Implementations

## History

Land and Doig (1960) described the method for discrete programming problems, with LP bounds, fixings of a variable to successive integer values, and a choice among the live problems by their LP values. Dakin (1965) gave the two-way split on bounds that solvers use today. Little, Murty, Sweeney and Karel (1963) introduced the name branch and bound for the same idea in their traveling salesman algorithm. Jeroslow (1974) showed that the method can need exponentially many nodes on trivial programs.

## References
