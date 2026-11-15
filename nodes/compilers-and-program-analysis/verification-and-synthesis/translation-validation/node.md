---
tag: HA37X1
kind: technique
slug: translation-validation
name: Translation validation
aliases:
- compiler translation validation
area: compilers-and-program-analysis/verification-and-synthesis
level: advanced
summary: Proves after each compilation that the output program refines the input one, instead of proving the compiler correct once.
prereqs: [simulation-relation, control-flow-graph]
see_also: [verified-compilation, self-composition, equivalence-checking, peephole-optimization, smt-problem, bounded-model-checking, proof-carrying-code, bisimulation]
sources:
  - paper: doi:10.1007/BFb0054170
    title: Amir Pnueli, Michael Siegel and Eli Singerman, Translation validation, Proceedings of TACAS 1998, LNCS 1384
    locator: the name and the idea, a validator that checks each run of a compiler from the synchronous language Signal to C instead of the compiler itself
  - paper: doi:10.1145/349299.349314
    title: George C. Necula, Translation validation for an optimizing compiler, Proceedings of PLDI 2000
    locator: pp. 83 to 94, a validator for the optimizations of the GNU C compiler that infers a simulation relation between the program before and after each pass and checks it
  - paper: doi:10.1145/1328438.1328444
    title: Jean-Baptiste Tristan and Xavier Leroy, Formal verification of translation validators, a case study on instruction scheduling optimizations, Proceedings of POPL 2008
    locator: pp. 17 to 27, validators for list scheduling and trace scheduling whose own soundness is proved in Coq, so that the validated pass is as trusted as a verified one
  - paper: doi:10.1145/2737924.2737965
    title: Nuno P. Lopes, David Menendez, Santosh Nagarakatte and John Regehr, Provably correct peephole optimizations with Alive, Proceedings of PLDI 2015
    locator: pp. 22 to 32, peephole rewrite rules of LLVM checked with an SMT solver, with refinement in the presence of undefined behavior
  - paper: doi:10.1145/3453483.3454030
    title: Nuno P. Lopes, Juneyoung Lee, Chung-Kil Hur, Zhengyang Liu and John Regehr, Alive2, bounded translation validation for LLVM, Proceedings of PLDI 2021
    locator: pp. 65 to 79, refinement checking of whole LLVM functions with loops unrolled a bounded number of times, and the bugs it found
---

Translation validation checks the output of a compiler instead of the compiler. After each compilation, or each pass, a separate validator tries to prove that the target program refines the source program: every behavior of the target is a behavior of the source. If the proof succeeds, that one output is correct; if it fails, the output is rejected or the pass is skipped. The method proves one run of the compiler, not the compiler, so it can work with a large, untrusted, changing compiler, but it says nothing about the next input.

## In plain words

Proving a whole compiler correct is a huge job, and the proof breaks each time somebody changes the compiler. There is a cheaper way. Let the compiler do its work as usual, and then check its answer. A checker looks at the program before and after the change and tries to show that the two do the same thing, often with hints about which parts of one match which parts of the other. Checking is usually much simpler than the clever work that made the change. If the check passes, you can trust this one output. If the check fails, you throw the output away and use a safer one. You never learn whether the compiler is right in general, only whether it was right this time.

## When it applies

- A transformation is hard to prove correct once, but easy to check on each example: instruction scheduling, register allocation, loop optimizations, peephole rewrites, code generation from a high-level language.
- The source and the target have a precise semantics, so "the target refines the source" has a meaning.
- The two programs are close in structure, so a relation between their program points and states can be guessed or emitted by the compiler.

