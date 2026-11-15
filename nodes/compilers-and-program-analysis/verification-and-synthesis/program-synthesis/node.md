---
tag: YH7B5E
kind: problem
slug: program-synthesis
name: Program synthesis
aliases:
- automatic programming
area: compilers-and-program-analysis/verification-and-synthesis
level: core
summary: Given a specification, such as a formula, examples or a type, find a program in a given language that meets it.
prereqs: [context-free-grammar, rice-theorem]
see_also: [syntax-guided-synthesis, cegis, programming-by-example, reactive-synthesis, automated-program-repair, superoptimization, loop-invariant-synthesis, genetic-programming]
sources:
  - paper: doi:10.1561/2500000010
    title: Sumit Gulwani, Oleksandr Polozov and Rishabh Singh, Program Synthesis, Foundations and Trends in Programming Languages 4(1-2), 2017
    locator: chapter 1 (the three dimensions of a synthesizer, user intent, program space and search technique), chapters 4 to 6 (enumerative search, constraint solving and stochastic search) and chapter 7 (programming by examples)
  - paper: "Alonzo Church, Applications of recursive arithmetic to the problem of circuit synthesis, Summaries of the Summer Institute of Symbolic Logic, vol. I, Cornell University, Ithaca, 1957, pp. 3-50"
    locator: the first statement of the synthesis problem, for circuits that map input streams to output streams (Church's problem)
  - paper: doi:10.2307/1994916
    title: J. Richard Büchi and Lawrence H. Landweber, Solving sequential conditions by finite-state strategies, Transactions of the American Mathematical Society 138, 1969
    locator: pp. 295-311, the solution of Church's problem for specifications in S1S, with finite-state strategies
  - paper: doi:10.1145/357084.357090
    title: Zohar Manna and Richard Waldinger, A deductive approach to program synthesis, ACM Transactions on Programming Languages and Systems 2(1), 1980
    locator: pp. 90-121, synthesis as theorem proving, with the program read from the proof
  - paper: doi:10.1145/75277.75293
    title: Amir Pnueli and Roni Rosner, On the synthesis of a reactive module, Principles of Programming Languages (POPL 1989)
    locator: pp. 179-190, synthesis of reactive modules from LTL specifications in doubly exponential time
  - paper: doi:10.1109/FMCAD.2013.6679385
    title: Rajeev Alur, Rastislav Bodík, Garvit Juniwal, Milo M. K. Martin, Mukund Raghothaman, Sanjit A. Seshia, Rishabh Singh, Armando Solar-Lezama, Emina Torlak and Abhishek Udupa, Syntax-guided synthesis, Formal Methods in Computer-Aided Design (FMCAD 2013)
    locator: pp. 1-8, a specification in a logical theory together with a grammar that limits the programs
  - paper: doi:10.1145/1806596.1806632
    title: Viktor Kuncak, Mikaël Mayer, Ruzica Piskac and Philippe Suter, Complete functional synthesis, Programming Language Design and Implementation (PLDI 2010)
    locator: pp. 316-329, synthesis procedures for specifications in linear arithmetic and sets, which produce a program whenever one exists
---

Program synthesis asks for a program that meets a specification. The specification may be a logical formula, a list of input-output examples, a type, a program with holes, or a temporal formula over infinite runs. This page states the general problem, its decidable and undecidable cases, and the main families of methods. The close pages each fix one kind of specification: [programming by example](/programming-by-example/) uses examples, [syntax-guided synthesis](/syntax-guided-synthesis/) uses a formula and a grammar, and [reactive synthesis](/reactive-synthesis/) builds systems that run forever against an environment.

## In plain words

Normally a person writes a program and a tool checks it. Synthesis turns this around. The person says what the program must do, and the tool writes the program.

The description can take many forms. It can be a precise rule, a few examples of inputs and the right outputs, the type of the function, or a program with some parts left blank. The tool also needs a list of the building blocks it may use.

The search space is huge, because the number of possible programs grows very fast with their length. So tools limit the language, search the smallest programs first, and throw away programs that behave like ones they have already seen. In general no tool can always succeed, because synthesis can encode questions that no algorithm can answer. With a finite set of candidate programs and a decidable check, the problem is decidable.

## Definition

**Input.**

- A *program space* $L$: a set of programs, usually the terms of a [context-free grammar](/context-free-grammar/), with a semantics $[\![P]\!] : I \rightharpoonup O$ that maps an input to an output or is undefined.
- A *specification* $\varphi \subseteq I \times O$: a relation between inputs and allowed outputs. It is given by a formula $\varphi(x, y)$, by a finite list of pairs, by a type, or in another finite form.

**Output.** A program $P \in L$ such that for every input $x \in I$, $[\![P]\!](x)$ is defined and $\varphi(x, [\![P]\!](x))$ holds. If no such program exists, the specification is *unrealizable* in $L$, and an exact solver says so.

**Optimal synthesis.** With a cost $c : L \to \mathbb{N}$, such as the number of nodes of the syntax tree, find a program of least cost among those that meet $\varphi$.

**Example-based specification.** When $\varphi$ is a finite list of pairs $(x_1, y_1), \ldots, (x_k, y_k)$, a program meets it if $[\![P]\!](x_i) = y_i$ for each $i$. Inputs outside the list are free. This is [programming by example](/programming-by-example/).

**Reactive specification.** For a system that reads an input letter and writes an output letter at each step, forever, $I$ and $O$ are infinite words, and the program must be causal: the output at step $t$ may depend only on the inputs up to step $t$. This is [reactive synthesis](/reactive-synthesis/). It is not the same as satisfiability of the specification, because the program must meet $\varphi$ for every input sequence that the environment chooses.

## Variants

- **Logical specification with a grammar** ([syntax-guided synthesis](/syntax-guided-synthesis/)). A formula $\forall \bar{x}\, \psi(f, \bar{x})$ in a decidable theory, and a grammar for the body of $f$.
- **Examples** ([programming by example](/programming-by-example/)). Few examples, a domain-specific language, and a ranking function that picks one program from the many that fit.
- **Sketches** ([program sketching](/program-sketching/)). A program with holes for constants or expressions; the solver fills the holes.
- **Deductive synthesis** ([deductive program synthesis](/deductive-program-synthesis/)). Prove that for each input an output exists, and read the program from the proof.
- **Types** ([type-directed synthesis](/type-directed-synthesis/)). The goal type, often with examples or refinement predicates, guides a search over well-typed terms only.
- **Reactive systems** ([reactive synthesis](/reactive-synthesis/)). A temporal logic formula over input and output signals; the answer is a finite-state transducer.
- **Repair** ([automated program repair](/automated-program-repair/)). The specification is a test suite, and the search space is the set of small edits to a given program.
- **Superoptimization** ([superoptimization](/superoptimization/)). The specification is an existing program, and the cost is speed or length.
- **Invariants** ([loop invariant synthesis](/loop-invariant-synthesis/)). The "program" is a predicate that makes a proof go through.

## Examples

The numbers below come from a short script that enumerates all programs of a grammar by size and runs them.

**A grammar and its size.** Take the grammar
$$E \to x \mid y \mid 0 \mid 1 \mid E + E \mid E - E \mid E \times E \mid \mathrm{ite}(B, E, E), \qquad B \to E \le E,$$
and let the size of a program be the number of nodes of its syntax tree. The number of integer programs of sizes $1, 3, 5, 7, 9$ is $4, 48, 1152, 34560, 1161216$. There are $1460$ programs of size at most $6$ and $2{,}247{,}860$ of size at most $10$. Each step of two in size multiplies the count by about 30, so enumeration is exponential in the size of the answer.

**A logical specification.** Let $\varphi(x, y, r)$ be $r \ge x \wedge r \ge y \wedge (r = x \vee r = y)$ over the integers. The smallest programs that meet it on all inputs in $\{-3, \ldots, 3\}^2$ have size $6$: $\mathrm{ite}(x \le y, y, x)$ and $\mathrm{ite}(y \le x, x, y)$. Both meet $\varphi$ on all integers. Without ite the specification is unrealizable in this grammar. Every program then denotes a polynomial $p(x, y)$ with integer coefficients. If $p(x, y) = \max(x, y)$, then $q(x) = p(x, 0)$ equals $x$ for every $x \ge 0$, so $q(x) = x$ as polynomials, but $q(-1) = \max(-1, 0) = 0$. This is a contradiction.

**Examples underspecify the intent.** Give only the examples $(1, 2) \mapsto 2$ and $(3, 1) \mapsto 3$. The smallest programs that fit are $x \times y$ and $y \times x$, of size $3$. They fit the examples but are not the maximum. Add $(2, 2) \mapsto 2$. Now no program of size at most $5$ fits, and four programs of size $6$ fit: the two correct ones, $\mathrm{ite}(x \le 1, y, x)$ and $\mathrm{ite}(y \le 1, x, y)$. The examples $(3, 5) \mapsto 5$ and $(5, 3) \mapsto 5$ remove the last two. So a synthesizer from examples needs more examples, or a ranking function that prefers some programs, or a question to the user.

## Known algorithms

| method | idea | page |
|---|---|---|
| bottom-up enumeration | build programs by size from smaller ones, and keep one program per output vector on the examples | [bottom-up enumerative synthesis](/bottom-up-enumerative-synthesis/) |
| top-down deduction | split the examples of a goal into sub-goals for the arguments of an operator, and store all answers in a shared graph | [version space algebra](/version-space-algebra/), [string transformation synthesis](/string-transformation-synthesis/) |
| counterexample-guided search | a synthesizer for finitely many inputs and a verifier for all inputs, in a loop | [CEGIS](/cegis/) |
| constraint solving | encode the holes or the shape of a bounded program as variables, and solve with a SAT or SMT solver | [program sketching](/program-sketching/) |
| theorem proving | prove $\forall x\, \exists y\, \varphi(x, y)$ constructively, and extract the program from the proof | [deductive program synthesis](/deductive-program-synthesis/) |
| type-guided search | build only well-typed terms, and split the examples over pattern matches and conditionals | [type-directed synthesis](/type-directed-synthesis/) |
| stochastic search | mutate programs and keep the better ones by a cost on the tests | [genetic programming](/genetic-programming/) |
| games | turn a temporal specification into a game against the environment, and read a strategy | [reactive synthesis](/reactive-synthesis/) |
| complete functional synthesis | for linear integer arithmetic, compile $\varphi(x, y)$ into a program that computes a $y$ whenever one exists (Kuncak et al. 2010) | |

## Bounds

The hypotheses matter. A semantic check of one candidate program is already undecidable for a Turing-complete language, by [Rice's theorem](/rice-theorem/). So the decidable cases restrict either the language or the specification.

**Theorem 1 (undecidable in general).** Realizability is undecidable even when every candidate is a numeral and each check of a candidate is decidable.

*Proof.* Fix a deterministic Turing machine $M$. Let $L$ be the numerals $0, 1, 2, \ldots$, each read as a constant function. Let $\varphi(x, y)$ say "$M$ halts on the empty input within $y$ steps". For one candidate $y$, the check runs $M$ for $y$ steps, so it is decidable. A numeral meets $\varphi$ if and only if $M$ halts. So an algorithm for realizability would decide the [halting problem](/halting-problem/). $\square$

The [syntax-guided synthesis](/syntax-guided-synthesis/) page proves the same for a small arithmetic grammar, from Hilbert's tenth problem.

**Theorem 2 (finite program spaces).** If $L$ is finite and the check "$P$ meets $\varphi$" is decidable for each $P \in L$, then realizability and optimal synthesis are decidable.

*Proof.* Check each program, and return a cheapest one that passes. $\square$

**Theorem 3 (semi-decision).** If $L$ can be enumerated in order of cost and the check is decidable, then enumeration finds a cheapest program whenever one exists, and runs forever on unrealizable specifications.

*Proof.* Each program of cost $c$ appears after finitely many programs, all of cost at most $c$. The first program that passes has the least cost. $\square$

With finitely many examples and a language whose programs all terminate, the check is decidable, so Theorem 3 applies to programming by example. The cost is the problem: the counts in the examples above grow exponentially with the size.

**Known decidable cases with special methods.**

- Linear integer arithmetic: every specification $\varphi(x, y)$ in Presburger arithmetic can be compiled into a program that returns some $y$ with $\varphi(x, y)$ whenever one exists (Kuncak, Mayer, Piskac and Suter 2010). This follows from quantifier elimination for [Presburger arithmetic](/presburger-arithmetic/).
- Church's problem for specifications in S1S, the monadic second-order logic of one successor, is decidable, and when a solution exists, a finite-state one exists (Büchi and Landweber 1969).
- Reactive synthesis from LTL is 2EXPTIME-complete ([Pnueli-Rosner theorem](/pnueli-rosner-theorem/)).
- Sketches whose holes and inputs range over finite domains: decidable, by Theorem 2. [CEGIS](/cegis/) stops on finite candidate spaces.

## Reductions

- **Examples to logic.** A list of examples is the formula $\bigwedge_i f(x_i) = y_i$ with no quantifiers.
- **Bounded synthesis to one exists-forall query.** Encode a program of size at most $s$ by selector variables $\bar{h}$, and ask $\exists \bar{h}\, \forall x\, \varphi(x, [\![P_{\bar{h}}]\!](x))$. Over Boolean inputs this is a 2QBF formula.
- **Synthesis to proof search.** A constructive proof of $\forall x\, \exists y\, \varphi(x, y)$ contains a program; see [deductive program synthesis](/deductive-program-synthesis/) and the [Curry-Howard correspondence](/curry-howard-correspondence/).
- **Reactive synthesis to games.** An LTL specification becomes a [parity game](/parity-game/) between the environment and the system.
- **From the halting problem.** As in Theorem 1.

## Applications

- FlashFill in Microsoft Excel (2013) fills a column of strings from one or two examples ([string transformation synthesis](/string-transformation-synthesis/)).
- Superoptimizers find the shortest instruction sequence equal to a given one.
- Verifiers synthesize loop invariants and ranking functions.
- Repair tools search for small edits that make the failing tests pass.
- Controllers for hardware and robots are synthesized from temporal specifications.
- Code completion in typed languages searches for terms of the expected type.

## References
