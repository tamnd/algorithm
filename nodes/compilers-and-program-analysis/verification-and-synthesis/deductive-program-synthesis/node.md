---
tag: EYDYMW
kind: technique
slug: deductive-program-synthesis
name: Deductive program synthesis
aliases:
- Manna-Waldinger synthesis
area: compilers-and-program-analysis/verification-and-synthesis
level: advanced
summary: Extracts a program from a constructive proof that for every input there is an output meeting the specification.
prereqs: [program-synthesis, robinson-resolution]
see_also: [answer-substitution, curry-howard-correspondence, skolemization, first-order-theorem-proving, structural-induction, well-founded-relation, refinement-calculus, dependent-types]
sources:
  - paper: "Cordell Green, Application of theorem proving to problem solving, Proceedings of the International Joint Conference on Artificial Intelligence (IJCAI 1969), Washington, D.C."
    locator: pp. 219-239, the answer literal in resolution proofs, and the extraction of programs with conditionals and recursion from proofs
  - paper: doi:10.1145/362566.362568
    title: Zohar Manna and Richard Waldinger, Toward automatic program synthesis, Communications of the ACM 14(3), 1971
    locator: pp. 151-165, conditionals from case analysis and recursion from induction in the proof of an existence theorem
  - paper: doi:10.1145/357084.357090
    title: Zohar Manna and Richard Waldinger, A deductive approach to program synthesis, ACM Transactions on Programming Languages and Systems 2(1), 1980
    locator: pp. 90-121, the deductive tableau with output columns, the resolution rule with conditional outputs, and the induction rule that yields recursive calls
  - paper: doi:10.1145/2363.2528
    title: Joseph L. Bates and Robert L. Constable, Proofs as programs, ACM Transactions on Programming Languages and Systems 7(1), 1985
    locator: pp. 113-136, the extraction of programs from constructive proofs in the Nuprl type theory
  - paper: doi:10.1145/321992.321996
    title: Rod M. Burstall and John Darlington, A transformation system for developing recursive programs, Journal of the ACM 24(1), 1977
    locator: pp. 44-67, the fold and unfold rules for deriving programs from equations
  - paper: doi:10.1561/2500000010
    title: Sumit Gulwani, Oleksandr Polozov and Rishabh Singh, Program Synthesis, Foundations and Trends in Programming Languages 4(1-2), 2017
    locator: the overview of deductive synthesis in the history of the field
---

Deductive program synthesis builds a program from a proof. The specification says that for every input $x$ with $P(x)$ there is an output $z$ with $Q(x, z)$. A theorem prover proves this statement in a constructive way, and each step of the proof also builds a part of the output: the term that the proof gives for $z$ is the program. Case splits in the proof become conditionals, and proofs by induction become recursive calls. So the program meets its specification by construction. Green (1969) extracted answers from resolution proofs, and Manna and Waldinger (1971, 1980) gave the general method with the deductive tableau.

## In plain words

To find a program, prove that the answer exists, and prove it in a way that says how to find it. Say you must prove that every pair of numbers has a larger-or-equal member. One proof goes: "if the first is at most the second, take the second; else take the first." That sentence is already a program.

The method writes such proofs with strict rules, so a machine can find them and read off the program. Splitting into cases gives an "if". Proving a claim for 0, and for n from the claim for n minus 1, gives a function that calls itself on n minus 1.

The program needs no testing against its specification, because the proof is a proof of exactly that. The hard part is to find the proof.

## When it applies

Use it when the specification is a logical formula, not a set of examples, and when the background facts about the data types can be written as axioms. The output is a program with a proof of correctness. The method fits small programs on numbers, lists and trees, and the derivation of algorithms from formal definitions.

It needs a constructive proof. A proof by contradiction can show that some $z$ exists without naming it, and then there is no program. A case split on a property that no program can decide gives no executable conditional. So the rules may split cases only on *primitive* conditions, which the target language can compute, and the axioms may use in programs only *primitive* functions.

For specifications given by examples, use [programming by example](/programming-by-example/). For a known program shape with unknown details, use [program sketching](/program-sketching/).

## The template

**Step 1: the specification.** Write it as $\forall x\, (P(x) \rightarrow \exists z\, Q(x, z))$. Mark the function and predicate symbols that the target language can compute.

**Step 2: the theory.** Write axioms for the data types and for the primitive functions: for example the order of the integers, the equations for addition, and an induction principle for the natural numbers or for lists.

**Step 3: prove with output terms.** Every formula in the proof carries an output term, which may contain variables of the proof. The basic rules are:

