---
tag: W95AD0
kind: problem
slug: minimal-correction-subset
name: Minimal correction subset
aliases:
- MCS
- minimal correction set
- co-MSS
area: logic-and-constraints/sat-solving
level: advanced
summary: A set of clauses, minimal under inclusion, whose removal makes the formula satisfiable; the MCSes are exactly the minimal hitting sets of the MUSes.
prereqs: [sat, conjunctive-normal-form, minimal-unsatisfiable-subset]
see_also: [hitting-set, minimal-transversal-enumeration, max-sat, partial-max-sat, weighted-max-sat, core-guided-maxsat, incremental-sat, backbone]
sources:
  - paper: doi:10.1016/0004-3702(87)90062-2
    title: Raymond Reiter, A theory of diagnosis from first principles, Artificial Intelligence 32(1), 1987, 57-95
    locator: diagnoses as the minimal hitting sets of the conflict sets, and the HS-tree that computes them
  - paper: doi:10.1007/s10817-007-9084-z
    title: Mark H. Liffiton and Karem A. Sakallah, Algorithms for computing minimal unsatisfiable subsets of constraints, Journal of Automated Reasoning 40(1), 2008, 1-33
    locator: the hitting set duality between MUSes and MCSes, MCS enumeration with blocking, and the CAMUS algorithm
  - paper: "Joao Marques-Silva, Federico Heras, Mikoláš Janota, Alessandro Previti and Anton Belov, On computing minimal correction subsets, IJCAI 2013, 615-622"
    title: On computing minimal correction subsets
    locator: linear search, the clause D (CLD) algorithm and their experimental comparison
  - book: isbn:9781643681603
    title: Biere, Heule, van Maaren and Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 14 (Kleine Büning and Kullmann, Minimal Unsatisfiability and Autarkies), and the MaxSAT chapters on cores and correction sets
---

A *minimal correction subset* (MCS) of an unsatisfiable CNF formula is a set of clauses whose removal makes the rest satisfiable, while removing any proper subset of it does not. Its complement is a *maximal satisfiable subset* (MSS): a satisfiable set of clauses to which no other clause of the formula can be added. MCSes are minimal under inclusion, not minimum; a smallest MCS is the complement of an optimal [MaxSAT](/max-sat/) solution. The central fact is the hitting set duality of Reiter (1987) and Liffiton and Sakallah (2008): the MCSes are exactly the minimal [hitting sets](/hitting-set/) of the [MUSes](/minimal-unsatisfiable-subset/), and the MUSes are exactly the minimal hitting sets of the MCSes. One MCS takes at most $m + 1$ calls to a SAT oracle.

## In plain words

You have a list of rules that cannot all hold. You want to give up as few rules as you must, in the sense that no rule you gave up can be taken back. That set of dropped rules is a minimal correction subset.

Every set of clashing rules must lose at least one member, so a correction must touch every clash. A minimal correction touches every clash and has nothing spare. In the other direction, a minimal clash is a set of rules that every possible correction touches. The two kinds of sets describe each other.

## Definition

Notation: $F$ is a CNF formula with $n$ variables, $m$ clauses and size $|F|$, the total number of literal occurrences. The clauses are split into hard clauses $H$, which always stay, and soft clauses $S$, with $H$ satisfiable. The plain case is $H = \emptyset$ and $S = F$.

- **Correction set.** $C \subseteq S$ is a correction set if $H \cup (S \setminus C)$ is satisfiable.
- **MCS.** A correction set $C$ such that no proper subset of $C$ is a correction set. Since a superset of a correction set is again a correction set, it is enough that $C \setminus \{c\}$ is not a correction set for each $c \in C$.
- **MSS.** $K \subseteq S$ is a maximal satisfiable subset if $H \cup K$ is satisfiable and $H \cup K \cup \{c\}$ is unsatisfiable for each $c \in S \setminus K$. Then $C$ is an MCS exactly when $S \setminus C$ is an MSS.
- **Hitting set.** $T$ hits a family of sets if $T$ meets each set of the family. It is a minimal hitting set if no proper subset of $T$ hits the family.

