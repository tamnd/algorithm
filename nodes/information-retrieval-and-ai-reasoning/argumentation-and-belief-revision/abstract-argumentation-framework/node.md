---
tag: ASBT6S
kind: model
slug: abstract-argumentation-framework
name: Abstract argumentation framework
aliases:
- Dung argumentation framework
- argumentation framework
area: information-retrieval-and-ai-reasoning/argumentation-and-belief-revision
level: core
summary: A set of arguments with an attack relation, as in Dung (1995). A semantics picks the sets of arguments that can be accepted together, using only the attack graph.
prereqs: [directed-graph]
see_also: [admissible-set, grounded-extension, preferred-extension, stable-extension-argumentation, argument-labelling, argument-acceptance-problem, stable-model-semantics, aspic-plus]
sources:
  - paper: doi:10.1016/0004-3702(94)00041-X
    title: Phan Minh Dung, On the acceptability of arguments and its fundamental role in nonmonotonic reasoning, logic programming and n-person games, Artificial Intelligence 77(2), 321 to 357 (1995)
    locator: Section 2 (Definition 2 to Theorem 30, pp. 326 to 331), Section 3 (n-person games and stable marriage) and Section 4 (logic programming)
  - paper: "Pietro Baroni, Martin Caminada and Massimiliano Giacomin, An introduction to argumentation semantics, The Knowledge Engineering Review 26(4), 365 to 410 (2011)"
    locator: the whole paper (extension-based and labelling-based semantics)
  - book: isbn:9781848902756
    title: Wolfgang Dvořák and Paul E. Dunne, Computational problems in formal argumentation and their complexity, in Pietro Baroni, Dov Gabbay, Massimiliano Giacomin and Leendert van der Torre (eds), Handbook of Formal Argumentation, volume 1, College Publications (2018)
    locator: Section 3.2 (the reasoning problems), Section 3.3 with Table 1 (their complexity) and Section 3.4 (tractable classes of frameworks)
---

An abstract argumentation framework is a directed graph whose nodes are arguments and whose arcs are attacks. Phan Minh Dung introduced it in 1995. The arguments have no inner structure: a semantics decides which sets of arguments can be accepted together by looking only at who attacks whom. This page fixes the model, the notation and the questions that are asked in it. Each semantics has its own page, and the complexity of the questions is on [argument acceptance](/argument-acceptance-problem/).

## The machine

**Definition (Dung 1995, Definition 2).** An argumentation framework is a pair $F = (A, R)$, where $A$ is a set of arguments and $R \subseteq A \times A$ is the attack relation. $(a, b) \in R$ means that $a$ attacks $b$. On this site $A$ is finite unless a page says otherwise. Self-attacks $(a, a)$ are allowed.

For a set $S \subseteq A$ and an argument $b$:

- $S$ attacks $b$ when some $a \in S$ attacks $b$. The set of the arguments that $S$ attacks is $S^+$.
- $S$ is *conflict-free* when no member of $S$ attacks a member of $S$.
- $S$ *defends* $a$ (Dung says: $a$ is acceptable with respect to $S$) when $S$ attacks every attacker of $a$.
- The *characteristic function* is $F(S) = \{a \in A : S \text{ defends } a\}$ (Dung 1995, Definition 16).
- The *range* of $S$ is $S \cup S^+$.

A *semantics* $\sigma$ maps each framework to a set $\sigma(F)$ of subsets of $A$, the $\sigma$-extensions. The standard ones are defined on their own pages:

| semantics | an extension $S$ is | page |
|---|---|---|
| conflict-free | a set with no attack inside it | [admissible set](/admissible-set/) |
| admissible | conflict-free and $S \subseteq F(S)$ | [admissible set](/admissible-set/) |
| complete | conflict-free and $S = F(S)$ | [complete extension](/complete-extension/) |
| grounded | the least fixed point of $F$ | [grounded extension](/grounded-extension/) |
| preferred | a maximal admissible set | [preferred extension](/preferred-extension/) |
| stable | conflict-free with $S^+ = A \setminus S$ | [stable extension](/stable-extension-argumentation/) |
| semi-stable | a complete extension with a maximal range | [semi-stable extension](/semi-stable-extension/) |

The same semantics can be given by [labellings](/argument-labelling/), which map each argument to in, out or undec.

**Example.** Take $A = \{a, b, c, d, e\}$ with $a \leftrightarrow b$, $b \to c$, and the 3-cycle $c \to d \to e \to c$. The extensions, found by a check of all 32 subsets, are:

| semantics | extensions |
|---|---|
| admissible | $\emptyset$, $\{a\}$, $\{b\}$, $\{b, d\}$ |
| complete | $\emptyset$, $\{a\}$, $\{b, d\}$ |
| grounded | $\emptyset$ |
| preferred | $\{a\}$, $\{b, d\}$ |
| stable | $\{b, d\}$ |
| semi-stable | $\{b, d\}$ |

