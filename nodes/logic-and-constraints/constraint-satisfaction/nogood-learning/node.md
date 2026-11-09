---
tag: 9MNEB0
kind: technique
slug: nogood-learning
name: Nogood learning
aliases:
- constraint learning
- no-good recording
- nogood recording
- learning while searching
area: logic-and-constraints/constraint-satisfaction
level: advanced
summary: When a search for a CSP solution reaches a dead end, record the part of the current assignment that caused it as a nogood, a new constraint, so the search never repeats the same failure.
prereqs: [constraint-satisfaction-problem, chronological-backtracking, conflict-directed-backjumping]
see_also: [clause-learning, cdcl, first-uip, dynamic-backtracking, graph-based-backjumping, non-chronological-backtracking, restarts, implication-graph]
sources:
  - paper: doi:10.1016/0004-3702(90)90046-3
    title: Rina Dechter, Enhancement schemes for constraint processing, backjumping, learning, and cutset decomposition, Artificial Intelligence 41(3), 1990
    locator: pages 273 to 312 (shallow and deep learning at dead ends, bounded learning by the size of the nogood, and its cost)
  - paper: doi:10.1016/0004-3702(77)90029-7
    title: Richard M. Stallman and Gerald J. Sussman, Forward reasoning and dependency-directed backtracking in a system for computer-aided circuit analysis, Artificial Intelligence 9(2), 1977
    locator: pages 135 to 196 (dependency-directed backtracking, which records the assumptions behind each contradiction as a nogood)
  - book: isbn:9781558608900
    title: Rina Dechter, Constraint Processing, Morgan Kaufmann, 2003
    locator: Chapter 6, General search strategies, look-back (learning algorithms, graph-based and jumpback learning, bounded and relevance-bounded learning)
  - paper: "Thomas Schiex and Gérard Verfaillie, Nogood recording for static and dynamic constraint satisfaction problems, International Journal on Artificial Intelligence Tools 3(2), 1994, pages 187 to 207"
    locator: nogood recording during search with forward checking and in dynamic CSPs
  - paper: "Roberto J. Bayardo Jr. and Robert C. Schrag, Using CSP look-back techniques to solve real-world SAT instances, Proceedings of AAAI-97, 1997, pages 203 to 208"
    locator: conflict-directed backjumping with learning and relevance-bounded learning in a SAT solver
  - paper: "George Katsirelos and Fahiem Bacchus, Generalized nogoods in CSPs, Proceedings of AAAI-05, 2005, pages 390 to 396"
    locator: nogoods that contain both assignments and value removals, learned from propagation
  - paper: doi:10.1007/s10601-008-9064-x
    title: Olga Ohrimenko, Peter J. Stuckey and Michael Codish, Propagation via lazy clause generation, Constraints 14(3), 2009
    locator: pages 357 to 391 (explaining propagators by clauses and learning with a SAT solver)
---

Nogood learning is a look-back technique for backtracking search on a [constraint satisfaction problem](/constraint-satisfaction-problem/). A *nogood* is a partial assignment that no solution extends. When the search reaches a dead end, it finds the earlier assignments that caused the dead end and records their conjunction as a new constraint. The new constraint is implied by the problem, so it removes no solution. But it prunes every later branch that contains the same assignments, so the search does not repeat the same failure in a different part of the tree. Dechter (1990) studied it for CSPs with [backjumping](/conflict-directed-backjumping/). Stallman and Sussman (1977) used the same idea in dependency-directed backtracking. [Clause learning](/clause-learning/) in [CDCL](/cdcl/) SAT solvers is the same technique for Boolean variables, and it made learning the core of modern solvers.

## In plain words

A search that fails often fails for a reason that has nothing to do with most of its current choices. If choosing "Monday" for meeting A and "Room 3" for meeting C makes meeting D impossible, then that pair fails whatever else was chosen. Write the pair down as a new rule: never Monday for A together with Room 3 for C.

