---
tag: JW67BF
kind: concept
slug: stable-matching-rotations
name: Stable matching rotations
aliases:
- rotation poset
- rotations
area: graphs/matching
level: advanced
summary: Cyclic shifts between stable matchings that organize the lattice of all stable matchings.
prereqs: [stable-matching, lattice, directed-acyclic-graph]
see_also: [gale-shapley, irving-stable-roommates, stable-roommates-problem, maximum-weight-closure, max-flow-problem, topological-sort, transitive-closure, hospitals-residents-problem]
sources:
  - paper: doi:10.1137/0215048
    title: Robert W. Irving and Paul Leather, The complexity of counting stable marriages, SIAM Journal on Computing 15(3), 655 to 667 (1986)
    locator: the whole paper (rotations, the rotation poset and the correspondence with closed sets)
  - paper: doi:10.1137/0216010
    title: Dan Gusfield, Three fast algorithms for four problems in stable marriage, SIAM Journal on Computing 16(1), 111 to 128 (1987)
    locator: the whole paper (finding all rotations and the rotation poset in O(n^2) time, and listing all stable matchings)
  - paper: doi:10.1145/28869.28871
    title: Robert W. Irving, Paul Leather and Dan Gusfield, An efficient algorithm for the optimal stable marriage, Journal of the ACM 34(3), 532 to 543 (1987)
    locator: the whole paper (the egalitarian stable matching by a minimum cut in the rotation poset)
  - book: isbn:9780262071185
    title: Dan Gusfield and Robert W. Irving, The Stable Marriage Problem, Structure and Algorithms, MIT Press (1989)
    locator: Chapter 2, The Structure of the Set of Stable Matchings, and Chapter 3, Algorithms for the Stable Marriage Problem
---

A rotation is a cyclic exchange of partners that turns one [stable matching](/stable-matching/) into another one, slightly worse for one side and better for the other. Every stable matching is obtained from the proposer-optimal one by eliminating a set of rotations, and the sets that work are exactly the closed sets of a partial order on the rotations, the *rotation poset*. This poset has at most $k(k - 1)/2$ elements for $k$ agents per side and is computed in $O(k^2)$ time, though the number of stable matchings can be exponential. So it is a compact description of the whole [lattice](/lattice/) of stable matchings, and it turns several optimization problems over stable matchings into problems on a [directed acyclic graph](/directed-acyclic-graph/).

## In plain words

Take a stable plan between two groups, say students and schools. Sometimes a few students can pass their schools around in a circle: each student moves to the next school in the circle, which is the best school that would take that student instead of its current one. The new plan is again stable. Each student in the circle gets a worse school, and each school gets a student it likes more.

Such a circle is a rotation. Start from the plan that is best for all students, and apply rotations one after another, until you reach the plan that is best for all schools. Each rotation is used exactly once on any such route, and some rotations must come before others. Every stable plan is what you get by applying a set of rotations that respects this order.

## The idea

Take a classical instance: sets $P$ and $R$ with $|P| = |R| = k$ and complete strict lists, as on the page [stable matching](/stable-matching/). The graph of acceptable pairs is the complete bipartite graph, with preferences instead of weights. Let $M$ be a stable matching and $p \in P$.

- $s_M(p)$ is the first $r$ after $M(p)$ on the list of $p$ such that $r$ prefers $p$ to $M(r)$, if such an $r$ exists.
- $\text{next}_M(p) = M(s_M(p))$, the current partner of $s_M(p)$, which is in $P$.

**Rotations.** A *rotation exposed in $M$* is a cyclic sequence $\rho = (p_0, r_0), (p_1, r_1), \ldots, (p_{t-1}, r_{t-1})$ of pairs of $M$, with $t \ge 2$, such that $r_{i+1} = s_M(p_i)$ for each $i$, indices modulo $t$. Equivalently, $p_{i+1} = \text{next}_M(p_i)$. In the directed graph on $P$ with an arc $p \to \text{next}_M(p)$, the rotations exposed in $M$ are its cycles.

**Elimination.** Eliminating $\rho$ from $M$ gives $M / \rho$, in which $p_i$ is matched to $r_{i+1}$ for each $i$ and all other pairs stay. Then:

1. $M / \rho$ is a stable matching.
2. Every $p_i$ is worse off, and every $r_{i+1}$ is better off, in $M / \rho$ than in $M$.
3. If $M \ne M_R$, the receiver-optimal stable matching, then $M$ has at least one exposed rotation. Every stable matching $M'$ that is worse than $M$ for all of $P$ is reached from $M$ by a sequence of eliminations.

**The rotation poset.** Let $\Pi$ be the set of all rotations that are exposed in some stable matching. Every sequence of eliminations from the proposer-optimal $M_P$ to $M_R$ eliminates every rotation of $\Pi$ exactly once. Define $\rho \prec \rho'$ if $\rho$ is eliminated before $\rho'$ on every such sequence. This is a partial order.

