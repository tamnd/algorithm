---
tag: QS5856
kind: definition
slug: join-semilattice
name: Join-semilattice
aliases:
- semilattice
- idempotent commutative monoid
area: distributed/replication-and-crdts
level: intro
summary: A partial order in which each pair of elements has a least upper bound, or a set with an associative, commutative and idempotent join.
prereqs: []
see_also: [state-based-crdt, crdt-convergence-theorem, g-counter, crdt, delta-state-crdt, monoid, knaster-tarski-theorem, calm-theorem]
sources:
  - book: isbn:9780521784511
    title: B. A. Davey and H. A. Priestley, Introduction to Lattices and Order, second edition, Cambridge University Press, 2002
    locator: Chapter 1 (ordered sets, upper bounds) and Chapter 2 (lattices as ordered sets and as algebraic structures, the absorption laws)
  - paper: doi:10.1007/978-3-642-24550-3_29
    title: Marc Shapiro, Nuno Preguiça, Carlos Baquero and Marek Zawirski, Conflict-free replicated data types, SSS 2011, LNCS 6976
    locator: pages 386 to 400, Section 2.3 (semilattice, least upper bound, Definition 4 of a monotonic semilattice object)
  - paper: doi:10.1016/j.jpdc.2017.08.003
    title: Paulo Sérgio Almeida, Ali Shoker and Carlos Baquero, Delta state replicated data types, Journal of Parallel and Distributed Computing 111, 2018
    locator: pages 162 to 173, the subsection Simple lattice compositions (the pair and the lexicographic pair, Figures 3 and 4 of the arXiv version)
---

A join-semilattice is a partially ordered set in which every two elements $x$ and $y$ have a least upper bound $x \sqcup y$, called their *join*. Equivalently, it is a set with a binary operation $\sqcup$ that is associative, commutative and idempotent, and the order is recovered as $x \le y \iff x \sqcup y = y$. Joins are the merge functions of [state-based CRDTs](/state-based-crdt/): because a join ignores order, grouping and repeats, replicas that exchange states in any order and any number of times end with the same state.

## Definition

A *partial order* on a set $S$ is a relation $\le$ that is reflexive ($x \le x$), antisymmetric ($x \le y$ and $y \le x$ give $x = y$) and transitive ($x \le y$ and $y \le z$ give $x \le z$). An *upper bound* of $x$ and $y$ is an element $z$ with $x \le z$ and $y \le z$. A *least upper bound* is an upper bound $z$ such that $z \le u$ for every upper bound $u$. By antisymmetry, there is at most one.

**Definition (order form).** A partially ordered set $(S, \le)$ is a *join-semilattice* if every pair $x, y \in S$ has a least upper bound, written $x \sqcup y$.

**Definition (algebraic form).** A *semilattice* is a set $S$ with a binary operation $\sqcup$ such that, for all $x, y, z \in S$:

- associativity: $(x \sqcup y) \sqcup z = x \sqcup (y \sqcup z)$;
- commutativity: $x \sqcup y = y \sqcup x$;
- idempotence: $x \sqcup x = x$.

These are the *ACI laws*. The two forms describe the same objects.

**Proposition.** If $(S, \le)$ is a join-semilattice, then its join satisfies the ACI laws, and $x \le y \iff x \sqcup y = y$. Conversely, if $(S, \sqcup)$ satisfies the ACI laws, then $x \le y :\iff x \sqcup y = y$ is a partial order, and $x \sqcup y$ is the least upper bound of $x$ and $y$ in it.

*Proof.* Order to algebra. $x \sqcup y$ and $y \sqcup x$ are both the least upper bound of the same pair, so they are equal. $x$ is the least upper bound of $x$ and $x$, so $x \sqcup x = x$. Both $(x \sqcup y) \sqcup z$ and $x \sqcup (y \sqcup z)$ are the least upper bound of the three elements $x, y, z$, so they are equal. If $x \le y$, then $y$ is an upper bound of $x$ and $y$ and is below every other one, so $x \sqcup y = y$; if $x \sqcup y = y$, then $x \le x \sqcup y = y$.

Algebra to order. Reflexivity is idempotence. If $x \sqcup y = y$ and $y \sqcup x = x$, then $x = y$ by commutativity. If $x \sqcup y = y$ and $y \sqcup z = z$, then $x \sqcup z = x \sqcup (y \sqcup z) = (x \sqcup y) \sqcup z = y \sqcup z = z$. The element $x \sqcup y$ is an upper bound of $x$, because $x \sqcup (x \sqcup y) = (x \sqcup x) \sqcup y = x \sqcup y$, and of $y$ in the same way. If $u$ is an upper bound of both, then $(x \sqcup y) \sqcup u = x \sqcup (y \sqcup u) = x \sqcup u = u$, so $x \sqcup y \le u$. $\square$

**Finite joins.** By induction on the size, every finite nonempty subset $\{x_1, \ldots, x_k\}$ has a least upper bound $x_1 \sqcup \cdots \sqcup x_k$, and by the ACI laws its value does not depend on the order of the elements or on repeated elements. An infinite subset can lack a join: in $(\mathbb{N}, \max)$ the whole set has no upper bound.

