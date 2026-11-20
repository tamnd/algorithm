---
tag: SETRS2
kind: problem
slug: egalitarian-stable-matching
name: Egalitarian stable matching
aliases:
- optimal stable marriage
area: algorithmic-game-theory/matching-markets-and-market-equilibria
level: advanced
summary: Find a stable matching that minimizes the sum of the ranks of partners. Irving, Leather and Gusfield solve it by min cut on rotations.
model: word-ram
complexity:
  vars: {n: the number of men and of women}
  time: {worst: O(n^4)}
prereqs: [lattice-of-stable-matchings, stable-matching-rotations]
see_also: [stable-matching-rotations, lattice-of-stable-matchings, maximum-weight-closure, min-cut-problem, gale-shapley, stable-matching-with-ties, stable-roommates-problem, rural-hospitals-theorem]
sources:
  - paper: doi:10.1145/28869.28871
    title: Robert W. Irving, Paul Leather and Dan Gusfield, An efficient algorithm for the "optimal" stable marriage, Journal of the ACM 34(3), 532 to 543 (1987)
    locator: the whole paper (the O(n^4) algorithm through rotations and a minimum cut)
  - paper: doi:10.1137/0215048
    title: Robert W. Irving and Paul Leather, The complexity of counting stable marriages, SIAM Journal on Computing 15(3), 655 to 667 (1986)
    locator: the whole paper (rotations and the rotation poset)
  - paper: doi:10.1137/0216010
    title: Dan Gusfield, Three fast algorithms for four problems in stable marriage, SIAM Journal on Computing 16(1), 111 to 128 (1987)
    locator: the whole paper (the minimum regret stable matching and the listing of all stable matchings)
  - paper: doi:10.1007/BF03167200
    title: Akiko Kato, Complexity of the sex-equal stable marriage problem, Japan Journal of Industrial and Applied Mathematics 10(1), 1 to 19 (1993)
    locator: the whole paper (NP-hardness of the sex-equal problem)
  - book: isbn:9780262071185
    title: Dan Gusfield and Robert W. Irving, The Stable Marriage Problem, Structure and Algorithms, MIT Press (1989)
    locator: the chapter on optimal stable matchings
---

The egalitarian stable matching problem asks for the stable matching that is best for everyone on average: each person pays the rank of the partner in their own list, and the total over both sides must be as small as possible. It replaces the one-sided optimum of [deferred acceptance](/gale-shapley/) with a fair objective. It is solved in polynomial time by optimizing over the [lattice of stable matchings](/lattice-of-stable-matchings/) through its [rotations](/stable-matching-rotations/), which turns the problem into a [maximum-weight closure](/maximum-weight-closure/) and so a [minimum cut](/min-cut-problem/). Close objectives that look just as simple, such as balancing the costs of the two sides, are NP-hard.

## In plain words

In a stable matching, nobody wants to break up and pair with someone who also wants them more. There can be many stable matchings. Deferred acceptance gives the one that is best for the side that proposes and worst for the other side. To be fair to both sides, give each person a score: one if they get their first choice, two for their second choice, and so on. Add up the scores of all people. The egalitarian stable matching is the stable matching with the smallest total. Trying all stable matchings is too slow, because there can be very many. But the stable matchings have a neat structure that turns the search into a flow problem, which is fast to solve.

## Definition

An instance has $n$ men and $n$ women. Each person ranks all people of the other side in a strict order. Let $r_m(w)$ be the position of $w$ in the list of $m$ (1 for the first choice), and define $r_w(m)$ in the same way. The *egalitarian cost* of a perfect matching $\mu$ is
$$c(\mu) = \sum_{m} r_m(\mu(m)) + \sum_{w} r_w(\mu(w)).$$
The task is to find a stable matching of minimum egalitarian cost. The output is the matching; the measure is $c$.

The *weighted* version (the "optimal stable marriage" of Irving, Leather and Gusfield) gives each pair $(m, w)$ two weights, one for each person, that grow along each list, and minimizes the sum of the weights of the matched pairs.

## Variants

- **Incomplete lists.** People may list only some partners. Every stable matching matches the same people (by the [rural hospitals theorem](/rural-hospitals-theorem/)), so the cost is still well defined, and the same algorithm applies.
- **Minimum regret.** Minimize the largest rank that any person gets. Gusfield (1987) solved it in $O(n^2)$ time by walking down the lattice.
- **Sex-equal stable matching.** Minimize the difference between the men's total rank and the women's total rank. Kato (1993) proved it NP-hard.
- **Ties.** With ties in the lists and weak stability, finding a weakly stable matching of minimum egalitarian cost is NP-hard; see [stable matching with ties](/stable-matching-with-ties/).
- **Roommates.** The egalitarian version of the [stable roommates problem](/stable-roommates-problem/) is NP-hard, although a stable matching, if one exists, is found in polynomial time.

