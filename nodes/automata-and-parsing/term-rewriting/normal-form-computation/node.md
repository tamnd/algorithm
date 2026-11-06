---
tag: K3BF8G
kind: problem
slug: normal-form-computation
name: Normal form computation
aliases:
- normalization
- evaluation of terms
area: automata-and-parsing/term-rewriting
level: core
summary: Compute the normal form of a given term under a rewrite system.
prereqs: [normal-form, term-rewriting-system, rewrite-step]
see_also: [innermost-reduction, outermost-reduction, reduction-strategy, termination, weak-normalization, word-problem, graph-reduction, halting-problem]
sources:
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Chapter 2, Abstract Reduction Systems (Section 2.1, normal forms and normalization); Chapter 5, Termination (the undecidability of termination)
  - book: isbn:9780521391153
    title: Terese (Marc Bezem, Jan Willem Klop and Roel de Vrijer, editors), Term Rewriting Systems, Cambridge University Press, 2003
    locator: Chapter 5, Properties of rewriting, decidability and modularity; Chapter 9, Strategies
  - paper: doi:10.1007/3-540-51081-8_107
    title: Dieter Hofbauer and Clemens Lautemann, Termination proofs and the length of derivations, Rewriting Techniques and Applications (RTA 1989), Lecture Notes in Computer Science 355
    locator: pp. 167 to 177 (polynomial interpretations bound derivation lengths by a double exponential)
  - paper: doi:10.1016/0304-3975(92)90289-r
    title: Dieter Hofbauer, Termination proofs by multiset path orderings imply primitive recursive derivation lengths, Theoretical Computer Science 105(1) (1992)
    locator: pp. 129 to 140
  - paper: doi:10.1016/0304-3975(94)00135-6
    title: Andreas Weiermann, Termination proofs for term rewriting systems by lexicographic path orderings imply multiply recursive derivation lengths, Theoretical Computer Science 139 (1995)
    locator: pp. 355 to 362
---

**Normal form computation** asks for a [normal form](/normal-form/) of a term: rewrite it with the rules of a [term rewriting system](/term-rewriting-system/) until no rule applies. It is what an interpreter of a functional or equational language does, what a computer algebra system does when it simplifies, and what a theorem prover does to decide an equation with a convergent system. In general the problem is not computable, because rewriting can simulate any Turing machine; when the system terminates, every [strategy](/reduction-strategy/) solves it, and the questions become which normal form and at what cost.

## In plain words

You have a list of simplification rules, such as "zero plus anything is that thing", and an expression. Apply rules wherever they fit, again and again, until no rule fits anywhere. What is left is the answer.

Three things can go wrong. The process may never stop, because some rule keeps creating new work. It may stop or not depending on where you apply the rules first. And different choices may stop at different answers. Good rule sets avoid the first and third problems, and good choices of where to apply the rules avoid the second.

## Definition

We use the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, positions as sequences of positive integers, subterm $t|_p$ and replacement $t[s]_p$, substitutions $\sigma$ applied as $t\sigma$, rules $l \to r$, the rewrite relation $\to_R$ and its reflexive transitive closure $\to_R^*$.

**Input.** A finite term rewriting system $R$ and a term $t \in T(\Sigma, V)$.

**Output.** A term $v$ with $t \to_R^* v$ such that $v$ is in normal form, that is, no subterm of $v$ is an instance $l\sigma$ of a left side of $R$. If $t$ has no normal form, the output is undefined.

This is a search problem. When $R$ is [confluent](/confluence/), a normal form of $t$ is unique if it exists, and the problem becomes the computation of a function, written $t{\downarrow}_R$. When $R$ is also terminating ([convergent](/termination/)), the function is total and computable.

## Variants

- **Existence of a normal form.** Decide whether $t$ has a normal form at all. This is the halting problem of rewriting; see Bounds.
- **With a step bound.** Given also $B$, return a normal form reachable in at most $B$ steps, or report that there is none. Breadth-first search over reducts solves this.
- **Fixed strategy.** Compute the normal form reached by a given strategy, such as [innermost reduction](/innermost-reduction/) or [outermost reduction](/outermost-reduction/). Each strategy defines a deterministic function, possibly partial on terms that have a normal form.
- **Head or weak head normal form.** Stop when the root can no longer be rewritten, or when it is a constructor; lazy languages compute these and leave the arguments unevaluated.
- **Modulo a theory.** Rewrite equivalence classes modulo equations such as associativity and commutativity, as in [rewriting modulo equations](/rewriting-modulo-equations/), with [AC matching](/ac-matching/) at each step.
- **Lambda terms.** For [beta-reduction](/beta-reduction/), normal forms are unique by the [Church-Rosser theorem](/church-rosser-theorem/), and the leftmost-outermost strategy finds them.

## Examples

**Arithmetic.** With $\mathit{add}(0, y) \to y$, $\mathit{add}(s(x), y) \to s(\mathit{add}(x, y))$, $\mathit{mul}(0, y) \to 0$ and $\mathit{mul}(s(x), y) \to \mathit{add}(\mathit{mul}(x, y), y)$, the term $\mathit{mul}(s^2(0), s(0))$ has the normal form $s^2(0)$, reached in 6 innermost steps. The system is convergent, so every strategy reaches the same result.

