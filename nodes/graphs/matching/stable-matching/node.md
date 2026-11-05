---
tag: ED689Z
kind: problem
slug: stable-matching
name: Stable matching
aliases:
- stable marriage problem
- Gale-Shapley problem
area: graphs/matching
level: core
summary: Pair agents from two sides with preference lists so that no blocking pair exists.
model: word-ram
complexity:
  vars: {n: the number of agents on both sides, m: the total length of the preference lists}
  time: {worst: O(n + m)}
prereqs: [bipartite-graph, maximal-matching]
see_also: [gale-shapley, stable-matching-rotations, stable-matching-with-ties, stable-roommates-problem, hospitals-residents-problem, irving-stable-roommates, lattice, bipartite-matching]
sources:
  - paper: doi:10.2307/2312726
    title: David Gale and Lloyd S. Shapley, College admissions and the stability of marriage, The American Mathematical Monthly 69(1), 9 to 15 (1962)
    locator: the whole paper (existence of stable matchings and the optimality of deferred acceptance)
  - book: isbn:9780262071185
    title: Dan Gusfield and Robert W. Irving, The Stable Marriage Problem, Structure and Algorithms, MIT Press (1989)
    locator: Chapter 1 (the basic algorithm, optimality, incomplete lists and the set of matched agents) and Chapter 2 (the lattice of stable matchings)
  - book: isbn:9789814425247
    title: David F. Manlove, Algorithmics of Matching Under Preferences, World Scientific (2013)
    locator: Chapter 2, The Stable Marriage Problem, an update
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Section 1.1, A First Problem, Stable Matching
  - paper: doi:10.1137/0215048
    title: Robert W. Irving and Paul Leather, The complexity of counting stable marriages, SIAM Journal on Computing 15(3), 655 to 667 (1986)
    locator: the whole paper (counting stable matchings is #P-complete)
  - paper: "Cheng Ng and Daniel S. Hirschberg, Lower bounds for the stable marriage problem and its variants, SIAM Journal on Computing 19(1), 71 to 77 (1990)"
    locator: the whole paper (the quadratic lower bound)
---

The stable matching problem, also called the stable marriage problem, takes two disjoint sets of agents in which each agent ranks some agents of the other set. It asks for a matching with no *blocking pair*: no two agents who are not partners would both rather be with each other than with their current partners. The pairs that may be matched form a [bipartite graph](/bipartite-graph/), and the graph has no weights; each vertex has a strict ranking of its neighbours instead. Gale and Shapley proved in 1962 that a stable matching always exists, and their [deferred acceptance algorithm](/gale-shapley/) finds one in time linear in the input.

## In plain words

Some students and some schools each rank the other side. A plan assigns each student to at most one school, and each school takes at most one student. The plan is unstable if a student and a school who are not assigned to each other both prefer each other to what the plan gives them, because then they would leave the plan and go together.

A stable plan has no such student and school. One always exists. To find one, the students apply to schools in order of preference, and each school keeps its best applicant so far and turns away the others. The plan you get is the best stable plan for every student at the same time, and the worst stable plan for every school.

## Definition

The input is two disjoint finite sets $P$ and $R$, with $n = |P| + |R|$, and for each agent a strict preference list, best first, of some agents of the other set. A pair $pr$ with $p \in P$ and $r \in R$ is *acceptable* if each is on the list of the other. The acceptable pairs are the edges of a bipartite graph $G$, unweighted, and $m$ is the total length of the lists.

A *matching* is a set $M$ of acceptable pairs in which no agent occurs twice. Write $M(a)$ for the partner of $a$, if $a$ is matched. An acceptable pair $pr \notin M$ *blocks* $M$ if both hold:

- $p$ is single in $M$, or $p$ prefers $r$ to $M(p)$, and
- $r$ is single in $M$, or $r$ prefers $p$ to $M(r)$.

$M$ is *stable* if no pair blocks it.

- **Input:** $P$, $R$ and the preference lists.
- **Output:** a stable matching.

The *classical* case has $|P| = |R|$ and complete lists, in which every agent ranks every agent of the other set. Then $G$ is a complete bipartite graph, every stable matching is perfect, and $m = 2|P|^2$.

**Basic facts.**

- *Existence.* A stable matching always exists; the [Gale-Shapley algorithm](/gale-shapley/) constructs one.
- *Stability implies maximality.* A stable matching is a [maximal matching](/maximal-matching/) of $G$: if an edge $pr$ had both ends single, it would block. So a stable matching has at least half the size of a [maximum matching](/maximum-matching/).
- *The same agents are matched.* In every stable matching of an instance the same set of agents is matched. So all stable matchings have the same size. This is often called the rural hospitals theorem.
- *Optimality.* There is a stable matching $M_P$ in which every $p \in P$ has the best partner it has in any stable matching, and in $M_P$ every $r \in R$ has the worst partner it has in any stable matching. The symmetric matching $M_R$ exists as well.
- *Lattice.* Order the stable matchings by $M \preceq M'$ when each $p \in P$ likes $M(p)$ at least as much as $M'(p)$. Under this order the stable matchings form a distributive [lattice](/lattice/), with least element $M_P$ and greatest element $M_R$. The meet of $M$ and $M'$ gives each $p$ the better of its two partners, and that is a stable matching. The interests of the two sides are opposite: if every $p$ likes $M$ at least as much as $M'$, then every $r$ likes $M'$ at least as much as $M$. The structure of this lattice is described by [rotations](/stable-matching-rotations/).

## Variants

- **Incomplete lists.** Each agent lists only the agents it accepts, as in the definition above. Stable matchings still exist and need not be perfect.
- **Unequal sides.** $|P| \ne |R|$. Then some agents are single in every stable matching.
- **Many-to-one.** Each $r$ has a capacity and may take several agents of $P$: the [hospitals/residents problem](/hospitals-residents-problem/), which was the original setting of Gale and Shapley, called college admissions.
- **Ties.** Lists may contain ties. Then there are several notions of stability; see [stable matching with ties](/stable-matching-with-ties/). With ties and incomplete lists, finding a largest weakly stable matching is NP-hard.
- **One set.** All agents form one set and any two may be paired: the [stable roommates problem](/stable-roommates-problem/), on a general graph. A stable matching may then not exist.
- **Optimal stable matchings.** Among all stable matchings, find one that minimizes the sum of the ranks of the partners (the egalitarian stable matching) or the largest rank of a partner (the minimum regret stable matching). Both are solvable in polynomial time through rotations. The sex-equal stable matching, which balances the two sides, is NP-hard.
- **Counting.** Count the stable matchings. This is #P-complete, by Irving and Leather.

## Examples

**Three stable matchings.** Let $P = \{A, B, C\}$, $R = \{x, y, z\}$, with complete lists

| agent | list | agent | list |
|---|---|---|---|
| $A$ | $x, y, z$ | $x$ | $B, C, A$ |
| $B$ | $y, z, x$ | $y$ | $C, A, B$ |
| $C$ | $z, x, y$ | $z$ | $A, B, C$ |

The instance has exactly three stable matchings out of the $3! = 6$ perfect matchings:

| matching | ranks of the partners of $A, B, C$ | ranks of the partners of $x, y, z$ |
|---|---|---|
| $M_P = \{Ax, By, Cz\}$ | 1, 1, 1 | 3, 3, 3 |
| $\{Ay, Bz, Cx\}$ | 2, 2, 2 | 2, 2, 2 |
| $M_R = \{Az, Bx, Cy\}$ | 3, 3, 3 | 1, 1, 1 |

The lattice is a chain of three elements. The perfect matching $\{Ax, Bz, Cy\}$ is not stable: $C$ prefers $z$ to $y$, and $z$ prefers $C$ to $B$, so $Cz$ blocks it.

**A stable matching that is smaller than a maximum matching.** Let $A$ list $x, y$, let $B$ list $x$, let $x$ list $A, B$, and let $y$ list $A$. The graph has the perfect matching $\{Ay, Bx\}$, but $Ax$ blocks it, because $A$ and $x$ are each other's first choice. The only stable matching is $\{Ax\}$, with $B$ and $y$ single. Its size is 1, half the maximum, which is the worst case allowed by maximality.

**A graph with no perfect matching.** If $|P| = 3$ and $|R| = 2$ with complete lists, every stable matching has two pairs, and the agent of $P$ left single is the same in all of them.

**The empty instance.** With no agents, or with no acceptable pair, the only matching is empty, and it is stable.

## Known algorithms

| algorithm | output | time |
|---|---|---|
| [Gale-Shapley](/gale-shapley/), $P$ proposes | $M_P$ | $O(n + m)$ |
| Gale-Shapley, $R$ proposes | $M_R$ | $O(n + m)$ |
| breakmarriage and rotation elimination, see [rotations](/stable-matching-rotations/) | all stable matchings | $O(n + m)$ setup, then $O(n)$ per matching |
| minimum-weight closure in the rotation poset | egalitarian stable matching | polynomial, by a [max-flow](/max-flow-problem/) computation |
| [Irving's algorithm](/irving-stable-roommates/) | a stable matching of a roommates instance, which includes this problem | $O(n + m)$ |

The Gale-Shapley algorithm reads each list entry at most once, so the time is linear when the rank of a proposer in a list can be read in $O(1)$; for complete lists an $|R| \times |P|$ table of ranks does this.

## Bounds

- **Upper bound.** $O(n + m)$ on the [word RAM](/word-ram/), which is $O(|P|^2)$ for the classical case with complete lists.
- **Lower bound.** For complete lists with $|P| = |R| = k$, every algorithm that reads the lists needs $\Omega(k^2)$ steps in the worst case, by Ng and Hirschberg; this is linear in the size of the input.
- **Number of stable matchings.** It can grow exponentially in $|P|$, so listing all of them needs time proportional to their number.
- **Counting.** #P-complete.

## Reductions

- **To stable roommates.** Put $P \cup R$ into one set and let each agent keep its own list. Pairs inside $P$ or inside $R$ are unacceptable, so they never block, and the stable matchings are the same. So algorithms for the [stable roommates problem](/stable-roommates-problem/) also solve this problem.
- **Many-to-one to one-to-one.** Replace a hospital with capacity $c$ by $c$ copies that share its list, and replace the hospital in each resident's list by its copies in order. The stable matchings correspond.
- **Egalitarian stable matching to minimum cut.** The stable matchings correspond to the closed sets of the rotation poset, so the egalitarian problem is a [maximum-weight closure](/maximum-weight-closure/) problem, solved by one [max-flow](/max-flow-problem/) computation.
- **Linear programming.** The convex hull of the incidence vectors of stable matchings is described by the matching constraints plus one stability inequality for each acceptable pair, by Vande Vate. So [linear programming](/linear-programming-problem/) also finds an optimal stable matching for a linear objective.

## Applications

- **Medical residency.** The National Resident Matching Program in the United States has used a stable matching procedure since the 1950s; its present algorithm, by Roth and Peranson, is a version of deferred acceptance with couples.
- **School choice.** Several cities assign pupils to public schools by deferred acceptance with the pupils proposing. A proposer cannot get a better partner by giving a false list, which makes the procedure safe for the applying side.
- **Other markets.** Assignment of cadets to branches, of students to dormitories, and of tasks to servers in content delivery networks.

## References
