---
tag: 974KXE
kind: algorithm
slug: hypertableau
name: Hypertableau calculus
aliases:
- Motik-Shearer-Horrocks hypertableau
area: information-retrieval-and-ai-reasoning/knowledge-representation-and-description-logics
level: research
summary: Turns a TBox into DL-clauses and builds a model with hyperresolution-like steps that branch only on real disjunctions, with anywhere blocking to stop.
solves: [concept-satisfiability, concept-subsumption]
model: word-ram
complexity:
  vars: {n: the size of the concept and the TBox}
  time: {worst: 2^2^2^O(n)}
  space: {extra: 2^2^O(n)}
properties: {deterministic: true, exact: true, builds_model: true, backtracking: true}
history:
  year: 2009
  people: [Boris Motik, Rob Shearer, Ian Horrocks]
  note: The journal paper gave the calculus for expressive description logics with DL-clauses, the Hyp-rule and anywhere blocking. It is the core of the HermiT reasoner.
prereqs: [alc-tableau-algorithm, tableau-blocking, concept-satisfiability, hyperresolution]
see_also: [alc-description-logic, sroiq, el-classification, chronological-backtracking, conflict-directed-backjumping, skolemization, ontology-classification, horn-clause]
sources:
  - paper: doi:10.1613/jair.2811
    title: Boris Motik, Rob Shearer and Ian Horrocks, Hypertableau reasoning for description logics, Journal of Artificial Intelligence Research 36, 2009
    locator: pages 165 to 228 (Table 4 on page 192 for the translation into DL-clauses, Definition 7 on page 193 and Table 5 on page 196 for the rules, Section 3.1.1 for the example with some R.A subsumed by A, Section 3.2.2 for anywhere blocking)
---

The hypertableau calculus decides satisfiability of a concept with respect to a general TBox by first turning every axiom into DL-clauses, rules of the form "if these atoms hold, then one of those atoms holds", and then building a model by applying the clauses forward. A clause fires only when its whole body is already true, as in [hyperresolution](/hyperresolution/), so an inclusion such as $A \sqsubseteq B$ adds $B$ only where $A$ holds, and the search branches only when a clause with two or more head atoms fires. New nodes come from existential atoms, and anywhere blocking stops the tree from growing forever. Motik, Shearer and Horrocks introduced it in 2009 to cut the nondeterminism of the [ALC tableau](/alc-tableau-algorithm/).

## In plain words

A tableau reasoner checks whether a description can be met by building an example step by step. The plain method turns each rule of the form "every A is a B" into a choice at every element: either it is not an A, or it is a B. With many rules, it makes many choices that do not matter and then undoes them. The hypertableau method writes each rule as "if A holds here, then B holds here" and uses it only when A is already known. A rule that says "if a child has A, then the parent has A" also becomes a plain forward step, with no guess at all. Choices are left only for rules that really say "one of these". To stop making new elements forever, an element that looks exactly like an earlier one is not expanded; it reuses the earlier one instead.

## The problem

The input is an [ALC](/alc-description-logic/) concept $C$ and a TBox $T$ of general concept inclusions; the output is whether some model of $T$ puts an element in $C$ ([concept satisfiability](/concept-satisfiability/)). Subsumption $C \sqsubseteq_T D$ is the unsatisfiability of $C \sqcap \neg D$ ([concept subsumption](/concept-subsumption/)). The problem is EXPTIME-complete ([ALC with general TBoxes](/alc-general-tbox-exptime/)). This page and its code treat ALC without inverse roles; the paper covers much larger logics with inverse roles, nominals and number restrictions.

## The algorithm

**DL-clauses.** Each inclusion $D_1 \sqsubseteq D_2$ becomes $\top \sqsubseteq \mathrm{nnf}(\neg D_1 \sqcup D_2)$, and each disjunction is read as a clause over a center variable $x$ and one variable $y_i$ for each value restriction:

| disjunct | goes to | as |
|---|---|---|
| $A$ | head | $A(x)$ |
| $\neg A$ | body | $A(x)$ |
| $\exists r.D$ | head | $(\exists r.Q_D)(x)$ |
| $\forall r.\neg A$ | body | $r(x, y_i) \wedge A(y_i)$ |
| $\forall r.D$ | body and head | $r(x, y_i)$ in the body, $Q_D(y_i)$ in the head |
| $D_1 \sqcap D_2$ | head | $Q_D(x)$ |

Here $Q_D$ is $D$ when $D$ is a name and otherwise a fresh name with the clauses of $Q_D \sqsubseteq D$. So $A \sqsubseteq B$ is $A(x) \to B(x)$, $A \sqsubseteq \exists r.B$ is $A(x) \to (\exists r.B)(x)$, and $\exists r.A \sqsubseteq B$ is $r(x, y) \wedge A(y) \to B(x)$, with no disjunction in any of them. The input concept gets a fresh name $Q_0$ with the clauses of $Q_0 \sqsubseteq C$.

