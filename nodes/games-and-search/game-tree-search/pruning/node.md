---
tag: CJHSNE
kind: concept
slug: pruning
name: Pruning in game trees
aliases:
- cutoff
area: games-and-search/game-tree-search
level: intro
summary: Skipping a subtree of a game tree search. Sound pruning skips only what provably cannot change the root value; forward pruning skips what looks unpromising and can be wrong.
prereqs: [game-tree, minimax]
see_also: [alpha-beta-pruning, search-tree-pruning, futility-pruning, null-move-pruning, knuth-moore-theorem, move-ordering, late-move-reductions, bounding-function]
sources:
  - paper: doi:10.1016/0004-3702(75)90019-3
    title: Donald E. Knuth and Ronald W. Moore, An analysis of alpha-beta pruning, Artificial Intelligence 6(4) (1975)
    locator: pp. 293 to 326 (shallow and deep cutoffs, the proof that alpha-beta returns the minimax value, and the least number of leaves that any proof of the value needs)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition
    locator: Chapter 5, Section 5.2 (alpha-beta pruning, with a worked tree of three MIN nodes, and move ordering) and Section 5.3 (forward pruning, beam search and ProbCut)
  - paper: doi:10.3233/ICG-1995-18202
    title: Michael Buro, ProbCut, an effective selective extension of the alpha-beta algorithm, ICCA Journal 18(2) (1995)
    locator: pp. 71 to 76 (forward pruning by a shallow search that predicts the result of a deep one, with a statistical test)
---

Pruning in a game tree means skipping a part of the tree during a search: the program decides not to look at some moves, or stops looking at a position before all its moves are searched. There are two kinds, and they differ in what they promise. *Sound* pruning skips a subtree only when it is proved that the subtree cannot change the [minimax](/minimax/) value of the root. The cutoffs of [alpha-beta pruning](/alpha-beta-pruning/) are of this kind, and the search returns exactly the same value as a full search. *Forward* pruning skips moves that look bad by some estimate, such as [null-move pruning](/null-move-pruning/) and [futility pruning](/futility-pruning/). It saves much more work, but it can skip the best move and change the result. This page is about pruning in game trees only. Pruning in backtracking, where a branch is cut because it cannot lead to a valid solution, is [search tree pruning](/search-tree-pruning/), and pruning by bounds in optimization is the job of the [bounding function](/bounding-function/) in branch and bound.

## In plain words

You are choosing between two moves. You look at the first one carefully and see that it gets you at least a draw. Then you look at the second one, and the first reply of your opponent that you try beats you. You can stop there: the second move is worse than the first, whatever the other replies are. You did not look at them, and you did not need to. That is sound pruning.

Strong players also skip moves that look silly without checking them at all. This saves a lot of time, and it is almost always right. But now and then the silly-looking move was the best one. That is forward pruning.

## The idea

### When a subtree cannot matter

The root value is a function of the values of the leaves. A subtree $S$ cannot matter, given the leaves read so far, if the root value is the same for every assignment of values to the leaves of $S$. Sound pruning skips only such subtrees.

Alpha-beta finds these subtrees with two bounds. At each node it keeps $\alpha$, the best value that MAX is sure of on the path from the root, and $\beta$, the best that MIN is sure of. The value of a node matters only if it lies strictly between $\alpha$ and $\beta$.

- **Shallow cutoff.** At a MAX node with $\alpha = 3$ from its first child, the second child is a MIN node. If its first child has value 2, the MIN node is worth at most 2, which is below 3, so its other children are skipped.
- **Deep cutoff.** The bound can come from a node higher up than the parent. A MIN node three plies below the root can be cut by an $\alpha$ that MAX got at the root, because every MAX node in between will pass the low value up only if nothing better is found, and the root already has better.

Knuth and Moore (1975) proved that alpha-beta returns the minimax value. They also showed that any method that proves the value of a uniform tree with branching factor $b$ and depth $d$ must read at least $b^{\lceil d/2 \rceil} + b^{\lfloor d/2 \rfloor} - 1$ leaves, and that alpha-beta reads exactly that many when the best move is searched first everywhere; see the [Knuth-Moore theorem](/knuth-moore-theorem/). With the worst order, alpha-beta prunes nothing. So how much sound pruning happens depends on [move ordering](/move-ordering/), and the value does not.

