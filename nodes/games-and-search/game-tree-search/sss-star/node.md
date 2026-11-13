---
tag: QXZG5Q
kind: algorithm
slug: sss-star
name: "SSS*"
aliases:
- SSS-star
- state space search star
area: games-and-search/game-tree-search
level: research
summary: Best-first search for the minimax value. It keeps a priority list of partial solutions and never evaluates a leaf that alpha-beta skips, but it needs much memory.
solves: [game-tree-evaluation]
model: word-ram
complexity:
  vars: {b: the branching factor, d: the depth in plies}
  time: {worst: O(d b^d log b), best: O(d b^⌈d/2⌉ log b)}
  space: {extra: O(b^⌈d/2⌉)}
properties: {deterministic: true, recursive: false}
prereqs: [priority-queue, alpha-beta-pruning]
see_also: [mtdf, knuth-moore-theorem, scout-search, principal-variation-search, best-first-search, a-star-search, proof-number-search, move-ordering]
sources:
  - paper: doi:10.1016/0004-3702(79)90016-x
    title: G. C. Stockman, A minimax algorithm better than alpha-beta?, Artificial Intelligence 12(2) (1979)
    locator: pp. 179 to 196 (the algorithm with the six cases of the operator Gamma, and the theorem that SSS* never evaluates a leaf that alpha-beta skips)
  - paper: doi:10.1016/s0004-3702(83)80010-1
    title: Igor Roizen and Judea Pearl, A minimax algorithm better than alpha-beta? Yes and no, Artificial Intelligence 21(1-2) (1983)
    locator: pp. 199 to 220 (the expected number of leaves of SSS* and alpha-beta on random trees)
  - paper: doi:10.1016/0020-0190(83)90061-3
    title: McGlinn, Is SSS* better than alpha-beta?, Information Processing Letters 16(3) (1983)
    locator: pp. 113 to 120
  - paper: doi:10.1016/0004-3702(83)90001-2
    title: Murray S. Campbell and T. Anthony Marsland, A comparison of minimax tree search algorithms, Artificial Intelligence 20(4) (1983)
    locator: pp. 347 to 367 (SSS* against alpha-beta and its variants on many kinds of trees)
  - paper: doi:10.1016/0004-3702(87)90019-1
    title: T. A. Marsland, A. Reinefeld and J. Schaeffer, Low overhead alternatives to SSS*, Artificial Intelligence 31(2) (1987)
    locator: pp. 185 to 199 (phased SSS* and other variants with less memory)
  - paper: doi:10.1016/0004-3702(95)00126-3
    title: Aske Plaat, Jonathan Schaeffer, Wim Pijls and Arie de Bruin, Best-first fixed-depth minimax algorithms, Artificial Intelligence 87(1-2) (1996)
    locator: pp. 255 to 293 (SSS* as a sequence of null-window alpha-beta searches with memory, MT-SSS*, and experiments)
---

SSS* is a best-first search for the [minimax](/minimax/) value of a game tree, from George Stockman (1979). It keeps a list OPEN of states, one for each node at the frontier of the search, with a merit $h$ that is an upper bound on the value the node can still give to the root. At each step it takes the state with the highest merit and works on it. So it looks first where the value of the root can still be the highest. Stockman proved that SSS* never evaluates a leaf that [alpha-beta](/alpha-beta-pruning/), with the same order of the moves, skips, and on many trees it evaluates fewer. The price is memory: OPEN can hold $b^{\lceil d/2 \rceil}$ states, and each step needs operations on a [priority queue](/priority-queue/). Plaat, Schaeffer, Pijls and de Bruin later showed that SSS* is the same as a sequence of null-window alpha-beta searches with a [transposition table](/transposition-table/) large enough to keep every node it stores, [MTD(f)](/mtdf/) with a first guess above every value.

## In plain words

You choose a move, then your opponent answers, many times. Each plan for you, one move at each of your turns, guarantees you some score. You want the plan with the best guarantee.

