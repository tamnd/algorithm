---
tag: 550QCQ
kind: problem
slug: argument-acceptance-problem
name: Credulous and skeptical acceptance
aliases:
- argument acceptance problem
area: information-retrieval-and-ai-reasoning/argumentation-and-belief-revision
level: core
summary: Given a framework, an argument and a semantics, decide whether the argument is in some extension (credulous) or in every extension (sceptical).
prereqs: [grounded-extension, preferred-extension, stable-extension-argumentation]
see_also: [preferred-semantics-complexity, grounded-extension-algorithm, semi-stable-extension, complete-extension, argumentation-sat-encoding, polynomial-hierarchy, np-complete, horn-sat]
sources:
  - book: isbn:9781848902756
    title: Wolfgang Dvořák and Paul E. Dunne, Computational problems in formal argumentation and their complexity, in Pietro Baroni, Dov Gabbay, Massimiliano Giacomin and Leendert van der Torre (eds), Handbook of Formal Argumentation, volume 1, College Publications (2018)
    locator: Section 3.2 (the reasoning problems), Section 3.3 with Table 1 and Reductions 3.6 to 3.8, and Section 3.4 (tractable classes)
  - paper: "Yannis Dimopoulos and Alberto Torres, Graph theoretical structures in logic programs and default theories, Theoretical Computer Science 170(1-2), 209 to 244 (1996)"
    locator: the whole paper (NP-completeness for stable, admissible and preferred semantics)
  - paper: doi:10.1016/S0004-3702(02)00261-8
    title: Paul E. Dunne and Trevor J. M. Bench-Capon, Coherence in finite argument systems, Artificial Intelligence 141(1-2), 187 to 203 (2002)
    locator: the whole paper (sceptical acceptance under preferred semantics is Pi2P-complete)
  - paper: "Sylvie Coste-Marquis, Caroline Devred and Pierre Marquis, Symmetric argumentation frameworks, ECSQARU 2005, Lecture Notes in Computer Science 3571, 317 to 328 (2005)"
    locator: the whole paper (complete and naive semantics, and symmetric frameworks)
  - paper: "Wolfgang Dvořák and Stefan Woltran, Complexity of semi-stable and stage semantics in argumentation frameworks, Information Processing Letters 110(11), 425 to 430 (2010)"
    locator: the whole paper (semi-stable and stage semantics)
  - paper: "Paul E. Dunne, The computational complexity of ideal semantics, Artificial Intelligence 173(18), 1559 to 1591 (2009)"
    locator: the whole paper (ideal semantics)
  - paper: doi:10.1016/0004-3702(94)00041-X
    title: Phan Minh Dung, On the acceptability of arguments and its fundamental role in nonmonotonic reasoning, logic programming and n-person games, Artificial Intelligence 77(2), 321 to 357 (1995)
    locator: Section 2 (the semantics)
---

The acceptance problem is the main reasoning task of abstract argumentation. A semantics can give a framework several extensions, so "is this argument accepted?" has two readings: it is accepted by some reasonable position (credulous), or by all of them (sceptical). The answer depends on the semantics, and so does the difficulty: the problem is solvable in linear time for grounded semantics, NP-complete for credulous preferred acceptance, and complete for the second level of the [polynomial hierarchy](/polynomial-hierarchy/) for sceptical preferred acceptance. The semantics are defined on [abstract argumentation framework](/abstract-argumentation-framework/) and the pages it links.

## In plain words

You are given a set of arguments and a list of who attacks whom. A semantics is a rule that says which groups of arguments may be accepted together. Often several groups qualify, each one a different way to settle the conflicts. Now pick one argument. The credulous question is whether at least one of the groups contains it. The sceptical question is whether every group contains it.

For the most cautious semantics there is only one group, it can be found fast, and the two questions are the same. For the others the groups can be many, and the questions are as hard as solving logic puzzles, or harder. The sceptical question for preferred semantics needs, in the worst case, a search inside a search.

## Definition

The input is a finite argumentation framework $F = (A, R)$ with $n = |A|$ arguments and $m = |R|$ attacks, and an argument $a \in A$. The semantics $\sigma$ is fixed, and $\sigma(F)$ is the set of the $\sigma$-extensions of $F$.

