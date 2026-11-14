---
tag: HZB5S0
kind: technique
slug: recursive-learning
name: Recursive learning
aliases:
- Kunz-Pradhan recursive learning
area: eda/test-and-diagnosis
level: advanced
summary: Kunz and Pradhan's method that tries each way to justify an unjustified gate up to a depth and keeps the implications common to all, used in ATPG and verification.
prereqs: [automatic-test-pattern-generation, static-learning]
see_also: [fan-algorithm, podem, sat-based-atpg, implication-graph, redundant-fault, unit-propagation, cdcl, d-algorithm]
sources:
  - paper: doi:10.1109/43.310903
    title: W. Kunz and D. K. Pradhan, Recursive learning, a new implication technique for efficient solutions to CAD problems (test, verification and optimization), IEEE Transactions on Computer-Aided Design 13(9), 1143 to 1158, 1994
    locator: the procedure make_all_implications, unjustified gates and complete sets of justifications, the depth r_max, and the claim that enough depth gives all necessary assignments
  - paper: doi:10.1109/TEST.1992.527905
    title: W. Kunz and D. K. Pradhan, Recursive learning, an attractive alternative to the decision tree for test generation in digital circuits, Proc. International Test Conference 1992, 816 to 825
    locator: the first form of recursive learning, inside a FAN-based test generator
  - paper: "M. H. Schulz, E. Trischler and T. M. Sarfert, SOCRATES: a highly efficient automatic test pattern generation system, IEEE Transactions on Computer-Aided Design 7(1), 126 to 137, 1988"
    title: M. H. Schulz, E. Trischler and T. M. Sarfert, SOCRATES, a highly efficient automatic test pattern generation system, IEEE Transactions on Computer-Aided Design 7(1), 126 to 137, 1988
    locator: static learning, the weaker method that recursive learning extends
---

Recursive learning is a method by Kunz and Pradhan (1992, journal version 1994) that finds the values a set of signal assignments forces on the other lines of a circuit. Simple rules, one gate at a time, miss many of these values. Recursive learning looks at each gate whose output value is not yet explained by its inputs, tries every way to explain it, makes all implications of each way, and keeps the values on which all the ways agree. Inside each way it does the same again, up to a depth $r_{\max}$. Depth 0 gives the plain one-gate implications. With enough depth the method finds every conflict, and so, with one extra check per line, every value that the assignments force. Test generators such as [FAN](/fan-algorithm/) use it to find conflicts before they search and to prove faults [redundant](/redundant-fault/), and equivalence checkers use it to find related signals in two circuits.

## In plain words

Say an AND gate must output 0. Then one of its inputs is 0, but you do not know which. A simple implication engine stops here. Recursive learning does not. It tries "the first input is 0" and works out what follows, then "the second input is 0" and works out what follows. Whatever follows in every case is true for sure, so it learns it.

While it works out one case, it meets new gates of the same kind, and it can split them again. Each extra level of splitting finds more facts and costs more time. At full depth it is a complete search, but in practice a small depth already finds most of the useful facts.

## When it applies

- The circuit is combinational, or the combinational part of a [scan design](/scan-design/), with lines (stems and fanout branches) as on the [PODEM](/podem/) page.
- A *situation* is given: some lines have values 0 or 1, for example the values that a test generator has set so far. The task is to find more values that every input vector agreeing with the situation also has, or to see that no such vector exists.
- Plain implications are too weak. This happens at reconvergent fanout, where the effect of one value reaches a gate along two paths.
- The cost of case splits is acceptable. It grows exponentially with the depth, so a depth limit is part of the method.

## The template

A **consistent extension** of a situation $S$ is an input vector whose simulation gives every line of $S$ its value in $S$. A value $(k, v)$ is **necessary** for $S$ when every consistent extension gives line $k$ the value $v$. A **direct implication** uses one gate: forward, known inputs fix the output, and backward, for example, an AND output 1 sets all inputs to 1, an AND output 0 with all inputs but one at 1 sets the last input to 0, and a branch and its stem take the same value. A gate is **unjustified** when its output has a value and three-valued evaluation of its inputs still gives X, for example an AND at 0 with two inputs at X. A **justification** of such a gate is one assignment that would explain it: for an AND at 0, one X input set to 0. The set of all of them is **complete**: every consistent extension satisfies at least one, since an AND at 0 has some input at 0. For XOR, the two values of one X input form a complete set.

