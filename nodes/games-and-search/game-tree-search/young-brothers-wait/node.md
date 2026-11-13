---
tag: QFBJRN
kind: concept
slug: young-brothers-wait
name: Young Brothers Wait
aliases:
- YBW
area: games-and-search/game-tree-search
level: research
summary: Parallel strategy that searches the first child sequentially before splitting the remaining children.
prereqs: [alpha-beta-pruning, knuth-moore-theorem, move-ordering]
see_also: [parallel-alpha-beta, principal-variation-search, transposition-table, work-stealing, speedup, minimax]
sources:
  - paper: "Rainer Feldmann, Burkhard Monien, Peter Mysliwietz and Oliver Vornberger, Distributed game-tree search, ICCA Journal 12(2) (1989)"
    locator: pp. 65 to 73 (the distributed alpha-beta search of the Paderborn group, in which a node is split only after its first child is searched)
  - paper: doi:10.1016/0004-3702(75)90019-3
    title: Donald E. Knuth and Ronald W. Moore, An analysis of alpha-beta pruning, Artificial Intelligence 6(4) (1975)
    locator: pp. 293 to 326 (the minimal tree, its nodes of types 1, 2 and 3, and its size b^ceil(d/2) + b^floor(d/2) - 1 at depth d)
  - paper: doi:10.1145/356893.356895
    title: T. Anthony Marsland and Murray S. Campbell, Parallel search of strongly ordered game trees, ACM Computing Surveys 14(4) (1982)
    locator: pp. 533 to 551 (principal variation splitting, which waits for the first child at the nodes of the principal variation only)
  - paper: doi:10.3233/ICG-1997-20102
    title: Robert M. Hyatt, The dynamic tree-splitting parallel search algorithm, ICCA Journal 20(1) (1997)
    locator: pp. 3 to 19 (DTS, a later method that also splits a node only after its first child is searched, and that chooses the split point dynamically)
---

Young Brothers Wait (YBW) is the rule of [parallel alpha-beta search](/parallel-alpha-beta/) that the younger children of a node, the "young brothers", may be given to other processors only after the first child, the "eldest brother", has been searched. The rule comes from the way [alpha-beta](/alpha-beta-pruning/) saves work. The value of the eldest brother either cuts off the node at once, so that the young brothers are not needed at all, or gives them a bound that makes their searches small. A young brother that starts before that bound is known can do much more work than in the sequential search; this extra work is the *search overhead*. With the best move first at every node, a search with the rule visits exactly the nodes of the sequential search on every number of processors, while a search without it does not. The rule was used in the distributed chess search of the Paderborn group (Feldmann, Monien, Mysliwietz and Vornberger, 1989), and dynamic tree splitting (Hyatt, 1997) keeps it too.

## In plain words

Several people search a game tree together. At each position, someone must first look at the most promising move alone. Only when that is done may the other moves of the position be shared out.

The reason is that the first answer tells the others what to beat. If the first move already decides the position, the other moves need no look at all. If it does not, the others get a clear bar, and most of them can stop early, as soon as they fall below it.

People who start on the other moves before the first answer is in have no bar. They work hard on moves that a single searcher would drop after a quick look. The wait costs some idle time, but it saves much more wasted work.

## The idea

**The rule.** In the pseudocode of [parallel alpha-beta](/parallel-alpha-beta/), a node $n$ with window $(\alpha, \beta)$ does three things in order:

1. It searches its first child $c_1$ alone, with the window $(-\beta, -\alpha)$, and gets $m = -\text{value}(c_1)$.
2. If $m \ge \beta$, it returns at once. No young brother is started.
3. Otherwise it offers $c_2, \ldots, c_k$ to idle processors. Each one reads the bound $\max(m, \alpha)$ when it starts, and a cutoff found by one of them cancels the others.

The rule says nothing about *which* processor takes the young brothers. That is the job of the scheduler, for example [work stealing](/work-stealing/). The rule is also not a full algorithm: programs add a split depth, below which a node is searched by one processor, and a limit on the number of split points.

**Why the eldest brother.** Knuth and Moore (1975) show that with the best move first, alpha-beta visits only the *minimal tree*, whose nodes are of three types:

- A node of type 1, a PV node, has an exact value. Its eldest child is of type 1, and its other children are of type 2.
- A node of type 2, a CUT node, fails high. Only its eldest child, of type 3, is searched, and it gives the cutoff.
- A node of type 3, an ALL node, fails low. All its children are searched, and all are of type 2.

