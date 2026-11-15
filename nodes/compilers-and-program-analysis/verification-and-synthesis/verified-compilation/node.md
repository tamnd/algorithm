---
tag: NYWK2C
kind: concept
slug: verified-compilation
name: Verified compilation
aliases:
- certified compiler
- compiler correctness proof
area: compilers-and-program-analysis/verification-and-synthesis
level: advanced
summary: A compiler with a machine-checked proof that the semantics of each compiled program refines the semantics of its source.
prereqs: [simulation-relation, structural-induction]
see_also: [translation-validation, proof-carrying-code, type-soundness, bisimulation, verification-condition-generation, equivalence-checking, peephole-optimization, curry-howard-correspondence]
sources:
  - paper: "John McCarthy and James Painter, Correctness of a compiler for arithmetic expressions, in Mathematical Aspects of Computer Science, Proceedings of Symposia in Applied Mathematics 19, American Mathematical Society, 1967"
    locator: pp. 33 to 41, the first proof that a compiler preserves the meaning of the programs it translates, for arithmetic expressions
  - paper: doi:10.1145/1538788.1538814
    title: Xavier Leroy, Formal verification of a realistic compiler, Communications of the ACM 52(7), 2009
    locator: pp. 107 to 115, the CompCert compiler from a large subset of C to PowerPC assembly, programmed and proved in Coq, and the statement of semantic preservation
  - paper: doi:10.1007/s10817-009-9155-4
    title: Xavier Leroy, A formally verified compiler back-end, Journal of Automated Reasoning 43(4), 2009
    locator: pp. 363 to 446, forward simulation diagrams, the use of determinism of the target to turn a forward simulation into a backward one, and the proof of each pass
  - paper: doi:10.1145/2535838.2535841
    title: Ramana Kumar, Magnus O. Myreen, Michael Norrish and Scott Owens, CakeML, a verified implementation of ML, Proceedings of POPL 2014
    locator: pp. 179 to 191, a verified compiler and read-eval-print loop for a subset of Standard ML, proved in HOL4
  - paper: doi:10.1145/1993498.1993532
    title: Xuejun Yang, Yang Chen, Eric Eide and John Regehr, Finding and understanding bugs in C compilers, Proceedings of PLDI 2011
    locator: pp. 283 to 294, random testing with Csmith, which found wrong-code bugs in every compiler tested except the verified middle end of CompCert, and bugs in its unverified parts
---

A verified compiler comes with a proof, checked by a machine, that every program it compiles behaves as its source says. The proof is about the compiler, so it covers every input at once, unlike [translation validation](/translation-validation/), which checks one output at a time. The usual statement is *semantic preservation*: if the source program has no undefined behavior, every behavior of the compiled program is a behavior of the source. The proof is a chain of [simulation relations](/simulation-relation/), one for each pass, checked in a proof assistant such as Coq or HOL4.

## In plain words

A compiler can have bugs, and a bug in a compiler can break a program that was correct, even a program that was proved correct. A verified compiler removes that risk. Its authors write down exactly what the source language means and what the machine code means. Then they prove, with a computer that checks every step of the proof, that the compiler never changes what a program does. The proof is about all programs, not only the ones that were tested. What is left to trust is small: the two descriptions of meaning, the proof checker, and the tools that run before and after the compiler.

## The idea

**The statement.** Let $\mathrm{Beh}(P)$ be the set of behaviors of a program $P$: for example, "stops with output $o$", "runs for ever", or "goes wrong". A compiler $\mathrm{Comp}$ is a partial function: it returns a target $T = \mathrm{Comp}(S)$ or fails. It is *correct* if for every source $S$ with $\mathrm{Comp}(S) = T$ and every $S$ that cannot go wrong,

$$\mathrm{Beh}(T) \subseteq \mathrm{Beh}(S).$$

A compiler that always fails is correct under this definition. Correctness promises nothing about which programs compile, only about the outputs. Undefined behavior in $S$ is excluded because the source semantics allows anything then, and the target may do anything.