- **Credulous acceptance** $\mathrm{Cred}_\sigma$: is there an $S \in \sigma(F)$ with $a \in S$?
- **Sceptical acceptance** $\mathrm{Skept}_\sigma$: is $a \in S$ for every $S \in \sigma(F)$?

If $\sigma(F)$ is empty, every argument is sceptically accepted and none is credulously accepted. Among the semantics below, only stable semantics can have no extension. The whole framework is the input, so all bounds are combined complexity in $n + m$.

## Variants

The same table of results covers four related questions (Dvořák and Dunne, Section 3.2):

- **Verification** $\mathrm{Ver}_\sigma$: given $S \subseteq A$, is $S \in \sigma(F)$?
- **Existence** $\mathrm{Exists}_\sigma$: is $\sigma(F)$ nonempty?
- **Nonempty existence** $\mathrm{Exists}^{\neg\emptyset}_\sigma$: is there a nonempty $S \in \sigma(F)$?
- **Uniqueness** $\mathrm{Unique}_\sigma$: does $\sigma(F)$ have exactly one member?

Other variants are enumeration of all extensions, counting them, and acceptance with a set of query arguments instead of one.

## Examples

- **Nixon.** $a \leftrightarrow b$. Preferred and stable extensions: $\{a\}$ and $\{b\}$. So $a$ is credulously but not sceptically accepted under both. The grounded extension is $\emptyset$, so $a$ is not accepted under grounded semantics.
- **Floating acceptance.** $a \leftrightarrow b$, both attack $c$, and $c$ attacks $d$. Preferred: $\{a, d\}$ and $\{b, d\}$. So $d$ is sceptically accepted under preferred semantics, but not under grounded semantics, whose extension is $\emptyset$. Sceptical preferred acceptance can accept more than grounded semantics.
- **Semantics disagree.** $a \leftrightarrow b$, $b \to c$, the 3-cycle $c \to d \to e \to c$, and a self-attacking $g$. Preferred: $\{a\}$ and $\{b, d\}$. Semi-stable: $\{b, d\}$ only. Stable: none. So $b$ is credulously but not sceptically accepted under preferred semantics, sceptically accepted under semi-stable semantics, and, by the convention for an empty $\sigma(F)$, sceptically accepted under stable semantics, like every other argument.

## Known algorithms

- **Grounded semantics.** The [grounded extension algorithm](/grounded-extension-algorithm/) computes the grounded extension in $\Theta(n + m)$ time. This answers both acceptance questions at once.
- **Brute force.** Try all $2^n$ subsets and test each in $O(n + m)$ time. For maximality conditions, compare the qualifying sets. This is what the test helper `af.py` of these pages does on at most 10 arguments.
- **SAT for the first level.** Credulous acceptance under admissible, complete, preferred and stable semantics, and sceptical acceptance under stable semantics, are one call to a [SAT](/sat/) solver on the [argumentation SAT encoding](/argumentation-sat-encoding/) with the query argument forced in or out.
- **Iterated SAT for the second level.** Sceptical preferred and the semi-stable and stage problems need a search for a maximal extension that avoids the query, and a check of maximality. Solvers do this with a loop of SAT calls, or with an answer set solver that handles the second level directly.
- **Labelling search.** Backtracking over in, out and undec labels with propagation of the local rules of [labellings](/argument-labelling/).

## Bounds

The known classes, from Table 1 of Dvořák and Dunne. "c" means complete, "trivial" means that the answer is the same for every input or is read off at once, and L is [logspace](/logspace/).

