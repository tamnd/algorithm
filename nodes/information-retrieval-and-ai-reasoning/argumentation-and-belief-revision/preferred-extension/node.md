---
tag: MRM91K
kind: definition
slug: preferred-extension
name: Preferred extension
aliases:
- preferred semantics
area: information-retrieval-and-ai-reasoning/argumentation-and-belief-revision
level: core
summary: An admissible set of arguments that is maximal under set inclusion. Every framework has one, and each preferred extension is complete.
prereqs: [admissible-set, complete-extension]
see_also: [stable-extension-argumentation, semi-stable-extension, grounded-extension, argument-labelling, argument-acceptance-problem, preferred-semantics-complexity, argumentation-sat-encoding]
sources:
  - paper: doi:10.1016/0004-3702(94)00041-X
    title: Phan Minh Dung, On the acceptability of arguments and its fundamental role in nonmonotonic reasoning, logic programming and n-person games, Artificial Intelligence 77(2), 321 to 357 (1995)
    locator: Definition 7, Theorem 11 and Corollary 12 (p. 327), Lemma 15 (p. 328) and Theorem 25 (p. 330)
  - paper: doi:10.1016/S0004-3702(02)00261-8
    title: Paul E. Dunne and Trevor J. M. Bench-Capon, Coherence in finite argument systems, Artificial Intelligence 141(1-2), 187 to 203 (2002)
    locator: the whole paper (coherence, and sceptical acceptance under preferred semantics)
  - book: isbn:9781848902756
    title: Wolfgang Dvořák and Paul E. Dunne, Computational problems in formal argumentation and their complexity, in Pietro Baroni, Dov Gabbay, Massimiliano Giacomin and Leendert van der Torre (eds), Handbook of Formal Argumentation, volume 1, College Publications (2018)
    locator: Section 3.3, Table 1 (the row for preferred semantics) and Section 3.4 (odd-cycle-free frameworks)
---

A preferred extension is a largest position that a rational agent can defend: an [admissible set](/admissible-set/) to which no argument can be added without losing admissibility. Dung proposed it in 1995 as the credulous semantics of argumentation. A framework can have several preferred extensions, one for each way to resolve its conflicts, and it always has at least one. The framework and its notation are on [abstract argumentation framework](/abstract-argumentation-framework/).

## Definition

Let $(A, R)$ be an argumentation framework.

**Definition (Dung 1995, Definition 7).** A preferred extension of $(A, R)$ is an admissible set $S$ such that no admissible set $T$ satisfies $S \subsetneq T$.

**Existence (Theorem 11, Corollary 12).** Each admissible set is contained in a preferred extension. Since $\emptyset$ is admissible, every framework has at least one preferred extension. For an infinite framework this uses Zorn's lemma: the union of a chain of admissible sets is admissible.

**Completeness (Theorem 25).** Every preferred extension is a [complete extension](/complete-extension/). So the preferred extensions are also the maximal complete extensions.

It is not enough to try one new argument at a time. In the 4-cycle $a \to d \to b \to c \to a$, the empty set is admissible and no single argument is, but $\{a, b\}$ and $\{c, d\}$ are, so $\emptyset$ is not preferred. So checking that a given set is preferred is a hard problem, unlike checking that it is admissible.

## Examples and non-examples

Take $A = \{a, b, c, d, e\}$ with $a \leftrightarrow b$, $b \to c$, and the 3-cycle $c \to d \to e \to c$. The admissible sets are $\emptyset$, $\{a\}$, $\{b\}$ and $\{b, d\}$. The preferred extensions are the maximal ones:

$$\{a\},\qquad \{b, d\}.$$

- $\{b, d\}$ attacks every other argument, so it is also [stable](/stable-extension-argumentation/).
- $\{a\}$ is preferred but not stable. It beats $b$, but then it cannot do anything about the 3-cycle: adding $c$, $d$ or $e$ gives a set that does not defend the new member.
- $\{b\}$ is admissible but not preferred, because $\{b, d\}$ is admissible and larger.

More cases:

- In the framework with $a \to b \to c \to d \to e$, $e \leftrightarrow f$ and a self-attacking $g$ that attacks $d$, the preferred extensions are $\{a, c, e\}$ and $\{a, c, f\}$. There is no stable extension, because nothing attacks $g$.
- In the Nixon framework $a \leftrightarrow b$, the preferred extensions are $\{a\}$ and $\{b\}$. With $k$ separate 2-cycles there are $2^k$ of them.
- In a 3-cycle, the only preferred extension is $\emptyset$. A preferred extension can be empty, even when the framework is not.
- Floating acceptance. Let $a \leftrightarrow b$, let both attack $c$, and let $c$ attack $d$. The preferred extensions are $\{a, d\}$ and $\{b, d\}$. So $d$ is sceptically accepted under preferred semantics, while the [grounded extension](/grounded-extension/) is $\emptyset$.

## Related definitions

- **[Stable extension](/stable-extension-argumentation/).** Every stable extension is preferred (Lemma 15). The converse fails, as $\{a\}$ above shows. A framework is *coherent* when its preferred and stable extensions coincide. A finite framework with no cycle of odd length is coherent (Dung 1995; see Dvořák and Dunne, Section 3.4).
- **[Semi-stable extension](/semi-stable-extension/).** A complete extension with a maximal range. Every semi-stable extension is preferred, and in the first example only $\{b, d\}$ is semi-stable.
- **[Grounded extension](/grounded-extension/).** It is contained in every preferred extension, and it can be strictly smaller than their intersection, as the floating example shows.
- **[Preferred labelling](/argument-labelling/).** A complete labelling with a maximal set of in arguments. The same labellings have a maximal set of out arguments.
- **Complexity.** Credulous acceptance is NP-complete, sceptical acceptance is $\Pi_2^P$-complete, and verification is coNP-complete (Dvořák and Dunne, Table 1). The statements and proofs are on [complexity of preferred semantics](/preferred-semantics-complexity/). Credulous acceptance under preferred semantics is the same question as under admissible semantics, because each admissible set lies inside a preferred extension.
- **Computation.** Solvers encode admissibility in SAT and search for maximal models, see the [argumentation SAT encoding](/argumentation-sat-encoding/). For sceptical acceptance they need a sequence of SAT calls, which matches the $\Pi_2^P$ bound.

## References
