---
tag: ENVVRQ
kind: technique
slug: reduction-strategy
name: Reduction strategy
aliases:
- rewriting strategy
- evaluation strategy
area: automata-and-parsing/term-rewriting
level: core
summary: A rule that chooses which redex to contract at each step.
prereqs: [normal-form, rewrite-step]
see_also: [innermost-reduction, outermost-reduction, weak-normalization, normal-form-computation, orthogonal-rewrite-system, parallel-rewriting, graph-reduction, standardization-theorem]
sources:
  - book: isbn:9780521391153
    title: Terese (Marc Bezem, Jan Willem Klop and Roel de Vrijer, editors), Term Rewriting Systems, Cambridge University Press, 2003
    locator: Chapter 9, Strategies (normalizing, cofinal and perpetual strategies; parallel-outermost, Gross-Knuth and needed reduction for orthogonal systems)
  - paper: doi:10.1007/3-540-08531-9
    title: Michael J. O'Donnell, Computing in Systems Described by Equations, Lecture Notes in Computer Science 58, Springer, 1977
    locator: the chapters on reduction strategies (parallel-outermost and leftmost-outermost normalization for orthogonal systems)
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Section 11.5, Reduction strategies
---

A **reduction strategy** tells a rewriting engine which [redex](/rewrite-step/) to contract next when a term has several. The choice does not matter for the result in a [confluent](/confluence/) and [terminating](/termination/) system, but it decides whether a computation stops at all when the system is only [weakly normalizing](/weak-normalization/), and how many steps it takes when it does. Call-by-value is [innermost reduction](/innermost-reduction/), call-by-name is [outermost reduction](/outermost-reduction/), and lazy evaluation is outermost reduction with sharing.

## In plain words

An expression can contain several places where a rule applies. A strategy is the policy that picks one of them, or several at once, at each step. Different policies can lead to very different runs. One policy may finish in a few steps, another may take many more because it copies a part before working on it, and a third may never finish because it keeps working on a part whose result is thrown away later.

So the strategy is part of the meaning of a program. Languages fix one: some evaluate the arguments of a function before the call, others only when the value is needed. For a given set of rules, the useful questions are whether a strategy always finds the result when one exists, and how much work it does.

## When it applies

- The rules are a [term rewriting system](/term-rewriting-system/) used to compute: a term is evaluated by rewriting until a [normal form](/normal-form/) is reached. See [normal form computation](/normal-form-computation/).
- A term can have several redexes. If the system is confluent, all normal forms reached agree, so the strategy can only change termination and cost, not the answer. If it is not confluent, the strategy also selects which answer is computed.
- The interesting guarantees need structure. For [orthogonal](/orthogonal-rewrite-system/) systems, several strategies are proved to be **normalizing**: they reach the normal form of every term that has one.

## The template

We use the notation of the term rewriting pages: terms $T(\Sigma, V)$, positions with root $\varepsilon$, $t|_p$ and $t[s]_p$, substitutions $\sigma$, rules $l \to r$, and $\to_R^*$ for the reflexive transitive closure.

A **one-step strategy** maps each term $t$ that is not a normal form to one redex position of $t$. A **many-step strategy** maps it to a nonempty set of redex positions, contracted together in one [parallel](/parallel-rewriting/) or multi-step. The evaluator is the same for all strategies; the strategy is the hole SELECT, and for systems with overlapping rules a second hole chooses the rule at a position.

```pseudo id=main
EVALUATE(t, R)                             ▷ SELECT is the strategy
L1  while t has a redex do
L2      P ← SELECT(t)                       ▷ nonempty set of redex positions, pairwise parallel
L3      for each p in P do
L4          choose a rule l → r in R and σ with t|_p = lσ
L5          t ← t[rσ]_p
L6  return t                                ▷ a normal form
```

Because the positions in $P$ are pairwise parallel (no one is a prefix of another), the replacements in line L5 do not interfere, and their order does not matter. A one-step strategy returns a single position. The properties used to compare strategies:

- **Normalizing**: for each term that has a normal form, EVALUATE stops.
- **Perpetual**: for each term with an infinite reduction, EVALUATE does not stop. A perpetual strategy finds the longest computations; it is a tool for termination proofs.
- **Cofinal**: for each term $t$ and each $s$ with $t \to_R^* s$, the run of EVALUATE from $t$ reaches a term $u$ with $s \to_R^* u$. A cofinal strategy is normalizing for a confluent system.

**Why the choice matters.** The run stops only when no redex is left, so a strategy fails to normalize exactly when it keeps choosing redexes inside a part of the term that a later step would erase, or that has no normal form. It costs extra steps exactly when it contracts a redex that a later step copies before it is contracted, so the same work is done twice, or contracts a redex that a later step erases.

## Classic examples

**Leftmost innermost (call by value).** Pick the leftmost redex that contains no other redex. Each step needs only the arguments to be in normal form, which matches strict function calls. It is not normalizing: with $f(x) \to b$ and $a \to a$, the term $f(a)$ has the normal form $b$, but innermost reduction loops on $a \to a$. See [innermost reduction](/innermost-reduction/).

