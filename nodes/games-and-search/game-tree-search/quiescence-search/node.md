---
tag: F29MJX
kind: algorithm
slug: quiescence-search
name: Quiescence search
aliases:
- quiescence extension
area: games-and-search/game-tree-search
level: advanced
summary: Extends the search at the leaves through noisy moves, such as captures, until the position is stable.
solves: [game-tree-evaluation]
model: word-ram
complexity:
  vars: {b: the branching factor, d: the nominal depth in plies, k: the length of the longest chain of captures}
  time: {worst: O(b^(d+k))}
  space: {extra: O(b (d + k))}
properties: {deterministic: true, recursive: true}
prereqs: [alpha-beta-pruning, evaluation-function, horizon-effect]
see_also: [search-extensions, null-move-pruning, futility-pruning, move-ordering, iterative-deepening-search, principal-variation-search, pruning]
sources:
  - paper: doi:10.1080/14786445008521796
    title: Claude E. Shannon, Programming a computer for playing chess, Philosophical Magazine, Series 7, 41(314) (1950)
    locator: pp. 256 to 275 (the type B strategy, which applies the evaluation only in relatively quiescent positions and follows forceful variations further)
  - paper: doi:10.1016/0004-3702(90)90072-8
    title: Don F. Beal, A generalised quiescence search algorithm, Artificial Intelligence 43(1) (1990)
    locator: pp. 85 to 98 (quiescence search with null moves, a revised version of the 1989 paper on the null move)
  - url: https://apps.dtic.mil/sti/tr/pdf/AD0784881.pdf
    title: Hans J. Berliner, Chess as Problem Solving, The Development of a Tactics Analyzer, PhD thesis, Carnegie-Mellon University (1974)
    locator: the chapter on the horizon effect (the negative and the positive horizon effect of a search that stops at a fixed depth and then looks only at captures)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, 4th edition, Pearson (2020)
    locator: Chapter 5, Adversarial Search and Games (the part on heuristic alpha-beta tree search, cutting off the search and quiescence)
---

Quiescence search is the part of a depth-limited game search that runs after the nominal depth is used up. It does not apply the [evaluation function](/evaluation-function/) to a position at once. It goes on through the *noisy* moves only, usually the captures and sometimes the promotions and checks, until it reaches a *quiet* position in which the static score can be trusted. At each node the side to move may *stand pat*, that is, decline all captures and take the static score. The search is an [alpha-beta](/alpha-beta-pruning/) search of this smaller "capture or stop" game, so it costs little, and it removes the worst cases of the [horizon effect](/horizon-effect/), in which the program counts a piece it has just captured and does not see the recapture.

## In plain words

A chess program looks a fixed number of moves ahead and then scores the board by counting material. This goes wrong when the last move it looks at is a capture. The program sees "I won a pawn" and stops, but the very next move takes back its queen.

Quiescence search fixes this. When the normal search stops, the program keeps going, but only with captures. Each side may also say "I stop here" and keep the current score, because nobody has to capture. The search ends when no side wants to capture any more. Only then is the score used.

There are few captures in most positions, so this extra search is small. It does not see quiet threats, such as a mate or a fork, but it sees all the simple trades.

## The problem

The input is a position $n$, a nominal depth $d$, a function EVALUATE that gives the static score for the side to move, and a rule that marks some moves as captures. Every chain of captures must be finite, which is true when each capture removes a piece. The output is the depth-$d$ [negamax](/negamax/) value of $n$ in which each frontier position gets the quiescence value
$$ Q(n) = \max\Bigl(\text{EVALUATE}(n),\ \max_{c} \bigl(-Q(c)\bigr)\Bigr) $$
instead of its static score, with $c$ over the positions after one capture from $n$. The first term is the stand-pat option. $Q$ is the exact negamax value of a game in which the side to move either captures or stops, so it is a value of a well-defined game and not only a heuristic number. It is not the value of the real game, because quiet moves after the frontier are not searched.

## The algorithm

