---
tag: 19GY6J
kind: problem
slug: state-assignment
name: State assignment
aliases:
- state encoding
- FSM state encoding
area: cad/logic-synthesis
level: core
summary: Choose a binary code for each state of a finite state machine so the next-state and output logic is small, NP-hard in general.
prereqs: [mealy-machine, two-level-logic-minimization]
see_also: [incompletely-specified-fsm-minimization, espresso, multi-level-logic-synthesis, sum-of-products, gray-code, hamming-distance, dont-care-condition, moore-machine]
sources:
  - paper: "Giovanni De Micheli, Robert K. Brayton and Alberto L. Sangiovanni-Vincentelli, Optimal state assignment for finite state machines, IEEE Transactions on Computer-Aided Design CAD-4(3), 269 to 285, 1985"
    title: Optimal state assignment for finite state machines
    locator: KISS, symbolic minimization of the state table, the face constraints on the codes, and their embedding in a hypercube
  - paper: doi:10.1109/43.59068
    title: Tiziano Villa and Alberto L. Sangiovanni-Vincentelli, NOVA, state assignment of finite state machines for optimal two-level logic implementation, IEEE Transactions on Computer-Aided Design 9(9), 905 to 924, 1990
    locator: the encoding of states to satisfy as many face constraints as possible with a short code, and the measured PLA areas on benchmark machines
  - paper: "E. J. McCluskey and S. H. Unger, A note on the number of internal variable assignments for sequential switching circuits, IRE Transactions on Electronic Computers EC-8(4), 439 to 440, 1959"
    title: A note on the number of internal variable assignments for sequential switching circuits
    locator: the count of the assignments that differ by more than a permutation or complementation of the state variables
  - book: isbn:9780070163331
    title: Giovanni De Micheli, Synthesis and Optimization of Digital Circuits, McGraw-Hill, 1994
    locator: Chapter 9, Sequential Logic Optimization (state encoding for two-level and multiple-level circuits)
---

State assignment chooses a distinct binary code for each state of a finite state machine. Once the codes are fixed, the next state and the outputs become Boolean functions of the input bits and the state bits, and these functions are built as logic between the state registers. Different codes give very different logic. The goal is the code that makes the logic smallest, usually measured after [two-level minimization](/two-level-logic-minimization/) as the number of product terms, or after [multi-level synthesis](/multi-level-logic-synthesis/) as a literal count. Even for one state the problem contains two-level minimization, so it is NP-hard, and the space of codes grows very fast. Practical tools such as KISS and NOVA work on a symbolic description of the machine and turn it into constraints on the codes.

## In plain words

A controller moves between named states such as "idle", "load" and "run". Hardware stores the state as bits in flip-flops, so each name needs a bit pattern. Any choice works, as long as two states never share a pattern. But the gates that compute the next pattern and the outputs depend a lot on this choice. If states that behave alike get patterns that differ in one bit, the logic can often treat them as one group and get simpler. The task is to find the patterns that make the logic small. There are too many choices to try them all, except for tiny machines.

## Definition

**Input.** A Mealy machine with a set $S$ of $n$ states, input bits $x_1, \dots, x_m$, output bits, a next state map $\delta$ and an output map $\lambda$, possibly with don't-cares. A code length $k \ge \lceil \log_2 n \rceil$. A cost model for the logic.

**Feasible solutions.** Injective maps $e : S \to \{0,1\}^k$. For a code $e$, the encoded machine has next state functions $Y_1, \dots, Y_k$ and output functions $z_j$ of $x_1, \dots, x_m, y_1, \dots, y_k$, with $Y(x, e(s)) = e(\delta(s, x))$ and $z(x, e(s)) = \lambda(s, x)$. The $2^k - n$ unused codes, and the don't-cares of the machine, are don't-cares of these functions.

**Objective.** Minimize the cost of a minimized implementation of $Y$ and $z$: for example the number of distinct product terms of a minimum two-level cover (the rows of a PLA), the pair (cubes, literals), or the literal count of a multi-level network.

**Decision version.** Given the machine, $k$, the cost model and a bound $c$, is there a code whose minimized logic costs at most $c$?

## Variants

- **Code length.** Minimum length $k = \lceil \log_2 n \rceil$, which needs the fewest flip-flops; a free length; or one-hot codes with $k = n$, where each state has its own flip-flop.
- **Two-level or multi-level cost.** A PLA cost counts product terms. A multi-level cost counts literals after factoring, which rewards common subexpressions instead of large cubes.
- **Input encoding.** Only the use of the state as an input of the logic is considered: states that the minimized logic treats as one group should have codes that span a face of the hypercube, and no other code should lie in that face.
- **Output encoding.** Only the use of the state as an output is considered: the code of a next state should let the logic for $Y$ share terms, for example when one code covers another bit by bit.
- **Low power.** The cost is the expected number of bits that change on a transition, weighted by how often each transition occurs, so frequent transitions get codes at small [Hamming distance](/hamming-distance/).
- **Encoding of other symbols.** The same problem arises for any symbolic signal, such as an opcode or a bus command.

## Examples

Take a Mealy machine with states $S_0, \dots, S_3$, one input bit $x$ and one output bit $z$. All four states are distinct, so none can be merged.