| semantics $\sigma$ | $\mathrm{Cred}_\sigma$ | $\mathrm{Skept}_\sigma$ | $\mathrm{Ver}_\sigma$ | $\mathrm{Exists}_\sigma$ | $\mathrm{Exists}^{\neg\emptyset}_\sigma$ | $\mathrm{Unique}_\sigma$ |
|---|---|---|---|---|---|---|
| conflict-free | in L | trivial | in L | trivial | in L | in L |
| naive | in L | in L | in L | trivial | in L | in L |
| [grounded](/grounded-extension/) | P-c | P-c | P-c | trivial | in L | trivial |
| [stable](/stable-extension-argumentation/) | NP-c | coNP-c | in L | NP-c | NP-c | DP-c |
| [admissible](/admissible-set/) | NP-c | trivial | in L | trivial | NP-c | coNP-c |
| [complete](/complete-extension/) | NP-c | P-c | in L | trivial | NP-c | coNP-c |
| ideal | $\Theta_2^P$-c | $\Theta_2^P$-c | $\Theta_2^P$-c | trivial | $\Theta_2^P$-c | trivial |
| [preferred](/preferred-extension/) | NP-c | $\Pi_2^P$-c | coNP-c | trivial | NP-c | coNP-c |
| [semi-stable](/semi-stable-extension/) | $\Sigma_2^P$-c | $\Pi_2^P$-c | coNP-c | trivial | NP-c | in $\Theta_2^P$ |
| stage | $\Sigma_2^P$-c | $\Pi_2^P$-c | coNP-c | trivial | in L | in $\Theta_2^P$ |

Notes on the table:

- Credulous acceptance is the same problem for admissible, complete and preferred semantics, because every admissible set lies in a preferred extension, which is complete.
- Sceptical acceptance under complete semantics is membership in the grounded extension, because the grounded extension is the least complete extension.
- Sceptical acceptance under admissible semantics is trivial: $\emptyset$ is admissible, so no argument is in every admissible set.
- Dvořák and Dunne credit the NP and coNP results for stable, admissible and preferred semantics to Dimopoulos and Torres (1996), the $\Pi_2^P$-completeness of sceptical preferred acceptance to Dunne and Bench-Capon (2002), complete and naive semantics to Coste-Marquis, Devred and Marquis (2005), semi-stable and stage semantics to Dvořák and Woltran (2010) and Caminada, Carnielli and Dunne (2012), and ideal semantics to Dunne (2009).
- On restricted classes the picture changes. On acyclic, bipartite and even-cycle-free frameworks, the problems for grounded, admissible, complete, preferred, stable and semi-stable semantics are in polynomial time. On frameworks without odd cycles, preferred and stable semantics coincide, so sceptical preferred acceptance falls to coNP-complete (Dvořák and Dunne, Section 3.4).

## Reductions

- **SAT to credulous acceptance (Reduction 3.6).** For a CNF formula $\varphi$ with clause set $C$ over variables $Y$, build arguments $\{\varphi\} \cup C \cup Y \cup \bar{Y}$. Each clause attacks $\varphi$, each literal attacks the clauses that contain it, and $y \leftrightarrow \bar{y}$ for each variable. Then $\varphi$ is credulously accepted under admissible, complete, preferred and stable semantics exactly when the formula is satisfiable. This gives NP-hardness. A new argument $\bar\varphi$ attacked only by $\varphi$ is then sceptically accepted under stable or preferred semantics exactly when the formula is unsatisfiable, which gives coNP-hardness.
- **QBF to sceptical preferred acceptance (Reduction 3.7).** A version of the construction with a self-attacking argument $\bar\varphi$ that attacks the literals of the existential variables reduces the truth of $\forall Y \exists Z\, \varphi$ to sceptical acceptance of $\varphi$. The full statement and proof are on [complexity of preferred semantics](/preferred-semantics-complexity/).
- **Horn-SAT to grounded acceptance (Reduction 3.8).** One argument for each Horn rule and a self-attacking argument for each atom simulate [Horn satisfiability](/horn-sat/), which is P-complete. So grounded acceptance is P-hard, and a fast parallel algorithm is unlikely.

## Applications

- **Reasoning back-ends.** Structured formalisms such as [ASPIC+](/aspic-plus/) and [assumption-based argumentation](/assumption-based-argumentation/) build a framework and then ask acceptance questions on it. Sceptical acceptance gives the conclusions that hold in every reasonable position, credulous acceptance gives the defensible ones.
- **Logic programming and nonmonotonic reasoning.** Dung's translation of a normal logic program maps stable extensions to [stable models](/stable-model-semantics/) and the grounded extension to the [well-founded model](/well-founded-semantics/). So credulous and sceptical acceptance under stable semantics play the role of brave and cautious reasoning, and grounded acceptance the role of well-founded reasoning.
- **Solver competitions.** The International Competition on Computational Models of Argumentation (ICCMA) ranks solvers on credulous and sceptical acceptance for several semantics, among other tasks.

## References
