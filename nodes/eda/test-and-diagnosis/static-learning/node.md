---
tag: 8EB5WS
kind: technique
slug: static-learning
name: Static learning
aliases:
- SOCRATES learning
- implication learning
area: eda/test-and-diagnosis
level: advanced
summary: Precomputes indirect implications of each signal value by contraposition, as in SOCRATES, so ATPG and equivalence checking find conflicts earlier.
prereqs: [automatic-test-pattern-generation, podem]
see_also: [recursive-learning, fan-algorithm, failed-literal-probing, redundant-fault, equivalence-checking, 2-sat, implication-graph, d-algorithm]
sources:
  - paper: "M. H. Schulz, E. Trischler and T. M. Sarfert, SOCRATES: a highly efficient automatic test pattern generation system, IEEE Transactions on Computer-Aided Design 7(1), 126 to 137, 1988"
    title: M. H. Schulz, E. Trischler and T. M. Sarfert, SOCRATES, a highly efficient automatic test pattern generation system, IEEE Transactions on Computer-Aided Design 7(1), 126 to 137, 1988
    locator: the section on static learning, with the learning procedure, the contrapositive law and the test that keeps only useful implications
  - paper: "M. H. Schulz and E. Auth, Improved deterministic test pattern generation with applications to redundancy identification, IEEE Transactions on Computer-Aided Design 8(7), 811 to 816, 1989"
    title: M. H. Schulz and E. Auth, Improved deterministic test pattern generation with applications to redundancy identification, IEEE Transactions on Computer-Aided Design 8(7), 811 to 816, 1989
    locator: the improved implication procedure (dynamic learning during the search) and its use to prove faults redundant
  - paper: doi:10.1109/43.310903
    title: W. Kunz and D. K. Pradhan, Recursive learning, a new implication technique for efficient solutions to CAD problems (test, verification and optimization), IEEE Transactions on Computer-Aided Design 13(9), 1143 to 1158, 1994
    locator: the comparison of static learning with recursive learning, and examples of implications that static learning misses
  - book: isbn:9780792379911
    title: Michael L. Bushnell and Vishwani D. Agrawal, Essentials of Electronic Testing for Digital, Memory and Mixed-Signal VLSI Circuits, Kluwer, 2000
    locator: the chapter Combinational Circuit Test Generation (SOCRATES and learning)
---

Static learning is a step that a test generator runs once, before it looks at any fault. For each line of the circuit and each value 0 and 1, it sets the value, makes all the simple implications, and turns what it finds around by contraposition: if $a = 0$ implies $f = 0$, then $f = 1$ implies $a = 1$. The turned-around implications are often ones that the simple one-gate rules can never find, so the tool stores them and uses them in every later implication step. Schulz, Trischler and Sarfert introduced it in the SOCRATES test generator (1988), which was built on [FAN](/fan-algorithm/). The method is sound, which this page proves: every stored implication holds for every input vector. It is not complete: some implications need case splits, which is what [recursive learning](/recursive-learning/) adds.

## In plain words

When you set one signal of a circuit, simple rules tell you what other signals must be. Those rules move easily forward through gates but often get stuck going backward. For example, knowing that an OR gate outputs 1 does not tell you which input is 1.

Static learning works around this with an old rule of logic. If "A is true" always makes "B true", then "B false" always makes "A false". The tool tries every signal at 0 and at 1 before the real work starts, writes down every new fact it gets this way, and keeps the list. Later, when the test generator sets values, it reads the list and sees conflicts sooner, so it makes fewer wrong guesses.

## When it applies

- The circuit is combinational, or the combinational part of a [scan design](/scan-design/), with stems and fanout branches as on the [PODEM](/podem/) page.
- An implication engine exists, as in [PODEM](/podem/), [FAN](/fan-algorithm/) or the [D-algorithm](/d-algorithm/): from a set of values, it applies one-gate rules until nothing changes, or it finds a line that needs both values.
- There is time to run the engine twice per line before the search, and memory to store the learned implications.
- The search will meet the same kinds of situation many times, as in test generation for a long fault list, so a one-time cost pays off.

## The template

