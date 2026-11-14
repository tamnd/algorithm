---
tag: KS79ZE
kind: algorithm
slug: critical-path-tracing
name: Critical path tracing
aliases:
- Abramovici critical path tracing
area: eda/test-and-diagnosis
level: advanced
summary: Finds the faults a vector detects by tracing back from the outputs through the gate inputs whose flip flips the output, with an explicit check at fanout stems.
solves: [fault-simulation]
model: word-ram
complexity:
  vars: {T: the number of vectors, L: the number of lines, P: the number of gate input pins, S: the number of fanout stems}
  time: {worst: "O(T (L + P) (1 + S))"}
  space: {extra: O(L)}
properties: {deterministic: true, exact: true, recursive: false}
history:
  year: 1983
  people: [Miron Abramovici, P. R. Menon, D. T. Miller]
  note: Abramovici, Menon and Miller presented critical path tracing at DAC 1983 and in IEEE Design and Test of Computers in 1984.
prereqs: [fault-simulation, stuck-at-fault-model]
see_also: [deductive-fault-simulation, ppsfp, parallel-fault-simulation, concurrent-fault-simulation, dominator-tree, transition-density, critical-path, fault-coverage]
sources:
  - paper: "M. Abramovici, P. R. Menon and D. T. Miller, Critical path tracing: an alternative to fault simulation, IEEE Design and Test of Computers 1(1), 83 to 93, 1984"
    title: M. Abramovici, P. R. Menon and D. T. Miller, Critical path tracing, an alternative to fault simulation, IEEE Design and Test of Computers 1(1), 83 to 93, February 1984
    locator: the method, with sensitive inputs, the backward trace inside fanout-free regions and the rules for stems
  - paper: "M. Abramovici, P. R. Menon and D. T. Miller, Critical path tracing: an alternative to fault simulation, Proceedings of the 20th Design Automation Conference, 214 to 220, 1983"
    title: M. Abramovici, P. R. Menon and D. T. Miller, Critical path tracing, an alternative to fault simulation, Proceedings of the 20th Design Automation Conference, 214 to 220, 1983
    locator: the conference version of the method
  - paper: "F. Maamari and J. Rajski, A method of fault simulation based on stem regions, IEEE Transactions on Computer-Aided Design 9(2), 212 to 220, 1990"
    title: F. Maamari and J. Rajski, A method of fault simulation based on stem regions, IEEE Transactions on Computer-Aided Design 9(2), 212 to 220, 1990
    locator: exact stem analysis by explicit simulation of the stems, limited to the stem region of each stem
  - book: isbn:9780780310629
    title: Miron Abramovici, Melvin A. Breuer and Arthur D. Friedman, Digital Systems Testing and Testable Design, IEEE Press, 1994
    locator: the chapter on fault simulation (critical path tracing, fanout-free regions and stem analysis)
---

Critical path tracing is a method for [fault simulation](/fault-simulation/) that finds, for one vector, every line whose value change would reach a primary output. Such a line is called critical, and the vector detects it stuck at the opposite of its good value. Inside a fanout-free region the critical lines follow from the good values alone, by a backward trace from the root. At a fanout stem, the trace cannot decide criticality from the branches, so this page checks each stem by an explicit simulation of its flip. The cost per vector depends on the number of stems, not on the number of faults.

## In plain words

Run the good circuit on one input. Then ask, for each wire, a simple question: if this wire had the other value, would an output change? If yes, a break that holds the wire at the other value is found by this input.

Start at an output and walk back. A gate input passes a change through when the other inputs let it through. For an AND gate, if all inputs are 1, each input passes a change. If one input is 0, only that input passes a change. If two inputs are 0, no single input does.

Where a wire splits into several wires and the parts meet again later, the walk back cannot tell the answer. There, flip the wire and simulate forward to see.

## The problem

The input is a combinational circuit $C$ with $L$ lines in topological order, a list of single stuck-at faults, a sequence of two-valued input vectors, and a flag for fault dropping. The lines are the primary inputs, the gate outputs and the fanout branches, and $P$ is the number of gate input pins. The output is, for each vector, the set of faults that it detects among those still simulated.

For a vector $t$, a line $k$ is critical if changing the value of $k$ alone from $g(k)$ to $\lnot g(k)$ changes some primary output. The fault $k$ stuck at $v$ is detected by $t$ exactly when $v = \lnot g(k)$ and $k$ is critical, since the faulty circuit is the good one with $k$ forced to $v$. So the detected faults follow from the set of critical lines. This set is the set of lines with a nonzero [Boolean difference](/transition-density/) of some output at the vector.

The name has no relation to the [critical path](/critical-path/) of a task graph or the longest path of [static timing analysis](/static-timing-analysis/). Here a critical path is a chain of critical lines from a line to an output.

## The algorithm