- *Resolution.* From clauses $C \vee L$ and $D \vee \neg L'$, where $L$ and $L'$ have a [most general unifier](/most-general-unifier/) $\sigma$, infer $(C \vee D)\sigma$. This is the rule of [Robinson resolution](/robinson-resolution/). A proof shows that a set of clauses is contradictory by deriving the empty clause.
- *The answer literal.* Green (1969) negates the goal $\exists z\, Q(a, z)$, which gives the clause $\neg Q(a, z)$, and adds a literal: $\neg Q(a, z) \vee \mathrm{Ans}(z)$. The input $a$ is a new constant, as in [Skolemization](/skolemization/). Resolution applies the unifiers to Ans too. When the derived clause is $\mathrm{Ans}(t)$ alone, the term $t$ is an answer; see [answer substitution](/answer-substitution/).
- *Conditional outputs.* If one clause states "$p$ holds, or $t_1$ is an answer" and another "$p$ fails, or $t_2$ is an answer", resolution on the primitive condition $p$ gives the answer $\mathbf{if}\ p\ \mathbf{then}\ t_2\ \mathbf{else}\ t_1$. Manna and Waldinger (1980) build this into the rule, so the derived row carries the conditional term.
- *Induction.* To prove the goal for $x$, assume it for all $y$ smaller than $x$ in a [well-founded relation](/well-founded-relation/). Each use of this hypothesis with an output $f(y)$ becomes a recursive call of the program $f$ that is being built. Well-foundedness makes the recursion stop.

**Step 4: read off the program.** The output term of the final step is the body of the program, with the input as its parameter.

**Step 5: correctness.** The program meets the specification by soundness of the rules: each rule preserves the meaning "the output term is a correct $z$ for the inputs where the row holds". Termination follows from the well-founded relation of the induction.

## Classic examples

**The maximum by resolution with an answer literal.** The theory has a primitive order $\mathrm{Le}$ and a predicate $\mathrm{Max}(u, v, w)$, "w is a larger-or-equal member of u and v":

1. $\mathrm{Le}(u, v) \vee \mathrm{Le}(v, u)$
2. $\neg \mathrm{Le}(u, v) \vee \mathrm{Max}(u, v, v)$
3. $\neg \mathrm{Le}(v, u) \vee \mathrm{Max}(u, v, u)$

The goal is $\exists z\, \mathrm{Max}(a, b, z)$ for input constants $a$ and $b$. Negate it and add the answer literal:

4. $\neg \mathrm{Max}(a, b, z) \vee \mathrm{Ans}(z)$

The proof:

5. From 4 and 2 with $\{u \mapsto a, v \mapsto b, z \mapsto b\}$: $\neg \mathrm{Le}(a, b) \vee \mathrm{Ans}(b)$.
6. From 4 and 3 with $\{u \mapsto a, v \mapsto b, z \mapsto a\}$: $\neg \mathrm{Le}(b, a) \vee \mathrm{Ans}(a)$.
7. From 5 and 1 with $\{u \mapsto a, v \mapsto b\}$: $\mathrm{Le}(b, a) \vee \mathrm{Ans}(b)$.
8. From 7 and 6 on the primitive literal $\mathrm{Le}(b, a)$: the clause $\mathrm{Ans}(b) \vee \mathrm{Ans}(a)$, which is the answer $\mathbf{if}\ \mathrm{Le}(b, a)\ \mathbf{then}\ a\ \mathbf{else}\ b$.

Clause 6 says "if $\mathrm{Le}(b, a)$, then $a$ is an answer", and clause 7 says "if not, then $b$ is". The program is $\max(a, b) = \mathbf{if}\ b \le a\ \mathbf{then}\ a\ \mathbf{else}\ b$.

**A query instead of a program.** With the facts $\mathrm{Parent}(a, b)$ and $\mathrm{Parent}(b, c)$, the rule $\neg \mathrm{Parent}(x, y) \vee \neg \mathrm{Parent}(y, z) \vee \mathrm{Grand}(x, z)$ and the goal clause $\neg \mathrm{Grand}(a, w) \vee \mathrm{Ans}(w)$, three resolution steps give $\neg \mathrm{Parent}(a, y) \vee \neg \mathrm{Parent}(y, w) \vee \mathrm{Ans}(w)$, then $\neg \mathrm{Parent}(b, w) \vee \mathrm{Ans}(w)$, then $\mathrm{Ans}(c)$. The answer is a constant, because the goal has no input. [Logic programming](/logic-programming/) answers queries in this way.

**Recursion from induction.** Specification: for every natural number $n$ there is $z$ with $2z = n(n + 1)$. Prove it by induction on $n$.

