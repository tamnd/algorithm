---
tag: E1V4HN
kind: algorithm
slug: even-paz-algorithm
name: Even-Paz algorithm
aliases:
- Even-Paz divide and conquer
area: algorithmic-game-theory/fair-division
level: core
summary: A proportional cake cutting protocol that cuts at the median of the agents' half-value marks and recurses on each half, with O(n log n) queries.
solves: [cake-cutting-problem]
model: robertson-webb-query-model
complexity:
  vars: {n: the number of agents}
  time: {worst: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: true, online: false}
prereqs: [proportional-division, robertson-webb-query-model, divide-and-choose]
see_also: [last-diminisher, dubins-spanier-moving-knife, edmonds-pruhs-lower-bound, cake-cutting-problem, merge-sort, median, recursion-tree-method, envy-freeness]
sources:
  - paper: doi:10.1016/0166-218X(84)90005-2
    title: Shimon Even and Azaria Paz, A note on cake cutting, Discrete Applied Mathematics 7(3) (1984)
    locator: pp. 285-296 (the divide and conquer protocol with O(n log n) cuts, and the randomized protocol with O(n) expected cuts)
  - paper: doi:10.1145/2000807.2000819
    title: Jeff Edmonds and Kirk Pruhs, Cake cutting really is not a piece of cake, ACM Transactions on Algorithms 7(4) (2011)
    locator: Article 51; Section 2, Theorem 4 (the matching lower bound for deterministic protocols)
  - book: isbn:9781107060432
    title: Felix Brandt, Vincent Conitzer, Ulle Endriss, Jerome Lang and Ariel D. Procaccia (eds.), Handbook of Computational Social Choice, Cambridge University Press, 2016
    locator: Chapter 13, Ariel D. Procaccia, Cake Cutting Algorithms, Section 13.3, classic algorithms (from p. 313), and Section 13.4, complexity of cake cutting (from p. 316)
---

The Even-Paz algorithm is a divide and conquer protocol for [proportional division](/proportional-division/) of a [cake](/cake-cutting-problem/) among $n$ agents. Each agent marks the point that splits the current piece in the ratio $\lfloor n/2 \rfloor : \lceil n/2 \rceil$ by its own measure. The cake is cut at the median mark: the agents with the smaller marks share the left part, the others share the right part, and each group repeats the method. Each agent gets a connected piece worth at least $1/n$ to it. The protocol uses $O(n \log n)$ queries in the [Robertson-Webb query model](/robertson-webb-query-model/), and the [Edmonds-Pruhs lower bound](/edmonds-pruhs-lower-bound/) shows that no deterministic protocol does better.

## In plain words

A large group of friends shares a cake. Instead of cutting one fair slice at a time, they split the group in two. Each friend draws a line where the cake splits into a left part that is fair for half of the group and a right part that is fair for the other half, as that friend sees it. The cake is cut at the middle line of all the lines.

The friends whose lines are left of the cut think the left part is big enough for half the group, so they take it. The other friends think the same of the right part. Each half then does the same thing on its own part, until each friend is alone with a piece. Because the group halves each time, each friend draws only a few lines.

## The problem

The cake is $[0, 1]$. Agent $i \in \{1, \dots, n\}$ has a nonnegative, additive and nonatomic valuation $V_i$ with $V_i([0, 1]) = 1$. The protocol must output disjoint intervals $X_1, \dots, X_n$ that cover $[0, 1]$, with $V_i(X_i) \ge 1/n$ for every $i$. It learns the valuations only by queries: $\mathrm{Eval}_i(a, b)$ returns $V_i([a, b])$, and $\mathrm{Cut}_i(a, t)$ returns the least point $x \ge a$ with $V_i([a, x]) = t$.

## The algorithm

The recursive call gets a set $S$ of $k$ agents and an interval $[a, b]$. It guarantees that each agent $i \in S$ gets at least $V_i([a, b])/k$. The first call is $\textsc{Even-Paz}(\{1, \dots, n\}, [0, 1])$, where $V_i([0, 1]) = 1$ is known and needs no query.

