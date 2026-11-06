---
tag: 02HYDR
kind: theorem
slug: undecidability-of-termination
name: Undecidability of termination
aliases:
- undecidability of strong normalization
- uniform halting problem for rewriting
area: automata-and-parsing/term-rewriting
level: advanced
summary: Termination of general term rewriting systems is undecidable.
prereqs: [termination, post-correspondence-problem]
see_also: [termination-decision-problem, undecidability-of-word-problem, halting-problem, turing-machine, dependency-pairs, recursive-path-ordering, polynomial-interpretation, weak-normalization]
sources:
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Section 5.1.1, Undecidability in the general case
  - paper: doi:10.1016/0304-3975(92)90022-8
    title: Max Dauchet, Simulation of Turing machines by a regular rewrite rule, Theoretical Computer Science 103(2) (1992)
    locator: pp. 409 to 420 (termination is undecidable for one left-linear, non-overlapping, variable-preserving rule)
  - paper: doi:10.1007/978-3-642-04027-6_20
    title: Jörg Endrullis, Herman Geuvers and Hans Zantema, Degrees of undecidability in term rewriting, Computer Science Logic (CSL 2009), Lecture Notes in Computer Science 5771
    locator: pp. 255 to 270 (strong normalization of one term is Σ^0_1-complete, uniform termination is Π^0_2-complete)
  - paper: doi:10.2307/2269811
    title: Philip K. Hooper, The undecidability of the Turing machine immortality problem, Journal of Symbolic Logic 31(2) (1966)
    locator: pp. 219 to 234
  - paper: doi:10.1016/S0747-7171(87)80022-6
    title: Nachum Dershowitz, Termination of rewriting, Journal of Symbolic Computation 3(1 and 2) (1987)
    locator: pp. 69 to 115 (survey of termination methods, undecidability, and decidable cases such as ground systems)
---

The **undecidability of termination** says that no algorithm decides, for every finite term rewriting system $R$, whether $R$ is [terminating](/termination/), that is, whether every term has only finite reductions. It is the rewriting form of the [halting problem](/halting-problem/), and it holds both for the termination of one given term and for termination of all terms. It holds even for very restricted systems: Dauchet (1992) showed that it is undecidable for systems with a single left-linear rule. This is why termination tools search for proofs, with orders such as the [recursive path ordering](/recursive-path-ordering/) and methods such as [dependency pairs](/dependency-pairs/), and can always answer "don't know".

## Statement

We use the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, positions as sequences of positive integers, substitutions $\sigma$, rules $l \to r$, and $\to_R^*$ for the reflexive transitive closure. A term $t$ is **terminating** (strongly normalizing) if there is no infinite reduction $t = t_0 \to_R t_1 \to_R \cdots$, and $R$ is terminating if every term is.

**Theorem.**

1. (One term.) There is no algorithm that decides, given a finite $R$ and a term $t$, whether $t$ is terminating. The same holds for a fixed suitable $R$.
2. (Uniform.) There is no algorithm that decides, given a finite $R$, whether $R$ is terminating.

## In plain words

A rewriting system is a list of rules for simplifying expressions. It terminates if every way of applying the rules, to every expression, stops after finitely many steps. One would like a program that reads the rules and says whether they always stop.

No such program exists. The rules can be written so that they run a computer program, and they stop exactly when the program stops, so a termination checker would solve the halting problem. A second construction turns a matching puzzle into rules that loop exactly when the puzzle has a solution, and those puzzles cannot be solved by any program either.

## Proof

**Part 1, by Turing machines.** The proof of the [undecidability of the word problem](/undecidability-of-word-problem/) builds, for a deterministic [Turing machine](/turing-machine/) $M$, a finite string rewriting system $T_M$, which is a term rewriting system over unary symbols, such that the configuration word of $M$ on input $w$ has at most one successor, and each step of $M$ is one or two rewrite steps. So the unique reduction from the start word $q_0 w \rhd$ is infinite iff $M$ runs forever on $w$. Deciding termination of the term $q_0 w \rhd$ would decide whether $M$ halts on $w$, which is impossible; with $M$ a universal machine, $T_M$ is one fixed system.

**Part 2, by the Post correspondence problem.** An instance of the [Post correspondence problem](/post-correspondence-problem/) is a finite list of pairs $(\alpha_1, \beta_1), \ldots, (\alpha_n, \beta_n)$ of nonempty words over $\{a, b\}$; a solution is a sequence $i_1, \ldots, i_k$ with $k \ge 1$ and $\alpha_{i_1} \cdots \alpha_{i_k} = \beta_{i_1} \cdots \beta_{i_k}$. It is undecidable whether an instance has a solution. Read $a, b$ as unary symbols, and write $w(t)$ for the term that puts the letters of $w$ on top of $t$; for example $ab(t) = a(b(t))$. Let $e$ be a constant, $g$ unary, and $f, h$ ternary. The system $R_P$ has the rules

$$g(x) \to h(x, x, x),$$
$$h(\alpha_i(x), \beta_i(y), z) \to f(x, y, z) \quad \text{and} \quad f(\alpha_i(x), \beta_i(y), z) \to f(x, y, z) \qquad (1 \le i \le n),$$
$$f(e, e, z) \to g(z).$$

