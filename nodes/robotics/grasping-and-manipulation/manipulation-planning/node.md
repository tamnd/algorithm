---
tag: KETH12
kind: problem
slug: manipulation-planning
name: Manipulation planning
aliases:
- pick-and-place planning
area: robotics/grasping-and-manipulation
level: advanced
summary: Plan robot motions that grasp, carry and place objects, in a space of robot and object configurations split into modes.
prereqs: [configuration-space, motion-planning, grasp-synthesis]
see_also: [task-and-motion-planning, probabilistic-roadmap, rapidly-exploring-random-tree, piano-movers-problem, in-hand-manipulation, quasi-static-pushing, caging-grasp, hybrid-automata]
sources:
  - paper: "Rachid Alami, Thierry Siméon and Jean-Paul Laumond, A geometrical approach to planning manipulation tasks: the case of discrete placements and grasps, in Robotics Research: The Fifth International Symposium (ISRR), MIT Press, 453-463, 1990"
    locator: the whole paper (the composite configuration space, transit and transfer paths, and the manipulation graph for finite sets of grasps and placements)
  - paper: doi:10.1177/0278364904045471
    title: Thierry Siméon, Jean-Paul Laumond, Juan Cortés and Anis Sahbani, Manipulation planning with probabilistic roadmaps, The International Journal of Robotics Research 23(7-8), 729-746, 2004
    locator: the whole paper (continuous sets of grasps and placements, and a roadmap planner that connects the components of their intersection)
  - paper: doi:10.1007/BF01530890
    title: Gordon Wilfong, Motion planning in the presence of movable obstacles, Annals of Mathematics and Artificial Intelligence 3, 131-150, 1991
    locator: the abstract and main results (PSPACE-hard when the final positions of the movable obstacles are given, NP-hard when they are not, and O(n^3) time for one convex movable obstacle in a polygonal workspace)
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Chapters 10 and 12 (motion planning, and grasping and manipulation)
---

Manipulation planning asks for robot motions that move objects: reach an object, grasp it, carry it, put it down, and perhaps grasp it again in another way, until every object is where it should be. It extends [motion planning](/motion-planning/), where only the robot moves, to a space that holds the configurations of the robot and of the objects. The objects cannot move by themselves, so the space splits into modes: in one mode the robot moves alone, in another it carries an object with a fixed grasp. A plan is a path that stays in the modes and switches between them only where a grasp or a release is possible.

## In plain words

A robot must move a box from a table to a high shelf. It can only hold the box from the side, but from the side the box does not fit on the shelf, which needs a grasp from the top. So the robot puts the box down on a free table, lets go, grasps it again from the top, and then places it. A manipulation planner finds such plans: when to grasp, how to hold, where to put things down for a moment, and the collision-free motions in between.

## Definition

The *composite configuration space* is $C = C_R \times C_{O_1} \times \cdots \times C_{O_m}$, with $C_R$ the configuration space of the robot and $C_{O_i}$ that of object $i$. A configuration is free if no two bodies overlap and no object hangs in the air: each object either rests in a stable *placement* on a surface or is held in a *grasp*, a fixed pose relative to the hand.

Two kinds of motion are allowed (Alami, Siméon and Laumond 1990):

- a *transit path*, in which the robot moves and every object stays at its placement;
- a *transfer path*, in which the robot moves while it holds one object with a fixed grasp, and the other objects stay still.

A transit path and a transfer path can meet only at a configuration in which the held object is both in a stable placement and in a grasp: the robot grasps or releases it there.

**The problem.** Given an initial configuration and a goal (a configuration, or a set of goal placements for the objects), find a finite sequence of transit and transfer paths, joined at grasp and release configurations, from the start to the goal.

## Variants

