---
tag: XHG8NR
kind: algorithm
slug: observability-based-coverage
name: Observability-based coverage
aliases:
- OCCOM
- tag coverage
area: eda/hardware-verification
level: research
summary: Devadas, Ghosh and Keutzer's metric, made fast by OCCOM, that propagates tags from each assignment and counts it covered only if an error there would reach an output.
model: word-ram
complexity:
  vars: {n: "the number of lines, all of them tag sites", P: the number of gate input pins, V: the number of vectors, w: the word size}
  time: {worst: "O(V P n / w)"}
  space: {extra: "O(n^2 / w)"}
properties: {deterministic: true, exact: false, recursive: false}
history:
  year: 1996
  people: [Srinivas Devadas, Abhijit Ghosh, Kurt Keutzer]
  note: Devadas, Ghosh and Keutzer defined the tag metric on HDL code in 1996. Fallah, Devadas and Keutzer computed it efficiently in OCCOM in 1998, with a journal version in 2001.
prereqs: [code-coverage-metrics, fault-simulation, boolean-circuit]
see_also: [transition-density, stuck-at-fault-model, deductive-fault-simulation, critical-path-tracing, fault-coverage, functional-coverage, fsm-coverage, logic-simulation]
sources:
  - paper: "Srinivas Devadas, Abhijit Ghosh and Kurt Keutzer, An observability-based code coverage metric for functional simulation, ICCAD 1996, 418 to 425"
    title: S. Devadas, A. Ghosh and K. Keutzer, An observability-based code coverage metric for functional simulation, Proceedings of the IEEE/ACM International Conference on Computer-Aided Design (ICCAD), 418 to 425, 1996
    locator: the tags attached to assignments, the tag calculus for the operators of the code, and the definition of an assignment as covered when its tag reaches an output
  - paper: "Farzan Fallah, Srinivas Devadas and Kurt Keutzer, OCCOM: efficient computation of observability-based code coverage metrics for functional verification, DAC 1998, 152 to 157"
    title: F. Fallah, S. Devadas and K. Keutzer, OCCOM, efficient computation of observability-based code coverage metrics for functional verification, Proceedings of the 35th Design Automation Conference, 152 to 157, 1998
    locator: the efficient computation of the tag metric during simulation of the HDL description
  - paper: "Farzan Fallah, Srinivas Devadas and Kurt Keutzer, OCCOM: efficient computation of observability-based code coverage metrics for functional verification, IEEE TCAD 20(8), 1003 to 1015, 2001"
    title: F. Fallah, S. Devadas and K. Keutzer, OCCOM, efficient computation of observability-based code coverage metrics for functional verification, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 20(8), 1003 to 1015, 2001
    locator: the journal version of OCCOM (general locator)
  - paper: doi:10.1109/54.936247
    title: Serdar Tasiran and Kurt Keutzer, Coverage metrics for functional validation of hardware designs, IEEE Design and Test of Computers 18(4), 36 to 45, 2001
    locator: the section on observability-based metrics and their place among code coverage metrics
  - book: isbn:9780780310629
    title: Miron Abramovici, Melvin A. Breuer and Arthur D. Friedman, Digital Systems Testing and Testable Design, IEEE Press, 1994
    locator: the chapter on fault simulation (deductive fault simulation and the rules for controlling values), the source of the propagation rules used here
---

Observability-based coverage counts a piece of a design as covered by a simulation only when an error at that piece would have reached an output, not merely when the piece was executed. Devadas, Ghosh and Keutzer (1996) attach a *tag* to the value computed at each assignment of the HDL code, propagate tags through the operators during simulation, and count an assignment as covered when its tag reaches an output. Fallah, Devadas and Keutzer made the computation fast in OCCOM (1998). This page gives a gate-level version of the idea, in which a tag means "this line has the wrong value", proves that a tag at an output means that the error is really observable for that vector, and shows that the converse fails because of reconvergent fanout.

## In plain words

Ordinary code coverage asks: did this line run? But a line can run, compute a wrong value, and the wrong value can die before anyone sees it, because a later gate or condition blocks it. Then the test could never catch a bug at that line, although the line was "covered".

