---
tag: EG491A
kind: algorithm
slug: nova-state-encoding
name: NOVA state encoding
aliases:
- NOVA
- Villa-Sangiovanni-Vincentelli encoding
area: eda/high-level-synthesis-and-scheduling
level: advanced
summary: Villa and Sangiovanni-Vincentelli's state encoder that satisfies as many face embedding constraints from symbolic minimization as possible to give a small two-level controller.
solves: [state-assignment]
model: word-ram
complexity:
  vars: {n: the number of states, k: the code length (the least that holds n codes), G: the number of face constraints, T: the time of the symbolic two-level minimization}
  time: {worst: O(T + G^2 n 2^(k n))}
  space: {extra: O(n G + 2^k)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1990
  people: [Tiziano Villa, Alberto L. Sangiovanni-Vincentelli]
  note: Villa and Sangiovanni-Vincentelli published NOVA in IEEE Transactions on Computer-Aided Design in 1990, encoding states at a fixed code length by satisfying a weighted subset of the face constraints of symbolic minimization.
prereqs: [kiss-symbolic-minimization, state-assignment, two-level-logic-minimization]
see_also: [mustang-state-assignment, espresso, dfa-minimization, incompletely-specified-fsm-minimization, hamming-distance, set-cover, generic-backtracking-algorithm, fsm-decomposition]
sources:
  - paper: doi:10.1109/43.59068
    title: Tiziano Villa and Alberto L. Sangiovanni-Vincentelli, NOVA, state assignment of finite state machines for optimal two-level logic implementation, IEEE Transactions on Computer-Aided Design 9(9), 905 to 924, 1990
    locator: the weighted face constraints, the exact and heuristic embedding algorithms at a fixed code length, and the PLA areas measured on benchmark machines
  - paper: "Giovanni De Micheli, Robert K. Brayton and Alberto L. Sangiovanni-Vincentelli, Optimal state assignment for finite state machines, IEEE Transactions on Computer-Aided Design CAD-4(3), 269 to 285, 1985"
    title: Giovanni De Micheli, Robert K. Brayton and Alberto L. Sangiovanni-Vincentelli, Optimal state assignment for finite state machines, IEEE Transactions on Computer-Aided Design CAD-4(3), 269 to 285, 1985
    locator: symbolic minimization and face constraints, on which NOVA builds
  - book: isbn:9780070163331
    title: Giovanni De Micheli, Synthesis and Optimization of Digital Circuits, McGraw-Hill, 1994
    locator: Chapter 9 (state encoding for two-level circuits and the embedding of face constraints)
---

NOVA is a method of [state assignment](/state-assignment/) for two-level logic that keeps the number of state bits fixed. Like [KISS](/kiss-symbolic-minimization/), it starts from a symbolic minimization of the state table, whose product terms give face constraints: groups of states whose codes should span a face of the code cube that holds no other code. KISS lengthens the code until every constraint is met. NOVA instead fixes the code at the least length, usually $\lceil \log_2 n \rceil$ bits for $n$ states, and meets as many constraints as it can, giving more weight to the groups that more product terms use. Villa and Sangiovanni-Vincentelli published it in 1990. This page proves the bound that makes the idea work, a count of product terms that charges each unmet group the number of cubes it needs. It also shows by exhaustive search that NOVA is not optimal for the final logic: the codes that meet the most weight can differ from each other by several product terms.

## In plain words

KISS asks for codes in which every merged group of states can be named by one pattern with some bits left free, and it adds bits until that works. Extra bits mean extra flip-flops. NOVA keeps the fewest bits and accepts that some groups will need two or more patterns. It ranks the groups by how many rows of the merged table use them, and walks down the list, keeping a group whenever the groups kept so far and the new one can still all be given single patterns. Then it picks codes that give every kept group one pattern.

## The problem

The input is a reduced finite state machine with $n$ states, as on the [KISS](/kiss-symbolic-minimization/) page, and the output is an injective code of $k$ bits, with $k$ fixed in advance. The aim is a small minimum two-level cover of the encoded next-state and output functions, with unused codes as don't cares.

**Weights.** Let $S$ be a minimum symbolic cover. For a group $G$ of present states with $1 < |G| < n$, its weight $w(G)$ is the number of cubes of $S$ whose group is $G$.

**Cube count of a group.** For a code $\mathrm{enc}$ and a group $G$, let $\kappa(G)$ be the least number of subcubes of $\{0, 1\}^k$ whose union holds every code of $G$ and no code of a state outside $G$; unused codes may lie in them or not. If $\mathrm{enc}$ meets the face constraint of $G$, then $\kappa(G) = 1$; otherwise $\kappa(G) \ge 2$.

## The algorithm

```pseudo id=main
NOVA(M)
L1  S_cover ← a minimum symbolic cover of M, as in KISS
L2  for each group G of S_cover with 1 < |G| < n do w(G) ← the number of cubes of S_cover whose group is G
L3  order the groups by decreasing w(G), then by increasing size, then by first appearance in S_cover
L4  k ← ⌈log2 n⌉; kept ← empty; dropped ← empty
L5  for each group G in that order do
L6      if some injective code of k bits meets every face constraint in kept and G then add G to kept
L7      else add G to dropped
L8  return an injective code of k bits that meets every face constraint in kept
```

The test of line L6 is the face embedding problem at a fixed length. The reference code answers it by backtracking over all codes, which fits only small machines. Villa and Sangiovanni-Vincentelli's program offers several algorithms for this step, exact ones and heuristics, and options that this sketch leaves out; the version here keeps only the greedy rule of lines L5 to L7, with the weights of line L2. It is a simplified form of NOVA, not a transcription of the paper.

**The bound behind the weights.** For any injective code, the encoded function has a two-level cover with at most
$$\sum_{c \in S} \kappa(G_c)$$
cubes, where $G_c$ is the group of cube $c$ (proved in the [full proof](proofs/correctness.md)). A met group adds $w(G)$ to this sum and an unmet group adds $w(G)\,\kappa(G) \ge 2 w(G)$, so the sum is at least $|S|$ plus the weight of the unmet groups. Keeping heavy groups lowers this lower part of the bound. It does not control $\kappa$ of the dropped groups, and it says nothing about the minimum cover itself, which can be much smaller than the bound.

## Example

Take the machine $M_2$ with one input $x$, one output $z$ and four states:

| present | $x = 0$ | $x = 1$ |
| --- | --- | --- |
| $s_0$ | $s_1$ / 1 | $s_0$ / 1 |
| $s_1$ | $s_0$ / 1 | $s_0$ / 1 |
| $s_2$ | $s_2$ / 0 | $s_2$ / 1 |
| $s_3$ | $s_3$ / 1 | $s_2$ / 0 |

A minimum symbolic cover has 7 cubes:

| cube | $x$ | group | next | $z$ |
| --- | --- | --- | --- | --- |
| 1 | - | $\{s_1\}$ | $s_0$ | 1 |
| 2 | 1 | $\{s_0, s_1\}$ | $s_0$ | 1 |
| 3 | - | $\{s_2\}$ | $s_2$ | |
| 4 | 0 | $\{s_0\}$ | $s_1$ | 1 |
| 5 | 0 | $\{s_3\}$ | $s_3$ | 1 |
| 6 | 1 | $\{s_2, s_3\}$ | $s_2$ | |
| 7 | 1 | $\{s_0, s_1, s_2\}$ | | 1 |

The groups $\{s_0, s_1\}$, $\{s_2, s_3\}$ and $\{s_0, s_1, s_2\}$ each have weight 1, and line L3 orders them by size. With $k = 2$, the first two can be met together, but not with the third: three codes span a face of two bits only if that face is the whole square, which holds the fourth code. So NOVA keeps $\{s_0, s_1\}$ and $\{s_2, s_3\}$, drops $\{s_0, s_1, s_2\}$, and returns $s_0 = 00$, $s_1 = 01$, $s_2 = 10$, $s_3 = 11$. The dropped group $\{00, 01, 10\}$ needs two cubes, $0{-}$ and ${-}0$, so the bound is $6 + 2 = 8$ cubes. An exact minimization of the encoded function under these codes gives 5 cubes and 10 literals.

An exhaustive search over the 12 classes of two-bit codes (24 codes up to swapping the bits) gives a best cover of 4 cubes and 9 literals, with $s_0 = 01$, $s_1 = 11$, $s_2 = 00$, $s_3 = 10$. These codes meet the same two constraints as NOVA's codes. In fact 8 of the 12 classes meet both of them, so all 8 have the same total weight in NOVA's sense, and their exact covers range from 4 to 6 cubes. NOVA has no way to tell them apart, and its choice gives 5.

[KISS](/kiss-symbolic-minimization/) meets all three groups by going to three bits, with codes $000$, $001$, $010$, $110$; its encoded cover has 7 cubes, which an exact minimization reduces to 5 cubes and 9 literals. So on this machine KISS spends one more flip-flop for no fewer product terms than NOVA, and both miss the best two-bit code.

## Correctness

The [full proof](proofs/correctness.md) shows:

- **Valid codes.** The returned code is injective and meets every face constraint in kept, since line L6 adds a group only when such a code exists, and line L8 returns one.
- **The bound.** For any injective code, the encoded function has a cover with at most $\sum_{c} \kappa(G_c)$ cubes. With every constraint met, this is the KISS bound.
- **A maximal set.** Every dropped group cannot be met together with the groups kept before it. So no group can be added to kept without dropping another.

What is not proved: that the kept set has the largest weight that any code can meet. A greedy choice gives no such guarantee in general, since a kept group can block later groups. What is false: that the codes minimize the final logic. As the example shows, codes of equal weight can differ by two cubes. As a measurement, on 100 random machines with 4 states, one input bit, one output bit and every entry specified (seed 1990), the kept weight equalled the largest weight that any two-bit code can meet on all 100, which says more about how few constraints such small machines have than about the greedy rule. The final logic matched the best two-bit code on 41 of the 100, with 71 extra cubes in total and at most 3 on one machine.

## Complexity

The symbolic minimization of line L1 is a two-level minimization, hard in general. Lines L2 and L3 take $O(|S| n + G \log G)$ time. Line L6 runs $G$ times, and each run of the reference backtracking tries at most $2^{k n}$ placements with $O(G n)$ checks each, which gives the $O(G^2 n 2^{k n})$ term. The heuristics of the NOVA program replace this exponential step by polynomial ones.

## Properties

- **Fixed code length.** The number of flip-flops is always $\lceil \log_2 n \rceil$, unless the user asks for more.
- **Maximal.** The kept set cannot be extended. Nothing proves that its weight is the largest possible.
- **Not optimal.** The final logic need not be the smallest over codes of the same length. None of [KISS](/kiss-symbolic-minimization/), NOVA and [MUSTANG](/mustang-state-assignment/) is optimal for the final logic: on the example machines of the three pages, an exhaustive search over all codes finds cheaper logic than each of them gives.
- **Same bound as KISS when all constraints fit.** If every group can be met at length $k$, NOVA keeps them all and the KISS bound holds.
- **Deterministic.** The order of line L3 and the search order fix the result.

## Variants and improvements

- **Exact embedding at fixed length.** For small machines, the largest-weight set of constraints that some code meets can be found by searching all codes, as the tests do. This gives the best answer to NOVA's own objective, which is still not the final logic.
- **Weights from the cubes saved.** A weight $w(G) (\kappa(G) - 1)$ would measure what failing $G$ costs under the bound, but $\kappa$ depends on the code, so it is known only after the embedding.
- **Output constraints.** Constraints from the next-state field, described in De Micheli's book (Chapter 9), let cubes share next-state bits, which input constraints alone cannot see.
- **Multilevel logic.** For multilevel implementations, [MUSTANG](/mustang-state-assignment/) uses attraction weights between pairs of states instead of face constraints.
- **Longer codes.** Raising $k$ by one or two bits often lets every constraint fit, which turns NOVA into KISS with a heuristic embedding.

## When to use it

Use NOVA when the controller is a PLA or another two-level form and the number of flip-flops is fixed, so KISS's longer codes are not allowed. For small machines, compare its result with an exhaustive search over codes, since equal-weight codes can differ in cost. For multilevel logic, a method aimed at multilevel cost, such as MUSTANG, is the usual choice.

## Pitfalls

- **Taking the weight as the cost.** The met weight is a proxy. Two codes that meet the same groups can give different logic, as in the example.
- **Unreduced machines.** Equivalent states give extra groups and waste code space. Reduce the machine first with [DFA minimization](/dfa-minimization/) or [incompletely specified FSM minimization](/incompletely-specified-fsm-minimization/).
- **Ties in the order.** All groups often have weight 1, so the tie rule of line L3 decides what is kept. A different tie rule can give a different result.
- **Unused codes.** When $n < 2^k$, the unused codes are don't cares in the final minimization, and they also make more groups fit.
- **Skipping the final minimization.** The bound counts cubes before minimization. The real cost is the size of a two-level cover after minimization with [Espresso](/espresso/) or an exact minimizer.

## Implementations

## History

De Micheli, Brayton and Sangiovanni-Vincentelli (1985) introduced face constraints with KISS, which satisfies all of them with codes as long as needed. Villa and Sangiovanni-Vincentelli (1990) gave NOVA, which keeps the code length fixed, weights the constraints, and offers exact and heuristic embeddings; they reported PLA areas on a set of benchmark machines, a measurement on that set rather than a bound. De Micheli's 1994 textbook places both in a common framework of input and output encoding constraints.

## References
