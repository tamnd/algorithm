---
tag: N70HNE
kind: problem
slug: sokoban-problem
name: Sokoban problem
aliases:
- Sokoban
area: games-and-search/puzzles
level: advanced
summary: Push boxes onto goal squares in a grid, one box per push. NP-hard (Dor and Zwick 1999) and PSPACE-complete (Culberson 1999); small levels are solved by BFS over states.
prereqs: [state-space-search, pspace]
see_also: [breadth-first-search, iterative-deepening-a-star, pattern-database, duplicate-detection, assignment-problem, rush-hour-problem, sliding-tile-puzzle, motion-planning]
sources:
  - paper: "Joseph C. Culberson, Sokoban is PSPACE-complete, Proceedings of the International Conference on Fun with Algorithms (FUN 98), Proceedings in Informatics 4, Carleton Scientific, 1999, 65 to 76"
    locator: the whole paper (the reduction from linear bounded automata, and levels whose solutions need exponentially many moves)
  - paper: "Dorit Dor and Uri Zwick, SOKOBAN and other motion planning problems, Computational Geometry 13(4), 1999, 215 to 228"
    locator: the whole paper (NP-hardness of Sokoban and of related pushing problems)
  - book: isbn:9781568813226
    title: Robert A. Hearn and Erik D. Demaine, Games, Puzzles, and Computation, A K Peters, 2009
    locator: Part II, the chapter on one-player games (puzzles) (a proof of PSPACE-completeness for Sokoban by nondeterministic constraint logic)
  - paper: doi:10.1016/S0004-3702(01)00109-6
    title: Andreas Junghanns and Jonathan Schaeffer, Sokoban, enhancing general single-agent search methods using domain knowledge, Artificial Intelligence 129(1-2), 2001, 219 to 251
    locator: the whole paper (the Rolling Stone solver, IDA* with a matching lower bound, deadlock detection, macro moves and pattern search)
---

The Sokoban problem gives a grid of walls and floor, some boxes, as many goal squares, and a player. The player walks to a free neighbor square, or walks into a box and pushes it one square, if the square beyond is free. The player cannot pull a box or push two at once. Decide whether the player can put every box on a goal, and find a solution with the fewest moves or the fewest pushes. Dor and Zwick (1999) showed the problem is [NP-hard](/np-hard/), and Culberson (1999) showed it is [PSPACE](/pspace/)-complete. For small levels, [breadth-first search](/breadth-first-search/) over the states (player square, box squares) finds optimal solutions. Larger levels need [IDA*](/iterative-deepening-a-star/) with strong lower bounds and deadlock tests (Junghanns and Schaeffer 2001).

## In plain words

You are a worker in a warehouse seen from above. You can walk up, down, left and right, and you can push one box in front of you if the space behind it is empty. You cannot pull boxes. The job is to push every box onto a marked square.

The hard part is that some pushes cannot be undone. A box pushed into a corner can never move again, and a box against a wall can only slide along that wall. So one bad push early can make the level impossible many moves later.

A computer can try every position of the worker and the boxes, but the number of positions grows very fast with the number of boxes. In general, no fast method is known, and the levels can be made as hard as any problem a computer can solve with a fixed amount of memory.

## Definition

A *level* is a set $F$ of floor squares in the grid, a set $G \subseteq F$ of goals, a set $B_0 \subseteq F$ of boxes with $|B_0| = |G|$, and a start square $p_0 \in F \setminus B_0$. A *state* is a pair $(p, B)$ with $B \subseteq F$ and $p \in F \setminus B$. For a direction $d$:

- a *walk* goes from $(p, B)$ to $(p + d, B)$ when $p + d \in F \setminus B$;
- a *push* goes from $(p, B)$ to $(p + d, (B \setminus \{p + d\}) \cup \{p + 2d\})$ when $p + d \in B$ and $p + 2d \in F \setminus B$.

A *solution* is a sequence of moves from $(p_0, B_0)$ to a state with $B = G$.

- **Decision.** Does a solution exist?
- **Moves.** Find a solution with the fewest moves, walks and pushes together.
- **Pushes.** Find a solution with the fewest pushes; walks are free.

Solutions are written in the LURD notation: one letter per move, lowercase for a walk and uppercase for a push.

## Variants