**Theorem (Irving and Leather, 1986).** The map that sends a set $X \subseteq \Pi$ to the matching obtained from $M_P$ by eliminating the rotations of $X$ in an order compatible with $\prec$ is a bijection from the closed sets of $(\Pi, \prec)$, those that contain every predecessor of each of their elements, onto the stable matchings. Union and intersection of closed sets correspond to the join and meet of the lattice.

So the lattice of stable matchings is isomorphic to the lattice of closed sets of $\Pi$, as Birkhoff's representation theorem predicts for a finite distributive lattice. Conversely, every finite distributive lattice is the lattice of stable matchings of some instance.

**Size and computation.** A pair $(p, r)$ appears in at most one rotation as a pair that is removed and in at most one as a pair that is created, so $|\Pi| \le k(k - 1)/2$. Gusfield showed how to find all rotations, and a directed acyclic graph on $\Pi$ with $O(k^2)$ arcs whose [transitive closure](/transitive-closure/) is $\prec$, in $O(k^2)$ total time. The method runs a modified [Gale-Shapley algorithm](/gale-shapley/) for $M_P$, then repeatedly finds a cycle of the next pointers, eliminates it, and continues.

## Examples

**A chain of two rotations.** Let $P = \{A, B, C\}$ and $R = \{x, y, z\}$ with lists

| agent | list | agent | list |
|---|---|---|---|
| $A$ | $x, y, z$ | $x$ | $B, C, A$ |
| $B$ | $y, z, x$ | $y$ | $C, A, B$ |
| $C$ | $z, x, y$ | $z$ | $A, B, C$ |

In $M_P = \{Ax, By, Cz\}$: after $x$ on the list of $A$ comes $y$, and $y$ prefers $A$ to its partner $B$, so $s(A) = y$ and $\text{next}(A) = B$. In the same way, $s(B) = z$ with $\text{next}(B) = C$, and $s(C) = x$ with $\text{next}(C) = A$. So $\rho_1 = (A, x), (B, y), (C, z)$ is exposed. Eliminating it gives $\{Ay, Bz, Cx\}$. In that matching the same computation gives $\rho_2 = (A, y), (B, z), (C, x)$, and eliminating it gives $M_R = \{Az, Bx, Cy\}$. Here $\Pi = \{\rho_1, \rho_2\}$ with $\rho_1 \prec \rho_2$. The closed sets $\emptyset$, $\{\rho_1\}$, $\{\rho_1, \rho_2\}$ are the three stable matchings. The set $\{\rho_2\}$ is not closed, and indeed $\rho_2$ is not exposed in $M_P$.

**Two independent rotations.** Let $P = \{A, B, C, D\}$ and $R = \{x, y, z, w\}$ with

| agent | list | agent | list |
|---|---|---|---|
| $A$ | $x, y, z, w$ | $x$ | $B, A, C, D$ |
| $B$ | $y, x, z, w$ | $y$ | $A, B, C, D$ |
| $C$ | $z, w, x, y$ | $z$ | $D, C, A, B$ |
| $D$ | $w, z, x, y$ | $w$ | $C, D, A, B$ |

In $M_P = \{Ax, By, Cz, Dw\}$ two rotations are exposed: $\rho_1 = (A, x), (B, y)$ and $\rho_2 = (C, z), (D, w)$. They are incomparable, so all four subsets of $\{\rho_1, \rho_2\}$ are closed, and the instance has exactly four stable matchings. The lattice is a square, not a chain.

**A single stable matching.** If $M_P = M_R$, no rotation is exposed, $\Pi$ is empty, and the empty set is the only closed set. This happens, for example, when every $p$ has a different first choice $r$ and that $r$ ranks $p$ first.

**The empty instance.** With $k = 0$, there is one stable matching, the empty one, and $\Pi = \emptyset$.

## Where it is used

- **Listing all stable matchings.** A search over the closed sets of $\Pi$ lists all stable matchings with $O(k)$ work each after $O(k^2)$ preprocessing.
- **The egalitarian stable matching.** Give each rotation $\rho$ the weight $w(\rho)$, the change in the total rank of the partners caused by eliminating it. A stable matching of least total rank is a closed set of least weight, a [maximum-weight closure](/maximum-weight-closure/) problem solved by one [max-flow](/max-flow-problem/) computation. Irving, Leather and Gusfield gave an $O(k^4)$ algorithm in this way, and any linear objective in the ranks is handled the same way.
- **Minimum regret.** The stable matching that minimizes the worst rank of a partner comes from Gusfield's algorithm in $O(k^2)$ time.
- **Counting.** The number of stable matchings is the number of closed sets of $\Pi$. Irving and Leather used rotations to show that counting stable matchings is #P-complete.
- **Pairs that are stable somewhere.** A pair $(p, r)$ is in some stable matching if and only if it is in $M_P$ or is created by some rotation. So all stable pairs are found in $O(k^2)$ time.
- **Other models.** Rotations exist for the [hospitals/residents problem](/hospitals-residents-problem/), and a version of them appears in phase 2 of [Irving's algorithm](/irving-stable-roommates/) for the [stable roommates problem](/stable-roommates-problem/), where the poset of rotations has no lattice structure in general.

## References
