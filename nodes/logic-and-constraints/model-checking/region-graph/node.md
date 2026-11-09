---
tag: VER2WP
kind: data-structure
slug: region-graph
name: Region graph
aliases:
- Region automaton
- Region transition system
- Region abstraction
area: logic-and-constraints/model-checking
level: advanced
summary: A finite quotient of a timed automaton's state space by clock regions. It has at most n! 2^n Π(2c+2) regions per location and decides reachability exactly.
model: word-ram
complexity:
  vars: {r: the number of regions, l: the number of locations, e: the number of edges, n: the number of clocks}
  time: {worst: O(r (l + e) n)}
  space: {extra: O(r l n)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [timed-automata, bisimulation, reachability-problem]
see_also: [difference-bound-matrix, hybrid-automata, state-explosion-problem, symbolic-model-checking, ctl-model-checking, safety-property, depth-first-search, pspace]
sources:
  - paper: doi:10.1016/0304-3975(94)90010-8
    title: Rajeev Alur and David L. Dill, A theory of timed automata, Theoretical Computer Science 126(2), 1994, pages 183 to 235
    locator: region equivalence, the region automaton, the bound on the number of regions, and the PSPACE-completeness of emptiness
  - paper: "Rajeev Alur, Costas Courcoubetis and David L. Dill, Model-checking in dense real-time, Information and Computation 104(1), 1993, pages 2 to 34"
    title: Model-checking in dense real-time
    locator: the region graph as the basis of model checking the timed branching-time logic TCTL
  - book: isbn:9780262026499
    title: Christel Baier and Joost-Pieter Katoen, Principles of Model Checking, MIT Press, 2008
    locator: Chapter 9 (timed automata, clock regions, the region transition system and its time-abstract bisimulation with the timed automaton)
  - paper: "Thomas A. Henzinger, Zohar Manna and Amir Pnueli, What good are digital clocks?, ICALP 1992, Lecture Notes in Computer Science 623, Springer, pages 545 to 558"
    title: What good are digital clocks?
    locator: digitization, which shows that integer delays suffice for some properties of timed systems with non-strict constraints
---

The *region graph* of a [timed automaton](/timed-automata/) is a finite graph that answers the same reachability questions as the automaton, although the automaton has uncountably many states. Alur and Dill defined it in 1990 and 1994. Two clock valuations are in the same *region* when no guard or invariant can tell them apart, now or after any amount of time passes. Three things must match: the integer part of each clock (up to the largest constant it is compared with), which clocks have a zero fractional part, and the order of the fractional parts. A node of the graph is a pair of a location and a region. There are two kinds of edge: a step to the next region in time, and a discrete edge of the automaton. The equivalence is a time-abstract [bisimulation](/bisimulation/), so a location is reachable in the automaton exactly when it is reachable in the region graph. This gives the PSPACE upper bound for timed automata reachability. The number of regions is exponential in the number of clocks and in the size of the constants. Tools therefore search with zones stored as [difference bound matrices](/difference-bound-matrix/) instead, and use the region graph as the proof that the search is correct and terminates.

## In plain words

A timed automaton has clocks that all run at the same speed, and its moves depend on tests such as "clock x is at most 2". Clock values are real numbers, so there are infinitely many states. Most of them behave the same. If two clock settings agree on the whole part of each clock, on which clocks sit exactly on a whole number, and on which clock will reach the next whole number first, then every test gives the same answer for both, now and after any wait. A clock that is above every number it is ever compared with only needs the fact that it is "large". Put settings that agree in this way into one box, called a region. There are only finitely many boxes. So we draw a finite graph of boxes and search it like any other graph.

## The abstract type

Fix a diagonal-free timed automaton $A$ with clocks $x_1, \ldots, x_n$, locations $L$ and edges $E$. Its guards and invariants are conjunctions of atomic constraints $x \sim c$ with $\sim \in \{<, \le, =, \ge, >\}$ and $c \in \mathbb{N}$. For each clock $x$, let $c_x$ be the largest constant that $x$ is compared with. A valuation is a map $v$ from clocks to $\mathbb{R}_{\ge 0}$. Write $\lfloor t \rfloor$ and $\mathrm{fr}(t)$ for the integer part and the fractional part of $t$.

Two valuations $v$ and $v'$ are *region equivalent*, $v \cong v'$, when these three conditions hold:

1. For every clock $x$, either $v(x) > c_x$ and $v'(x) > c_x$, or $\lfloor v(x) \rfloor = \lfloor v'(x) \rfloor$.
2. For every clock $x$ with $v(x) \le c_x$: $\mathrm{fr}(v(x)) = 0$ if and only if $\mathrm{fr}(v'(x)) = 0$.
3. For all clocks $x, y$ with $v(x) \le c_x$ and $v(y) \le c_y$: $\mathrm{fr}(v(x)) \le \mathrm{fr}(v(y))$ if and only if $\mathrm{fr}(v'(x)) \le \mathrm{fr}(v'(y))$.

A *region* is an equivalence class of $\cong$. The *region graph* $R(A)$ has the nodes $(\ell, r)$ with $\ell \in L$ and $r$ a region that satisfies the invariant of $\ell$. It has these edges:

- a *delay edge* $(\ell, r) \to (\ell, \mathrm{succ}(r))$ when $\mathrm{succ}(r) \ne r$ satisfies the invariant of $\ell$, where $\mathrm{succ}(r)$ is the first region after $r$ that time passing reaches;
- an *action edge* $(\ell, r) \to (\ell', r[Y := 0])$ for each edge $(\ell, g, Y, \ell')$ of $A$ such that $r$ satisfies $g$ and $r[Y := 0]$ satisfies the invariant of $\ell'$.

The operations of the type are: the initial region, the test of a constraint on a region, the time successor, the reset, and the search for the reachable nodes.

## Representation

A region is stored as a triple $(\mathit{ints}, \mathit{zero}, \mathit{order})$:

- $\mathit{ints}[x]$ is $\lfloor v(x) \rfloor$ if $v(x) \le c_x$, and the marker $c_x + 1$ if $v(x) > c_x$;
- $\mathit{zero}$ is the set of bounded clocks whose fractional part is 0;
- $\mathit{order}$ is a list of disjoint nonempty sets that splits the other bounded clocks by their fractional parts, from the smallest part to the largest. Clocks with equal fractional parts are in the same set.

A clock is *bounded* when its value is at most $c_x$. Every triple of this shape is the code of exactly one nonempty region, and every region has exactly one code. A region takes $O(n)$ words. The graph is never stored in full. A search keeps a set of visited nodes, as a hash set of codes.

## Operations

```pseudo id=main
TIME-SUCC(ints, zero, order, c)       ▷ the next region that time passing reaches
L1  if zero ≠ ∅ then                    ▷ some bounded clock is on an integer
L2      for each clock x in zero do
L3          if ints[x] = c[x] then ints[x] ← c[x] + 1, remove x from zero   ▷ x leaves the bounded range
L4      if zero ≠ ∅ then order ← (zero) · order     ▷ the other clocks of zero get the smallest fractional part
L5      return (ints, ∅, order)
L6  if order is empty then return none            ▷ every clock is above its constant: time changes nothing
L7  last ← the last set in order                ▷ the clocks with the largest fractional part
L8  for each clock x in last do ints[x] ← ints[x] + 1
L9  return (ints, last, order without last)       ▷ they reach the next integer first
```

```pseudo id=ops
SATISFIES(ints, zero, order, x ∼ c)   ▷ c ≤ c[x]
S1  if ints[x] > c[x] then return ∼ ∈ {>, ≥}
S2  if x ∈ zero then return ints[x] ∼ c
S3  return the truth of ints[x] + 1/2 ∼ c     ▷ x lies strictly between ints[x] and ints[x] + 1

RESET(ints, zero, order, Y)
R1  for each x in Y do ints[x] ← 0
R2  return (ints, zero ∪ Y, the sets of order with Y removed, empty sets dropped)

REGION-REACH(A)
Q1  start ← (ℓ0, ((0, …, 0), {all clocks}, ()))
Q2  seen ← {start}, stack ← [start]
Q3  while stack is not empty do
Q4      (ℓ, r) ← pop stack
Q5      s ← TIME-SUCC(r)
Q6      if s ≠ none and s satisfies Inv(ℓ) then visit (ℓ, s)
Q7      for each edge (ℓ, g, Y, ℓ') of A with r satisfying g do
Q8          r' ← RESET(r, Y)
Q9          if r' satisfies Inv(ℓ') then visit (ℓ', r')
Q10 return seen       ▷ visit adds a new node to seen and to stack
```

Lines L1 to L5 handle a region where some clock has a zero fractional part. A small delay $\delta > 0$ moves those clocks off the integer. Their fractional part becomes $\delta$, which is smaller than every other fractional part. A clock that was exactly at its constant goes above it. Lines L6 to L9 handle a region where no bounded clock is on an integer. The clocks in the last set have the largest fractional part, so they reach the next integer first, all at the same time. Clocks above their constants never change their code. In S3 the value $\mathit{ints}[x] + 1/2$ stands for any value in the open interval, because $c$ is an integer.

## Example

Take two clocks $x$ and $y$ and four locations. The edge $\ell_0 \to \ell_1$ has guard $x \le 1$ and resets $y$. The edge $\ell_1 \to \ell_2$ has guard $x \ge 2 \wedge y \le 1$. The edge $\ell_1 \to \ell_3$ has guard $x \ge 2 \wedge y < 1$. There are no invariants. So $c_x = 2$ and $c_y = 1$.

The delay edges from the initial region give this chain, which ends in the region where both clocks are above their constants:

| Step | $\mathit{ints}$ | $\mathit{zero}$ | $\mathit{order}$ | Valuations |
|---|---|---|---|---|
| 0 | $(0, 0)$ | $\{x, y\}$ | empty | $x = y = 0$ |
| 1 | $(0, 0)$ | $\emptyset$ | $(\{x, y\})$ | $0 < x = y < 1$ |
| 2 | $(1, 1)$ | $\{x, y\}$ | empty | $x = y = 1$ |
| 3 | $(1, 2)$ | $\emptyset$ | $(\{x\})$ | $1 < x < 2$, $y > 1$ |
| 4 | $(2, 2)$ | $\{x\}$ | empty | $x = 2$, $y > 1$ |
| 5 | $(3, 2)$ | $\emptyset$ | empty | $x > 2$, $y > 1$ |

At step 3, $y$ was on its constant 1, so line L3 marks it as above its constant. The guard $x \le 1$ holds in steps 0, 1 and 2, so there are three action edges to $\ell_1$:

- From step 0, the reset gives $x = y = 0$.
- From step 1, it gives $0 < x < 1$, $y = 0$, coded as $\mathit{ints} = (0, 0)$, $\mathit{zero} = \{y\}$, $\mathit{order} = (\{x\})$.
- From step 2, it gives $x = 1$, $y = 0$.

In $\ell_1$ the difference $x - y$ stays fixed while time passes. Only the third branch, with $x - y = 1$, reaches the region $x = 2$, $y = 1$. That region satisfies $x \ge 2 \wedge y \le 1$, so $\ell_2$ is reachable. In the other branches $y > 1$ when $x$ reaches 2. No reachable region in $\ell_1$ satisfies $x \ge 2 \wedge y < 1$, so $\ell_3$ is unreachable. The search visits 22 nodes: 6 in $\ell_0$, 14 in $\ell_1$ and 2 in $\ell_2$. There are 28 regions for these constants, and the bound of the next sections gives $2! \cdot 2^2 \cdot 6 \cdot 4 = 192$.

## Correctness

The proof file shows four facts.

- The code is a bijection with the regions.
- Equivalent valuations satisfy the same constraints, and SATISFIES computes the answer from the code.
- Resets map regions to regions, and RESET computes the result.
- As time passes from any valuation in a region $r$, the valuation goes through $r, \mathrm{succ}(r), \mathrm{succ}^2(r), \ldots$ in this order and skips none, and TIME-SUCC computes $\mathrm{succ}$.

From these facts, region equivalence is a time-abstract bisimulation, because invariants are upper bounds and so they hold on a whole delay if they hold at its end. Every path of the region graph lifts to a run of the automaton from any valuation in its first region. Every run projects to a path of the region graph. So location $\ell$ is reachable in $A$ if and only if some node $(\ell, r)$ is reachable in $R(A)$.

## Complexity

Let $r$ be the number of regions. The proof file shows

$$r \le n! \, 2^{n-1} \prod_{x} (2 c_x + 2) \le n! \, 2^n \prod_{x} (2 c_x + 2).$$

The product counts the choices for each clock: one of $c_x + 1$ integer values, one of $c_x$ open unit intervals, or "above $c_x$". The factorial term bounds the number of orders of the fractional parts. With one clock there are exactly $2 c_x + 2$ regions. The graph has at most $r |L|$ nodes. REGION-REACH handles each node once. It spends $O(n)$ time on the time successor and $O(n)$ time per outgoing edge, if guards have $O(n)$ atomic constraints and edges are indexed by their source. That is $O(r (l + e) n)$ time and $O(r l n)$ space. Since the bound is exponential in $n$ and in the binary size of the constants, the search is exponential. A depth-first search that stores only the current node and guesses the path runs in polynomial space, which gives the PSPACE upper bound of Alur and Dill. Reachability is also PSPACE-hard, so no method runs in polynomial time unless P = PSPACE.

## Variants

- **Diagonal constraints.** Guards of the form $x - y \sim c$ need the regions to also respect the differences up to the largest diagonal constant. The equivalence above is not enough when one of the two clocks is above its constant.
- **Per-location constants.** Taking $c_x$ per location, from the constraints that can still be tested before $x$ is reset, gives coarser regions and a smaller graph.
- **Lower and upper bounds.** Using separate maximal lower-bound and upper-bound constants gives coarser equivalences. These are mostly used through zones, as in the LU extrapolation of [difference bound matrices](/difference-bound-matrix/).
- **Zone graph.** A zone is a convex union of regions, coded as a [difference bound matrix](/difference-bound-matrix/). The zone graph with extrapolation is usually far smaller, and its correctness proof reduces to the region graph.
- **Timed logics.** Alur, Courcoubetis and Dill model check the branching-time logic TCTL by adding a clock for the formula and labelling the region graph, in the style of [CTL model checking](/ctl-model-checking/).
- **Region automaton.** Adding the action letters to the edges gives a finite automaton for the untimed language of $A$. Its emptiness is the emptiness of $A$, and a [Büchi](/buchi-automaton/) version handles infinite runs with a progress condition.

## When to use it

Use the region graph to prove that a question about a timed automaton is decidable, to bound its complexity, or to justify a coarser abstraction. It is also a clear reference to test an implementation against, as the tests here do. For real verification, use zones and [difference bound matrices](/difference-bound-matrix/), as UPPAAL and similar tools do. The region graph grows with the product of all constants and with $n!$, which is the [state explosion problem](/state-explosion-problem/) in its timed form. Do not use regions for [hybrid automata](/hybrid-automata/) with clocks that run at different rates. There is no finite bisimulation in general, and reachability is undecidable.

## Pitfalls

- **Forgetting the order of fractional parts.** Integer parts alone do not form a bisimulation. In the example, $x = 1.3$, $y = 0.5$ and $x = 1.5$, $y = 0.3$ have the same integer parts, but only the second one reaches $x = 2$ while $y < 1$.
- **Keeping large values exact.** If a clock above $c_x$ keeps its integer part, the graph is infinite, because a clock that is never reset grows without limit. All values above $c_x$ must be one class.
- **Ordering clocks above their constants.** The order condition must only use bounded clocks. Ordering all clocks makes the classes finer than needed, and the bound fails.
- **Self loops.** The time successor of the region where every clock is above its constant is itself. A search must not treat this as a new node.
- **Strict invariants.** A delay edge is allowed only when the next region satisfies the invariant. Since invariants are upper bounds, the earlier regions on the way then satisfy it too. Lower-bound invariants break this argument.

## Implementations

## History

Alur and Dill introduced timed automata and the region construction at ICALP 1990, and gave the full theory in 1994. They showed that the emptiness of timed Büchi automata is PSPACE-complete, and that universality and inclusion are undecidable. Alur, Courcoubetis and Dill (1990, journal version 1993) used the region graph to model check TCTL. Later tools such as Kronos and UPPAAL moved to zones, but their correctness proofs still go through regions. Bouyer (2004) showed that the standard zone extrapolation is exact for diagonal-free automata, by comparing it with regions, and that it can be wrong with diagonal constraints.

## References