The rule waits at all three types, and it costs nothing at each. At a CUT node the eldest brother gives the cutoff, so there are no young brothers to search. At a PV or ALL node, the bound after the eldest brother is already the final one: at a PV node it is the exact value, and at an ALL node it is $\alpha$, because every child fails low. So every young brother gets the same window as in the sequential search, whatever the time at which it starts.

**What happens without the rule.** At a CUT node, the young brothers start with the bound $\alpha$, not with the cutoff value, and they are searched in full or until the cancellation arrives. At a PV node they start with no bound from the eldest, so a brother that should be a small CUT node becomes a larger search.

**What the rule does not fix.** When the move order is wrong, the eldest brother of a CUT node fails low, and the cutoff comes from a young brother. The others may already be running, and their work up to the cancellation is overhead. The wait also puts the eldest brothers on a chain that no processor can share: the eldest brother of the root, its eldest brother, and so on down to a leaf. This chain limits the speedup.

## Examples

All numbers come from the deterministic simulator of the tests. Each node visit costs one time unit, idle processors take the newest ready task, and nodes of depth less than 2 are searched by one processor. The trees are lazy random game trees with branching factor 4 and height 6, seeded per node with Python's `random.Random`, and a move changes the score by $-9$ to $+9$. These are numbers for this model only.

**Perfect order.** The children of every node are sorted by their true value, best first. The tests use 20 such trees from the seeds 80000 to 80019, searched to depth 6. The minimal tree has $\sum_{k=0}^{6} (4^{\lceil k/2 \rceil} + 4^{\lfloor k/2 \rfloor} - 1) = 268$ nodes, and sequential alpha-beta visits exactly these 268 nodes in each tree, 5,360 in all.

| processors $P$ | nodes, with the rule | time steps, with the rule | nodes, without the rule | time steps, without the rule |
| --- | --- | --- | --- | --- |
| 1 | 5,360 | 5,360 | 5,360 | 5,360 |
| 2 | 5,360 | 3,200 | 8,619 | 4,339 |
| 4 | 5,360 | 1,840 | 13,887 | 3,494 |
| 8 | 5,360 | 1,420 | 18,681 | 2,374 |

With the rule the overhead is zero for every $P$, as the argument above predicts, and the tests check this on 90 trees with branching factors 2 to 4. With 8 processors the speedup is $5360 / 1420 \approx 3.8$, not 8, because of the chain of eldest brothers. Without the rule the search visits up to 3.5 times as many nodes, and it is slower on every $P$ in this table.

**Static order.** The tests also use 100 trees from the seeds 50000 to 50099 in which the moves are sorted only by their static score, so the order is often wrong. Sequential alpha-beta visits 38,839 nodes in all.

| processors $P$ | nodes, with the rule | time steps, with the rule | nodes, without the rule | time steps, without the rule |
| --- | --- | --- | --- | --- |
| 2 | 42,250 | 23,288 | 60,282 | 30,239 |
| 4 | 44,381 | 13,972 | 107,363 | 27,003 |
| 8 | 44,951 | 10,370 | 157,021 | 19,919 |

Now the rule has some overhead, from 8.8% to 15.7%, because a wrong eldest brother lets young brothers start with a poor bound. Without the rule the overhead is 55% to 304%. In both tables, and on 300 more random trees, the root value is the same as that of sequential alpha-beta, with and without the rule.

## Where it is used

- **Parallel alpha-beta.** The rule is the core of the Paderborn distributed search (Feldmann, Monien, Mysliwietz and Vornberger, 1989) and of dynamic tree splitting in Cray Blitz (Hyatt, 1997). The [parallel alpha-beta](/parallel-alpha-beta/) page gives the full search and its correctness proof.
- **Principal variation splitting.** Marsland and Campbell (1982) wait for the eldest brother only at the nodes of the [principal variation](/principal-variation/). YBW extends the wait to every node at which work is split.
- **Shared-memory chess programs.** Many programs before lazy SMP used a YBW split rule with a split depth and a pool of helper threads. This is program practice, and we have not seen a paper that surveys it.
- **Other tree searches with pruning.** The same rule fits any parallel [depth-first branch and bound](/depth-first-branch-and-bound/) in which the first branch gives the bound for the others.

## References