- **Discrete grasps and placements.** Each object has a finite set of grasps and placements. Alami, Siméon and Laumond (1990) build the *manipulation graph*: its nodes are connected components of the free space in each mode, and its edges are grasp and release configurations that join them.
- **Continuous grasps and placements.** Grasps and placements form manifolds, and the planner must find where the transit and transfer spaces meet. Siméon, Laumond, Cortés and Sahbani (2004) use [probabilistic roadmaps](/probabilistic-roadmap/) to sample and connect them.
- **Navigation among movable obstacles.** The robot must reach its own goal and may push obstacles out of the way, with or without fixed final positions for them (Wilfong 1991).
- **Rearrangement.** Many objects must be moved to given goal placements, as when a robot sets a table or packs a box.
- **Non-prehensile manipulation.** The robot pushes, tilts or slides objects instead of grasping them. The modes then follow the contact mechanics, such as [quasi-static pushing](/quasi-static-pushing/).
- **Multi-step tasks with symbols.** When the order of actions is itself hard to find, the problem is [task and motion planning](/task-and-motion-planning/).

## Examples

**The regrasp on the shelf.** One object, two placements (table $A$, shelf $B$), one more free placement $T$, and two grasps (side, top). The side grasp collides with the shelf at $B$, and the top grasp collides with a wall above $A$. The manipulation graph has the modes (placed at $A$), (held by the side grasp), (placed at $T$), (held by the top grasp) and (placed at $B$). The only path from $A$ to $B$ is: transit to $A$, grasp by the side, transfer to $T$, release, transit, grasp from the top, transfer to $B$, release. A planner that only moves the robot with a fixed grasp finds no plan.

**Pushing a door open.** A robot must pass through a door that is closed. The door is a movable obstacle with one degree of freedom. The plan has a transit to the handle, a transfer that swings the door, and a transit through the gap.

## Known algorithms

- **The manipulation graph.** For finite grasps and placements, compute the free components of each mode and their connections, then search the graph (Alami, Siméon and Laumond 1990). It is complete if the components are computed exactly, which is costly in high dimension.
- **Roadmaps of the transit and transfer spaces.** Sample configurations in each mode and at their intersections, connect them by local paths, and search the roadmap (Siméon and others 2004). This is probabilistically complete under the usual conditions of sampling planners.
- **Tree search with mode switches.** Grow trees like [rapidly-exploring random trees](/rapidly-exploring-random-tree/) in the composite space, and add a grasp or a release when the tree reaches a configuration where one is possible.
- **Exact algorithms for small cases.** For one convex movable obstacle of constant complexity in a polygonal workspace with $n$ corners, Wilfong (1991) gives an algorithm with $O(n^3)$ time.
- **Symbolic layers.** Plan the order of grasps and placements with a task planner and fill in the motions with a motion planner, as in [task and motion planning](/task-and-motion-planning/).

## Bounds

- **Hardness with movable obstacles.** Wilfong (1991) proves that motion planning with movable obstacles is PSPACE-hard when the final positions of the obstacles are given, and NP-hard when they are not (theorems).
- **Hardness from motion planning.** A manipulation problem with no objects is a motion planning problem, so the hardness of the [generalized piano movers' problem](/piano-movers-problem/) carries over when the robot has many degrees of freedom.
- **One movable obstacle.** $O(n^3)$ time for the convex case above (Wilfong 1991).

## Reductions

- **From motion planning.** With no objects, or with all objects fixed, the problem is motion planning in $C_R$.
- **To planning in a hybrid system.** The modes are discrete states, the motions in each mode are continuous, and grasps and releases are guarded switches; the problem is reachability in a [hybrid automaton](/hybrid-automata/) with a geometric structure.
- **To task and motion planning.** Adding symbolic goals and actions, such as "stack the blocks", gives [task and motion planning](/task-and-motion-planning/), which contains manipulation planning.

## Applications

Pick and place in factories and warehouses, assembly that needs regrasping, rearrangement of objects by service robots, and the motion layer of every robot that moves objects. It is also the motion part of [in-hand manipulation](/in-hand-manipulation/) when the robot regrasps an object on a table.

## References
