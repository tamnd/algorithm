---
tag: HT82RC
kind: concept
slug: program-verification
name: Program verification
aliases:
- Formal verification of programs
- Deductive verification
area: foundations/correctness-and-invariants
level: advanced
summary: Using formal logic and proof tools to establish that a program meets its specification.
prereqs: [specification, hoare-triple, weakest-precondition, loop-invariant]
see_also: [hoare-logic, separation-logic, refinement-calculus, abstract-interpretation, symbolic-execution, rice-theorem, temporal-logic, smt-problem]
sources:
  - paper: doi:10.1090/psapm/019/0235771
    title: R. W. Floyd, Assigning meanings to programs, in Mathematical Aspects of Computer Science, Proceedings of Symposia in Applied Mathematics 19, AMS (1967)
    locator: pp. 19 to 32
  - paper: doi:10.1145/363235.363259
    title: C. A. R. Hoare, An axiomatic basis for computer programming, Communications of the ACM 12(10) (1969)
    locator: pp. 576 to 580
  - paper: doi:10.1145/360933.360975
    title: Edsger W. Dijkstra, Guarded commands, nondeterminacy and formal derivation of programs, Communications of the ACM 18(8) (1975)
    locator: pp. 453 to 457 (weakest preconditions)
  - paper: doi:10.1137/0207005
    title: Stephen A. Cook, Soundness and completeness of an axiom system for program verification, SIAM Journal on Computing 7(1) (1978)
    locator: pp. 70 to 90 (relative completeness, expressive assertion languages)
  - paper: doi:10.1090/S0002-9947-1953-0053041-6
    title: H. G. Rice, Classes of recursively enumerable sets and their decision problems, Transactions of the American Mathematical Society 74(2) (1953)
    locator: pp. 358 to 366
  - paper: doi:10.1007/978-3-642-17511-4_20
    title: K. Rustan M. Leino, Dafny, an automatic program verifier for functional correctness, LPAR-16 (2010), LNCS 6355, Springer
    locator: pp. 348 to 370 (specification constructs, translation to Boogie)
  - paper: doi:10.1007/11804192_17
    title: Mike Barnett, Bor-Yuh Evan Chang, Robert DeLine, Bart Jacobs and K. Rustan M. Leino, Boogie, a modular reusable verifier for object-oriented programs, FMCO 2005, LNCS 4111, Springer (2006)
    locator: pp. 364 to 387 (the intermediate language, verification conditions sent to an SMT solver)
  - paper: doi:10.1007/978-3-642-37036-6_8
    title: Jean-Christophe Filliatre and Andrei Paskevich, Why3, where programs meet provers, ESOP 2013, LNCS 7792, Springer
    locator: pp. 125 to 128 (WhyML, verification conditions sent to several provers)
  - paper: doi:10.1145/1538788.1538814
    title: Xavier Leroy, Formal verification of a realistic compiler, Communications of the ACM 52(7) (2009)
    locator: pp. 107 to 115 (CompCert, proved in Coq)
  - paper: doi:10.1145/1629575.1629596
    title: Gerwin Klein and others, seL4, formal verification of an OS kernel, SOSP 2009
    locator: pp. 207 to 220 (proof in Isabelle/HOL)
  - url: "https://rocq-prover.org/releases/9.0.0"
    locator: release notes of Rocq 9.0 (March 2025), the rename of Coq to Rocq
  - paper: doi:10.1007/BFb0025774
    title: Edmund M. Clarke and E. Allen Emerson, Design and synthesis of synchronization skeletons using branching time temporal logic, Logics of Programs 1981, LNCS 131, Springer (1982)
    locator: pp. 52 to 71
  - paper: doi:10.1007/3-540-11494-7_22
    title: Jean-Pierre Queille and Joseph Sifakis, Specification and verification of concurrent systems in CESAR, International Symposium on Programming 1982, LNCS 137, Springer
    locator: pp. 337 to 351
  - paper: doi:10.1145/781131.781153
    title: Bruno Blanchet, Patrick Cousot, Radhia Cousot, Jerome Feret, Laurent Mauborgne, Antoine Mine, David Monniaux and Xavier Rival, A static analyzer for large safety-critical software, PLDI 2003
    locator: pp. 196 to 207 (the Astree analyzer)
---

