---
tag: W79DQ3
kind: problem
slug: polygon-pursuit-evasion
name: Visibility-based pursuit-evasion
aliases:
- pursuit-evasion in a polygon
area: robotics/multi-robot-systems
level: research
summary: Find a motion of searchers with line of sight that is sure to see an evader of unbounded speed in a polygonal region.
prereqs: [simple-polygon, visibility-polygon, polygon-with-holes]
see_also: [art-gallery-problem, watchman-route-problem, art-gallery-theorem, minimum-guard-np-hardness, np-hard, coverage-path-planning, frontier-based-exploration, multi-robot-system]
sources:
  - paper: doi:10.1142/S0218195999000273
    title: Leonidas J. Guibas, Jean-Claude Latombe, Steven M. LaValle, David Lin and Rajeev Motwani, A visibility-based pursuit-evasion problem, International Journal of Computational Geometry and Applications 9(4-5), 1999
    locator: pages 471 to 493 (the problem, the bounds on the number of pursuers, and the complete algorithm for one pursuer by critical events)
  - paper: doi:10.1137/0221051
    title: Ichiro Suzuki and Masafumi Yamashita, Searching for a mobile intruder in a polygonal region, SIAM Journal on Computing 21(5), 1992
    locator: pages 863 to 888 (searchers with a fixed number of flashlights and the first conditions for a polygon to be searchable)
  - book: isbn:9780521862059
    title: Steven M. LaValle, Planning Algorithms, Cambridge University Press, 2006
    locator: Section 12.4.1 (visibility-based pursuit-evasion, information states, and the NP-hardness of finding the fewest pursuers)
---

Visibility-based pursuit-evasion asks for a motion of one or more pursuers in a polygon that is sure to see an evader, when the evader can move arbitrarily fast, knows everything and is seen only when it is in a pursuer's line of sight. It is the moving version of the [art gallery problem](/art-gallery-problem/): there, fixed guards must see every point at once, here pursuers sweep the region over time so that no hidden part can still hold the evader. It also differs from the [watchman route problem](/watchman-route-problem/), where one guard must see every point once along a route but the target does not move, so a route that sees everything may still let a moving evader slip behind the guard.

## In plain words

Some people search a dark building with lamps for an intruder who can run as fast as they like and always knows where the searchers are. The intruder is caught as soon as a searcher can see it. The searchers must plan a walk that leaves the intruder no place to hide, even when the intruder slips from room to room behind their backs.

A room that a searcher has looked at can become unsafe again if the intruder can sneak back in from a part nobody sees. So the plan must clear the building in an order where cleared parts stay cleared. The questions are how many searchers a building needs and how they should move.

## Definition

The free space $P$ is a polygon with $n$ vertices, simply connected or with $h$ holes. There are $q$ pursuers, each a point that moves along a continuous path in $P$, and an evader, a point that moves along any continuous path in $P$ at any speed. A pursuer sees a point when the segment between them lies in $P$, so its view is its [visibility polygon](/visibility-polygon/). The evader is *found* at time $t$ if some pursuer sees it at time $t$.

A *search schedule* is a set of $q$ pursuer paths over a time interval $[0, T]$. It is a *solution* if every evader path in $P$ is found at some time in $[0, T]$. The *search number* of $P$ is the smallest $q$ that admits a solution.

The pursuers know the polygon, they plan together before they start, and they move in continuous time; they need no messages during the search if the plan is fixed. The evader knows the plan.

**Questions.** Given $P$ and $q$, is there a solution? Construct one. Find the search number.

The *contaminated* region at time $t$ is the set of points where the evader could be, given that it has not been found yet. A schedule is a solution exactly when the contaminated region becomes empty.

## Variants

- **Limited field of view.** Suzuki and Yamashita (1992) studied the $k$-searcher, which holds $k$ flashlights, each a ray it can turn; the $\infty$-searcher sees all around.
- **Curved regions and unknown maps.** The region has curved boundaries, or the pursuers must also map it, which links the problem to [frontier-based exploration](/frontier-based-exploration/).
- **Graph searching.** On a graph, searchers move along edges and the evader hides in edges; this is the edge-searching game of Parsons, a combinatorial relative.
- **Bounded speed.** If the evader's speed is bounded, fewer pursuers may suffice.
- **Capture.** Pursuers must reach the evader, not only see it, as in lion and man games.

## Examples

**A convex room.** One pursuer standing anywhere sees the whole room, so the search number is 1 and the schedule takes no time.

**An L-shaped room.** A pursuer at the reflex vertex sees both arms at once, so one pursuer suffices without moving.

**A long corridor with side rooms.** One pursuer walks along the corridor and looks into each side room as it passes. If the corridor is straight, the pursuer keeps seeing all of the corridor behind it, so a side room it has looked into cannot be entered again unseen, and it stays clear.

**A ring.** Take a square with a square hole, so the free space is four arms around the hole. One pursuer cannot win (theorem, by this argument): the part hidden behind the hole is never empty, it moves continuously as the pursuer moves, and the evader, being fast enough, stays in it. Two pursuers at opposite outer corners each see the two arms that meet at their corner, so together they see the whole ring at once.

## Known algorithms

- **One pursuer, complete algorithm.** Guibas, Latombe, LaValle, Lin and Motwani (1999) split the polygon into cells by *critical events*, the lines where a gap in the pursuer's view appears, disappears, splits or merges. In each cell, the information state is the pursuer's cell and a label of each gap, contaminated or clear. A search of the finite graph of these states decides whether one pursuer can win, and gives a schedule if it can (theorem).
- **Several pursuers.** The same idea works for $q$ pursuers in the joint space, with a cost that grows exponentially in $q$.
- **Bounding strategies.** The upper bounds below come from explicit strategies that split the polygon recursively, so that a few pursuers guard the cuts while the others search one side.
- **Heuristics.** For large maps, sampling-based and greedy strategies are used, without guarantees.

## Bounds

All results in this section are theorems from Guibas et al. (1999), unless another source is named.

- **Simply connected.** $\Theta(\log n)$ pursuers always suffice for a polygon with $n$ vertices, and some polygons need that many.
- **With holes.** $\Theta(\sqrt{h} + \log n)$ pursuers always suffice for a polygon with $h$ holes and $n$ vertices, and some polygons need that many.
- **Fewest pursuers.** Computing the search number is [NP-hard](/np-hard/) (LaValle 2006, Section 12.4.1).
- **Static guards for comparison.** The [art gallery theorem](/art-gallery-theorem/) says $\lfloor n/3 \rfloor$ fixed guards always suffice to see a simple polygon at once, and finding the fewest is NP-hard ([minimum guard NP-hardness](/minimum-guard-np-hardness/)). Moving pursuers can do with $O(\log n)$.

## Reductions

- With $q$ pursuers that do not move, the problem is the art gallery problem: a solution exists exactly when $q$ guards see the whole polygon.
- A solution for one pursuer gives a [watchman route](/watchman-route-problem/)-like path that sees every point, but not the other way round: a watchman route need not keep cleared parts clear.
- On the graph of critical-event cells, the one-pursuer problem becomes a search in a finite state graph, as in [breadth-first search](/breadth-first-search/).

## Applications

Search and rescue in buildings, security patrols with robots, finding a lost person in a cave system, and clearing a region before people enter it are uses of pursuit-evasion. The bounds tell planners how many robots a site needs, and the critical-event method gives sure schedules for one robot in a known map.

## References
