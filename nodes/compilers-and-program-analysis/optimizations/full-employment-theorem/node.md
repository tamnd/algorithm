---
tag: QQ9T6J
kind: theorem
slug: full-employment-theorem
name: Full employment theorem for compiler writers
aliases:
- no perfect optimizer theorem
area: compilers-and-program-analysis/optimizations
level: core
summary: No algorithm maps every program to a smallest equivalent program, because such an algorithm would decide the halting problem. So every optimizer can be improved.
prereqs: [halting-problem, three-address-code]
see_also: [rice-theorem, halting-problem, superoptimization, dead-code-elimination, constant-folding, dataflow-analysis, register-machine, verified-compilation]
sources:
  - book: isbn:9780521820608
    title: Andrew W. Appel with Jens Palsberg, Modern Compiler Implementation in Java, second edition, Cambridge University Press, 2002
    locator: Chapter 17 (Dataflow analysis), the opening pages before Section 17.1 (a fully optimizing compiler would decide the halting problem, because it maps each program that never halts to the one-line infinite loop)
  - paper: doi:10.1090/S0002-9947-1953-0053041-6
    title: H. Gordon Rice, Classes of recursively enumerable sets and their decision problems, Transactions of the American Mathematical Society 74(2), 1953, 358-366
    locator: the main theorem (no nontrivial class of recursively enumerable sets is recursive), which gives the undecidability of every nontrivial property of the function a program computes
  - paper: doi:10.1112/plms/s2-42.1.230
    title: Alan M. Turing, On computable numbers, with an application to the Entscheidungsproblem, Proceedings of the London Mathematical Society (2) 42, 1936, 230-265
    locator: Section 8 (no machine decides whether a given machine ever prints a given symbol, the root of the halting problem)
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition, Cengage Learning, 2013
    locator: Section 5.1 (Theorem 5.1, the halting problem is undecidable, by reduction from the acceptance problem) and the exercise on Rice's theorem at the end of Chapter 5
---

