---
tag: A3F268
kind: theorem
slug: kleene-recursion-theorem
name: Kleene's recursion theorem
aliases:
- recursion theorem
- fixed-point theorem for computability
area: complexity/computability
level: advanced
summary: "For every total computable f on program indices there is an n with phi_n = phi_f(n). So a program can use its own code, and self-printing programs (quines) exist."
prereqs: [s-m-n-theorem]
see_also: [s-m-n-theorem, godel-numbering, rice-theorem, halting-problem, diagonalization-argument, lambda-calculus, godel-incompleteness-theorem, kolmogorov-complexity]
sources:
  - paper: doi:10.2307/2267778
    title: "Stephen C. Kleene, On notation for ordinal numbers, Journal of Symbolic Logic 3(4) (1938)"
    locator: "pp. 150 to 155 (the recursion theorem and its use for notations of ordinals)"
  - book: isbn:9780262680523
    title: "Hartley Rogers Jr., Theory of Recursive Functions and Effective Computability, MIT Press (reprint of the McGraw-Hill edition of 1967)"
    locator: "Chapter 11, Section 11.2 (the fixed-point form of the recursion theorem)"
  - book: isbn:9781133187790
    title: "Michael Sipser, Introduction to the Theory of Computation, third edition"
    locator: "Chapter 6, Section 6.1, The Recursion Theorem"
---

Kleene's recursion theorem says that every total computable transformation of programs has a fixed point in behavior: if $f$ maps program indices to program indices, there is an $n$ such that the programs $n$ and $f(n)$ compute the same function. An equivalent form says that a program may be written as if it had its own code available as an input. Self-printing programs, called quines, are the simplest case. The theorem gives short proofs of [Rice's theorem](/rice-theorem/) and of the undecidability of the [halting problem](/halting-problem/), and it is the computability form of the self-reference in [Gödel's incompleteness theorem](/godel-incompleteness-theorem/). Kleene proved it in 1938 using the [s-m-n theorem](/s-m-n-theorem/). It is sometimes called the second recursion theorem, to separate it from the first recursion theorem, which concerns least fixed points of operators on partial functions.

## Statement

Fix an acceptable numbering $\varphi_0, \varphi_1, \ldots$ of the partial computable functions, for example the Turing machine numbering of the [Gödel numbering](/godel-numbering/) page, where the encoding is fixed and computable. Write $\alpha \simeq \beta$ if both sides are undefined or both are defined and equal.

**Theorem (fixed-point form).** For every total computable function $f : \mathbb{N} \to \mathbb{N}$ there is an $n$ with
$$\varphi_n = \varphi_{f(n)}.$$

**Theorem (Kleene's form).** For every partial computable function $\psi(e, x)$ there is an $e$ with
$$\varphi_e(x) \simeq \psi(e, x) \quad \text{for all } x.$$

**Uniformity.** In both forms the fixed point can be computed from an index of $f$ or $\psi$, by a total computable injective function. A form with parameters also holds: for a total computable $f(e, y)$ there is a total computable injective $n(y)$ with $\varphi_{n(y)} = \varphi_{f(n(y), y)}$ for every $y$.

The fixed point is a fixed point of behavior, $\varphi_n = \varphi_{f(n)}$, not of numbers. For $f(e) = e + 1$ there is no $n$ with $n = f(n)$, but there is an $n$ such that the programs $n$ and $n + 1$ compute the same function.

## In plain words

Imagine any tool that edits programs: it might add a line, swap two commands, or replace a program with a fixed one. The theorem says that some program is not changed in what it does by the tool. The text can change, but the edited program and the original give the same answers on every input.

The second form says the same thing from the other side. When you write a program, you may pretend that it can read its own source code. Some real program does exactly what you described. A program that prints its own text is the shortest example, and it exists in every general programming language.

## Proof

The proof uses the [s-m-n theorem](/s-m-n-theorem/) twice and the [universal function](/universal-turing-machine/) once.

*The diagonal map.* The function $(u, x) \mapsto \varphi_{\varphi_u(u)}(x)$ is partial computable: run $\varphi_u$ on $u$, and if it halts with output $v$, run $\varphi_v$ on $x$. By s-m-n there is a total computable injective $d$ with
$$\varphi_{d(u)}(x) \simeq \varphi_{\varphi_u(u)}(x).$$
So $\varphi_{d(u)} = \varphi_{\varphi_u(u)}$ if $\varphi_u(u)$ is defined, and $\varphi_{d(u)}$ is the everywhere undefined function otherwise. The map $d$ is total even when $\varphi_u(u)$ is undefined, since it only builds a program.

*The fixed point.* Let $f$ be total computable. Then $f \circ d$ is total computable, so $f \circ d = \varphi_v$ for some $v$. Since $\varphi_v$ is total, $\varphi_v(v)$ is defined, and
$$\varphi_{d(v)} = \varphi_{\varphi_v(v)} = \varphi_{f(d(v))}.$$
So $n = d(v)$ is a fixed point. The index $v$ is obtained from an index of $f$ by a third use of s-m-n, so $n$ is a computable function of the index of $f$.

*Kleene's form.* Let $\psi(e, x)$ be partial computable, with index $i$. By s-m-n, $f(e) = s(i, e)$ is total computable with $\varphi_{f(e)}(x) \simeq \psi(e, x)$. A fixed point $e$ of $f$ gives $\varphi_e(x) \simeq \varphi_{f(e)}(x) \simeq \psi(e, x)$. $\blacksquare$

The proof is a [diagonal argument](/diagonalization-argument/) that does not reach a contradiction. In the proof that $K$ is undecidable, the diagonal function is changed at every point and so cannot be in the list. Here the change $f$ is applied to the diagonal program $d(u)$, and $f \circ d$ is in the list, at index $v$, so its diagonal entry $d(v)$ is a fixed point.

**Worked example: a quine.** Apply Kleene's form to $\psi(e, x) = e$, the function that outputs its first argument. The theorem gives a program $e$ that outputs $e$ on every input, a program that prints its own text. In Python the construction is the same as in the proof: a template with a hole, and the template applied to its own text. The program

```
s = 's = %r\nprint(s %% s)'
print(s % s)
```

has 40 characters, and its output is exactly its own text. The string `s` plays the role of $v$: the code that builds a program from a text. The expression `s % s` plays the role of $d(v)$: the template applied to itself. The same pattern with `print(len(s % s))` in place of `print(s % s)` gives a program of 50 characters that prints the number 50, and any other computable function of the program text can be put in that place.

## Consequences

**Rice's theorem.** Let $A$ be a set of indices that is closed under equal functions (if $\varphi_a = \varphi_b$ and $a \in A$, then $b \in A$), with $A \ne \emptyset$ and $A \ne \mathbb{N}$. Choose $a \in A$ and $b \notin A$. If $A$ were decidable, the function $f(e) = b$ for $e \in A$ and $f(e) = a$ for $e \notin A$ would be total computable. A fixed point $n$ gives a contradiction: if $n \in A$, then $\varphi_n = \varphi_b$ and so $n \notin A$; if $n \notin A$, then $\varphi_n = \varphi_a$ and so $n \in A$. This is the index-set form of [Rice's theorem](/rice-theorem/), proved here without a reduction from the halting problem.

**The halting problem.** If a total computable $h$ decided whether $\varphi_e(e)$ is defined, Kleene's form applied to "halt on input $x$ if and only if $h$ says that $\varphi_e(e)$ does not halt" would give a program that halts on its own index exactly when it does not.

**Programs that use their own code.** Self-reproducing programs, programs that print their own checksum, and a program that searches for the shortest program equivalent to itself can all be written. The theorem gives one proof that [Kolmogorov complexity](/kolmogorov-complexity/) is not computable: a program that knows its own length could search for the first string whose complexity is larger than that length and print it, which gives a contradiction.

**Recursive definitions are sound.** A definition of a partial function in terms of itself, such as the equations of the [Ackermann function](/ackermann-function/), can be read as the specification $\psi(e, x)$ of a program that calls the program $e$, and the theorem gives an index $e$ that satisfies it. In the [lambda calculus](/lambda-calculus/), the fixed-point combinators play the same role.

**Gödel's diagonal lemma.** The diagonal lemma of [Gödel's incompleteness theorem](/godel-incompleteness-theorem/) builds a sentence that states a property of its own Gödel number. It has the same structure as the proof above, with formulas in place of programs and substitution in place of s-m-n.

