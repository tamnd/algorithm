---
tag: WV9WKJ
kind: theorem
slug: s-m-n-theorem
name: s-m-n theorem
aliases:
- Kleene s-m-n theorem
- parameter theorem
area: complexity/computability
level: advanced
summary: "A total computable injective function s maps a program e and a value x to a program for the function y to phi_e(x, y). Fixing some inputs of a program is a computable operation on programs."
prereqs: [partial-recursive-function, godel-numbering]
see_also: [kleene-recursion-theorem, godel-numbering, universal-turing-machine, halting-problem, rice-theorem, many-one-reducibility, partial-evaluation, futamura-projections]
sources:
  - paper: doi:10.2307/2267778
    title: "Stephen C. Kleene, On notation for ordinal numbers, Journal of Symbolic Logic 3(4) (1938)"
    locator: pp. 150 to 155
  - paper: doi:10.1007/BF01565439
    title: "Stephen C. Kleene, General recursive functions of natural numbers, Mathematische Annalen 112 (1936)"
    locator: pp. 727 to 742
  - paper: doi:10.2307/2964292
    title: "Hartley Rogers Jr., Gödel numberings of partial recursive functions, Journal of Symbolic Logic 23(3) (1958)"
    locator: "pp. 331 to 341 (numberings with a universal function and the s-m-n property)"
  - paper: doi:10.2307/2964290
    title: "Richard M. Friedberg, Three theorems on recursive enumeration, Journal of Symbolic Logic 23(3) (1958)"
    locator: "pp. 309 to 316 (a numbering of the partial recursive functions without repetition)"
  - book: isbn:9780262680523
    title: "Hartley Rogers Jr., Theory of Recursive Functions and Effective Computability, MIT Press (reprint of the McGraw-Hill edition of 1967)"
    locator: Chapter 1
---