Equivalence of programs is undecidable, by [Rice's theorem](/rice-theorem/), so every validator is incomplete: it can reject a correct output. For loop-free code over fixed-width integers the check is decidable, and validators hand it to an [SMT solver](/smt-problem/).

## The template

```pseudo id=main
VALIDATED-COMPILE(S)
L1  T <- PASS(S)                          ▷ any compiler pass, not trusted
L2  R <- RELATION(S, T)                   ▷ hole RELATION: cut points and a relation between states at them
L3  conds <- CONDITIONS(S, T, R)          ▷ hole CONDITIONS: entry, step and exit conditions below
L4  if PROVE(conds) then return T         ▷ hole PROVER: an SMT solver, a decision procedure, a symbolic evaluator
L5  return FALLBACK(S)                    ▷ hole FALLBACK: the output without this pass, or an error
```

**The relation.** Choose *cut points* in the [control flow graph](/control-flow-graph/) of $T$, including the entry, the exit and a point on every cycle, and a matching cut point in $S$ for each. A *segment* is a path from one cut point to the next with no cut point inside. For each pair of matching points, $R$ is a formula over the states of $T$ and $S$ there, for example "the variables $x$ agree, and $t_T = a \cdot b$". This is a [simulation relation](/simulation-relation/) at the level of segments.

**The conditions.**

1. *Entry.* The two entry states, with equal inputs, are related by $R$.
2. *Step.* If $(t, s) \in R$ at matching points and a segment of $T$ leads from $t$ to $t'$, then some nonempty segment path of $S$ leads from $s$ to an $s'$ with $(t', s') \in R$ at the matching points.
3. *Exit.* If $(t, s) \in R$ at the exits, the outputs of $t$ and $s$ are equal.

**Why it is sound.** Suppose the three conditions hold. Take a run of $T$ and cut it at its cut points into segments $t_0 \to t_1 \to \cdots$. By induction on $k$, with the entry condition as the base and the step condition as the step, there are states $s_0 \to s_1 \to \cdots$ of a run of $S$ with $(t_k, s_k) \in R$ for every $k$. If the run of $T$ stops, the exit condition gives the same output. If it does not stop, the run of $S$ does not stop either, since each matched segment is nonempty. So every behavior of $T$ is a behavior of $S$. $\square$

The theorem is about this $S$ and this $T$. It does not mention PASS, so it gives no guarantee for a different input.

**Walk-through.** [Loop-invariant code motion](/loop-invariant-code-motion/) turns

$S$: $i := 0;\ \mathbf{while}\ i < n\ \mathbf{do}\ (t := a \cdot b;\ c[i] := t + i;\ i := i + 1)$

into

$T$: $t := a \cdot b;\ i := 0;\ \mathbf{while}\ i < n\ \mathbf{do}\ (c[i] := t + i;\ i := i + 1)$,

where $t$ is a temporary that is not an output. The cut points are the entries, the loop heads and the exits. At the loop heads, $R$ says $i_T = i_S$, $c_T = c_S$, $n$, $a$ and $b$ agree, and $t_T = a \cdot b$. It does not say $t_T = t_S$: before the first turn of $S$, $t_S$ is unset. Entry: the segment of $T$ to the loop head sets $t_T = a \cdot b$ and $i_T = 0$, and the matching segment of $S$ sets $i_S = 0$. Step: one turn of each loop sets $t_S := a \cdot b = t_T$, so both write $c[i] := a \cdot b + i$, and both increase $i$. Exit: both leave the loop when $i \ge n$, with equal $c$. An SMT solver proves each condition from the formulas of the segments. If $t$ were an output, the exit condition would fail for $n \le 0$, and the validator would reject the pass, rightly.

## Classic examples

- **Synchronous languages.** Pnueli, Siegel and Singerman named the method and used it for a code generator from the synchronous language Signal to C, a generator that was too big to verify.
- **An optimizing C compiler.** Necula validated the optimization passes of the GNU C compiler, such as [common subexpression elimination](/common-subexpression-elimination/), register allocation and instruction scheduling, by inferring the relation from the two programs and checking it with a symbolic evaluator.
- **Peephole rules.** Alive proves each [peephole](/peephole-optimization/) rewrite rule of LLVM correct for all inputs with an SMT solver, or gives a counterexample. Here the validated object is a rule, which then serves for every compilation.
- **Whole-function checking.** Alive2 checks that the LLVM function after an optimization refines the function before it. It unrolls loops a bounded number of times, so it is a bounded check in the sense of [bounded model checking](/bounded-model-checking/), and it found dozens of bugs in LLVM.
- **Verified validators.** In [verified compilation](/verified-compilation/), Tristan and Leroy proved in Coq that their validators for list scheduling and trace scheduling are sound. A pass that is checked by a verified validator is then as trusted as a verified pass, though the pass itself is not proved.

## Variations

- **Equivalence or refinement.** For deterministic, fully defined programs the condition is equivalence. With undefined behavior or nondeterminism it is refinement: the target may do anything the source may do, so the target may be more defined than the source, but not less.
- **Certifying compilers.** The compiler emits the relation $R$, or a full proof, with its output. The validator only checks it, which is simpler than inferring it. This is close to [proof-carrying code](/proof-carrying-code/), with a correctness property instead of a safety policy.
- **Product programs.** The two programs can be combined into one product program, whose safety is the equivalence, as in [self-composition](/self-composition/); then any one-program verifier can do the check.
- **Bounded validation.** Unroll loops and check up to a bound. It finds real bugs with no false alarms, but a pass is not proved correct for longer runs.
- **Equivalence checking of circuits.** Hardware design uses the same idea to check a synthesized netlist against its specification; see [equivalence checking](/equivalence-checking/).

## Pitfalls

- **One run, not the compiler.** A validator that accepts a million compilations proves nothing about the next one. A bug in the pass shows up as a rejected output, so a fallback is needed.
- **False alarms.** The validator can fail to find a relation for a correct output, for example after a transformation that it does not understand. Then a correct optimization is lost, or the build fails.
- **The validator is trusted.** A bug in the validator, or in the semantics it uses, lets wrong code through. Either keep it small and simple or prove it, as Tristan and Leroy did.
- **Use the compiler's semantics.** The validator must use the same rules as the compiler for undefined behavior, memory and integer overflow. A validator that is stricter rejects good code, and one that is looser accepts bad code.
- **Bounded checks are not proofs.** A check that unrolls loops $k$ times, or tests inputs from a small range, is evidence, not proof.

## Exercises

1. Why does validating every compilation of a test suite not prove the compiler correct? *Answer.* The theorem is about each pair $(S, T)$ that was checked. A new source program can hit a bug that no checked program hit, and then its validation fails or, with a bounded validator, can even pass.
2. In the walk-through, let $t$ be an output. Give an input on which $S$ and $T$ differ. *Answer.* $n = 0$ and $t$ unset, say 7, at the start. $S$ never assigns $t$ and ends with $t = 7$, while $T$ ends with $t = a \cdot b$.
3. The source is $x := y / z$ in a language where division by zero is undefined behavior, and the target is $x := (z = 0\ ?\ 0 : y / z)$. Does the target refine the source? *Answer.* Yes. When $z = 0$ the source may do anything, so returning 0 is one of its behaviors; when $z \ne 0$ both compute $y / z$. The other direction fails.
4. Why must each segment of $T$ be matched by a nonempty path of $S$? *Answer.* Otherwise a non-terminating run of $T$ could be matched by a finite run of $S$ that then stops, and the target could loop where the source stops.

## References
