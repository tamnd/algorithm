---
tag: X5X0T8
kind: algorithm
slug: scout-search
name: SCOUT
aliases:
- SCOUT algorithm
area: games-and-search/game-tree-search
level: advanced
summary: Pearl's game-tree search. It finds the value of the first move, then tests each later move with a yes-or-no search, and searches a move for its value only if the test shows that it is better.
solves: [game-tree-evaluation]
model: word-ram
complexity:
  vars: {b: the branching factor, d: the depth in plies}
  time: {worst: O(d b^d), best: O(b^(d/2))}
  space: {extra: O(b d)}
properties: {deterministic: true, recursive: true}
prereqs: [alpha-beta-pruning]
see_also: [principal-variation-search, knuth-moore-theorem, mtdf, sss-star, aspiration-search, move-ordering, transposition-table]
sources:
  - paper: "Judea Pearl, SCOUT: a simple game-searching algorithm with proven optimal properties, Proceedings of the First Annual National Conference on Artificial Intelligence (AAAI-80), Stanford (1980)"
    title: Pearl 1980, AAAI
    locator: pp. 143 to 145 (EVAL and TEST in Section II, the branching factor results in Section III, the table of SCOUT and alpha-beta on Kalah)
  - paper: doi:10.1016/0004-3702(80)90037-5
    title: Judea Pearl, Asymptotic properties of minimax trees and game-searching procedures, Artificial Intelligence 14(2) (1980)
    locator: pp. 113 to 138 (SCOUT and TEST in full, with the proofs of the branching factor and of optimality among directional algorithms)
  - paper: doi:10.3233/icg-1983-6402
    title: Alexander Reinefeld, An improvement to the Scout tree search algorithm, ICCA Journal 6(4) (1983)
    locator: pp. 4 to 14 (NegaScout, which merges TEST and EVAL into one search with a null window)
  - paper: doi:10.1016/0004-3702(83)90001-2
    title: Murray S. Campbell and T. Anthony Marsland, A comparison of minimax tree search algorithms, Artificial Intelligence 20(4) (1983)
    locator: pp. 347 to 367 (SCOUT compared with alpha-beta and its variants on strongly ordered trees)
---

SCOUT is a [game tree](/game-tree/) search by Judea Pearl that computes the [minimax](/minimax/) value with two procedures. SCOUT finds the exact value of a node. TEST answers only a yes-or-no question: is the value of this node greater than $v$? To find the value of a node, SCOUT finds the value of its first child, then tests each later child against the best value so far. A child that fails the test, which is the usual case when the moves are well ordered, is never searched for its value. A child that passes the test is searched again by SCOUT, so some leaves are evaluated twice. TEST is cheap because it can stop at the first child that proves the answer, like an [alpha-beta](/alpha-beta-pruning/) search with a window of zero width. Pearl introduced SCOUT in 1980 as a tool for analysis: with it he proved that random game trees can be searched with the optimal branching factor. It is the direct ancestor of [principal variation search](/principal-variation-search/), which merges the two procedures into one.

## In plain words

You look at your first move carefully and find out exactly how good it is.

For each other move, you do not ask "how good is it?". You ask a simpler question: "is it better than my first move?". A simple question has a fast answer. To show that a move is not better, it is enough to find one good reply for the opponent. You do not need the best reply.

Most of the time the answer is no, and you go on to the next move. If the answer is yes, you now look at this move carefully, and it becomes the move to beat. That costs some work twice, but if your first guesses are usually good, it does not happen often.

## The problem

The input is a finite [game tree](/game-tree/) of a two-player [zero-sum game](/zero-sum-game/) with perfect information, with a function EVALUATE on the terminal nodes, or on the nodes at the depth limit. As on the [negamax](/negamax/) page, every value is for the side to move at that node, and $N(n) = \max_c(-N(c))$ for an inner node $n$. The output is $N(\text{root})$. This is the [game tree evaluation](/game-tree-evaluation/) problem.

## The algorithm