If $H \cup S$ is satisfiable, its only MCS is $\emptyset$ and it has no MUS.

### The hitting set duality

**Theorem 1.** Let $H$ be satisfiable, and let $\mathcal{U}$ and $\mathcal{C}$ be the families of all MUSes and all MCSes of $S$ relative to $H$.

1. $C \subseteq S$ is a correction set if and only if $C$ hits $\mathcal{U}$. So the MCSes are the minimal hitting sets of $\mathcal{U}$.
2. $M \subseteq S$ makes $H \cup M$ unsatisfiable if and only if $M$ hits $\mathcal{C}$. So the MUSes are the minimal hitting sets of $\mathcal{C}$.

*Proof.* (1) Suppose $C$ is a correction set and some MUS $U$ misses $C$. Then $U \subseteq S \setminus C$, so $H \cup (S \setminus C)$ contains the unsatisfiable $H \cup U$, a contradiction. Conversely, suppose $C$ is not a correction set. Then $H \cup (S \setminus C)$ is unsatisfiable. Remove clauses of $S \setminus C$ one at a time while $H$ together with the rest stays unsatisfiable. This ends, since $S$ is finite, with an MUS $U \subseteq S \setminus C$, and $U$ misses $C$. So the correction sets are exactly the sets that hit $\mathcal{U}$, and the minimal ones on both sides are the same sets.

(2) Suppose $H \cup M$ is unsatisfiable and some MCS $C$ misses $M$. Then $M \subseteq S \setminus C$, and $H \cup (S \setminus C)$ is satisfiable, so $H \cup M$ is too, a contradiction. Conversely, suppose $H \cup M$ is satisfiable. Add clauses of $S$ to $M$ one at a time while $H$ together with the set stays satisfiable. This ends with an MSS $K \supseteq M$, and $C = S \setminus K$ is an MCS that misses $M$. So the sets that make $H \cup M$ unsatisfiable are exactly the sets that hit $\mathcal{C}$. The minimal ones among them are the MUSes. $\blacksquare$

Part 2 needs $H$ to be satisfiable only so that the families are the right ones: if $H$ is unsatisfiable, there is no correction set and the empty set is the only MUS.

## Variants

- **Smallest MCS.** A correction set of minimum size, which is the complement of an optimal MaxSAT solution. With weights it is [weighted MaxSAT](/weighted-max-sat/), and with hard clauses it is [partial MaxSAT](/partial-max-sat/).
- **MCS enumeration.** List all MCSes. With the duality this also lists all MUSes, as in the CAMUS algorithm.
- **Group MCS.** Clauses are put into groups, and whole groups are removed.
- **MSS.** The same problem from the other side, with the same algorithms.

## Examples

Take the six clauses of the [MUS page](/minimal-unsatisfiable-subset/):
$$c_1 = (x_1),\ c_2 = (\neg x_1 \vee x_2),\ c_3 = (\neg x_2),\ c_4 = (\neg x_1 \vee x_3),\ c_5 = (\neg x_3 \vee x_2),\ c_6 = (x_3 \vee x_4).$$
Its MUSes are $\{c_1, c_2, c_3\}$ and $\{c_1, c_3, c_4, c_5\}$. The minimal hitting sets of these two sets are
$$\{c_1\},\quad \{c_3\},\quad \{c_2, c_4\},\quad \{c_2, c_5\},$$
and these are exactly the four MCSes. For instance, without $c_2$ and $c_5$ the model $x_1 = 1, x_2 = 0, x_3 = 1$ satisfies the rest. A smallest MCS has one clause, so a MaxSAT solution leaves one clause false. The sets $\{c_2, c_4\}$ and $\{c_2, c_5\}$ are MCSes too, though they are larger.

