---
tag: V0RSZE
kind: problem
slug: minimal-unsatisfiable-subset
name: Minimal unsatisfiable subset
aliases:
- MUS
- minimal unsatisfiable core
- minimally unsatisfiable subformula
area: logic-and-constraints/sat-solving
level: advanced
summary: Find an unsatisfiable subset of clauses that is minimal under inclusion; deletion uses m + 1 SAT calls, QuickXplain O(k log(m/k) + k) calls for an MUS of size k.
prereqs: [sat, conjunctive-normal-form, unsat-core]
see_also: [minimal-correction-subset, hitting-set, minimal-transversal-enumeration, incremental-sat, autarky, core-guided-maxsat, max-sat]
sources:
  - book: isbn:9781643681603
    title: Biere, Heule, van Maaren and Walsh (eds.), Handbook of Satisfiability, second edition, IOS Press, 2021
    locator: Chapter 14 (Kleine Büning and Kullmann, Minimal Unsatisfiability and Autarkies), the deficiency of minimally unsatisfiable formulas and the complexity of recognizing them
  - paper: "Ulrich Junker, QuickXplain: Preferred explanations and relaxations for over-constrained problems, AAAI 2004, 167-172"
    title: "QuickXplain: Preferred explanations and relaxations for over-constrained problems"
    locator: the divide-and-conquer algorithm QX and its number of consistency checks
  - paper: doi:10.1007/s10817-007-9084-z
    title: Mark H. Liffiton and Karem A. Sakallah, Algorithms for computing minimal unsatisfiable subsets of constraints, Journal of Automated Reasoning 40(1), 2008, 1-33
    locator: the hitting set duality between MUSes and MCSes and the CAMUS algorithm that enumerates all MUSes
  - paper: "Ron Aharoni and Nathan Linial, Minimal non-two-colorable hypergraphs and minimal unsatisfiable formulas, Journal of Combinatorial Theory, Series A 43(2), 1986, 196-204"
    title: Minimal non-two-colorable hypergraphs and minimal unsatisfiable formulas
    locator: Tarsi's lemma, a minimally unsatisfiable formula has more clauses than variables
  - paper: "Christos H. Papadimitriou and David Wolfe, The complexity of facets resolved, Journal of Computer and System Sciences 37(1), 1988, 2-13"
    title: The complexity of facets resolved
    locator: minimal unsatisfiability is complete for the class D^P
  - paper: "Paolo Liberatore, Redundancy in logic I: CNF propositional formulae, Artificial Intelligence 163(2), 2005, 203-232"
    title: "Redundancy in logic I: CNF propositional formulae"
    locator: the complexity of deciding whether a formula has a small unsatisfiable subset
  - paper: "Herbert Fleischner, Oliver Kullmann and Stefan Szeider, Polynomial-time recognition of minimal unsatisfiable formulas with fixed clause-variable difference, Theoretical Computer Science 289(1), 2002"
    title: Polynomial-time recognition of minimal unsatisfiable formulas with fixed clause-variable difference
    locator: minimal unsatisfiability for each fixed deficiency in polynomial time
  - paper: "John W. Chinneck and Erik W. Dravnieks, Locating minimal infeasible constraint sets in linear programs, ORSA Journal on Computing 3(2), 1991, 157-168"
    title: Locating minimal infeasible constraint sets in linear programs
    locator: the deletion filter for irreducible infeasible subsets of linear constraints
---

A *minimal unsatisfiable subset* (MUS) of an unsatisfiable CNF formula $F$ is a subset $M \subseteq F$ of its clauses that is unsatisfiable, while every proper subset of $M$ is satisfiable. It is minimal under inclusion, not minimum: a formula can have MUSes of different sizes, and in the worst case exponentially many of them. An MUS is the sharpest kind of [unsat core](/unsat-core/). It explains why a set of requirements cannot hold together, and it is the dual of the [minimal correction subset](/minimal-correction-subset/): the MUSes are exactly the minimal hitting sets of the MCSes. With a SAT oracle, the deletion algorithm finds one MUS with $m + 1$ calls, and Junker's QuickXplain needs $O(k \log(m/k) + k)$ calls when the MUS it returns has $k$ clauses.

