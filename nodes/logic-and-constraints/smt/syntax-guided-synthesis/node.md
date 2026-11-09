---
tag: 99PKFF
kind: problem
slug: syntax-guided-synthesis
name: Syntax-guided synthesis
aliases:
- SyGuS
- syntax-guided program synthesis
area: logic-and-constraints/smt
level: research
summary: Find a program from a given grammar that satisfies a logical specification.
prereqs: [smt-problem, context-free-grammar]
see_also: [cegis, hilberts-tenth-problem, inductive-invariant, quantifier-instantiation, linear-integer-arithmetic-satisfiability, bit-vector-satisfiability, halting-problem, symbolic-execution]
sources:
  - paper: doi:10.1109/FMCAD.2013.6679385
    title: Rajeev Alur, Rastislav Bodík, Garvit Juniwal, Milo M. K. Martin, Mukund Raghothaman, Sanjit A. Seshia, Rishabh Singh, Armando Solar-Lezama, Emina Torlak and Abhishek Udupa, Syntax-guided synthesis, Formal Methods in Computer-Aided Design (FMCAD 2013)
    locator: the definition of the problem (background theory, typed function to synthesize, grammar and specification), the enumerative, symbolic and stochastic solvers, and the first benchmarks
  - paper: "Benjamin Caulfield, Markus N. Rabe, Sanjit A. Seshia and Stavros Tripakis, What's decidable about syntax-guided synthesis?, arXiv:1510.08393, 2015"
    locator: undecidability for the theory of uninterpreted functions, a decidable fragment that is EXPTIME-complete, and decidability for finite bit-vector domains without concatenation (to be checked)
  - paper: doi:10.1145/1168857.1168907
    title: Armando Solar-Lezama, Liviu Tancau, Rastislav Bodík, Sanjit Seshia and Vijay Saraswat, Combinatorial sketching for finite programs, Architectural Support for Programming Languages and Operating Systems (ASPLOS 2006)
    locator: synthesis from a program with holes, the forerunner of grammars as the syntactic restriction, solved by CEGIS
  - paper: "Rajeev Alur, Arjun Radhakrishna and Abhishek Udupa, Scaling enumerative program synthesis via divide and conquer, Tools and Algorithms for the Construction and Analysis of Systems (TACAS 2017)"
    locator: the EUSolver, which enumerates terms and learns decision trees over predicates (to be checked)
  - paper: "Andrew Reynolds, Morgan Deters, Viktor Kuncak, Cesare Tinelli and Clark Barrett, Counterexample-guided quantifier instantiation for synthesis in SMT, Computer Aided Verification (CAV 2015)"
    locator: single-invocation specifications solved inside an SMT solver by quantifier instantiation (to be checked)
  - paper: "Sumit Gulwani, Automating string processing in spreadsheets using input-output examples, Principles of Programming Languages (POPL 2011)"
    locator: synthesis from examples over a domain-specific language with version space algebras (FlashFill)
  - paper: "Qinheping Hu, Jason Breck, John Cyphert, Loris D'Antoni and Thomas Reps, Proving unrealizability for syntax-guided synthesis, Computer Aided Verification (CAV 2019)"
    locator: methods that prove that no term of the grammar meets the specification (to be checked)
  - paper: "Yuri Matiyasevich, Enumerable sets are Diophantine, Soviet Mathematics Doklady 11 (1970)"
    locator: the undecidability of Hilbert's tenth problem, used in the undecidability proof
---

Syntax-guided synthesis (SyGuS) asks for a term, taken from a language given by a [context-free grammar](/context-free-grammar/), that makes a logical specification valid in a background theory such as [linear integer arithmetic](/linear-integer-arithmetic-satisfiability/) or [bit-vectors](/bit-vector-satisfiability/). The specification says *what* the program must do; the grammar says *which* programs are allowed, and so limits the search and keeps the answers readable. SyGuS is a common input format for synthesis tools and a yearly competition. The usual algorithm is [CEGIS](/cegis/): that page gives the loop and proves that it stops on finite candidate spaces, and this page states the problem, its decidable cases, and why it is undecidable in general.

## In plain words

You describe what a small program must do, with a logical rule such as "the answer is at least each input, and equal to one of them". You also give a grammar that lists which building blocks the program may use, such as plus, comparison and "if then else". The task is to find a program built from those blocks that obeys the rule for every input, or to show that no such program exists.

Tools try candidate programs, test them with a solver, and use each failed test to guide the next try. When the grammar allows only finitely many programs, this search always ends. In general, no method can decide every question of this kind, because such questions can encode any equation about whole numbers.

## Definition

**Input.** A SyGuS problem has four parts.

