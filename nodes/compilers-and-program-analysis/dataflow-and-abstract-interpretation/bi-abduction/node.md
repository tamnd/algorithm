---
tag: 3ADHQE
kind: technique
slug: bi-abduction
name: Bi-abduction
aliases:
- biabductive inference
area: compilers-and-program-analysis/dataflow-and-abstract-interpretation
level: research
summary: Infers the missing precondition and the leftover frame of a call in separation logic, which makes heap analysis compositional.
prereqs: [separation-logic, shape-analysis, call-graph]
see_also: [three-valued-logic-shape-analysis, symbolic-execution, hoare-logic, weakest-precondition, interprocedural-dataflow-analysis, abstract-interpretation, use-after-free, strongly-connected-components]
sources:
  - paper: doi:10.1145/1480881.1480917
    title: Cristiano Calcagno, Dino Distefano, Peter O'Hearn and Hongseok Yang, Compositional shape analysis by means of bi-abduction, Proceedings of the 36th ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL '09), 2009, pages 289-300
    locator: the bi-abduction question, the proof rules for abduction and frame inference over symbolic heaps, and the bottom-up inference of procedure specifications
  - paper: doi:10.1145/2049697.2049700
    title: Cristiano Calcagno, Dino Distefano, Peter W. O'Hearn and Hongseok Yang, Compositional shape analysis by means of bi-abduction, Journal of the ACM 58(6), article 26, 2011
    locator: the full version, with the footprint phase, the re-execution phase that checks candidate preconditions, and the experiments on large C code
  - paper: doi:10.1007/978-3-319-17524-9_1
    title: Cristiano Calcagno, Dino Distefano, Jeremy Dubreil, Dominik Gabi, Pieter Hooimeijer, Martino Luca, Peter O'Hearn, Irene Papakonstantinou, Jim Purbrick and Dulma Rodriguez, Moving fast with software verification, NASA Formal Methods (NFM 2015), LNCS 9058, 2015, pages 3-11
    locator: the use of bi-abduction in Facebook Infer and the analysis of each code change at review time
  - paper: doi:10.1109/LICS.2002.1029817
    title: John C. Reynolds, Separation logic, a logic for shared mutable data structures, Proceedings of the 17th Annual IEEE Symposium on Logic in Computer Science (LICS 2002), 2002, pages 55-74
    locator: the separating conjunction, the points-to assertion and the frame rule
---

Bi-abduction answers one question about a procedure call in [separation logic](/separation-logic/). The caller is in a symbolic state $A$ and the callee needs the precondition $B$. Bi-abduction finds two formulas: the *anti-frame* $M$, the part of $B$ that $A$ does not have, and the *frame* $F$, the part of $A$ that $B$ does not use, with $A \ast M \vdash B \ast F$. The analysis adds $M$ to the precondition of the caller and carries $F$ across the call by the frame rule. This gives a [shape analysis](/shape-analysis/) that infers a specification for each procedure from its body and the specifications of its callees, without the callers, so it can run on one procedure at a time, bottom-up over the [call graph](/call-graph/). Calcagno, Distefano, O'Hearn and Yang introduced it at POPL 2009, and it is the core of the Facebook Infer analyzer.

## In plain words

A procedure needs some memory to exist before it runs, and it changes some of that memory. When one procedure calls another, the analysis knows what memory the caller has at that point and what the callee needs. Two parts are missing. The first is memory that the callee needs and the caller does not have yet. The analysis guesses it and adds it to what the caller itself must get from its own caller. The second is memory that the caller has and the callee never touches. That part passes over the call unchanged. Bi-abduction finds both parts in one step. Each procedure then gets a contract from its own code and the contracts of the procedures it calls. So the analysis can treat one procedure at a time, from the leaves of the call graph up.

## When it applies

- The program changes the heap through pointers, as C, C++, Objective-C and Java programs do, and the question is about memory safety: null dereferences, accesses to freed or unallocated cells, and memory leaks.
- No specifications are given. Bi-abduction infers the preconditions, so the user does not write them.
- The program is large or changes often. Each procedure is analyzed once from the specifications of its callees, so a change needs new analysis only of the changed procedures and of the callers whose callee specifications change.
- The heap shapes fit a fixed set of inductive predicates, such as list segments. The proof search and the abstraction are only as good as these predicates.

