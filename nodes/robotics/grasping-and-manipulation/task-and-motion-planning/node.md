---
tag: CWC7KR
kind: problem
slug: task-and-motion-planning
name: Task and motion planning
aliases:
- TAMP
- integrated task and motion planning
area: robotics/grasping-and-manipulation
level: research
summary: Plan a sequence of symbolic actions together with feasible continuous motions for each, so the plan can be run by a real robot.
prereqs: [motion-planning, classical-planning, manipulation-planning]
see_also: [pomdp-planning, strips-plan-existence-pspace-complete, pddl, htn-planning, constraint-satisfaction-problem, probabilistic-roadmap, piano-movers-problem, belief-space]
sources:
  - paper: doi:10.1109/ICRA.2011.5980391
    title: Leslie Pack Kaelbling and Tomás Lozano-Pérez, Hierarchical task and motion planning in the now, IEEE International Conference on Robotics and Automation (ICRA), 1470-1477, 2011
    locator: the whole paper (a hierarchical planner that commits to the first steps of an abstract plan and plans motions for them before it refines the rest)
  - paper: "Caelan Reed Garrett, Rohan Chitnis, Rachel Holladay, Beomjoon Kim, Tom Silver, Leslie Pack Kaelbling and Tomás Lozano-Pérez, Integrated task and motion planning, Annual Review of Control, Robotics, and Autonomous Systems 4, 265-293, 2021"
    locator: the whole paper (a survey of the formulations and methods of task and motion planning)
  - paper: doi:10.1177/0278364904045471
    title: Thierry Siméon, Jean-Paul Laumond, Juan Cortés and Anis Sahbani, Manipulation planning with probabilistic roadmaps, The International Journal of Robotics Research 23(7-8), 729-746, 2004
    locator: the whole paper (the geometric layer that task and motion planning extends with symbolic actions)
---

Task and motion planning (TAMP) asks for a robot plan at two levels at once: a sequence of discrete actions, such as "pick the cup" and "open the door", and for each action a continuous motion that the robot can run without collision. A symbolic planner alone can choose actions that no motion can carry out, for example picking a cup that another object blocks. A [motion planner](/motion-planning/) alone cannot choose the order of many actions. TAMP joins the two, so that the symbolic choices and the geometric facts constrain each other.

## In plain words

A robot must put a cup in a cupboard. A list of steps is easy: open the door, pick the cup, place it inside. But a bowl stands in front of the shelf, so the robot must first move the bowl, and it must put the bowl where it does not block the door. It must also choose how to hold the cup so that it fits through the door. None of this shows in the list of steps until the robot checks the geometry. A task and motion planner finds the steps and the motions together, and changes the steps when a motion turns out to be impossible.

## Definition

A TAMP problem has a *hybrid state*: discrete facts (which object is in the hand, which door is open) and continuous values (the poses of the robot and the objects). It has *action schemas* with parameters, as in [PDDL](/pddl/) or [STRIPS](/strips/), but some parameters are continuous: a grasp, a placement pose, a robot configuration, or a trajectory. Each action has:

- symbolic preconditions and effects on the facts, as in [classical planning](/classical-planning/);
- geometric constraints on its continuous parameters: kinematic constraints (the hand at the grasp pose is reachable by [inverse kinematics](/inverse-kinematics/)), stability (a placement rests on a surface), and collision-free motion (the trajectory avoids every obstacle in the current state).

**The problem.** Given an initial hybrid state and a goal formula on the facts, find a sequence of actions together with values for all their continuous parameters such that every precondition and every geometric constraint holds when the action runs, and the goal holds at the end.

A *plan skeleton* is the sequence of actions with the continuous parameters left open. For a fixed skeleton, choosing the parameters is a [constraint satisfaction problem](/constraint-satisfaction-problem/) over continuous variables, with collision constraints that are not convex.

## Variants