**Bounded semilattice.** If $S$ has a least element $\bot$, then $\bot \sqcup x = x$ for all $x$, and $(S, \sqcup, \bot)$ is a commutative [monoid](/monoid/) in which every element is idempotent. This is where the alias *idempotent commutative monoid* comes from. The empty join is then $\bot$, so every finite subset, the empty one included, has a join.

**Monotone and inflationary maps.** A map $f : S \to S$ is *monotone* if $x \le y$ implies $f(x) \le f(y)$, and *inflationary* if $x \le f(x)$ for all $x$. The join is monotone in each argument: $x \le y$ gives $x \sqcup z \le y \sqcup z$. The updates of a state-based CRDT must be inflationary.

## Examples and non-examples

**Examples.**

- **A chain.** $(\mathbb{Z}, \max)$: the order is the usual $\le$, and every two integers are comparable. Any total order with $\max$ is a join-semilattice.
- **Sets under union.** The finite subsets of a set $U$, with $\sqcup = \cup$ and $\le$ the inclusion $\subseteq$. The bottom is $\varnothing$. This is the state of a [grow-only set](/g-set/).
- **Vectors under pointwise max.** $\mathbb{N}^n$ with $(x \sqcup y)_i = \max(x_i, y_i)$ and the order $x \le y$ iff $x_i \le y_i$ for all $i$. For example $(3, 0, 1) \sqcup (1, 2, 1) = (3, 2, 1)$, while $(3, 0, 1)$ and $(1, 2, 1)$ are incomparable. This is the state of a [g-counter](/g-counter/) and the form of [vector clocks](/vector-clocks/) and [version vectors](/version-vectors/).
- **Products and maps.** If $A$ and $B$ are join-semilattices, so is $A \times B$ with the pointwise join. Finite maps from keys to a bounded semilattice, with a missing key read as $\bot$, are one too.
- **Lexicographic pairs.** If $A$ is a chain and $B$ is a join-semilattice, then $A \times B$ with $(a, b) \sqcup (a', b')$ equal to the pair with the larger first part, or to $(a, b \sqcup b')$ when $a = a'$, is a join-semilattice. A [last-writer-wins register](/lww-register/) uses a pair of this kind with a timestamp first.
- **Divisibility.** The positive integers ordered by "$x$ divides $y$", with $x \sqcup y = \operatorname{lcm}(x, y)$, see the [lcm](/lcm-of-integers/).

**Non-examples.**

- **Addition.** $(\mathbb{N}, +)$ is associative and commutative but not idempotent: $1 + 1 = 2$. A counter that merges two replica values by adding them counts a state twice when it receives it twice.
- **Keep the last arrival.** $x \sqcup y = y$ is associative and idempotent but not commutative, so two replicas that receive the same two states in two orders keep different values.
- **The mean.** $(x + y)/2$ is commutative and idempotent but not associative: $((0 + 0)/2 + 4)/2 = 2$, but $(0 + (0 + 4)/2)/2 = 1$.
- **A bow tie.** Take $\{a, b, c, d\}$ with $a < c$, $a < d$, $b < c$, $b < d$, and $c$, $d$ incomparable. Then $c$ and $d$ are both minimal upper bounds of $a$ and $b$, and there is no least one, so this partial order is not a join-semilattice.

## Related definitions

- **Meet-semilattice.** The dual notion: every pair has a greatest lower bound $x \sqcap y$. Turning the order upside down turns one into the other, for example $(\mathbb{Z}, \min)$ is a join-semilattice for the reversed order.
- **Lattice.** A partial order that is both a join- and a meet-semilattice. In algebraic form, two ACI operations that satisfy the *absorption laws* $x \sqcup (x \sqcap y) = x$ and $x \sqcap (x \sqcup y) = x$. Absorption is what makes the two operations define the same order. Sets under $\cup$ and $\cap$, vectors under $\max$ and $\min$, and positive integers under $\operatorname{lcm}$ and $\gcd$ are lattices. A join-semilattice needs no meets, and CRDTs never use them.
- **Complete lattice.** Every subset, infinite ones included, has a join and a meet. The [Knaster-Tarski theorem](/knaster-tarski-theorem/) on fixed points is about complete lattices. A join-semilattice only guarantees finite joins.
- **Monoid.** A bounded join-semilattice is a commutative [monoid](/monoid/) with idempotent elements. A general commutative monoid, such as $(\mathbb{N}, +, 0)$, is not a semilattice.
- **Monotonic semilattice object.** Shapiro, Preguiça, Baquero and Zawirski (2011, Definition 4) call a replicated object a monotonic semilattice object when its states form a join-semilattice, merge computes the join, and each update is inflationary. The [CRDT convergence theorem](/crdt-convergence-theorem/) says that such an object reaches [strong eventual consistency](/strong-eventual-consistency/).
- **Monotone queries.** The [CALM theorem](/calm-theorem/) uses monotonicity in the sense of set inclusion, the order of the semilattice of sets under union.

## References