SSS* works on all your plans in parallel, and keeps for each one the best score it can still guarantee: at first, everything. It always works on the plan that looks best now. When a reply of the opponent turns out bad for that plan, its score goes down, and another plan can become the best one.

When the best plan has no more open questions, its score is the answer. No other plan can do better, since each of them already has a lower score.

## The problem

The input is a finite [game tree](/game-tree/) of a two-player [zero-sum game](/zero-sum-game/), with MAX to move at the root, an evaluation of the leaves, and a depth $d$; a node at depth $d$ counts as a leaf. The children of each node have a fixed order. The output is the minimax value of the root, the [game tree evaluation](/game-tree-evaluation/) problem.

A state is $(n, s, h)$: a node $n$, a status LIVE (not yet searched) or SOLVED (its value, capped at $h$, is known), and a merit $h$.

## The algorithm

```pseudo id=main
SSSSTAR(root)
L1  OPEN ← {(root, LIVE, +∞)}
L2  loop
L3      take (n, s, h) with the highest h from OPEN; ties go to the leftmost n
L4      if n = root and s = SOLVED then return h
L5      if s = LIVE then
L6          if n is a leaf then insert (n, SOLVED, min(h, f(n)))
L7          else if n is a MIN node then insert (first child of n, LIVE, h)
L8          else for each child c of n do insert (c, LIVE, h)
L9      else if n is a MIN node then
L10         remove every state below the parent p of n; insert (p, SOLVED, h)
L11     else if n has a next sibling m then insert (m, LIVE, h)
L12     else insert (parent of n, SOLVED, h)
```

These are Stockman's six cases of the operator $\Gamma$. A MAX node puts all its children in OPEN at once (line L8): they are alternatives, and the best one wins. A MIN node searches its children one at a time, from left to right (lines L7 and L11): MAX needs a guarantee against every reply, so each child lowers the merit in turn, through the cap $\min(h, f(n))$ of line L6. When a child of a MAX node is solved with the highest merit in OPEN, no other child can beat it, so line L10 solves the MAX node and removes the rest of its subtree from OPEN. When the root is solved, its merit is the value.

## Example

The tree has MAX at the root A, MIN at B and C, and MAX at D and E below B and at G and F below C. The leaves are 19 and 8 under D, 23 and 11 under E, 25 and 22 under G, and 30 and 26 under F. Then D is 19, E is 23 and B is 19; G is 25, F is 30 and C is 25; the value is 25.

| step | state taken | case | what it inserts |
| --- | --- | --- | --- |
| 1 | (A, LIVE, ∞) | L8 | (B, LIVE, ∞), (C, LIVE, ∞) |
| 2 | (B, LIVE, ∞) | L7 | (D, LIVE, ∞) |
| 3 | (D, LIVE, ∞) | L8 | both leaves of D, LIVE, ∞ |
| 4, 5 | the leaves 19 and 8 | L6 | (19, SOLVED, 19), (8, SOLVED, 8) |
| 6 | (C, LIVE, ∞) | L7 | (G, LIVE, ∞) |
| 7 | (G, LIVE, ∞) | L8 | both leaves of G, LIVE, ∞ |
| 8, 9 | the leaves 25 and 22 | L6 | (25, SOLVED, 25), (22, SOLVED, 22) |
| 10 | (25, SOLVED, 25) | L10 | removes the leaf 22; (G, SOLVED, 25) |
| 11 | (G, SOLVED, 25) | L11 | (F, LIVE, 25) |
| 12 | (F, LIVE, 25) | L8 | both leaves of F, LIVE, 25 |
| 13 | the leaf 30 | L6 | (30, SOLVED, 25) |
| 14 | (30, SOLVED, 25) | L10 | removes the leaf 26; (F, SOLVED, 25) |
| 15 | (F, SOLVED, 25) | L12 | (C, SOLVED, 25) |
| 16 | (C, SOLVED, 25) | L10 | removes the leaves 19 and 8; (A, SOLVED, 25) |
| 17 | (A, SOLVED, 25) | L4 | returns 25 |

