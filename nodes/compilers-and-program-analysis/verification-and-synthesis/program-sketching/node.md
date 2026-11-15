---
tag: M40E38
kind: technique
slug: program-sketching
name: Program sketching
aliases:
- sketch-based synthesis
area: compilers-and-program-analysis/verification-and-synthesis
level: advanced
summary: The programmer writes a program with holes and the synthesizer fills the holes with constants or expressions so the assertions hold.
prereqs: [program-synthesis, cegis]
see_also: [syntax-guided-synthesis, qbf, polynomial-hierarchy, bounded-model-checking, bit-blasting, symbolic-execution, superoptimization, deductive-program-synthesis]
sources:
  - paper: doi:10.1145/1065010.1065045
    title: Armando Solar-Lezama, Rodric Rabbah, Rastislav Bodík and Kemal Ebcioğlu, Programming by sketching for bit-streaming programs, Programming Language Design and Implementation (PLDI 2005)
    locator: pp. 281-294, the first form of sketching, for bit-level stream programs in StreamBit
  - paper: doi:10.1145/1168857.1168907
    title: Armando Solar-Lezama, Liviu Tancau, Rastislav Bodík, Sanjit Seshia and Vijay Saraswat, Combinatorial sketching for finite programs, Architectural Support for Programming Languages and Operating Systems (ASPLOS 2006)
    locator: pp. 404-415, the sketch language with integer holes, the reduction of a finite sketch to an exists-forall problem, and the counterexample-guided loop with a SAT solver
  - paper: "Armando Solar-Lezama, Program synthesis by sketching, PhD thesis, University of California, Berkeley, 2008, technical report UCB/EECS-2008-177"
    locator: the Sketch language, generators, the semantics of holes, the encoding into Boolean formulas and CEGIS
  - paper: doi:10.1007/s10009-012-0249-7
    title: Armando Solar-Lezama, Program sketching, International Journal on Software Tools for Technology Transfer 15(5-6), 2013
    locator: pp. 475-495, an overview of the language, of the solver and of its use
  - paper: doi:10.1145/2509578.2509586
    title: Emina Torlak and Rastislav Bodík, Growing solver-aided languages with Rosette, Onward! 2013
    locator: pp. 135-152, holes and synthesis queries inside a host language with symbolic evaluation
  - paper: doi:10.1561/2500000010
    title: Sumit Gulwani, Oleksandr Polozov and Rishabh Singh, Program Synthesis, Foundations and Trends in Programming Languages 4(1-2), 2017
    locator: the parts on constraint-based search and on sketching
  - paper: doi:10.1016/0304-3975(76)90061-X
    title: Larry J. Stockmeyer, The polynomial-time hierarchy, Theoretical Computer Science 3(1), 1976
    locator: pp. 1-22, the levels of the hierarchy and their complete problems
  - paper: doi:10.1016/0304-3975(76)90062-1
    title: Celia Wrathall, Complete sets and the polynomial-time hierarchy, Theoretical Computer Science 3(1), 1976
    locator: pp. 23-33, the completeness of quantified Boolean formulas with k alternations for the k-th level
---

Program sketching is a way to write a program in two parts. The programmer writes a *sketch*: a program with *holes*, written `??`, where the details are unknown. A synthesizer fills the holes so that the program meets its specification, for example the assertions in the code or equality with a slow reference program, for all inputs. The programmer gives the structure, which is hard for a machine to guess. The machine finds the constants, indices and small expressions, which are hard for a person to get right. Solar-Lezama and others built the method into the Sketch language (2005 to 2008). For a sketch with bounded inputs and loops, the question is $\exists c\, \forall x\, \varphi(x, c)$, and Sketch answers it with [counterexample-guided inductive synthesis](/cegis/) and a SAT solver.

## In plain words

Say you know that a trick with "and" and "plus" can clear the lowest set bit of a number, but you forget the exact constant. You write the program with a blank where the constant goes, and you state what the result must be. The tool tries to fill the blank.

It does not try all inputs for every possible constant. It picks a constant that works on a few inputs, then looks for an input where that constant fails. That input joins the list, and the tool picks a new constant. When no failing input is left, the blank is filled.

Holes can also stand for a choice between a few expressions, so you can say "one of these operators goes here" and let the tool decide.

## When it applies