**Why it is not automatic.** Whether two programs have the same behaviors is undecidable, by [Rice's theorem](/rice-theorem/), and a compiler must be right for infinitely many sources. So the proof cannot be found by a decision procedure. People write it, by [induction](/structural-induction/) over programs and runs, and a proof assistant checks it. The proof assistant reduces the trust to its small kernel, by the [Curry-Howard correspondence](/curry-howard-correspondence/) in the case of Coq.

**Simulation diagrams.** Each pass is proved with a relation $\sim$ between the states of its source and its target. A *forward simulation* says: initial states are related; if $s \sim t$ and $s \to s'$ in the source, then $t \to^+ t'$ in the target with $s' \sim t'$; and related final states give the same result. Variants allow the target to take zero steps when a measure on the source decreases, so that a source step that is compiled away does not hide divergence. A forward simulation is natural for a compiler, since each source construct is compiled into some target code, and an induction on the source run shows $\mathrm{Beh}(S) \subseteq \mathrm{Beh}(T)$ for the behaviors that stop or run for ever.

**Forward plus determinism gives backward.** The statement asks for the other inclusion, $\mathrm{Beh}(T) \subseteq \mathrm{Beh}(S)$, which is harder to prove directly, because the target has more, smaller steps. Determinism closes the gap. *Claim.* If $S$ cannot go wrong and has at least one behavior, every behavior of $S$ is a behavior of $T$, and $T$ is deterministic, so that it has exactly one behavior, then $\mathrm{Beh}(T) \subseteq \mathrm{Beh}(S)$. *Proof.* Pick a behavior $b$ of $S$. By the forward simulation $b \in \mathrm{Beh}(T)$. Since $T$ has only one behavior, $\mathrm{Beh}(T) = \{b\} \subseteq \mathrm{Beh}(S)$. $\square$ CompCert uses this argument: its target languages are deterministic, so forward simulations are enough.

**Composition.** A compiler is a sequence of passes $S = P_0 \to P_1 \to \cdots \to P_k = T$. Simulations compose. Suppose each pass satisfies $\mathrm{Beh}(P_{j+1}) \subseteq \mathrm{Beh}(P_j)$ whenever $P_j$ cannot go wrong. If $S = P_0$ cannot go wrong, then $P_1$ has no behavior that $P_0$ lacks, so it cannot go wrong either, and by induction on $j$ every $P_j$ cannot go wrong and $\mathrm{Beh}(T) \subseteq \mathrm{Beh}(S)$. So each pass is proved alone, against the semantics of its own intermediate languages.

**Validated passes.** A pass can be left unproved if its output is checked by a validator whose soundness is proved, as Tristan and Leroy did for instruction scheduling. The composed theorem still holds, because a pass that fails validation makes the compiler fail, which is allowed.

**What is trusted.** The semantics of the source and of the target, the proof checker, and the tools around the verified part: the parser if it is not verified, the assembler, the linker, and the extraction of the compiler from the proof assistant into runnable code. Errors in any of these are outside the theorem.

## Examples

**A compiler for expressions.** In the spirit of McCarthy and Painter (1967), take expressions $e ::= n \mid x \mid e_1 + e_2$ and a stack machine with instructions $\mathrm{PUSH}\ n$, $\mathrm{LOAD}\ x$ and $\mathrm{ADD}$, which pops two values and pushes their sum. The compiler is

$$C(n) = [\mathrm{PUSH}\ n], \quad C(x) = [\mathrm{LOAD}\ x], \quad C(e_1 + e_2) = C(e_1) \mathbin{+\!\!+} C(e_2) \mathbin{+\!\!+} [\mathrm{ADD}].$$

Let $\mathrm{run}(c, \sigma)$ be the stack after running code $c$ from stack $\sigma$ in an environment $\rho$, and $[\![e]\!]\rho$ the value of $e$. *Claim.* For every $e$, code $c$ and stack $\sigma$, $\mathrm{run}(C(e) \mathbin{+\!\!+} c, \sigma) = \mathrm{run}(c, [\![e]\!]\rho :: \sigma)$. *Proof.* By [structural induction](/structural-induction/) on $e$. For $n$ and $x$ the first instruction pushes $n$ or $\rho(x)$. For $e_1 + e_2$, the hypothesis for $e_1$, with the code $C(e_2) \mathbin{+\!\!+} [\mathrm{ADD}] \mathbin{+\!\!+} c$, gives the stack $v_1 :: \sigma$; the hypothesis for $e_2$ gives $v_2 :: v_1 :: \sigma$; and $\mathrm{ADD}$ leaves $(v_1 + v_2) :: \sigma$, which is $[\![e_1 + e_2]\!]\rho :: \sigma$. $\square$ With $c$ empty and $\sigma$ empty, the compiled code leaves exactly the value of $e$. The general $c$ and $\sigma$ in the claim are what makes the induction go through: a statement only about $C(e)$ alone on an empty stack is too weak to be an induction hypothesis.

**CompCert.** Leroy and others wrote a compiler from a large subset of C to assembly language for several processors, as a program in Coq, and proved semantic preservation for it in Coq. The compiler is extracted to OCaml to run. It optimizes, with passes such as constant propagation, common subexpression elimination and register allocation, so it is a real compiler and not a toy.

**CakeML.** Kumar, Myreen, Norrish and Owens built a verified implementation of a subset of Standard ML in HOL4, including the parser, type inference and a read-eval-print loop, and ran the compiler on itself inside the logic, so that the verified compiler is also the binary that runs.

**Evidence from testing.** Yang, Chen, Eide and Regehr ran the random program generator Csmith against many C compilers for years. They found wrong-code bugs in every compiler they tested except in the verified middle end of CompCert. They did find bugs in its unverified parts, which then were verified or fixed. The theorem covered what it claimed, and nothing more.

**Non-example.** A compiler whose output is checked by an unverified validator for each run is not a verified compiler. It may produce only correct outputs in practice, but no theorem covers the next input.

## Where it is used

- **Safety-critical code.** When the source code has been verified, for example with [verification conditions](/verification-condition-generation/), a verified compiler carries the proof to the machine code, so that the binary is covered and not only the source.
- **Language implementations.** Verified compilers exist for C, ML, and a growing number of domain-specific languages, and for parts of larger systems such as just-in-time compilers.
- **Certified optimizations.** Each optimization added to a verified compiler needs its own simulation proof, or a verified validator. [Peephole](/peephole-optimization/) rules can be checked one by one by an SMT solver, which is a lighter form of the same goal.
- **Relation to other methods.** [Proof-carrying code](/proof-carrying-code/) proves a safety policy of each output without trusting the compiler. Translation validation proves the correctness of each output. A verified compiler proves the correctness of all outputs once, at the cost of a large proof that must be updated when the compiler changes. [Type soundness](/type-soundness/) is the analog for one language: well-typed programs do not go wrong, proved once for the type system.

## References