```pseudo id=main
EVEN-PAZ(S, [a, b])                         ▷ each i in S gets at least V_i([a, b]) / |S|
L1  if |S| = 1 then give [a, b] to the agent of S; return
L2  k ← |S|; k1 ← ⌊k/2⌋
L3  for each agent i of S do
L4      w_i ← EVAL_i(a, b)                    ▷ no query at the root, where w_i = 1
L5      m_i ← CUT_i(a, w_i · k1/k)            ▷ [a, m_i] is worth k1/k of [a, b] to i
L6  sort S by (m_i, i)
L7  x ← the k1-th mark; L ← the first k1 agents; R ← the other k − k1 agents
L8  EVEN-PAZ(L, [a, x])
L9  EVEN-PAZ(R, [x, b])
```

The cut point $x$ is a median of the marks: $k_1$ marks are at most $x$, and the other $k - k_1$ marks are at least $x$. Ties go to the agent with the smaller index, so the split of $S$ into $L$ and $R$ is well defined. For $k = 2$ the call is a form of [divide and choose](/divide-and-choose/) in which both agents mark their half points and the cake is cut at the smaller mark.

## Example

Split $[0, 1]$ into four equal segments, and let the densities be $(1, 1, 1, 1)$ for agent 1, $(0, 1, 1, 2)$ for agent 2, $(2, 2, 0, 0)$ for agent 3 and $(1, 0, 0, 3)$ for agent 4. Each list sums to 4, so each agent values the whole cake at 1.

| call | agents | $w_i$ | marks $m_i$ | cut $x$ | left group | right group |
|---|---|---|---|---|---|---|
| $[0, 1]$ | 1, 2, 3, 4 | 1, 1, 1, 1 | $1/2, 3/4, 1/4, 5/6$ | $1/2$ | 3, 1 | 2, 4 |
| $[0, 1/2]$ | 1, 3 | $1/2, 1$ | $1/4, 1/4$ | $1/4$ | 1 | 3 |
| $[1/2, 1]$ | 2, 4 | $3/4, 3/4$ | $13/16, 7/8$ | $13/16$ | 2 | 4 |

In the second call, both marks are $1/4$, and the tie goes to agent 1. The pieces are $[0, 1/4]$ for agent 1, $[1/4, 1/2]$ for agent 3, $[1/2, 13/16]$ for agent 2 and $[13/16, 1]$ for agent 4. Their values for the owners are $1/4$, $1/2$, $3/8$ and $9/16$, all at least $1/4$. The run makes 8 cut queries and 4 eval queries, 12 in total. The result is not [envy-free](/envy-freeness/): agent 1 values the piece of agent 2 at $5/16$.

## Correctness

**Claim.** A call on $S$ and $[a, b]$ gives each agent $i \in S$ a piece worth at least $V_i([a, b])/|S|$ to it.

The proof is by induction on $k = |S|$. For $k = 1$ the agent gets all of $[a, b]$. For $k \ge 2$, let $w = V_i([a, b])$. If $i \in L$, then $m_i \le x$, so $V_i([a, x]) \ge V_i([a, m_i]) = w k_1/k$, and the call on $L$ gives $i$ at least $(w k_1 / k)/k_1 = w/k$. If $i \in R$, then $m_i \ge x$, so $V_i([a, x]) \le w k_1/k$ and $V_i([x, b]) \ge w (k - k_1)/k$; the call on $R$ gives $i$ at least $w/k$. At the root, $w = 1$ and $k = n$, so each agent gets at least $1/n$. The full proof is in proofs/correctness.md.

## Complexity

A call on $k \ge 2$ agents makes $k$ cut queries and $k$ eval queries (none at the root), and then calls itself on $\lfloor k/2 \rfloor$ and $\lceil k/2 \rceil$ agents. With $T(1) = 0$ and $T(k) = 2k + T(\lfloor k/2 \rfloor) + T(\lceil k/2 \rceil)$, the protocol makes $T(n) - n$ queries, because the root skips its $n$ evals. The recursion has depth $\lceil \lg n \rceil$, and each level asks each agent at most one cut and one eval. A closed form is
$$T(n) - n = 2n \lceil \lg n \rceil - 2^{\lceil \lg n \rceil + 1} + n \le 2n \lceil \lg n \rceil - n,$$
with equality when $n$ is a power of 2. For $n = 4$ this is 12, as in the example. The cut queries number at most $n \lceil \lg n \rceil$. So the cost is $\Theta(n \log n)$ on every input, the same shape as the cost of [merge sort](/merge-sort/). The sort of line L6 takes $O(k \log k)$ comparisons, which the query model does not count, and the extra space is $O(n)$ for the marks and the recursion.

## Properties

