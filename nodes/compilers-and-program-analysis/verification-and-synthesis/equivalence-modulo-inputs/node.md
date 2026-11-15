---
tag: 2CNJHT
kind: technique
slug: equivalence-modulo-inputs
name: Equivalence modulo inputs
aliases:
- EMI compiler testing
area: compilers-and-program-analysis/verification-and-synthesis
level: research
summary: Tests compilers by deleting code not run on a given input and checking that the compiled variants all give the same output.
prereqs: [differential-testing, control-flow-graph]
see_also: [translation-validation, dead-code-elimination, grammar-based-fuzzing, delta-debugging, coverage-guided-fuzzing, metropolis-hastings]
sources:
  - paper: doi:10.1145/2594291.2594334
    title: Vu Le, Mehrdad Afshari and Zhendong Su, Compiler validation via equivalence modulo inputs, Proceedings of PLDI 2014
    locator: pp. 216 to 226, the definition of EMI, the Orion tool and its results on GCC and LLVM
  - paper: doi:10.1145/2814270.2814319
    title: Vu Le, Chengnian Sun and Zhendong Su, Finding deep compiler bugs via guided stochastic program mutation, Proceedings of OOPSLA 2015
    locator: pp. 386 to 399, Athena, insertion and deletion in unexecuted code guided by Markov chain Monte Carlo
  - paper: doi:10.1145/2983990.2984038
    title: Chengnian Sun, Vu Le and Zhendong Su, Finding compiler bugs via live code mutation, Proceedings of OOPSLA 2016
    locator: pp. 849 to 863, Hermes and the mutation of executed code
  - paper: doi:10.1145/1993498.1993532
    title: Xuejun Yang, Yang Chen, Eric Eide and John Regehr, Finding and understanding bugs in C compilers, Proceedings of PLDI 2011
    locator: pp. 283 to 294, Csmith, the source of many seed programs, and differential testing of compilers
  - paper: doi:10.1145/3363562
    title: Junjie Chen, Jibesh Patra, Michael Pradel, Yingfei Xiong, Hongyu Zhang, Dan Hao and Lu Zhang, A survey of compiler testing, ACM Computing Surveys 53(1), 2020
    locator: the sections on test oracles, differential testing and EMI
---

Equivalence modulo inputs (EMI) is a way to test an optimizing compiler without a second compiler and without a specification of the output. Take a program $P$ and an input $I$, run $P$ on $I$, and record which statements execute. Statements that do not execute on $I$ can be deleted or changed, and the new program $P'$ still computes the same output on $I$: it is *equivalent modulo $I$*. The compiler, however, sees a different program, and its optimizations take different decisions. If the compiled $P'$ gives a different output on $I$ than the compiled $P$, the compiler has a bug. Le, Afshari and Su introduced the idea in 2014 with the tool Orion and found many bugs in GCC and LLVM.

## In plain words

Give a program one fixed input and watch which lines run. The lines that never run on this input cannot change the result for this input. So delete some of them, at random, and get many slightly different programs that must all print the same thing for this input. Compile each one and run it. A compiler sees all the lines, including the ones that do not run, and its optimizer may treat each version differently. If one compiled version prints something else, the compiler made a mistake, because the programs agree on this input. This needs no second compiler and no list of correct answers, only the original program and its output. The method finds wrong compilations, not proof that a compiler is right.

## When it applies

- The system under test transforms programs and must preserve their meaning: optimizing compilers above all, and also interpreters with JIT compilers, program translators and code generators.
- Seed programs are deterministic and free of undefined behavior on the chosen input, so that their output is defined. Generators such as Csmith make such programs, and existing test suites provide others.
- A coverage tool can tell which statements run on the input. Orion uses the coverage tool of GCC.

What is decidable sets the frame. Whether two programs are equivalent on all inputs is undecidable, by Rice's theorem, and so is whether a compiler is correct for all programs. EMI never asks either question. Equivalence on one input holds by construction, as shown below, so the oracle is a comparison of two outputs. The price is that EMI finds bugs and proves nothing: a variant that agrees does not show that the compiler is right on it, and no number of variants covers all programs. To check one compilation for correctness, use [translation validation](/translation-validation/).

## The template

**Definition.** Programs $P$ and $Q$ are *equivalent modulo $I$*, for a set of inputs $I$, when $P(i) = Q(i)$ for every $i \in I$, where the output includes the termination behavior. Every program is equivalent modulo $I$ to the programs that agree with it on $I$; the set of such programs is infinite.

**Step 1: profile.** Compile $P$ with coverage instrumentation, run it on every $i \in I$ and record the set $U$ of statements that run on no input of $I$.

**Step 2: make variants.** For each variant, delete each statement of $U$ with some probability, keeping the program well-formed: declarations stay, and so do the brackets of compound statements. Orion deletes only. Athena also inserts code into unexecuted regions, and Hermes changes executed code in ways that keep its effect.

