---
tag: H5K2T7
kind: definition
slug: complete-extension
name: Complete extension
aliases:
- complete semantics
area: information-retrieval-and-ai-reasoning/argumentation-and-belief-revision
level: core
summary: An admissible set that also contains every argument it defends, which is the same as a conflict-free fixed point of the characteristic function.
prereqs: [admissible-set]
see_also: [grounded-extension, preferred-extension, stable-extension-argumentation, semi-stable-extension, argument-labelling, argument-acceptance-problem, fixed-point]
sources:
  - paper: doi:10.1016/0004-3702(94)00041-X
    title: Phan Minh Dung, On the acceptability of arguments and its fundamental role in nonmonotonic reasoning, logic programming and n-person games, Artificial Intelligence 77(2), 321 to 357 (1995)
    locator: Definition 23 (p. 329), Lemma 24 and Theorem 25 (p. 330)
  - paper: doi:10.1007/11853886_11
    title: Martin Caminada, On the issue of reinstatement in argumentation, JELIA 2006, Lecture Notes in Computer Science 4160, 111 to 123 (2006)
    locator: the whole paper (reinstatement labellings and complete extensions)
  - paper: "Martin W. A. Caminada and Dov M. Gabbay, A logical account of formal argumentation, Studia Logica 93(2), 109 to 145 (2009)"
    locator: the whole paper (complete labellings and the semantics defined from them)
  - book: isbn:9781848902756
    title: Wolfgang Dvořák and Paul E. Dunne, Computational problems in formal argumentation and their complexity, in Pietro Baroni, Dov Gabbay, Massimiliano Giacomin and Leendert van der Torre (eds), Handbook of Formal Argumentation, volume 1, College Publications (2018)
    locator: Section 3.3, Table 1 (the row for complete semantics)
---

A complete extension is an [admissible set](/admissible-set/) that is closed under defence: if it defends an argument, it contains that argument. It describes a position that is coherent, answers every attack on itself, and does not leave out anything it has already justified. The grounded, preferred, stable and semi-stable extensions are all complete extensions.

## Definition

Let $(A, R)$ be an argumentation framework. For $S \subseteq A$, let $F(S)$ be the set of the arguments that $S$ defends: $a \in F(S)$ when $S$ attacks every attacker of $a$.

**Definition (Dung 1995, Definition 23).** $S$ is a complete extension when $S$ is admissible and every argument that $S$ defends is in $S$.

**Lemma 24.** A conflict-free set $S$ is a complete extension if and only if $S = F(S)$.

So the complete extensions are the conflict-free fixed points of $F$. The inclusion $S \subseteq F(S)$ says that $S$ defends its members, and $F(S) \subseteq S$ says that $S$ takes in every argument it defends. The second condition is called reinstatement: an argument whose attackers are all beaten must come back.

## Examples and non-examples

Take the framework with $a \to b \to c \to d \to e$, the 2-cycle $e \leftrightarrow f$, and an argument $g$ that attacks itself and $d$. Its seven admissible sets are listed on [admissible set](/admissible-set/). Three of them are complete:

$$\{a, c\},\quad \{a, c, e\},\quad \{a, c, f\}.$$

- $\{a, c\}$: it attacks $b$ and $d$. The argument $e$ is not defended, because nothing in the set attacks $f$. The argument $f$ is not defended, because nothing attacks $e$. And $g$ is not defended, because nothing attacks $g$. So $F(\{a, c\}) = \{a, c\}$.
- $\{a, c, e\}$ and $\{a, c, f\}$ each pick one side of the 2-cycle, and each side defends itself.

Non-examples, all admissible:

- $\emptyset$ is not complete, because it defends $a$, which has no attacker.
- $\{a\}$ is not complete, because it defends $c$.
- $\{f\}$ is not complete, because it defends $a$. And $\{a, f\}$ is not complete, because it defends $c$.

Two more frameworks:

- In the Nixon framework $a \leftrightarrow b$, the complete extensions are $\emptyset$, $\{a\}$ and $\{b\}$. Here $\emptyset$ is complete, because no argument is unattacked.
- With $k$ separate 2-cycles there are $3^k$ complete extensions, because each cycle can be empty or pick one side. So a framework can have exponentially many complete extensions.

## Related definitions

- **Structure (Theorem 25).** Every [preferred extension](/preferred-extension/) is complete, but not every complete extension is preferred ($\emptyset$ in the Nixon framework). The [grounded extension](/grounded-extension/) is the least complete extension. The complete extensions form a complete semilattice: every nonempty family of them has a greatest lower bound. They do not form a lattice in general, since $\{a\}$ and $\{b\}$ in the Nixon framework have no common complete superset.
- **[Stable](/stable-extension-argumentation/) and [semi-stable](/semi-stable-extension/) extensions.** Both are complete extensions, with a condition on the range $S \cup S^+$.
- **[Complete labelling](/argument-labelling/).** A labelling with in, out and undec where an argument is in exactly when all its attackers are out, and out exactly when some attacker is in. The in arguments of a complete labelling form a complete extension, and each complete extension gives exactly one complete labelling: in for $S$, out for $S^+$, undec for the rest (Caminada 2006; Caminada and Gabbay 2009).
- **Ideal extension.** The largest admissible set that is contained in every preferred extension. It is complete, and it contains the grounded extension.
- **Complexity.** Verification is easy (in logspace). Credulous acceptance is NP-complete, and an argument is in some complete extension exactly when it is in some admissible set. Sceptical acceptance is P-complete, because the arguments in every complete extension are exactly the grounded extension. Deciding whether a nonempty complete extension exists is NP-complete (Dvořák and Dunne, Table 1). See [argument acceptance](/argument-acceptance-problem/).

## References