- **Connected pieces.** Each call cuts its interval at one point, so each agent gets one interval.
- **Safe for an honest agent.** The guarantee of $1/n$ for agent $i$ uses only the answers of agent $i$ and the choice of $x$ as a median. An agent that answers by its true valuation gets at least $1/n$ whatever the others answer.
- **Optimal query count.** The Edmonds-Pruhs lower bound shows that every deterministic proportional protocol needs $\Omega(n \log n)$ queries, even with pieces that are unions of intervals. Woeginger and Sgall had shown this before for connected pieces.
- **Not envy-free, not equitable.** The example shows envy, and the values of the agents differ.
- **Balanced recursion.** The split $\lfloor k/2 \rfloor : \lceil k/2 \rceil$ keeps the depth at $\lceil \lg n \rceil$. Any split $k_1 : k - k_1$ with $1 \le k_1 < k$ keeps the guarantee, but an unbalanced split costs more queries. The split $1 : k - 1$ gives a protocol much like the [Dubins-Spanier moving knife](/dubins-spanier-moving-knife/), with $\Theta(n^2)$ queries.

## Variants and improvements

- **No evals.** The evals of line L4 can be dropped. Give each agent a budget $B_i$ with $B_i \le V_i([a, b])$, starting at $B_i = 1$, and mark at $\mathrm{Cut}_i(a, B_i k_1/k)$. An agent in $L$ goes on with budget $B_i k_1/k$, and an agent in $R$ with budget $B_i (k - k_1)/k$, and the same induction shows that each agent gets at least $B_i/|S|$. This version uses at most $n \lceil \lg n \rceil$ cut queries and no eval query.
- **Randomized version.** Even and Paz also gave a randomized protocol with $O(n)$ expected cut queries. Edmonds and Pruhs showed that randomized protocols still need $\Omega(n \log n)$ queries when the answers are approximate.
- **Linear cuts.** A 2026 preprint by Arndt, Moseley, Im and Pruhs (arXiv 2606.07238) gives a deterministic protocol with $O(n)$ cut queries and $O(n^2)$ eval queries. It does not beat $\Omega(n \log n)$ queries in total, but it shows that cuts alone need not grow as $n \log n$.
- **Unequal shares.** When agent $i$ is entitled to a share $w_i$ instead of $1/n$, the same idea works with splits by entitlement instead of by count. The query complexity of this case was studied by Cseh and Fleiner.
- **Simpler quadratic protocols.** The [last diminisher](/last-diminisher/) and the Dubins-Spanier procedure use $\Theta(n^2)$ queries but give one piece per round, which is easier to run by hand.

## When to use it

Use Even-Paz when $n$ is large and queries are costly, for example when each query is a question to a person or a call to a slow model of preferences. It gives connected pieces and the best possible order of queries for deterministic proportional division. If envy matters, it is not enough: use an envy-free protocol such as [Selfridge-Conway](/selfridge-conway-procedure/) for three agents.

## Pitfalls

- **Marks of the wrong size.** Line L5 asks for a fraction $k_1/k$ of the value of the current interval $[a, b]$, not of the whole cake. With the whole cake as the base, the induction fails.
- **Odd $k$.** For odd $k$ the two groups differ in size. The mark must use $k_1/k$ with $k_1 = \lfloor k/2 \rfloor$, the size of the left group. A mark at value $1/2$ breaks the guarantee for the larger group.
- **Ties in the marks.** When several marks equal $x$, the agents with these marks must be split by a fixed rule so that exactly $k_1$ agents go left. Each agent with $m_i = x$ is safe in either group.
- **Recursion on the wrong side.** The left group must get $[a, x]$ and the right group $[x, b]$, with $x$ the $k_1$-th mark in sorted order. Swapping them gives no guarantee.

## Implementations

## History

Even and Paz published the protocol in 1984 in "A note on cake cutting", in Discrete Applied Mathematics. It improved the $\Theta(n^2)$ queries of the last diminisher (Steinhaus, 1948) and of the Dubins-Spanier procedure (1961) to $O(n \log n)$. The same paper gave a randomized protocol with $O(n)$ expected cuts. The question whether $O(n \log n)$ is optimal stayed open until Woeginger and Sgall (2007) proved $\Omega(n \log n)$ for connected pieces and Edmonds and Pruhs (SODA 2006; ACM Transactions on Algorithms 2011) proved it for all deterministic protocols.

## References