The full employment theorem for compiler writers says that no algorithm transforms every program into a smallest program with the same behavior. Such an algorithm would map each program that never halts on any input to the one-instruction infinite loop, and so it would decide the [halting problem](/halting-problem/). It follows that every optimizer misses some improvement, and that a better optimizer can always be written. The name is a joke about job security; the content is an undecidability result, close to [Rice's theorem](/rice-theorem/).

## Statement

We state the theorem for the toy IR of this area: [three-address code](/three-address-code/) in basic blocks, with unbounded integers. The size $|P|$ of a program $P$ is its number of instructions plus its number of terminators. We consider only programs that never read an undefined name.

The *outcome* of $P$ on an argument tuple $\vec{a}$ is `ret v` if $P$ returns $v$, `trap` if it divides by zero or shifts out of range, and *no end* if it runs forever. Two programs $P$ and $Q$ are *equivalent*, $P \equiv Q$, if they have the same number of parameters and the same outcome on every argument tuple. A program $Q$ is a *smallest equivalent* of $P$ if $Q \equiv P$ and $|Q| \le |R|$ for every $R \equiv P$.

**Theorem.** There is no computable function $\mathrm{Opt}$ from programs to programs such that $\mathrm{Opt}(P)$ is a smallest equivalent of $P$ for every program $P$.

The proof uses only two facts about the toy IR: it can simulate a Turing machine, and an algorithm can recognize the smallest programs that never end. So the theorem holds for every language and size measure with these two properties.

What this page needs from the other pages: from [halting-problem](/halting-problem/), that no algorithm decides, for a Turing machine $M$ and an input $w$, whether $M$ halts on $w$; from [rice-theorem](/rice-theorem/), that no algorithm decides a nontrivial property of the partial function that a program computes.

## In plain words

A perfect optimizer would give back the shortest program that does the same thing as its input. Feed it a program that never stops, whatever its input is. The shortest program that never stops is a single jump to itself. So the perfect optimizer would have to give back that one line. Now look at its answer: if the answer is the one-line loop, the input program never stops; otherwise it stops on some input. That would tell us whether any program stops, and that question has no algorithm. So the perfect optimizer cannot exist. Every real optimizer finds some improvements and misses others, and someone can always write a better one.

## Proof

**Step 1: the programs of size 1.** Each block ends with a terminator, so a program of size 1 has one block and no instructions. Its terminator is `ret a`, `jump L` or `br a L L`, where `L` is its only label. A program `L: ret a` returns on every input. A program `L: jump L` or `L: br a L L` runs forever on every input. So a program of size 1 either ends on every input or never ends on any input, and a look at its terminator tells which.

**Step 2: a perfect optimizer decides "never ends".** Let $D$ be the set of programs that end on no input. Take a program $P$ with $k$ parameters. Let $\Omega_k$ be the program `L: jump L` with the same $k$ parameters, so $|\Omega_k| = 1$.

- If $P \in D$, then $\Omega_k \equiv P$. So a smallest equivalent of $P$ has size at most 1. Every program has size at least 1, so $|\mathrm{Opt}(P)| = 1$. By Step 1 and $\mathrm{Opt}(P) \equiv P$, the terminator of $\mathrm{Opt}(P)$ is `jump` or `br`.
- If $P \notin D$, then $P$ ends on some input, so $\mathrm{Opt}(P)$ ends on that input. By Step 1, $\mathrm{Opt}(P)$ is not a size-1 program with a `jump` or `br` terminator.

So $P \in D$ if and only if $\mathrm{Opt}(P)$ has size 1 and its terminator is not `ret`. If $\mathrm{Opt}$ is computable, this test decides $D$.

**Step 3: $D$ is undecidable.** Take a Turing machine $M$ with states $0$ to $q_{max}$, tape alphabet $\{0, \dots, b-1\}$ with blank $0$, and an input word $w$. We build a toy IR program $P_{M,w}$ that ignores its parameters and simulates $M$ on $w$. It keeps four integers: the state `q`, the symbol under the head `s`, the cells left of the head as a base-$b$ number `lft` with the nearest cell as the lowest digit, and the cells to the right as `rgt` in the same way. A blank part of the tape is the number 0. The entry block sets `q = 0` and sets `s` and `rgt` from $w$. A chain of blocks tests `q == i` and `s == j` for each pair $(i, j)$ of the finite transition table. The block for a transition to $(i', j', \text{right})$ runs

```
lft = lft * b
lft = lft + j'
s = rgt % b
rgt = rgt / b
q = i'
jump dispatch
```

with the constants $b$, $j'$ and $i'$ written in. A move to the left is the same with `lft` and `rgt` swapped. A halting state jumps to a block `ret 0`. All values stay nonnegative and every divisor is the constant $b \ge 2$, so the program never traps. $P_{M,w}$ is computable from $M$ and $w$, and it ends on some input if and only if it ends on every input, if and only if $M$ halts on $w$. So $P_{M,w} \in D$ if and only if $M$ does not halt on $w$. If $D$ were decidable, the halting problem would be decidable, which is false (Turing 1936; Sipser, Theorem 5.1).

**Conclusion.** Steps 2 and 3 show that a computable $\mathrm{Opt}$ would decide $D$, and $D$ is undecidable. So $\mathrm{Opt}$ is not computable. $\blacksquare$

**A shorter route through Rice's theorem.** The class $D$ depends only on the partial function that a program computes: $P \in D$ if and only if that function is undefined everywhere. Some programs are in $D$ and some are not. By Rice's theorem, $D$ is undecidable. Step 3 is a direct proof of this one case.

**Example.** The program below, with parameter `n`, runs the Collatz map until `n` drops below 2, then returns 0.

```
entry:
  jump test
test:
  t = n < 2
  br t done step
step:
  r = n % 2
  br r odd even
odd:
  m = n * 3
  n = m + 1
  jump test
even:
  n = n / 2
  jump test
done:
  ret 0
```

For `n = 27` it applies the map 111 times and executes 711 instructions and terminators before it returns 0. For every `n` below 2 it returns 0 at once. It returns 0 for all `n` up to 2000. It is equivalent to the one-block program `entry: ret 0` if and only if the Collatz conjecture is true. So a perfect size optimizer applied to these 15 lines would settle an open problem in number theory.

## Consequences

- **There is always a better optimizer.** Let $O$ be any computable optimizer that keeps behavior. By the theorem there is a program $P$ such that $O(P)$ is not a smallest equivalent, so some $Q \equiv P$ has $|Q| < |O(P)|$. Define $O'(X) = Q$ if $X = P$ and $O'(X) = O(X)$ otherwise. $O'$ is computable, keeps behavior, is never worse than $O$ and is strictly better on $P$. The same step applies to $O'$, and so on without end. This is the "full employment" of the name.
- **Every exact program fact is undecidable.** The same reduction shows that no algorithm decides whether an instruction ever executes, whether a variable has the same value on every run, or whether two expressions always have equal values: put the instruction or the expression after the code of $P_{M,w}$. So real optimizations act on facts that a conservative analysis can prove, such as the facts of [dataflow analysis](/dataflow-analysis/), and they find some opportunities, not all. [Dead code elimination](/dead-code-elimination/), [constant folding](/constant-folding/) and [common subexpression elimination](/common-subexpression-elimination/) all follow this pattern.
- **Correctness stays decidable for one transform.** The theorem does not stop a compiler from proving that its own transform keeps behavior. [Verified compilation](/verified-compilation/) proves a fixed set of rewrites correct once, for all programs.

## Tightness

- **Unbounded state is needed.** Step 3 needs integers without a bound. If every value is a $w$-bit word, the number of variables is fixed and there is no memory allocation, then a program is a finite-state system. On a given input, a run either ends or repeats a state, and a simulation finds which. There are finitely many inputs and, up to the renaming of names and labels, finitely many programs of each size. So a search in order of size finds a smallest equivalent program. This search is far too slow for real code, but it is an algorithm. The theorem is about computability, not about cost.
- **Loop-free code is decidable.** For loop-free code on $w$-bit words, every run ends, so equivalence is decidable by trying all inputs, and a smallest equivalent program can be found by enumeration. This is the idea of [superoptimization](/superoptimization/), which is practical only for a few instructions.
- **The smallest form of $D$ is the key.** Step 2 only uses that the smallest members of $D$ form a decidable set. The proof stays the same for any size measure with this property.
## History

Turing showed in 1936 that no machine decides whether a given machine ever prints a given symbol, the origin of the halting problem. Rice proved in 1953 that every nontrivial property of the function computed by a program is undecidable. Appel uses the argument of this page at the start of the chapter on dataflow analysis in his compiler textbooks: a fully optimizing compiler would decide the halting problem, because it would turn every program that never halts into the one-line infinite loop. The name "full employment theorem" is a joke used in teaching; this page does not claim who used it first.

## References