Write $(a, v) \Rightarrow (b, w)$ when every input vector that gives line $a$ the value $v$ also gives line $b$ the value $w$. A **direct implication** comes from one gate: known inputs fix the output, an AND output at 1 sets every input to 1, an AND output at 0 with all inputs but one at 1 sets the last one to 0, and a stem and its branches have one value. IMPLY$(S)$ applies the direct implications and the stored learned implications to a set of values until nothing changes. It returns CONFLICT when a line gets both values.

```pseudo id=main
STATIC-LEARN(circuit)
L1  learned ← empty; constants ← empty
L2  repeat
L3      for each line a and each value v in {0, 1}
L4          S ← IMPLY({(a, v)})
L5          if S is CONFLICT then add (a, ¬v) to constants; continue
L6          for each (b, w) in S with b ≠ a
L7              if (b, ¬w) ⇒ (a, ¬v) passes the usefulness test then
L8                  add (b, ¬w) ⇒ (a, ¬v) to learned
L9  until a whole pass adds nothing
L10 return learned, constants
```

The holes are the implication engine and the usefulness test at line L7. SOCRATES runs one pass. Later tools repeat the passes, because a learned implication can make IMPLY find more on the next pass.

**The usefulness test.** Most contrapositives repeat what the direct rules already know. From $a = 0$ at the input of an AND gate $d$, IMPLY gives $d = 0$, and the contrapositive $d = 1 \Rightarrow a = 1$ is a direct implication. SOCRATES keeps a contrapositive only when it adds something. The idea of its test is to look at the gate that drives $b$. If $w$ is the value that the gate gives when all its inputs are at their non-controlling values, for example 0 at an OR output or 1 at an AND output, then $\lnot w$ is the value that the gate cannot pass back to its inputs, so the direct rules cannot find anything from $(b, \lnot w)$, and the contrapositive is worth storing. The paper gives the exact conditions.

**Why it is sound.** Every value in $S$ at line L4 holds in every input vector with $a = v$. Each direct implication follows from the function of one gate, so it holds in every vector where its premises hold. By induction on the order in which values enter $S$, every value of $S$ holds in every vector with $a = v$, as long as every learned implication used by IMPLY is sound too. The learned implications are sound by induction on the order in which they are added, since each one comes from a sound IMPLY run by the following step.

- **Contraposition.** If $(a, v) \Rightarrow (b, w)$, then $(b, \lnot w) \Rightarrow (a, \lnot v)$. Take any input vector with $b = \lnot w$. If it gave $a = v$, it would give $b = w$ by the first implication, which is false. Lines have only the values 0 and 1, so the vector gives $a = \lnot v$.
- **Constants.** If IMPLY$(\{(a, v)\})$ returns CONFLICT, then no input vector gives $a = v$, since such a vector would give some line both values. So $a = \lnot v$ in every vector, and $a$ is a constant line. The fault $a$ stuck-at $\lnot v$ is then [redundant](/redundant-fault/), because no vector can activate it.

So every learned implication and every constant holds for all input vectors of the circuit. In a test generator, a situation $S$ is a set of values that the search wants, and an implication that holds for every vector also holds for every vector that agrees with $S$. Using the learned implications therefore never removes a test that exists. They only find conflicts earlier.

**What it misses.** Static learning is not complete. Take inputs $a$ and $b$, the gates $x = a \oplus b$ and $y = a \oplus b$, and the output $z = x \oplus y$. The line $z$ is the constant 0. But setting any one line to any value implies nothing except the values of its stem and branches, because an XOR gate with one input unknown has an unknown output, and an XOR output tells nothing about one input. So static learning learns no implication and finds no constant, and the fault $z$ stuck-at 0 looks testable. Recursive learning at depth 2 shows that $z = 1$ has no consistent input vector, as its page explains. In general, a contrapositive can only be as good as the forward run it comes from, and the forward run never splits cases.

**Cost.** Each IMPLY run takes time linear in the number of lines, gate inputs and stored implications, so one pass takes $O(L (L + P + E))$ time for $L$ lines, $P$ gate input pins and $E$ learned implications. The learned list can hold up to $4L^2$ implications in principle. In practice the usefulness test keeps it much smaller.