## The template

**Symbolic heaps.** A state is a stack $s$, from program variables and logical variables to values, and a heap $h$, a finite partial map from addresses to values. The constant $\mathit{nil}$ is not an address. A *symbolic heap* is $\Pi \wedge \Sigma$, where $\Pi$ is a conjunction of equalities and disequalities between variables and $\mathit{nil}$, and $\Sigma$ is a separating conjunction of spatial atoms:

- $s, h \models \mathsf{emp}$ when $h$ is empty;
- $s, h \models x \mapsto e$ when $h = \{s(x) \mapsto s(e)\}$, a heap of exactly one cell (one field per cell keeps the notation short);
- $s, h \models \Sigma_1 \ast \Sigma_2$ when $h$ is the union of two disjoint heaps $h_1$ and $h_2$ with $s, h_1 \models \Sigma_1$ and $s, h_2 \models \Sigma_2$;
- $\mathsf{ls}(x, y)$ is the least predicate with $\mathsf{ls}(x, y) \Leftrightarrow (x = y \wedge \mathsf{emp}) \vee (x \ne y \wedge \exists z.\ x \mapsto z \ast \mathsf{ls}(z, y))$, a list segment from $x$ to $y$.

Logical variables that occur only in a precondition stand for unknown values and are read as existentially bound. The entailment $A \vdash B$ means that every state that satisfies $A$ satisfies $B$.

**Triples and the frame rule.** A triple $\{P\}\ C\ \{Q\}$ is read in the fault-avoiding way: from every state that satisfies $P$, the command $C$ does not access a cell outside the heap, and every final state satisfies $Q$. The *frame rule* is

$$ \frac{\{P\}\ C\ \{Q\}}{\{P \ast R\}\ C\ \{Q \ast R\}} \qquad \text{if } C \text{ assigns no variable that occurs free in } R. $$

It is sound because a command that runs safely from the heap of $P$ touches only cells of that heap, so a disjoint heap that satisfies $R$ is still there at the end. The rule fails for a reading of triples that allows faults: from $\mathsf{emp}$, a write to $x$ could then change a cell of $R$.

**The bi-abduction question.** Given $A$ and $B$, find $M$ and $F$ with

$$ A \ast M \vdash B \ast F, \qquad A \ast M \text{ satisfiable}. $$

With $F$ fixed to $\mathsf{emp}$ this is abduction. With $M$ fixed to $\mathsf{emp}$ it is frame inference. The answer is not unique: $M = B$ and $F = A$ is an answer when $A \ast B$ is satisfiable, and it is useless. A good answer has a small $M$, and Calcagno and coauthors search for one with a set of proof rules. The procedure below covers points-to atoms and list segments. It matches the atoms of $B$ one by one against $A$, moves the atoms that it cannot match into $M$, and returns what is left of $A$ as $F$. Variables of $B$ that do not occur in $A$ are the logical variables of the callee, and a match instantiates them.

```
biabduce(A, B):                      A = PiA & SigA, B = PiB & SigB
  S := atoms of SigA ; G := atoms of SigB ; M := emp ; Q := conjuncts of PiB
  while G is not empty:
    take g from G
    if g = (x |-> e) and S has (x' |-> e') with PiA |- x = x':
        remove (x' |-> e') from S ; add e = e' to Q
    else if g = ls(x, y) and PiA |- x = y:
        skip
    else if g = ls(x, y) and S has (x' |-> z) with PiA |- x = x':
        remove (x' |-> z) from S ; add ls(z, y) to G ; add x != y to Q
    else:
        M := M * g
  instantiate the callee variables from the equalities in Q
  M := M & (the conjuncts of Q that PiA does not imply)
  F := PiA & S
  if PiA & M is unsatisfiable: report an error
  return (M, F)
```

The unsatisfiable case is how the analysis finds bugs. If $\Pi_A \vdash x = \mathit{nil}$ and the callee needs $x \mapsto e$, then $M$ contains $x \mapsto e$, which cannot hold with $x = \mathit{nil}$, and the call is a null dereference.