- **Fully observed and deterministic.** The state is known and the actions do what they say. This is the base case.
- **Partially observed.** The robot does not know where some objects are and must plan sensing actions too. The problem becomes planning in a [belief space](/belief-space/), as in [POMDP planning](/pomdp-planning/), with continuous motions.
- **Optimal TAMP.** Minimize the total cost, such as the path length or the time, not just find a plan.
- **Hierarchical TAMP.** Actions are refined into sub-actions, as in [HTN planning](/htn-planning/); Kaelbling and Lozano-Pérez (2011) plan the first steps at full detail and leave the later ones abstract until the robot gets to them.
- **With learning.** Learned models propose grasps, placements or plan skeletons, to cut down the search; the planner still checks the constraints.

## Examples

**Moving a blocker.** Objects $A$ and $B$ stand on a shelf, with $B$ in front of $A$. The goal is $A$ in the robot's hand. The symbolic plan "pick $A$" has no collision-free motion, since every path to $A$ passes through $B$. A TAMP planner finds the plan "pick $B$, place $B$ at pose $p$, pick $A$", where $p$ is a free pose on the table that does not block the path to $A$. The symbolic level knows nothing about the blocking until the motion level reports it.

**Stacking with a fixed grasp.** To stack a long block on a short one, the robot must hold the long block at its end so that its fingers do not hit the short block during the placement. The grasp chosen in the first action is constrained by the motion of the last one, so the continuous parameters of different actions depend on each other.

## Known algorithms

Garrett and others (2021) survey the methods. They differ in when the continuous values are chosen.

- **Sequence first.** Search for a plan skeleton with a symbolic planner, then try to bind its continuous parameters by sampling or optimization. If the binding fails, add the failure as a new fact or constraint and search for another skeleton.
- **Satisfaction first.** Sample many continuous values in advance (grasps, placements, configurations, and roadmap motions between them, as in a [probabilistic roadmap](/probabilistic-roadmap/)), turn them into discrete objects, and then solve one discrete planning problem over them.
- **Interleaved.** Search over plan prefixes and sample continuous values as the search reaches each action. Kaelbling and Lozano-Pérez (2011) plan hierarchically "in the now": they refine and run the first step of an abstract plan before they plan the rest in detail.
- **Optimization based.** Fix a skeleton and solve one nonlinear program for all the continuous values and trajectories at once, then search over skeletons. These methods handle constraints that couple many actions but find only local optima.

Sampling-based methods of these kinds are probabilistically complete under conditions on the samplers; none of them is complete in the exact sense for the general problem.

## Bounds

- **PSPACE-hard.** TAMP contains plan existence for propositional [STRIPS](/strips/) planning, which is PSPACE-complete (Bylander 1994; see [STRIPS plan existence](/strips-plan-existence-pspace-complete/)), as the case with no geometry. It also contains motion planning, as the case of one action with a free trajectory, and the [generalized piano movers' problem](/piano-movers-problem/) is PSPACE-hard. Either reduction makes TAMP PSPACE-hard (a theorem).
- **No general upper bound is given here.** With continuous parameters and an unbounded number of actions, the upper bound depends on the formulation.

## Reductions

- **From classical planning.** A STRIPS problem is a TAMP problem with no continuous parameters.
- **From motion planning and manipulation planning.** A motion planning query is a TAMP problem with one move action; [manipulation planning](/manipulation-planning/) is a TAMP problem with pick and place actions and no other symbolic goals.
- **To constraint satisfaction per skeleton.** For a fixed skeleton, TAMP is a continuous constraint satisfaction problem, which is how sequence-first methods use it.
- **To POMDPs under uncertainty.** With noisy sensing, TAMP is a [POMDP](/pomdp/) with a hybrid state, solved approximately by [POMDP planning](/pomdp-planning/) in belief space.

## Applications

Household and service robots that tidy, cook or load a dishwasher; mobile manipulators in warehouses and factories that must clear the way before they pick; assembly with many parts and tools; and any robot task where the order of actions depends on the geometry of the scene.

## References