## In plain words

You have a list of rules that cannot all hold at the same time. You want a short list of rules that already clash, so short that dropping any one of them removes the clash. That is a minimal unsatisfiable subset.

The simple way is to try to drop each rule in turn. If the rest still clash, the rule was not needed and stays out. Otherwise it goes back in. A faster way splits the list in halves and searches each half, which pays off when the clash involves only a few of many rules.

## Definition

Notation: $F = \{c_1, \ldots, c_m\}$ is a CNF formula with $n$ variables and $m$ clauses, and $|F|$ is the total number of literal occurrences. For $G \subseteq F$, $\mathrm{var}(G)$ is the set of variables in $G$.

**Minimal unsatisfiable subset.** $M \subseteq F$ is an MUS of $F$ if $M$ is unsatisfiable and $M \setminus \{c\}$ is satisfiable for every $c \in M$.

Since every subset of a satisfiable set of clauses is satisfiable, the second condition already gives that every proper subset of $M$ is satisfiable. A formula $F$ is *minimally unsatisfiable* if $F$ itself is an MUS of $F$.

**With hard clauses.** Often the clauses are split into hard clauses $H$, which always stay, and soft clauses $S$. An MUS of $S$ relative to $H$ is $M \subseteq S$ such that $H \cup M$ is unsatisfiable and $H \cup (M \setminus \{c\})$ is satisfiable for every $c \in M$. This assumes $H$ is satisfiable. The plain case is $H = \emptyset$.

**The problems.**

- *Extract one MUS:* given an unsatisfiable $F$, output an MUS.
- *Recognize:* decide whether $F$ is minimally unsatisfiable.
- *Smallest MUS:* find an MUS with the fewest clauses.
- *Enumerate:* list all MUSes of $F$.

## Variants

- **Group MUS.** The clauses are put into groups, and a minimal set of groups is wanted. This is the natural form when one requirement is encoded by many clauses, for example by a [Tseitin transformation](/tseitin-transformation/). The algorithms below work unchanged with groups in the role of clauses.
- **Variable MUS.** A minimal set of variables whose clauses are unsatisfiable.
- **Smallest MUS.** A minimum-cardinality MUS. It is much harder than finding some MUS; see Bounds.
- **MUS enumeration.** All MUSes. By the duality with MCSes, the MUSes are the minimal hitting sets of all MCSes, which the CAMUS algorithm of Liffiton and Sakallah uses. See [minimal correction subset](/minimal-correction-subset/) and [minimal transversal enumeration](/minimal-transversal-enumeration/).
- **Irreducible infeasible subsystems.** The same problem for linear inequalities, where Chinneck and Dravnieks used the deletion filter.

## Examples

Take six clauses over $x_1, \ldots, x_4$:
$$c_1 = (x_1),\ c_2 = (\neg x_1 \vee x_2),\ c_3 = (\neg x_2),\ c_4 = (\neg x_1 \vee x_3),\ c_5 = (\neg x_3 \vee x_2),\ c_6 = (x_3 \vee x_4).$$
The formula has exactly two MUSes:

- $\{c_1, c_2, c_3\}$: $x_1$ forces $x_2$, which clashes with $\neg x_2$.
- $\{c_1, c_3, c_4, c_5\}$: $x_1$ forces $x_3$, which forces $x_2$.

Both are minimal, but only the first is a smallest MUS. The clause $c_6$ is in no MUS. A brute-force check of all 64 subsets in the tests confirms the list.

**Deletion on this formula.** Try to drop the clauses in the order $c_1, \ldots, c_6$.