This method puts a marker on a value, meaning "suppose this value were wrong". It then follows the marker through the circuit during the normal simulation. At each gate it asks: if only this input were wrong, would the output be wrong too? If yes, the marker moves on. A marker that reaches an output proves that a bug at its source would have shown. A marker that dies means the test saw nothing of that place. The rule is careful: a marker it moves is real, but it sometimes stops a marker that would reach the output.

## The problem

**Input.** A combinational circuit $C$ of AND, OR, NAND, NOR, XOR, XNOR, NOT and BUF gates in topological order, with $n$ lines (primary inputs and gate outputs) and $P$ gate input pins; a set $V$ of input vectors; and a set of *sites*, here all lines.

**The exact target.** For a vector $v$ and a site $t$, let $C^t$ be the circuit with the value of line $t$ complemented, as seen by every gate that reads $t$. Site $t$ is *observable* for $v$ when some primary output of $C^t$ differs from that of $C$. Equivalently, if the circuit is cut at $t$ and $t$ becomes a free variable, the [Boolean difference](/transition-density/) of some output with respect to $t$ is 1 at $v$. The *exact observability coverage* of $V$ is the fraction of sites that are observable for at least one vector of $V$.

**What is computed.** For each vector, a set of *tagged* sites, by one pass over the circuit, and the fraction of sites tagged at an output for at least one vector. The tagged set is contained in the observable set (proved below). It is equal on circuits without reconvergent fanout, and smaller in general.

**Not a code metric, not fault coverage.** Flipping line $t$ under $v$ is the single [stuck-at fault](/stuck-at-fault-model/) "$t$ stuck at the complement of its value", so at gate level the exact target is the set of stem faults that the vectors detect, in the sense of [fault simulation](/fault-simulation/). The question is different: here the vectors come from functional simulation and the sites stand for design errors, and the number is a coverage of the design, not the [fault coverage](/fault-coverage/) of a manufacturing test.

## The algorithm

Every line starts with its own tag. A gate passes the tags of input $i_j$ to its output when every other input has a value that does not decide the gate alone (a non-controlling value: 1 for AND and NAND, 0 for OR and NOR, anything for XOR, XNOR, NOT and BUF) and does not itself depend on the tagged site. The second condition is what makes the rule sound: a tag that arrives at a gate along two paths could cancel or change the gate in a way that the rule does not track, so it is dropped. $\mathrm{Fin}(\ell)$ is the set of lines on which $\ell$ depends, $\ell$ included.

```pseudo id=main
TagCoverage(C, V)
L1  for each line ℓ in topological order: Fin(ℓ) ← {ℓ} ∪ ⋃ of Fin(i) over the inputs i of ℓ
L2  Covered ← ∅
L3  for each vector v in V:
L4      simulate C on v to get val(ℓ) for every line ℓ
L5      for each primary input x: Tag(x) ← {x}
L6      for each gate g with output ℓ and inputs i_1, ..., i_k, in topological order:
L7          Tag(ℓ) ← {ℓ}
L8          for j ← 1 to k:
L9              if no i_m with m ≠ j has the controlling value of g then
L10                 Tag(ℓ) ← Tag(ℓ) ∪ (Tag(i_j) \ ⋃ of Fin(i_m) over m ≠ j)
L11     Covered ← Covered ∪ ⋃ of Tag(o) over the primary outputs o
L12 return Covered and |Covered| / n
```

Line L1 computes the cones once. Lines L4 to L10 are one simulation with tag sets. Line L9 is the sensitization test of path tracing: the other inputs must let a change through. Line L10 removes the sites that also reach the gate by another input, which is where reconvergence is cut off. Line L11 collects the sites whose tags reached an output.

## Example

Take the inputs $x, b, c, d$, the gates $p = \mathrm{AND}(x, b)$, $q = \mathrm{AND}(x, c)$, $y = \mathrm{OR}(p, q)$ and $z = \mathrm{AND}(q, d)$, and the outputs $y$ and $z$. The line $x$ fans out to $p$ and $q$, and the two paths meet again at $y$. There are 8 sites.

