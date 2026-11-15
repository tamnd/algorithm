---
tag: XYFY0N
kind: technique
slug: tableau-blocking
name: Blocking
aliases:
- subset blocking
- pairwise blocking
area: information-retrieval-and-ai-reasoning/knowledge-representation-and-description-logics
level: advanced
summary: Stops expanding a tableau node whose label is contained in that of an ancestor, so tableaux with general TBoxes terminate.
prereqs: [alc-tableau-algorithm, tbox-and-abox]
see_also: [alc-general-tbox-exptime, hypertableau, sroiq, concept-satisfiability, memoization, cycle-detection]
sources:
  - book: isbn:9780521695428
    title: Franz Baader, Ian Horrocks, Carsten Lutz and Ulrike Sattler, An Introduction to Description Logic, Cambridge University Press, 2017
    locator: Chapter 4, Section 4.2.3 (general knowledge base consistency and blocking) and Section 4.3 (blocking for ALCIN)
  - paper: doi:10.1613/jair.21
    title: Martin Buchheit, Francesco M. Donini and Andrea Schaerf, Decidable reasoning in terminological knowledge representation systems, Journal of Artificial Intelligence Research 1, 1993
    locator: pages 109 to 138 (a terminating calculus for general inclusions, general locator)
  - paper: doi:10.1007/3-540-48242-3_11
    title: Ian Horrocks, Ulrike Sattler and Stephan Tobies, Practical reasoning for expressive description logics, Proceedings of LPAR'99, LNAI 1705, Springer, 1999
    locator: pages 161 to 180 (the SHIQ tableau and pairwise blocking)
  - paper: "Ian Horrocks and Ulrike Sattler, A description logic with transitive and inverse roles and role hierarchies, Journal of Logic and Computation 9(3), 1999"
    locator: dynamic blocking for inverse roles (general locator)
  - paper: "Boris Motik, Rob Shearer and Ian Horrocks, Hypertableau reasoning for description logics, Journal of Artificial Intelligence Research 36, 2009"
    locator: anywhere blocking in the hypertableau calculus (general locator)
  - book: isbn:9780521876254
    title: Franz Baader, Diego Calvanese, Deborah L. McGuinness, Daniele Nardi and Peter F. Patel-Schneider (eds.), The Description Logic Handbook, second edition, Cambridge University Press, 2007
    locator: Chapter 2, Basic Description Logics, by Franz Baader and Werner Nutt, Section 2.3 (blocking for general inclusions)
---

Blocking is the technique that makes tableau algorithms stop when the search could build an endless chain of new nodes. A node is *blocked* when an earlier node, usually an ancestor, already has every concept that the blocked node would get. The search then builds nothing below the blocked node, and the model reuses the blocking node in its place. It is what lets the [tableau algorithm for ALC](/alc-tableau-algorithm/) decide satisfiability with respect to a general TBox, and its forms differ by logic: subset blocking for ALC, equality blocking for inverse roles, and pairwise blocking for SHIQ.

## In plain words

A search builds a chain of objects, and each one asks for a next one. Rules that apply to every object can make the chain go on forever. But each object is described by a list of facts taken from a fixed, finite stock. So after enough steps, a new object would get a list that an earlier object already has. Blocking stops there. It does not build the new object, and points the link back to the earlier one. The earlier object already meets every demand that the new one would have, so the loop is a correct part of the example. The search stops, because a chain of objects with different lists cannot be longer than the number of possible lists.

## When it applies

- **Tableaux that can loop.** The rules can create new nodes without end. In ALC this happens with a general or cyclic TBox, because each node gets the concepts of the TBox again. In logics with transitive roles (the S in SHIQ) it happens even without a TBox, because a $\forall r.C$ with $r$ transitive is passed on to each new $r$-successor.
- **Labels from a finite set.** Each label is a subset of a fixed finite set of concepts, the closure of the input. So only finitely many labels exist.
- **Models that may repeat.** Two nodes with the same relevant information can be merged, or the part below one can be copied from the other. This holds for logics with the tree model property, where the model can be a tree that repeats itself.

Without a TBox, ALC needs no blocking: the role depth of the labels drops by one at each level, so the tree is finite.

## The template

1. **Fix the closure.** Let $\mathrm{cl}$ be the set of subconcepts of the input concept and of the TBox concepts, in negation normal form, with $m = |\mathrm{cl}|$. Every label is a subset of $\mathrm{cl}$.
2. **Choose a blocking condition.** For a node $x$ and an earlier node $y$, define when $y$ blocks $x$. For ALC, use subset blocking: $y$ is an ancestor of $x$ and $L(x) \subseteq L(y)$.
3. **Do not expand blocked nodes.** The rules that create new nodes do not apply to a blocked node, or to a node below a blocked one.
4. **Prove termination.** Along each path, the nodes that are not blocked have pairwise different labels (or pairs of labels). So a path has at most $2^m$ such nodes (or $2^{2m}$ for pairs).
5. **Build the model.** Send each edge into a blocked node $x$ to its blocker $y$ instead, or unravel the structure into an infinite tree. Check each $\forall r.C$: the edge goes to a node whose label holds every concept that $x$ had, so it holds $C$.