**Many MCSes, few MUSes.** The $2t$ unit clauses $(x_i), (\neg x_i)$ for $i = 1, \ldots, t$ have the $t$ MUSes $\{(x_i), (\neg x_i)\}$ and $2^t$ MCSes, one for each way to drop one unit of each pair. The duality swaps the roles: with the chains of the MUS page there are $2^t$ MUSes and $4t + 2$ MCSes.

## Known algorithms

All of these use a SAT oracle that returns a model when one exists. With an [incremental solver](/incremental-sat/), each soft clause gets an activation literal, and a query assumes the activation literals of the clauses it uses.

### Linear search

The algorithm grows a satisfiable set $K$. Each model is used to add every clause that it satisfies, not only the clause that was tested.

```pseudo id=main
LINEAR-MCS(H, S)
L1  μ ← SAT(H); if there is no model then return "no MCS: H is unsatisfiable"
L2  K ← the clauses of S that μ satisfies
L3  for each clause c of S \ K, in order
L4      if c ∉ K and SAT(H ∪ K ∪ {c}) gives a model μ then
L5          K ← K ∪ the clauses of S that μ satisfies
L6  return S \ K
```

**Theorem 2.** LINEAR-MCS returns an MCS and makes at most $1 + |S \setminus K_0|$ oracle calls, where $K_0$ is the set of L2. This is at most $m + 1$.

*Proof.* Invariant: $H \cup K$ is satisfiable, with the last model as a witness, so $S \setminus K$ is always a correction set. A clause $c$ that is still outside $K$ at the end was tested at L4 against some earlier set $K_t$, and $H \cup K_t \cup \{c\}$ was unsatisfiable. Since $K$ only grows, $H \cup K \cup \{c\}$ is unsatisfiable for the final $K$. So $K$ is an MSS and $S \setminus K$ is an MCS. There is one call at L1 and at most one per clause of $S \setminus K_0$. $\blacksquare$

On the example, the empty model of L1 sets every variable to false and satisfies $c_2, c_3, c_4, c_5$. The test of $c_1$ fails, because $x_1$ forces $x_2$ through $c_2$. The test of $c_6$ succeeds. The result is the MCS $\{c_1\}$, after 3 calls.

### Clause D (CLD)

Marques-Silva and others ask a different question: is there a model of $H \cup K$ that satisfies at least one more clause? The disjunction of all clauses of $U = S \setminus K$ is a single clause $D$, the union of their literals.

```pseudo id=cld
CLD-MCS(H, S)
D1  μ ← SAT(H); if there is no model then return "no MCS"
D2  K ← the clauses of S that μ satisfies
D3  loop
D4      D ← the clause made of all literals of the clauses in S \ K
D5      if SAT(H ∪ K ∪ {D}) gives a model μ then
D6          K ← K ∪ the clauses of S that μ satisfies
D7      else return S \ K
```

**Theorem 3.** CLD-MCS returns an MCS. Each model at D5 moves at least one clause into $K$, so there are at most $|S \setminus K_0| + 2$ calls, and the number is often much smaller.

*Proof.* A model of $D$ satisfies some clause of $S \setminus K$, so D6 makes $K$ larger. If D5 finds no model, then for every $c \in S \setminus K$ the set $H \cup K \cup \{c\}$ is unsatisfiable, because every model of $c$ is a model of $D$. So $K$ is an MSS. $\blacksquare$

The D clause can be very long. Marques-Silva et al. (IJCAI 2013) compare CLD with linear search and other methods in their experiments.

### Enumeration by blocking

**Lemma 4.** Let $C_1, \ldots, C_j$ be MCSes, and let $B_i$ be the clause made of all literals of the clauses in $C_i$. Then the MCSes of $S$ relative to $H' = H \cup \{B_1, \ldots, B_j\}$ are exactly the MCSes of $S$ relative to $H$ other than $C_1, \ldots, C_j$.