- *Base.* For $n = 0$, take $z = 0$, since $2 \cdot 0 = 0 \cdot 1$.
- *Step.* For $n > 0$, the hypothesis for $n - 1$ gives $z'$ with $2z' = (n - 1)n$, with the output $f(n - 1)$. Take $z = z' + n$: then $2z = (n - 1)n + 2n = n(n + 1)$.

The case split on $n = 0$ is primitive, so it becomes a conditional, and the use of the hypothesis becomes a call:

$$ f(n) = \mathbf{if}\ n = 0\ \mathbf{then}\ 0\ \mathbf{else}\ f(n - 1) + n. $$

A different proof gives a different program. A proof that uses the axiom "$n(n + 1)$ is even" and a primitive halving function gives $f(n) = n(n + 1)/2$ with no recursion.

## Variations

- **The deductive tableau.** Manna and Waldinger (1980) write the proof as a table of assertions and goals, each with an output column. Rules for resolution, for equality, and for induction act on rows and combine their outputs.
- **Proofs as programs in type theory.** In a constructive type theory a proof of $\forall x\, \exists z\, Q(x, z)$ is itself a function that returns $z$ together with a proof of $Q(x, z)$. Bates and Constable (1985) extracted programs in this way from Nuprl proofs, and proof assistants such as Coq extract programs from proofs today. This is the [Curry-Howard correspondence](/curry-howard-correspondence/) used for synthesis, often with [dependent types](/dependent-types/).
- **Transformational synthesis.** Burstall and Darlington (1977) start from a clear but slow set of equations and rewrite them with the rules fold and unfold into a fast recursive program. Each rule keeps the meaning, so the result is correct. The [refinement calculus](/refinement-calculus/) is a related method for imperative programs.
- **Synthesis with a solver.** Modern tools often mix the two worlds: a proof rule splits the goal, and a solver or a search fills the small parts.

## Pitfalls

- **Classical proofs give no program.** "Either the program halts or it does not, and in each case the claim holds" is a valid classical proof, but the case split cannot be computed. Restrict case splits to primitive conditions.
- **Non-primitive symbols in the answer.** If the answer term uses a function that the axioms only describe, such as "the $z$ with $Q(x, z)$", the program cannot run. Only primitive symbols may appear in output terms.
- **The proof decides the program.** Two proofs of the same theorem can give programs of very different cost. The prover has no notion of efficiency unless the method adds one.
- **The search is hard.** Proving the existence theorem is as hard as theorem proving in general, which is undecidable for first-order logic. Practical systems need guidance by the user or strong heuristics for induction.
- **The specification must be complete.** A program that meets a weak specification is correct only in that weak sense. A sort that only asks "the output is ordered" can return the empty list.
- **Induction needs a well-founded order.** An induction on an order with infinite descending chains gives a recursion that may not stop.

## Exercises

1. In the maximum example, resolve 5 with 1 first on the other literal: unify $\mathrm{Le}(a, b)$ with $\mathrm{Le}(v, u)$. What clause do you get, and how does the proof finish? *Answer.* The unifier $\{v \mapsto a, u \mapsto b\}$ gives $\mathrm{Le}(b, a) \vee \mathrm{Ans}(b)$ again, since clause 1 is symmetric, and step 8 is the same.
2. Derive a recursive program for $\exists z\, z = 2^n$ from the axioms $2^0 = 1$ and $2^{n} = 2 \cdot 2^{n-1}$ for $n > 0$. *Answer.* Induction on $n$ gives $f(n) = \mathbf{if}\ n = 0\ \mathbf{then}\ 1\ \mathbf{else}\ 2 \cdot f(n - 1)$.
3. Why is the goal clause $\neg \mathrm{Max}(a, b, z) \vee \mathrm{Ans}(z)$ and not $\neg \mathrm{Max}(x, y, z) \vee \mathrm{Ans}(z)$ with variables $x$ and $y$? *Answer.* The goal is $\forall x\, \forall y\, \exists z\, \mathrm{Max}(x, y, z)$. Its negation is $\exists x\, \exists y\, \forall z\, \neg \mathrm{Max}(x, y, z)$, and Skolemization replaces $x$ and $y$ by constants. With variables, resolution could pick special inputs, and the answer would hold only for them.
4. A proof of $\forall n\, \exists z\, z^2 \le n < (z + 1)^2$ by induction on $n$ with the step "if $(z' + 1)^2 \le n$ then $z = z' + 1$ else $z = z'$" gives which program? *Answer.* $f(n) = \mathbf{if}\ n = 0\ \mathbf{then}\ 0\ \mathbf{else}\ (\mathbf{if}\ (f(n - 1) + 1)^2 \le n\ \mathbf{then}\ f(n - 1) + 1\ \mathbf{else}\ f(n - 1))$, an [integer square root](/integer-square-root/) in $O(n)$ steps.

## References