- **Push-$k$.** The player may push up to $k$ boxes in a line, or any number in Push-$*$. Sokoban is Push-1 with goals; the motion planning versions only ask the player to reach a target square. Dor and Zwick (1999) and later papers classify many of these.
- **PushPush.** A pushed box slides until it hits something.
- **Pulling.** With pulls allowed as well, every move can be undone. The state graph is then undirected and no state is a dead end.
- **Move-optimal and push-optimal.** The two goals can disagree, as in the example below. Solvers often find the fewest pushes first and then the fewest moves among those.
- **Related puzzles.** [Rush Hour](/rush-hour-problem/) and the [sliding tile puzzle](/sliding-tile-puzzle/) are also block-moving puzzles with a state graph to search. Their moves can be undone, but a Sokoban push often cannot.

## Examples

**A level where fewest moves and fewest pushes disagree.**

```text
########
##  #  #
#  $@# #
#   . ##
#      #
########
```

The fewest moves is 8, with `LulDldRR`: it pushes the box left, walks around it, pushes it down, then pushes it right twice, 4 pushes in all. The fewest pushes is 2, with `dlluurDldR`: the player walks around to stand above the box, pushes it down once, then steps around and pushes it right once, 10 moves in all. No solution has both 8 moves and 2 pushes.

**A dead level.**

```text
#####
#$ .#
# @ #
#####
```

The box is in a corner, so no push can move it, and the level has no solution. Search proves this by running out of states.

**The size of the search.** A level with $f$ floor squares and $b$ boxes has at most $f \binom{f}{b}$ states. With 40 floor squares and 6 boxes this is about $1.5 \times 10^8$, and real levels have more boxes. So plain breadth-first search works only for small levels.

## Known algorithms

- **Breadth-first search for moves.** Search the graph of states $(p, B)$ with all moves as edges, with a hash set of visited states ([duplicate detection](/duplicate-detection/)). The first solved state found gives the fewest moves.
- **Breadth-first search for pushes.** Make a node the box set $B$ with the area the player can reach without a push, written as its least square; each edge is one push. This graph is much smaller, and the first solved node gives the fewest pushes. A 0-1 search on the full graph, with walks of cost 0 and pushes of cost 1, finds the same number.
- **IDA* with a matching bound.** Junghanns and Schaeffer (2001) use [IDA*](/iterative-deepening-a-star/) on pushes. The lower bound is a minimum-cost matching of boxes to goals by push distances, an [assignment problem](/assignment-problem/). They add tables of deadlock patterns, macro moves through tunnels and goal rooms, and pruning of moves that do not matter. Their solver Rolling Stone solved a large part of the standard 90-level test set.
- **Deadlock tests.** A *dead square* is a floor square from which a box can never reach a goal, such as a corner that is not a goal. Pushing a box there ends the search on that branch. Patterns of several boxes that can never move, found by search on small regions, extend this, in the manner of a [pattern database](/pattern-database/).
- **Bidirectional and backward search.** Search backward from the goal state with pulls. This finds the squares from which a box can still reach a goal, and it can meet a forward search in the middle.

## Bounds

- **NP-hard.** Dor and Zwick (1999).
- **PSPACE-complete.** Culberson (1999) reduces the acceptance problem of a linear bounded automaton to Sokoban. Hearn and Demaine (2009) give a proof by nondeterministic constraint logic. Membership in PSPACE holds since a state has polynomial size: a nondeterministic search guesses the moves one at a time, and [Savitch's theorem](/savitch-theorem/) removes the guessing.
- **Long solutions.** Since Sokoban is PSPACE-complete, it is not in NP unless NP = PSPACE. In line with this, Culberson's construction gives levels whose shortest solutions need exponentially many moves in the size of the level, too long to serve as a certificate.
- **Search.** Breadth-first search takes time and space linear in the number of reachable states, at most $f \binom{f}{b}$ times the 4 directions.

## Reductions

- **From linear bounded automata.** Culberson builds gadgets of boxes and walls that act as the tape cells and the control of a linear bounded automaton. The level is solvable exactly when the automaton accepts.
- **From nondeterministic constraint logic.** Hearn and Demaine (2009) reduce NCL to Sokoban with local gadgets. The same framework covers [Rush Hour](/rush-hour-problem/) and sliding-block puzzles.
- **To graph search.** Each level is a reachability question in a directed graph of states, so every [state-space search](/state-space-search/) method applies. The graph is exponential in the number of boxes.

## Applications

- **A benchmark for planning and search.** Sokoban is a standard test domain for heuristic search and for automated planning, because its dead ends defeat many methods.
- **Robot motion planning.** Pushing objects in a cluttered space, where moves cannot always be undone, is a [motion planning](/motion-planning/) problem of the same kind.
- **Teaching complexity.** It is a small, familiar puzzle whose general form is PSPACE-complete.

## References