```pseudo id=main
QUIESCE(n, α, β)                    ▷ values for the side to move at n
L1  stand ← EVALUATE(n)            ▷ the stand-pat score
L2  if stand ≥ β then return stand
L3  m ← stand, α ← max(α, stand)
L4  for each capture c of n, best capture first do
L5      t ← −QUIESCE(c, −β, −α)
L6      if t > m then m ← t
L7      if m ≥ β then return m
L8      α ← max(α, m)
L9  return m

SEARCH(n, d, α, β)                  ▷ fail-soft alpha-beta with a quiescence frontier
L10 if n is terminal then return EVALUATE(n)
L11 if d = 0 then return QUIESCE(n, α, β)
L12 m ← −∞
L13 for each move to a child c of n do m ← max(m, −SEARCH(c, d − 1, −β, −max(m, α)))
L14     if m ≥ β then return m
L15 return m
```

Lines L1 to L3 are the stand pat. The side to move is never forced to capture, so the static score is a lower bound on $Q(n)$, and if it already reaches $\beta$ the node fails high at once (line L2). This early exit is the main reason why quiescence search is cheap. Lines L4 to L8 are an ordinary alpha-beta loop over the captures. Programs order the captures with the most valuable victim first and, among equal victims, the least valuable attacker first (MVV-LVA), which is common engine practice and gives early cutoffs.

The procedure SEARCH is the normal [negamax](/negamax/) alpha-beta search; only line L11 is new. Without quiescence, line L11 would return EVALUATE($n$).

## Example

White is to move at A, and the static score is 0. Move 1 is QxP: the queen takes a pawn, and the static score is now $+1$ for White. But the pawn is defended by a rook, and Black can take the queen. Move 2 is a quiet move that keeps the score at 0. The numbers are the static scores for White (the tests store them for the side to move).

| line | after White's move | after Black's best reply | true value for White |
| --- | --- | --- | --- |
| QxP | $+1$ | RxQ: $+1 - 9 = -8$ | $-8$ |
| quiet move | $0$ | quiet: $0$ | $0$ |

A depth-1 search without quiescence scores QxP at $+1$ and the quiet move at 0, so it plays QxP and loses the queen. This is the horizon effect. With quiescence, line L11 calls QUIESCE on the position after QxP. Black's stand pat is $-1$, but the capture RxQ gives Black $+8$, so $Q = 8$ for Black and $-8$ for White. The quiet position has no captures, so its $Q$ is its static score 0. The search now plays the quiet move, which is right.

The tests also measure the effect on random trees. The instance is 200 lazy random "material games" with seeds 20000 to 20199, branching factor 3 and height 6, in which a move is a capture with probability 0.35 and wins 1, 3, 3, 5 or 9 points, and a quiet move changes the score by $-1$, 0 or $+1$. A depth-2 search was compared with the exact value of the whole tree. Without quiescence, the root value was wrong in 164 trees, with a total error of 347 points, and the search visited 1938 nodes. With quiescence, it was wrong in 150 trees, with a total error of 298 points, and it visited 3774 nodes. So quiescence made the value better here, but not exact, because the quiet moves after the frontier still change the result.

## Correctness

The [proof](proofs/correctness/) shows by induction on the length of the longest capture chain that QUIESCE($n, \alpha, \beta$) returns a *fail-soft* answer for $Q(n)$: a value $r$ with $Q(n) \le r \le \alpha$ when $Q(n) \le \alpha$, $r = Q(n)$ when $\alpha < Q(n) < \beta$, and $\beta \le r \le Q(n)$ when $Q(n) \ge \beta$.

- **Stand pat.** The stop option is always there, so EVALUATE$(n) \le Q(n)$, and the return at line L2 is a correct fail-high.
- **The capture loop.** It is the alpha-beta loop, with the stand-pat score as the starting value of $m$ instead of $-\infty$.
- **Equivalence.** With the full window, QUIESCE returns exactly the negamax value of the tree in which each node gets one more leaf child "stop" with its static score. The tests check this against a plain recursive solver at every node of the top four levels (depths 0 to 3) of 40 random trees, 1600 nodes in all.