**Step 3: compile and compare.** Compile $P$ and each variant $P'$ with the compiler under test, at each optimization level of interest, and run them on $I$. Report a bug when an output differs from $P(i)$, or when the compiler crashes. Reduce the failing variant with [delta debugging](/delta-debugging/) or a C-specific reducer before reporting it.

**Why deleting unexecuted code is safe.** Model the program as a [control flow graph](/control-flow-graph/) of blocks of instructions with a deterministic semantics, as in the toy IR of these pages. Let $B$ be the set of blocks that the run on input $i$ visits, and let $P'$ be $P$ with any instructions removed or changed in blocks outside $B$, terminators and the graph unchanged. By induction on the steps of the run, the run of $P'$ on $i$ visits the same blocks in the same order with the same values in every variable: the two programs agree on every block in $B$, the run of $P$ never leaves $B$, and each step depends only on the current block and the current values. So $P'(i) = P(i)$, including traps and non-termination. For a language such as C the same argument holds for the abstract machine of the language standard, provided that the run of $P$ on $i$ has no undefined behavior; then any difference between the compiled programs is a bug of the compiler.

## Classic examples

**A toy IR illustration.** The program below, on the input $x = 4$, visits `entry` and `small` and returns 5.

```
entry:
  t = x < 10
  br t small big
small:
  y = x + 1
  ret y
big:
  z = x * 3
  w = z - x
  ret w
```

The two instructions of `big` never run on this input, so the four programs obtained by deleting any of them are equivalent modulo $\{x = 4\}$ and must all return 5 after compilation. A compiler that, for instance, merged `small` and `big` into a select, and computed the select wrongly when `big` has no instructions, would show the bug on one of the variants and not on the original. Deleting `w = z - x` leaves `ret w` reading an undefined name, but only on a path that the input never takes. Variants of real C programs must avoid this when the read is undefined behavior on some other input that the test uses.

**Orion (2014).** Orion takes programs generated by Csmith, from the GCC and LLVM test suites and from open-source projects, profiles them with gcov on their single fixed input, and deletes unexecuted statements at random. Le, Afshari and Su report 147 confirmed, unique bugs in GCC and LLVM found in eleven months of testing, most of them miscompilations at common optimization levels, a kind of bug that crashes do not reveal.

**Athena (2015).** Athena both deletes and inserts code in unexecuted regions, and searches the space of variants with [Metropolis-Hastings](/metropolis-hastings/) sampling, preferring variants that differ more from the original program in their control and data flow. It found bugs that Orion's deletions did not reach.

**Hermes (2016).** Hermes changes code that does execute: it inserts code into live regions whose net effect on the state is none on the input, for example code under a condition that is false at run time, or code that saves the variables it changes and restores them, so that the output on $I$ is unchanged. This tests the optimizer on hot paths, which Orion and Athena cannot change.

## Variations

- **Many inputs.** With a larger $I$, fewer statements are unexecuted, and the variants are equivalent on more inputs. Orion uses one input per program, which maximizes the deletable code.
- **Differential EMI.** Compile the variants with several compilers or optimization levels and compare all outputs, combining EMI with [differential testing](/differential-testing/).
- **Other targets.** The same idea tests graphics shader compilers, JIT compilers of dynamic languages and analyzers that must give the same verdict on equivalent programs.
- **Generated seeds.** EMI turns each seed program from a [grammar-based](/grammar-based-fuzzing/) generator such as Csmith into many test programs, which raises the value of each seed.

## Pitfalls

- **Undefined behavior.** If the seed program has undefined behavior on the input, the compiler may produce any output, and a difference is not a bug. Use seeds that avoid it, and check reduced test cases with a tool for undefined behavior before reporting.
- **Nondeterministic programs.** Output that depends on time, addresses or uninitialized memory differs without a bug. Use deterministic seeds and print values, not addresses.
- **Unspecified behavior.** C leaves some choices to the compiler, such as the order in which some function arguments are evaluated. A seed must not depend on them.
- **Well-formedness.** Deleting a declaration, or a statement that a label or a later declaration depends on, makes the variant fail to compile. That is a bug of the mutator, not of the compiler.
- **Duplicate reports.** Many variants trigger the same compiler bug. Reduce them and group them by the reduced test case before reporting.
- **Expecting a proof.** A long EMI campaign with no difference does not show that the compiler is correct.

## Exercises

1. Prove the lemma of the template for the toy IR, with traps and running out of fuel included in the output.
2. Give a program and two inputs such that a statement that does not run on the first input runs on the second, and show a variant that is equivalent modulo the first input but not modulo both.
3. Explain why deleting a statement that does not execute in C can still change the output of a correct compiler when the seed program has undefined behavior on the input.
4. For a program with $k$ unexecuted statements, how many variants does deletion alone give? Why does Orion sample them at random instead of enumerating them?
5. Design a semantics-preserving change of executed code in the toy IR, in the spirit of Hermes, and show that it keeps the output on every input.

## References
