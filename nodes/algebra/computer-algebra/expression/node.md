---
tag: 4C89CW
kind: abstract-type
slug: expression
name: Symbolic expression (abstract type)
aliases:
- symbolic expression
- symbolic term
- formula object
area: algebra/computer-algebra
level: core
summary: Abstract type for symbolic expressions supporting construction, simplification and substitution.
prereqs: [term-algebra]
see_also: [expression-tree, expression-dag, canonical-form, constant-problem, straight-line-program, e-graph, abstract-syntax-tree, expression-swell]
sources:
  - book: isbn:9780792392590
    title: Keith O. Geddes, Stephen R. Czapor and George Labahn, Algorithms for Computer Algebra, Kluwer, 1992
    locator: Chapter 1 (introduction to computer algebra) and Chapter 3 (normal forms and algebraic representations, including the representation of expressions as trees and the levels of abstraction)
  - book: isbn:9781568811581
    title: Joel S. Cohen, Computer Algebra and Symbolic Computation, Elementary Algorithms, A K Peters, 2002
    locator: Chapter 3, the recursive structure of mathematical expressions (operators, operands, substitution, free of)
  - paper: doi:10.1145/362637.362648
    title: Joel Moses, Algebraic simplification, a guide for the perplexed, Communications of the ACM 14(8), 527-537, 1971
    locator: the discussion of simplification as a map on expressions and its classes
  - paper: doi:10.2307/2271358
    title: Daniel Richardson, Some undecidable problems involving elementary functions of a real variable, Journal of Symbolic Logic 33(4), 514-520, 1968
    locator: undecidability of zero-equivalence, the lower bound for the simplify operation
---

A symbolic expression is a formula held as data: a constant, a symbol, or an operator applied to a list of smaller expressions. The abstract type gives ways to build expressions, to take them apart, to substitute expressions for symbols, to evaluate them at numbers, and to simplify them. Every computer algebra system has such a type at its core. Its data structures differ, as [trees](/expression-tree/), as [DAGs](/expression-dag/) with shared subexpressions, or as [straight-line programs](/straight-line-program/), but the operations and laws below are the same.

## In plain words

A formula such as "x times (y plus 1)" can be stored in a program as a small structure: a times sign, with two parts, the first the letter x and the second a plus sign with the letter y and the number 1. The program can then do with the formula what a person does on paper. It can look at the outer sign and the parts. It can put a new formula in place of a letter. It can plug in numbers. It can tidy the formula, for example by multiplying out or collecting equal terms.

Two formulas can look different and still mean the same thing. Deciding whether they do is the hard part. For some kinds of formulas it is easy, and for others it is impossible in general.

## Operations

Fix a set $C$ of constants (integers, rationals, or elements of a field $K$), a set $X$ of symbols, and a set $\Omega$ of operators, each with an arity or variadic, for example $+$, $\times$, power, $\exp$, $\sin$. The values of the type are the finite terms over $C$, $X$ and $\Omega$, as in a [term algebra](/term-algebra/). Write $E$ for this set. Each operator $\omega$ has a meaning $[\![\omega]\!]$, a partial function on a domain $D$ such as $\mathbb{Q}$, $\mathbb{C}$ or a ring $R$.

