---
tag: QRSANA
kind: algorithm
slug: kiss-symbolic-minimization
name: KISS symbolic minimization
aliases:
- KISS state assignment
- symbolic minimization of FSMs
area: eda/high-level-synthesis-and-scheduling
level: advanced
summary: De Micheli, Brayton and Sangiovanni-Vincentelli's method that minimizes the FSM table with symbolic states, then encodes states to satisfy the face constraints it yields.
solves: [state-assignment]
model: word-ram
complexity:
  vars: {n: the number of states, k: the code length that is returned, C: the number of face constraints, T: the time of the symbolic two-level minimization}
  time: {worst: O(T + C n 2^(k n))}
  space: {extra: O(n C + 2^k)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1985
  people: [Giovanni De Micheli, Robert K. Brayton, Alberto L. Sangiovanni-Vincentelli]
  note: De Micheli, Brayton and Sangiovanni-Vincentelli published KISS in IEEE Transactions on Computer-Aided Design in 1985, with symbolic minimization of the state table followed by the embedding of face constraints.
prereqs: [state-assignment, two-level-logic-minimization, espresso]
see_also: [nova-state-encoding, mustang-state-assignment, dfa-minimization, incompletely-specified-fsm-minimization, fsm-decomposition, partition-pair, prime-implicant, hamming-distance]
sources:
  - paper: "Giovanni De Micheli, Robert K. Brayton and Alberto L. Sangiovanni-Vincentelli, Optimal state assignment for finite state machines, IEEE Transactions on Computer-Aided Design CAD-4(3), 269 to 285, 1985"
    title: Giovanni De Micheli, Robert K. Brayton and Alberto L. Sangiovanni-Vincentelli, Optimal state assignment for finite state machines, IEEE Transactions on Computer-Aided Design CAD-4(3), 269 to 285, 1985
    locator: symbolic minimization of the state table, the face constraints, the bound on the number of product terms, and the heuristic embedding of the constraints
  - book: isbn:9780070163331
    title: Giovanni De Micheli, Synthesis and Optimization of Digital Circuits, McGraw-Hill, 1994
    locator: Chapter 9 (state encoding for two-level circuits, symbolic minimization, input and output encoding constraints)
  - paper: "Richard L. Rudell and Alberto L. Sangiovanni-Vincentelli, Multiple-valued minimization for PLA optimization, IEEE Transactions on Computer-Aided Design 6(5), 727 to 750, 1987"
    title: Richard L. Rudell and Alberto L. Sangiovanni-Vincentelli, Multiple-valued minimization for PLA optimization, IEEE Transactions on Computer-Aided Design 6(5), 727 to 750, 1987
    locator: ESPRESSO-MV, the multiple-valued two-level minimizer used for symbolic minimization
---

KISS is a method of [state assignment](/state-assignment/) for finite state machines whose logic is built as a two-level sum of products, such as a PLA. Its idea is to minimize the logic before the codes exist. The present state is treated as one multiple-valued variable, and the state table is minimized as a multiple-valued function. Each product term of the result covers a group of present states, and if every such group occupies a face of the code cube that holds no other state's code, then the encoded logic needs no more product terms than the symbolic cover. KISS then looks for short codes that meet these face constraints. De Micheli, Brayton and Sangiovanni-Vincentelli published it in 1985. This page proves the bound and shows by exhaustive search that it is only a bound: the codes that KISS returns are not the best codes for the final logic, and on the example of this page the best two-bit code breaks the only face constraint.

## In plain words

A controller has a table: in this state, on this input, go to that state and set these outputs. Before choosing bit patterns for the states, KISS simplifies the table with the state names left as names, merging rows where it can: "in state A or state B, on any input, go to C". After that, it chooses bit patterns so that every merged group of states can be named by one pattern with some bits left free, such as "first bit 0", without also naming a state outside the group. Then every merged row of the table becomes one row of the circuit. The catch is that a smaller circuit may exist with codes that break this rule.

## The problem

The input is a deterministic finite state machine, given as a table of rows (input cube, present state, next state, outputs), as on the [state assignment](/state-assignment/) page. Entries that no row specifies are don't cares. The machine should first be reduced by [DFA minimization](/dfa-minimization/), or by [incompletely specified FSM minimization](/incompletely-specified-fsm-minimization/) when it has don't cares. The output is an injective code of $k$ bits for the $n$ states. The quantity that matters is the number of product terms, and then of literals, in a minimum two-level cover of the encoded next-state and output functions, where unused codes are don't cares. KISS does not minimize this quantity; it minimizes a bound on it.

**Symbolic function.** Its variables are the input bits and one variable $S$ with the $n$ states as values. Its outputs are one output per state (the next state, one-hot) and the primary outputs. A cube has a set of values for $S$, called its group.

**Face constraint.** For codes $\mathrm{enc}$ of $k$ bits and a group $G$, the face of $G$ is the smallest subcube of $\{0, 1\}^k$ that holds $\mathrm{enc}(s)$ for every $s \in G$. The codes meet the face constraint of $G$ when this face holds no code $\mathrm{enc}(t)$ with $t \notin G$.

## The algorithm

```pseudo id=main
KISS(M)
L1  build the symbolic function of M: the inputs and S as variables, the next state one-hot and the outputs as outputs
L2  S_cover ← a minimum multiple-valued cover of it (ESPRESSO-MV in the original, exact here)
L3  F ← the groups of the cubes of S_cover with more than one state and fewer than n
L4  k ← ⌈log2 n⌉
L5  while no injective code of k bits meets every face constraint in F do k ← k + 1
L6  enc ← an injective code of k bits that meets every face constraint in F
L7  for each cube of S_cover, emit the encoded cube: its input part; the face of its group; as outputs, the next state bits that are 1 in the code of the state it asserts, and the outputs it asserts
L8  return enc and the encoded cover, which a two-level minimizer such as Espresso may shrink further
```

Line L2 is a two-level minimization in the sense of [Espresso](/espresso/), run on a function with one multiple-valued input. Line L5 is the face embedding problem. The original KISS solves it with a heuristic that may make $k$ longer than needed; the reference code here searches all codes of each length by backtracking, so it returns the least $k$ that meets every constraint, and among those codes the first one in its search order. This exact search fits only small machines. Groups of size 1 and $n$ give no constraint, since a single code is a face and the whole cube is one.

## Example

Take the machine $M_1$ with one input $x$, one output $z$ and four states:

| present | $x = 0$ | $x = 1$ |
| --- | --- | --- |
| $s_0$ | $s_2$ / 1 | $s_2$ / 0 |
| $s_1$ | $s_2$ / 0 | $s_2$ / 1 |
| $s_2$ | $s_3$ / 0 | $s_1$ / 1 |
| $s_3$ | $s_1$ / 1 | $s_3$ / 0 |

A minimum symbolic cover has 7 cubes, written as input, group, next state, output:

| cube | $x$ | group | next | $z$ |
| --- | --- | --- | --- | --- |
| 1 | - | $\{s_0, s_1\}$ | $s_2$ | |
| 2 | 0 | $\{s_3\}$ | $s_1$ | 1 |
| 3 | 1 | $\{s_2\}$ | $s_1$ | 1 |
| 4 | 0 | $\{s_2\}$ | $s_3$ | |
| 5 | 1 | $\{s_3\}$ | $s_3$ | |
| 6 | 0 | $\{s_0\}$ | $s_2$ | 1 |
| 7 | 1 | $\{s_1\}$ | $s_2$ | 1 |

The only face constraint is $\{s_0, s_1\}$. Two bits suffice, and the search returns $s_0 = 00$, $s_1 = 01$, $s_2 = 10$, $s_3 = 11$, where $\{s_0, s_1\}$ is the face $0{-}$. Line L7 turns the 7 symbolic cubes into 7 encoded cubes; cube 1 becomes "$x = -$, state $0{-}$, set the high next-state bit". By the theorem below this cover is correct, and an exact two-level minimization of the encoded function under these codes finds nothing smaller: 7 cubes and 19 literals.

Now search every code. Four states in two bits have 24 injective codes, which fall into 12 classes up to swapping the two bits, and the cost is the same within a class. An exact minimization of each class gives:

- The best class has 4 cubes and 8 literals, with $s_0 = 01$, $s_1 = 10$, $s_2 = 11$, $s_3 = 00$. Its cover is $\bar x \bar q_1$, $x q_1$ (which set the high bit and $z$) and $\bar q_1 q_0$, $q_1 \bar q_0$ (which set both bits), where $q_1 q_0$ is the code. These codes break the face constraint: the face of $01$ and $10$ is the whole square.
- The 8 classes that meet the constraint cost between 5 cubes (9 literals) and 7 cubes (19 literals). The codes that KISS returned are the worst of them.
- With three bits, the best code needs 3 cubes and 6 literals.

So meeting the face constraints is not needed for small logic, and among the codes that meet them the cost still varies from 5 to 7 cubes. The KISS bound says only that the result is at most 7.

## Correctness

The [full proof](proofs/correctness.md) shows:

- **The construction is correct.** If $\mathrm{enc}$ meets every face constraint of the symbolic cover, the encoded cubes of line L7 implement the machine: at every specified pair of input and state they give the code of the next state and the specified outputs.
- **The bound.** Hence the encoded function has a two-level cover with at most as many cubes as the symbolic cover. Cubes whose output part is empty are dropped, so it can be smaller.
- **Termination.** Line L5 stops with $k \le n$, since the one-hot code of $n$ bits meets every face constraint.

What is not proved, and is false: that the codes minimize the cubes or literals of the final logic. The example has a code with 4 cubes where KISS gives 7. As a measurement, 100 random machines with 4 states, one input bit, one output bit and every entry specified (seed 1985) were encoded by the reference code and minimized exactly. Of these, 32 needed 3 or more bits to meet all face constraints. On the 99 machines with $k \le 3$, the final logic matched the best code of the same length on 41, with 70 extra cubes in total and at most 3 on one machine. These numbers describe this small random sample only.

## Complexity

The symbolic minimization of line L2 is a two-level minimization, which is hard in general; Espresso-MV runs it as a heuristic, and the reference code runs an exact search that fits only tiny machines. Line L5 tries all injective placements of the $n$ states on the $2^k$ codes in the worst case, at most $2^{k n}$ of them for each length, checking $C$ constraints of up to $n$ states at each step, which gives the $O(C n 2^{k n})$ term. Line L7 takes $O(k n)$ time per cube. The KISS paper uses a polynomial heuristic for line L5 instead, at the price of codes longer than needed.

## Properties

- **A proved bound.** The number of product terms is at most the size of the symbolic cover, whatever code meets the constraints.
- **Not optimal.** Neither the codes nor the code length minimize the final logic. None of KISS, [NOVA](/nova-state-encoding/) and [MUSTANG](/mustang-state-assignment/) is optimal for the final logic: on the example machines of the three pages, an exhaustive search over all codes finds cheaper logic than each of them gives.
- **Code length can grow.** Meeting every constraint may need more than $\lceil \log_2 n \rceil$ bits, and so more flip-flops.
- **Input constraints only.** The face constraints come from the present state. The next state is treated as $n$ separate outputs, and the sharing of next-state bits between cubes is not used.
- **Deterministic.** The reference code always returns the same codes.

## Variants and improvements

- **NOVA.** Villa and Sangiovanni-Vincentelli (1990) fix $k$ at the least length and meet as many weighted face constraints as they can; see [NOVA](/nova-state-encoding/).
- **Output constraints.** Later work on symbolic minimization, described in De Micheli's book (Chapter 9), also extracts constraints from the next-state field, such as dominance constraints between codes, so that cubes can share next-state bits.
- **Multilevel targets.** For multilevel logic, [MUSTANG](/mustang-state-assignment/) chooses codes from attraction weights instead of face constraints.
- **Exact embedding.** For small machines the embedding of line L5 can be solved exactly, as in the reference code, which gives the least $k$ that meets every constraint.

## When to use it

Use KISS when the controller is built as a PLA or another two-level form and a guaranteed bound on the number of product terms is wanted. Treat its codes as a good start, not as the best: for small machines, an exhaustive or exact search over codes, as in the example, can find much smaller logic. When the number of flip-flops is fixed, use NOVA, which never makes the code longer.

## Pitfalls

- **Reading the title as a promise.** The 1985 paper is titled "Optimal state assignment", but the method minimizes the symbolic cover, which only bounds the logic.
- **Unreduced machines.** Equivalent states give redundant groups and constraints. Minimize the states first.
- **Long codes.** A small machine can need many bits to meet all its face constraints, as the measurements show for a third of random 4-state machines. Each extra bit is a flip-flop and a next-state function.
- **Skipping the final minimization.** The encoded cover of line L7 is only an upper bound. Running a two-level minimizer on the encoded function can remove more cubes.
- **Unused codes.** When $2^k > n$, the unused codes are don't cares. Forgetting them in the final minimization gives larger logic.

## Implementations

## History

De Micheli, Brayton and Sangiovanni-Vincentelli (1985) introduced symbolic minimization and face constraints, with the bound on product terms and a heuristic embedding. Rudell and Sangiovanni-Vincentelli (1987) built ESPRESSO-MV, the multiple-valued minimizer that such methods use. Villa and Sangiovanni-Vincentelli (1990) gave NOVA, which keeps the code length fixed and meets constraints selectively. De Micheli's 1994 textbook presents these methods together with the output constraints of later work.

## References
