---
tag: HEP6QK
kind: problem
slug: next-best-view-planning
name: Next-best-view planning
aliases:
- NBV planning
- view planning
area: robotics/mobile-and-legged-robots
level: advanced
summary: "Choose the next sensor pose that most increases the known part of a scene or object, weighing gain against travel cost."
prereqs: [occupancy-grid-map, information-gain]
see_also: [frontier-based-exploration, art-gallery-problem, octree-occupancy-map, max-coverage, greedy-set-cover, rapidly-exploring-random-tree, ray-casting, coverage-path-planning]
sources:
  - paper: doi:10.1109/ROBOT.1985.1087372
    title: "C. I. Connolly, The determination of next best views"
    locator: "Proceedings of the 1985 IEEE International Conference on Robotics and Automation, the whole paper (an octree model with unknown nodes, and views chosen to see the most unknown space)"
  - paper: doi:10.1109/ICRA.2016.7487281
    title: "Andreas Bircher, Mina Kamel, Kostas Alexis, Helen Oleynikova and Roland Siegwart, Receding horizon next-best-view planner for 3D exploration"
    locator: "Proceedings of the 2016 IEEE International Conference on Robotics and Automation, pp. 1462-1468 (the gain of a tree node, with the visible unknown volume discounted by the exponential of the path cost, and the execution of the first edge only)"
---

Next-best-view planning chooses where a sensor should look next. A robot that builds a 3D model of an object, or a map of a building, has a partial model in which some space is known to be free, some is known to be occupied and the rest is unknown. Each candidate sensor pose would reveal some of the unknown space, and getting there costs travel time. The next best view is the pose with the best trade-off between the expected gain and the cost. The problem is solved again after each scan, so it is a greedy step of a larger problem: find a short sequence of views that together see everything, which contains the [art gallery problem](/art-gallery-problem/) and is NP-hard. Connolly posed it in 1985 for scanning objects with an octree model; today it drives the exploration of aerial and ground robots.

## In plain words

You walk around a statue with a camera and want a full 3D model of it. After a few photos, some parts are still unseen: the back of the head, the underside of an arm. Where should you stand for the next photo? A spot that shows a lot of unseen surface is good, but a spot far away costs a long walk. So for each place you could stand, you count how much new surface you would see and how far you would walk, and you pick the best balance.

You decide again after each photo, because each photo changes what is still unseen. This simple rule does not always give the fewest photos, but it works well in practice.

## Definition

**Input.**

- A partial model $M$ of the scene: a voxel grid or an [octree](/octree-occupancy-map/) whose cells are free, occupied or unknown, often with an occupancy probability.
- The current sensor pose $\xi_0$, and a set $V$ of candidate poses (finite, or the continuous pose space of the robot).
- A sensor model: the field of view, the range, and the rule that a cell is seen when a ray from the sensor reaches it through cells that are not occupied.
- A travel cost $c(\xi_0, \xi)$, such as the length of a collision-free path through known free space.

**Gain.** The gain $G(\xi)$ of a pose is the number, or the volume, of unknown cells that would be seen from $\xi$. With a probabilistic model, it is the expected [information gain](/information-gain/): the expected drop in the [entropy](/shannon-entropy/) of the map after a scan from $\xi$.

**Output.** A pose $\xi^\ast \in V$ that maximizes a score $s(\xi)$ that grows with $G(\xi)$ and falls with $c(\xi_0, \xi)$. Common choices are $G(\xi) - \lambda c$, $G(\xi)/c$ and $G(\xi)\, e^{-\lambda c}$ for a weight $\lambda \ge 0$. The loop scans, updates $M$ and plans again, and stops when no pose has a gain above a threshold.

## Variants

- **Object reconstruction.** The sensor moves on a sphere or a cylinder around one object, and the goal is a complete surface model. The gain counts unknown surface, not unknown volume.
- **Scene exploration.** A mobile robot explores a building or a field. The views are reachable poses, and the travel cost is large. [Frontier-based exploration](/frontier-based-exploration/) is the special case that goes to the nearest boundary between free and unknown space, without counting the gain.
- **Inspection.** The model is known and the task is to see every surface point at a good angle and resolution. The views are planned all at once, as a covering problem, and then ordered as a tour.
- **Paths instead of points.** The gain is collected along the whole path to the view, not only at its end.
- **Several sensors or robots.** Each robot picks a view that the others do not cover.