A gate input is **sensitive** under $t$ if flipping it alone flips the gate output. For a gate with controlling value $c$ (0 for AND and NAND, 1 for OR and NOR), if no input is at $c$, all inputs are sensitive. If exactly one input is at $c$, only that input is sensitive. If two or more inputs are at $c$, no input is sensitive. For a buffer, an inverter, a fanout branch, XOR and XNOR, every input is sensitive.

The lines with exactly one fanout belong to the fanout-free region of that fanout. The other lines are the roots: primary outputs, which have no fanout in the line model, and fanout stems. Each region is a tree that ends at its root. Inside a region, a line is critical exactly when its chain of gate inputs to the root is sensitive at every step and the root is critical. An output root is critical. A stem root is checked by flipping it and simulating forward.

```pseudo id=main
CRITICAL-PATH-TRACING(C, vectors, faults, drop)
    alive ← faults
L1  for each vector t do
L2      simulate the good circuit on t, which gives g(k) for every line k
L3      for each root r (a line whose fanout count is not 1) do
L4          if r is a primary output then r is critical
L5          else if r is a stem then flip r, simulate forward; r is critical if an output changes
L6          if r is critical then push r on a stack; while the stack is not empty do pop k
L7              mark k critical
L8              for each sensitive input j of the gate of k do
L9                  if j has exactly one fanout then push j
L10     D ← {k stuck at ¬g(k) : k critical} ∩ alive; report D as detected by t
L11     if drop then alive ← alive ∖ D
```

Line L9 stops the trace at a stem: a stem is the root of its own region, and line L5 decides it. A line with no fanout that is not an output is never critical. The forward simulation of line L5 needs only the cone of the stem and stops at the first output that changes.

## Example

The circuit is $g = \mathrm{NAND}(a, b)$, $h = \mathrm{NAND}(b, c)$, $z = \mathrm{NAND}(g, h)$, so $z = ab + bc$. The stem $b$ has the branches $b_g$ into $g$ and $b_h$ into $h$. The roots are $z$ and $b$. All other lines have one fanout and lie in the region of $z$.

Take the vector $abc = 101$, so $g = 1$, $h = 1$ and $z = 0$. The trace starts at $z$. Neither input of $z$ is at 0, so both $g$ and $h$ are sensitive. The gate $g$ has $a = 1$ and $b_g = 0$, so only $b_g$ is sensitive. In the same way only $b_h$ is sensitive at $h$. The branches lead to the stem $b$, where the trace stops. The check of $b$ flips it to 1, which gives $g = 0$, $h = 0$ and $z = 1$, so $b$ is critical. The critical lines are $b$, $b_g$, $b_h$, $g$, $h$, $z$, and the vector detects b/1, $b_g$/1, $b_h$/1, g/0, h/0 and z/1.

Two vectors show why the stems need a check.

| circuit | vector | critical lines | stem | branches |
|---|---|---|---|---|
| $z = \mathrm{NAND}(\mathrm{NAND}(a, b), \mathrm{NAND}(b, c))$ | 111 | $b$, $z$ | $b$ critical | no branch critical |
| $z = \mathrm{OR}(\mathrm{AND}(a, b), \mathrm{AND}(\lnot a, c))$ | 111 | $a_p$, $b$, $p$, $z$ | $a$ not critical | $a_p$ critical |

In the first row, both inputs of $z$ are at 0, so no input of $z$ is sensitive and the trace marks only $z$. But flipping $b$ flips both $g$ and $h$ to 1, and $z$ changes. The stem is critical through two paths together, while no branch is critical alone. In the second row, $p = \mathrm{AND}(a_p, b)$ is the only input at 1 of the OR, so the branch $a_p$ is critical. Flipping the stem $a$ to 0 gives $p = 0$ but also $q = \mathrm{AND}(\lnot a, c) = 1$, so $z$ stays 1. The two paths cancel each other. So the criticality of a stem is not a function of the criticality of its branches.

For the sequence 101, 010, 011, 110, the method reports the same first detections as the table of the [fault simulation](/fault-simulation/) page. It makes 4 stem checks with 19 gate evaluations in them. For the c17 benchmark circuit with all 32 vectors in counting order, the three stems of c17 give 96 checks with 526 gate evaluations, whatever the dropping. These are counts of the code of this page on a 6-gate toy circuit, not benchmark results.

## Correctness

Inside a fanout-free region, let $\ell$ be a line and $\ell = k_0, k_1, \ldots, k_m = r$ its chain of single fanouts to the root $r$. The lines that $\ell$ can change are the chain and the lines that $r$ can change. So the side inputs of each gate on the chain keep their good values when $\ell$ flips, and $\ell$ flips $k_{i+1}$ exactly when $k_i$ is a sensitive input, given that $k_i$ flips. By induction along the chain, flipping $\ell$ flips $r$ exactly when every step is sensitive, and then the circuit sees the same change as when $r$ flips. So $\ell$ is critical exactly when the chain is sensitive and $r$ is critical. This is what lines L6 to L9 compute. An output root is critical by definition, and line L5 decides a stem root by its definition. So every line is marked exactly when it is critical, and line L10 reports exactly the detected faults.

