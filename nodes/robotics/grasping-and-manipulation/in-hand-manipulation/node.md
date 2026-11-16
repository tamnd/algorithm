---
tag: 0GV370
kind: problem
slug: in-hand-manipulation
name: In-hand manipulation
aliases:
- dexterous manipulation
area: robotics/grasping-and-manipulation
level: advanced
summary: Change the pose of a grasped object within the hand by rolling, sliding and regrasping with the fingers.
prereqs: [grasp-matrix, force-closure, montana-contact-kinematics]
see_also: [grasp-synthesis, manipulation-planning, caging-grasp, nonholonomic-constraint, rigid-contact-complementarity, hybrid-automata, imitation-learning, cooperative-manipulation]
sources:
  - paper: "Allison M. Okamura, Niels Smaby and Mark R. Cutkosky, An overview of dexterous manipulation, IEEE International Conference on Robotics and Automation (ICRA), vol. 1, 255-262, 2000"
    locator: the whole paper (a survey of the methods of dexterous manipulation, including rolling, sliding and finger gaiting)
  - paper: doi:10.1177/027836498800700302
    title: David J. Montana, The kinematics of contact and grasp, The International Journal of Robotics Research 7(3), 17-32, 1988
    locator: the whole paper (the kinematics of rolling and sliding contacts between fingers and an object)
  - book: isbn:9780849379819
    title: Richard M. Murray, Zexiang Li and S. Shankar Sastry, A Mathematical Introduction to Robotic Manipulation, CRC Press, 1994
    locator: Chapter 5 (multifingered hand kinematics, the grasp map and the hand Jacobian, and rolling contact)
  - paper: doi:10.1109/70.88118
    title: Zexiang Li and John F. Canny, Motion of two rigid bodies with rolling constraint, IEEE Transactions on Robotics and Automation 6(1), 62-72, 1990
    locator: the whole paper (which contact configurations can be reached by rolling, and a path planner when one body is flat)
  - paper: doi:10.1177/0278364919887447
    title: OpenAI (Marcin Andrychowicz and others), Learning dexterous in-hand manipulation, The International Journal of Robotics Research 39(1), 3-20, 2020
    locator: the whole paper (a policy learned in simulation with randomized physics that turns a block in a real five-finger hand)
---

In-hand manipulation asks a multi-finger hand to change the pose of an object that it already holds, without putting the object down. The fingers can roll on the object, let it slide, lift one finger and put it at a new place while the others hold, or use gravity and outside surfaces. The difficulty is that the object must stay held during the whole motion, while the contacts change. [Grasp synthesis](/grasp-synthesis/) chooses one grasp; in-hand manipulation moves from one grasp to another and turns the object in the hand.

## In plain words

You pick up a pen and turn it in your fingers until the tip points down, ready to write. You do not put it on the table. You roll it between your thumb and fingers, let it slide a little, and move one finger at a time to a new place while the others hold it. A robot hand must do the same: it has a pen in its fingers and a goal pose for the pen, and it must find finger motions that reach the goal and never drop it.

## Definition

A hand with $k$ fingers holds a rigid object. The state has:

