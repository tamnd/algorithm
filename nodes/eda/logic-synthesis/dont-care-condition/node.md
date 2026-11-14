---
tag: J7N02D
kind: definition
slug: dont-care-condition
name: Don't-care condition
aliases:
- incompletely specified function
- don't-care set
area: eda/logic-synthesis
level: intro
summary: An input combination where the output of a function may be 0 or 1, which a minimizer may choose to make the circuit smaller.
prereqs: [implicant, boolean-function]
see_also: [prime-implicant, karnaugh-map, two-level-logic-minimization, espresso, observability-dont-care, dont-care-minimization, incompletely-specified-fsm-minimization, boolean-network]
sources:
  - book: isbn:9780898381641
    title: Robert K. Brayton, Gary D. Hachtel, Curtis T. McMullen and Alberto L. Sangiovanni-Vincentelli, Logic Minimization Algorithms for VLSI Synthesis, Kluwer, 1984
    locator: Chapter 2, Basic Definitions (the on-set, off-set and don't-care set of a function)
  - book: isbn:9780070163331
    title: Giovanni De Micheli, Synthesis and Optimization of Digital Circuits, McGraw-Hill, 1994
    locator: Chapter 7, Two-Level Combinational Logic Optimization
  - book: isbn:9780792397465
    title: Gary D. Hachtel and Fabio Somenzi, Logic Synthesis and Verification Algorithms, Kluwer, 1996
    locator: Chapter 4, Synthesis of Two-Level Circuits
---

A don't-care condition is an input of a Boolean function where the output may be 0 or 1. The designer does not care, usually because the input never occurs or because nobody looks at the output then. The set of these inputs is the don't-care set $D$. A minimizer may give each point of $D$ the value that makes the circuit smaller, and an [implicant](/implicant/) may contain points of $D$. In a [Karnaugh map](/karnaugh-map/) these cells hold an x, and a group of 1s may take them in. A digit circuit is the classic case: a 4-bit code for a decimal digit never takes the values 10 to 15, so those six inputs are don't-cares, and the circuit for "digit at least 5" shrinks from 9 literals to 5.

## Definition

A function with don't-cares on $n$ variables is a map
$$f : \{0,1\}^n \to \{0, 1, *\},$$
where $*$ means "either". It gives three disjoint sets that cover $\{0,1\}^n$: the on-set $F = f^{-1}(1)$, the off-set $R = f^{-1}(0)$ and the **don't-care set** $D = f^{-1}(*)$. Each point of $D$ is a **don't-care condition**. The set $F \cup R$ is the care set.

**Realization.** A completely specified function $g : \{0,1\}^n \to \{0,1\}$ realizes $f$ if $g = f$ on the care set, that is,
$$F \subseteq g^{-1}(1) \subseteq F \cup D.$$
So the realizations of $f$ form the interval $[F, F \cup D]$ in the lattice of functions ordered by $g \le h$ when $g(x) \le h(x)$ for all $x$. There are $2^{|D|}$ realizations. A cover of $f$, in the sense of the implicant page, is a sum of products of some realization.

**Kinds of don't-cares.** The definition does not say where $D$ comes from. In practice there are three sources.

1. **Input don't-cares,** also called satisfiability or controllability don't-cares. The input never occurs: an unused code, or a combination that the logic before this block cannot produce.
2. **Output don't-cares,** also called [observability don't-cares](/observability-dont-care/). The input occurs, but the output does not change any primary output of the whole circuit then. They come from the context of a node in a [Boolean network](/boolean-network/).
3. **External don't-cares.** The specification leaves the output free, for example for the unused states of a state machine. These lead to [incompletely specified FSM minimization](/incompletely-specified-fsm-minimization/).

Two-level minimizers take $D$ as given, as a cover of cubes or a list of minterms, and do not care which kind it is.

## Examples and non-examples

- **BCD digit at least 5.** The inputs $a b c d$ hold a decimal digit in binary, so the codes 10 to 15 never occur. Let $f = 1$ for the digits 5 to 9: $F = \{5, 6, 7, 8, 9\}$, $D = \{10, \ldots, 15\}$, $R = \{0, \ldots, 4\}$. Without the don't-cares the minimum SOP is $a \bar{b} \bar{c} + \bar{a} b d + \bar{a} b c$, with 3 cubes and 9 literals. With them it is $a + b d + b c$, with 3 cubes and 5 literals. The cube $a$ covers 8, 9 and the six don't-cares. This realization sets all six don't-cares to 1, and it is one of the $2^6 = 64$ realizations.
- **One don't-care.** For $\sum m(1, 3, 6, 7)$ over $x_1 x_2 x_3$, the minimum SOP is $x_1 x_2 + \bar{x}_1 x_3$, with 4 literals. With minterm 5 as a don't-care, it is $x_1 x_2 + x_3$, with 3 literals, and the realization is 1 at minterm 5.
- **All don't-cares.** If $F = \emptyset$, the empty cover realizes $f$, with no cube at all. If $R = \emptyset$, the cube with no literal does. A minimizer never needs a cube that lies inside $D$ alone.
- **Non-example: a required value.** An input that can occur and whose output the specification fixes is not a don't-care, even if the designer thinks it is rare. If a minimizer treats it as one, the circuit gives a fixed value there, which may be wrong.
- **Non-example: a value per use.** A realization gives each point of $D$ one value. A two-output design may have a point that is a don't-care for one output and a 1 for the other, but in one output the point is either 0 or 1. Two cubes of one cover cannot treat the same point in two ways, since the cover is the union of its cubes.

**A trap in practice.** A don't-care that comes from "this input never occurs" is only as good as that claim. After synthesis the circuit has a fixed value at each point of $D$. If the input does occur, the circuit gives that value, and a simulation of the source that showed an unknown value at that point will not match the netlist. For the same reason, an [equivalence check](/boolean-equivalence-checking/) of the source against the netlist must compare them on the care set only.

## Related definitions

- **[Implicant](/implicant/)** and **[prime implicant](/prime-implicant/).** Cubes inside $F \cup D$, and the largest such cubes. Don't-cares make the primes larger and fewer.
- **[Two-level logic minimization](/two-level-logic-minimization/).** The search for a cheapest sum of products among all realizations of $f$.
- **[Karnaugh map](/karnaugh-map/).** Marks don't-cares as x cells that a group may use or leave out.
- **[Espresso](/espresso/).** Takes the on-set and the don't-care set as two covers and computes the off-set from them.
- **[Observability don't-care](/observability-dont-care/).** The don't-cares that the rest of a circuit gives to one node of a multi-level network.
- **[Don't-care-based function minimization](/dont-care-minimization/).** The same freedom used to make a BDD small instead of a sum of products.
- **[Incompletely specified FSM minimization](/incompletely-specified-fsm-minimization/).** Don't-cares in the next state and output tables of a state machine.

## References