Plain backtracking forgets this. Later, after it changes some unrelated choice, it can make the same two choices again and fail again in the same way. With the rule written down, it sees the problem at once. The cost is memory: the list of rules can grow very large, so solvers keep only the short or recent ones.

## When it applies

- The search is a depth-first [backtracking](/chronological-backtracking/) search with dead ends, and failures have *local* causes: a few assignments explain each dead end.
- The search can compute a reason for each removed value. This is the conflict set of [conflict-directed backjumping](/conflict-directed-backjumping/), an explanation in [dynamic backtracking](/dynamic-backtracking/), or a clause that explains a propagation in lazy clause generation.
- The same partial assignments are likely to occur again. This happens with backjumping that does not jump far enough, with dynamic variable orders, and with restarts.
- There is memory for the nogoods, or a rule to forget them.

## The template

The holes are how a dead end is explained, which nogood is stored, and when stored nogoods are deleted.

```pseudo id=main
BACKTRACKING WITH NOGOOD LEARNING
L1  N ← ∅                                           ▷ the store of nogoods
L2  search depth first; treat each ν ∈ N as a constraint: a value is removed if it would complete some ν
L3  for each removed value of x, keep a reason: earlier variables whose values remove it   ▷ hole: how reasons are found
L4  at a dead end at x, with every value removed:
L5      J ← the union of the reasons of the values of x
L6      ν ← the current assignment restricted to J
L7      if ν is empty then return "no solution"
L8      if ν passes the storage test then add ν to N                   ▷ hole: size, relevance or activity bound
L9      jump back to the deepest variable y in J; its value is now removed, with reason J − {y}
L10 from time to time, delete nogoods from N                                ▷ hole: forgetting
```

**Why each learned nogood is correct.** Let $\nu = \sigma|_J$ be learned at the dead end at $x$. Each value $b$ of $x$ has a reason $R_b \subseteq J$: the constraint or the nogood that removes $b$ uses only $x$ and the variables of $R_b$, and the current values of $R_b$ violate it with $x = b$. Suppose a solution $\tau$ extends $\nu$. Then $\tau(x) = b$ for some $b$, and $\tau$ agrees with $\sigma$ on $R_b \subseteq J$, so $\tau$ violates the same constraint, or it extends a nogood. By induction on the order in which nogoods are learned, each earlier nogood is extended by no solution, so this is a contradiction. So no solution extends $\nu$, and adding $\nu$ as a constraint keeps the solution set the same. In particular, an empty $\nu$ at line L7 proves that there is no solution.

**Shallow and deep learning.** Dechter (1990) records at each dead end the conflict set of the dead-end variable, as above. *Graph-based learning* uses the earlier neighbours of $x$ in the [constraint graph](/constraint-graph/) instead, which is easy to compute but gives longer nogoods. *Deep learning* records only minimal nogoods, subsets of $J$ that are still nogoods, which takes extra checks.

**A worked example.** Take $x_1 \in \{1\}$ and $x_2, x_3, x_4 \in \{1, 2\}$, with three constraints: $x_1 = 1$ forces $x_4 = 2$; $x_3 = 1$ forces $x_4 = 1$; and $x_2 = 1$ forbids $x_3 = 2$. The order is $x_1, x_2, x_3, x_4$, and values are tried in increasing order.

1. $x_1 = 1$, $x_2 = 1$, $x_3 = 1$.
2. At $x_4$, the value 1 is removed by $x_1$ and the value 2 by $x_3$. Dead end with $J = \{x_1, x_3\}$. Learn $\nu_1 = \{x_1 = 1, x_3 = 1\}$. Jump back to $x_3$.
3. $x_3 = 1$ is now removed with reason $\{x_1\}$. $x_3 = 2$ is removed by $x_2 = 1$. Dead end with $J = \{x_1, x_2\}$. Learn $\nu_2 = \{x_1 = 1, x_2 = 1\}$. Jump back to $x_2$.
4. $x_2 = 2$. At $x_3$, the value 1 is removed at once by $\nu_1$, and $x_3 = 2$ is consistent.
5. $x_4 = 2$ gives the solution $(1, 2, 2, 2)$.

