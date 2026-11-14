---
tag: C6DBQN
kind: algorithm
slug: d-algorithm
name: D-algorithm
aliases:
- Roth D-algorithm
area: eda/timing-and-verification
level: core
summary: Roth's ATPG over the five values 0, 1, X, D and D-bar, which drives a D-frontier to an output and justifies internal line values by backtracking search.
solves: [automatic-test-pattern-generation]
model: word-ram
complexity:
  vars: {L: the number of lines, P: the number of gate input pins, B: "the most children of one call, at most max(L, P)"}
  time: {worst: "O(B^(2L) L (L + P))", best: "O(L (L + P))"}
  space: {extra: O(L^2)}
properties: {deterministic: true, exact: true, complete: true, recursive: true}
history:
  year: 1966
  people: [J. Paul Roth]
  note: Roth gave the D-calculus and the D-algorithm at IBM in 1966. It was the first test generation method that is complete for single stuck-at faults in combinational circuits.
prereqs: [automatic-test-pattern-generation]
see_also: [podem, sat-based-atpg, stuck-at-fault-model, scoap, unit-propagation]
sources:
  - paper: doi:10.1147/rd.104.0278
    title: J. P. Roth, Diagnosis of automata failures, a calculus and a method, IBM Journal of Research and Development 10(4), 278 to 291, 1966
    locator: the D-calculus, the singular cover and the D-cubes, D-intersection, and the D-algorithm with its D-drive and consistency steps
  - book: isbn:9780792379911
    title: Michael L. Bushnell and Vishwani D. Agrawal, Essentials of Electronic Testing for Digital, Memory and Mixed-Signal VLSI Circuits, Kluwer, 2000
    locator: the chapter Combinational Circuit Test Generation (Roth's five values, the D-frontier, the J-frontier and the D-algorithm)
  - book: isbn:9780780310629
    title: Miron Abramovici, Melvin A. Breuer and Arthur D. Friedman, Digital Systems Testing and Testable Design, IEEE Press, 1994
    locator: the chapter on test generation for combinational circuits (the D-algorithm, implication and the two frontiers)
---

The D-algorithm is Roth's method of 1966 for [automatic test pattern generation](/automatic-test-pattern-generation/). For a combinational circuit and one [single stuck-at fault](/stuck-at-fault-model/), it computes with five values: 0, 1, X, D for "1 in the good circuit and 0 in the faulty one", and D' (D-bar) for the opposite. It puts D or D' on the fault site, drives it through a gate of the D-frontier toward an output, and then justifies each internal value that is not yet explained by the inputs. It backtracks on a conflict, and it was the first complete method: it finds a test whenever one exists.

## In plain words

A fault is seen when the good circuit and the broken circuit give different outputs. The D-algorithm writes down, on each wire, the value in the good circuit and the value in the broken circuit.

It starts at the broken wire and gives it the value opposite to its stuck value. Then it pushes the difference forward, one gate at a time: to let it through a gate, the other inputs of that gate must not block it. Each time it writes a value, it also writes everything that value forces, both forward and backward.

When the difference reaches an output, some wires still hold values that nothing explains yet. The algorithm chooses inputs of their gates to explain them. When two forced values clash, it undoes its last choice and tries another.

## The problem

The input is a combinational circuit $C$ of AND, OR, NAND, NOR, NOT and BUF gates with $L$ lines in topological order, and a fault $(\ell, s)$. The lines are the primary inputs, the gate outputs and the fanout branches. The output is a vector over $\{0, 1, X\}$ whose two-valued completions all detect the fault, or "untestable". XOR gates are written as AND, OR and NOT first, so that every gate has a controlling value: 0 for AND and NAND, 1 for OR and NOR.

A state gives each line a good entry and a faulty entry, each in $\{0, 1, X\}$. The five values are the pairs $0 = (0, 0)$, $1 = (1, 1)$, $D = (1, 0)$ and $D' = (0, 1)$, and X for the rest. The faulty entry of $\ell$ is $s$ and is never derived from the inputs of $\ell$.

- The **D-frontier** is the set of gates whose output has an X and that have an input with D or D'.
- The **J-frontier** is the set of pairs (gate, circuit) where the entry of the gate is known but its known inputs do not imply it.

## The algorithm

```pseudo id=main
D-ALGORITHM(C, (ℓ, s))
    set every entry to X; faulty entry of ℓ ← s; good entry of ℓ ← ¬s
    if D-ALG() then return the good entries of the primary inputs
    return "untestable"

D-ALG()
L1  apply all implications; if there is a conflict then return false
L2  if no primary output has D or D' then
L3      if the D-frontier is empty then return false
L4      for each gate G of the D-frontier do
L5          give each input of G without D or D' the non-controlling value of G in both circuits
L6          if there is no conflict and D-ALG() then return true
L7          undo the values of this pass
L8      return false
L9  if the J-frontier is empty then return true
L10 (G, m) ← a pair of the J-frontier
L11 for each input j of G that is X in circuit m do
L12     set j to the controlling value of G in circuit m
L13     if D-ALG() then return true
L14     undo this pass, and set j to the non-controlling value of G in circuit m
L15 return false
```

The implications of line L1 are the rules that the gates force, in each circuit on its own. Forward, a line whose known inputs fix it gets that value. A primary input other than $\ell$ has the same entry in both circuits. Backward, the input of a NOT, a BUF or a branch follows from its output. If an AND-type gate has the output that needs all inputs non-controlling, every input gets the non-controlling value. If it has the other output, no input is controlling yet and only one input is X, that input gets the controlling value. Two different values for one entry are a conflict.

## Example

The circuit is $g = \mathrm{NAND}(a, b)$, $h = \mathrm{NAND}(b, c)$, $z = \mathrm{NAND}(g, h)$, so $z = ab + bc$. The stem $b$ has the branches $b_g$ into $g$ and $b_h$ into $h$. The fault is $h$ stuck at 0, so the start state has $h = D$.

| call | line | what happens | state |
|---|---|---|---|
| 1 | L1 | faulty $z = \mathrm{NAND}(X, 0) = 1$ | $h = D$, $z$ = (X, 1) |
| 1 | L4, L5 | D-frontier $\{z\}$: set the other input $g$ to 1, the non-controlling value of NAND | $g = 1$ |
| 2 | L1 | good $z = \mathrm{NAND}(1, 1) = 0$ | $z = D'$ |
| 2 | L10 | J-frontier: good $h = 1$ and $g = 1$ in both circuits, all with X inputs; take good $h$ | |
| 2 | L12 | set good $b_h$ to 0, the controlling value | |
| 3 | L1 | $b_h = 0$ gives $b = 0$, then $b_g = 0$ and $g = 1$ in both circuits | $b = b_g = b_h = 0$ |
| 3 | L9 | J-frontier empty: return true | |

The answer is the good input values X0X. Every completion detects the fault, since good $z$ is 0 and faulty $z$ is 1 whenever $b = 0$. The search made 3 calls and no backtrack.

A redundant fault shows the failure case. Take $na = \mathrm{NOT}(a)$, $p = \mathrm{AND}(a, b)$, $q = \mathrm{AND}(na, c)$, $r = \mathrm{AND}(b, c)$ and $z = \mathrm{OR}(p, q, r)$, with $r$ stuck at 0. Line L1 of the first call justifies good $r = 1$ backward, so $b = c = 1$ in both circuits. The D-frontier is $\{z\}$, and line L5 sets $p = q = 0$, the non-controlling value of OR. In the second call, $p = 0$ with $b = 1$ forces $a = 0$, so $na = 1$ and $q = \mathrm{AND}(1, 1) = 1$, which conflicts with $q = 0$. The first call undoes the pass, has no other D-frontier gate, and returns false. So the answer is "untestable" after 2 calls and 1 backtrack.

## Correctness

The implications write only values that the gate equations force, so they never remove a test. When line L9 returns true, the implications are at a fixpoint and nothing is left to justify, so every known entry follows from the input entries, whatever values the X inputs take, and an output with D or D' really differs. This is soundness.

For completeness, fix a test $\tau$ and keep a state whose known entries all match $\tau$. If no output has D or D' yet, take the first line in topological order that differs under $\tau$ but has no D or D' in the state. It is a D-frontier gate, and its other inputs do not differ under $\tau$, so under $\tau$ they are all non-controlling, which is what line L5 writes. In justification, line L11 tries the inputs in order, and line L14 writes the non-controlling value on each input that failed. So the pass for the first input that $\tau$ sets to the controlling value matches $\tau$. Each call makes at least one more entry known, so the depth is at most $2L$. The [full proof](proofs/correctness.md) gives the details.

## Complexity

Line L1 makes passes over all lines until nothing changes. One pass costs $O(L + P)$, where $P$ is the number of gate input pins, and each pass but the last makes a new entry known, so line L1 costs $O(L (L + P))$. The recursion has depth at most $2L$, and a call has at most $B$ children, where $B$ is bounded by the size of the D-frontier or the fanin of the gate at line L10. So the worst case is $O(B^{2L} L (L + P))$ time. It is exponential in the number of lines, not in the number of inputs as for [PODEM](/podem/). The problem is NP-complete, so no polynomial bound is expected. Each level of the recursion keeps a copy of the $2L$ entries, which is $O(L^2)$ extra space.

## Properties

- **Complete.** For a combinational circuit, the D-algorithm returns a test exactly when the fault is detectable. "Untestable" proves that the fault is redundant.
- **Decisions on internal lines.** Lines L5 and L12 set values inside the circuit. This finds tests with few decisions when the paths are clear, but a bad choice may show as a conflict only much later, after many more decisions.
- **Tests with X.** The result leaves free inputs at X, which helps test compaction.
- **Deterministic.** The order of the D-frontier at line L4 and the choice at line L10 fix the result.
- **No XOR.** The rules need a controlling value, so XOR and XNOR gates are expanded first, or need their own D-cubes.

## Variants and improvements

- **Roth's cube form.** Roth wrote each gate as a singular cover of cubes over its inputs and output, and the propagation through a gate as a propagation D-cube. The fault is a primitive D-cube of failure. A step of the algorithm is the D-intersection of the current test cube with a cube of a gate. The two-circuit form of this page holds the same information in pairs of three-valued entries.
- **D-drive with many paths.** Line L5 drives the effect through one gate at a time. Some faults need the effect on several reconvergent paths at once. The algorithm still finds them, because a later pass adds the second path while the first is still open.
- **Better implication.** Static learning finds implications such as "$a = 1$ forces $b = 0$" before the search, and recursive learning finds them during the search. Both cut the number of conflicts.
- **PODEM and FAN.** [PODEM](/podem/) makes decisions only on primary inputs, and FAN adds rules on head lines and fanout stems. Both are on the PODEM page.
- **SAT.** [SAT-based ATPG](/sat-based-atpg/) writes the same constraints as clauses. The implication step of line L1 then becomes [unit propagation](/unit-propagation/).

## When to use it

Use the D-algorithm to learn and to reason about test generation: its five values, its two frontiers and its implications are the vocabulary of the field, and later algorithms reuse them. For tools, [PODEM](/podem/) or FAN, with a SAT engine for the hard faults, is the usual choice, because the D-algorithm can make many conflicting decisions on circuits with much reconvergent fanout.

## Pitfalls

- **Deriving the faulty value of the site.** The faulty entry of $\ell$ is $s$. If the implications compute it from the inputs of $\ell$, they find a false conflict and report a detectable fault as untestable.
- **Too strong a propagation.** Line L5 must not write the non-controlling value on an input that already has D or D'. Such an input carries the effect, and forcing it to one value is a conflict that hides a test.
- **Forgetting the second value in justification.** After the pass for an input fails, line L14 sets that input to the non-controlling value. This is safe, because every test that the failed pass did not cover has that value there. Without it the search is still complete, but the later passes cannot use the value in their implications and repeat work.
- **Mixing the two circuits.** Justification is done per circuit. A good value of 1 on an AND gate needs all its good inputs at 1, but says nothing about its faulty inputs.
- **Reconvergent fanout.** An effect that reaches a gate on two paths as D and D' cancels. The implications see it, but only after the values on both paths are known, which is often deep in the search.

## Implementations

## History

Roth published the D-calculus and the D-algorithm in 1966, while at IBM, and with Bouricius and Schneider gave programmed versions in 1967. It was the first test generation method that is proved to find a test for every detectable single stuck-at fault in a combinational circuit, and its terms (D, D', D-frontier, justification and implication) became the standard ones. Goel's [PODEM](/podem/) of 1981 moved the decisions to the primary inputs, and the NP-completeness results of Ibarra and Sahni (1975) and Fujiwara and Toida (1982) showed that no method is expected to avoid exponential cases.

## References
