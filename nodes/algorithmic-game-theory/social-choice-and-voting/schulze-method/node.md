---
tag: PFHMFN
kind: algorithm
slug: schulze-method
name: Schulze method
aliases:
- beatpath method
- Schwartz sequential dropping
area: algorithmic-game-theory/social-choice-and-voting
level: core
summary: Elects the candidate whose strongest path of pairwise majorities to each rival is at least as strong as the reverse, using the widest path variant of Floyd-Warshall.
model: word-ram
complexity:
  vars: {n: the number of voters, m: the number of candidates}
  time: {worst: O(n m^2 + m^3)}
  space: {extra: O(m^2)}
properties: {deterministic: true, comparison: false, recursive: false}
history:
  year: 1997
  people: [Markus Schulze]
  note: "Schulze proposed the method in 1997 on an election methods mailing list and published the full analysis in Social Choice and Welfare in 2011."
prereqs: [condorcet-winner, widest-path, floyd-warshall]
see_also: [ranked-pairs, copeland-method, smith-set, slater-rule, condorcet-paradox, preference-profile, voting-manipulation-problem, election-control-problem]
sources:
  - paper: doi:10.1007/s00355-010-0475-4
    title: "Markus Schulze, A new monotonic, clone-independent, reversal symmetric, and Condorcet-consistent single-winner election method, Social Choice and Welfare 36(2) (2011), 267-303"
    locator: "the definition by strongest paths, the proof that the relation it defines is transitive, the properties, and the O(C^3) algorithm for C candidates"
  - book: isbn:9781107060432
    title: "Felix Brandt, Vincent Conitzer, Ulle Endriss, Jérôme Lang and Ariel D. Procaccia (eds.), Handbook of Computational Social Choice, Cambridge University Press, 2016"
    locator: "Chapter 4 (Felix Fischer, Olivier Hudry and Rolf Niedermeier, Weighted tournament solutions), Section 4.5.2, Schulze's method and its computation with widest paths in O(m^3) time; Chapter 6 (Vincent Conitzer and Toby Walsh, Barriers to manipulation), the polynomial-time manipulation of Schulze's method by one voter"
  - paper: doi:10.1016/0022-0531(88)90253-0
    title: "Hervé Moulin, Condorcet's principle implies the no show paradox, Journal of Economic Theory 45(1) (1988), 53-64"
    locator: "the theorem that no Condorcet consistent rule satisfies participation when there are at least 4 candidates and 25 voters"
---

The Schulze method is a Condorcet method that settles majority cycles by looking at chains of majorities. Candidate $a$ has a path to $b$ when $a$ beats some $c_1$, $c_1$ beats $c_2$, and so on, until the last one beats $b$. The strength of a path is its weakest majority. The method compares the strongest path from $a$ to $b$ with the strongest path from $b$ to $a$, and elects a candidate that is never worse in this comparison. All strongest paths together are a [widest path](/widest-path/) problem, which a version of [Floyd-Warshall](/floyd-warshall/) solves in $O(m^3)$ time. The Wikimedia Foundation and several Pirate Parties use the method.

## In plain words

Two candidates may be linked not only by their own head-to-head result but also through others: if most voters prefer A to B and most prefer B to C, then A has a chain of wins that leads to C. A chain is only as strong as its narrowest win. For each pair of candidates, the method finds the strongest chain in each direction and lets the stronger direction decide. A candidate wins if no rival has a stronger chain against it than it has against that rival. One such candidate always exists. A candidate that beats everyone directly always wins, and when wins go round in a circle, the narrowest win in the circle counts the least.

## The problem

There are $m$ candidates $A = \{0, \ldots, m - 1\}$ and $n$ voters with rankings, each best first. Let $n_P(a, b)$ be the number of voters who rank $a$ above $b$, and $g(a, b) = n_P(a, b) - n_P(b, a)$ the margin. The weighted majority graph has a link $a \to b$ of strength $g(a, b)$ whenever $g(a, b) > 0$. The strength of a path is the smallest strength of its links, and $p(a, b)$ is the largest strength of a path from $a$ to $b$, or 0 if there is none. Candidate $a$ beats $b$ in the Schulze relation when $p(a, b) > p(b, a)$. The Schulze winners are the candidates that no other candidate beats in this relation: $W(P) = \{ a : p(a, b) \ge p(b, a) \text{ for all } b \ne a \}$. Ties go to the candidate with the smallest index, as on every rule page of this area.