**The call rule and its soundness.** Let the analysis of the caller have reached the call $f(\ldots)$ with a precondition $P$ and a current state $A$, so that $\{P\}\ C_0\ \{A\}$ holds for the code $C_0$ before the call. Let $\{B\}\ f\ \{B'\}$ be a specification of $f$, with its parameters replaced by the arguments. Bi-abduction gives $(M, F)$, and the analysis continues with the precondition $P \ast M$ and the state $B' \ast F$.

*Claim.* If $\{P\}\ C_0\ \{A\}$ and $\{B\}\ f\ \{B'\}$ hold, $A \ast M \vdash B \ast F$, $C_0$ assigns no variable free in $M$, and $f$ assigns no variable free in $F$, then $\{P \ast M\}\ C_0;\ f\ \{B' \ast F\}$ holds.

*Proof sketch.* The frame rule on $C_0$ with the frame $M$ gives $\{P \ast M\}\ C_0\ \{A \ast M\}$. The rule of consequence and $A \ast M \vdash B \ast F$ give $\{P \ast M\}\ C_0\ \{B \ast F\}$. The frame rule on $f$ with the frame $F$ gives $\{B \ast F\}\ f\ \{B' \ast F\}$. The rule of sequential composition joins the two. $\square$

The side condition on $C_0$ is why the analysis writes $M$ over logical variables that keep the values of the parameters at entry: $C_0$ can assign the program variables, but no command assigns a logical variable. The satisfiability check matters too. If $P \ast M$ were unsatisfiable, the triple would hold for the trivial reason that no state meets its precondition. Calcagno and coauthors state a stronger soundness theorem for the whole analysis; this sketch covers the step at one call.

**The compositional analysis.** Bi-abduction is one step of an analysis that infers a set of pairs (precondition, postcondition) for each procedure.

1. Order the procedures bottom-up by the call graph. A set of mutually recursive procedures, a [strongly connected component](/strongly-connected-components/), is iterated to a fixed point.
2. *Footprint phase.* Run a [symbolic execution](/symbolic-execution/) of the body from the precondition $\mathsf{emp}$. A load or store of a cell that is not in the state is a call with a small specification, such as $\{x \mapsto a\}\ [x] := e\ \{x \mapsto e\}$, and bi-abduction adds the cell to the precondition. At a call, bi-abduction runs against each specification of the callee. At loop heads, an abstraction folds chains of cells into list segments, so that the footprint stops growing and the iteration terminates.
3. *Re-execution phase.* The preconditions from step 2 are guesses: a precondition found on one path may not be enough for another path. Run each candidate again without abduction. Keep it only if the run needs nothing that is missing, and take the final states of that run as its postconditions.
4. Store the pairs of each procedure as its specifications for the callers.

## Classic examples

**Frame inference at a call.** The caller is in the state $x \mapsto a \ast y \mapsto b$ and calls `free(x)`, with the specification $\{x \mapsto \_\}\ \texttt{free(x)}\ \{\mathsf{emp}\}$. The procedure matches $x \mapsto \_$ against $x \mapsto a$, so $M = \mathsf{emp}$ and $F = y \mapsto b$. After the call the state is $y \mapsto b$: the cell of $y$ passed over the call unchanged.

**Frame and anti-frame together.** Take a callee and a caller.

```
void set_next(node *p, node *q) { p->next = q; }    // {p |-> b} set_next(p, q) {p |-> q}

void g(node *x, node *y) {
  x->next = NULL;      // line 1
  set_next(y, x);      // line 2
}
```

The analysis of `g` starts with the precondition $\mathsf{emp}$. Line 1 writes the cell of `x`, which is missing, so bi-abduction gives $M = x \mapsto a$. The precondition becomes $x \mapsto a$ and the state $x \mapsto \mathit{nil}$. At line 2 the callee needs $B = y \mapsto b$. The state does not imply $y = x$, so the atom does not match and goes to the anti-frame: $M = y \mapsto b$ and $F = x \mapsto \mathit{nil}$. By the call rule, `g` has the specification

$$ \{x \mapsto a \ast y \mapsto b\}\ \texttt{g(x, y)}\ \{y \mapsto x \ast x \mapsto \mathit{nil}\}. $$

The separating conjunction in the precondition says that `x` and `y` are different cells. An analysis that also splits on $y = x$ finds the second specification $\{x \mapsto a \wedge y = x\}\ \texttt{g(x, y)}\ \{x \mapsto x \wedge y = x\}$: the match of $y \mapsto b$ with $x \mapsto \mathit{nil}$ sets $b = \mathit{nil}$, and the frame is empty. Callers of `g` use whichever specification their state matches.

**A null dereference.** If a caller of `g` is in the state $x = \mathit{nil} \wedge \mathsf{emp}$, bi-abduction against $x \mapsto a \ast y \mapsto b$ puts $x \mapsto a$ into $M$ together with $x = \mathit{nil}$. That is unsatisfiable, and the analysis reports a null dereference at the call, in the caller, without looking into `g` again.

**A list traversal.** For `while (x != NULL) x = x->next;` the footprint phase adds one cell per iteration to the precondition: $x_0 \mapsto a_1$, then $x_0 \mapsto a_1 \ast a_1 \mapsto a_2$, and so on, where $x_0$ is the entry value of `x`. The abstraction folds such a chain into $\mathsf{ls}(x_0, a_k)$, the footprint stops growing, and the exit condition $a_k = \mathit{nil}$ gives the precondition $\mathsf{ls}(x_0, \mathit{nil})$: the loop needs a list from `x` that ends in null.

## Variations

- **Frame inference alone.** The Smallfoot tool of Berdine, Calcagno and O'Hearn used frame inference to check given specifications. Bi-abduction adds the anti-frame, which removes the need to write the preconditions.
- **Richer predicates.** Doubly linked lists, trees and nested lists need more inductive predicates and more rules in the proof search and the abstraction. The method stays the same.
- **Bugs instead of proofs.** Infer reports the errors that bi-abduction finds, such as null dereferences and leaks, and runs on each code change at review time. It uses heuristics that drop some specifications and paths, so in practice it finds bugs and does not prove their absence.
- **Under-approximate analysis.** Later analyses in Infer use bi-abduction with an under-approximate reading, in the style of incorrectness logic, where every reported bug is reachable.
- **Abduction in other domains.** The same question, find the missing hypothesis, is asked in arithmetic and first-order theories to infer preconditions and to explain false alarms.
- **Whole-program shape analysis.** [Three-valued logic shape analysis](/three-valued-logic-shape-analysis/) analyzes the program from its entry and can track more general shapes, but it does not give procedure specifications that hold in every caller.

## Pitfalls

- **Taking any answer.** $M = B$ and $F = A$ is always an answer when it is satisfiable, and it hides every match. The quality of the analysis rests on the search for a small $M$, and a weakest $M$ need not exist.
- **Skipping the satisfiability check.** An unsatisfiable $P \ast M$ makes every triple valid. It is the signal of a bug, not a specification.
- **Skipping re-execution.** A precondition from the footprint phase can be too weak for some paths. Without the second phase the specifications can be unsound.
- **Writing $M$ over program variables.** The code before the call can assign them, and then the frame rule does not apply to $M$. Use logical variables for the values at entry.
- **Expecting a proof from Infer.** The production tool trades soundness for speed and few false alarms. A clean run is not a proof of memory safety.
- **Shapes outside the predicates.** A data structure that the predicates cannot describe makes the abstraction lose it, and the analysis then finds no precondition or a precondition that callers never meet.

## Exercises

1. Run `biabduce` on $A = x \mapsto y \ast y \mapsto \mathit{nil}$ and $B = \mathsf{ls}(x, \mathit{nil})$, and on $A = x \mapsto y$ and $B = \mathsf{ls}(x, \mathit{nil})$. Give $M$ and $F$ in both cases.
2. Show that the frame rule fails if triples allow faults. Give $P$, $C$, $Q$ and $R$ for which $\{P\}\ C\ \{Q\}$ holds in that reading and $\{P \ast R\}\ C\ \{Q \ast R\}$ does not.
3. In the call rule, find $C_0$ and $M$ where $C_0$ assigns a variable of $M$, and show that the conclusion fails.
4. Give $A$ and $B$ for which two answers $(M_1, F_1)$ and $(M_2, F_2)$ exist and neither $M_1 \vdash M_2$ nor $M_2 \vdash M_1$ holds.
5. Write a recursive procedure that frees a list, and infer its specification by hand with the footprint and re-execution phases.

## References