## Classic examples

The page of the [tableau algorithm](/alc-tableau-algorithm/) shows the smallest case, $T = \{A \sqsubseteq \exists r.A\}$, where the root blocks its own child.

- **Two names that need each other.** Let $T = \{A \sqsubseteq \exists r.B,\ B \sqsubseteq \exists r.A,\ A \sqsubseteq \neg B\}$ and test the concept $A$. Each node gets $\neg A \sqcup \neg B$, $\neg A \sqcup \exists r.B$ and $\neg B \sqcup \exists r.A$. The root completes to $\{A,\ \neg B,\ \exists r.B\}$ plus these three. Its child starts with $\{B\}$ plus the three, and completes to $\{B,\ \neg A,\ \exists r.A\}$ plus the three. The grandchild would start with $\{A\}$ plus the three, which is a subset of the root label, so the root blocks it. The run expands 2 nodes, blocks 1 and meets 3 clashes. The model is the cycle $0 \to 1 \to 0$ with $A^I = \{0\}$ and $B^I = \{1\}$.
- **A transitive role.** With $r$ transitive and no TBox, the concept $\exists r.A \sqcap \forall r.\exists r.A$ makes each new $r$-successor hold $A$, $\exists r.A$ and $\forall r.\exists r.A$ again. Blocking stops the chain at the second successor, which has the same label as the first.

## Variations

- **Subset blocking.** $L(x) \subseteq L(y)$ for an ancestor $y$. It is sound for ALC and for logics with transitive roles but without inverse roles. A form of it is in the calculus of Buchheit, Donini and Schaerf (1993).
- **Equality blocking.** $L(x) = L(y)$. It blocks later than subset blocking, but it stays sound for inverse roles (ALCI).
- **Dynamic blocking.** With inverse roles, a node can add concepts to its parent, so labels change after a block is set. Blocks are then checked again and can be broken (Horrocks and Sattler 1999).
- **Pairwise blocking.** $x$ with parent $x'$ is blocked by $y$ with parent $y'$ when $L(x) = L(y)$, $L(x') = L(y')$, and the edges $x' \to x$ and $y' \to y$ have the same roles. It is needed with inverse roles and number restrictions together, in SHIQ (Horrocks, Sattler and Tobies 1999). The model is then built by unravelling into an infinite tree, and SHIQ has no finite model property.
- **Anywhere blocking.** The blocker can be any node that was created earlier, not only an ancestor. This can stop the search sooner. The [hypertableau](/hypertableau/) calculus uses it (Motik, Shearer and Horrocks 2009).
- **Caching.** A related idea: store the result for each label that was seen, in any branch, and reuse it ([memoization](/memoization/)). Global caching gives tableaux that run in exponential time for ALC with general TBoxes.

## Pitfalls

- **Subset blocking with inverse roles.** The blocker can hold a $\forall r^-.C$ that, along the edge sent to it, asks for $C$ at the parent of the blocked node. The parent may not hold $C$, so the model is wrong. Use equality or pairwise blocking there.
- **Blocking named individuals.** In a tableau for ABox consistency, the nodes for individuals of the ABox are never blocked. Only the new nodes can be.
- **Expanding below a blocked node.** Each node below a blocked node must also stay unexpanded. Otherwise the search can still go on without end.
- **Expecting a fast search.** Blocking alone allows paths of length $2^m$. The plain search then takes double exponential time, more than the EXPTIME bound of the problem ([ALC with general TBoxes is EXPTIME-complete](/alc-general-tbox-exptime/)).

## Exercises

1. Run the tableau with subset blocking on the concept $A$ and $T = \{A \sqsubseteq \exists r.A \sqcap \exists s.A\}$. How many nodes are expanded, and what is the model?
2. Show that with $T = \{A \sqsubseteq \exists r.A\}$ and the concept $A \sqcap B$, subset blocking expands 1 node and equality blocking expands 2. Which labels do the nodes have?
3. Prove that with subset blocking, a path has at most $2^m$ nodes that are not blocked, where $m$ is the size of the closure.
4. Explain why ALC with the empty TBox needs no blocking, and give the bound on the depth of the tree.
5. With inverse roles, give a TBox and a concept for which subset blocking returns a structure that is not a model.

## References