SEARCH is alpha-beta on the tree cut at depth $d$, and its frontier values are fail-soft answers, so SEARCH returns the depth-$d$ value with $Q$ at the frontier. The tests check this against a brute force on 500 random trees with depths 0 to 3.

## Complexity

The costs are in the [word RAM](/word-ram/), with each call of EVALUATE and of the move generator counted as $O(1)$.

**Time.** In the worst case each frontier node starts a full capture tree, so the search can visit $O(b^{d+k})$ nodes, where $k$ is the length of the longest capture chain. In chess $k$ is at most the number of pieces, about 30. In practice the stand-pat cutoff at line L2 and the small number of captures make the quiescence part a fraction of the whole search, but the share depends on the program and on the position, and we give no general number.

**Space.** The active calls lie on one path of at most $d + k$ moves, so the extra space is $O(b(d + k))$ with a move list per call.

## Properties

- **A value of a game.** $Q$ is the exact value of the capture-or-stop game, so a quiescence search can be checked against a brute force.
- **The static score is a lower bound.** Stand pat makes $Q(n) \ge$ EVALUATE$(n)$. The search assumes that the side to move always has a quiet move that keeps the score, which is false in zugzwang and false when the side to move is in check.
- **Selective.** It searches only the noisy moves, so it is a form of [pruning](/pruning/) of the quiet moves below the frontier. It is not exact for the real game.
- **Stable at the frontier.** Its values change less from one depth to the next than the static scores do, which helps [iterative deepening](/iterative-deepening-search/) and [aspiration windows](/aspiration-search/).

## Variants and improvements

- **Check evasions.** When the side to move is in check, stand pat is not allowed, because the side has no free quiet move. The node must search all evasions, and a node with no evasion is mate.
- **Checks in the first ply.** Some programs also search checking moves in the first one or two plies of quiescence, to see simple mates.
- **Delta pruning.** Skip a capture when even the static score plus the value of the captured piece plus a margin cannot reach $\alpha$. It is the [futility pruning](/futility-pruning/) idea inside quiescence, and it is a heuristic.
- **Static exchange evaluation.** Compute the result of the whole exchange on one square without a search, and skip the captures that lose material. This is common engine practice; we have not seen a primary source for it.
- **Null-move quiescence.** Beal (1990) gave a generalised quiescence search in which the side to move may also play a null move, so that threats against it are seen.
- **[Transposition table](/transposition-table/) probes** in quiescence, which some programs use and others skip because the nodes are cheap.

## When to use it

Use quiescence search in every depth-limited search of a game in which single moves change the evaluation by large amounts, such as captures in chess, shogi and checkers. It is not needed when the evaluation is stable from move to move, and it is not used by [Monte Carlo tree search](/monte-carlo-tree-search/), which plays moves to the end of the game or uses a learned evaluation.

## Pitfalls

- **Stand pat in check.** If the side in check may stand pat, the search can miss a mate. Generate evasions instead.
- **Explosion.** If quiet checks, or all moves, are added to the quiescence moves, the capture-or-stop game becomes the full game and the search does not finish. Keep the move set small, and add depth limits for checks.
- **Wrong capture order.** With a bad order, the capture loop gets few cutoffs. MVV-LVA or a static exchange score is the usual order.
- **Mate and stalemate.** A position with no legal moves is not quiet, it is terminal. Test for it before stand pat, as line L10 of SEARCH does.
- **Fail-hard and fail-soft mixed.** QUIESCE on this page returns fail-soft values. If the caller expects values clamped to the window, convert them.

## Implementations

## History

Shannon (1950) already noted that an evaluation function for chess can only be applied in relatively quiescent positions, and his type B strategy follows the forceful variations, such as captures, further than the others. Berliner (1973, 1974) gave the name horizon effect to the errors that a search with a fixed depth still makes, and he showed that a capture search at the frontier does not remove all of them. Beal (1990) generalised the quiescence search with null moves, so that the search also sees threats. The details used by programs today, such as MVV-LVA, delta pruning and check evasions, are engine practice that is described in program documentation and on the Chess Programming Wiki rather than in one paper.

## References