**Vector 1: $(x, b, c, d) = (0, 1, 1, 0)$.** The values are $p = q = y = z = 0$.

| line | rule applied | Tag |
|---|---|---|
| $p = \mathrm{AND}(x, b)$ | $b = 1$ passes $x$; $x = 0$ blocks $b$ | $\{p, x\}$ |
| $q = \mathrm{AND}(x, c)$ | $c = 1$ passes $x$; $x = 0$ blocks $c$ | $\{q, x\}$ |
| $y = \mathrm{OR}(p, q)$ | $q = 0$ passes $p$, minus $\mathrm{Fin}(q) \ni x$; $p = 0$ passes $q$, minus $\mathrm{Fin}(p) \ni x$ | $\{y, p, q\}$ |
| $z = \mathrm{AND}(q, d)$ | $d = 0$ blocks $q$; $q = 0$ blocks $d$ | $\{z\}$ |

The tagged sites at the outputs are $\{p, q, y, z\}$, 4 of 8. Flipping each site and simulating gives the observable set $\{x, p, q, y, z\}$, 5 of 8. The site $x$ is observable (flipping it makes $p = q = y = 1$) but its tag was dropped at $y$, because both inputs of $y$ depend on $x$.

**Vector 2: $(1, 0, 1, 1)$.** The values are $p = 0$, $q = 1$, $y = 1$, $z = 1$. The tags are $\mathrm{Tag}(p) = \{p, b\}$, $\mathrm{Tag}(q) = \{q, x, c\}$, $\mathrm{Tag}(y) = \{y, q, c\}$ (the input $q = 1$ is controlling for the OR, so $p$ passes nothing, and $x$ is removed from the tags of $q$ because $x \in \mathrm{Fin}(p)$) and $\mathrm{Tag}(z) = \{z, q, x, c, d\}$. The tagged sites at the outputs are $\{x, c, d, q, y, z\}$, and flipping each site gives the same set.

**Both vectors.** The tag coverage is $\{p, q, y, z\} \cup \{x, c, d, q, y, z\}$, 7 of 8, equal to the exact coverage. Only $b$ is missed: it is observable only when $x = 1$ and $c = 0$, and neither vector has that. Every line of this circuit is evaluated on every vector, so a line or toggle count of the gates says nothing about $b$, while the tag coverage points at it.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It shows, by induction over the lines in topological order:

- **Cones.** If $t \notin \mathrm{Fin}(\ell)$, flipping $t$ does not change $\ell$.
- **Soundness.** If $t \in \mathrm{Tag}(\ell)$, flipping $t$ changes $\ell$. At line L10 exactly one input of the gate changes, the others are non-controlling, and a gate whose other inputs are non-controlling passes a change of one input. So every tagged site at an output is observable for its vector, and the tag coverage is at most the exact coverage.
- **Exactness without reconvergence.** If every line feeds at most one gate input, the tagged sets equal the observable sets.
- **Not complete in general.** Vector 1 of the example has $x$ observable and not tagged.

These are proved for the gate-level model of this page. The papers state their tag calculus for HDL operators on words, where the claims of soundness and the trade-offs between rules are their own; this page does not reproduce them.

## Complexity

On a [word RAM](/word-ram/) with sets of sites as bit vectors of $\lceil n / w \rceil$ words:

- **Cones.** Line L1 does one union per pin, $O(P n / w)$ time, and stores $n$ sets, $O(n^2 / w)$ words.
- **One vector.** The simulation is $O(n + P)$. For a gate with $k$ inputs, prefix and suffix unions of the cones give the union over $m \ne j$ for every $j$ with $O(k)$ unions in all, so lines L6 to L10 cost $O(P n / w)$.
- **All vectors.** $O(V P n / w)$ time in the worst case, and $O(n^2 / w)$ extra space.