The s-m-n theorem says that fixing some of the inputs of a program is itself a computable operation on programs. Given the index $e$ of a program with $m + n$ inputs and values for the first $m$ inputs, a total computable function $s^m_n$ returns the index of a program with $n$ inputs that does the same as $e$ with those values filled in. The function can be chosen primitive recursive and injective. In programming terms, $s^m_n$ is currying done on source code, and it is the simplest case of partial evaluation. The theorem is a basic tool of recursion theory: it turns constructions on functions into total computable maps on indices, which is what a [many-one reduction](/many-one-reducibility/) between sets of indices needs, and it is the main step in the proof of [Kleene's recursion theorem](/kleene-recursion-theorem/). Kleene introduced it, with the notation $S^m_n$, in his work of the 1930s.

## Statement

Fix the standard numbering of Turing machines of the [Gödel numbering](/godel-numbering/) page, where $\varphi^{(k)}_e$ is the partial function with $k$ arguments computed by the machine with index $e$. The encoding is fixed and computable. Write $\alpha \simeq \beta$ if both sides are undefined, or both are defined and equal.

**Theorem (s-m-n).** For all $m, n \ge 1$ there is a total computable injective function $s^m_n : \mathbb{N}^{m+1} \to \mathbb{N}$ such that, for all $e$, $\vec{x} = (x_1, \ldots, x_m)$ and $\vec{y} = (y_1, \ldots, y_n)$,
$$\varphi^{(n)}_{s^m_n(e, \vec{x})}(\vec{y}) \simeq \varphi^{(m+n)}_e(\vec{x}, \vec{y}).$$
Moreover $s^m_n$ can be taken primitive recursive, and for Turing machines it can be computed in time polynomial in the length of its input.

The case used most often is $m = n = 1$: there is a total computable injective $s$ with $\varphi_{s(e, x)}(y) \simeq \varphi_e(x, y)$.

**Parameter form.** If $\psi(\vec{x}, \vec{y})$ is any partial computable function, there is a total computable injective $f$ with $\varphi_{f(\vec{x})}(\vec{y}) \simeq \psi(\vec{x}, \vec{y})$. Take an index $e$ of $\psi$ and $f(\vec{x}) = s^m_n(e, \vec{x})$.

## In plain words

You have a program that takes two inputs, and you want a program that takes one input and always uses the number 7 as the first one. You can write it by hand: put "x = 7" at the top and keep the rest. The theorem says that this editing step can be done by a program, for every program and every value, and that it never fails.

So any recipe of the form "for each value of the parameter, build a program that does something with that value" gives a computable list of programs. Most proofs that a question about programs is undecidable use this step.

## Proof

Take $m = n = 1$; the general case is the same with more inputs. Let the machine $M_e$ with index $e$ compute $\varphi^{(2)}_e$, reading its input as $\langle x, y \rangle$ in a fixed computable pair format on the tape.

*The new machine.* For given $e$ and $x$, let $N_{e,x}$ be the machine that on input $y$:

1. moves to the left end of the input and writes the code of $x$ followed by the separator of the pair format, shifting $y$ to the right;
2. returns the head to the left end and enters the start state of a copy of $M_e$;
3. from then on runs that copy of $M_e$.

On input $y$ the copy of $M_e$ starts on the tape $\langle x, y \rangle$, so $N_{e,x}$ halts on $y$ if and only if $M_e$ halts on $\langle x, y \rangle$, with the same output. Hence $\varphi_{\mathrm{code}(N_{e,x})}(y) \simeq \varphi_e(x, y)$.

*The map is total and computable.* Let $s(e, x)$ be the index of $N_{e,x}$. The rules of $N_{e,x}$ are a block of $O(|x|)$ states that writes the bits of $x$ and shifts the input, which depends only on $x$, a fixed block that returns the head, and the rules of $M_e$ with every state number raised by the number of states in the first two blocks. Each part is produced from the binary forms of $e$ and $x$ by loops whose bounds are their lengths, with no search, so $s$ is primitive recursive and runs in time polynomial in $|e| + |x|$. If $e$ is not the code of a machine, the numbering maps it to a fixed machine, and $s$ uses that machine in step 3.

*The map is injective.* The writer block has a fixed form from which $x$ can be read back, and the rules after the first two blocks give back $M_e$, and so its code $e$. So $s(e, x) = s(e', x')$ implies $e = e'$ and $x = x'$. For an $e$ that is not a valid code, add $e$ in unary as a block of unreachable states at the end; this keeps $s$ injective on all of $\mathbb{N}^2$.

*More inputs.* For $s^m_n$, step 1 writes the codes of $x_1, \ldots, x_m$ in front of the input, and the same argument applies. $\blacksquare$

**Worked example in a programming language.** Use Python source text as the program index, with $\varphi_e(x, y)$ the result of the function `f` defined by the text $e$. Let $e$ be

```
def f(x, y):
    return x * y + 1
```

The map $s(e, 7)$ puts the text of $e$ inside a new function `g` and adds a one-argument `f` that calls `g(7, y)`:

```
def g(x, y):
    def f(x, y):
        return x * y + 1
    return f(x, y)
def f(y):
    return g(7, y)
```

Running $e$ on $(7, 5)$ gives $36$, and running $s(e, 7)$ on $5$ gives $36$. The map only copies text and prints the decimal form of $x$, so it is total and fast. It is injective because the text of $e$ and the number $x$ can be read back from the output. The output for $x = 7$ has 103 characters and the output for $x = 70$ has 104.

## Consequences

**Reductions between index sets.** A many-one reduction from one set of indices to another is usually built as $x \mapsto s(e, x)$ for a fixed $e$. For example, the map from a pair $\langle M, w \rangle$ to an index of the machine that ignores its input and runs $M$ on $w$ reduces HALT to the diagonal set $K = \{ e : \varphi_e(e)\!\downarrow \}$ by a many-one reduction (see the [halting problem](/halting-problem/) page). The same step gives the index-set form of [Rice's theorem](/rice-theorem/), and the reductions that place $\mathrm{TOT} = \{ e : \varphi_e \text{ total} \}$ and similar sets in the [arithmetical hierarchy](/arithmetical-hierarchy/). Because $s$ is injective, these reductions are one-one reductions, which is what Myhill's isomorphism theorem needs.

**Computable operations on programs.** For every way of combining functions that is itself computable, the s-m-n theorem gives a total computable map on indices. For example, there is a total computable $c$ with $\varphi_{c(a, b)} = \varphi_a \circ \varphi_b$: apply the parameter form to $\psi(a, b, y) = \varphi_a(\varphi_b(y))$, which is partial computable by the [universal Turing machine](/universal-turing-machine/).

**The recursion theorem.** The proof of [Kleene's recursion theorem](/kleene-recursion-theorem/) applies $s$ to a program that receives its own index as the parameter. The fixed point it gives is an index of the form $s(e, e)$.

**Infinitely many indices.** The padding lemma follows: every partial computable function has infinitely many indices, and a total computable injective $p$ lists them, for example $p(e, k) = s(e', \langle e, k \rangle)$, where $e'$ is an index of the function $\psi(\langle a, k \rangle, y) = \varphi_a(y)$. Then $\varphi_{p(e, k)} = \varphi_e$ for every $k$, and the values $p(e, k)$ are all different because $s$ is injective.

**Acceptable numberings.** Rogers (1958) studied the numberings of the partial computable functions that have a partial computable universal function and the s-m-n property. These are called *acceptable*, and the theorems of recursion theory that are stated in terms of indices hold for every acceptable numbering. Any two acceptable numberings are related by a computable permutation of the indices, so the choice of numbering does not matter.

**Partial evaluation.** In programming, [partial evaluation](/partial-evaluation/) is $s^m_n$ with a goal: the output program should run faster than the input program on the remaining inputs, not only compute the same function. The [Futamura projections](/futamura-projections/) apply it to an interpreter and a source program to obtain a compiled program, a compiler, and a compiler generator.

## Tightness

**The numbering matters.** The theorem is a property of the numbering, not of the class of functions. Friedberg (1958) built a computable numbering of all partial computable functions in which each function has exactly one index. The s-m-n theorem fails for it: in a numbering with s-m-n and a universal function, the padding lemma above gives every function infinitely many indices.

**Total and injective, not more.** The function $s$ is total even when $\varphi_e(x, \cdot)$ is undefined everywhere. It returns a program, not a value, so it never needs to run $e$. What it cannot do is return a canonical index: there is no computable $s$ with $s(e, x) = s(e', x')$ exactly when $\varphi_e(x, \cdot) = \varphi_{e'}(x', \cdot)$, since that would decide the equality of computable functions, which is undecidable by Rice's theorem.

**Time.** For the standard Turing machine numbering $s$ runs in polynomial time, so the many-one reductions built from it are polynomial-time reductions. For an arbitrary acceptable numbering, $s$ is total computable, but there is no general bound on its running time.

## History

Kleene introduced the theorem in his work on recursive functions in the 1930s and used it in his 1938 paper on notations for ordinals, where he proved the recursion theorem. The name comes from his notation $S^m_n$ for the function. Rogers (1958) took the universal function and the s-m-n property as the axioms of an acceptable numbering, and his textbook of 1967 presents recursion theory on this basis.

## References