The explicit check is needed. The multiplexer at 110 has the same branch pattern as at 111, $a_p$ critical and $a_n$ not, but there the stem $a$ is critical, since $c = 0$ keeps $q$ at 0. So no rule over the branches decides a stem. If the branches of a stem do not reconverge, the stem is critical exactly when some branch is. The [full proof](proofs/correctness.md) gives the induction, the counterexamples and the case with no reconvergence.

## Complexity

The good simulation costs $O(L + P)$. Every line other than a root lies in exactly one region, and the trace visits it at most once, with $O(\text{fanin})$ work to find its sensitive inputs, so all traces cost $O(L + P)$. Each of the $S$ stem checks simulates forward in the cone of the stem, at most $O(L + P)$, plus a log factor for the priority queue of the code. A vector costs $O((L + P)(1 + S))$, and $T$ vectors cost $O(T (L + P)(1 + S))$. The extra space is $O(L)$ for the good values, the marks and one stem check.

The bound does not depend on the number of faults $F$, which is about $2L$. Serial simulation costs $O(T (L + P) F)$, so the gain is large when stems are few compared to lines. When stems are many, the checks dominate, and fault dropping does not reduce them, since a stem must be decided for the lines of its region even when its own faults are dropped. Only the lines of its own region need the answer for a stem, so a stem whose region holds no alive fault can be skipped. The code of this page does not do that.

## Properties

- **Exact, with explicit stem checks.** With line L5 as written, the result equals serial fault simulation for two-valued vectors on a combinational circuit, with or without dropping. The original method decided stems by rules on the traces and was approximate in some cases of reconvergence.
- **Fault-free trace.** Inside regions, no faulty circuit and no fault list is formed. The trace uses only the good values.
- **Independent of the fault list.** The critical lines are the same for all alive faults. Dropping changes only the report at line L10.
- **Detects only.** The method gives the lines that a single flip makes visible. It does not give the faulty output values, which a [fault dictionary](/fault-dictionary/) needs.
- **Two values.** Sensitivity needs known values on the side inputs. With an unknown value X, a side input may or may not block, and the trace is no longer exact.

## Variants and improvements

- **Stem regions.** Maamari and Rajski bound, for each reconvergent stem, the region outside of which its flip need not be simulated, and simulate the stem flip only inside it. Stems whose branches do not reconverge need no simulation at all: such a stem is critical exactly when some branch is.
- **Dominators.** If every path from a stem to the outputs passes through one line $d$, a [dominator](/dominator-tree/) of the stem, then the stem is critical exactly when its flip reaches $d$ and $d$ is critical. So the forward simulation can stop at $d$.
- **Bit-parallel tracing.** The good values of $w$ vectors fit in one word as in [PPSFP](/ppsfp/), and the sensitivity of each input becomes a word, so the trace and the stem checks run for $w$ vectors at once.
- **Mixed with other simulators.** Combining critical path tracing inside regions with [deductive](/deductive-fault-simulation/) or parallel simulation of the stems is a common split: the regions hold most lines, and the stems are few.

## When to use it

Use critical path tracing to grade a large set of two-valued vectors on a combinational circuit, or the combinational part of a full-scan design, when most faults are not on reconvergent stems. It is well suited to random or pseudo-random patterns, where fault dropping helps little at first and the cost per vector should not grow with the number of faults. For circuits with many reconvergent stems, [PPSFP](/ppsfp/) or the stem-region variant is often faster. For sequential circuits with unknown states, use [concurrent fault simulation](/concurrent-fault-simulation/).

## Pitfalls

- **Inferring stems from branches.** Marking a stem critical when one branch is critical, or not critical when no branch is, gives wrong answers. The table of the example has a case of each kind.
- **Tracing through a stem.** If the trace passes a stem as if it had one fanout, it uses only one branch and misses the effect of the others. The trace must stop at line L9 and leave the stem to line L5.
- **Treating two controlling inputs as sensitive.** With two or more inputs at the controlling value, no single input is sensitive, although a pair of them is. A stem that feeds both of them is decided by its check.
- **XOR as AND.** Every input of an XOR is sensitive, whatever the values.
- **Reporting both faults of a line.** A critical line gives only the fault at the opposite of its good value.

## Implementations

## History

Abramovici, Menon and Miller presented critical path tracing at the Design Automation Conference in 1983 and in the first issue of IEEE Design and Test of Computers in 1984, as an alternative to fault simulation that does not handle faults one by one. Their stem analysis used rules over the traces, which are approximate in some cases of reconvergent fanout. Later work made the method exact by simulating the stems explicitly, and Maamari and Rajski in 1990 bounded the part of the circuit that each stem check must simulate. The trace inside fanout-free regions became a standard part of fast fault simulators for combinational and full-scan circuits.

## References
