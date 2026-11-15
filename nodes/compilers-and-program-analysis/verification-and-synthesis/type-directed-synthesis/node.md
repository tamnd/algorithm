---
tag: 3WFWA4
kind: algorithm
slug: type-directed-synthesis
name: Type-directed program synthesis
aliases:
- synthesis from refinement types
area: compilers-and-program-analysis/verification-and-synthesis
level: research
summary: Searches for a program top-down by the goal type, using examples or refinement types to prune each partial program early.
model: word-ram
complexity:
  vars: {b: the number of kept E-terms in one bank, d: the bound on nested conditionals, w: the number of examples}
  time: {one bank: O(w b^2), whole search: "O((2b)^d w b^2) worst case"}
  space: {whole search: "O((2b)^d w b) worst case"}
properties: {deterministic: true, recursive: true}
history:
  year: 2015
  people: [Peter-Michael Osera, Steve Zdancewic]
  note: Myth (PLDI 2015) refined examples through the typing rules of a functional language with algebraic data types. Synquid (PLDI 2016) used refinement types as the specification.
prereqs: [bottom-up-enumerative-synthesis, simply-typed-lambda-calculus]
see_also: [hindley-milner-type-system, algorithm-w, curry-howard-correspondence, dependent-types, deductive-program-synthesis, programming-by-example, syntax-guided-synthesis, structural-induction]
sources:
  - paper: doi:10.1145/2737924.2738007
    title: Peter-Michael Osera and Steve Zdancewic, Type-and-example-directed program synthesis, Programming Language Design and Implementation (PLDI 2015)
    locator: pp. 619-630, the refinement of examples into worlds by the typing rules, the split into introduction and elimination terms, the match rule, structural recursion and trace completeness
  - paper: doi:10.1145/2908080.2908093
    title: Nadia Polikarpova, Ivan Kuraj and Armando Solar-Lezama, Program synthesis from polymorphic refinement types, Programming Language Design and Implementation (PLDI 2016)
    locator: pp. 522-538, Synquid, the round-trip type checking of partial programs against refinement types, with liquid type inference
  - paper: doi:10.1145/2737924.2737977
    title: John K. Feser, Swarat Chaudhuri and Isil Dillig, Synthesizing data structure transformations from input-output examples, Programming Language Design and Implementation (PLDI 2015)
    locator: pp. 229-239, hypotheses with holes typed by higher-order combinators, and deduction that rules out a hole from the examples
  - paper: doi:10.1007/978-3-642-39799-8_67
    title: Aws Albarghouthi, Sumit Gulwani and Zachary Kincaid, Recursive program synthesis, Computer Aided Verification (CAV 2013)
    locator: pp. 934-950, recursive calls answered from the examples, and the closure condition on the examples
  - paper: doi:10.1016/0304-3975(79)90006-9
    title: Richard Statman, Intuitionistic propositional logic is polynomial-space complete, Theoretical Computer Science 9(1), 1979
    locator: pp. 67-72, the PSPACE-completeness of provability, and so of type inhabitation in the simply typed lambda calculus
  - paper: doi:10.1561/2500000010
    title: Sumit Gulwani, Oleksandr Polozov and Rishabh Singh, Program Synthesis, Foundations and Trends in Programming Languages 4(1-2), 2017
    locator: the parts on top-down enumeration and on type-directed search
---

Type-directed program synthesis searches for a program from the top down, guided by the type of the goal. At a function type it adds an abstraction and moves the examples inside it. At a data type it either guesses a term built from the variables in scope, or it splits the goal by a case analysis and solves each case. Each step follows a typing rule, so every partial program is well typed, and the examples or a refined type remove a wrong partial program before its holes are filled. Myth (Osera and Zdancewic 2015) uses examples and the types of a functional language with algebraic data types. Synquid (Polikarpova and others 2016) uses refinement types, such as "a list whose length is n", as the whole specification. The code on this page is a small instance on integers in the toy lambda language of the [Algorithm W](/algorithm-w/) page.