**Example.** Take inputs $a$, $b$ and $c$, the AND gates $d = a b$ and $e = a c$, and the output $f = d + e$. The input $a$ fans out to $d$ and $e$.

| set | IMPLY gives | contrapositive | kept? |
|---|---|---|---|
| $a = 0$ | $d = 0$, $e = 0$, $f = 0$ | $f = 1 \Rightarrow a = 1$ | yes: $f = 0$ is the value of an OR with all inputs at 0 |
| $a = 0$ | $d = 0$ | $d = 1 \Rightarrow a = 1$ | no: direct |
| $b = 0$ | $d = 0$ | $d = 1 \Rightarrow b = 1$ | no: direct |
| $d = 1$ | $a = 1$, $b = 1$, $f = 1$ | $f = 0 \Rightarrow d = 0$ | no: direct |
| $f = 0$ | $d = 0$, $e = 0$ | $d = 1 \Rightarrow f = 1$ | no: direct |

The only new implication is $f = 1 \Rightarrow a = 1$. It is true, since $f = a (b + c)$, and the direct rules cannot find it: an OR at 1 with two unknown inputs implies nothing. Now say the search sets $f = 1$ to propagate a fault effect and later tries $a = 0$. Without learning, the conflict shows only when $d$ and $e$ are evaluated after more decisions. With the learned implication, $f = 1$ sets $a = 1$ at once, and the search never tries $a = 0$.

## Classic examples

- **SOCRATES.** The test generator of Schulz, Trischler and Sarfert ran static learning before test generation, together with improved multiple backtrace and unique sensitization. It cut the number of backtracks on the ISCAS benchmark circuits a lot. These are measured results of the paper.
- **Redundancy identification.** A conflict at line L5 proves at once that a line is constant, so the faults that need the other value are [redundant](/redundant-fault/). Learned implications also help the search prove other faults redundant.
- **Equivalence checking.** In [equivalence checking](/equivalence-checking/), implications learned between the lines of two circuits show lines that are equal or complementary, which splits the problem into small parts.
- **SAT solving.** [Failed literal probing](/failed-literal-probing/) in SAT preprocessing is the same idea on clauses: set a literal, propagate, and learn its negation if a conflict appears. In clause form contraposition is free, because a two-literal clause $\lnot a \lor b$ gives both $a \Rightarrow b$ and $\lnot b \Rightarrow \lnot a$, as in the implication graph of [2-SAT](/2-sat/).

## Variations

- **Several passes.** Repeating the loop until it adds nothing finds implications that need an earlier learned one.
- **Dynamic learning.** Schulz and Auth (1989) also learn during the search, from the current situation and not only from single values, and use it to prove faults redundant.
- **Recursive learning.** [Recursive learning](/recursive-learning/) splits each unjustified gate into cases and keeps what all cases share. With enough depth it finds every necessary value, which static learning cannot.
- **Sequential circuits.** The same idea works across clock cycles in [time-frame expansion](/time-frame-expansion/), where implications can relate a line in one frame to a line in another.
- **Cheaper learning.** Later work limits learning to fanout stems or to gates near reconvergence, where most useful implications come from.

## Pitfalls

- **Applying good-circuit facts to the faulty circuit.** The learned implications hold for the fault-free circuit. In a five-valued test generator with D and D', they apply to the good-circuit part of each value. The faulty circuit computes a different function near the fault.
- **Keeping everything.** Without a usefulness test the list grows close to quadratic in the circuit size and slows every implication step, while most entries add nothing.
- **Reading an empty result as a proof.** If static learning finds no constant, the line can still be constant, as the XOR example shows.
- **Changing the circuit.** The learned list belongs to one netlist. After any change, such as inserting a test point, it must be learned again.

## Exercises

1. In the example, add the gate $g = b + c$. Which new implications does static learning find from $g$?
2. Build $f = a (b + c)$ as one AND gate of $a$ and $g = b + c$, without fanout. Show that $f = 1 \Rightarrow a = 1$ is now a direct implication, so the usefulness test rejects it.
3. Give a circuit with a constant line that static learning finds by a conflict at line L5.

## References