**The exact answer costs about the same at gate level.** One extra simulation per site and vector gives the observable sets in $O(V n (n + P))$ word operations, or $O(V n (n + P) / w)$ with bit-parallel simulation of $w$ flips at once. Deductive fault simulation of the stem faults, which keeps exact lists of faults per line, also runs in one pass per vector. So the tag rule is not a speed-up at gate level. Its value is on HDL code, where values are words and an operator such as an adder or a comparison has no simple exact rule for a change in one operand, while a conservative tag rule per operator is easy to state.

## Properties

- **Sound, not complete.** Tagged implies observable for that vector; the converse fails on reconvergent fanout.
- **Monotone in the vector set.** Adding vectors can only add covered sites.
- **Deterministic.** The result depends only on the circuit and the vectors.
- **A lower bound on detection.** At gate level, a covered site $t$ means that some vector detects the stuck-at fault on the stem $t$ at the complement of its value under that vector.

## Variants and improvements

- **The HDL metric.** Devadas, Ghosh and Keutzer tag the value assigned by each statement of the HDL description and propagate tags through the operators of the code by their tag calculus. A statement is covered when its tag reaches an output. Code coverage asks only whether the statement ran.
- **OCCOM.** Fallah, Devadas and Keutzer compute the metric efficiently during simulation of the HDL description.
- **Sequential designs.** Tags enter registers and can reach an output in a later cycle. A site is covered when its tag reaches an output at any later cycle of the run, so the propagation runs along the simulation in time.
- **Exact sets by deductive rules.** Use the rules of [deductive fault simulation](/deductive-fault-simulation/) on the flip faults: with no input at the controlling value, the output set is the union of the input sets (for XOR and XNOR, the sites that are in an odd number of them); otherwise it is the set of sites that are in the set of every controlling input and in no set of a non-controlling input; then add the output line itself. These sets are exact for single errors in a combinational circuit, and line L10 is a cheaper and weaker form of them.
- **Path tracing.** [Critical path tracing](/critical-path-tracing/) walks backward from the outputs along sensitized inputs and treats stems with reconvergent fanout by a separate check, which gives the exact set at gate level.
- **Mutation-style checks.** Inserting an actual change into the code (an operator replaced, a constant changed) and running the suite again gives an exact answer for that change, at the cost of one run per change.

## When to use it

Use it when line and decision coverage are high but the suite may still miss bugs because wrong values are masked before any checker sees them. It points at statements or lines whose effects never reach an output. Use exact flip simulation or deductive fault simulation instead when the design is a small gate-level netlist and the exact answer is cheap. Do not read a tag coverage of 100 percent as proof that every bug is found: a site is covered by one error effect for one vector, not by every possible wrong value, and an output that is reached must still be checked by the test bench.

## Pitfalls

- **Reading untagged as unobservable.** The rule is sound only in one direction. An untagged site may be observable through reconvergent paths, as in vector 1 of the example.
- **Dropping the cone test.** Without the condition $t \notin \mathrm{Fin}(i_m)$ at line L10, the rule is not sound: if two inputs of an AND both change, one from 0 to 1 and the other from 1 to 0, the output can stay the same while the rule moves the tag.
- **Outputs that nobody checks.** Reaching a primary output is the model of observation. If the test bench compares only some outputs, or only at some cycles, those are the outputs to use.
- **One error value.** At gate level a flip is the only possible error. On words, a tag for "the value is wrong" stands for many possible wrong values, and a rule that is sound for one of them may not be for another.
- **Confusing it with fault coverage.** The number counts design sites under functional vectors. It is not the fault coverage of a manufacturing test, even though it uses the same propagation ideas.

## Implementations

## History

Devadas, Ghosh and Keutzer proposed in 1996 to count an assignment of the HDL code as covered only when an error there propagates to an output, and gave a calculus of tags for this. The idea is close to the sensitization of paths in test generation and fault simulation, applied to design errors instead of manufacturing faults. Fallah, Devadas and Keutzer gave the efficient computation OCCOM at DAC 1998 and in IEEE TCAD in 2001. Tasiran and Keutzer place the metric among the code and state-machine metrics in their 2001 survey.

## References
