---
tag: 3RBAMV
kind: technique
slug: time-frame-expansion
name: Time-frame expansion
aliases:
- iterative logic array model
- sequential circuit unrolling
area: eda/test-and-diagnosis
level: core
summary: Unrolls a sequential circuit into copies of its combinational logic, one per clock cycle, so combinational ATPG can find test sequences.
prereqs: [automatic-test-pattern-generation, podem, stuck-at-fault-model]
see_also: [scan-design, bounded-model-checking, mealy-machine, breadth-first-search, ternary-simulation, d-algorithm, sat-based-atpg, static-learning]
sources:
  - paper: doi:10.1109/T-C.1971.223315
    title: G. R. Putzolu and J. P. Roth, A heuristic algorithm for the testing of asynchronous circuits, IEEE Transactions on Computers C-20(6), 639 to 647, 1971
    locator: the extension of the D-algorithm to sequential circuits through the iterative array model of the circuit
  - paper: doi:10.1109/TC.1976.1674663
    title: P. Muth, A nine-valued circuit model for test generation, IEEE Transactions on Computers C-25(6), 630 to 636, 1976
    locator: the nine values (good value, faulty value), each 0, 1 or X, needed because the fault is present in every copy of the iterative array
  - paper: "T. M. Niermann and J. H. Patel, HITEC: a test generation package for sequential circuits, Proceedings of the European Design Automation Conference, 214 to 218, 1991"
    title: T. M. Niermann and J. H. Patel, HITEC, a test generation package for sequential circuits, Proceedings of the European Design Automation Conference, 214 to 218, 1991
    locator: forward and reverse time processing with a PODEM-based generator, without scan or a reset state
  - paper: "K.-T. Cheng, Gate-level test generation for sequential circuits, ACM Transactions on Design Automation of Electronic Systems 1(4), 405 to 442, 1996"
    title: K.-T. Cheng, Gate-level test generation for sequential circuits, ACM Transactions on Design Automation of Electronic Systems 1(4), 405 to 442, 1996
    locator: the survey of iterative logic array methods, forward and reverse time processing, and the cost of many time frames
  - book: isbn:9780780310629
    title: Miron Abramovici, Melvin A. Breuer and Arthur D. Friedman, Digital Systems Testing and Testable Design, IEEE Press, 1994
    locator: the chapter on test generation for sequential circuits (the iterative array model)
---

Time-frame expansion turns test generation for a sequential circuit into test generation for a combinational one. A synchronous sequential circuit is a block of combinational logic and a set of flip-flops, and in each clock cycle the logic computes the outputs and the next state from the inputs and the present state. To look at $k$ clock cycles at once, make $k$ copies of the combinational logic, one per cycle, and wire the next-state outputs of each copy to the present-state inputs of the next one. The result is a combinational circuit, an *iterative logic array*, and a combinational test generator such as the [D-algorithm](/d-algorithm/), [PODEM](/podem/) or [SAT-based ATPG](/sat-based-atpg/) can search it. A test for the array is a sequence of $k$ input vectors that detects the fault. This page proves that the method is exact for a given number of frames, that a bound on the number of frames makes it complete, and that the number of frames needed can grow exponentially with the number of flip-flops.

## In plain words

A circuit with memory gives different answers to the same input, depending on what it has stored. So a test is not one input but a list of inputs, given one per clock tick, starting from a known reset.

The trick is to draw the circuit once for each clock tick and connect the drawings in a row: what one tick stores is what the next tick reads. The row has no memory any more. It is just a big circuit with the inputs of every tick at once, so the usual tools for circuits without memory can find a test in it. If no test fits in a row of a given length, make the row longer and try again. The bad news is that some faults need a very long row.

## When it applies

- The circuit is synchronous: one clock, and $m$ flip-flops that all load their next state at each clock edge. Its combinational part $C$ has the primary inputs and the present-state lines $q_1, \ldots, q_m$ as inputs, and the primary outputs and the next-state lines $d_1, \ldots, d_m$ as outputs. As a machine it is a [Mealy machine](/mealy-machine/) with $2^m$ states.
- The circuit starts in a known reset state, the same in the good and the faulty machine. (Without one, see Variations.)
- The flip-flops are not in a scan chain, or only some of them are. With full [scan design](/scan-design/), every flip-flop is a primary input and output of test mode, and combinational test generation on $C$ is enough.
- The fault is permanent, such as a single stuck-at fault on a line of $C$ as in the [stuck-at fault model](/stuck-at-fault-model/). It is then present in every clock cycle.

## The template

An **iterative logic array** is a combinational circuit made of identical cells in a row. Cell $t$ has its own inputs and outputs, and it also passes some signals to cell $t + 1$, which reads them as inputs. A ripple-carry adder is one, with the carry as the signal passed on. Time-frame expansion builds an iterative logic array whose cell is $C$, whose passed signals are the state lines, and whose cell $t$ stands for clock cycle $t$, also called **time frame** $t$.