- A *background theory* $T$, such as LIA, BV or strings, with its signature.
- A *function symbol* $f$ to synthesize, with a type, for example $f : \mathrm{Int} \times \mathrm{Int} \to \mathrm{Int}$, and named parameters.
- A *grammar* $G$: a context-free grammar whose words are terms of the type of $f$, built from the signature of $T$ and the parameters.
- A *specification* $\varphi$: a formula of $T$ extended with $f$, usually of the form $\forall \bar{x}\, \psi(f, \bar{x})$.

**Output.** A term $e \in L(G)$ such that $\varphi[f := \lambda \bar{p}.\, e]$ is valid in $T$, or the answer that none exists (the problem is *unrealizable*).

Several functions may be synthesized at once, each with its own grammar.

**Relation to CEGIS.** CEGIS is an algorithm; SyGuS is a problem. CEGIS solves a SyGuS problem by taking the candidates from $L(G)$, the synthesizer from an enumerator or a solver, and the verifier from a decision procedure for $T$.

## Variants

- **General track.** Any specification in a theory: CLIA (conditional linear integer arithmetic), LIA, BV, strings.
- **Programming by example (PBE).** The specification is a finite list of input-output pairs, such as string transformations in spreadsheets.
- **Invariant synthesis (INV).** Find a predicate $\mathit{inv}$ with the three conditions of an [inductive invariant](/inductive-invariant/) of a loop.
- **Single-invocation.** Each occurrence of $f$ in $\psi$ has the same arguments $\bar{x}$; then $\forall \bar{x}\, \exists y\, \psi[y/f(\bar{x})]$ is an equivalent form, and solvers use [quantifier instantiation](/quantifier-instantiation/).
- **Unrealizability.** Prove that no term of $G$ works.
- **Optimal synthesis.** Find a smallest or cheapest term of $G$.
- **Sketching.** A grammar with one fixed shape and holes for constants.

## Examples

All three examples were checked by brute force; the first over the inputs $-4 \le x, y \le 4$.

1. **Maximum of two integers.** Let $T$ be LIA, $f(x, y)$ of type Int, the specification
$$\forall x, y.\ f(x, y) \ge x \wedge f(x, y) \ge y \wedge (f(x, y) = x \vee f(x, y) = y),$$
and the grammar $S \to x \mid y \mid 0 \mid 1 \mid S + S \mid \mathrm{ite}(B, S, S)$, $B \to S \le S$. Enumerating terms by size (the number of nodes), the 148 integer terms of size at most 5 all fail, and the first solutions have size 6: $\mathrm{ite}(x \le y, y, x)$ and $\mathrm{ite}(y \le x, x, y)$. CEGIS with this enumerator, and a verifier that returns the first failing input in the order of $x$ and then $y$, needs only two counterexamples, $(-4, -3)$ and $(-3, -4)$, and three rounds.
2. **The same specification without ite.** With $S \to x \mid y \mid 0 \mid 1 \mid S + S$, the problem is unrealizable. Each term denotes $a x + b y + c$ with natural numbers $a, b, c$. The inputs $(0, 0)$, $(1, 0)$ and $(0, 1)$ force $c = 0$, $a = 1$ and $b = 1$, but then $f(1, 1) = 2 \ne 1$. The brute force over all terms up to size 7 also finds no solution.
3. **A loop invariant.** For the loop `x := 0; while x < 10 do x := x + 1` with the assertion $x = 10$ at the exit, find $\mathit{inv}(x)$ with $x = 0 \Rightarrow \mathit{inv}(x)$, $\mathit{inv}(x) \wedge x < 10 \Rightarrow \mathit{inv}(x + 1)$, and $\mathit{inv}(x) \wedge x \ge 10 \Rightarrow x = 10$. The term $x \le 10$ is a solution. The term true is not, because it fails the third condition at $x = 11$. Here $\mathit{inv}$ occurs with two different arguments, so the problem is not single-invocation.

## Known algorithms

| method | idea | notes |
|---|---|---|
| [CEGIS](/cegis/) | a synthesizer for finite example sets and a verifier for all inputs, in a loop | the frame of most solvers; stops for finite candidate spaces |
| enumerative search (Udupa et al. 2013; Alur et al. 2013) | enumerate the terms of $G$ by size, and keep one term for each behaviour on the current examples | strong for small programs; the first solution is a smallest one |
| divide and conquer (EUSolver, Alur, Radhakrishna and Udupa 2017) | enumerate terms that fit some examples and predicates that separate them, then learn a decision tree of ite | strong for CLIA and PBE |
| symbolic search | encode a term of bounded size as a tree with selector variables, and solve the formula with an SMT solver | complete up to the bound; used with sketches |
| single-invocation solving (Reynolds et al. 2015) | for single-invocation specifications, solve $\forall \bar{x} \exists y$ by quantifier instantiation, and read a term from the instances | inside cvc5; often far faster |
| version space algebras (Gulwani 2011) | represent all programs consistent with the examples at once | for PBE over domain-specific languages |
| stochastic search | random walk over terms, guided by a cost on the examples | finds unusual programs; incomplete |
| unrealizability proofs (Hu et al. 2019) | summarize the semantics of the grammar on the examples, and show that no term fits | proves that no answer exists |