The first rule makes three copies of a candidate word. The $h$ and $f$ rules strip the same tile $\alpha_i$ from the first copy and $\beta_i$ from the second; $h$ forces at least one tile. The last rule restarts from the third copy when both copies are used up.

*If $P$ has a solution, $R_P$ does not terminate.* Let $W = \alpha_{i_1} \cdots \alpha_{i_k} = \beta_{i_1} \cdots \beta_{i_k}$. Then
$$g(W(e)) \to h(W(e), W(e), W(e)) \to^{k} f(e, e, W(e)) \to g(W(e)),$$
using the $h$ rule for $i_1$ and the $f$ rule for $i_2, \ldots, i_k$. This is a cycle.

*If $R_P$ does not terminate, $P$ has a solution.* Three facts about $R_P$:

- (a) Every right side has the form $F(\text{variables})$ with $F \in \{f, g, h\}$, and the letters $a, b$ and the constant $e$ are not at the root of any left side. So a rewrite step never happens at a position whose symbol is a letter or $e$, and a term whose root is $f$, $g$ or $h$ keeps a root in $\{f, g, h\}$.
- (b) Hence the maximal prefix of letters of a term never changes, and the part below it either is $e$ or a variable, which do not change, or has a root in $\{f, g, h\}$, which stays there. In particular, if $u \to_{R_P}^* W(e)$ for a word $W$, then $u = W(e)$.
- (c) Take a non-terminating term $t$ of least size, so all its proper subterms terminate. An infinite reduction from $t$ must contain a root step, since otherwise one of its finitely many arguments would have an infinite reduction. After a root step the term is $F(u_1, u_2, u_3)$ or $g(u)$, where each argument is a subterm of a reduct of a proper subterm of $t$, so it terminates, and the same argument gives another root step. So the reduction has infinitely many root steps.

Root steps can only follow the cycle $g \to h \to f \to \cdots \to f \to g$, since the root symbol after each rule is fixed by (a). With infinitely many root steps, some root step $g(u) \to h(u, u, u)$ is followed by a root step with the $h$ rule for some $i_1$, then $f$ rules for $i_2, \ldots, i_k$, then $f(e, e, z) \to g(z)$. The arguments are reducts of $u$, so by (b), stripping $\alpha_{i_1}, \ldots, \alpha_{i_k}$ from the first copy and reaching $e$ means $u \to^* \alpha_{i_1} \cdots \alpha_{i_k}(e)$, so $u = \alpha_{i_1} \cdots \alpha_{i_k}(e)$; the same argument for the second copy gives $u = \beta_{i_1} \cdots \beta_{i_k}(e)$. Since $k \ge 1$, the sequence $i_1, \ldots, i_k$ is a solution.

So $R_P$ terminates iff $P$ has no solution. The map $P \mapsto R_P$ is computable, so a decision procedure for termination would decide the Post correspondence problem. $\blacksquare$

**Example.** For $P = \{(a, baa),\ (ab, aa),\ (bba, bb)\}$, the sequence $3, 2, 3, 1$ is a solution, with $W = bbaabbbaa$, and a program found the cycle from $g(W(e))$ back to itself. For 179 random instances with up to two pairs of words of length at most 3 and no solution of length at most 7, the program explored all reductions from 5368 random terms of depth up to 3 and found the reachable graph finite and acyclic each time, so each of these terms terminates; 2 more terms had too many reducts to explore. For the 21 instances with a solution, the cycle above was found.

## Consequences

- **Termination proofs are incomplete.** Every termination method that can be checked by a program, such as a path order, polynomial interpretations, or [dependency pairs](/dependency-pairs/) with a fixed set of processors, fails on some terminating systems. The methods prove termination of many practical systems, but no method proves all of them.
- **Related properties.** The same encodings show that [weak normalization](/weak-normalization/) and the existence of normal forms are undecidable, and the [confluence decision problem](/confluence-decision-problem/) is undecidable as well.
- **Arithmetical level.** By König's lemma, a term is terminating iff there is a bound on the length of its reductions, so termination of one term is recursively enumerable, while uniform termination quantifies over all terms. Endrullis, Geuvers and Zantema (2009) showed that termination of one term is $\Sigma^0_1$-complete and uniform termination is $\Pi^0_2$-complete, so uniform termination is not even semi-decidable, nor is its complement.

## Tightness

- **One rule is enough.** Dauchet (1992) proved that termination is undecidable for systems with a single rule that is left-linear, non-overlapping and variable-preserving.
- **String rewriting.** Uniform termination is undecidable for finite string rewriting systems too; the proof in Baader and Nipkow, Section 5.1.1, reduces the uniform halting problem of Turing machines, whose undecidability is due to Hooper (1966).
- **Decidable classes.** Termination is decidable for ground systems, whose left and right sides contain no variables (Huet and Lankford, 1978, as surveyed by Dershowitz, 1987). It is also decidable for systems with an explicit bound, such as "does $t$ terminate within $n$ steps", which is a finite search. So the undecidability needs variables in the rules.

## History

Huet and Lankford proved in 1978 that uniform termination of term rewriting systems is undecidable, by reduction from the uniform halting problem of Turing machines (Baader and Nipkow, Section 5.1.1). Dauchet (1992) extended the result to one left-linear rule. Endrullis, Geuvers and Zantema (2009) placed termination and related properties exactly in the arithmetical hierarchy.

## References