| state | next, $x = 0$ | next, $x = 1$ | $z$, $x = 0$ | $z$, $x = 1$ |
|---|---|---|---|---|
| $S_0$ | $S_2$ | $S_1$ | 1 | 0 |
| $S_1$ | $S_0$ | $S_3$ | 0 | 1 |
| $S_2$ | $S_2$ | $S_0$ | 0 | 0 |
| $S_3$ | $S_0$ | $S_2$ | 0 | 0 |

With $k = 2$ there are $4! = 24$ codes. The cost below is the pair (cubes, literals) of minimum sums of products for $Y_1$, $Y_0$ and $z$, each output on its own. Two codes put the same pairs of states at Hamming distance 1 exactly when they differ by a permutation and a complementation of the bits, so the 24 codes fall into 3 classes of 8. An exhaustive search gives:

| pairs at distance 1 | costs in the class |
|---|---|
| $S_0 S_1$, $S_0 S_2$, $S_1 S_3$, $S_2 S_3$ | from (5, 12) to (6, 12) |
| $S_0 S_2$, $S_0 S_3$, $S_1 S_2$, $S_1 S_3$ | (6, 16) or (7, 15) |
| $S_0 S_1$, $S_0 S_3$, $S_1 S_2$, $S_2 S_3$ | (9, 25) for all 8 codes |

The best code is $S_0 = 00$, $S_1 = 01$, $S_2 = 10$, $S_3 = 11$, with state bits $y_1 y_0$:
$$Y_1 = \bar{x}\bar{y}_0 + x y_0, \qquad Y_0 = x \bar{y}_1, \qquad z = \bar{x}\bar{y}_1\bar{y}_0 + x \bar{y}_1 y_0.$$
In the worst class, $Y_1$ alone needs 4 cubes and 12 literals, since it behaves like a parity function. Note that complementing a bit can change the cost inside a class, from (5, 12) to (6, 12) here, because it complements the next state function of that bit. For every code, the encoded machine was simulated against the original on all input sequences of length up to 6.

## Known algorithms

- **Exhaustive search.** Try every code, or one code per class, and minimize the logic for each. Feasible only for very small machines.
- **Adjacency heuristics.** Give a weight to each pair of states, high when the pair has the same next state, the same output, or a common predecessor on the same input. Then embed the states in the hypercube so that heavy pairs get codes at Hamming distance 1. This is a weighted graph embedding, solved greedily or by [simulated annealing](/simulated-annealing/).
- **Symbolic minimization and face constraints.** KISS (De Micheli, Brayton and Sangiovanni-Vincentelli 1985). Minimize the state table as a multiple-valued function, with the present state as one symbolic variable. Each product term of the result groups some states, and gives a face constraint: those states must span a face that holds no other state code. If all constraints hold, the encoded logic needs no more product terms than the symbolic cover. Then find a short code that meets the constraints.
- **NOVA.** Villa and Sangiovanni-Vincentelli (1990). With a fixed short code length, satisfy as many face constraints as possible, weighted by their gain, by exact or heuristic embedding.
- **Multi-level methods.** Weight the pairs of states by the common factors that they would allow after encoding, and embed as above.
- **One-hot and simple codes.** One-hot codes with $n$ flip-flops, binary counting codes, or [Gray codes](/gray-code/) for machines that step through states in order. These need no search.

## Bounds

**Upper bounds (proved).**

- The number of codes of length $k$ is $2^k! / (2^k - n)!$, so exhaustive search is finite but grows faster than exponentially in $n$. McCluskey and Unger (1959) counted the codes that remain when two codes that differ only by a permutation or a complementation of the bits are counted once. For $n = 4$ and $k = 2$ this leaves 3, as in the example.
- With a cost of product terms and the machine given as a table, the decision version is in NP: a code and a cover of at most $c$ product terms are a certificate, checked on all rows of the encoded table.
- If a code meets all face constraints of a minimum symbolic cover, the encoded two-level logic has at most as many product terms as that cover (De Micheli, Brayton and Sangiovanni-Vincentelli 1985). This makes the symbolic minimum an upper bound for the best code that meets the constraints.

**Lower bounds (proved, as hardness).**

- The problem is NP-hard for the two-level cost. A machine with one state needs no state bits, and its output logic is the given output table. So state assignment of one-state machines is [two-level minimization](/two-level-logic-minimization/) from a truth table, which is NP-hard.
- Every code needs $k \ge \lceil \log_2 n \rceil$ bits, since the codes are distinct.

**Measured.** The KISS and NOVA papers report the PLA areas of their encodings on sets of benchmark machines, and compare them with other encodings. These are measurements on those machines, not proved bounds, and they show only that the methods help on those sets.

## Reductions

- **From two-level minimization.** By the one-state machine above.
- **To symbolic minimization and constraint satisfaction.** KISS splits the problem into a multiple-valued minimization, as in [Espresso](/espresso/), and the satisfaction of face constraints on the codes.
- **To graph embedding.** The adjacency heuristics reduce the problem to embedding a weighted graph in the hypercube $\{0,1\}^k$ with the least total weight of edges between codes at large distance.
## Applications

- **Controller synthesis.** Every synchronous controller described as a state table, for example in an HDL with an enumerated state type, needs a code. Synthesis tools choose it, often after [state minimization](/incompletely-specified-fsm-minimization/).
- **FPGAs.** One-hot codes use more flip-flops but give small next state logic for each flip-flop, which suits devices with many flip-flops and small lookup tables.
- **Low power.** Codes that keep the frequent transitions at small Hamming distance reduce switching in the state register and the logic.
- **Safe machines.** Codes with spare distance between states can detect a flip of one state bit.

## References
