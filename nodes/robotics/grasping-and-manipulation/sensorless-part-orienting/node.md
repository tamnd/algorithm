---
tag: WCHSRJ
kind: problem
slug: sensorless-part-orienting
name: Sensorless part orienting
aliases:
- sensorless manipulation
area: robotics/grasping-and-manipulation
level: advanced
summary: Bring a part from any unknown orientation to one known orientation by a fixed sequence of actions without sensing, such as squeezes, pushes or tilts of a tray.
prereqs: [belief-space, conformant-planning]
see_also: [goldberg-part-orienting-algorithm, quasi-static-pushing, mason-voting-theorem, fixture-planning, breadth-first-search, np-hard, pomdp-planning, manipulation-planning]
sources:
  - paper: doi:10.1109/56.800
    title: Michael A. Erdmann and Matthew T. Mason, An exploration of sensorless manipulation, IEEE Journal of Robotics and Automation 4(4), 369-379, 1988
    locator: the whole paper (orienting planar parts without sensors by tilting a tray)
  - paper: doi:10.1007/BF01891840
    title: Kenneth Y. Goldberg, Orienting polygonal parts without sensors, Algorithmica 10, 201-225, 1993
    locator: "Sections 3 to 7 (every polygonal part can be oriented up to symmetry by squeezes, a shortest plan in O(n^2 log n) time, plans of length O(n^2)) and Section 8 (push-grasp actions)"
  - paper: doi:10.1007/BF01192046
    title: Yu-Bin Chen and Doug J. Ierardi, The complexity of oblivious plans for orienting and distinguishing polygonal parts, Algorithmica 14(5), 367-397, 1995
    locator: the whole paper (plans of O(n) squeezes)
  - paper: doi:10.1137/0219033
    title: David Eppstein, Reset sequences for monotonic automata, SIAM Journal on Computing 19(3), 500-510, 1990
    locator: the whole paper (shortest reset sequences of monotonic automata by breadth-first search, bounds on their length, and NP-hardness of the shortest reset sequence for general automata)
  - paper: "B. K. Natarajan, An algorithmic approach to the automated design of parts orienters, 27th Annual Symposium on Foundations of Computer Science (FOCS), 132-142, 1986"
    locator: the whole paper (the design of parts orienters as a problem on finite automata)
  - book: isbn:9780262133968
    title: Matthew T. Mason, Mechanics of Robotic Manipulation, MIT Press, 2001
    locator: Chapter 7, Section 7.4 (parts orienting)
---