SSS* evaluates five leaves: 19, 8, 25, 22 and 30. After step 5, B has the merit 19 at most, and C stays above it, so SSS* never goes back to B. Alpha-beta in the same order evaluates six leaves: it must look at the leaf 23 of E to finish B, since it does not know yet that C is better. OPEN never holds more than 4 states here, $2^{\lceil 3/2 \rceil}$.

On 30 random trees with 4 moves per position, depth 6 and leaf values from $-1000$ to $1000$, SSS* evaluates 643 leaves on average and alpha-beta 922, of 4096. In tic-tac-toe from the empty board, with a win scored as 10 plus the number of empty squares, SSS* evaluates 6475 leaves and alpha-beta 8453, with at most 797 states in OPEN.

## Correctness

The [proof](proofs/correctness/) follows the merits. A LIVE state has as merit the smallest value of the left siblings, below MIN nodes, of the nodes on its path: an upper bound from the replies already searched. A SOLVED state has the value of its node, capped at that merit. A lemma shows that a subtree that is not solved yet always has a state in OPEN with a merit at least its capped value. So when line L10 takes the first solved child of a MAX node, it has the largest capped value of all the children, which is the capped value of the node. At the root, the cap is $+\infty$, so the result is the value. Each node gets at most one LIVE and one SOLVED state, so the loop stops.

The proof of Stockman's theorem shows that SSS* evaluates a leaf $\ell$ only if $\alpha(\ell) < \beta(\ell)$. Here $\alpha(\ell)$ is the best value of the left siblings, below MAX nodes, of the nodes on the path to $\ell$, and $\beta(\ell)$ is the smallest such value below MIN nodes. Alpha-beta evaluates every such leaf. The proof needs the rule that ties go to the left.

The tests compare SSS* with negamax on random uniform and irregular trees with integer and fraction leaves, with and without a depth limit. They check that no leaf is evaluated twice, and, on trees with many ties, that every leaf SSS* evaluates is one that alpha-beta evaluates too. They check the example, that MTD with a first guess above every value evaluates the same leaves in the same order, the bound $b^{\lceil d/2 \rceil}$ on OPEN, and tic-tac-toe.

## Complexity

Costs are in the [word RAM](/word-ram/), with each move generation and evaluation counted as $O(1)$, on a uniform tree of branching factor $b$ and depth $d$.

**Leaves.** SSS* evaluates at most the leaves that alpha-beta evaluates in the same order: all $b^d$ in the worst case, and the minimal tree of the [Knuth-Moore theorem](/knuth-moore-theorem/), $b^{\lceil d/2 \rceil} + b^{\lfloor d/2 \rfloor} - 1$ leaves, with the best order. On random trees, Roizen and Pearl showed that the saving over alpha-beta does not grow exponentially: both have the same asymptotic branching factor.

**Time.** Each node gets at most two states, so there are $O(b^d)$ steps. Each step is a heap operation on OPEN, $O(\log b^d) = O(d \log b)$, so the worst case is $O(d\, b^d \log b)$. The removals of line L10 are lazy in the code: a removed state stays in the heap, and a step skips it after an $O(d)$ check of the path. Every state taken from OPEN is at a node on the path to an evaluated leaf: a LIVE state taken has the highest merit and is the leftmost with it, so a state that it inserts below it is taken next, and so on down to a leaf, and a node is solved only after a leaf below it. Each step inserts one state, or $b$ at line L8. With the best order, SSS* evaluates only leaves of the minimal tree, which has $O(b^{\lceil d/2 \rceil})$ nodes, so $O(b^{\lceil d/2 \rceil})$ states are taken and, counting the $b$ children of each MAX node at line L8, also $O(b^{\lceil d/2 \rceil})$ are inserted. This gives the best case $O(d\, b^{\lceil d/2 \rceil} \log b)$. On best-ordered random trees, it took 3 to 5 steps per leaf.