## Examples

Four men and four women with these lists:

| person | list | | person | list |
|---|---|---|---|---|
| $m_1$ | $w_2, w_3, w_1, w_4$ | | $w_1$ | $m_1, m_4, m_2, m_3$ |
| $m_2$ | $w_3, w_1, w_2, w_4$ | | $w_2$ | $m_4, m_2, m_3, m_1$ |
| $m_3$ | $w_2, w_4, w_1, w_3$ | | $w_3$ | $m_3, m_2, m_1, m_4$ |
| $m_4$ | $w_4, w_2, w_1, w_3$ | | $w_4$ | $m_2, m_3, m_4, m_1$ |

There are exactly three stable matchings. All three contain the pair $m_1 w_1$.

| stable matching | other pairs | men's total | women's total | cost |
|---|---|---|---|---|
| $A$ (man-optimal) | $m_2 w_3$, $m_3 w_2$, $m_4 w_4$ | 6 | 9 | 15 |
| $B$ | $m_2 w_3$, $m_3 w_4$, $m_4 w_2$ | 8 | 6 | 14 |
| $C$ (woman-optimal) | $m_2 w_4$, $m_3 w_3$, $m_4 w_2$ | 13 | 4 | 17 |

The egalitarian stable matching is $B$, which neither proposing order of deferred acceptance finds. The lattice is the chain $A, B, C$, with two rotations. The first, $(m_3, w_2), (m_4, w_4)$, moves $m_3$ to $w_4$ and $m_4$ to $w_2$; it changes the cost by $+2$ for the men and $-3$ for the women, so by $-1$. The second, $(m_2, w_3), (m_3, w_4)$, moves $m_2$ to $w_4$ and $m_3$ to $w_3$; it changes the cost by $+5 - 2 = +3$. The best closed set of rotations is the first rotation alone, which gives $B$.

## Known algorithms

- **Enumeration.** List all stable matchings with Gusfield's algorithm in $O(n^2 + n N)$ time, where $N$ is their number, and take the best. This is exponential in the worst case, since $N$ can be exponential in $n$.
- **Rotations and minimum cut (Irving, Leather and Gusfield 1987).** Compute the man-optimal matching and the rotation poset, which has $O(n^2)$ rotations. Give each rotation the change in cost that its elimination causes; the cost of a stable matching is the cost of the man-optimal matching plus the weights of the rotations in its closed set. Finding a closed set of minimum total weight is a maximum-weight closure problem, solved by one minimum cut in a network with a node per rotation. The total time is $O(n^4)$. The method works for every weighted version in which the cost is a sum over people of a function of their own partner.
- **Minimum regret (Gusfield 1987).** $O(n^2)$ time, also with rotations.

## Bounds

- The problem is solvable in polynomial time, although the number of stable matchings can be exponential and counting them is #P-complete (Irving and Leather 1986).
- The input has size $\Theta(n^2)$, so $\Omega(n^2)$ time is needed; the gap to the $O(n^4)$ bound comes from the minimum cut.
- Objectives that are not sums of individual costs can be hard: the sex-equal problem is NP-hard, and so is the egalitarian problem with ties.

## Reductions

- **To maximum-weight closure.** The stable matchings correspond one to one to the closed sets (down-sets) of the rotation poset, and the egalitarian cost is additive over rotations. So the problem is a [maximum-weight closure](/maximum-weight-closure/) problem with weights $-\Delta(\rho)$, where $\Delta(\rho)$ is the change in cost by rotation $\rho$. The rotation poset is a [directed acyclic graph](/directed-acyclic-graph/), and the closure problem reduces to a [minimum cut](/min-cut-problem/) by the [max-flow min-cut theorem](/max-flow-min-cut-theorem/).
- **From the man-optimal matching.** The rotations and their poset are found from one run of [deferred acceptance](/gale-shapley/) and a walk from the man-optimal to the woman-optimal matching.

## Applications

Knuth (1976) posed the problem of finding a fair stable matching, and the egalitarian cost is the most used fairness measure for stable marriage. It serves as a compromise between the two one-sided optima in matching markets where both sides are people and both sides' welfare counts. It is also the standard example of optimizing a linear function over a distributive lattice given by a poset of rotations.

## References