## Examples

**The trade-off with the travel cost.** Three candidate views $A$, $B$ and $C$ would see 12, 20 and 30 unknown cells, at travel costs of 1, 3 and 8 m. With the score $G e^{-\lambda c}$:

| $\lambda$ | $A$ | $B$ | $C$ | Best |
|---|---|---|---|---|
| 0 | 12 | 20 | 30 | $C$ |
| 0.25 | 9.35 | 9.45 | 4.06 | $B$ |
| 0.5 | 7.28 | 4.46 | 0.55 | $A$ |

A small $\lambda$ sends the robot far for a large gain; a large $\lambda$ keeps it close. The ratio score $G/c$ gives 12, 6.67 and 3.75 and picks $A$.

**Greedy views are not optimal.** Six unknown cells $\{1, \dots, 6\}$ can be seen from three views: $V_1$ sees $\{1, 2, 3, 4\}$, $V_2$ sees $\{1, 2, 5\}$ and $V_3$ sees $\{3, 4, 6\}$. The greedy rule takes $V_1$ first, because it sees the most, and then needs both $V_2$ and $V_3$ to see cells 5 and 6: three views. The two views $V_2$ and $V_3$ already see all six cells. This is the classic bad case of [greedy set cover](/greedy-set-cover/).

## Known algorithms

- **Connolly's methods (1985).** On an octree with unknown nodes, Connolly scored views on a sphere around the object by the unknown space that they see. This is the original next best view method.
- **Sampling of candidate views.** Sample poses in the free space, score each one by [ray casting](/ray-casting/) through the map, and take the best. The cost is the number of samples times the number of rays times the cells per ray.
- **Receding horizon NBV (Bircher et al., 2016).** Grow a [rapidly-exploring random tree](/rapidly-exploring-random-tree/) from the robot in the known free space. The gain of a node is the gain of its parent plus the unknown volume visible from the node, multiplied by $e^{-\lambda c}$, where $c$ is the cost of the path to the node. Take the branch to the best node, execute only its first edge, and plan again. It is a heuristic with no optimality guarantee.
- **Frontier methods.** [Frontier-based exploration](/frontier-based-exploration/) and its scored versions, which add a gain term to the distance to each frontier.
- **Information-theoretic methods.** Compute the expected entropy drop of each view under a probabilistic sensor model, which favors views of uncertain cells over views of cells that are almost known.

## Bounds

- **Hardness of the full problem.** Seeing all of a polygon from the fewest points is the art gallery problem, which is NP-hard; see [art gallery problem](/art-gallery-problem/). Choosing the fewest views from a finite candidate set to see a finite set of cells is [set cover](/set-cover/), so it is NP-hard too, and the greedy rule is within a factor $\ln n + 1$ of the fewest views, where $n$ is the number of cells (theorem, see [greedy set cover](/greedy-set-cover/)).
- **Fixed number of views.** Seeing the most cells with $k$ views from a finite set is [maximum coverage](/max-coverage/). The number of cells seen is a monotone [submodular function](/submodular-function/) of the set of views, so the greedy rule sees at least $1 - 1/e$ of the best possible (theorem, for a known model). In next-best-view planning, the model is not known in advance, so this bound does not apply to the online loop.
- **Cost of one step.** Scoring $|V|$ candidates with $R$ rays each, through at most $D$ cells per ray, takes $O(|V| R D)$ time.

## Reductions

- **From the art gallery problem.** With an exact sensor model and a known polygon, picking views that see the whole polygon is the art gallery problem, or the [watchman route problem](/watchman-route-problem/) when the path length counts.
- **To set cover and maximum coverage.** With a finite set of candidate views and a known model, the planning of all views at once is set cover or maximum coverage, as in the Bounds section.
- **To coverage path planning.** When the sensor sees only what is directly under it, seeing every point means passing over it, which is [coverage path planning](/coverage-path-planning/).

## Applications

3D scanning of objects, for reverse engineering and cultural heritage. Inspection of industrial parts, bridges and power plants. Exploration of mines, buildings and caves by aerial and ground robots. Search and rescue mapping. Active perception in grasping, where the robot moves its camera to see the occluded side of an object.

## References