| step | query | answer | action |
|---|---|---|---|
| L1 | $F$ | UNSAT | start with $M = F$ |
| 1 | $M \setminus \{c_1\}$ | SAT | keep $c_1$ |
| 2 | $M \setminus \{c_2\}$ | UNSAT | drop $c_2$ |
| 3 | $M \setminus \{c_3\}$ | SAT | keep $c_3$ |
| 4 | $M \setminus \{c_4\}$ | SAT | keep $c_4$ |
| 5 | $M \setminus \{c_5\}$ | SAT | keep $c_5$ |
| 6 | $M \setminus \{c_6\}$ | UNSAT | drop $c_6$ |

The result is $\{c_1, c_3, c_4, c_5\}$, after 7 oracle calls. Dropping $c_2$ early left only the longer explanation. QuickXplain on the same order returns $\{c_1, c_2, c_3\}$, also with 7 calls.

**A non-example.** $\{(x_1), (\neg x_1), (x_1 \vee x_2)\}$ is unsatisfiable but not minimally unsatisfiable: $(x_1 \vee x_2)$ can go.

## Known algorithms

All of these use a SAT solver as an oracle that answers whether a set of clauses is satisfiable. With an [incremental solver](/incremental-sat/), each clause $c_i$ gets an activation literal $s_i$, and a query on a subset assumes the $s_i$ of the clauses it contains.

### Deletion

```pseudo id=main
DELETION-MUS(H, S = (c_1, …, c_m))
L1  if SAT(H ∪ S) then return "no MUS: H ∪ S is satisfiable"
L2  M ← S
L3  for i ← 1 to m
L4      if SAT(H ∪ (M \ {c_i})) is false then
L5          M ← M \ {c_i}
L6  return M
```

**Theorem 1.** DELETION-MUS returns an MUS of $S$ relative to $H$ and makes exactly $m + 1$ oracle calls.

*Proof.* Invariant: $H \cup M$ is unsatisfiable. It holds after L2 by L1, and L5 only removes $c_i$ when the smaller set is still unsatisfiable. Now take $c_i$ in the final $M$. At step $i$ the oracle found $H \cup (M_i \setminus \{c_i\})$ satisfiable, where $M_i$ is the set at that time. Later steps only remove clauses, so the final $M \setminus \{c_i\}$ is a subset of $M_i \setminus \{c_i\}$, and it is satisfiable too. So every clause of the final $M$ is necessary. The count is one call in L1 and one per step. $\blacksquare$

**Clause set refinement.** When the oracle returns UNSAT at L4 with a core $K$, replace $M$ by $K$: every clause outside $K$ is dropped without a call. When it returns SAT with a model, a clause $c_i$ that is the only clause of $M$ false in the model is necessary, and *model rotation* flips one variable of $c_i$ to find more such clauses. These ideas do not change the worst case, but in practice they save most calls.

### QuickXplain

Junker's QuickXplain splits the candidates in halves and recurses. The background $B$ holds clauses that are known to stay; $\Delta$ is the set that was last added to $B$.

```pseudo id=quickxplain
QX(B, Δ, C)
Q1  if Δ ≠ ∅ and SAT(H ∪ B) is false then return ∅
Q2  if |C| = 1 then return C
Q3  split C into two halves C_1 and C_2
Q4  Δ_2 ← QX(B ∪ C_1, C_1, C_2)
Q5  Δ_1 ← QX(B ∪ Δ_2, Δ_2, C_1)
Q6  return Δ_1 ∪ Δ_2
```

The top level checks that $H$ is satisfiable and $H \cup S$ is not, and then returns QX$(\emptyset, \emptyset, S)$.

**Theorem 2.** Suppose $H \cup B \cup C$ is unsatisfiable, and $H \cup B$ is satisfiable if $\Delta = \emptyset$. Then QX$(B, \Delta, C)$ returns $X \subseteq C$ such that $H \cup B \cup X$ is unsatisfiable and $H \cup B \cup (X \setminus \{x\})$ is satisfiable for every $x \in X$. So the top call returns an MUS.

