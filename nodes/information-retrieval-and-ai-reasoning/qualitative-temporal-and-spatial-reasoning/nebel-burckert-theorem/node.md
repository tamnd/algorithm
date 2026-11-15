---
tag: KP8408
kind: theorem
slug: nebel-burckert-theorem
name: Nebel-Bürckert theorem
aliases:
- ORD-Horn tractability theorem
- maximality of ORD-Horn
area: information-retrieval-and-ai-reasoning/qualitative-temporal-and-spatial-reasoning
level: advanced
summary: For interval networks whose labels are ORD-Horn, algebraic closure decides consistency in O(n^3) time, and adding any other relation makes the problem NP-complete.
prereqs: [ord-horn-subclass, interval-algebra-np-completeness, algebraic-closure]
see_also: [interval-algebra-tractable-subclasses, allen-constraint-propagation, horn-sat, unit-propagation, point-algebra-consistency, allens-interval-algebra]
sources:
  - paper: doi:10.1145/200836.200848
    title: Bernhard Nebel and Hans-Jürgen Bürckert, Reasoning about temporal relations, a maximal tractable subclass of Allen's interval algebra, Journal of the ACM 42(1), 1995
    locator: pages 43 to 66 (the translation to ORD-Horn clauses, positive unit resolution, the theorem that path consistency decides networks over H, and the maximality of H)
  - paper: doi:10.1145/876638.876639
    title: Andrei Krokhin, Peter Jeavons and Peter Jonsson, Reasoning about temporal relations, the tractable subalgebras of Allen's interval algebra, Journal of the ACM 50(5), 2003
    locator: pages 591 to 640 (H is the only maximal tractable subalgebra that contains all base relations)
  - paper: "Gérard Ligozat, A new proof of tractability for ORD-Horn relations, Proceedings of AAAI-96, AAAI Press, 1996"
    locator: a geometric proof through preconvex relations
  - paper: doi:10.1016/0004-3702(92)90011-L
    title: Peter van Beek, Reasoning about qualitative temporal information, Artificial Intelligence 58(1-3), 1992
    locator: pages 297 to 326 (the pointisable subclass, which H extends)
---