Use it when you know the shape of the solution but not its details. Typical cases are bit tricks, the constants and masks of a fast routine, the index arithmetic of a loop, and the order of a few statements. The specification is a set of assertions, or a simple reference program that the fast one must match.

The method needs a bounded problem. The inputs must have a fixed width, such as 8 or 32 bits, loops must be unrolled to a fixed depth, and recursion must be inlined to a fixed depth. Then the program and its assertions become a finite formula. Without bounds, even a sketch with no holes asks whether a program meets its assertions, and that is undecidable by [Rice's theorem](/rice-theorem/).

It does not fit when the structure itself is unknown. Then use a search over a whole grammar, as in [syntax-guided synthesis](/syntax-guided-synthesis/), or a search from examples.

## The template

**Step 1: the specification.** Write a reference program `spec(x)`, or assertions inside the code. The sketch must give the same result as `spec` on every input, or no assertion may fail.

**Step 2: the sketch.** Write the program with holes. An integer hole `??` stands for a constant of a fixed number of bits. A choice `{| e1 | e2 | e3 |}` stands for one of the listed expressions. A generator is a function whose body has holes, and each call of it gets its own copies of the holes. All holes together form the control vector $c$.

**Step 3: the bounds.** Fix the width of the inputs and of the holes, the number of times each loop is unrolled, and the depth of inlining. An assertion that fails after the last unrolling counts as a failure, so the bound does not hide a bug inside the bound.

**Step 4: the formula.** Run the sketch on a symbolic input $x$ and symbolic holes $c$, as in [symbolic execution](/symbolic-execution/), and translate each operation into a Boolean circuit by [bit-blasting](/bit-blasting/). The result is a formula $\varphi(x, c)$ that is true when the assertions hold on input $x$ with holes $c$.

**Step 5: the search.** Solve $\exists c\, \forall x\, \varphi(x, c)$ by CEGIS. Keep a small set $E$ of inputs. A SAT call finds a $c$ with $\varphi(x, c)$ for all $x \in E$. A second SAT call looks for an $x$ with $\neg \varphi(x, c)$. If there is one, add it to $E$ and repeat. If there is none, $c$ is correct for all bounded inputs. If the first call fails, no completion exists within the bounds. The loop stops because the space of $c$ is finite; the proof is on the [CEGIS](/cegis/) page.

**Step 6: the program.** Put the values of $c$ into the sketch. The result is an ordinary program with no holes. Check it outside the bounds with a verifier or with tests.

**How hard is it.** For a sketch where holes and inputs are bits and $\varphi$ is a polynomial-size circuit, the question "is there a completion?" is complete for $\Sigma_2^P$, the second level of the [polynomial hierarchy](/polynomial-hierarchy/).

*Proof.* It is in $\Sigma_2^P$: the certificate is $c$, of polynomial size, and checking $\forall x\, \varphi(x, c)$ is a co-NP question. It is $\Sigma_2^P$-hard: take any true or false [quantified Boolean formula](/qbf/) $\exists c\, \forall x\, \psi(c, x)$. The sketch "assert $\psi(??, x)$" with input $x$ and one hole bit for each variable of $c$ has a completion exactly when the formula is true. Deciding such formulas is $\Sigma_2^P$-complete (Stockmeyer and Wrathall, 1976). $\square$

So no polynomial algorithm is expected, and CEGIS is a way to split the hard query into many SAT calls that are often easy.

## Classic examples

**Clear the lowest set bit.** On 8-bit words, the specification is `spec(x) = x & (x - 1)`, with arithmetic modulo 256. The sketch is

```
int8 f(int8 x) implements spec { return x & (x + ??); }
```

with an 8-bit hole. Of the 256 values, only $?? = 255$, which is $-1$ modulo 256, gives `spec` on all inputs. Run CEGIS, where the synthesizer returns the least constant that fits the inputs in $E$ and the verifier returns the least input where the constant fails:

| round | candidate | counterexample |
|---|---|---|
| 1 | 0 | 1 |
| 2 | 1 | 2 |
| 3 | 3 | 4 |
| 4 | 7 | 8 |
| 5 to 8 | 15, 31, 63, 127 | 16, 32, 64, 128 |
| 9 | 255 | none |

The constant $2^j - 1$ fits every input whose lowest set bit is below bit $j$, and fails on $2^j$. So the loop needs 8 counterexamples out of 256 inputs, one for each bit, and stops after 9 rounds.

**A choice of operators.** In the sketch `return x OP1 (x OP2 ??);` each of OP1 and OP2 is a choice among the five operators and, or, exclusive or, plus and minus. It has $5 \cdot 5 \cdot 256 = 6400$ completions. Two of them are correct: `x & (x + 255)` and `x & (x - 1)`. With candidates in a fixed order, CEGIS again stops after 9 rounds; its counterexamples are 3, 2, 4, 8, 16, 32, 64 and 128. So 8 inputs out of 256 decide among 6,400 candidates.

**Loops with index holes.** A sketch of an in-place array reversal can leave the loop bound and the index of the swap partner as holes, for example `for i < n / ?? : swap(a[i], a[n - ?? - i])`. With 4-bit holes, $n$ bounded by 8 and the loop unrolled up to 8 times, the divisor 2 and the offset 1 are the only completion that reverses every array, and an index out of range counts as a failed assertion. The bound on $n$ matters: the formula says nothing about longer arrays.

**Bit-level kernels.** The first sketching work (Solar-Lezama and others 2005) targeted bit-stream programs, where a short reference program says what each output bit is, and a fast version works on whole machine words with masks and shifts. The 2006 paper extended this to finite programs in a C-like language.

## Variations

- **Generators.** A generator is a function with holes that the synthesizer expands at each call. A recursive generator describes a whole grammar of expressions up to a depth, so a sketch can contain a small [syntax-guided synthesis](/syntax-guided-synthesis/) problem.
- **Minimization.** Ask for the completion with the least value of a cost written in the sketch, such as the number of operations. The solver repeats the search with a bound on the cost that drops each time.
- **Solver-aided languages.** Rosette (Torlak and Bodík 2013) adds holes and synthesis queries to a host language. It evaluates the program symbolically and sends the formula to an SMT solver, so holes can also range over integers and other theories.
- **Concurrent programs.** The inputs include the choices of the scheduler, so the formula holds for all thread interleavings up to the bound.
- **Hole-free sketches.** With no holes, the second query of CEGIS alone is [bounded model checking](/bounded-model-checking/) of the assertions.

## Pitfalls

- **Bounds are not proofs.** A completion correct for all 8-bit inputs and for loops of up to 8 rounds may fail on 32-bit inputs or on longer loops. Check the result outside the bounds.
- **Holes are tied to the width.** Solve the first example with 4-bit words and the answer is $?? = 15$, which is $-1$ at 4 bits. Copied into 8-bit code it is wrong: on $x = 16$ it gives $16 \mathbin{\&} 31 = 16$, and the right result is 0. Write the constant as $-1$ or solve at the final width.
- **A failed search says little.** If no completion exists, the solver reports only that. The cause can be a wrong structure, a hole that is too narrow, or a bound that is too small. Change one thing at a time.
- **Weak specifications.** Assertions that check only part of the behaviour give programs that pass them and do the wrong thing. A reference program is a stronger specification than a few assertions.
- **Too many holes.** The formula grows with the bit width, the number of holes, and the unrolling depth. A sketch with many wide holes can make each SAT call slow, even if CEGIS needs few rounds.
- **Not the same as satisfiability.** Finding $c$ and $x$ with $\varphi(x, c)$ is one SAT call, but it shows only that the completion works on one input. The question is for all inputs.

## Exercises

1. In the first example, why is $?? = 254$ wrong? *Answer.* On $x = 1$, $x + 254 = 255$ and $1 \mathbin{\&} 255 = 1$, but `spec(1)` $= 0$.
2. Give a sketch with one 8-bit hole for `spec(x) = x & -x`, the lowest set bit, using $\neg x$ (bitwise not) and $+$. *Answer.* `x & (~x + ??)`, with $?? = 1$, since $-x = \neg x + 1$ modulo 256.
3. A sketch has $h$ hole bits and $n$ input bits. Give a bound on the number of CEGIS rounds. *Answer.* Each round removes at least one candidate and adds a new input, so there are at most $\min(2^h, 2^n) + 1$ rounds.
4. Show that a sketch whose assertions hold for no input has no completion, and that a sketch whose holes do not occur in the assertions has a completion exactly when the program is correct for all inputs. *Answer.* In the first case $\forall x\, \varphi(x, c)$ is false for every $c$. In the second case $\varphi$ does not depend on $c$, so $\exists c\, \forall x\, \varphi(x)$ is the same as $\forall x\, \varphi(x)$, which is verification.

## References
