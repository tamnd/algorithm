---
tag: FHMN9N
kind: algorithm
slug: podem
name: PODEM
aliases:
- path-oriented decision making
area: eda/timing-and-verification
level: core
summary: Goel's ATPG that decides values on primary inputs only, backtraces each objective to an input and simulates forward, so the search tree has at most 2^(n+1) - 1 nodes.
solves: [automatic-test-pattern-generation]
model: word-ram
complexity:
  vars: {n: the number of primary inputs, L: the number of lines, P: the number of gate input pins}
  time: {worst: "O(2^n (L + P))", best: "O(L + P)"}
  space: {extra: O(L + n)}
properties: {deterministic: true, exact: true, complete: true, recursive: false}
history:
  year: 1981
  people: [Prabhakar Goel]
  note: Goel gave PODEM in 1981 as an implicit enumeration over the primary inputs. Fujiwara and Shimono added the FAN rules in 1983.
prereqs: [automatic-test-pattern-generation, d-algorithm]
see_also: [scoap, sat-based-atpg, stuck-at-fault-model, fault-simulation, dpll, scan-design]
sources:
  - paper: "Prabhakar Goel, An implicit enumeration algorithm to generate tests for combinational logic circuits, IEEE Transactions on Computers C-30(3), 215 to 222, 1981"
    title: P. Goel, An implicit enumeration algorithm to generate tests for combinational logic circuits, IEEE Transactions on Computers C-30(3), 215 to 222, March 1981
    locator: the algorithm with decisions on primary inputs, the objective, the backtrace and the X-path check
  - paper: doi:10.1109/TC.1983.1676174
    title: H. Fujiwara and T. Shimono, On the acceleration of test generation algorithms, IEEE Transactions on Computers C-32(12), 1137 to 1144, 1983
    locator: FAN, with head lines, multiple backtrace, unique sensitization and immediate implications
  - book: isbn:9780792379911
    title: Michael L. Bushnell and Vishwani D. Agrawal, Essentials of Electronic Testing for Digital, Memory and Mixed-Signal VLSI Circuits, Kluwer, 2000
    locator: the chapter Combinational Circuit Test Generation (PODEM, its backtrace and FAN)
  - book: isbn:9780780310629
    title: Miron Abramovici, Melvin A. Breuer and Arthur D. Friedman, Digital Systems Testing and Testable Design, IEEE Press, 1994
    locator: the chapter on test generation for combinational circuits (PODEM and FAN)
---

PODEM (path-oriented decision making) is an algorithm for [automatic test pattern generation](/automatic-test-pattern-generation/). Given a combinational circuit and one [single stuck-at fault](/stuck-at-fault-model/), it finds an input vector that detects the fault, or proves that no such vector exists. Unlike the [D-algorithm](/d-algorithm/), it makes decisions only on the primary inputs. It turns each goal on an internal line into an input value by a backtrace, then finds all consequences by simulation, so it never meets an inconsistent internal value and its search tree has at most $2^{n+1} - 1$ nodes for $n$ inputs.

## In plain words

You want a fault inside a circuit to show at an output. First the faulty line must get the value opposite to its stuck value. Then the difference must travel through gates to an output.

PODEM only ever sets the circuit inputs. It picks a goal, such as "this line must be 1", and walks back from that line through gates that are still unknown until it reaches an input that is still open. It sets that input to the value that helps the goal, then simulates the good and the faulty circuit to see what is now known.

If a difference reaches an output, it is done. If the fault can no longer show, it flips the last input it chose. When both values of that input fail, it frees the input and goes back one more step.

## The problem

The input is a combinational circuit $C$ with $n$ primary inputs and $L$ lines, in topological order, and a fault $(\ell, s)$: line $\ell$ is stuck at $s \in \{0, 1\}$. The lines are the outputs of the primary inputs and gates and the fanout branches. The output is a vector over $\{0, 1, X\}$ such that every two-valued completion of it detects the fault, or the answer "untestable" if no input vector detects it.

Each line holds a pair (good value, faulty value), each in $\{0, 1, X\}$. Roth's five values name these pairs: $0 = (0, 0)$, $1 = (1, 1)$, $D = (1, 0)$, $D' = (0, 1)$, and X for any pair with an X. The D-frontier is the set of gates whose output has an X and that have an input with D or D'. An X-path is a path of lines that all have an X.

## The algorithm