Sensorless part orienting asks for a fixed sequence of actions that brings a part from any orientation to one known orientation, without a camera or any other sensor. The actions use the mechanics of contact: a gripper that squeezes the part turns it to a stable orientation, a fence that pushes it turns it against a flat side, a tray that tilts makes it slide into a corner. Each action maps many orientations to a few, and a good sequence maps all of them to one. This page is the general problem; [Goldberg's part orienting algorithm](/goldberg-part-orienting-algorithm/) is the algorithm for one case, a parallel-jaw gripper that squeezes a polygon.

## In plain words

A part falls onto a table in some unknown way. The robot must put it into one known pose, but it cannot see the part. It can still act on the part. If it closes a gripper on it, the part turns until a flat side lies against a jaw, and only a few results are possible. A second squeeze at a well chosen angle merges some of these results. The question is whether some list of actions, chosen in advance, always ends in the same pose, and what the shortest such list is. The answer is a plan that a simple machine can repeat forever, with no sensing and no decisions.

## Definition

Let $X$ be the set of possible orientations of the part (the circle of angles, or a finite set of stable orientations) and $A$ a set of actions. Each action $a$ is a known map $f_a : X \to X$; the actions are deterministic, and the model of the contact mechanics (for example [quasi-static](/quasi-static-pushing/) motion with Coulomb friction) defines the maps. A plan is a finite sequence $a_1, \ldots, a_k$ of actions. It *orients* the part if the image

$$f_{a_k} \circ \cdots \circ f_{a_1}(X)$$

is a single orientation. The problem: given the part and the action set, decide whether a plan exists and find a shortest one.

Symmetry limits what any plan can do. If every action commutes with a turn by an angle $T$, then two orientations $T$ apart stay $T$ apart, and a plan can only orient the part up to that symmetry. The goal is then a single orientation modulo $T$.

The plan is open loop: it is the same for every initial orientation. In the language of planning, the set of possible states is the [belief state](/belief-space/), each action maps one set to the next, and the problem is [conformant planning](/conformant-planning/) with deterministic actions and a goal of one state.

## Variants

- **Squeeze plans.** A parallel-jaw gripper turns to an angle and closes. Without friction at the jaws, the part turns to a local minimum of its width. This is the case of [Goldberg's algorithm](/goldberg-part-orienting-algorithm/).
- **Push-grasp plans.** One jaw touches first and pushes the part, so it turns to a stable side relative to its center of mass, and then the other jaw closes. Goldberg (1993) treats these too; they can resolve symmetries that squeezes cannot.
- **Push plans and fences.** A pusher or a row of fences over a conveyor belt pushes the part. The rotation under a push follows the [quasi-static pushing](/quasi-static-pushing/) model, and [Mason's voting theorem](/mason-voting-theorem/) gives its sense.
- **Tray tilting.** Erdmann and Mason (1988) tilt a tray so that the part slides into walls and corners.
- **Recognition as well as orientation.** A plan can also be asked to distinguish parts of different shapes by their final poses (Chen and Ierardi 1995).
- **Positions as well as orientations.** Some action sets also bring the part to a known position, which matters for the next step of an assembly.

## Examples

A rectangle under a frictionless parallel-jaw gripper. Each squeeze leaves the rectangle with a long side or a short side against the jaws. A squeeze at angle 0 leaves it at one of two orientations, 90 degrees apart. A second squeeze with the gripper turned by 45 degrees maps both to the same orientation, modulo the half turn that the rectangle's symmetry cannot remove. Two squeezes are needed and enough.

A square, or any regular polygon, needs only one squeeze up to its symmetry. Its width function has one minimum per period, so one squeeze already leaves it in a single orientation modulo the period.

A general quadrilateral with no symmetry, such as the one with vertices $(-42, -41)$, $(48, -41)$, $(39, 25)$ and $(-34, 59)$ in Goldberg's paper, needs four squeezes. Squeezes alone leave a half-turn ambiguity even for a part with no symmetry, because the gripper turned by 180 degrees is the same gripper.

## Known algorithms

- **Goldberg's algorithm** for squeeze and push-grasp plans on a polygon with $n$ vertices. It builds the step function of the action and searches backward over intervals of orientations. It finds a shortest plan in $O(n^2 \log n)$ time (Goldberg 1993).
- **Breadth-first search over sets of states.** When the actions map a finite set of stable states to itself, search the sets of possible states from the full set, with [breadth-first search](/breadth-first-search/), until a set with one element appears. Eppstein (1990) shows that for monotonic automata, those whose maps keep the cyclic order of the states as squeezes do, a shortest plan is found by breadth-first search in polynomial time.
- **Greedy merging.** Merge two states at a time with a shortest sequence that maps them to one state, and repeat. This finds a plan, not always a shortest one, whenever every pair of states can be merged.
- **Belief-space search.** For actions with noise, plan in a space of probability distributions or of sets with error margins, as in [POMDP planning](/pomdp-planning/).

## Bounds

- **Existence.** For a polygonal part and frictionless squeezes, a plan that orients the part up to the symmetry of its squeeze function always exists (Goldberg 1993, a theorem).
- **Plan length.** Goldberg proves plans of $O(n^2)$ squeezes and conjectured $O(n)$; Chen and Ierardi (1995) proved that $O(n)$ squeezes always suffice (a theorem).
- **Planning time.** Goldberg's algorithm runs in $O(n^2 \log n)$ time. For monotonic automata with a fixed action set, Eppstein's breadth-first search is polynomial.
- **Hardness.** For general finite automata, deciding whether a reset sequence of length at most $k$ exists is [NP-hard](/np-hard/) (Eppstein 1990). So the shortest plan for arbitrary deterministic actions on a finite set of states is hard; the monotone structure of squeezes and pushes is what makes the polygon case easy.

## Reductions

With a finite set of stable states, each action is a map of a finite set to itself, so the part and its actions form a deterministic finite automaton with one letter per action. A plan that orients the part is a *reset sequence*, or synchronizing word, of the automaton: a word that sends every state to the same state. Natarajan (1986) wrote parts orienter design in this form, and Eppstein (1990) gave the breadth-first search and the hardness result in it.

In the other direction, the problem is a special case of [conformant planning](/conformant-planning/): the initial belief is the set of all orientations, the actions are deterministic, and the goal is any single state. Planning in the [belief space](/belief-space/) of sets of orientations is the same search.

## Applications

The main use is parts feeding in automated assembly: a feeder must deliver each part in a known pose to the next machine. A fixed plan can be built into hardware, for example as a sequence of fences above a conveyor, or as a program for a simple gripper, and it does not need a camera or its calibration. The same idea, actions chosen so that the result does not depend on the unknown state, appears in [fixture planning](/fixture-planning/) and in the planning of compliant motions with uncertainty.

## References