*Proof.* Induction on $|C|$. If Q1 returns, $\emptyset$ is a correct answer. Otherwise $H \cup B$ is satisfiable, by Q1 or by the hypothesis. If $|C| = 1$, then $X = C$ is correct. Otherwise both halves are nonempty. The call at Q4 meets the hypotheses: $B \cup C_1 \cup C_2 = B \cup C$ and $\Delta = C_1 \neq \emptyset$. So $H \cup B \cup C_1 \cup \Delta_2$ is unsatisfiable, and removing any one clause of $\Delta_2$ makes it satisfiable. The call at Q5 meets them too: $H \cup B \cup \Delta_2 \cup C_1$ is unsatisfiable, and if $\Delta_2 = \emptyset$ the background is $B$, which is satisfiable. So $H \cup B \cup \Delta_2 \cup \Delta_1$ is unsatisfiable and each clause of $\Delta_1$ is necessary. A clause $x \in \Delta_2$ is necessary as well, because $B \cup \Delta_1 \cup (\Delta_2 \setminus \{x\}) \subseteq B \cup C_1 \cup (\Delta_2 \setminus \{x\})$, which is satisfiable with $H$. $\blacksquare$

**Theorem 3.** If QuickXplain returns an MUS of size $k$ from $m$ soft clauses, it makes at most
$$2 + \sum_{d=1}^{\lceil \log_2 m \rceil} \min(2^d, 2k) \;\le\; 2 + 2k \lceil \log_2 m \rceil$$
oracle calls, which is $O(k \log(m/k) + k)$.

*Proof.* Each call of QX makes at most one oracle call, and the top level makes two. Look at the recursion tree, with the top call at depth 0. A call that reaches Q3 has $H \cup B$ satisfiable and $H \cup B \cup C$ unsatisfiable, so its result $X$ is not empty. The result of a call is the union of the results of its two children, and calls at the same depth have disjoint sets $C$. So the calls at depth $d$ that reach Q3 have disjoint, nonempty results inside the final MUS, and there are at most $k$ of them. Each has two children, so depth $d + 1$ has at most $2k$ calls, and also at most $2^{d+1}$. The halves at depth $d$ have at most $\lceil m / 2^d \rceil$ clauses, so no call below depth $\lceil \log_2 m \rceil$ exists. Summing $\min(2^d, 2k)$ over the depths gives the bound. Split the sum at $d = \lceil \log_2 2k \rceil$: the small terms add up to less than $4k$, and the other terms are $2k$ each, with about $\log_2(m/k)$ of them. $\blacksquare$

Junker's paper gives a worst-case bound of the same order for this recursion. When $k$ is close to $m$, deletion is the better choice, since QuickXplain then pays its extra factor.

**In the tests.** The code checks every returned set against a brute-force list of all MUSes of random formulas with up to 11 clauses, checks that every proper subset of it is satisfiable, and checks the call bounds of Theorems 1 and 3. With 2 clashing unit clauses hidden among 62 clauses, deletion makes 63 calls and QuickXplain makes 18.

### Other algorithms

- **Insertion.** Grow a set $T$ from the empty set by adding clauses until $H \cup T$ is unsatisfiable. The last clause added is in an MUS; keep it and start again. This takes $O(mk)$ calls.
- **Dichotomic search.** Binary search for the next necessary clause in the insertion order. This needs $O(k \log m)$ calls.
- **Enumeration by duality.** CAMUS first lists all MCSes, then all their minimal hitting sets, which are exactly the MUSes. MARCO alternates between the two to list MUSes and MCSes one at a time.

## Bounds

**Complexity.**

