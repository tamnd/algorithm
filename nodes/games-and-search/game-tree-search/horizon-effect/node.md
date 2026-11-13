---
tag: 86NNG4
kind: concept
slug: horizon-effect
name: Horizon effect
aliases:
- search horizon
area: games-and-search/game-tree-search
level: advanced
summary: Error where a depth-limited search misjudges a position because a consequence lies beyond the horizon.
prereqs: [minimax, evaluation-function, game-tree]
see_also: [quiescence-search, search-extensions, iterative-deepening-search, negamax, alpha-beta-pruning, null-move-pruning, pruning]
sources:
  - url: https://apps.dtic.mil/sti/tr/pdf/AD0784881.pdf
    title: Hans J. Berliner, Chess as Problem Solving, The Development of a Tactics Analyzer, PhD thesis, Carnegie-Mellon University (1974)
    locator: the chapter on the horizon effect (the definitions of the negative and the positive horizon effect, with chess examples)
  - paper: "Hans J. Berliner, Some necessary conditions for a master chess program, Proceedings of the Third International Joint Conference on Artificial Intelligence (IJCAI 1973), Stanford"
    locator: the part on the horizon effect, where the term is first used
  - paper: doi:10.1080/14786445008521796
    title: Claude E. Shannon, Programming a computer for playing chess, Philosophical Magazine, Series 7, 41(314) (1950)
    locator: pp. 256 to 275 (the remark that the evaluation can only be applied in relatively quiescent positions)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, 4th edition, Pearson (2020)
    locator: Chapter 5, Adversarial Search and Games (the part on cutting off the search, quiescence and the horizon effect)
---

The horizon effect is the error of a game search that stops at a fixed depth: an event that lies just past the last ply, the *horizon*, is not seen, and the [evaluation function](/evaluation-function/) scores the frontier position as if the event did not exist. Berliner gave the effect its name in 1973 and described two forms. In the *negative* horizon effect, the program cannot avoid a loss, but it can push the loss past the horizon with delaying moves, so it plays those moves, which often lose more. In the *positive* horizon effect, the program hurries to get a good result inside the horizon, though it would do better to wait. The simplest case of the effect is a capture that the search counts, with the recapture one ply too far. [Quiescence search](/quiescence-search/) and [search extensions](/search-extensions/) reduce the effect, but no search with a depth limit removes it.

## In plain words

A program that looks four moves ahead cannot see the fifth move. If the fifth move loses its queen, it does not know, and it scores the position as fine.

The effect is worse than a simple lack of sight. When the program sees that a loss is coming, it looks for moves that delay the loss until it falls out of view. For example, it gives away a pawn, which forces the opponent to spend a move to take it. The queen is still lost, but now the loss is past the limit, so the program thinks it lost only the pawn. In the end it loses the pawn and the queen.

Looking one move deeper does not fix this. The limit only moves, and the same thing happens one move later.

## The idea

Let the true value of a position be its [minimax](/minimax/) value in the whole game, and let a search with depth $d$ return the minimax value of the tree cut at depth $d$, with the static score at the cut. The two values differ when the static score at a frontier node is far from the true value of that node. A static score is a guess about the future. It is a good guess in a quiet position and a bad guess in the middle of a fight, for example when a piece is attacked or a capture has just been made.

The search does not only make the error at random frontier nodes. It looks for the nodes where the guess is wrong in its favour, because [minimax](/minimax/) picks the best value among many. So the errors at the frontier are not averaged out. They are selected:

- **A capture just past the horizon.** The last move of a line is a capture, and the static score counts the material, but the recapture comes one ply later.
- **The negative horizon effect.** In every line a loss comes, but in some lines it comes later. Each delaying move, such as a pawn sacrifice or a series of checks, pushes the loss past the horizon. The search prefers these lines and plays the delay, which costs extra material.
- **The positive horizon effect.** The search sees a gain inside the horizon and takes it at once, even when a quiet move first would make the gain larger or safer. The search cannot see the better gain later, so it takes the gain that it sees.

The fixes all make the search go deeper where the static score is not reliable:

- [Quiescence search](/quiescence-search/) goes on with captures at the frontier until the position is quiet. It removes the first case, but not threats made with quiet moves.
- [Search extensions](/search-extensions/) go one ply deeper after checks, recaptures and forced moves, so that the delaying moves cost the delayer depth.
- A generalised quiescence search with null moves (Beal 1990) also looks at the threats against the side to move.
- [Iterative deepening](/iterative-deepening-search/) does not fix the effect, but it gives a value from the previous depth that shows when the score changes a lot.

## Examples

**A capture just past the horizon.** White is to move. QxP takes a pawn, and Black's rook then takes the queen. A quiet move keeps the score at 0. A depth-1 search scores QxP at $+1$ and plays it. The true value of QxP is $-8$. With quiescence the frontier position after QxP gets the value of the capture-or-stop game, Black takes the queen, and the search plays the quiet move. The [quiescence search](/quiescence-search/) page gives the full table.

**A delaying sacrifice.** The white queen is trapped, and Black will win it in every line. The static scores are for White.

| line | moves | static score after the moves | true value |
| --- | --- | --- | --- |
| let | quiet move, RxQ | $-9$ | $-9$ |
| sac | pawn push, PxP, quiet move, RxQ | $-1$ after PxP, $-10$ after RxQ | $-10$ |

A depth-2 search sees RxQ in line "let" and only PxP in line "sac", so it scores "let" at $-9$ and "sac" at $-1$, and it plays the sacrifice. Quiescence at depth 2 does not help, because after PxP it is White's turn, there is no capture, and White stands pat at $-1$: the threat RxQ is a quiet threat. At depth 3 the plain search still plays "sac", because it then stops at the quiet move before RxQ. With depth 3 and quiescence, or with depth 4, the search sees RxQ in both lines and plays "let".

**Measured on random trees.** The tests build 300 random "material game" trees from the seed 2024 (Python's `random.Random`), with branching factor 3 and height 6. A move is a capture with probability 0.35 and wins 1, 3, 3, 5 or 9 points, and a quiet move changes the score by $-1$, 0 or $+1$. They count the trees in which the root move of a depth-limited search has a lower exact value than the best move.

| depth | wrong root moves without quiescence | with quiescence |
| --- | --- | --- |
| 1 | 113 | 58 |
| 2 | 71 | 41 |

Quiescence removed about half of the wrong moves at depth 1 and fewer at depth 2. Those that remain come from quiet moves after the frontier, which quiescence does not search.

**Real programs.** Berliner's thesis gives chess positions with both forms of the effect, from programs of the early 1970s. We do not repeat them here.

## Where it is used

- Every depth-limited search with a static evaluation, in [minimax](/minimax/), [negamax](/negamax/) and [alpha-beta](/alpha-beta-pruning/) programs, has a horizon. The effect is the reason for [quiescence search](/quiescence-search/) and for [search extensions](/search-extensions/).
- Forward pruning such as [null-move pruning](/null-move-pruning/) and [late move reductions](/late-move-reductions/) makes some lines shorter, so it brings the horizon nearer on those lines.
- [Monte Carlo tree search](/monte-carlo-tree-search/) with playouts to the end of the game has no fixed horizon, but it has a similar problem when a narrow forced line is sampled too rarely.
- The term is also used for planning and control with a finite lookahead, where a receding horizon controller cannot see costs past the end of its window.

## References