Without learning, step 4 tries $x_3 = 1$ again, goes down to $x_4$, and fails on both values again before it tries $x_3 = 2$. Backjumping alone does not prevent this, because the jump in step 3 must stop at $x_2$, which really is part of the reason for the failure of $x_3 = 2$.

## Classic examples

- **[Conflict-directed backjumping](/conflict-directed-backjumping/) with learning.** The conflict set at each dead end is the nogood. Dechter (1990) and Frost and Dechter (1994) measured the effect of bounded learning on random CSPs.
- **[Clause learning](/clause-learning/) in [CDCL](/cdcl/).** A learned clause is the negation of a nogood over Boolean literals. The [first UIP](/first-uip/) rule chooses which nogood to learn from the [implication graph](/implication-graph/). Bayardo and Schrag (1997) brought CSP learning to SAT, and GRASP and Chaff made it standard.
- **[Dynamic backtracking](/dynamic-backtracking/).** Ginsberg's method keeps only the nogoods that explain the current eliminations, and deletes each one when its assignments change. This bounds the space by a polynomial.
- **Lazy clause generation.** Each propagator explains its removals with clauses over literals such as $x = v$ and $x \le v$, and a SAT solver learns nogoods from them (Ohrimenko, Stuckey and Codish, 2009). Solvers such as Chuffed use it.
- **Nogood recording from restarts.** Before a restart, the search records nogoods that describe the parts of the tree it has fully explored, so that the next run does not explore them again (Lecoutre and colleagues, 2007).

## Variations

- **Bounded learning.** Keep only nogoods with at most $i$ assignments (Dechter, 1990). There are at most $\sum_{j \le i} \binom{n}{j} d^j$ such nogoods, which is polynomial for fixed $i$.
- **Relevance-bounded learning.** Keep a nogood while at most $i$ of its assignments differ from the current assignment (Bayardo and Miranker, 1996). Dynamic backtracking is the case $i = 1$.
- **Activity-based deletion.** CDCL solvers delete learned clauses with low activity or high literal block distance from time to time.
- **Generalized nogoods.** Nogoods may also contain value removals, such as $x \neq 3$, which come from propagation. They can be shorter and stronger than nogoods of assignments alone (Katsirelos and Bacchus, 2005).
- **Learning with propagation.** With [forward checking](/forward-checking/) or [maintaining arc consistency](/maintaining-arc-consistency/), the reason of a removed value is the set of variables whose assignments caused its removal, and the template is the same.

## Pitfalls

- **Memory blow-up.** Without a bound, the number of nogoods can grow exponentially, and checking them slows down every node. Use a size or relevance bound, and delete nogoods.
- **Long nogoods.** A nogood with many assignments is rarely met again. Graph-based conflict sets give longer nogoods than conflict-directed ones.
- **Wrong reasons.** If a reason includes too few variables, the learned nogood is not implied, and the search can miss solutions. Every removal must keep a complete reason, including removals by learned nogoods.
- **Learning in an all-solutions search.** When the search goes on after a solution, the branches it closes are not dead ends, and a nogood that excludes a found solution is not implied by the problem. Record only nogoods from real dead ends.
- **Dynamic CSPs.** If constraints are removed, nogoods that depend on them become wrong, and they must be removed too (Schiex and Verfaillie, 1994).

## Exercises

1. Prove that the nogood learned at line L6 is still implied when a reason in line L3 comes from an earlier learned nogood, and not only from an original constraint.
2. Show that the number of nogoods with at most $i$ assignments over $n$ variables with $d$ values is at most $\sum_{j \le i} \binom{n}{j} d^j$, and that $i$-bounded learning therefore uses space polynomial in $n$ and $d$ for fixed $i$.
3. In the worked example, let $x_2 \in \{1, 2, 3\}$ and add the constraint "$x_2 = 2$ forbids $x_3 = 2$". Trace the search with and without learning, and count how many times each search reaches $x_4$.

## References