**The strategy matters.** With $f(x) \to a$ and $b \to b$, the term $f(b)$ has the normal form $a$, reached by one step at the root. Innermost reduction never reaches it: it contracts $b$ forever. The term $b$ has no normal form at all.

**More than one normal form.** With $a \to b$ and $a \to c$, the term $a$ has the two normal forms $b$ and $c$, and both are correct outputs. The system is not confluent.

**The empty system.** With $R = \emptyset$ every term is its own normal form, reached in zero steps.

**Size of the answer.** With $d(x) \to p(x, x)$, the term $d^k(a)$ has a normal form with $2^k$ occurrences of $a$, reached in $k$ steps. Written as a tree the output is exponential in the input; written as a graph with sharing it has $k + 1$ nodes.

## Known algorithms

- **Breadth-first search over reducts.** A finite $R$ gives each term finitely many one-step reducts, so the reducts of $t$ form a finitely branching tree. Searching it breadth-first finds a normal form whenever one exists, and runs forever otherwise. This is the reference algorithm, and the slowest.
- **[Innermost reduction](/innermost-reduction/).** Evaluate arguments before the function, call-by-value. Fast, and it reuses evaluated arguments, but not normalizing.
- **[Outermost reduction](/outermost-reduction/).** Contract the leftmost-outermost redex. Normalizing for left-normal orthogonal systems and for the lambda calculus; parallel-outermost reduction is normalizing for all orthogonal systems.
- **Needed reduction.** In orthogonal systems, contract a redex that every normalizing reduction must contract. Normalizing; a needed redex can be found from the left sides alone in strongly sequential systems.
- **[Graph reduction](/graph-reduction/).** Rewrite a graph instead of a tree, so that copied subterms are shared and evaluated at most once. This is how lazy functional languages run.
- **Fast matching.** Every strategy spends most of its time finding redexes. [Bottom-up tree automata](/hoffmann-odonnell-matching/) and [discrimination trees](/discrimination-tree/) find all matching rules in one pass.

## Bounds

**Not computable in general.** A Turing machine can be encoded as a term rewriting system with one rule per transition, so that a configuration term has a normal form iff the machine halts from it. Hence it is undecidable whether a term has a normal form, by reduction from the [halting problem](/halting-problem/), and there is a fixed finite system for which this is undecidable, built from a universal machine. The problem is semi-decidable: breadth-first search confirms a normal form when there is one. For the same reason [termination](/termination/) of a system is undecidable ([undecidability of termination](/undecidability-of-termination/)).

**Number of steps.** For terminating systems, the cost is governed by the derivation length, the longest reduction from a term of size $n$. No computable function bounds it for all terminating systems, since rewriting can compute any total computable function. The method used to prove termination bounds it:

| termination proof | bound on derivation length |
|---|---|
| [polynomial interpretation](/polynomial-interpretation/) | double exponential in $n$ (Hofbauer and Lautemann, 1989) |
| multiset path ordering, a [recursive path ordering](/recursive-path-ordering/) | primitive recursive (Hofbauer, 1992) |
| [lexicographic path ordering](/lexicographic-path-ordering/) | multiply recursive (Weiermann, 1995) |

The bounds cannot be improved to a smaller class in general: for instance the [Ackermann function](/ackermann-function/) has a terminating system proved by the lexicographic path ordering, and its derivation lengths are not primitive recursive.

**Lower bounds from the output.** The output can have size exponential in the number of steps, as the example $d^k(a)$ shows, so any algorithm that writes the answer as a tree needs exponential time on it; with sharing the output has polynomial size in the number of steps.

## Reductions

- **Word problem.** If $R$ is convergent, $s \approx_R t$ iff $s{\downarrow}_R = t{\downarrow}_R$. So the [word problem](/word-problem/) of the equations of $R$ reduces to two normal form computations and one comparison; [Knuth-Bendix completion](/knuth-bendix-completion/) produces such systems.
- **Halting problem.** The halting problem reduces to the existence of a normal form, as above, and the existence of a normal form reduces to the halting problem, since breadth-first search is a program that halts iff a normal form exists.
- **Confluence testing.** For a finite terminating system, [deciding confluence](/confluence-decision-problem/) reduces to computing the normal forms of both sides of each [critical pair](/critical-pair/).

## Applications

- **Functional and equational programming.** Running a program in languages such as OBJ, Maude, Haskell or ML is normal form computation under a fixed strategy, innermost for strict languages and outermost with sharing for lazy ones.
- **Decision procedures.** With a convergent system, equality in an equational theory is decided by normalizing both sides, as for the group axioms after completion.
- **Simplification.** Computer algebra systems, compilers and theorem provers simplify expressions by rewriting with oriented equations, and rely on termination of the rule set to stop.
- **Proof assistants.** Type checkers for dependent types compare terms by normalizing them; beta-reduction and the computation rules of inductive types are the rewrite rules.

## References
