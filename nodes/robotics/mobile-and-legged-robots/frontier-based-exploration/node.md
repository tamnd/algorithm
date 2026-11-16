---
tag: KCQHFD
kind: algorithm
slug: frontier-based-exploration
name: Frontier-based exploration
aliases:
- frontier exploration
area: robotics/mobile-and-legged-robots
level: core
summary: "Yamauchi's method that moves the robot to the nearest boundary between known free space and unknown space, until no frontier is left."
model: word-ram
complexity:
  vars: {c: "the number of grid cells", r: "the sensor range in cells"}
  time: {worst: O(c^2 r^2)}
  space: {extra: O(c)}
properties: {deterministic: true, randomized: false, online: true, exact: false}
history:
  year: 1997
  people: [Brian Yamauchi]
  note: Yamauchi defined frontiers on an evidence grid and drove a real robot to the nearest accessible frontier until none was left.
prereqs: [occupancy-grid-map, breadth-first-search]
see_also: [next-best-view-planning, coverage-path-planning, occupancy-grid-mapping, slam-problem, connected-components, bresenham-line-algorithm, watchman-route-problem, multi-robot-task-allocation]
sources:
  - paper: doi:10.1109/CIRA.1997.613851
    title: A frontier-based approach for autonomous exploration
    locator: "pp. 146-151, the whole paper (frontier cells, frontier regions with a minimum size, and travel to the nearest accessible frontier)"
---

Frontier-based exploration lets a mobile robot build a map of an unknown place on its own. The robot keeps an [occupancy grid](/occupancy-grid-map/) in which each cell is unknown, free or occupied. A frontier is the boundary between the known free space and the unknown space: a free cell next to an unknown cell. Brian Yamauchi's rule is simple. Find the frontiers, group the adjacent frontier cells into regions, drive to the nearest region that the robot can reach through known free space, and look around there. Each visit pushes the boundary of the known map outward. When no reachable frontier is left, the part of the world that the robot can reach is mapped. The method needs no model of the environment and works with any sensor that can mark cells as free or occupied, which is why it is still the default baseline for exploration.

## In plain words

Imagine walking into a dark building with a flashlight. You see a little of each room. Wherever the lit floor ends and darkness begins, there is something left to see. So you walk to the nearest such edge, shine the light, and look again. Each time, the dark part shrinks. You stop when every edge between lit floor and darkness is behind a wall or out of reach. Then you have seen every place you could walk to.

The method does not plan the best tour. It only goes to the closest edge each time, so it can walk back and forth more than needed. But it is simple and it always finishes.

## The problem

**Input.** A grid world of $c$ cells, each free or occupied, that the robot does not know; a start cell, which is free; and a sensor of range $r$ cells. At each cell, the sensor casts [digital lines](/bresenham-line-algorithm/) from the robot to every cell on the square of radius $r$ around it, and reveals the cells along each line up to and including the first occupied one. The robot moves between free cells that share a side, and only through cells its map marks free. Cells are integers and each map access costs one step, as in the [word RAM](/word-ram/).

**Output.** A map in which every free cell that the robot can reach from the start is marked free, and the walk that produced it.

**How it differs from close pages.** [Coverage path planning](/coverage-path-planning/) assumes a known map and asks for a path that passes over every point; exploration asks only to see every point, in a map that is built along the way. [Next-best-view planning](/next-best-view-planning/) scores candidate views by the unknown volume they would reveal and picks the best; frontier exploration picks the nearest frontier, which is cheaper and needs no sensor model beyond free, occupied and unknown. Building the map itself, with noisy poses, is the [SLAM problem](/slam-problem/).

## The algorithm

```pseudo id=main
EXPLORE(start)
L1  mark every cell unknown, then the start free;  p ← start;  SENSE(p)
L2  loop:  F ← the free cells with an unknown neighbor
L3      group F into 8-connected regions and keep the regions with at least min_size cells
L4      P ← a shortest path, through free cells, from p to the nearest cell of a kept region
L5      if there is no such path then return the map
L6      for each cell q of P after p:
L7          p ← q;  SENSE(p)
```

Line L2 finds the frontier cells; the code tests the four neighbors that share a side. Line L3 finds the [connected components](/connected-components/) of the frontier cells, with diagonal cells counted as adjacent, and drops small regions, which Yamauchi did to ignore frontiers smaller than the robot. Line L4 is a [breadth-first search](/breadth-first-search/) from the robot over the free cells, which stops at the first frontier cell of a kept region. The robot senses at every cell on the way (line L7), so the map often changes before it arrives; the code still finishes the path, then plans again.

## Example

A building of $10 \times 5$ cells has two rooms joined by a doorway in the bottom row (`#` is a wall):

```
##########
#....#...#
#....#...#
#........#
##########
```

