---
tag: DWARFM
kind: algorithm
slug: slater-rule
name: "Slater's rule"
aliases:
- Slater ranking
area: algorithmic-game-theory/social-choice-and-voting
level: advanced
summary: Finds the ranking that disagrees with the fewest pairwise majority outcomes, a minimum feedback arc set of the majority tournament.
model: word-ram
complexity:
  vars: {n: the number of voters, m: the number of candidates}
  time: {worst: O(n m^2 + 2^m m)}
  space: {extra: O(2^m)}
properties: {deterministic: true, comparison: false, recursive: false}
history:
  year: 1961
  people: [Patrick Slater]
  note: "Slater asked for the ranking that reverses the fewest outcomes of a schedule of paired comparisons. Its use as a voting rule and its NP-hardness came later, in social choice and in computational social choice."
prereqs: [condorcet-winner, feedback-arc-set-problem, bitmask-dp]
see_also: [kemeny-rank-aggregation, kwiksort-rank-aggregation, smith-set, copeland-method, ranked-pairs, condorcet-paradox, np-hard, dodgson-rule]
sources:
  - paper: doi:10.1093/biomet/48.3-4.303
    title: "Patrick Slater, Inconsistencies in a schedule of paired comparisons, Biometrika 48(3-4) (1961), 303-312"
    locator: "the problem of finding the ranking with the fewest inconsistencies with the outcomes of paired comparisons"
  - book: isbn:9781107060432
    title: "Felix Brandt, Vincent Conitzer, Ulle Endriss, Jérôme Lang and Ariel D. Procaccia (eds.), Handbook of Computational Social Choice, Cambridge University Press, 2016"
    locator: "Chapter 3 (Felix Brandt, Markus Brill and Paul Harrenstein, Tournament solutions): the Slater set and Theorem 3.3 on its NP-hardness; the top cycle (Smith set) and Theorem 3.8"
---

Slater's rule turns the majority relation of an election into a ranking. For each pair of candidates, a majority of voters prefers one to the other, and the rule looks for the ranking that goes against as few of these majorities as possible. When the majority relation has no cycle, the answer is that relation itself. When it has cycles, some majorities must be reversed, and the rule reverses the fewest. In graph terms, it finds a minimum [feedback arc set](/feedback-arc-set-problem/) of the majority tournament. The Slater winners are the candidates on top of some optimal ranking. The problem is [NP-hard](/np-hard/). The algorithm below is a [dynamic program over subsets](/bitmask-dp/) that takes $O(2^m m)$ time after the majorities are counted, which is fast enough for about 20 candidates.

## In plain words

For every pair of candidates, count which one more voters prefer. Each such result is one fact about the voters. A ranking agrees with some of these facts and goes against others. Slater's rule picks the ranking that goes against the fewest facts, and the top of that ranking wins. Only who won each pair counts, not by how much. The program builds the best ranking one place at a time: for every group of candidates, it remembers the best way to rank that group, and it tries each member of a group as its first.

## The problem

There are $m$ candidates $A = \{0, \ldots, m - 1\}$ and a profile $P$ of $n$ rankings. Let $g(x, y) = n_P(x, y) - n_P(y, x)$ be the margin of $x$ over $y$. The majority graph has an arc $x \to y$ when $g(x, y) > 0$; when $n$ is odd it is a tournament, with one arc between each pair. For a ranking $r$, its Slater cost is the number of pairs where $r$ puts $y$ above $x$ although $g(x, y) > 0$. A Slater ranking has the least cost, and the Slater winners are the candidates on top of some Slater ranking. The code returns the Slater ranking that is first in lexicographic order, and its top as the winner. Pairs with margin 0 cost nothing in either order.

## The algorithm

For a set $S$ of candidates, let $\mathrm{cost}(S)$ be the least cost of a ranking of $S$ alone. If $v$ is first, it is above all of $S \setminus \{v\}$, so it goes against the arcs into $v$ from $S$, and the rest is ranked as well as possible:

$$\mathrm{cost}(S) = \min_{v \in S} \left( |\mathrm{lose}(v) \cap (S \setminus \{v\})| + \mathrm{cost}(S \setminus \{v\}) \right),$$

where $\mathrm{lose}(v) = \{ u : g(u, v) > 0 \}$. Sets are stored as bit masks.

```pseudo id=main
SLATER(P, m)
L1  lose[v] ← {u : g(u, v) > 0} for each v, from the margins of P
L2  cost[∅] ← 0
L3  for each nonempty S ⊆ A, in increasing order of its bit mask do
L4      cost[S] ← min over v ∈ S of |lose[v] ∩ (S \ {v})| + cost[S \ {v}]
L5  S ← A; r ← empty list
L6  while S ≠ ∅ do
L7      v ← the smallest v ∈ S with |lose[v] ∩ (S \ {v})| + cost[S \ {v}] = cost[S]
L8      append v to r; S ← S \ {v}
L9  return r
```

The bit mask of $S \setminus \{v\}$ is smaller than that of $S$, so line L4 only reads entries that are already filled. Lines L5 to L8 rebuild an optimal ranking from the table. Taking the smallest $v$ that is optimal at each step gives the lexicographically first Slater ranking. A candidate is a Slater winner exactly when it passes the test of line L7 for $S = A$.

## Example

Take four candidates $a, b, c, d$ (indices 0 to 3) and 13 voters:

| voters | ranking |
|---|---|
| 4 | $d \succ b \succ c \succ a$ |
| 6 | $b \succ a \succ d \succ c$ |
| 3 | $c \succ a \succ d \succ b$ |