```pseudo id=main
SCOUT(n)
L1  if n is terminal then return EVALUATE(n)
L2  v ← −SCOUT(c₁)                ▷ c₁ is the first child
L3  for each later child c of n, in order, do
L4      if not TEST(c, −v, ≥) then   ▷ −N(c) > v: c is strictly better
L5          v ← −SCOUT(c)
L6  return v

TEST(n, v, rel)                   ▷ true iff N(n) rel v, where rel is > or ≥
L7  if n is terminal then return EVALUATE(n) rel v
L8  for each child c of n, in order, do
L9      if not TEST(c, −v, the other relation) then return true
L10 return false
```

In the negamax form both questions turn into each other one level down: $N(n) > v$ holds iff some child has $N(c) < -v$, which is "not $N(c) \ge -v$". So a node that tests with $>$ asks its children a question with $\ge$, and the other way round. TEST stops at the first child that proves the claim. If no child proves it, the claim is false.

Pearl describes SCOUT in the MAX and MIN view, with EVAL in place of SCOUT. A MAX node tests whether $V(S_k) > v$ for each later child. A MIN node exempts a child from evaluation when $V(S_k) \ge v$. It is the same rule.

## Example

Take the tree of the [alpha-beta](/alpha-beta-pruning/) page. MAX is at the root A, MIN at B and C, and MAX at D, E, F and G. The leaves, as values for MAX, are 3 and 17 under D, 19 and 12 under E, 2 and 5 under G, and 15 and 25 under F. The children are in the order B, C at A, D, E at B and G, F at C.

| step | call | question or result | leaves evaluated |
| --- | --- | --- | --- |
| 1 | SCOUT(D) | first leaf 3; test 17: is 17 better than 3? yes; search 17 | 3, 17, 17 |
| 2 | D | value 17 | |
| 3 | TEST(E) | for MIN at B: is E below 17? the leaf 19 proves no | 19 |
| 4 | B | value 17, E is exempt | |
| 5 | TEST(C) | for MAX at A: is C above 17? G is 5 at most, so no | 2, 5 |
| 6 | A | value 17, C is exempt | |

The leaf 17 is evaluated twice: once by the test, and once more for its value. SCOUT evaluates 6 leaves, 5 of them distinct. Alpha-beta in the same order evaluates the same 5 distinct leaves. The tests check this run, leaf by leaf.

In tic-tac-toe from the empty board, with the squares tried in reading order, SCOUT evaluates 7194 terminal positions, repeats counted, and alpha-beta evaluates 7330. On 20000 random binary trees of depth 4 with integer leaves from $-9$ to 9, SCOUT made 379471 leaf evaluations, 232268 of them on distinct leaves, and alpha-beta made 234984.

## Correctness

The [proof](proofs/correctness/) shows by induction on the height that TEST$(n, v, >)$ is true iff $N(n) > v$, and TEST$(n, v, \ge)$ is true iff $N(n) \ge v$. With this, SCOUT keeps the invariant that after it handles the first $j$ children, $v$ is the best score among them: a child is searched at line L5 exactly when it is strictly better, and otherwise it cannot change the maximum. After the last child, $v = N(n)$.

The tests compare SCOUT with negamax on random uniform and irregular trees with integer and fraction leaves, with and without a depth limit, and on tic-tac-toe positions. They check TEST against the two inequalities for values at, below and above the true value. They check that on uniform trees with the best move first SCOUT evaluates exactly the minimal tree, and two trees on which SCOUT and alpha-beta each evaluate a leaf that the other skips.

## Complexity

Costs are in the [word RAM](/word-ram/), with each move generation and EVALUATE counted as $O(1)$, on a uniform tree of branching factor $b$ and depth $d$.

**Worst case.** TEST visits at most the $b^d$ leaves below its node. If every later child passes its test, SCOUT at a node of height $h$ costs $T(h) \le b\,T(h-1) + (b-1)\,b^{h-1}$, which solves to $T(d) \le b^d (1 + d(b-1)/b)$. So the time is $O(d\, b^d)$. Unlike alpha-beta, SCOUT can evaluate a leaf more than once, so its worst case is above $b^d$.

**Best case.** If the first child of every node is best, every test fails and no child is searched twice. Then SCOUT evaluates the minimal tree of the [Knuth-Moore theorem](/knuth-moore-theorem/), $b^{\lceil d/2 \rceil} + b^{\lfloor d/2 \rfloor} - 1$ leaves, the same leaves as alpha-beta. The tests check this on uniform trees up to depth 6.