The robot starts in the top left corner of the left room, at column 1 and row 1, with a sensor range of 2 cells. It sees part of the left room, and the frontier is one region along the right and bottom of what it saw. Then:

| Plan | Path | What it sees on arrival |
|---|---|---|
| 1 | (1,1) to (3,1) | the rest of the left room and the wall at column 5 |
| 2 | (3,1) to (3,3) | the bottom wall of the left room |
| 3 | (3,3) to (5,3) | through the doorway into the right room, up to column 7 |
| 4 | (5,3) to (7,3) | the bottom and right of the right room |
| 5 | (7,3) to (7,1) | the top wall of the right room |

After 5 plans and 10 moves, no free cell has an unknown neighbor. The corner cell outside the walls at (0,4) stays unknown, since no ray reaches it and it has no free neighbor.

## Correctness

The [proof](proofs/correctness/) shows two facts, for a sensor that marks cells correctly and has range at least 1, and for min_size = 1. First, the method stops: each plan ends at a cell that had an unknown neighbor, and the sensing at that cell reveals the neighbor, so the number of unknown cells drops with every plan, and there are at most $c$ plans. Second, when it stops, every free cell that the robot can reach from the start is marked free: otherwise, on a path through free cells to an unknown one, the last known cell before the first unknown cell is a frontier that line L4 reaches. With min_size > 1, the method still stops, but it can stop early and leave small regions unexplored. The tests check the frontier cells, the regions and the shortest paths against their definitions, and check both facts on 25 random worlds with random sensor ranges.

## Complexity

- **Time.** Each plan costs $O(c)$ for lines L2 to L4, and there are at most $c$ plans. Each path has at most $c$ cells, and each sensing casts $8r$ lines of at most $r + 1$ cells. This gives $O(c^2 r^2)$ in the worst case. In practice, paths are short. Measured on $40 \times 40$ worlds with 20% random obstacles: with $r = 4$, about 80 plans, 410 moves and 0.2 s in this Python code; with $r = 8$, about 47 plans and 320 moves.
- **Space.** $O(c)$ for the map, the frontier set and the search.

## Properties

- **Complete for reachable space.** With a correct sensor and no minimum size, every free cell reachable from the start ends up known.
- **Not optimal.** Going to the nearest frontier is a greedy choice. The length of the walk has no constant-factor bound against the shortest walk that sees everything; this would be a [watchman route problem](/watchman-route-problem/) on a map that the robot does not have.
- **Model-free.** It needs only the three states of each cell, not a probabilistic sensor model.
- **Online and replanning.** Each plan uses the current map only, so new obstacles and new openings are handled at the next plan.

## Variants and improvements

- **Scored frontiers.** Weigh the distance to a frontier against the expected information gain at it, as in [next-best-view planning](/next-best-view-planning/).
- **Multiple robots.** Each robot goes to a different frontier, assigned by distance, by an auction, or by a [task allocation](/multi-robot-task-allocation/) method, and the robots share one map.
- **Fast frontier detection.** Instead of scanning the whole grid, update the frontier set only in the cells that the last scan changed.
- **3D exploration.** The same idea runs on an [octree map](/octree-occupancy-map/) of voxels for aerial robots, often with a frontier region scored by its size.
- **Exploration with SLAM.** When the pose is uncertain, the planner can also pick goals that revisit known places to close loops.

## When to use it

Use frontier-based exploration when a robot must map an unknown indoor space by itself and the map is a grid. It is a strong baseline, easy to add on top of any grid mapping system. When travel is expensive, as for an aerial robot with a short battery life, or the sensor sees far, a method that scores views by information gain usually maps the same space with a shorter path.

## Pitfalls

- **Noisy maps.** A sensor that leaves holes in known free space creates many tiny frontiers. A minimum region size, or a filter on the map, removes them, but too large a size stops the exploration early: in our measurements on $20 \times 20$ worlds with $r = 2$, a minimum size of 3 sometimes stopped before the first move.
- **Unreachable frontiers.** A frontier seen through a gap that the robot cannot pass keeps the robot trying. Plan only to frontiers that the path search can reach, as line L4 does, and blacklist goals that fail.
- **Oscillation.** If two frontiers are almost equally near, the nearest one can change at every plan. Commit to a goal until it is reached or is no longer a frontier.
- **Pose drift.** The method assumes the map is correct. With drift, frontiers appear in the wrong place; use a SLAM system underneath.

## Implementations

## History

Yamauchi presented frontier-based exploration in 1997, at the IEEE International Symposium on Computational Intelligence in Robotics and Automation. His robot built an evidence grid from its range sensors, detected frontier cells, grouped them into regions, ignored regions smaller than the robot, and drove to the nearest accessible one. Yamauchi and others soon extended the idea to teams of robots that share one map. Frontiers became the basis of most later grid and voxel exploration systems.

## References