```pseudo id=main
MAKE-ALL-IMPLICATIONS(S, r, r_max)
L1  S ← S with all direct implications; if a line gets both values then return CONFLICT
L2  if r = r_max then return S
L3  repeat
L4      for each unjustified gate g of S
L5          for each justification J of g
L6              S_J ← MAKE-ALL-IMPLICATIONS(S ∪ J, r + 1, r_max)
L7          if every S_J is CONFLICT then return CONFLICT
L8          C ← the values on which all S_J that are not CONFLICT agree
L9          S ← S ∪ C with all direct implications; if a line gets both values then return CONFLICT
L10 until a whole pass adds no value
L11 return S
```

The holes are the logic values (two-valued here; test generators use the five values of the D-algorithm), the set of justifications of each gate type, and the depth $r_{\max}$. The call MAKE-ALL-IMPLICATIONS$(S, 0, r_{\max})$ is the recursive learning of $S$ to depth $r_{\max}$.

**Soundness.** Every value returned at any depth is necessary, and CONFLICT means that $S$ has no consistent extension. The proof is by induction on $r_{\max} - r$. Each direct implication follows from the function of one gate, so a consistent extension of $S$ also satisfies all of them, and a conflict at line L1 or L9 leaves no consistent extension. At line L6, take any consistent extension $\tau$ of $S$. The justifications of $g$ are complete, so $\tau$ satisfies some $J$ and is a consistent extension of $S \cup J$. By induction, $S_J$ is not CONFLICT and $\tau$ satisfies all of $S_J$, so $\tau$ satisfies the common values $C$. If every $S_J$ is CONFLICT, no such $\tau$ exists, which is line L7.

**Enough depth finds every conflict.** Suppose first that after line L1, $S$ has no conflict and no unjustified gate. Then $S$ has a consistent extension: take the values of $S$ on the inputs and anything on the other inputs. In topological order, every line with a value in $S$ is a primary input, a branch whose stem has the same value, or a gate whose assigned inputs already force its value. Three-valued simulation is monotone, so the full simulation gives each such line its value in $S$. Now let $U$ be the number of lines at X in $S$. If $r_{\max} - r \ge U$ and $S$ has no consistent extension, the call returns CONFLICT. By induction on $U$: if line L1 finds no conflict, then by the remark above some gate is unjustified, since otherwise a consistent extension would exist. Each justification $J$ of the first one handled sets one more line, so $S \cup J$ has at most $U - 1$ lines at X, has no consistent extension, and gets depth $r_{\max} - r - 1 \ge U - 1$. By induction every $S_J$ is CONFLICT, and line L7 returns CONFLICT. When $U = 0$, every gate has known inputs, and line L1 finds the conflict.

**All necessary values.** A value $(k, v)$ is necessary for $S$ exactly when $S \cup \{(k, \lnot v)\}$ has no consistent extension, so with $r_{\max} \ge L$, the number of lines, it is necessary exactly when that call returns CONFLICT. Two calls per line therefore find every necessary assignment, and soundness says that they find nothing else. Kunz and Pradhan state that recursive learning with enough depth gives all necessary assignments. This page proves it in this conflict form. A single call on $S$ can miss values that do not come from justifying a gate. With nothing assigned, no gate is unjustified, so the constant line $y = b \cdot \lnot b$ never gets its value 0. With $S = \{b = 1\}$, the gate NAND$(a, a \oplus b)$ is 1 in every consistent extension, and a single call does not see it. In a run on 3116 random situations that have a consistent extension, on random circuits with 2 to 4 inputs and 2 to 7 gates and with 1 to 3 assigned lines, drawn by `random.Random(5)`, a single call at full depth missed 563 necessary values, of which 377 hold for every input vector of the circuit. This is a measurement on toy inputs, not a benchmark result, and the tests check the conflict form against enumeration.

**Relation to static learning.** [Static learning](/static-learning/) stores implications between two single values, found by direct implication from one value and then by contraposition, once before the search. Recursive learning works on the whole current situation, with many values at once, and splits cases inside cases. Both give only necessary values. In the example below, static learning also finds $z = 1 \Rightarrow p = 1$, because $p = 0$ directly implies $b = c = 0$, then $q = r = 0$, then $z = 0$. The example shows how the depth levels work, not a gap between the two methods.