**Space.** OPEN never holds more than $b^{\lceil d/2 \rceil}$ states, the number of leaves of a subtree that takes all children at MAX nodes and one at MIN nodes. The proof shows this. Alpha-beta needs only $O(d)$ space. The code keeps the removed states in the heap and a map from paths to positions, so it uses more memory than OPEN itself.

## Properties

- **Exact.** It returns the minimax value, for every order of the moves.
- **Dominates alpha-beta in leaves.** With the same order of the moves and ties to the left, every leaf it evaluates is one that alpha-beta evaluates.
- **Best-first.** The order of the work does not follow the tree from left to right: it jumps to the frontier state with the highest upper bound.
- **Not recursive.** The whole search state is in OPEN, not on a call stack.
- **Large memory.** OPEN can grow to $b^{\lceil d/2 \rceil}$ states, and each step needs a priority queue and a removal of whole subtrees.

## Variants and improvements

- **MT-SSS*.** The same search as a sequence of null-window alpha-beta searches with memory, as in [MTD(f)](/mtdf/), with the first test above every value. With enough memory it evaluates the same leaves in the same order, and it is easy to add to a program that has alpha-beta and a [transposition table](/transposition-table/).
- **DUAL*.** The dual algorithm: it keeps lower bounds and starts from the bottom, with MIN in the role of MAX. It is MTD with the first guess below every value.
- **Phased and staged SSS*.** Marsland, Reinefeld and Schaeffer (1987) split the work into phases to keep OPEN small.
- **Recursive SSS* and the solution-tree view.** Later work wrote SSS* as a recursive search over solution trees, without the six cases.

## When to use it

Use SSS* to study how much a best-first order can save over alpha-beta, or as a baseline in experiments on game-tree search. For a program, use [MTD(f)](/mtdf/), or [principal variation search](/principal-variation-search/) with [aspiration windows](/aspiration-search/): they search a comparable number of leaves with good move ordering, use a transposition table of fixed size, and combine with [iterative deepening](/iterative-deepening-search/).

## Pitfalls

- **The tie rule.** Stockman's theorem needs ties in OPEN to go to the leftmost state. Another rule still gives the value, but it can evaluate a leaf that alpha-beta skips.
- **Leaves, not interior nodes.** The theorem is about the leaves that are evaluated. It does not count the work on OPEN, which is much larger per leaf than the work of alpha-beta.
- **The removal of line L10.** Without it, old states below a solved MAX node stay in OPEN and come back later. With a heap, remove them lazily, and check each state when it is taken.
- **The cap at the leaves.** Line L6 inserts $\min(h, f(n))$, not $f(n)$. Without the cap, a leaf can get a merit above the bound of its plan and draw the search to it.
- **Memory with depth.** OPEN grows exponentially with the depth. A deep search runs out of memory long before it runs out of time.
- **The sign of the evaluation.** The six cases use the MAX view. With an evaluation for the side to move, as in negamax, negate it at MIN nodes.

## Implementations

## History

Stockman published SSS* in 1979, with the title "A minimax algorithm better than alpha-beta?", and proved that it never evaluates a leaf that alpha-beta skips. Campbell and Marsland (1983) compared it with alpha-beta and its variants on many kinds of trees, and found that its memory and its overhead per node cost more than the leaves it saves. Roizen and Pearl (1983) answered Stockman's title with "yes and no": SSS* never evaluates more leaves, but on random trees the saving does not change the asymptotic branching factor. McGlinn (1983) asked the same question in Information Processing Letters. Marsland, Reinefeld and Schaeffer (1987) gave variants with less memory. Plaat, Schaeffer, Pijls and de Bruin (1994 to 1996) showed that SSS* is a sequence of null-window alpha-beta searches with memory, and that this form, MT-SSS*, is practical. In their tests with real programs it was not better than the best alpha-beta variants, and they recommended [MTD(f)](/mtdf/) instead.

## References