- Deciding whether a formula is satisfiable reduces to finding an MUS, so extraction is NP-hard. With a SAT oracle, one MUS takes $m + 1$ calls, so it is in $\mathrm{FP}^{\mathrm{NP}}$.
- Recognizing minimally unsatisfiable formulas is complete for $D^P$, the class of intersections of an NP and a coNP language (Papadimitriou and Wolfe, 1988). The "unsatisfiable" part is coNP, and "each $F \setminus \{c\}$ is satisfiable" is NP.
- Deciding whether $F$ has an unsatisfiable subset of at most $k$ clauses is $\Sigma_2^p$-complete (Liberatore, 2005).
- A formula can have exponentially many MUSes. Take the units $(z_0)$ and $(\neg z_t)$ and, for $i = 1, \ldots, t$, two paths from $z_{i-1}$ to $z_i$: the clauses $(\neg z_{i-1} \vee u_i), (\neg u_i \vee z_i)$ and $(\neg z_{i-1} \vee w_i), (\neg w_i \vee z_i)$. A subset is unsatisfiable exactly when it contains both units and a full chain of implications from $z_0$ to $z_t$. So the MUSes are the two units with one path for each $i$: $2^t$ MUSes among $m = 4t + 2$ clauses.

**Tarsi's lemma.** Every minimally unsatisfiable formula $F$ with $n$ variables has $m \ge n + 1$ clauses (Aharoni and Linial, 1986).

*Proof.* For $G \subseteq F$ let $\delta(G) = |G| - |\mathrm{var}(G)|$, so $\delta(\emptyset) = 0$. Pick $G$ with the largest $\delta(G)$.

- First, $\delta(G) \ge 1$. Otherwise $|\mathrm{var}(G')| \ge |G'|$ for every $G' \subseteq F$, and by Hall's theorem the bipartite graph between clauses and their variables has a [matching](/bipartite-matching/) that gives each clause its own variable. Set each matched variable so that it satisfies its clause; this satisfies $F$, a contradiction. So $\delta(G) \ge 1$ and $G \neq \emptyset$.
- Suppose $G \neq F$. For $G' \subseteq F \setminus G$ let $N(G') = \mathrm{var}(G') \setminus \mathrm{var}(G)$. Then $\delta(G \cup G') = \delta(G) + |G'| - |N(G')|$, and the choice of $G$ gives $|N(G')| \ge |G'|$. By Hall's theorem again, the clauses of $F \setminus G$ can be matched to distinct variables outside $\mathrm{var}(G)$, and setting these satisfies $F \setminus G$. Since $F$ is minimally unsatisfiable, the proper subset $G$ has a model, and that model uses only $\mathrm{var}(G)$. The two assignments share no variable, so together they satisfy $F$, a contradiction.

So $G = F$ and $m - n = \delta(F) \ge 1$. $\blacksquare$

The number $m - n$ is the *deficiency*. The second step of the proof builds an [autarky](/autarky/): the matched assignment satisfies every clause that it touches. Kleine Büning and Kullmann survey the classes of minimally unsatisfiable formulas with small deficiency; for each fixed deficiency, minimal unsatisfiability can be decided in polynomial time (Fleischner, Kullmann and Szeider). Both MUSes of the example above have deficiency 1.

## Reductions

- **To MCS.** MUSes are the minimal hitting sets of the MCSes, and the other way round; see the proof on the [minimal correction subset](/minimal-correction-subset/) page. So MUS enumeration reduces to MCS enumeration plus [minimal transversal enumeration](/minimal-transversal-enumeration/).
- **To MaxSAT.** A smallest MUS is not given by MaxSAT directly. But a [MaxSAT](/max-sat/) optimum gives a smallest MCS, and core-guided MaxSAT algorithms extract many cores, often shrunk to MUSes, on the way; see [core-guided MaxSAT](/core-guided-maxsat/).
- **From SAT.** $F$ is satisfiable if and only if it has no MUS.

## Applications

- **Explaining infeasibility.** Configuration, scheduling and timetabling tools show the user a small set of clashing requirements. QuickXplain was made for this use.
- **Model checking.** Abstraction refinement and proof-based abstraction use cores to decide which parts of a design matter; see [CEGAR](/cegar/) and [bounded model checking](/bounded-model-checking/).
- **Debugging.** In type checking, declarative specifications and hardware designs, an MUS points to the lines that cause an error.
- **MaxSAT and diagnosis.** Core-guided MaxSAT and model-based diagnosis work with cores and their hitting sets.

## References