## In plain words

Say you want a function from a number to a number, and you know its value at 0, 1, 2, 3 and 4. The type says that the program starts with "take a number x". Inside, the search knows x and the wanted result for each example.

First it tries short formulas in x. If none gives all the results, it splits the examples into "x is 0" and "x is not 0", and solves the two parts on their own. In the second part it may call the function itself on x minus 1. It does not run that call: it looks up the answer in the examples, since the value at x minus 1 is one of them.

The types keep the search small. A number is built only from numbers, and a test from two numbers, so no term of the wrong kind is made.

## The problem

**Input.** A goal type $\tau = \mathrm{int} \rightarrow \cdots \rightarrow \mathrm{int}$ with one to three arguments, and examples $(a, o)$ of argument tuples and outputs.

**Output.** A closed term $p$ of type $\tau$ in the toy language with $p\ a_1 \cdots a_n = o$ for every example, or "none" if no program in the bounded space fits.

**The space.** The program is $\mathbf{fix}\ f\ x \rightarrow \mathbf{fun}\ y \rightarrow \cdots \rightarrow B$. A body $B$ is an E-term, or a conditional $\mathbf{if}\ c\ \mathbf{then}\ B\ \mathbf{else}\ B$. An *E-term* is an argument, 0, 1, a sum, difference or product of E-terms, or a recursive call $f\ (x - 1)\ e_2 \cdots e_n$. A condition is $e_1 < e_2$ or $e_1 = e_2$ for E-terms, or the guard $x < 1$. The guard is the match of a natural number on zero and successor: a call of $f$ is allowed only in its false branch, and the guard appears at most once on each path. The size of an E-term is its number of nodes, where the call $f\ (x - 1)$ counts 2 and each further argument counts its own size. The bounds are $K$ on the size of E-terms and conditions, and $D$ on the nesting of conditionals.

**Trace completeness.** The search reads the value of a recursive call from the examples. So the examples should hold every call that the wanted program makes on an example input. For a function of one argument this means: if $n$ is an example input, so are $n - 1, \ldots, 0$.

## The algorithm

```pseudo id=main
SYNTHESIZE(τ, examples)
L1  T ← the examples as a table from argument tuples to outputs
L2  for k = 1, 2, …, K do
L3      for d = 0, 1, …, D do
L4          B ← REFINE(the examples as worlds, k, d, none)
L5          if B ≠ none then return fix f x → fun y → … → B     ▷ the introduction for the arrow type τ
L6  return none

REFINE(W, k, d, m)                   ▷ m is none, base or step
L7  look bottom-up for an int E-term of size ≤ k that gives the wanted output in every world of W   ▷ calls only if m = step, read from T
L8  if one is found then return it
L9  if d = 0 then return none
L10 if m = none then split W by x < 1 into W0 and W1, with W1 non-empty, and solve REFINE(W0, k, d - 1, base) and REFINE(W1, k, d - 1, step)
L11     if both are found then return if x < 1 then B0 else B1
L12 for each kept bool E-term c of size ≤ k that splits W into non-empty W⊤ and W⊥ do
L13     solve REFINE(W⊤, k, d - 1, m) and REFINE(W⊥, k, d - 1, m)
L14     if both are found then return if c then B⊤ else B⊥
L15 return none
```

**Introduction by the type (line L5).** The goal type is an arrow, so the program must be an abstraction. With recursion it is $\mathbf{fix}\ f\ x$, and further arguments add $\mathbf{fun}$. Each example $(a, o)$ becomes a *world*: the values of $x, y, \ldots$ and the wanted output of the body. This is how Myth pushes examples through the introduction rule of the function type.