The majority arcs, with margins, are $b \to a$ (7), $b \to c$ (7), $d \to c$ (7), $a \to d$ (5), $c \to a$ (1) and $d \to b$ (1). They form the cycles $a \to d \to b \to a$ and $a \to d \to c \to a$, so there is no Condorcet winner, and all four candidates are in the [Smith set](/smith-set/). The test of line L7 for $S = A$ gives:

| first $v$ | arcs into $v$ | best ranking of the rest | total |
|---|---|---|---|
| $a$ | $b \to a$, $c \to a$: 2 | $d \succ b \succ c$: 0 | 2 |
| $b$ | $d \to b$: 1 | $\{a, c, d\}$ is a cycle: 1 | 2 |
| $c$ | $b \to c$, $d \to c$: 2 | $\{a, b, d\}$ is a cycle: 1 | 3 |
| $d$ | $a \to d$: 1 | $b \succ c \succ a$: 0 | 1 |

So $\mathrm{cost}(A) = 1$, the only Slater ranking is $d \succ b \succ c \succ a$, and $d$ wins. It reverses only the arc $a \to d$. [Kemeny's rule](/kemeny-rank-aggregation/) weighs each reversed arc by its margin. It prefers $b \succ a \succ d \succ c$, which reverses $d \to b$ and $c \to a$, of margin 1 each, for a weight of 2 against 5 for the Slater ranking. So the two rules elect different candidates on this profile.

## Correctness

The recursion of line L4 is correct because in any ranking of $S$ with first element $v$, the pairs that include $v$ cost exactly $|\mathrm{lose}(v) \cap (S \setminus \{v\})|$, and the other pairs are a ranking of $S \setminus \{v\}$, which costs at least $\mathrm{cost}(S \setminus \{v\})$ and can cost exactly that. Lines L5 to L8 follow optimal choices, so the ranking they build has cost $\mathrm{cost}(A)$. The proof in `proofs/correctness.md` gives the details and proves the properties below.

## Complexity

Counting the margins takes $O(n m^2)$ time. The table has $2^m$ entries, and each entry tries at most $m$ candidates with $O(1)$ word operations: one AND and one population count on an $m$-bit mask, which fits in a word when $m$ is at most the word size of the [word RAM](/word-ram/). Lines L5 to L8 take $O(m^2)$ time. The total is $O(n m^2 + 2^m m)$ time and $O(2^m)$ space. Trying all $m!$ rankings instead would take $O(m! \, m^2)$ time.

Finding a Slater ranking, or deciding whether a candidate is a Slater winner, is NP-hard, so no polynomial algorithm is expected. For approximations of feedback arc set in tournaments, see [Kemeny rank aggregation](/kemeny-rank-aggregation/), which treats the weighted version, and [KwikSort](/kwiksort-rank-aggregation/), which gives an expected ratio of 3 for the unweighted version with random pivots.

## Properties

The proofs are in `proofs/correctness.md`, and the tests check each property on all profiles with up to 4 candidates and few voters and on random profiles with up to 6 candidates.

- **Smith set on top.** Every Slater ranking puts the whole [Smith set](/smith-set/) above all other candidates. So the Slater winners lie in the Smith set, and a Condorcet winner is the only winner.
- **Pareto.** If every voter ranks $a$ above $b$, then every Slater ranking puts $a$ above $b$, so $b$ does not win.
- **Monotone.** Moving a winner up on one ballot keeps it a winner.
- **Anonymous, and neutral as a correspondence.** Only the majority graph is used. The resolute rule is not neutral, because of the tie rule.
- **A tournament solution.** The result depends only on the majority graph. So two profiles with the same majorities but very different margins have the same Slater rankings, unlike [Kemeny's rule](/kemeny-rank-aggregation/).
- **Manipulable.** The tests find a voter who gains by a false ranking with 3 candidates and 3 voters.

## Variants and improvements

- **Kemeny's rule.** Weigh each reversed arc by its margin. This is the weighted feedback arc set problem on the same graph, and the same subset program solves it with sums of margins in place of counts.
- **Integer programs.** Exact solvers for larger $m$ use the integer program with one variable for each ordered pair and a constraint for each triple that forbids a cycle of length 3.
- **Approximation.** KwikSort, which sorts by majorities with random pivots, has an expected ratio of 3 for feedback arc set in tournaments.
- **Ties in the majority graph.** With $n$ even, some pairs have margin 0. This page charges nothing for them. Other versions charge one half in either order, which gives the same rankings.

## When to use it

Use Slater's rule when only the outcomes of pairwise contests are known or trusted, as in round-robin tournaments in sport or in comparisons by judges. For elections with full ballots, Kemeny's rule uses more of the information. With up to about 20 candidates, the subset program is exact and fast; beyond that, use an integer program solver or an approximation.

## Pitfalls

- **Ranking by wins.** Sorting candidates by their number of majority wins, the Copeland score, is not the Slater ranking, even when it has no ties.
- **Counting margins.** The cost counts reversed arcs, not their margins. Using margins gives Kemeny's rule, which can elect a different candidate, as in the example.
- **The memory of the table.** The table has $2^m$ entries. For $m = 30$, that is about a billion entries, too many for most machines.
- **Ties.** Several rankings can be optimal, and their tops can differ. Return the set of winners, or state the tie rule.

## Implementations

## History

Patrick Slater posed the problem in 1961 for paired comparisons, where a judge compares every pair of items and the comparisons may be inconsistent. He asked for the ranking with the fewest inconsistencies. The rule later became one of the standard tournament solutions in social choice. The minimum feedback arc set problem in tournaments was shown to be NP-hard in the mid-2000s, which settled the complexity of the Slater ranking and of the Slater winner. Work on approximation for the same problem gave KwikSort in 2005.

## References