```pseudo id=main
PODEM(C, (ℓ, s))
L1  set every primary input to X; stack ← empty
L2  loop
L3      simulate the good and the faulty circuit with three values
L4      if some primary output has D or D' then return the input values
L5      if ℓ is not at s in the good circuit and (ℓ has X or some D-frontier gate has an X-path to an output) then
L6          (k, v) ← OBJECTIVE()
L7          (p, u) ← BACKTRACE(k, v)
L8          set input p to u; push (p, u, not flipped)
L9      else
L10         pop each entry that is flipped and set its input to X
L11         if the stack is empty then return "untestable"
L12         flip the value of the top entry, set its input to it, and mark it flipped

OBJECTIVE()
L13 if the good value of ℓ is X then return (ℓ, ¬s)
L14 G ← a gate of the D-frontier with an X-path to an output
L15 j ← an input of G with value X
L16 return (j, the non-controlling value of G)

BACKTRACE(k, v)
L17 while k is not a primary input do
L18     j ← an input of k with value X
L19     u ← v xor inversion(k)
L20     (k, v) ← (j, u)
L21 return (k, v)
```

Here inversion(k) is 1 for NAND, NOR and NOT and 0 for the other gates and for fanout branches. For an XOR gate, line L16 asks for 0 and line L19 passes the wanted value on unchanged. Any choice at lines L14, L15 and L18 is correct. The choice only changes how fast the search ends, and the usual guide is [SCOAP](/scoap/): line L18 takes the easiest input when one input value is enough and the hardest input when all inputs need the value.

## Example

The circuit is $g = \mathrm{NAND}(a, b)$, $h = \mathrm{NAND}(b, c)$, $z = \mathrm{NAND}(g, h)$, so $z = ab + bc$. The stem $b$ has the branches $b_g$ into $g$ and $b_h$ into $h$. The fault is $h$ stuck at 0.

| pass | inputs $abc$ | values | line | action |
|---|---|---|---|---|
| 1 | XXX | all X | L13 | objective $(h, 1)$; backtrace: $h$ is a NAND, so $b_h = 0$, then $b = 0$ |
| 2 | X0X | $b = b_g = b_h = 0$, $g = 1$, $h = D$, $z = D'$ | L4 | return X0X |

Every completion of X0X, that is 000, 001, 100 and 101, detects $h$ stuck at 0, and so does 010, which PODEM did not need.

A second circuit shows a backtrack. It is $na = \mathrm{NOT}(a)$, $p = \mathrm{AND}(a, b)$, $q = \mathrm{AND}(na, c)$, $r = \mathrm{AND}(b, c)$ and $z = \mathrm{OR}(p, q, r)$, so $z = ab + \bar{a}c + bc$. The fault is $a$ stuck at 0, and the choices take the first candidate each time.

| pass | inputs $abc$ | values | action |
|---|---|---|---|
| 1 | XXX | all X | objective $(a, 1)$, which is an input: set $a = 1$ |
| 2 | 1XX | $a = D$, $na = D'$, D-frontier $\{p, q\}$ | objective: the input $b$ of $p$ to 1; set $b = 1$ |
| 3 | 11X | $p = D$, D-frontier $\{q, z\}$ | objective: the input $c$ of $q$ to 1; set $c = 1$ |
| 4 | 111 | $p = D$, $q = D'$, $r = 1$, $z = 1$ | no D-frontier is left: flip $c$ to 0 |
| 5 | 110 | $p = D$, $q = 0$, $r = 0$, $z = D$ | return 110 |

Pass 3 chose a gate on the wrong side of the reconvergent fanout of $a$: through $q$, the effect arrives at $z$ with the opposite sign. Simulation finds this at once, and one flip repairs it.

On the same circuit the fault $r$ stuck at 0 is redundant, because $bc$ is the consensus of $ab$ and $\bar{a}c$. PODEM makes 7 passes and 3 flips: it sets $b = 1$ and $c = 1$, so $r = D$, and then any value of $a$ makes $p$ or $q$ equal to 1, which blocks $z$. With $c = 0$ or $b = 0$, the line $r$ is at its stuck value. The stack becomes empty, and PODEM answers "untestable".

## Correctness

Three facts make PODEM correct. First, three-valued simulation never claims a value that some completion contradicts, so the vector returned by line L4 is a test whatever values the X inputs take. Second, the test of line L5 fails only when no completion of the current inputs is a test. If the site is at its stuck value, the two circuits agree on every line. Otherwise, any test has a path of differing lines from $\ell$ to an output, and the first line on it after the last line with D or D' is a D-frontier gate with an X-path. Third, lines L6 and L7 always find an unassigned input, so each pass goes one level deeper in a binary tree of depth at most $n$. The search walks this tree depth first and prunes only subtrees with no test. If a test exists, the branch that agrees with it is never pruned, and PODEM returns before the stack is empty. The [full proof](proofs/correctness.md) gives the details.