## The algorithm

```pseudo id=main
SCHULZE(P, m)
L1  g[a][b] ← n_P(a, b) - n_P(b, a) for all a ≠ b
L2  p[a][b] ← g[a][b] if g[a][b] > 0, else 0, for all a ≠ b
L3  for k ← 0 to m - 1 do
L4      for each i ≠ k with p[i][k] > 0, and each j ∉ {i, k} do
L5          p[i][j] ← max(p[i][j], min(p[i][k], p[k][j]))
L6  W ← {a : p[a][b] ≥ p[b][a] for every b ≠ a}
L7  return the smallest candidate in W
```

Line L2 keeps only the links of the weighted majority graph. Lines L3 to L5 are [Floyd-Warshall](/floyd-warshall/) with the sum replaced by the minimum and the minimum replaced by the maximum: a path through $k$ is as strong as the weaker of its two halves, and $p[i][j]$ keeps the stronger of the old value and the new path. The test $p[i][k] > 0$ skips rows where no path through $k$ can help. Line L6 collects the candidates that no rival beats, and line L7 applies the tie rule. The code also returns a full ranking: it repeatedly takes the smallest remaining candidate that no remaining candidate beats.

## Example

Take four candidates $a, b, c, d$ (indices 0 to 3) and 26 voters, the profile of the example on the [ranked pairs](/ranked-pairs/) page:

| voters | ranking |
|---|---|
| 3 | $a \succ b \succ c \succ d$ |
| 6 | $c \succ d \succ a \succ b$ |
| 11 | $b \succ c \succ d \succ a$ |
| 6 | $c \succ a \succ b \succ d$ |

The links of line L2 are $c \to d$ (26), $c \to a$ (20), $b \to d$ (14), $d \to a$ (8), $a \to b$ (4) and $b \to c$ (2). There is no Condorcet winner. The loop of lines L3 to L5 improves these entries:

| round $k$ | new paths |
|---|---|
| $a$ | $p[c][b] = 4$ by $c \to a \to b$; $p[d][b] = 4$ by $d \to a \to b$ |
| $b$ | $p[a][c] = 2$ by $a \to b \to c$; $p[a][d] = 4$ by $a \to b \to d$; $p[d][c] = 2$ by $d \to a \to b \to c$ |
| $c$ | $p[b][a] = 2$ by $b \to c \to a$ |
| $d$ | $p[b][a] = 8$ by $b \to d \to a$ |

The final strengths, row $x$ and column $y$ for $p[x][y]$:

| | $a$ | $b$ | $c$ | $d$ |
|---|---|---|---|---|
| $a$ | | 4 | 2 | 4 |
| $b$ | 8 | | 2 | 14 |
| $c$ | 20 | 4 | | 26 |
| $d$ | 8 | 4 | 2 | |

Candidate $c$ beats $a$ (20 against 2), $b$ (4 against 2) and $d$ (26 against 2), so $W = \{c\}$ and $c$ wins. The ranking is $c \succ b \succ d \succ a$. The direct result between $b$ and $c$ favours $b$ by 2, but $c$ reaches $b$ through $a$ with strength 4. Ranked pairs keeps the direct result and elects $b$ on this profile, so the two methods are different rules.

## Correctness

After round $k$ of the loop, $p[i][j]$ is the strength of the strongest path from $i$ to $j$ whose inner candidates are all among the first $k + 1$ candidates. This is the invariant of Floyd-Warshall, and it holds for the bottleneck measure because a strongest path through $k$ consists of a strongest path to $k$ and a strongest path from $k$, and the strength of a walk with a repeated candidate is at most the strength of the path that cuts out the loop. After the last round, $p[i][j] = p(i, j)$. The Schulze relation is transitive, so some candidate is beaten by no one and $W$ is not empty. The proof in `proofs/correctness.md` writes this out and proves the properties below.

## Complexity

