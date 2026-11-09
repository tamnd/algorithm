---
tag: XWAZA4
kind: concept
slug: singleton-arc-consistency
name: Singleton arc consistency
aliases:
- SAC
- singleton consistency
area: logic-and-constraints/constraint-satisfaction
level: advanced
summary: Arc consistency holds after restricting each variable to a single value in turn.
prereqs: [arc-consistency, ac-3]
see_also: [path-consistency, k-consistency, constraint-propagation, bounds-consistency, unit-propagation, maintaining-arc-consistency, ac-4, pc-2]
sources:
  - paper: "Romuald Debruyne and Christian Bessière, Some practicable filtering techniques for the constraint satisfaction problem, Proceedings of IJCAI 1997, pages 412 to 417"
    locator: the definition of singleton arc consistency, the algorithm SAC-1, and the comparison with path inverse consistency and strong path consistency
  - paper: "Christian Bessière and Romuald Debruyne, Optimal and suboptimal singleton arc consistency algorithms, Proceedings of IJCAI 2005, pages 54 to 59"
    locator: the algorithm SAC-Opt with O(e n d^3) time, and the bound for SAC-1
  - paper: "Romuald Debruyne and Christian Bessière, Domain filtering consistencies, Journal of Artificial Intelligence Research 14, 2001, pages 205 to 230"
    locator: the hierarchy of consistencies that delete values only, with SAC between arc consistency and strong path consistency
  - book: isbn:9780444527264
    title: Francesca Rossi, Peter van Beek and Toby Walsh (eds.), Handbook of Constraint Programming, Elsevier, 2006
    locator: Chapter 3, Constraint propagation, by Christian Bessière (singleton consistencies)
---

Singleton arc consistency (SAC) is a local consistency of a binary [constraint satisfaction problem](/constraint-satisfaction-problem/) that is stronger than [arc consistency](/arc-consistency/). A value $a$ of a variable $x_i$ is singleton arc consistent if, after the domain of $x_i$ is reduced to $\{a\}$, enforcing arc consistency leaves no domain empty. A problem is SAC if every value of every domain is. SAC deletes values only, never pairs, so it keeps the constraint graph as it is, unlike [path consistency](/path-consistency/). Debruyne and Bessière defined it in 1997. Its closure is unique and lies between the arc consistency closure and the domains left by strong path consistency.

## In plain words

Arc consistency checks each rule on its own. SAC asks a "what if" question for each value: suppose this unknown takes this value; do the rules, applied one at a time, already show that this is impossible? If they do, the value can be crossed out.

So SAC tries each value in turn, runs arc consistency on the trial, and deletes the value if some list of values becomes empty. Deleting a value can make other trials fail, so it repeats until no trial fails. This finds more dead values than arc consistency, at the price of many runs of arc consistency.

## The idea

**Notation.** $n$ variables, $e$ binary constraints, $d$ the largest domain size. $D = (D_1, \ldots, D_n)$ are the current domains, and $\mathrm{AC}(D)$ is the arc consistency closure of $D$, computed by [AC-3](/ac-3/) or [AC-4](/ac-4/). We write $\mathrm{AC}(D) = \bot$ when the closure has an empty domain. $D|_{x_i = a}$ is $D$ with $D_i$ replaced by $\{a\}$.

**Definition (Debruyne and Bessière 1997).** A value $a \in D_i$ is *singleton arc consistent* in $D$ if $\mathrm{AC}(D|_{x_i = a}) \ne \bot$. The domains $D$ are SAC if no domain is empty and every value of every domain is singleton arc consistent in $D$.

**SAC implies arc consistency.** Let $a \in D_i$ be SAC, and let $D' = \mathrm{AC}(D|_{x_i = a})$. Then $D'_i = \{a\}$ is not empty, and $D'$ is arc consistent, so for every constraint on $x_i$ and $x_j$ some $b \in D'_j \subseteq D_j$ supports $a$. So every value has a support on every arc in $D$.

**SAC is strictly stronger.** Three variables $X, Y, Z \in \{0, 1\}$ with $\ne$ on each pair are arc consistent. Fix $X = 0$: arc consistency deletes 0 from $Y$ and from $Z$, and then the constraint $Y \ne Z$ empties both. So $X = 0$ is not SAC, and in the same way no value is. SAC proves that this problem has no solution, and arc consistency does not.

> **Proposition (a unique closure).** For domains $D^0$, there are largest SAC domains $D^\ast \subseteq D^0$, or none at all, and $D^\ast$ contains every solution.
>
> *Proof.* If $D \subseteq E$ are domains, then $\mathrm{AC}(D) \subseteq \mathrm{AC}(E)$, because the closure of $D$ is arc consistent inside $E$ and the closure of $E$ is the largest such. So if $a$ is SAC in $D$, it is SAC in $E$. Now let $D'$ and $D''$ be SAC, and $E = D' \cup D''$. A value of $E$ is SAC in $D'$ or in $D''$, so it is SAC in $E$, and $E$ is SAC. The union of all SAC domains inside $D^0$ is then the largest one. For a solution $s$, the domains $\{s_1\}, \ldots, \{s_n\}$ are SAC: fixing $x_i = s_i$ leaves the solution, which is arc consistent. So the solution values lie in $D^\ast$. $\square$