Program verification is the use of formal logic and proof tools to show that a program meets its [specification](/specification/) for every input that the specification allows. A test checks some runs of the program. A verification covers all of them. The main methods are deductive proof with [Hoare logic](/hoare-logic/) and [weakest preconditions](/weakest-precondition/), model checking, and sound static analysis by [abstract interpretation](/abstract-interpretation/). [Rice's theorem](/rice-theorem/) shows that no tool can decide correctness for all programs, so each method accepts a limit.

## In plain words

A test runs your program on a few inputs and looks at the results. Verification is different: you write down what the program must do, and then you build a proof that it does this for every input.

You state what must be true before the program starts, and what must be true when it stops. For each loop you give a fact that stays true at each pass. A tool turns the program and these facts into many small questions of logic, and a prover answers each one. If it answers all of them, the program does what you wrote down, for every input. If one fails, it shows you where to look.

There is a hard limit. No tool can decide, for every program, whether the program is correct. So a verifier may say "I cannot prove this" about a program that is in fact correct.

## The idea

**What is proved.** Let $S$ be a program, $P$ a [precondition](/precondition/) and $Q$ a [postcondition](/postcondition/). Program verification proves the [Hoare triple](/hoare-triple/) $\{P\}\ S\ \{Q\}$ ([partial correctness](/partial-correctness/)) or $[P]\ S\ [Q]$ ([total correctness](/total-correctness/)). The proof is a mathematical object. It is valid for the semantics of the language that the tool uses, for example unbounded integers or machine integers, and it assumes that the tool itself is sound. It says nothing about a wrong specification.

**Deductive verification.** Floyd (1967) and Hoare (1969) founded the method, and Dijkstra (1975) gave the weakest precondition calculus. The user annotates each method with a precondition and a postcondition, and each loop with an [invariant](/loop-invariant/) and a [variant function](/variant-function/). A *verification condition generator* computes, from the annotated program, a list of logical formulas (the *verification conditions*) whose validity implies the triple. It uses the weakest precondition rules: for assignment $\mathrm{wp}(x \leftarrow E, Q) = Q[E/x]$, for sequence $\mathrm{wp}(S_1 ; S_2, Q) = \mathrm{wp}(S_1, \mathrm{wp}(S_2, Q))$, and for a loop a set of separate formulas. For a loop $\mathbf{while}\ B\ \mathbf{do}\ S$ with invariant $I$ and variant $V$ these formulas are:

- Initialization: $P \implies I$, where $P$ holds at the loop entry.
- Preservation: $I \wedge B \implies \mathrm{wp}(S, I)$.
- Exit: $I \wedge \neg B \implies Q$.
- Termination: $I \wedge B \implies 0 \le V$, and $I \wedge B \wedge V = V_0 \implies \mathrm{wp}(S, V < V_0)$ for each integer $V_0$.

An automatic prover checks the formulas. Usually it is an SMT solver, a program that decides the [SMT problem](/smt-problem/): satisfiability of formulas over theories such as linear arithmetic and arrays. A formula is valid when its negation is unsatisfiable. If every formula is valid, the triple holds. This is the soundness of the method, and it is the same argument as the one for the rule of iteration in [Hoare logic](/hoare-logic/).

A failed check does not prove the program wrong. The invariant may be too weak, or the formula may lie in an undecidable theory, such as nonlinear integer arithmetic (see [Hilbert's tenth problem](/hilberts-tenth-problem/)), where the solver times out or answers "unknown".

[Separation logic](/separation-logic/) is an extension of Hoare logic for programs with pointers. It adds an assertion that the heap splits into disjoint parts, and a frame rule for local proofs. Deductive tools for heap programs use it in the same way as above, with annotations and a prover.

**Tools.** Dafny (Leino 2010) has specification constructs in the language and translates a program to Boogie. Boogie (Barnett and others 2006) is an intermediate verification language: it generates the verification conditions and sends them to an SMT solver. Why3 (Filliatre and Paskevich 2013) is a platform in which a program is written with contracts in the language WhyML, and the generated conditions go to several automatic and interactive provers. Proof assistants such as Rocq (formerly Coq, renamed in 2025) and Isabelle/HOL use a richer logic, type theory or higher-order logic, in which the program and its semantics are encoded and the proof is built interactively. They need more work from the user. The CompCert C compiler is proved correct in Coq (Leroy 2009), and the seL4 microkernel is proved correct in Isabelle/HOL (Klein and others 2009).

**Model checking.** A model checker explores the states of a finite model of the system and checks a property in [temporal logic](/temporal-logic/). It needs no invariant from the user, and it returns a counterexample run when the property fails. Clarke and Emerson (1981, published 1982) and Queille and Sifakis (1982) introduced it. Its limit is the number of states, the [state explosion problem](/state-explosion-problem/). A program with unbounded data has an infinite state space, so a checker must use an abstraction or a bound, as in [bounded model checking](/bounded-model-checking/).

**Sound static analysis.** [Abstract interpretation](/abstract-interpretation/) computes an invariant by itself, in an abstract domain such as intervals. The analyzer is sound and automatic, and it can raise false alarms.

**Other approaches.** The [refinement calculus](/refinement-calculus/) derives a program from its specification, so the program is correct by construction. [Symbolic execution](/symbolic-execution/) explores paths with symbolic inputs. It is exhaustive only when the number of paths is bounded, so it is mainly a bug-finding method.

**The limit.** Rice's theorem (Rice 1953) states that each nontrivial semantic property of programs is undecidable. A property is *semantic* when it depends only on the function that the program computes. It is *nontrivial* when some programs have it and some do not. For a fixed function $f$, the property "the program computes $f$" is semantic. It is nontrivial when $f$ is computable, since some program computes $f$ and some program does not. So no algorithm takes a program and decides whether it meets this specification. The same is true for the property "the program stops on all inputs" (see the [halting problem](/halting-problem/)). Hence a verifier that always stops cannot be both sound and complete on all programs. It gives up something: it covers only a class of programs (for example finite-state ones), it rejects some correct programs, it may run forever, it needs a person to supply invariants or proofs, or it gives up soundness and may miss errors. The deductive tools above stay sound, reject some correct programs, and need annotations from the user.

Cook (1978) shows that Hoare logic is complete relative to the truth of the assertion language, provided that language is expressive (it can state every weakest precondition). So the hard parts of a proof are to find the invariants and to prove the formulas of the assertion language.

**Pitfalls.**

- *A weak specification.* The postcondition $s \ge 0$ for a sum of $1, \ldots, n$ is met by the program $s \leftarrow 0$. The proof succeeds, and the program is useless. A proof is only as good as the specification.
- *A mismatch of semantics.* A proof over unbounded integers says nothing about a run with [integer overflow](/integer-overflow/) on 64-bit machine integers. The tool must model the machine type, or the proof must add bounds.
- *Partial instead of total correctness.* Without a variant, the proof shows only that each run that stops is correct. A loop that never stops meets every partial-correctness triple.
- *Assumptions.* Verifiers let the user assume a fact without proof (for example the `assume` command of Boogie). A false assumption makes every later formula trivially valid.

## Examples

**A loop with an invariant.** The method below, in Dafny syntax, computes $1 + 2 + \cdots + n$.

```dafny
method Sum(n: int) returns (s: int)
  requires n >= 0
  ensures 2 * s == n * (n + 1)
{
  var i := 0;
  s := 0;
  while i < n
    invariant 0 <= i <= n
    invariant 2 * s == i * (i + 1)
    decreases n - i
  {
    i := i + 1;
    s := s + i;
  }
}
```

Let $I$ be $0 \le i \le n \wedge 2s = i(i+1)$. The body is $i \leftarrow i + 1 ;\ s \leftarrow s + i$. By the assignment rule and the rule for sequence, $\mathrm{wp}(\text{body}, I)$ is $I$ with $i$ replaced by $i + 1$ and $s$ replaced by $s + (i + 1)$. The verification conditions are as follows.

- Initialization: $n \ge 0 \implies 0 \le 0 \le n \wedge 2 \cdot 0 = 0 \cdot 1$. This is true.
- Preservation: $I \wedge i < n \implies 0 \le i + 1 \le n \wedge 2(s + i + 1) = (i + 1)(i + 2)$. The bounds follow from $0 \le i < n$. For the equation, $2(s + i + 1) = i(i+1) + 2i + 2 = i^2 + 3i + 2 = (i+1)(i+2)$, using $2s = i(i+1)$.
- Exit: $I \wedge \neg(i < n) \implies 2s = n(n+1)$. From $i \le n$ and $i \ge n$ we get $i = n$, and the equation follows.
- Termination: under $I \wedge i < n$, the value $n - i$ is positive, the new value $n - (i + 1)$ is not negative, and it is smaller by exactly 1.

These are the four formulas that the verifier sends to its prover, and all four are valid.

**A non-example: a wrong invariant.** Replace the second invariant by $2s = i(i - 1)$. Initialization holds, because $2 \cdot 0 = 0 \cdot (-1)$. Preservation fails: the new invariant needs $2(s + i + 1) = (i+1)i$, and under $2s = i(i-1)$ the left side is $i^2 + i + 2$ while the right side is $i^2 + i$. They differ by 2 for each $i$. For example, $i = 0$, $s = 0$, $n = 1$ satisfies the invariant and the guard, and after the body $i = 1$, $s = 1$, but $1 \cdot 0 = 0 \ne 2$. The verifier reports a failing condition for the loop body, and it does not accept the program with this invariant.

**A non-example: a test.** Running $\mathrm{Sum}$ for $n = 0$ to $29$ and comparing $2s$ with $n(n+1)$ finds no error. This is a test of 30 inputs. It does not show the result for $n = 30$. The proof above covers each integer $n \ge 0$.

## Where it is used

- Compilers and operating system kernels: CompCert (Leroy 2009) and seL4 (Klein and others 2009), both cited above.
- Tools for working programmers: Dafny and Why3 check contracts in the code, and the contracts are the [design by contract](/design-by-contract/) idea made formal.
- Static analyzers that prove the absence of run-time errors, built on abstract interpretation. Astree (Blanchet and others 2003) is such an analyzer for safety-critical embedded C code.
- Model checkers for protocols, hardware, and concurrent code with a finite state space.
- Teaching: the [loop invariant](/loop-invariant/) is the central skill, and a verifier gives fast feedback on it.

## References