Line L1 takes $O(n m^2)$ time, line L2 takes $O(m^2)$ and the three nested loops of lines L3 to L5 take $O(m^3)$. Line L6 takes $O(m^2)$. The total is $O(n m^2 + m^3)$ in the [word RAM](/word-ram/) model, with $O(m^2)$ extra space; the update of line L5 can be done in place, as in Floyd-Warshall. Real elections have few candidates, so the cubic loop is fast in practice.

## Properties

The proofs are in `proofs/correctness.md`, and the tests check each property by brute force over all profiles with up to 4 candidates and few voters, and on random profiles with up to 7 candidates.

- **The relation is transitive.** If $a$ beats $b$ and $b$ beats $c$, then $a$ beats $c$. So $W$ is never empty, and the relation extends to a ranking.
- **Condorcet and Smith consistent.** No path leads from outside the [Smith set](/smith-set/) into it, so every member beats every outsider in the Schulze relation.
- **Pareto.** If every voter ranks $a$ above $b$, then $a$ beats $b$ in the Schulze relation.
- **Anonymous, and neutral as a correspondence.** Only the margins are used, and renaming the candidates renames them. The resolute rule is not neutral, because of the tie rule.
- **Monotone.** Raising a winner on one ballot can only make its outgoing links stronger and its incoming links weaker, so it stays a winner.
- **Independent of clones and reversal symmetric.** Schulze proved both: adding a near copy of a candidate does not change which of the others wins, and if every ballot is reversed, a unique winner does not stay the winner.
- **No participation.** By Moulin's theorem, every Condorcet consistent rule, this one included, has profiles with at least 4 candidates where a voter does better by not voting.
- **Margins and winning votes agree on full rankings.** Schulze often uses the number of winning votes $n_P(a, b)$ as the link strength. With full rankings it is $(n + g(a, b))/2$, an increasing function of the margin, so both give the same relation.

## Variants and improvements

- **Winning votes and other strengths.** With ballots that leave candidates unranked, link strengths by winning votes, by margins or by ratios give different rules. Schulze recommends winning votes.
- **Sequential dropping.** Repeatedly restrict to the Schwartz set, the union of the minimal sets that no outsider beats, and drop the weakest remaining link. This is how the method was first described. The procedure is close to the path form, but the two are not always the same rule.
- **Ranked pairs.** [Ranked pairs](/ranked-pairs/) locks majorities greedily from the strongest down. Both rules are Condorcet consistent, monotone and independent of clones, and the example shows that they can disagree.
- **Proportional and multiwinner forms.** Schulze also defined a proportional ranking and a multiwinner version based on the same path strengths.

## When to use it

Use the Schulze method for single-winner elections with ranked ballots when you want a Condorcet winner whenever there is one, a defensible choice when there is not, and resistance to clones. Its count is easy to automate and to audit, since the strongest path table can be published. If voters must follow the count by hand, [ranked pairs](/ranked-pairs/) or [Copeland's method](/copeland-method/) is easier to explain.

## Pitfalls

- **Keeping negative links.** Line L2 must set $p[a][b] = 0$ when $g(a, b) \le 0$. A negative entry as a link makes $\min$ pick it, and then the maximum of line L5 can prefer a path that uses a lost contest.
- **Loop order.** The intermediate candidate $k$ must be the outermost loop, as in Floyd-Warshall. With $k$ inside, some paths are never found.
- **Testing only one direction.** A Schulze winner is a candidate with $p[a][b] \ge p[b][a]$ for every $b$. A candidate with the largest row sum or the largest single entry is not the same thing.
- **An unstated tie rule.** With few voters, $W$ often has several members. State the tie rule of line L7, or return $W$.

## Implementations

## History

Markus Schulze described the method in 1997 on a mailing list about election methods, first as a procedure that drops the weakest links one by one, and soon in its path form. It was adopted by many organizations that vote online, among them the Wikimedia Foundation and several Pirate Parties. Schulze published the full analysis in 2011, with proofs of transitivity, monotonicity, independence of clones and reversal symmetry, and with the cubic algorithm. In computational social choice, Parkes and Xia in 2012 and Gaspers and coauthors in 2013 showed that a manipulation by one voter can be found in polynomial time.

## References