**Example.** Take the inputs $a$, $b$ and $c$, the gates $p = b + c$ and $q = b + c$ (two separate OR gates, so $b$ and $c$ fan out), $r = a p$, and the output $z = q + r$. The situation is $S = \{z = 1\}$. In every consistent extension, $q = 1$ or $r = 1$, and either one forces $b + c = 1$, so $p = 1$ and $q = 1$ are necessary.

- Depth 0: no direct implication applies, since $z$ is an OR at 1 with two inputs at X.
- Depth 1: $z$ is unjustified with the justifications $q = 1$ and $r = 1$. The first one implies nothing more, since $q$ is an OR at 1 with two inputs at X. The second one implies $a = 1$ and $p = 1$. The two cases agree on no new line, so nothing is learned.
- Depth 2: inside the case $q = 1$, the gate $q$ is unjustified. Its cases $b = 1$ and $c = 1$ both imply $p = 1$, which is learned in this case. Inside the case $r = 1$, the gate $p$ is unjustified, and its cases $b = 1$ and $c = 1$ both imply $q = 1$. Now both cases of $z$ have $p = 1$ and $q = 1$, so recursive learning at depth 2 learns them.

So depth 1 misses the two necessary values, and depth 2 finds them. Adding $a = 1$ to the situation also gives $r = 1$ at depth 2.

**Cost.** One call at depth 0 takes time polynomial in the size of the circuit. A call at depth $r$ can make up to $j$ calls at depth $r + 1$ for each unjustified gate, where $j$ is the largest number of justifications of a gate, so the work grows like $(G j)^{r_{\max}}$ for $G$ gates in the worst case. This is expected: deciding whether a situation has a consistent extension is circuit satisfiability, which is NP-complete, so a complete method must take exponential time in the worst case unless P = NP.

## Classic examples

- **Test generation.** A FAN-based [ATPG](/automatic-test-pattern-generation/) calls recursive learning on the current situation to find necessary values, often at depth 1 or 2. Kunz and Pradhan showed that it can replace the search of the decision tree for many hard faults, including the proof that a fault is [redundant](/redundant-fault/).
- **Equivalence checking.** To check two circuits, recursive learning finds pairs of internal signals that are equal or complementary, which cuts the problem into small parts.
- **Logic optimization.** Necessary values found by learning show where a wire or gate can be removed or replaced.
- **SAT solving.** Splitting on a clause, deriving the consequences of each case, and keeping the common ones is the same idea as the dilemma rule of [Stålmarck's method](/stalmarck-algorithm/). [CDCL](/cdcl/) solvers instead learn clauses from conflicts during search.

## Variations

- **Depth limit.** Tools use a fixed small depth, or raise the depth only for the faults that a fixed small depth does not solve.
- **Learning only near the fault.** In test generation, only the unjustified gates in the part of the circuit that matters for the current fault are handled.
- **Stored learning.** The values learned for one situation can be stored as implications, as in static learning, and used again.
- **Other logic values.** The method works with the five values 0, 1, D, D' and X, or with the values of sequential test generation, as long as each gate type has a complete set of justifications.
- **Implication graphs.** The learned implications between pairs of values can be added as edges of an [implication graph](/implication-graph/), where [unit propagation](/unit-propagation/) uses them.

## Pitfalls

- **An incomplete set of justifications.** If one way to explain a gate is left out, the common values can be wrong. For an AND at 0, every X input must have its own case.
- **Forgetting to recompute.** A value learned from one gate can justify another gate or make a new gate unjustified. Line L10 repeats the pass until nothing changes.
- **Reading a depth limit as a proof.** At limited depth, the absence of a conflict says nothing. Only CONFLICT and the learned values are facts.
- **Cost of depth.** Each level multiplies the work. A depth that is fine for one fault can be far too slow for another, so tools use limits.
- **Constants and forward facts.** A single call learns from unjustified gates. Values forced by the circuit structure alone, such as a constant line, need the conflict test or a separate pass.

## Exercises

1. In the example, take the situation $\{z = 1, a = 0\}$. Which values do depth 0 and depth 1 give? (Depth 0 gives $r = 0$ and $q = 1$, and depth 1 adds $p = 1$.)
2. In the example, how many calls does depth 2 make? How many does depth 3 make?
3. Give a complete set of justifications for a three-input XOR gate with output 1 and all inputs at X, with fewer than 4 cases.

## References