The Nebel-Bürckert theorem says that the [ORD-Horn subclass](/ord-horn-subclass/) $\mathcal{H}$ of [Allen's interval algebra](/allens-interval-algebra/) is tractable and as large as a tractable class with all base relations can be: [algebraic closure](/algebraic-closure/) decides consistency of every network whose labels are in $\mathcal{H}$, and for every relation outside $\mathcal{H}$, allowing it too makes consistency NP-complete. The page [ORD-Horn subclass](/ord-horn-subclass/) defines the class; this page states and proves the theorem. It turns the general [NP-completeness of the interval algebra](/interval-algebra-np-completeness/) into a precise line between easy and hard labels.

## Statement

A *network over* $\mathcal{H}$ is a [qualitative constraint network](/qualitative-constraint-network/) of the interval algebra in which every label is in $\mathcal{H}$, the 868 relations (counting the empty one) that are conjunctions of ORD-Horn clauses on the endpoints.

> **Theorem 1 (tractability).** Let $N$ be a network over $\mathcal{H}$ on $n$ intervals that is algebraically closed, $C_{ij} \subseteq C_{ik} \diamond C_{kj}$ for all $i, j, k$, and has no empty label. Then $N$ has a solution. So a network over $\mathcal{H}$ is consistent exactly when its algebraic closure has no empty label, which is decided in $O(n^3)$ time.

> **Theorem 2 (maximality).** For every interval relation $R \notin \mathcal{H}$, consistency of networks whose labels are in $\mathcal{H} \cup \{R\}$ is NP-complete.

Theorem 1 needs that the closure of a network over $\mathcal{H}$ is again over $\mathcal{H}$. This holds because $\mathcal{H}$ is closed under converse, intersection and composition, which can be checked on the 868 relations.

## In plain words

Each allowed relation between two intervals can be written as a few simple rules about their four endpoints, where each rule says "if these pairs of endpoints coincide, then this endpoint is not after that one". Rules of this shape can be followed forward, one step at a time, and they never force a choice between two ways. The theorem shows that the three-at-a-time check of algebraic closure already does all the forward steps that matter. So if that check finds no empty label, the rules have no contradiction, and the intervals can be placed. The second half says that the class cannot grow: any further relation lets you encode hard puzzles.

## Proof

*Proof of Theorem 1.* Give each interval $i$ the endpoint variables $i^-$ and $i^+$. For a pair $(i, j)$, let $\Phi_{ij}$ be a set of ORD-Horn clauses over $i^-, i^+, j^-, j^+$ that defines $C_{ij}$, and let $\Phi_{ii}$ be the clauses $i^- \le i^+$ and $i^- \ne i^+$. Say that a clause or a literal over these endpoints *holds on* $C_{ij}$ when it is true for every pair of intervals in one of the base relations of $C_{ij}$.

**Step 1 (to propositional Horn).** Introduce a propositional atom $a_{pq}$ for "$p \le q$" for every two endpoints $p, q$. Write $p = q$ as $a_{pq} \land a_{qp}$ and $p \ne q$ as $\lnot a_{pq} \lor \lnot a_{qp}$. Each ORD-Horn clause becomes one or two propositional Horn clauses. Add the order axioms $a_{pp}$ and $\lnot a_{pq} \lor \lnot a_{qr} \lor a_{pr}$. Call the result $\Psi$.

If $\Psi$ has a model, its true atoms form a preorder on the endpoints that satisfies all clauses. Merging equivalent endpoints gives a partial order, and any linear extension keeps every $\le$ that held and keeps distinct endpoints distinct, so it satisfies every ORD-Horn literal that held. Numbering the linear order gives reals that satisfy all $\Phi_{ij}$, hence a solution of $N$. So it suffices to show that $\Psi$ is satisfiable.

**Step 2 (forward chaining).** A Horn formula is satisfiable exactly when forward chaining, the computation of its least model by [unit propagation](/unit-propagation/), never makes every atom of a clause without a positive literal true. We show by induction on the order in which forward chaining derives atoms:

*(Invariant.)* If $a_{pq}$ is derived, with $p$ an endpoint of $i$ and $q$ an endpoint of $j$, then $p \le q$ holds on $C_{ij}$.

- An axiom $a_{pp}$ holds on every label.
- A clause of $\Phi_{ij}$ with negative atoms $a_1, \ldots, a_t$ and positive atom $a$ fires when $a_1, \ldots, a_t$ are derived. Its atoms are about endpoints of $i$ and $j$ only, so by the invariant each $a_s$ holds on $C_{ij}$, and so does the clause. On every base relation of $C_{ij}$ all negative literals are false, so $a$ is true; $a$ holds on $C_{ij}$.
- A transitivity step derives $a_{pr}$ from $a_{pq}$ and $a_{qr}$, with $p, q, r$ endpoints of $i, k, j$. Take a base relation $c \in C_{ij}$. Closure gives $c \in C_{ik} \diamond C_{kj}$, so there are $b_1 \in C_{ik}$, $b_2 \in C_{kj}$ and three intervals $X, Y, Z$ with $X \mathrel{b_1} Y$, $Y \mathrel{b_2} Z$ and $X \mathrel{c} Z$. By the invariant, $p \le q$ holds for $X, Y$ and $q \le r$ for $Y, Z$, so $p \le r$ for $X, Z$. This is true for every $c \in C_{ij}$, so $p \le r$ holds on $C_{ij}$. The cases with $k = i$ or $k = j$ use $C_{ii} = \{eq\}$.

**Step 3 (no contradiction).** Suppose forward chaining makes all atoms of a clause without a positive literal true. That clause comes from some $\Phi_{ij}$, possibly with $i = j$, so its atoms concern endpoints of $i$ and $j$, and by the invariant they all hold on $C_{ij}$. The clause also holds on $C_{ij}$, since $\Phi_{ij}$ defines $C_{ij}$. On a base relation of $C_{ij}$ the clause would then be both true and false, so $C_{ij}$ has no base relation and is empty, which the hypothesis excludes. So $\Psi$ is satisfiable, and $N$ has a solution. Computing the closure takes $O(n^3)$ time by [algebraic closure](/algebraic-closure/). $\square$

*Proof sketch of Theorem 2 (Nebel and Bürckert 1995).* Membership in NP holds for all interval networks. For hardness, a relation $R$ outside $\mathcal{H}$ is combined with relations of $\mathcal{H}$ by intersection, converse and composition; these operations can be simulated in a network with extra intervals, so consistency over $\mathcal{H} \cup \{R\}$ is at least as hard as over the relations they generate. A case analysis over all relations outside $\mathcal{H}$, done with a computer, shows that each generates a relation for which consistency is NP-hard, by a reduction from 3-SAT in the style of the proof of [NP-completeness of the interval algebra](/interval-algebra-np-completeness/). The details are in Nebel and Bürckert (1995). $\square$

## Consequences

- **An exact cubic test.** Any network over $\mathcal{H}$, including all pointisable and all atomic networks, is decided by [algebraic closure](/algebraic-closure/) or by [Allen's constraint propagation](/allen-constraint-propagation/), in $O(n^3)$ time.
- **A solution, not only an answer.** The proof builds one: compute the least model of $\Psi$, merge equal endpoints, and sort the rest topologically. This is the same idea as [point algebra consistency](/point-algebra-consistency/), extended with Horn clauses.
- **Faster complete search.** For general networks, backtracking can split a label into ORD-Horn pieces instead of single base relations, and stop as soon as every label is in $\mathcal{H}$. Nebel (1997) showed that this cuts the search a lot.
- **Atomic networks.** All 13 base relations are in $\mathcal{H}$, so an atomic interval network is consistent exactly when it is algebraically closed.

## Tightness

- **The ORD-Horn hypothesis is needed.** The network $0 \mathrel{\{o, si\}} 1$, $0 \mathrel{\{fi, si\}} 2$, $0 \mathrel{\{o, fi\}} 3$, $1 \mathrel{\{m, mi\}} 2$, $1 \mathrel{\{b, f\}} 3$, $2 \mathrel{\{b, s\}} 3$ is closed with no empty label and has no solution; five of its six labels are not in $\mathcal{H}$.
- **Closure is needed.** Without the closure condition, a network over $\mathcal{H}$ with no empty label can be inconsistent, for example $0 \mathrel{\{m\}} 1$, $1 \mathrel{\{m\}} 2$, $0 \mathrel{\{m\}} 2$.
- **Maximal, but not the only class.** Theorem 2 shows that no relation can be added to $\mathcal{H}$. There are other maximal tractable classes that do not contain all base relations; Krokhin, Jeavons and Jonsson (2003) found all 18, and $\mathcal{H}$ is the only one that contains all 13 base relations. See [tractable subclasses of the interval algebra](/interval-algebra-tractable-subclasses/).

## History

Van Beek (1992) and Vilain, Kautz and van Beek (1990) showed that the pointisable relations, 188 counting the empty one, are tractable. Nebel and Bürckert (1995) defined the ORD-Horn relations, proved this theorem, and checked maximality with a computer. Ligozat (1996) gave a geometric proof via preconvex relations, which are the same class. Krokhin, Jeavons and Jonsson (2003) completed the picture with the full classification of tractable subclasses.

## References
