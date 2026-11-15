---
tag: 76GV5N
kind: definition
slug: grounded-extension
name: Grounded extension
aliases:
- grounded semantics
area: information-retrieval-and-ai-reasoning/argumentation-and-belief-revision
level: core
summary: The least fixed point of the characteristic function of a framework. It is the least complete extension, the set of the arguments that every complete extension accepts.
prereqs: [complete-extension, fixed-point]
see_also: [grounded-extension-algorithm, argument-labelling, preferred-extension, argument-acceptance-problem, well-founded-semantics, knaster-tarski-theorem, horn-sat]
sources:
  - paper: doi:10.1016/0004-3702(94)00041-X
    title: Phan Minh Dung, On the acceptability of arguments and its fundamental role in nonmonotonic reasoning, logic programming and n-person games, Artificial Intelligence 77(2), 321 to 357 (1995)
    locator: Definition 16 (pp. 328 to 329), Lemma 19 and Definition 20 (p. 329), Theorem 25 and Lemma 28 (p. 330), Theorem 30 (p. 331), and Section 4 (logic programming)
  - paper: doi:10.1007/11853886_11
    title: Martin Caminada, On the issue of reinstatement in argumentation, JELIA 2006, Lecture Notes in Computer Science 4160, 111 to 123 (2006)
    locator: the whole paper (the grounded extension as the complete labelling with the fewest in arguments)
  - book: isbn:9781848902756
    title: Wolfgang Dvořák and Paul E. Dunne, Computational problems in formal argumentation and their complexity, in Pietro Baroni, Dov Gabbay, Massimiliano Giacomin and Leendert van der Torre (eds), Handbook of Formal Argumentation, volume 1, College Publications (2018)
    locator: Section 3.3, Table 1 (the row for grounded semantics) and Reduction 3.8 (P-hardness from Horn satisfiability)
---

The grounded extension is the most cautious way to accept arguments in a framework. It contains the arguments that nobody attacks, then the arguments that these defend, and so on, and it never takes a side in a conflict that is not settled this way. It is unique, it always exists, and it can be computed in linear time by the [grounded extension algorithm](/grounded-extension-algorithm/). The framework and its notation are on [abstract argumentation framework](/abstract-argumentation-framework/).

## Definition

Let $(A, R)$ be an argumentation framework. The characteristic function maps a set $S \subseteq A$ to

$$F(S) = \{a \in A : \text{every attacker of } a \text{ is attacked by some member of } S\}$$

(Dung 1995, Definition 16). $F$ is monotone: $S \subseteq T$ implies $F(S) \subseteq F(T)$ (Lemma 19), because a larger set attacks more arguments and so defends more.

**Definition (Definition 20).** The grounded extension of $(A, R)$ is the least [fixed point](/fixed-point/) of $F$.

The subsets of $A$ form a complete lattice under $\subseteq$, so the [Knaster-Tarski theorem](/knaster-tarski-theorem/) gives the least fixed point for every framework, also an infinite one. Three equivalent descriptions hold:

- **The least complete extension (Theorem 25).** The grounded extension is a [complete extension](/complete-extension/), and it is contained in every complete extension. So it is also the intersection of all complete extensions.
- **The limit of the iteration (Lemma 28).** If each argument has finitely many attackers, the grounded extension is $\bigcup_{i \ge 0} F^i(\emptyset)$. For a finite framework with $n$ arguments the chain $\emptyset \subseteq F(\emptyset) \subseteq F^2(\emptyset) \subseteq \cdots$ becomes constant after at most $n$ steps.
- **The grounded labelling.** In terms of [labellings](/argument-labelling/), it is the set of in arguments of the complete labelling with the fewest in arguments, which is also the one with the most undec arguments (Caminada 2006).

$F(\emptyset)$ is the set of the unattacked arguments. If there is none, the grounded extension is empty.

## Examples and non-examples

Take the framework with $a \to b \to c \to d \to e$, the 2-cycle $e \leftrightarrow f$, and an argument $g$ that attacks itself and $d$. The iteration gives

$$F(\emptyset) = \{a\},\quad F(\{a\}) = \{a, c\},\quad F(\{a, c\}) = \{a, c\},$$

so the grounded extension is $G = \{a, c\}$, and it attacks $G^+ = \{b, d\}$. The other complete extensions, $\{a, c, e\}$ and $\{a, c, f\}$, both contain $G$, and neither of them is grounded. They take a side in the 2-cycle, which the grounded extension does not do.

More cases:

- A chain $x_1 \to x_2 \to \cdots \to x_n$: the grounded extension is $\{x_1, x_3, x_5, \ldots\}$, and the iteration adds one argument in each step.
- The Nixon framework $a \leftrightarrow b$, an odd cycle, and a single self-attacking argument: in each case no argument is unattacked, and the grounded extension is $\emptyset$.
- Floating acceptance. Let $a \leftrightarrow b$, let both $a$ and $b$ attack $c$, and let $c$ attack $d$. The preferred extensions are $\{a, d\}$ and $\{b, d\}$, so $d$ is in every preferred extension. But the grounded extension is $\emptyset$: $d$ is defended only after one side of the 2-cycle is chosen. So the grounded extension can be strictly smaller than the intersection of the preferred extensions.
- A finite acyclic framework, or more generally a well-founded one (Definition 29): the grounded extension is the only complete extension, and it is also preferred and stable (Theorem 30).

## Related definitions

- **[Grounded extension algorithm](/grounded-extension-algorithm/).** A queue with one counter for each argument computes $G$ and $G^+$ in $\Theta(n + m)$ time for $n$ arguments and $m$ attacks. The direct iteration of $F$ is quadratic in the worst case.
- **Grounded semantics.** It is a unique-status semantics: there is exactly one extension, so credulous and sceptical acceptance are the same question. That question is P-complete, by a reduction from [Horn satisfiability](/horn-sat/) (Dvořák and Dunne, Table 1 and Reduction 3.8). See [argument acceptance](/argument-acceptance-problem/).
- **[Preferred extension](/preferred-extension/).** Every preferred extension contains $G$, and every argument of $G^+$ is out in it.
- **[Well-founded semantics](/well-founded-semantics/).** For the framework that Dung builds from a normal logic program, the grounded extension corresponds to the well-founded model (Dung 1995, Section 4).
- **Ideal extension.** The largest admissible set inside every preferred extension. It contains $G$. In the floating example it is $\emptyset$, because $\{d\}$ does not defend $d$ against $c$.

## References