**Leftmost outermost (call by name).** Pick the leftmost redex that is not inside another redex. With $f(x) \to b$ and $a \to a$, it finds $f(a) \to b$ in one step. For left-normal orthogonal systems, which include [combinatory logic](/combinatory-logic/), it is normalizing, and for the [lambda calculus](/lambda-calculus/) the same strategy is normalizing by the [standardization theorem](/standardization-theorem/). In general orthogonal systems it is not: with $f(x, b) \to d$, $a \to a$, $c \to b$, the term $f(a, c)$ is not a redex, its leftmost outermost redex is $a$, and the strategy loops on $a \to a$, while $f(a, c) \to f(a, b) \to d$. See [outermost reduction](/outermost-reduction/).

**Parallel outermost.** Contract all outermost redexes at once. On $f(a, c)$ above it gives $f(a, c) \to f(a, b) \to d$, since the step on $a$ gives $a$ again and the step on $c$ gives $b$. It is normalizing for all orthogonal systems (O'Donnell, 1977).

**Gross-Knuth (full substitution).** Contract all redexes of the term, by a complete development of the set of all its redexes. It is cofinal, and so normalizing, for orthogonal systems.

**Needed redexes.** In an orthogonal system, a redex is **needed** if every reduction of the term to normal form contracts it or one of its residuals. Every term that is not a normal form has a needed redex, and contracting needed redexes is normalizing; the leftmost outermost redex is needed in left-normal systems. Whether a redex is needed is undecidable in general, and decidable in the strongly sequential systems, where an automaton on the left sides finds a needed redex.

**Cost: copying versus erasing.** With $f(x) \to g(x, x)$ and $a \to b$, innermost reduction takes 2 steps from $f(a)$ ($f(a) \to f(b) \to g(b, b)$), and outermost reduction takes 3 ($f(a) \to g(a, a) \to g(b, a) \to g(b, b)$). If $a$ needs $k$ steps instead of one, the counts are $k + 1$ and $2k + 1$, and nested copying makes the gap exponential. With an erasing rule $f(x) \to c$ the comparison turns around: outermost takes 1 step and innermost $k + 1$. [Graph reduction](/graph-reduction/) and [term graph rewriting](/term-graph-rewriting/) get the best of both: outermost order, with the copies of $x$ shared so that $a$ is reduced at most once. This is lazy evaluation.

## Variations

- **Context-sensitive rewriting.** For each symbol, allow steps only in some argument positions. With $\mathit{if}$ allowed to rewrite only its first argument, the two branches are left alone until the condition is a value.
- **Strategy annotations and strategy languages.** Systems such as Maude and Stratego let the user attach an evaluation order to each symbol, or write the strategy as a program built from combinators such as sequence, choice and "apply everywhere, top-down".
- **Innermost termination.** A system can terminate under the innermost strategy without being terminating. The [dependency pair](/dependency-pairs/) method has a special form for innermost termination, which is weaker and easier to prove.
- **Narrowing strategies.** For [narrowing](/narrowing/), which also instantiates variables, needed narrowing chooses steps in the same spirit as needed reduction.
- **Non-deterministic search.** For a non-confluent system, EVALUATE with a fixed strategy finds one normal form. Finding all normal forms, or a normal form when the strategy loops, needs a search over the reduction graph, such as the breadth-first search on the [weak normalization](/weak-normalization/) page.

## Pitfalls

- **Assuming innermost always works for terminating programs.** It does for terminating systems, since every strategy stops there. It does not for weakly normalizing ones: an argument that is erased later can loop.
- **Assuming outermost is always normalizing.** Leftmost outermost fails on the orthogonal example $f(x, b) \to d$, $a \to a$, $c \to b$. Parallel outermost or needed reduction is needed for general orthogonal systems.
- **Ignoring non-orthogonal systems.** Without orthogonality, no strategy defined by positions alone can be normalizing in general, since the rule choice in line L4 also matters: in $\{a \to b,\ a \to a\}$ the strategy must also choose the rule.
- **Counting steps without sharing.** Outermost reduction can repeat work on copied arguments. Results that bound the number of steps of lazy evaluation assume shared subterms.
- **Parallel steps on overlapping positions.** A many-step strategy must choose pairwise parallel positions, or contract nested redexes as a development; replacing an outer redex first changes the positions inside it.

## Exercises

1. Show that every strategy is normalizing for a terminating system, and that for $\{f(x) \to b,\ a \to a\}$ no strategy is both normalizing and perpetual.
2. Show that rightmost outermost reduction normalizes $f(a, c)$ under $f(x, b) \to d$, $a \to a$, $c \to b$, and give an orthogonal system and a term on which rightmost outermost reduction loops although the term has a normal form.
3. Give a system where innermost reduction from some term takes exponentially fewer steps than outermost reduction without sharing.
4. Prove that a cofinal strategy is normalizing for a confluent system.
5. Show that in $\{f(x) \to b,\ a \to a\}$ the redex $a$ in $f(a)$ is not needed, and that the root redex is.

## References