## Bounds

**Theorem 1 (finite grammars).** If $L(G)$ is finite and the validity of quantifier-free formulas of $T$ (and so of their universal closures) is decidable, then SyGuS is decidable. CEGIS with an enumerator decides it within $|L(G)| + 1$ rounds.

*Proof.* Check each of the finitely many terms with the decision procedure. The bound for CEGIS is the termination theorem on the [CEGIS](/cegis/) page, with the candidate space $L(G)$. $\square$

**Theorem 2 (semi-decidability).** If validity in $T$ is decidable and $G$ is any grammar, the set of realizable SyGuS problems is recursively enumerable: enumerating $L(G)$ by size and checking each term finds a solution whenever one exists. In general, no algorithm also detects every unrealizable problem, by Theorem 3.

**Theorem 3 (undecidability).** SyGuS is undecidable, even when the grammar uses only the symbols $0$, $1$, $+$, $=$ and ite, and each check of a candidate is a formula without variables in the arithmetic of the integers, whose truth can be computed by evaluation.

*Proof.* Reduce Hilbert's tenth problem over the natural numbers, which is undecidable (Matiyasevich 1970): given a polynomial $p(n_1, \ldots, n_k)$ with integer coefficients, does it have a root in $\mathbb{N}^k$? Write $p = p^+ - p^-$ with $p^+$ and $p^-$ having natural coefficients. Build a SyGuS problem with $f : \mathrm{Int} \to \mathrm{Int}$ and parameter $x$:

- the grammar $S \to \mathrm{ite}(x = 1, N, \mathrm{ite}(x = 2, N, \ldots \mathrm{ite}(x = k, N, 0) \ldots))$ and $N \to 0 \mid N + 1$;
- the specification $p^+(f(1), \ldots, f(k)) = p^-(f(1), \ldots, f(k))$, with integer arithmetic with $+$ and $\times$ as the background theory.

Each term of $L(G)$ picks numerals $m_1, \ldots, m_k \ge 0$ for the $k$ copies of $N$, and it defines a function with $f(i) = m_i$ for $1 \le i \le k$; each tuple of natural numbers arises in this way. After the substitution, the specification is the closed formula $p^+(m_1, \ldots, m_k) = p^-(m_1, \ldots, m_k)$, which holds exactly when $(m_1, \ldots, m_k)$ is a root of $p$. So the problem is realizable if and only if $p$ has a root in $\mathbb{N}^k$, and the construction is computable. $\square$

For example, $p = n_1 n_2 - 6$ together with the condition $f(1) + 1 \le f(2)$ in the specification has the solutions $(m_1, m_2) = (1, 6)$ and $(2, 3)$.

The proof shows that the hardness comes from the search over the grammar, not from the checks. If $f$ does not occur in $\varphi$, the problem is the validity of $\forall \bar{x}\, \varphi$ in $T$, so SyGuS is also undecidable for each theory with undecidable validity, such as nonlinear integer arithmetic. Caulfield, Rabe, Seshia and Tripakis (2015) report that SyGuS is undecidable already for the theory of uninterpreted functions, decidable and EXPTIME-complete for a restricted fragment of it, and decidable over finite bit-vector domains without concatenation (to be checked).

## Reductions

- **To CEGIS rounds.** Each round is a satisfiability query of $T$ for the synthesizer and one for the verifier.
- **To one exists-forall SMT query, for bounded size.** Encode a term of size at most $s$ by selector variables, and ask $\exists \mathrm{sel}\, \forall \bar{x}\, \psi$.
- **From validity in $T$.** The case where $f$ does not occur.
- **From Hilbert's tenth problem.** As in Theorem 3.
- **Invariant synthesis to constrained Horn clauses.** The INV track is the solving of Horn clauses with one unknown predicate and a grammar for its body.
- **PBE to SyGuS.** A finite list of examples is a specification without universal quantifiers.

## Applications

- Loop invariants and ranking functions for program verification.
- Superoptimization: find the shortest instruction sequence equal to a given one, for example tricks with bit-vector operations.
- String transformations in spreadsheets from a few examples.
- Program repair: replace a faulty expression by a term of a grammar that passes the tests and the specification.
- Deobfuscation of mixed Boolean and arithmetic expressions.
- Synthesis of controllers and of glue code between interfaces.

## References
