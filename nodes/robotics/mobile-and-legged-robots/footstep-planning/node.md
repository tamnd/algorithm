---
tag: 3034EM
kind: problem
slug: footstep-planning
name: Footstep planning
aliases:
- foothold planning
area: robotics/mobile-and-legged-robots
level: advanced
summary: "Choose a sequence of foot placements on safe terrain from a start stance to a goal, such that each step is within the reach of the legs and the robot can balance on it."
prereqs: [motion-planning, a-star-search]
see_also: [zmp-preview-control, capture-point, support-polygon, a-star-search, mixed-integer-programming, state-lattice-planning, motion-planning, breadth-first-search]
sources:
  - paper: doi:10.1109/IROS.2001.973406
    title: James Kuffner, Koichi Nishiwaki, Satoshi Kagami, Masayuki Inaba and Hirochika Inoue, Footstep planning among obstacles for biped robots, IEEE/RSJ International Conference on Intelligent Robots and Systems, 2001
    locator: volume 1, pages 500 to 505
  - paper: doi:10.1109/ROBOT.2005.1570188
    title: Joel Chestnutt, Manfred Lau, German Cheung, James Kuffner, Jessica Hodgins and Takeo Kanade, Footstep planning for the Honda ASIMO humanoid, IEEE International Conference on Robotics and Automation, 2005
    locator: pages 629 to 634
  - paper: doi:10.1109/HUMANOIDS.2014.7041373
    title: Robin Deits and Russ Tedrake, Footstep planning on uneven terrain with mixed-integer convex optimization, IEEE-RAS International Conference on Humanoid Robots, 2014
    locator: pages 279 to 286
---

Footstep planning is the problem of choosing where a legged robot puts its feet, step by step, to go from a start to a goal. Each foothold must be on safe terrain, each step must be within the reach of the legs, and the robot must be able to keep its balance while it moves from one stance to the next. A footstep plan is the input of the lower layers of a walking controller: a pattern generator such as [ZMP preview control](/zmp-preview-control/) turns it into a motion of the center of mass. The two main families of methods are graph search over a fixed set of steps and mixed-integer convex optimization over safe regions of the terrain.

## In plain words

A person who crosses a stream on stepping stones thinks about where each foot goes. Each stone must be big enough and flat enough, and the next stone must be close enough to reach. A stone that looks good can lead to a place where no stone is in reach.

A walking robot has the same task. It knows the terrain from a map or from its cameras, and it knows how far and in which directions each leg can step. It searches for a list of steps that starts where it stands and ends at the goal. Among the lists that work, it prefers short ones and ones that keep away from edges.

The plan only says where the feet go. Another part of the controller decides how the body moves so that the robot does not fall during the steps.

## Definition

**Input.**

- The terrain: a set $F$ of allowed foot poses, given as a height map with a list of safe areas, or as a set of convex regions $R_1, \dots, R_r$ of the terrain surface. A pose is allowed if the whole sole is supported and the surface is not too steep.
- The start stance: the poses of the feet at the start, for a biped the left and the right foot.
- The goal: a region for the final stance.
- The reach of the legs: for each foot, a set $\mathcal{R}$ of poses of the next foothold relative to the pose of the other foot (or of the body), from the leg kinematics and the joint limits. For a biped the feet alternate, so the set depends on which foot moves.
- A cost: the number of steps, the path length, a terrain cost, or a sum of these.

**Output.** A sequence of footholds $s_1, \dots, s_n$, each with its foot label, such that every $s_j \in F$, every $s_{j+1}$ is in the reach set of the stance that it follows, the last stance is in the goal, and the cost is minimum, or a report that no such sequence exists.

**Balance.** Each transition must allow a balanced motion: for slow walking, the center of mass must be able to move from one [support polygon](/support-polygon/) to the next; for dynamic walking, a pattern generator must find a center of mass path with the ZMP in the feet. Most planners do not model this directly. They use a reach set small enough that the pattern generator succeeds for every step in it, which is a design rule, not a guarantee.

## Variants

- **Discrete steps on a lattice.** The robot can take one of a fixed set of steps from each stance, and the poses lie on a grid in $(x, y, \text{yaw})$. The problem is then a shortest path problem on a graph.
- **Continuous footholds in convex regions.** The footholds are continuous variables, each assigned to one of $r$ convex safe regions. The assignment is discrete and the poses are continuous, which gives a mixed-integer problem.
- **Fixed step count or free step count.** Some formulations fix $n$ and minimize the cost; others also choose $n$.
- **Body path first.** A planner first plans a path of the body in the plane, then places footsteps along it. This is fast but can miss plans that need sidesteps or turns that the body path does not show.
- **Online replanning.** The robot plans a few steps ahead and plans again after each step, as the map changes or after a push. Controllers based on the [capture point](/capture-point/) move the next footstep in real time.
- **Quadrupeds and contact sequences.** A quadruped chooses footholds for four legs in a gait pattern; a humanoid that also uses its hands chooses a sequence of contacts. Both have the same structure with more contact labels.