- the pose $g \in SE(3)$ of the object relative to the palm;
- the joint angles $\theta$ of the fingers;
- for each finger in contact, the contact coordinates $(\alpha_f, \alpha_o, \psi)$ of [Montana's equations](/montana-contact-kinematics/), and its *contact mode*: rolling, sliding, or broken.

The joint velocities and the object twist are related at each contact by the contact model. For rolling contacts the relation is $J_h(\theta, g)\, \dot\theta = G(g)^T \dot g$, where $J_h$ is the hand Jacobian and $G$ is the [grasp map](/grasp-matrix/). A motion is *feasible* if at every instant there are contact forces in the friction cones that balance the external wrench on the object (gravity, and inertia if the motion is not slow); for the quasi-static case this is the condition of the [force closure](/force-closure/) or equilibrium grasp at each instant.

**The problem.** Given an initial grasp and a goal pose $g^*$ of the object relative to the palm, find a sequence of contact modes and a joint trajectory $\theta(t)$ that is feasible at every instant and ends with the object at $g^*$ in a stable grasp.

## Variants

- **Rolling only.** The fingers keep their contacts and roll on the object. The rolling constraint is [nonholonomic](/nonholonomic-constraint/): a small number of fingers can still reach many object poses by rolling along suitable paths.
- **Sliding.** A finger slides on the object, at the edge of its friction cone, to move the contact. This needs control of the contact forces, not only of positions.
- **Finger gaiting.** Some fingers hold the object in a stable grasp while another lifts off and moves to a new contact. A plan is a sequence of grasps in which consecutive grasps share a stable subgrasp.
- **Regrasping.** The object is put down on a table or held by the other hand and grasped again. This is the pick-and-place case of [manipulation planning](/manipulation-planning/).
- **External contacts.** The object is pushed against a table or a wall, or turned by gravity while held loosely (pivoting), so the environment acts as one more finger.
- **Under uncertainty.** The pose of the object and the contact locations are known only through tactile and visual sensing, and the plan must work for a set of possible states.

## Examples

**A ball between two flat fingers.** Two parallel flat fingers hold a ball of radius $\rho$, one above and one below. The lower finger is still and the upper finger moves sideways by $d$. If the contacts roll without slipping, the center of the ball moves by $d/2$ and the ball turns by $d / (2\rho)$ radians about the axis parallel to the fingers and normal to the motion. The contact point moves by $d/2$ on each finger and by an arc of length $d/2$ on the ball, as [Montana's equations](/montana-contact-kinematics/) give for a sphere on a plane. Moving the upper finger along a closed path can bring the ball back to its position with a new orientation, which is the nonholonomic effect.

**Turning a block with finger gaits.** Three fingers hold a block. To turn it by 90 degrees about a vertical axis, the hand turns it as far as the finger joints allow, then holds it with two fingers while the third moves to a new place, and repeats. Each gait step must keep a stable two-finger grasp, so the plan is a path in a graph of grasps.

**A learned policy.** Andrychowicz and others (2020) trained a policy in simulation with randomized physical parameters and used it on a real five-finger hand to turn a block to target orientations (a measurement on their hardware). The policy uses finger gaiting and rolling that were not programmed by hand.

## Known algorithms

- **Grasp map control.** For rolling contacts and a desired object twist, solve $J_h \dot\theta = G^T \dot g$ for the joint velocities, and choose internal forces that keep each contact force in its friction cone (Murray, Li and Sastry 1994). This tracks a path of the object while the contacts roll, as long as the grasp stays feasible.
- **Rolling path planning.** For two bodies with a rolling contact, Li and Canny (1990) decide which contact configurations can be reached and give a planner when one body is flat. More general rolling paths use methods of nonholonomic motion planning.
- **Graph search over grasps.** Sample stable grasps, connect two grasps when one finger gait or one rolling motion moves between them, and search the graph. This is the [probabilistic roadmap](/probabilistic-roadmap/) idea applied to grasps, and it is complete only in the probabilistic sense.
- **Contact-implicit optimization.** Write the contact modes and friction cones as [complementarity constraints](/rigid-contact-complementarity/) or as integer variables, and optimize the joint and force trajectories with the mode sequence as part of the solution. Local solvers find good motions but have no global guarantee.
- **Learning.** Train a policy with reinforcement learning in simulation, or by [imitation](/imitation-learning/) of human demonstrations. Results are measured on hardware, not proved.

## Bounds

No complexity bound specific to in-hand manipulation is given here. What is proved concerns parts of the problem:

- **Grasps along the way.** Each intermediate grasp that holds a planar object by frictionless point contacts needs at least four fingers, and a spatial one at least seven (the [finger bounds for form closure](/finger-bounds-for-form-closure/)), which limits finger gaiting without friction.
- **Reachability by rolling.** For a sphere rolling on a plane, every contact configuration can be reached (a theorem; Li and Canny 1990 treat rolling of two bodies in general).

## Reductions

- **To manipulation planning.** The hand is several robots that share one object, and the contact modes split the joint space of hand and object into modes, as in [manipulation planning](/manipulation-planning/). Regrasping on a table is exactly a pick-and-place plan.
- **To hybrid systems.** With rolling, sliding and broken contacts as discrete modes and the joint motion as the continuous state, the problem is a planning problem for a [hybrid automaton](/hybrid-automata/).
- **From cooperative manipulation.** When the fingers are separate arms, the problem is [cooperative manipulation](/cooperative-manipulation/) with changing contacts.

## Applications

Assembly that needs a part in a precise pose in the gripper, such as inserting a pin; tool use, where a tool must be turned in the hand before use; prosthetic and humanoid hands; and picking in warehouses, where an object grasped in an awkward pose must be turned before it is placed. Okamura, Smaby and Cutkosky (2000) survey the methods and their use with real hands.

## References