## Complexity

Each node of the search tree costs two simulations, the D-frontier, one sweep of the lines in reverse order to mark the X-paths, and a backtrace of at most $L$ steps, so $O(L + P)$ time, where $P$ is the number of gate input pins. The tree has at most $2^{n+1} - 1$ nodes, so the worst case is $O(2^n (L + P))$ time. This is exponential, and no polynomial bound is expected, because the problem is NP-complete. The best case is one simulation, when the first backtrace already gives a test. The extra space is the stack of at most $n$ entries and the values of the lines, $O(L + n)$.

The D-algorithm branches on internal lines, so the depth of its search tree is bounded by the number of line values, $2L$, and not by $n$. Goel's argument for PODEM was this smaller space and the absence of conflicts on internal lines. How much faster PODEM runs is a measured result on benchmark circuits, not a theorem.

## Properties

- **Complete.** For a combinational circuit, PODEM returns a test exactly when the fault is detectable, so "untestable" is a proof of redundancy.
- **Decisions on inputs only.** Every value on an internal line comes from simulation, so internal lines never hold values that conflict with each other.
- **Tests with X.** The returned vector can leave inputs at X. These free inputs help test compaction, where one vector is made to detect several faults.
- **Deterministic.** The choice rules of lines L14, L15 and L18 fix the output.
- **Combinational only.** For a sequential circuit, PODEM needs [scan design](/scan-design/), or a time frame expansion that unrolls the circuit.

## Variants and improvements

- **SCOAP guidance.** Pick the D-frontier gate with the best observability, and backtrace through the input that is easiest or hardest to control, as on the [SCOAP](/scoap/) page. This changes the order of the search, not its result.
- **FAN.** Fujiwara and Shimono (1983) keep decisions on a small set of lines but add four rules. Head lines are lines that no fanout reaches from behind, and backtrace stops at them, because a head line can always be justified later. Multiple backtrace sends several objectives back at once and counts how many want 0 or 1 at each fanout stem. Unique sensitization sets the side inputs of gates through which every path from the D-frontier must pass. Immediate implications fix forced values before the next decision.
- **Learning.** Later systems such as SOCRATES (Schulz, Trischler and Sarfert, 1988) find implications in a preprocessing pass, for example that $a = 1$ forces $b = 0$ through reconvergent fanout, and add them to simulation.
- **SAT solvers.** [SAT-based ATPG](/sat-based-atpg/) gives the same problem to a [CDCL](/cdcl/) solver, which learns clauses from conflicts. PODEM is close to [DPLL](/dpll/) with decisions on the input variables only.
- **Sequential circuits.** Unroll the circuit over several clock cycles and run PODEM on the unrolled copy, or use full scan so that every flip-flop becomes an input and an output.

## When to use it

Use PODEM, or one of its descendants such as FAN, for test generation on combinational logic or on the combinational part of a full scan design. It is a standard choice in teaching and a common base in tools, with a [fault simulator](/fault-simulation/) that removes the faults each new test also detects. For faults that it aborts after a backtrack limit, often redundant ones, a SAT-based engine is the usual second step, since it proves redundancy better.

## Pitfalls

- **A wrong X-path check.** Line L5 must look for a path of X lines from a D-frontier gate to an output. Without it, the search goes deep below a dead node and finds the dead end only at the leaves.
- **Stopping at the first D-frontier gate.** A gate of the D-frontier can be blocked while another one is still open. The X-path check must look at all of them, or the search prunes a node that still has a test.
- **Forgetting the inversion.** Line L19 must flip the wanted value at each inverting gate. A backtrace that ignores it still terminates but sets inputs to the wrong values and needs many more flips.
- **Treating "untestable" as a bug.** A redundant fault has no test. PODEM proves this only by exhausting the tree, so tools stop at a backtrack limit and report the fault as aborted, which is not the same as redundant.
- **Fanout branches.** Faults on a stem and on its branches are different faults. A circuit model without branch lines cannot target a branch fault.

## Implementations

## History

Roth's [D-algorithm](/d-algorithm/) of 1966 assigned values to internal lines and spent much time on conflicts between them. Goel (1981), at IBM, noticed that the values of all lines follow from the inputs, and called his method an implicit enumeration of the input space. He showed that it worked on error correction and translation circuits, which have much reconvergent XOR logic and were hard for the D-algorithm. Fujiwara and Shimono (1983) improved it to FAN. The search over inputs with forward simulation stayed the core of structural test generation, and SAT-based engines took over the hard faults from about 1990.

## References