| operation | signature | what it does |
|---|---|---|
| `const` | $C \to E$ | the expression for a constant $c$ |
| `sym` | $X \to E$ | the expression for a symbol $x$ |
| `apply` | $\Omega \times E^k \to E$ | the expression $\omega(e_1, \ldots, e_k)$ |
| `head`, `args` | $E \to \Omega \cup \{\text{const}, \text{sym}\}$, $E \to E^{*}$ | the outer operator and the list of operands; atoms have no operands |
| `equal` | $E \times E \to \text{bool}$ | syntactic identity $e_1 \equiv e_2$: same head and pairwise identical operands |
| `free_of` | $E \times X \to \text{bool}$ | true when the symbol $x$ does not occur in $e$ |
| `subs` | $E \times X \times E \to E$ | $e[x := e']$, every occurrence of $x$ replaced by $e'$ |
| `eval` | $E \times (X \to D) \to D$ | the value of $e$ when each symbol takes the value given by an environment $\rho$; partial, since $1/0$ is undefined |
| `simplify` | $E \to E$ | an equivalent expression, usually smaller or in a standard shape |
| `diff` | $E \times X \to E$ | the derivative with respect to $x$, by the chain rule, for differentiable operators |

Two notions of equality matter. Syntactic identity $\equiv$ is cheap: a walk over both terms. Semantic equivalence $e_1 \sim e_2$ means $\text{eval}(e_1, \rho) = \text{eval}(e_2, \rho)$ for every $\rho$ where both are defined, or equality in a stated ring. The operation `simplify` maps toward the second, and it is a [canonical form](/canonical-form/) when $e_1 \sim e_2$ implies $\text{simplify}(e_1) \equiv \text{simplify}(e_2)$.

### Example

Let $e = \text{apply}(\times, [\text{sym}(x), \text{apply}(+, [\text{sym}(y), \text{const}(1)])])$, that is $x(y + 1)$.

| step | operation | result |
|---|---|---|
| 1 | head$(e)$ | $\times$ |
| 2 | args$(e)$ | $[x,\ y + 1]$ |
| 3 | free_of$(e, z)$ | true |
| 4 | subs$(e, y, x - 1)$ | $x((x - 1) + 1)$ |
| 5 | eval of step 4 at $x = 3$ | $9$ |
| 6 | simplify of step 4, expanding and collecting | $x^2$ |
| 7 | equal(step 4, $x^2$) | false |
| 8 | diff$(e, x)$, then simplify | $y + 1$ |

Steps 6 and 7 show the two equalities: the expression of step 4 and $x^2$ are equivalent but not identical.

## Laws

For constants $c$, symbols $x \ne y$, operators $\omega$, expressions $e, e', e_i$ and environments $\rho$:

$$\begin{aligned}
&(\text{E1})\quad \text{head}(\text{apply}(\omega, [e_1, \ldots, e_k])) = \omega, \qquad \text{args}(\text{apply}(\omega, [e_1, \ldots, e_k])) = [e_1, \ldots, e_k],\\
&(\text{E2})\quad \text{subs}(\text{sym}(x), x, e') = e', \quad \text{subs}(\text{sym}(y), x, e') = \text{sym}(y), \quad \text{subs}(\text{const}(c), x, e') = \text{const}(c),\\
&(\text{E3})\quad \text{subs}(\text{apply}(\omega, [e_1, \ldots, e_k]), x, e') = \text{apply}(\omega, [\text{subs}(e_1, x, e'), \ldots, \text{subs}(e_k, x, e')]),\\
&(\text{E4})\quad \text{eval}(\text{apply}(\omega, [e_1, \ldots, e_k]), \rho) = [\![\omega]\!](\text{eval}(e_1, \rho), \ldots, \text{eval}(e_k, \rho)),\\
&(\text{E5})\quad \text{eval}(\text{subs}(e, x, e'), \rho) = \text{eval}(e, \rho[x \mapsto \text{eval}(e', \rho)]),\\
&(\text{E6})\quad \text{free\_of}(e, x) \implies \text{subs}(e, x, e') = e,\\
&(\text{E7})\quad \text{simplify}(e) \sim e .
\end{aligned}$$

Laws (E1) to (E4) say that the type is the free term algebra with its evaluation map; they fix `equal`, `subs` and `eval` by structural recursion. Law (E5) is the substitution lemma: it follows from (E2) to (E4) by induction on $e$. Law (E7) is the only law on `simplify`; it says nothing about the shape of the result, and this freedom is where systems differ. When `diff` is present, its laws are $\text{diff}(\text{const}(c), x) \sim 0$, $\text{diff}(\text{sym}(x), x) \sim 1$, the sum and product rules, and the chain rule for each unary operator.

## Implementations

| implementation | sharing | `equal` | `subs` | notes |
|---|---|---|---|---|
| [expression tree](/expression-tree/) | none | $O(n)$ for size $n$ | $O(n)$, copies the tree | simplest; a repeated subexpression is stored once per occurrence |
| [expression DAG](/expression-dag/) with [hash consing](/hash-consing/) | full, equal subterms are one node | $O(1)$ by pointer | $O(n)$ with a memo table over distinct nodes | size can be exponentially smaller than the tree |
| [term DAG](/term-dag/) | full | $O(1)$ after interning | as for the DAG | the same idea in term rewriting and SMT solvers |
| [straight-line program](/straight-line-program/) | full, explicit | not a canonical test | composition of programs | a sequence of assignments; the model of algebraic complexity |
| [e-graph](/e-graph/) | classes of equivalent terms | membership in a class | rebuilding after merges | stores many equivalent forms at once |
| [abstract syntax tree](/abstract-syntax-tree/) of a parser | none | $O(n)$ | $O(n)$ | the form produced by parsing, before any algebra |

Specialized representations implement a subtype. For polynomials, the [dense](/dense-polynomial/) and [sparse](/sparse-polynomial/) representations implement `simplify` as a canonical form in time linear in their size, with arithmetic in place of `apply`.

## Lower bounds

- **Zero equivalence is undecidable in general.** For expressions over the integers and $\pi$ built with $+$, $\times$, $\exp$, $\sin$ and $|\cdot|$ in one real variable, no algorithm decides $e \sim 0$ (Richardson 1968). So no implementation of `simplify` is canonical for this class; see [Richardson's theorem](/richardson-theorem/) and the [constant problem](/constant-problem/).
- **Canonical forms can be exponentially larger.** The expression $\prod_{i=1}^{n}(x_i + y_i)$ has size $\Theta(n)$, but its expanded form has $2^n$ terms, so any `simplify` that expands takes $\Omega(2^n)$ time on it. A DAG of size $O(n)$ for $(x + 1)^{2^n}$, built by repeated squaring, expands to $2^n + 1$ terms. See [expression swell](/expression-swell/).
- **Polynomial expressions: randomized but not known deterministic.** For expressions with only $+$, $-$, $\times$ and constants, $e \sim 0$ is decidable, and a random evaluation decides it with one-sided error by the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/). No deterministic polynomial-time test is known for DAG inputs; this is [polynomial identity testing](/polynomial-identity-testing/).
- **Syntactic equality needs to read the input.** On trees, `equal` must look at every node in the worst case, so it takes $\Omega(n)$; hash consing moves this cost to construction.

## References