```pseudo id=main
HYPERTABLEAU(C, T)
L1  Γ ← the DL-clauses of T and of Q0 ⊑ C; start with one node n0 and L(n0) = {Q0}
L2  repeat
L3      if a clause of Γ with at most one head atom has an instance σ whose body holds and whose head does not
L4          if the head is empty: return clash, with the branch points the body depends on
L5          add the head atom under σ; continue
L6      if a node x that is not BLOCKED has (∃r.A)(x) and no r-child with A: add a child w, r(x, w), A(w); continue
L7      if a clause with two or more head atoms has such an instance σ
L8          for each head atom V: try the branch with σ(V) added; stop on success; backjump past this point if the clash does not use V
L9          return clash, with the union of the branch points of the failed branches, without this one
L10     return satisfiable                     ▷ no rule applies: the nodes that are not blocked form a model

BLOCKED(w)
L11 w is blocked if its parent is blocked, or if some earlier node that is not blocked has the same label
```

Lines L3 to L5 are the deterministic part of the Hyp-rule: a body that matches the current nodes forces its only head atom, or a clash when the head is empty. The body may look at the children of $x$, so facts flow up the tree as well as down. Line L6 is the existential rule, applied before any branching so that clashes that need no choice are found first. Line L7 is the Hyp-rule with a real disjunction; line L8 tries each head atom in turn. Every fact carries the set of branch points it depends on, so a branch that fails for a reason that has nothing to do with the current choice returns at once to the choice that caused it, as in [conflict-directed backjumping](/conflict-directed-backjumping/). Line L11 is anywhere blocking with equality: the blocker may sit anywhere in the tree, not only on the path to the root.

## Example

Let $T = \{\exists r.A \sqsubseteq A\}$ and $C = \neg A \sqcap \exists r.\exists r.A$. The four clauses are (1) $r(x, y) \wedge A(y) \to A(x)$, (2) $Q_0(x) \wedge A(x) \to \bot$, (3) $Q_0(x) \to (\exists r.Q_1)(x)$ and (4) $Q_1(x) \to (\exists r.A)(x)$, where $Q_1$ stands for $\exists r.A$.

| step | line | clause or rule | result |
|---|---|---|---|
| 1 | L1 | start | $L(n_0) = \{Q_0\}$ |
| 2 | L3, L5 | clause 3 at $n_0$ | $(\exists r.Q_1)(n_0)$ |
| 3 | L6 | existential rule | new node $n_1$, $r(n_0, n_1)$, $Q_1(n_1)$ |
| 4 | L3, L5 | clause 4 at $n_1$ | $(\exists r.A)(n_1)$ |
| 5 | L6 | existential rule | new node $n_2$, $r(n_1, n_2)$, $A(n_2)$ |
| 6 | L3, L5 | clause 1 with $x = n_1$, $y = n_2$ | $A(n_1)$ |
| 7 | L3, L5 | clause 1 with $x = n_0$, $y = n_1$ | $A(n_0)$ |
| 8 | L3, L4 | clause 2 at $n_0$ | clash: $C$ is unsatisfiable |

The run makes 2 nodes and 5 Hyp-rule steps and never branches. A plain tableau with subset blocking and no optimizations, the reference of the tests, reads the axiom as $\forall r.\neg A \sqcup A$ at every node and, on the same input, expands 3 nodes and tries 7 completions.

## Correctness

The clauses have the same models as the TBox once each fresh name $Q_D$ is read as $D$. Each rule step is a consequence of the clauses, with the new nodes read as Skolem terms, so a clash that depends on a set of choices shows that those choices cannot hold together; this is also why backjumping is safe. The search stops: a node has at most one child for each existential atom, and the nodes on any path that still grows are not blocked and so have pairwise different labels, which bounds the depth by the number of possible labels. When no rule applies, the nodes that are not blocked form a model: an edge to a blocked node is sent to its blocker, which has the same label, so every clause instance in the model has a copy in the branch, where it already holds. The full proof, with the counterexample to subset blocking, is in proofs/correctness.md.

## Complexity

Let $n$ be the size of $C$ and $T$, so there are $O(n)$ names and existential atoms. A branch has depth at most $2^{O(n)}$ and out-degree $O(n)$, so it has at most $2^{2^{O(n)}}$ nodes, and the depth-first search over the branch points is bounded by $2^{2^{2^{O(n)}}}$ steps and $2^{2^{O(n)}}$ space. These are coarse bounds for this search; satisfiability in ALC with a general TBox is EXPTIME-complete, and worst-case optimal methods use global caching or type elimination instead.