**Random trees.** On uniform trees with independent random leaf values from a continuous distribution, Pearl proved that SCOUT has the branching factor $\xi_b / (1 - \xi_b)$, where $\xi_b$ is the positive root of $x^b + x - 1 = 0$, and that no directional algorithm can do better. The extra work of the repeated searches is too small to change the branching factor. He also proved that TEST alone is optimal among directional algorithms that test the value of the root against a bound. For leaves with discrete values the branching factor of SCOUT is $b^{1/2}$, except in one special case.

**Space.** Both procedures keep only the current path, so the space is $O(bd)$ with a list of children per call, the same as alpha-beta.

## Properties

- **Exact.** It returns the minimax value. TEST returns only a yes or a no.
- **Directional.** Each procedure visits the leaves from left to right, though SCOUT may visit a leaf again in a later pass.
- **Not comparable with alpha-beta leaf by leaf.** Pearl noted that SCOUT can evaluate leaves that alpha-beta skips, and the other way round. The tests contain one tree of each kind.
- **Small memory.** Like alpha-beta it keeps only the path to the current node. Pearl compared this with [SSS*](/sss-star/), which needs a large list of open nodes.
- **Depends on the order.** With good [move ordering](/move-ordering/), few tests pass and SCOUT is close to the minimal tree. With bad order, many children are searched twice.

## Variants and improvements

- **TEST as alpha-beta.** TEST$(n, v, >)$ is true iff an alpha-beta search of $n$ with any window $(v, \beta)$ returns more than $v$. With $\beta$ just above $v$, this is a null-window search, and it prunes as much as TEST.
- **Return a bound from TEST.** Pearl noted that a test that passes could also return a new bound, to save work in the search that follows. Reinefeld's NegaScout does this: it merges TEST and SCOUT into one procedure with an alpha-beta window. This is [principal variation search](/principal-variation-search/), the form that programs use.
- **Memory.** With a [transposition table](/transposition-table/), the second search of a child can reuse the results of its test. [MTD(f)](/mtdf/) carries this to the end, with only null-window searches.
- **Windows at the root.** [Aspiration search](/aspiration-search/) applies a narrow window to the whole search, in place of a test at each child.

## When to use it

Use SCOUT to understand and to analyse null-window search: the proofs of its branching factor are simpler than those for alpha-beta. In a program, use [principal variation search](/principal-variation-search/), which keeps the idea and avoids most of the repeated work, together with good [move ordering](/move-ordering/) and a [transposition table](/transposition-table/). Plain SCOUT does well on deep searches with good move order. In Pearl's Kalah table it was ahead of alpha-beta from depth 4 on with random move order, and from depth 5 on with dynamic order.

## Pitfalls

- **The relations.** A node that tests with $>$ must ask its children with $\ge$, and the other way round. With the same relation at all levels, ties come out wrong.
- **The test at line L4.** Searching a child again when it only ties the best value wastes work. Searching it only when it is strictly better is correct, because a tie does not change the maximum.
- **Repeated work.** A child that passes its test is searched twice. With bad move order this can cost more than plain alpha-beta. Order the moves, or use a [transposition table](/transposition-table/) to share the work.
- **No bound from the test.** TEST gives only a yes or a no, so a search that follows a passed test starts from nothing. Principal variation search fixes this by keeping the bound.
- **Evaluation from a fixed side.** In the negamax form, EVALUATE must score for the side to move, as on [negamax](/negamax/).

## Implementations

## History

Judea Pearl introduced SCOUT in 1980, in a report at UCLA that became his paper on the asymptotic properties of minimax trees in Artificial Intelligence, and in a short paper at the first AAAI conference. He built it first as a tool for analysis. With SCOUT he showed that random uniform trees can be evaluated with the branching factor $\xi_b/(1 - \xi_b)$, which Baudet had shown to be a lower bound for alpha-beta, and that no directional algorithm can do better. In 1982 Pearl showed that alpha-beta reaches the same branching factor. Tests on the game of Kalah, in a UCLA report by T. Noe, showed that SCOUT can also be faster than alpha-beta in practice. Reinefeld (1983) improved SCOUT into NegaScout, and Marsland and Campbell gave the closely related principal variation search. Campbell and Marsland (1983) compared SCOUT with alpha-beta and the other search algorithms of the time.

## References
