---
tag: 70YDGQ
kind: definition
slug: kinematic-chain
name: Kinematic chain
aliases:
- serial chain
- open chain
area: robotics/robot-kinematics
level: intro
summary: Rigid links joined by joints. An open chain has no loops, as in a serial robot arm; a closed chain has loops, as in a four-bar linkage or a parallel robot.
prereqs: [kinematic-pair]
see_also: [kinematic-pair, grubler-formula, forward-kinematics, parallel-manipulator, four-bar-linkage, watt-and-stephenson-six-bar, vector-loop-closure, slider-crank-mechanism]
sources:
  - book: "Franz Reuleaux, The Kinematics of Machinery: Outlines of a Theory of Machines, translated by Alexander B. W. Kennedy, Macmillan, London, 1876 (German original: Theoretische Kinematik, Vieweg, Braunschweig, 1875)"
    locator: the chapters on kinematic chains and mechanisms, where a mechanism is a closed chain with one link fixed (general locator)
  - book: isbn:9781107156302
    title: Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017
    locator: Chapter 2, Section 2.2 (open chains and closed chains, Grübler's formula), and Chapter 7, Kinematics of Closed Chains
  - book: isbn:9781846286414
    title: Bruno Siciliano, Lorenzo Sciavicco, Luigi Villani and Giuseppe Oriolo, Robotics, Modelling, Planning and Control, Springer, 2009
    locator: Section 2.8, Direct Kinematics, with Section 2.8.1 (open chain) and Section 2.8.3 (closed chain)
---

A kinematic chain is a set of rigid links joined by [kinematic pairs](/kinematic-pair/), the joints. If the joints form no loop, the chain is open: a serial robot arm is an open chain from a fixed base to a free hand. If the joints form loops, the chain is closed: a four-bar linkage, a car suspension and a parallel robot are closed chains. A mechanism is a chain with one link fixed as the ground. The chain is the object that [Grübler's formula](/grubler-formula/) counts and that [forward kinematics](/forward-kinematics/) evaluates.

## Definition

**Kinematic chain.** A kinematic chain is a finite set of rigid bodies, the **links**, and a finite set of [kinematic pairs](/kinematic-pair/), the **joints**, where each joint connects two different links. Its **graph** has one vertex for each link and one edge for each joint. We assume the graph is connected. Let $N$ be the number of links and $J$ the number of joints.

**Mechanism.** A chain with one link chosen as fixed is a mechanism, and the fixed link is the **ground** or the **base**. Fixing a different link of the same chain gives a different mechanism, an **inversion** of the chain. Robotics texts count the ground among the $N$ links, and so does this page.

**Open and closed chains.** A chain is **open** if its graph has no cycle, so the graph is a tree. It is a **serial** chain if the tree is a path, with the ground at one end. Branched open chains, such as a humanoid with two arms and two legs, are **trees**. A chain is **closed** if its graph has a cycle. A closed chain is also called a loop or a closed-loop mechanism, and a robot built on one is a [parallel manipulator](/parallel-manipulator/) when its end effector is held by two or more chains from the base.

**Number of loops.** A connected chain has

$$L = J - N + 1$$

independent loops. *Proof.* Take a spanning tree of the graph. It has $N - 1$ edges. Each of the other $J - N + 1$ edges closes exactly one cycle with the tree, and these cycles are a basis of the cycle space of the graph, so every loop of the chain is a sum of them. An open chain has $J = N - 1$ and $L = 0$. $\blacksquare$

Each loop gives one vector closure equation, the [vector loop closure](/vector-loop-closure/) of the mechanism, with $m = 3$ scalar equations in the plane and $m = 6$ in space. This is why closed chains need equations to be solved, while open chains do not.

## Examples and non-examples

The table counts links, joints and loops. Each row can be checked by drawing the graph.

| chain | $N$ | $J$ | $L = J - N + 1$ | type |
|---|---|---|---|---|
| a 6R industrial arm with its base | 7 | 6 | 0 | serial, open |
| planar four-bar linkage | 4 | 4 | 1 | closed |
| slider-crank | 4 | 4 | 1 | closed |
| Watt or Stephenson six-bar | 6 | 7 | 2 | closed |
| Stewart-Gough platform with 6 UPS legs | 14 | 18 | 5 | closed, parallel |
| a humanoid tree with a torso and 4 limbs of 6 joints | 25 | 24 | 0 | open tree |

**The four-bar.** Links: ground, crank, coupler, rocker. Joints: four revolute pairs in a ring. The graph is a 4-cycle, so $L = 4 - 4 + 1 = 1$, and the one loop gives the closure equation $a e^{i\theta_2} + b e^{i\theta_3} = d + c e^{i\theta_4}$ of the [four-bar linkage](/four-bar-linkage/). Fixing the crank instead of the ground gives an inversion with other motions, and the [Grashof condition](/grashof-condition/) tells which inversions have a link that turns fully.

**The Stewart-Gough platform.** Links: the ground, the moving platform, and two links in each of 6 legs, so $N = 2 + 12 = 14$. Joints: a universal, a prismatic and a spherical pair in each leg, so $J = 18$. Then $L = 18 - 14 + 1 = 5$. Six legs from one base to one platform make 6 paths, and 6 paths between two vertices close 5 independent loops.

**Non-example: a set of links that touch only by friction.** A stack of blocks on a table has no joints that hold for all time, so it is not a chain in this sense, even if it does not move.

**Non-example: a cable-driven robot.** A cable pulls but cannot push, so it is a unilateral constraint and not a pair. A cable robot is analyzed with inequality constraints, not as a closed chain with loop equations.

## Related definitions

- [Kinematic pair](/kinematic-pair/): the joints, the edges of the chain.
- [Grübler's formula](/grubler-formula/): the mobility of a chain, $m(N - 1 - J) + \sum f_i$, which is also $\sum f_i - mL$.
- [Forward kinematics](/forward-kinematics/): for an open chain, the end effector pose is a product of one transform per joint.
- [Parallel manipulator](/parallel-manipulator/): a robot built on a closed chain.
- [Four-bar linkage](/four-bar-linkage/), [slider-crank mechanism](/slider-crank-mechanism/) and [Watt and Stephenson six-bars](/watt-and-stephenson-six-bar/): the classic closed chains with one and two loops.

### History

Reuleaux (1875) defined the kinematic chain as a closed set of pairs and the mechanism as a chain with one link fixed, and he used inversions to classify machines. The robotics usage is wider. It calls a serial arm an open chain, though Reuleaux's chains were closed, and it counts the ground as a link.

## References