```pseudo id=main
TIME-FRAME-EXPANSION(C, reset state s0, fault f, k_max)
L1  for k ← 1 to k_max
L2      A ← k copies C1, …, Ck of the combinational logic C
L3      connect the next-state outputs of Ct to the present-state inputs of Ct+1
L4      fix the present-state inputs of C1 to s0
L5      put the fault f in every copy
L6      T ← a complete combinational test generator on A, with the primary outputs of all copies as outputs
L7      if T is a test then return the primary input vectors of C1, …, Ck in T
L8  return no test of at most k_max vectors
```

The holes are the combinational test generator at line L6 and the logic values it uses. Two-valued or three-valued values, with one copy of the array for the good machine and one for the faulty one, are enough for an exact method. A test generator that works on one array with D-style values needs the nine values of Muth: pairs (good value, faulty value) in which each part is 0, 1 or X, because the fault effect can enter a frame through the state lines and through the fault site at the same time.

**Why it is exact for $k$ frames.** For every sequence of input vectors $v_1, \ldots, v_k$, simulating the array with $v_t$ on the primary inputs of $C_t$ gives, in copy $t$, the outputs and next state of cycle $t$ of the sequential machine. This holds for the good machine and, with the fault in every copy, for the faulty one. The proof is by induction on $t$. In cycle 1 the machine is in $s_0$, and copy 1 reads $s_0$ by line L4. If copy $t$ has the state of cycle $t$, it computes the same function as the machine in that cycle, so its next-state outputs are the state of cycle $t + 1$, which copy $t + 1$ reads by line L3. So the array has a test exactly when some sequence of $k$ vectors makes some output of some cycle differ. A sequence of $j < k$ vectors that detects the fault still detects it after any $k - j$ more vectors, because later inputs do not change earlier outputs. So the $k$-frame array has a test exactly when some sequence of at most $k$ vectors detects the fault, and the loop at line L1 returns a shortest test sequence. If the search at line L6 uses X values, a test it reports is still a test of every completion, because three-valued simulation is monotone, as on the [ternary simulation](/ternary-simulation/) page.

**Why $4^m$ frames are enough.** Look at the pair (good state, faulty state) at the start of each cycle. From the pair and the input vector, the outputs of both machines and the next pair follow. Take a shortest test $v_1, \ldots, v_T$, which detects the fault only in cycle $T$. If the pairs at the start of cycles $i < j \le T$ were equal, dropping $v_i, \ldots, v_{j-1}$ would give a shorter sequence that reaches the same pair at the start of cycle $i$ and then sees the same inputs, so it would also detect the fault, which is a contradiction. So the $T$ pairs are all different, and $T$ is at most the number of pairs reachable from $(s_0, s_0)$, which is at most $2^m \cdot 2^m = 4^m$. With $k_{\max} \ge 4^m$, the answer "no test" at line L8 is a proof that no input sequence from reset detects the fault. The bound counts all pairs. In practice tools use far smaller limits, and their "no test" then says nothing about longer sequences.

**Why the number of frames can be exponential.** Take an $m$-bit counter with an enable input $e$: in each cycle it adds $e$ to its count, with the next-state logic $d_0 = q_0 \oplus e$, $c_1 = e$ AND $q_0$, $d_i = q_i \oplus c_i$, $c_{i+1} = c_i$ AND $q_i$, and the output $z = q_{m-1} \cdots q_0$. The reset state is 0. The fault $z$ stuck-at 0 (for $m \ge 2$, $z$ feeds only the output) leaves the state alone, and the faulty $z$ is always 0. The good $z$ is 1 only when the count is $2^m - 1$. The count grows by at most 1 per cycle, so in cycle $t$ it is at most $t - 1$, and $z$ can first be 1 in cycle $2^m$, after $2^m - 1$ cycles with $e = 1$. So every test needs at least $2^m$ vectors, and the array that finds one has $2^m$ copies of $C$, each with $\Theta(m)$ lines. The size of the array, not only the search in it, is exponential in the number of flip-flops. The scan design page shows the same effect on a 3-bit counter without the enable, where $z$/0 needs 7 clock edges.

**Example.** Take the 2-bit counter with enable: $d_0 = q_0 \oplus e$, $c_1 = e q_0$, $d_1 = q_1 \oplus c_1$ and $z = q_1 q_0$, reset to $q_1 q_0 = 00$. With the stems $e$, $q_0$ and $q_1$ split into branches, $C$ has 14 lines and 28 single stuck-at faults. Target $z$/0.