**Guessing E-terms (lines L7 and L8).** E-terms are elimination forms: they use the variables in scope, the operators and $f$. The search builds them bottom-up by size, as in [bottom-up enumerative synthesis](/bottom-up-enumerative-synthesis/), with their vectors of values over the worlds, and keeps one term for each vector. The vector of a call $f\ (x - 1)\ e_2$ in a world is the output of the example $(x - 1, e_2)$ in $T$, or "undefined" if there is no such example. An undefined entry never matches.

**Refinement by cases (lines L10 to L14).** If no E-term fits, the body becomes a conditional. The guard $x < 1$ splits the worlds into base and step cases, and only the step branch may call $f$. A guessed condition splits the worlds by its vector. Each part becomes a smaller problem with fewer worlds, so it is easier to fit by an E-term. Only one condition is kept for each distinct split.

**Iterative deepening (lines L2 and L3).** The outer loops raise the size bound and the nesting bound, so a program with small parts is found before one with large parts.

## Example

The examples are $0 \mapsto 0$, $1 \mapsto 1$, $2 \mapsto 3$, $3 \mapsto 6$ and $4 \mapsto 10$, of type int $\rightarrow$ int. They are trace complete.

- **$k \le 2$.** The kept E-terms are $x$, 0 and 1, with the vectors $(0, 1, 2, 3, 4)$, $(0, 0, 0, 0, 0)$ and $(1, 1, 1, 1, 1)$. None fits, and there are no conditions yet.
- **$k = 3$.** There are 11 kept E-terms and 6 conditions, and none of the E-terms gives $(0, 1, 3, 6, 10)$. The guard splits the worlds into $\{0\}$ and $\{1, 2, 3, 4\}$. The base branch is fitted by $x$. In the step branch $f\ (x - 1)$ has the vector $(0, 1, 3, 6)$, read from the examples, but no term of size 3 gives $(1, 3, 6, 10)$. The guessed conditions do not help either.
- **$k = 4$, $d = 1$.** In the step branch, $x + f\ (x - 1)$ has size 4 and the vector $(1, 3, 6, 10)$.

The result is

$$ \mathbf{fix}\ f\ x \rightarrow \mathbf{if}\ x < 1\ \mathbf{then}\ x\ \mathbf{else}\ x + f\ (x - 1), $$

after 51 calls of REFINE. Type inference gives int $\rightarrow$ int, and the interpreter gives 15 on 5 and 21 on 6. The code finds, in the same way, $x \times f\ (x - 1)$ with base 1 from the values 1, 1, 2, 6, 24 of the factorial, $f\ (x - 1) + x \times x$ from 0, 1, 5, 14, 30, and for two arguments $\mathbf{if}\ x < y\ \mathbf{then}\ y\ \mathbf{else}\ x$ from five examples of the maximum.

**What the examples do not decide.** The Fibonacci numbers 0, 1, 1, 2, 3, 5 on 0 to 5 need a call on $x - 2$, which is not in the space. The search still meets all six examples. Below the guard it finds the condition $1 < f\ (x - 1)$, with $f\ (x - 1) - (1 - f\ (x - 1))$ in its true branch and $x - f\ (x - 1)$ in its false branch. This program gives 9 on 6 and 17 on 7, where Fibonacci gives 8 and 13. The test file checks this case.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Every term is built at a known type from parts of known types, so the result has the goal type, and Hindley-Milner inference confirms it; when an argument is not used, the inferred type is more general and has the goal type as an instance. The vectors give the exact value of each term when calls are read from the table, so a returned body meets every world. Every call has a first argument that is one smaller and lies in the table, so by induction on the first argument the real run of the program gives the same values as the table. The calls happen only when $x \ge 1$, so the program stops on every integer input. Within the bounds the search is complete for trace complete examples: an E-term or a condition that works has a kept twin with the same vector, so the same split and the same leaves are found.

## Complexity