## Tightness

**$f$ must be computable.** With an oracle for $K$ there is a function with no fixed point. Let $g(e)$ be an index of the constant function $\varphi_e(0) + 1$ if $\varphi_e(0)$ is defined, and an index of the constant function $0$ otherwise. Then $\varphi_{g(e)}(0) \ne \varphi_e(0)$ for every $e$. The function $g$ is computable from $K$, since the oracle answers whether $\varphi_e(0)$ is defined. Arslanov's completeness criterion makes this exact for computably enumerable sets: a c.e. set computes a function with no fixed point if and only if it has the degree $\mathbf{0}'$ of $K$ (see [Turing degrees](/turing-degrees/)).

**The fixed point is not decidable.** For a given $f$ the set of all fixed points $\{ n : \varphi_n = \varphi_{f(n)} \}$ is infinite, by the form with parameters, but in general not decidable. For $f$ with constant value an index $z$ of the constant function $0$, the fixed points are the indices of that function, an index set that is undecidable by Rice's theorem. The proof gives some fixed points, not a way to recognize them.

**The numbering matters.** The proof uses the s-m-n theorem, so it holds for acceptable numberings. For the numbering of Friedberg without repetition, in which each function has one index, the fixed-point form fails for $f(e) = e + 1$, since no two indices compute the same function.

## History

Kleene published the theorem in 1938 in his paper on notations for ordinal numbers, where it is used to define the system $\mathcal{O}$ of notations: a notation for a limit ordinal is an index of a program that lists notations for a sequence of smaller ordinals, so the definition refers to programs that use notations of the system being defined. Kleene's form, with $\psi(e, x)$, is the form of that paper. Rogers (1967) stated the fixed-point form $\varphi_n = \varphi_{f(n)}$ and used it throughout his book. Sipser presents the theorem for Turing machines that obtain their own description, and derives the undecidability of the acceptance problem and the existence of self-reproducing machines from it.

## References