If no SAC domains exist inside $D^0$, the problem has no solution. Since the closure is unique, any order of trials reaches the same domains.

> **Proposition (strong path consistency is stronger on values).** Let a binary network be strongly path consistent, with no empty domain and no empty relation. Then its domains are SAC with respect to the original constraints.
>
> *Proof.* Let $R_{ij}$ be the relations of the strongly path consistent network, which lie inside the original constraints. Fix $a \in D_i$ and put $D'_i = \{a\}$ and $D'_j = \{b \in D_j : (a, b) \in R_{ij}\}$ for $j \ne i$. Each $D'_j$ is non-empty by arc consistency. For $j, k \ne i$ and $b \in D'_j$, path consistency gives $c \in D_k$ with $(a, c) \in R_{ik}$ and $(b, c) \in R_{jk}$; so $c \in D'_k$ supports $b$. Values of $D'_j$ have the support $a$ in $D'_i$, and $a$ has a support in each $D'_j$. So $D'$ is arc consistent, inside $D|_{x_i = a}$, with no empty domain, and $\mathrm{AC}(D|_{x_i = a}) \supseteq D' \ne \bot$. $\square$

So the domains left by strong path consistency are contained in the SAC closure: strong path consistency deletes at least the values that SAC deletes, besides the pairs it deletes. Debruyne and Bessière (1997, 2001) placed SAC in a hierarchy of consistencies that delete values only, above arc consistency and path inverse consistency and below strong path consistency.

**Enforcing it.** SAC-1 (Debruyne and Bessière 1997) runs arc consistency first, then repeats passes over all values. For each value $a \in D_i$ it computes $\mathrm{AC}(D|_{x_i = a})$; if this is $\bot$, it deletes $a$ and runs arc consistency again. It stops after a pass that deletes nothing. Each pass makes at most $n d$ trials, each costs $O(e d^2)$ with an optimal arc consistency algorithm, and each pass but the last deletes a value, so there are at most $n d + 1$ passes. The time is $O(n d \cdot n d \cdot e d^2) = O(e n^2 d^4)$.

SAC-Opt (Bessière and Debruyne 2005) keeps, for each value, a copy of the problem reduced by its trial, and updates these copies with an incremental arc consistency algorithm when values are deleted. Each of the $n d$ copies is then an arc consistency run that only deletes, so its total cost is $O(e d^2)$, and SAC-Opt runs in $O(e n d^3)$ time, which they show is optimal, with $O(e n d^2)$ space. SAC-SDS trades some of this time for less space.

**How the pages relate.** [Arc consistency](/arc-consistency/) is the base property, and [AC-3](/ac-3/) and [AC-4](/ac-4/) enforce it. SAC uses them as a subroutine. [Path consistency](/path-consistency/) and [PC-2](/pc-2/) also go beyond arc consistency, but they change relations; SAC changes domains only, which is why solvers find it easier to use. [k-consistency](/k-consistency/) is the general hierarchy, and SAC does not fit in it at a fixed level.

## Examples

**The triangle.** As above, $X, Y, Z \in \{0, 1\}$ with $\ne$ on each pair: every trial fails, SAC empties all domains, and the problem has no solution.

**A value that only SAC removes.** Take $W, X, Y \in \{0, 1\}$ with $X \ne Y$ and the two constraints "$W = 0$ implies $X = 0$" and "$W = 0$ implies $Y = 0$". The network is arc consistent: $W = 0$ has the supports $X = 0$ and $Y = 0$, $W = 1$ fits every value, and $X \ne Y$ gives each value of $X$ and $Y$ a partner. With $W = 0$, arc consistency reduces $X$ and $Y$ to $\{0\}$, and then $X \ne Y$ empties both. So $W = 0$ is not SAC. SAC deletes it and keeps $W = 1$, and the problem has the solutions with $W = 1$.

**A problem SAC does not decide.** Colouring $K_4$ with 3 colours: fixing one vertex to a colour leaves the two other colours for the other three vertices, which is arc consistent. So every value is SAC, but there is no solution. Only a search, or a higher level such as strong 4-consistency, shows this.

**Failed literals in SAT.** In a CNF formula, setting a literal to true and running [unit propagation](/unit-propagation/) until a clause becomes empty is a *failed literal* test. If it fails, the opposite literal must hold. Doing this for every literal until nothing changes is the SAT form of SAC, with unit propagation in place of arc consistency.

## Where it is used

- **Preprocessing.** Solvers run SAC before a search on hard problems, for example on quasigroup completion and scheduling, where it removes values that arc consistency keeps.
- **During search.** SAC at every node of the search is costly. Solvers use cheaper forms such as restricted SAC (one pass) or neighbourhood SAC, and fall back to [maintaining arc consistency](/maintaining-arc-consistency/).
- **Shaving.** In scheduling, *shaving* tests the smallest and largest value of a domain by the same trial with [bounds consistency](/bounds-consistency/), which is singleton bounds consistency.
- **SAT solving.** Failed literal probing is SAC for clauses with unit propagation, and it is part of many SAT preprocessors.
- **Theory.** SAC is one of the "singleton" consistencies, which turn any propagation into a stronger one by trials, and its closure is unique by the same argument as for [constraint propagation](/constraint-propagation/) in general.

## References
