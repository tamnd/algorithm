---
tag: PAQZZA
kind: definition
slug: semi-stable-extension
name: Semi-stable extension
aliases:
- semi-stable semantics
area: information-retrieval-and-ai-reasoning/argumentation-and-belief-revision
level: advanced
summary: A complete extension whose range, the set plus the arguments it attacks, is maximal. It equals stable when a stable extension exists, and still exists when none does.
prereqs: [complete-extension, stable-extension-argumentation, preferred-extension]
see_also: [argument-labelling, argument-acceptance-problem, grounded-extension, preferred-semantics-complexity, admissible-set]
sources:
  - paper: "Martin Caminada, Semi-stable semantics, in Computational Models of Argument (COMMA 2006), Frontiers in Artificial Intelligence and Applications 144, IOS Press, 121 to 130 (2006)"
    locator: the whole paper (the definition by labellings with a minimal set of undec arguments, and the relation to stable and preferred semantics)
  - paper: "Martin W. A. Caminada, Walter A. Carnielli and Paul E. Dunne, Semi-stable semantics, Journal of Logic and Computation 22(5), 1207 to 1254 (2012)"
    locator: the whole paper (equivalent definitions, properties and complexity)
  - paper: "Wolfgang Dvořák and Stefan Woltran, Complexity of semi-stable and stage semantics in argumentation frameworks, Information Processing Letters 110(11), 425 to 430 (2010)"
    locator: the whole paper (sceptical and credulous acceptance)
  - book: isbn:9781848902756
    title: Wolfgang Dvořák and Paul E. Dunne, Computational problems in formal argumentation and their complexity, in Pietro Baroni, Dov Gabbay, Massimiliano Giacomin and Leendert van der Torre (eds), Handbook of Formal Argumentation, volume 1, College Publications (2018)
    locator: Section 3.3, Table 1 (the row for semi-stable semantics)
---

Stable semantics fails on some frameworks: one self-attacking argument that nobody else attacks removes every stable extension. Semi-stable semantics, introduced by Martin Caminada in 2006, repairs this. It keeps the stable extensions when there are any, and otherwise picks the complete extensions that leave as few arguments undecided as possible. On finite frameworks a semi-stable extension always exists. The framework and its notation are on [abstract argumentation framework](/abstract-argumentation-framework/).

## Definition

Let $(A, R)$ be a finite argumentation framework. For $S \subseteq A$, let $S^+$ be the set of the arguments that $S$ attacks. The *range* of $S$ is $S \cup S^+$: the arguments that $S$ either accepts or refutes.

**Definition.** $S$ is a semi-stable extension when $S$ is a [complete extension](/complete-extension/) and no complete extension $T$ has $S \cup S^+ \subsetneq T \cup T^+$.

Equivalent forms (Caminada 2006; Caminada, Carnielli and Dunne 2012):

- **Labellings.** Each complete extension $S$ gives the complete [labelling](/argument-labelling/) with in for $S$, out for $S^+$ and undec for the rest. The semi-stable extensions are the in sets of the complete labellings whose set of undec arguments is minimal under $\subseteq$. This is Caminada's original form.
- **Admissible sets.** One may also take the admissible sets with a maximal range. These are the same sets.

The range is maximized under $\subseteq$, not by size, so two semi-stable extensions can have ranges of different sizes.

**Basic facts for finite frameworks.**

- A semi-stable extension exists, since the set of complete extensions is finite and not empty.
- Every [stable extension](/stable-extension-argumentation/) is semi-stable, because its range is all of $A$.
- If some stable extension exists, the semi-stable extensions are exactly the stable ones, because then the maximal ranges are all equal to $A$.
- Every semi-stable extension is [preferred](/preferred-extension/). Suppose that $S$ is semi-stable and $S \subsetneq T$ for an admissible $T$. Extend $T$ to a preferred extension $P$, which is complete. The range of $P$ contains the range of $S$. It also contains a $t \in T \setminus S$, and $t$ is not in $S^+$, because $P$ is conflict-free. So the range of $P$ is strictly larger, which is impossible.

## Examples and non-examples

Take $A = \{a, b, c, d, e, g\}$ with $a \leftrightarrow b$, $b \to c$, the 3-cycle $c \to d \to e \to c$, and a self-attacking argument $g$. The complete extensions and their ranges, from a check of all 64 subsets:

| complete extension | range | semi-stable |
|---|---|---|
| $\emptyset$ | $\emptyset$ | no |
| $\{a\}$ | $\{a, b\}$ | no |
| $\{b, d\}$ | $\{a, b, c, d, e\}$ | yes |

- There is no stable extension, because nothing attacks $g$.
- The preferred extensions are $\{a\}$ and $\{b, d\}$.
- The only semi-stable extension is $\{b, d\}$. It leaves only $g$ undecided, while $\{a\}$ leaves the whole 3-cycle and $g$ undecided.

So semi-stable semantics is strictly between stable and preferred here. Without $g$, the set $\{b, d\}$ is stable, and it is again the only semi-stable extension.

More cases:

- In the framework with $a \to b \to c \to d \to e$, $e \leftrightarrow f$ and a self-attacking $g$ that attacks $d$, both preferred extensions $\{a, c, e\}$ and $\{a, c, f\}$ have the range $\{a, b, c, d, e, f\}$. Both are semi-stable, and there is no stable extension.
- In a 3-cycle, $\emptyset$ is the only complete extension, so it is the only semi-stable extension.
- In the Nixon framework $a \leftrightarrow b$, the semi-stable extensions are the stable extensions $\{a\}$ and $\{b\}$. The complete extension $\emptyset$ is not semi-stable.

## Related definitions

- **Stage extension.** A conflict-free set with a maximal range. It drops the admissibility condition. When a stable extension exists, the stage extensions are the stable ones too.
- **[Grounded extension](/grounded-extension/).** The complete labelling with a maximal set of undec arguments. Semi-stable is the opposite end: a minimal set of undec arguments.
- **Infinite frameworks.** The existence proof above uses finiteness. For infinite frameworks this page makes no claim.
- **Complexity.** Credulous acceptance is $\Sigma_2^P$-complete, sceptical acceptance is $\Pi_2^P$-complete, and verification is coNP-complete (Dvořák and Woltran 2010; Caminada, Carnielli and Dunne 2012; Dvořák and Dunne, Table 1). Credulous acceptance is harder than under preferred semantics, where it is NP-complete, because a witness must also have a maximal range. See [argument acceptance](/argument-acceptance-problem/) and [complexity of preferred semantics](/preferred-semantics-complexity/).

## References
