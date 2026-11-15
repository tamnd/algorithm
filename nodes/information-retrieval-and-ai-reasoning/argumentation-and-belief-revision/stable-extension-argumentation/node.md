---
tag: GVQ2BD
kind: definition
slug: stable-extension-argumentation
name: Stable extension of an argumentation framework
aliases:
- stable semantics of argumentation
area: information-retrieval-and-ai-reasoning/argumentation-and-belief-revision
level: core
summary: A conflict-free set of arguments that attacks every argument outside it. It may not exist, and when it does it is a preferred extension.
prereqs: [admissible-set]
see_also: [preferred-extension, semi-stable-extension, argument-labelling, argument-acceptance-problem, stable-model-semantics, independent-set, argumentation-sat-encoding]
sources:
  - paper: doi:10.1016/0004-3702(94)00041-X
    title: Phan Minh Dung, On the acceptability of arguments and its fundamental role in nonmonotonic reasoning, logic programming and n-person games, Artificial Intelligence 77(2), 321 to 357 (1995)
    locator: Definition 13, Lemma 14 and Lemma 15 (p. 328), Section 3 (n-person games and stable marriage) and Section 4 (logic programming)
  - paper: "Yannis Dimopoulos and Alberto Torres, Graph theoretical structures in logic programs and default theories, Theoretical Computer Science 170(1-2), 209 to 244 (1996)"
    locator: the whole paper (kernels of directed graphs and the complexity of stable extensions)
  - book: isbn:9781848902756
    title: Wolfgang Dvořák and Paul E. Dunne, Computational problems in formal argumentation and their complexity, in Pietro Baroni, Dov Gabbay, Massimiliano Giacomin and Leendert van der Torre (eds), Handbook of Formal Argumentation, volume 1, College Publications (2018)
    locator: Section 3.3, Table 1 (the row for stable semantics) and Reduction 3.6
---

A stable extension is a set of arguments that is free of internal attacks and that attacks every argument it leaves out. It takes a firm position on every argument: each one is either accepted or refuted. It is the oldest semantics in Dung's paper, and it matches the stable models of logic programs and the kernels of directed graphs. Unlike the other main semantics, it may not exist. The framework and its notation are on [abstract argumentation framework](/abstract-argumentation-framework/).

## Definition

Let $(A, R)$ be an argumentation framework, and let $S^+$ be the set of the arguments that $S$ attacks.

**Definition (Dung 1995, Definition 13).** $S \subseteq A$ is a stable extension when $S$ is conflict-free and $S$ attacks every argument in $A \setminus S$.

Equivalent forms:

- $S^+ = A \setminus S$. Conflict-freeness says $S \cap S^+ = \emptyset$, and the second condition says $A \setminus S \subseteq S^+$.
- The range $S \cup S^+$ is all of $A$, and $S$ is conflict-free.
- $S = \{a \in A : \text{no member of } S \text{ attacks } a\}$ (Lemma 14). This is a fixed-point equation, but the map is antitone, not monotone, so it can have no solution or many.
- In the language of [labellings](/argument-labelling/): a complete labelling with no undec argument.

**Lemma 15.** Every stable extension is a [preferred extension](/preferred-extension/). A stable extension attacks every outside argument, so it defends itself, and no outside argument can be added without a conflict.

## Examples and non-examples

Take $A = \{a, b, c, d, e\}$ with $a \leftrightarrow b$, $b \to c$, and the 3-cycle $c \to d \to e \to c$.

- $\{b, d\}$ is stable: $b$ attacks $a$ and $c$, and $d$ attacks $e$. It is the only stable extension.
- $\{a\}$ is preferred but not stable. It attacks $b$ and nothing else, so $c$, $d$ and $e$ are neither in nor attacked.
- $\{b\}$ is conflict-free and admissible but not stable: it leaves $d$ and $e$ unattacked.

More cases, each checked over all subsets:

- **No stable extension.** A single argument $a$ that attacks itself: $\emptyset$ does not attack $a$, and $\{a\}$ is not conflict-free. A 3-cycle $a \to b \to c \to a$: one argument attacks only one of the other two, and two arguments of the cycle conflict. In general, a framework has no stable extension when it holds an odd cycle in which each argument is attacked only by its predecessor on the cycle.
- **A stable extension that is not the only preferred one.** Let $a \leftrightarrow b$, $b \to c$, and let $c$ attack itself. The preferred extensions are $\{a\}$ and $\{b\}$, but only $\{b\}$ is stable, since only $b$ attacks $c$.
- **Several stable extensions.** In the Nixon framework $a \leftrightarrow b$, both $\{a\}$ and $\{b\}$ are stable. With $k$ separate 2-cycles there are $2^k$ stable extensions.
- **Adding an argument can destroy all stable extensions.** Add a self-attacking argument $g$ to the first framework. Nothing else attacks $g$, so no set is stable any more, while the preferred extensions $\{a\}$ and $\{b, d\}$ stay the same.

## Related definitions

- **Kernels.** A kernel of a directed graph $D$ is an independent set $K$ such that every vertex outside $K$ has an arc into $K$. The stable extensions of $(A, R)$ are the kernels of the graph $(A, R^{-1})$ with all arcs reversed. In an undirected view, a stable extension is an [independent set](/independent-set/) that dominates every outside vertex along the attacks. Dimopoulos and Torres (1996) used this link to get the complexity of stable semantics.
- **Games and matchings.** Dung (1995, Section 3) shows that the stable solutions of von Neumann and Morgenstern for n-person games and the stable marriages of a marriage problem are the stable extensions of suitable frameworks.
- **[Stable models](/stable-model-semantics/).** For the framework that Dung builds from a normal logic program, the stable extensions correspond to the stable models (Section 4).
- **[Semi-stable extension](/semi-stable-extension/).** A complete extension with a maximal range. When a stable extension exists, the semi-stable extensions are exactly the stable ones. When none exists, semi-stable extensions still do.
- **[Preferred extension](/preferred-extension/).** A framework whose preferred and stable extensions coincide is called coherent. Finite frameworks without odd cycles are coherent.
- **Complexity.** Verification is easy (in logspace). Existence, nonempty existence and credulous acceptance are NP-complete, sceptical acceptance is coNP-complete, and deciding whether there is exactly one stable extension is DP-complete (Dvořák and Dunne, Table 1). Sceptical acceptance follows the convention that every argument is accepted when no stable extension exists. See [argument acceptance](/argument-acceptance-problem/).
- **[SAT encoding](/argumentation-sat-encoding/).** With one variable $x_a$ for each argument, the stable extensions are exactly the models of the clauses $\neg x_a \vee \neg x_b$ for each attack $(a, b)$ and $x_a \vee \bigvee_{(b, a) \in R} x_b$ for each argument $a$.

## References