The gain is in the nondeterminism. For $T_m = \{B_i \sqsubseteq C_i : 1 \le i \le m\} \cup \{A \sqsubseteq \exists r.D,\ D \sqsubseteq E,\ E \sqsubseteq \bot\}$ and the concept $A$, the hypertableau makes 1 node, takes 3 Hyp-rule steps and never branches, because no node has any $B_i$. The same plain tableau adds $\neg B_i \sqcup C_i$ to every node and tries every combination at the root:

| $m$ | plain tableau: nodes | plain tableau: completions tried |
|---|---|---|
| 0 | 2 | 20 |
| 2 | 5 | 221 |
| 4 | 17 | 3185 |
| 6 | 65 | 49601 |
| 8 | 257 | 788225 |

Tableau reasoners with absorption, which turns $B_i \sqsubseteq C_i$ into a rule that fires only on $B_i$, also avoid this blow-up; the DL-clauses give the same effect for every inclusion whose left side is a conjunction of names and existential restrictions on names.

## Properties

- **Branching only on disjunctions.** An inclusion with a conjunction of names and existential restrictions on names on the left, and no disjunction on the right, gives clauses with at most one head atom, and these never branch. When all clauses are of this kind, the search is deterministic.
- **Facts flow both ways.** A body atom $A(y)$ lets a child change its parent, which is what makes $\exists r.A \sqsubseteq A$ deterministic.
- **Builds a model.** An open branch gives a finite model of $T$ with the root in $C$.
- **Exact.** It answers both "yes" and "no" correctly for every ALC input.

## Variants and improvements

- **Expressive logics.** Motik, Shearer and Horrocks (2009) extend the clauses with inverse roles, number restrictions, nominals and equality atoms between successors, with pairwise anywhere blocking for inverse roles.
- **Blocking variants.** Anywhere blocking lets the blocker be any earlier node, not only an ancestor, so trees stop earlier. Single blocking with equality, as here, suffices without inverse roles; pairwise blocking compares a node and its parent with another such pair.
- **Absorption and caching.** Reasoners combine the calculus with absorption of axioms into the clause bodies, caching of results for labels, and individual reuse between subsumption tests during [ontology classification](/ontology-classification/).
- **Simple search.** Without the dependency sets, [chronological backtracking](/chronological-backtracking/) is correct too, but it can retry the same failing expansion under every combination of earlier, unrelated choices.

## When to use it

Use it for satisfiability, subsumption and classification in expressive description logics, up to the [SROIQ](/sroiq/) logic of OWL 2, especially for ontologies with many general concept inclusions whose left sides are conjunctions, where a plain tableau branches on every axiom at every node. For ontologies that stay inside the [EL family](/el-classification/), completion rules classify in polynomial time and are much faster. For query answering over large data in DL-Lite, [query rewriting](/perfectref-rewriting/) fits better.

## Pitfalls

- **Subset blocking.** Line L11 must ask for an equal label. With "subset of an earlier label", the concept $A \sqcap W \sqcap \exists r.W \sqcap \forall r.\neg A$ with $W \sqsubseteq \exists r.B$ and $\exists r.B \sqsubseteq A$ is reported satisfiable: the child for $W$ is blocked by the root, its $B$-successor is never made, and the $A$ it would force upward is never seen. Subset blocking is sound only when facts flow downward, as in the plain tableau.
- **A blocked blocker.** At line L11, the earlier node must not be blocked itself. A blocked node does not expand its existential atoms, so redirecting edges to it builds an interpretation in which those atoms fail.
- **Backjumping without the body set.** At line L8, the head atom chosen at a branch point must carry the branch points of the clause body as well as its own. If it carries only its own, a clash that comes from the body is blamed on nothing, the search jumps over a choice that matters, and a satisfiable concept can be reported unsatisfiable.
- **Clauses that guess.** Line L1 must put $\forall r.\neg A$ into the body as $r(x, y) \wedge A(y)$. Writing it into the head through a fresh name $Q$ with $Q \sqsubseteq \neg A$ is still correct, but $\exists r.A \sqsubseteq B$ then becomes a clause with two head atoms, and line L7 branches at every node with an $r$-successor, much as the plain tableau does.
- **Branching first.** If line L7 runs before line L6, a clash that needs no choice, deep in the tree, is found only after every choice above it, and without backjumping the search repeats it for each combination.

## Implementations

## History

Hyperresolution is due to Robinson (1965); hyper tableaux for first-order clauses were studied by Baumgartner, Furbach and Niemelä in the 1990s. Motik, Shearer and Horrocks (2009) adapted the idea to description logics: they defined DL-clauses, the Hyp-rule and anywhere pairwise blocking, proved the calculus correct for expressive logics with inverse roles, nominals and number restrictions, and showed with the HermiT reasoner that it classifies many ontologies faster than tableau reasoners of the time. HermiT is one of the standard reasoners for OWL 2.

## References