Let $b$ be the number of kept E-terms in one bank, $w$ the number of examples, and $d$ the bound on nested conditionals. A bank combines $O(b^2)$ pairs of kept terms, at $O(w)$ per vector, so it takes $O(w b^2)$ time and $O(w b)$ space. A call of REFINE tries the guard and up to $b$ conditions, each with two recursive calls, so the search tree has $O((2b)^d)$ nodes. Each node builds a bank for its set of worlds, and banks are shared between equal sets. The worst case is $O((2b)^d w b^2)$ time for one pair $(k, d)$. The number $b$ is bounded by the number of distinct vectors and grows exponentially with $k$.

The general problem is hard even with no examples: finding any closed term of a given simple type is the same as finding a proof in intuitionistic propositional logic, by the [Curry-Howard correspondence](/curry-howard-correspondence/), and that is PSPACE-complete (Statman 1979).

## Properties

- **Well typed by construction.** No ill-typed term is built, so the search never wastes time on one.
- **Sound for the examples.** The result meets every example, with no assumption on the examples.
- **Total.** The result stops on every input, because each call is structural.
- **Complete within the bounds** for trace complete examples, and it returns a body with the least size bound $k$.
- **Not a smallest program.** Iterative deepening bounds the size of each part, not of the whole program.

## Variants and improvements

- **Algebraic data types.** Myth works on lists and trees. The match rule splits the worlds by the constructor of a variable, and each branch binds the fields, such as the head and the tail of a list, which are then allowed as arguments of recursive calls.
- **Higher-order examples.** Myth allows examples of functions as partial functions, so a goal like "map" can be given by examples of its argument and its result.
- **Refinement types.** Synquid takes a type such as "a list of the same length, sorted" as the specification. It checks each partial program against the type with liquid type inference, and moves the conditions from the goal into the types of the holes, so a wrong partial program fails early with no examples.
- **Combinators with deduction.** λ² (Feser and others 2015) fills hypotheses such as "map of a hole" or "fold of a hole", and deduces from the examples the examples of the hole, or that no term can fill it.
- **Relaxed trace completeness.** Escher (Albarghouthi and others 2013) also answers recursive calls from the examples, and asks the user for the missing ones.

## When to use it

Use it for small functional programs with recursion over a data type, when the user can give a few examples that include the recursive cases, or a precise refinement type. The types cut the search at every step, which matters most for programs with several data types and higher-order functions. For flat expressions over one type, plain [bottom-up enumerative synthesis](/bottom-up-enumerative-synthesis/) is simpler. For a specification as a logical formula with a known structure, use [deductive program synthesis](/deductive-program-synthesis/) or a solver.

## Pitfalls

- **Missing examples for recursive calls.** If the example for $x - 1$ is missing, the call is undefined in that world, and the intended recursive program cannot be found. Give examples for all smaller inputs, or for all inputs that the intended program calls.
- **Overfitting with conditionals.** With enough nested conditionals, the search fits any finite set of examples, as the Fibonacci case shows. Keep the nesting bound small and prefer programs with few cases.
- **Unused arguments.** A result that ignores an argument has a more general principal type. Check it against the goal type by unification, not by equality of types.
- **Negative inputs.** A match on zero and successor is only meaningful on natural numbers. The guard $x < 1$ keeps the result total on negative inputs, but the examples say nothing about them.
- **Growth with the size bound.** Each step of $k$ can multiply the bank, and each level of $d$ multiplies the number of splits. Small examples with small numbers keep vectors short and banks small.

## Implementations

## History

Type inhabitation, the search for a term of a given type, is old: Statman (1979) showed that it is PSPACE-complete for simple types. Albarghouthi, Gulwani and Kincaid (2013) answered recursive calls from the examples in Escher. Osera and Zdancewic (2015) combined types and examples in Myth: examples move through the typing rules, elimination terms are guessed, and introduction forms and matches refine the goal. In the same year Feser, Chaudhuri and Dillig built λ² on typed higher-order combinators. Polikarpova, Kuraj and Solar-Lezama (2016) replaced the examples by refinement types in Synquid, which checks partial programs against the type as they grow.

## References
