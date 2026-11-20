---
tag: E1SRGM
kind: definition
slug: smith-set
name: Smith set
aliases:
- top cycle
- GETCHA
area: algorithmic-game-theory/social-choice-and-voting
level: core
summary: The smallest nonempty set of candidates each of whom beats every candidate outside it in pairwise majority votes.
prereqs: [condorcet-winner, preference-profile, strongly-connected-components]
see_also: [condorcet-paradox, copeland-method, ranked-pairs, schulze-method, slater-rule, kwiksort-rank-aggregation, tarjan-scc, kemeny-rank-aggregation]
sources:
  - paper: doi:10.2307/1914033
    title: "John H. Smith, Aggregation of preferences with variable electorate, Econometrica 41(6) (1973), 1027-1041"
    locator: "the generalized Condorcet criterion: the winners must come from the smallest set of candidates that beat every outsider"
  - book: isbn:9781107060432
    title: "Felix Brandt, Vincent Conitzer, Ulle Endriss, Jérôme Lang and Ariel D. Procaccia (eds.), Handbook of Computational Social Choice, Cambridge University Press, 2016"
    locator: "Chapter 3 (Felix Brandt, Markus Brill and Paul Harrenstein, Tournament solutions): the top cycle, also called GETCHA or the Smith set, and Theorem 3.8; Section 3.6 on GOCHA, the Schwartz set"
---

The Smith set of an election is the smallest group of candidates that beats everyone outside it. Each member wins a majority vote against each outsider. When there is a [Condorcet winner](/condorcet-winner/), the Smith set contains only that candidate. When the majorities form a cycle, as in the [Condorcet paradox](/condorcet-paradox/), the Smith set contains the whole cycle and every candidate that belongs to a cycle with it. A voting rule that always elects a member is called Smith consistent. This is a stronger demand than electing a Condorcet winner whenever there is one, and many Condorcet methods meet it. The set is computed in time linear in the size of the majority graph.

## Definition

Let $A$ be a finite set of $m$ candidates and $P$ a profile of rankings. Let $g(x, y)$ be the number of voters who rank $x$ above $y$ minus the number who rank $y$ above $x$. A nonempty set $D \subseteq A$ is dominant when $g(x, y) > 0$ for every $x \in D$ and every $y \notin D$. The set $A$ itself is dominant, since it has no outsiders.

The dominant sets form a chain: for any two of them, one contains the other. If $x \in D_1 \setminus D_2$ and $y \in D_2 \setminus D_1$, then $g(x, y) > 0$ because $D_1$ is dominant and $g(y, x) > 0$ because $D_2$ is dominant, which is impossible. So there is exactly one smallest dominant set. This is the Smith set $\mathrm{Sm}(P)$.

An equivalent form uses paths. Draw the weak majority graph, with an arc $x \to y$ whenever $g(x, y) \ge 0$. Every pair of candidates has an arc in at least one direction. The Smith set is the set of candidates that reach every other candidate by a directed path in this graph. In graph terms, it is the first [strongly connected component](/strongly-connected-components/) in the order of the condensation, which is a linear order because the graph is complete. When the number of voters is odd, no margin is 0, the majority graph is a tournament, and the Smith set is its top cycle.

To compute it, count the margins in $O(n m^2)$ time, then run [Tarjan's algorithm](/tarjan-scc/) on the weak majority graph in $O(m^2)$ time, and take the component that no other component reaches. A simpler method with the same bound sorts the candidates by the number of rivals they beat or tie, and returns the shortest prefix of this order that is dominant.

## Examples and non-examples

- **A Condorcet winner.** If $c$ beats every other candidate, then $\{c\}$ is dominant, and it is the Smith set.
- **A cycle and a loser.** Three voters rank $a \succ b \succ c \succ d$, $b \succ c \succ a \succ d$ and $c \succ a \succ b \succ d$. The majorities $a \to b \to c \to a$ form a cycle, and each of the three beats $d$ by 3 to 0. No single candidate is dominant, but $\{a, b, c\}$ is, so it is the Smith set, and $d$ is outside.
- **A dominated member.** Three voters rank $d \succ a \succ b \succ c$, $a \succ b \succ c \succ d$ and $b \succ c \succ d \succ a$. The majorities are $a \to b$, $a \to c$, $b \to c$, $b \to d$, $c \to d$ and $d \to a$. Every set that leaves out $d$ fails, since $d$ beats $a$, and $d$ reaches $b$ and $c$ through $a$. So the Smith set is all four candidates, although every voter ranks $b$ above $c$. A member of the Smith set can be Pareto dominated.
- **Even numbers of voters.** With two voters $a \succ b$ and $b \succ a$, the margin is 0, neither singleton is dominant, and the Smith set is $\{a, b\}$.
- **Not a winner set.** The Smith set is a set of acceptable winners, not a choice of one. Copeland's method, ranked pairs, the Schulze method, Slater's rule and Kemeny's rule always pick a winner inside it, and KwikSort always ranks it first. Plurality, the Borda count and instant runoff voting do not, since they can fail to elect a Condorcet winner.

## Related definitions

- **[Condorcet winner](/condorcet-winner/).** A Smith set of size 1. Smith consistency implies Condorcet consistency.
- **Schwartz set (GOCHA).** The union of the minimal sets that no outsider beats by a strict majority. It is a subset of the Smith set, and the two are equal when no margin is 0.
- **Uncovered set.** Candidate $x$ covers $y$ when $x$ beats $y$ and beats every candidate that $y$ beats. The uncovered candidates form a subset of the top cycle in a tournament, and it is a finer tournament solution.
- **[Copeland set](/copeland-method/), [Slater set](/slater-rule/) and Banks set.** Other tournament solutions, all contained in the top cycle of a tournament.
- **Smith consistency.** A rule is Smith consistent when its winners always lie in the Smith set. The rule pages of this area prove it for [ranked pairs](/ranked-pairs/), the [Schulze method](/schulze-method/) and [Slater's rule](/slater-rule/).

## References