$\{a\}$ defends itself against $b$ but says nothing about the 3-cycle, so it is preferred and not stable. $\{b, d\}$ attacks $a$, $c$ and $e$, so it is stable. $\{b\}$ is admissible, but it defends $d$ (the only attacker of $d$ is $c$, and $b$ attacks $c$), so it is not complete. Nothing is unattacked, so the grounded extension is empty.

## What it counts

The input is the whole framework, with $n = |A|$ arguments and $m = |R|$ attacks, stored as [adjacency lists](/adjacency-list/) of size $\Theta(n + m)$. Bounds are given in $n$ and $m$, so they are combined complexity in the sense of the reasoning pages: nothing is fixed. For a semantics $\sigma$, the standard questions are (Dvořák and Dunne, Section 3.2):

- **Verification.** Is a given set $S$ a $\sigma$-extension?
- **Credulous acceptance.** Is a given argument in some $\sigma$-extension?
- **Sceptical acceptance.** Is a given argument in every $\sigma$-extension?
- **Existence.** Does a $\sigma$-extension exist? And does a nonempty one exist?
- **Uniqueness.** Is there exactly one $\sigma$-extension?
- **Enumeration.** List all $\sigma$-extensions.

The two acceptance questions are the [argument acceptance problem](/argument-acceptance-problem/), which has a table of the known classes. On a [word RAM](/word-ram/), the operations $S^+$, $F(S)$, the conflict-free test and the range each take $\Theta(n + m)$ time.

## Relation to other models

- **Directed graphs.** A framework is just a [directed graph](/directed-graph/). A stable extension is a set of nodes that is independent (no arc inside it) and that reaches each outside node by one arc. This is a kernel of the graph with all arcs reversed. Stable extensions are therefore [independent sets](/independent-set/) that are also [dominating sets](/dominating-set/) in the direction of the attacks.
- **Games.** Dung (1995, Section 3) shows that the stable solutions of von Neumann and Morgenstern for n-person games, and the solutions of the stable marriage problem, are stable extensions of suitable frameworks. With moves from an argument to its attackers, the grounded labelling is the win, loss and draw labelling of [retrograde analysis](/retrograde-analysis/).
- **Logic programs.** Dung (1995, Section 4) builds a framework from a normal logic program. Its stable extensions correspond to the [stable models](/stable-model-semantics/) of the program, and its grounded extension to the [well-founded model](/well-founded-semantics/).
- **Structured argumentation.** [ASPIC+](/aspic-plus/), [assumption-based argumentation](/assumption-based-argumentation/), [value-based argumentation](/value-based-argumentation/) and [defeasible logic programming](/defeasible-logic-programming/) build arguments from rules and then compute the attacks. The abstract framework is the layer that the semantics work on.
- **SAT.** Conflict-freeness, admissibility and stability are sets of clauses over one variable for each argument, so a [SAT](/sat/) solver can enumerate extensions. See the [argumentation SAT encoding](/argumentation-sat-encoding/).

## Known results in the model

All results are for finite frameworks unless stated. The numbers refer to Dung (1995).

- **Fundamental Lemma (Lemma 10).** If $S$ is admissible and $S$ defends $a$ and $a'$, then $S \cup \{a\}$ is admissible and still defends $a'$.
- **Preferred extensions exist (Theorem 11, Corollary 12).** Each admissible set is contained in a preferred extension. Since $\emptyset$ is admissible, every framework, also an infinite one, has a preferred extension.
- **Stable extensions may not exist.** A single self-attacking argument, or a 3-cycle, has none. Every stable extension is preferred (Lemma 15), and the converse fails, as the example shows.
- **Fixed points (Lemma 19, Theorem 25).** $F$ is monotone. The grounded extension is its least fixed point and the least complete extension. Every preferred extension is complete, and the complete extensions form a complete semilattice.
- **Iteration (Lemma 28).** If each argument has finitely many attackers, the grounded extension is the union of $F^i(\emptyset)$ over $i \ge 0$. The [linear-time algorithm](/grounded-extension-algorithm/) computes it for finite frameworks.
- **Well-founded frameworks (Definition 29, Theorem 30).** If there is no infinite sequence $a_0, a_1, \ldots$ with $a_{i+1}$ attacking $a_i$ for all $i$, then there is exactly one complete extension, and it is grounded, preferred and stable. Every finite acyclic framework is of this kind.
- **Chain of semantics.** For finite frameworks, every stable extension is semi-stable, every semi-stable extension is preferred, every preferred extension is complete, and every complete extension is admissible.
- **Complexity.** Grounded acceptance is P-complete, credulous acceptance under preferred semantics is NP-complete, and sceptical acceptance under preferred semantics is $\Pi_2^P$-complete. The full table is on [argument acceptance](/argument-acceptance-problem/), and the proofs for preferred semantics are on [complexity of preferred semantics](/preferred-semantics-complexity/).
- **Tractable classes.** On acyclic, bipartite and even-cycle-free frameworks, the acceptance problems for the grounded, admissible, complete, preferred, stable and semi-stable semantics are in polynomial time. On symmetric frameworks this holds for the grounded, admissible, complete and preferred semantics (Dvořák and Dunne, Section 3.4).

## References