*Proof.* A model satisfies $B_i$ exactly when it satisfies some clause of $C_i$. Let $C$ be an MCS relative to $H$ other than every $C_i$. Some model $\nu$ of $H \cup (S \setminus C)$ falsifies exactly the clauses of $C$, by minimality. Two distinct MCSes are not subsets of each other, so $C_i \not\subseteq C$, and $\nu$ satisfies every $B_i$. So $C$ is a correction set relative to $H'$. It is minimal there, because a correction set relative to $H'$ is also one relative to $H$. Conversely, let $C$ be an MCS relative to $H'$. As before, a model $\mu$ of $H' \cup (S \setminus C)$ falsifies exactly the clauses of $C$. Since $\mu$ satisfies $B_i$, $C_i \not\subseteq C$. If $C$ were not minimal relative to $H$, it would contain an MCS $C^*$ relative to $H$. $C^*$ is not any $C_i$, since $C_i \not\subseteq C$, so by the first part $C^*$ is a correction set relative to $H'$, and $C$ is not minimal there. $\blacksquare$

So repeat: find an MCS, add its blocking clause to the hard part, and stop when the hard part becomes unsatisfiable. Each round finds a new MCS. With CAMUS, Liffiton and Sakallah enumerate MCSes this way, with an incremental solver and cardinality constraints so that they come in order of size. They then compute the MUSes as minimal hitting sets.

**In the tests.** The code checks every MCS from both algorithms against a brute-force list from all subsets, for random formulas with up to 10 soft clauses and some hard clauses, and checks that no proper subset is a correction set. Enumeration finds every MCS once. The minimal hitting sets of the MCSes, computed by Berge's algorithm, equal the brute-force MUSes, and the other way round.

## Bounds

- **One MCS.** At most $m + 1$ oracle calls by Theorem 2, so the problem is in $\mathrm{FP}^{\mathrm{NP}}$. It is NP-hard: with $H = \emptyset$, the formula $S$ is satisfiable exactly when its MCS is $\emptyset$.
- **Smallest MCS.** Deciding whether there is a correction set with at most $k$ clauses is NP-complete: it is the decision form of MaxSAT. So a smallest MCS is much easier than a smallest MUS.
- **Number of MCSes.** It can be exponential in $m$, as the example with $t$ pairs of units shows. The duality maps a family of $u$ MUSes to its minimal hitting sets, and there can be exponentially many of those in $u$.
- **Testing an MCS.** Given $C$, deciding whether it is an MCS is one SAT query for $S \setminus C$ and $|C|$ UNSAT queries.

## Reductions

- **To MUS and back.** By Theorem 1, enumerating all MCSes and computing their minimal hitting sets gives all MUSes; see [minimal transversal enumeration](/minimal-transversal-enumeration/). The MARCO method alternates between the two families.
- **To MaxSAT.** A smallest MCS is the complement of an optimal [MaxSAT](/max-sat/) solution. Core-guided MaxSAT can be read as the search for a minimum hitting set of the cores; see [core-guided MaxSAT](/core-guided-maxsat/).
- **To hitting set.** Given all MUSes, a smallest MCS is a minimum [hitting set](/hitting-set/), which is the same as [set cover](/set-cover/) in the dual form.

## Applications

- **Model-based diagnosis.** Reiter's theory: the components of a system are soft constraints, an observation contradicts the model of the system, the conflict sets play the role of MUSes, and the diagnoses are the minimal hitting sets of the conflicts, that is, the MCSes.
- **MaxSAT.** Each MCS gives an upper bound for MaxSAT, and some MaxSAT solvers enumerate MCSes to find good solutions fast.
- **Repair of specifications and configurations.** An MCS is a minimal set of requirements to give up. Fault localization tools for programs remove a minimal set of statements so that a failing test can pass.
- **Backbones and MUSes.** MCS algorithms share their machinery of models and blocking clauses with [backbone](/backbone/) computation, and MCS enumeration feeds MUS enumeration.

## References