| frames $k$ | inputs of the array | result |
|---|---|---|
| 1 | $e_1$ | no test: $q_1 q_0 = 00$ in frame 1, so the good $z_1 = 0$ |
| 2 | $e_1, e_2$ | no test: the count in frame 2 is at most 1 |
| 3 | $e_1, e_2, e_3$ | no test: the count in frame 3 is at most 2 |
| 4 | $e_1, \ldots, e_4$ | test $e = 1, 1, 1$, then any value |

With the test $1, 1, 1, 0$ the states in frames 1 to 4 are 00, 01, 10 and 11, the good $z$ is 0, 0, 0, 1 and the faulty $z$ is 0 in every frame, so the outputs differ in frame 4. The 4-frame array has 56 lines and 4 free inputs. A breadth-first search over pairs of states finds that every one of the 28 faults is detectable from reset, with shortest tests of 1 to 4 vectors. For example $z$/1 needs 1 vector, and $e$/0 and $e$/1 need 4.

**Cost.** The array for $k$ frames has $k L$ lines for $L$ lines of $C$. Combinational test generation is NP-complete in the size of its circuit, so the search at line L6 can take time exponential in $k$ times the number of primary inputs, and the loop over $k$ repeats it. This is why sequential test generation is so much harder than combinational test generation, and why scan design exists.

**Tests.** The implementation builds the array as $k$ copies of the line list of $C$, searches it with a complete branch and bound over the primary inputs, and is checked against brute force. On random sequential circuits with up to 2 inputs, 2 flip-flops and a random reset state, simulating the array equals simulating the machine cycle by cycle, the $k$-frame array has a test exactly when one of the $2^{k n}$ input sequences of length $k$ detects the fault, and the shortest test that time-frame expansion finds has the length found by [breadth-first search](/breadth-first-search/) over pairs of states, for every fault. For the counter, breadth-first search gives shortest tests of exactly $2^m$ vectors for $m = 1$ to 6, and the array search finds no test in $2^m - 1$ frames for $m = 1$ to 3.

## Classic examples

- **Sequential ATPG.** Test generators for circuits without scan, from the extension of the D-algorithm by Putzolu and Roth (1971) to HITEC (Niermann and Patel, 1991), work on an iterative logic array, often one frame at a time.
- **Partial scan.** When the flip-flops left out of scan form no cycle, the circuit is a pipeline, and a number of frames equal to its sequential depth is enough. Partial scan picks the scanned flip-flops to make this true, as the [scan design](/scan-design/) page explains.
- **Delay test.** A two-pattern test for a [transition fault](/transition-fault-model/) is a test in two time frames. Launch on capture builds exactly this 2-frame array, as on the [launch-on-capture and launch-on-shift](/launch-on-capture-and-launch-on-shift/) page.
- **Bounded model checking.** [Bounded model checking](/bounded-model-checking/) unrolls a design for $k$ steps in the same way and asks a SAT solver for a path to a bad state. Its completeness threshold plays the role of the $4^m$ bound here.

## Variations

- **Forward time processing.** Start with the frame that activates the fault and add frames forward until the effect reaches an output.
- **Reverse time processing.** Then justify the state that the first frame needs by adding frames backward, until the needed state is the reset state or has no constraint.
- **No reset.** Without a reset, the initial state is all X, and a test must detect the fault for every initial state. Three-valued simulation of that X is safe but pessimistic, so a method based on it can miss tests that exist.
- **One frame at a time.** Tools keep only a few frames in memory and move the window, trading completeness for memory.
- **SAT on the array.** [SAT-based ATPG](/sat-based-atpg/) turns the whole $k$-frame array, with the good and the faulty machine, into one formula, as bounded model checking does.
- **Learning across frames.** Implications learned between frames, as in [static learning](/static-learning/), cut the search in the array.

## Pitfalls

- **Putting the fault in one frame only.** The fault is in the hardware, so it is in every copy. A fault in one copy models a different defect.
- **Forgetting the faulty state.** The faulty machine can reach states that the good machine never reaches, so the effect can hide in the state for many cycles. The bound counts pairs, not good states.
- **Reading a frame limit as a proof.** "No test in 10 frames" says nothing about 11 frames, as the counter shows. Only a limit of at least the number of reachable state pairs proves that a fault is undetectable from reset.
- **Undetectable from reset is not redundant.** A fault can be undetectable from reset and still change the behavior from another state. Scan can make it testable.
- **Size.** The array grows linearly with $k$, and the number of frames needed can grow exponentially with $m$. Long sequential tests are the reason scan is used.

## Exercises

1. In the 2-bit counter, why does $e$/1 need 4 vectors? Give a shortest test.
2. Prove that the $k$-frame array for a pipeline with no feedback and sequential depth $d$ has a test for a fault whenever any longer array has one, for $k \ge d + 1$.
3. Change the counter so that its only primary output is the next-state line $d_{m-1}$, and target the fault on the branch of $d_{m-1}$ that drives that output, stuck-at 0. How many frames does a test need now?

## References