### Forward pruning

Forward pruning decides before the search, or after a cheap search, that a move is not worth searching in full. The decision uses an [evaluation function](/evaluation-function/) or a shallow search, so it is only an estimate.

| method | what it skips | when it can be wrong |
| --- | --- | --- |
| beam (keep the $k$ best moves by a static score) | all other moves | the best move has a poor static score |
| [futility pruning](/futility-pruning/) | quiet moves near the leaves whose static score plus a margin cannot reach $\alpha$ | a quiet move gains more than the margin |
| [null-move pruning](/null-move-pruning/) | a subtree, if giving the opponent a free move and searching less deep still fails high | zugzwang, where every legal move is worse than passing |
| ProbCut (Buro 1995) | a subtree, if a shallow search predicts with high probability that the deep search would fail high or low | the shallow result is a poor predictor in this position |
| [late move reductions](/late-move-reductions/) | nothing; late moves are searched less deep | a late move is good only at full depth |

Late move reductions reduce depth instead of pruning, and they search a move again at full depth when the reduced search shows it is good; they are listed here because they share the risk. None of these methods has a worst-case guarantee. They are used because, with good move ordering, the moves they skip are almost never the best ones, and the saved time buys a deeper search.

### Sound and forward pruning compared

| | sound pruning | forward pruning |
| --- | --- | --- |
| result | the same value as a full search | can differ from a full search |
| based on | bounds from moves already searched | estimates: static scores, shallow searches |
| leaves read | at best about $2\sqrt{n}$ of the $n$ leaves of a uniform tree | can be far fewer, with no bound on the error |
| examples | alpha-beta, Scout, [SSS*](/sss-star/), [MTD(f)](/mtdf/) | beam, futility, null move, ProbCut |

### With chance nodes

At a node that averages over chance outcomes, one bad outcome does not settle the value, so the shallow cutoff above does not work. A sound cutoff is still possible if the leaf values have known bounds, because then the average of the unseen outcomes is bounded too. The [expectiminimax](/expectiminimax/) page treats this.

## Examples

**A shallow cutoff.** MAX moves at the root to one of three MIN nodes, whose leaves are 3, 12, 8; then 2, 4, 6; then 14, 5, 2. Alpha-beta reads 3, 12 and 8, so the first MIN node is worth 3 and $\alpha = 3$. Under the second MIN node it reads 2. That node is now worth at most 2, below 3, so the leaves 4 and 6 are skipped. Under the third MIN node it reads 14, 5 and 2 and gets 2. The root value is 3, after 7 of the 9 leaves. If the MIN node with the leaves 3, 12, 8 comes last, no cutoff happens and alpha-beta reads all 9 leaves; the value is still 3. These counts were checked by a short script.

**Forward pruning gives a wrong move.** MAX has two moves, A and B. A static score rates A at 5 and B at 3. After A, MIN chooses between leaves 1 and 9; after B, between 4 and 6. The minimax values are 1 for A and 4 for B, so B is the best move. A beam of width 1 at the root keeps only A, by the static score, and plays it, for a value of 1 instead of 4. Sound pruning cannot make this mistake.

**Null move in zugzwang.** MAX is to move in a position where every legal move leads to a position of value $-1$ for MAX, but passing would keep the value 0. The search window is $\beta = 0$. Null-move pruning lets MAX pass, searches the result, gets 0, sees that $0 \ge \beta$, and cuts the node as if MAX were at least at 0. The true value is $-1$. This is why null-move pruning is switched off, or checked again, in endgames where zugzwang is common.

## Where it is used

- **Game programs.** Every chess, checkers and Othello program combines sound alpha-beta cutoffs with forward pruning and depth reductions. The forward pruning methods are tuned by testing on games, not proved.
- **Exact solvers.** Programs that [solve games](/solved-game/) use only sound pruning, since a wrong cutoff gives a wrong proof. [Proof-number search](/proof-number-search/) stops at a node as soon as its value is proved.
- **Analysis of search.** The bounds of the Knuth-Moore theorem, and the gap between best and worst move ordering, are statements about how much sound pruning is possible.
- **Other areas.** Backtracking and branch and bound prune by feasibility and by bounds on an objective; see [search tree pruning](/search-tree-pruning/) and [bounding function](/bounding-function/). The game-tree case is different because the bound comes from the other player's best reply.

## References