## Examples

**Stepping stones and a dead end.** A robot hops on one foot from stone to stone, with a reach of $0.45$ m between footholds. The stones are $S = (0, 0)$, $A = (0.4, 0.1)$, $B = (0.35, -0.15)$, $C = (0.8, 0.3)$, $D = (0.75, -0.2)$, $E = (1.15, -0.1)$ and the goal $G = (1.5, 0)$, in meters. Two stones are joined if their distance is at most $0.45$ m:

| stone | stones in reach (distance in m) |
|---|---|
| $S$ | $A$ (0.412), $B$ (0.381) |
| $A$ | $S$, $B$ (0.255), $C$ (0.447) |
| $B$ | $S$, $A$, $D$ (0.403) |
| $C$ | $A$ |
| $D$ | $B$, $E$ (0.412) |
| $E$ | $D$, $G$ (0.364) |

A greedy rule that always takes the stone farthest forward goes $S \to A \to C$ and then has no stone in reach: $C$ is a dead end. [Breadth-first search](/breadth-first-search/) from $S$ finds $S \to B \to D \to E \to G$, four steps, which is the minimum. A biped adds the left and right labels and a reach set that depends on the side, but the search is the same.

**A turn in place.** On flat ground with no obstacles, a biped that must turn by 90 degrees, with a limit of 30 degrees of yaw between the two feet, needs at least three steps that each add 30 degrees, and then one more step to bring the feet parallel. The order of the inner and the outer foot matters, because a foot must not cross the other. The reach set encodes these limits.

## Known algorithms

- **Search over a fixed set of steps.** Kuffner et al. (2001) plan footsteps among obstacles by a search over a finite set of footstep transitions, with the stability of each transition checked in advance. Chestnutt et al. (2005) use [A* search](/a-star-search/) with a heuristic from the distance to the goal for the Honda ASIMO humanoid. With an [admissible heuristic](/admissible-heuristic/), A* returns a plan of minimum cost among the plans made of the given steps. The result is optimal only for the chosen step set, and a coarse set can miss narrow passages.
- **Mixed-integer convex optimization.** Deits and Tedrake (2014) first compute convex safe regions of the terrain, then solve a [mixed-integer](/mixed-integer-programming/) convex program in which binary variables assign each footstep to a region and continuous variables give its pose. The reach of the legs is a convex constraint, and the yaw dependence is handled by a piecewise linear approximation of sine and cosine chosen by more binary variables. A branch and bound solver returns a global optimum of this model, or a proof that the model has no solution.
- **Lattice planners.** A [state lattice](/state-lattice-planning/) of stances with the step set as motion primitives gives a graph on which A* and its anytime variants work, as for wheeled robots.
- **Sampling and local optimization.** Trajectory optimization over contact locations and timing, with the footholds as continuous variables, finds locally optimal plans that also include the body motion.

## Bounds

With a step set of $a$ steps and plans of $n$ steps, the search tree has up to $a^n$ nodes. On a lattice with $g$ stance states, A* with a consistent heuristic expands each state at most once and runs in $O(g \log g)$ time with a binary heap. The mixed-integer program has a number of binary variables that grows linearly with $n$ and $r$, and its solver can take time exponential in that number in the worst case. These are bounds on the methods. No complexity classification of the footstep planning problem itself is given here.

## Reductions

- **To a shortest path problem.** With a discrete step set, each stance is a node and each step is an edge, and the minimum cost plan is a shortest path; A*, Dijkstra's algorithm and breadth-first search (for unit costs) apply.
- **To mixed-integer convex programming.** With convex safe regions and convex reach sets, the problem with a fixed number of steps is a mixed-integer convex program, as in Deits and Tedrake (2014).
- **From motion planning.** Footstep planning is [motion planning](/motion-planning/) in the space of stances, with discrete changes of contact. It is a special case of planning with contact modes.

## Applications

- **Humanoid robots on cluttered or uneven ground.** The footstep plan sets the ZMP reference of a pattern generator such as [ZMP preview control](/zmp-preview-control/).
- **Quadrupeds on rough terrain.** Foothold selection picks safe footholds for each leg in a gait; a controller such as [convex MPC](/convex-mpc-legged-locomotion/) then plans the forces for the chosen contacts.
- **Push recovery.** After a push, a controller based on the [capture point](/capture-point/) changes the next footstep, which is a footstep plan of one or two steps solved in real time.

## References
