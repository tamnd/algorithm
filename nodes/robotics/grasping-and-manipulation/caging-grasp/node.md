---
tag: M3EH9D
kind: concept
slug: caging-grasp
name: Caging
aliases:
- caging grasp
- object caging
area: robotics/grasping-and-manipulation
level: advanced
summary: Placing fingers so the object cannot escape to infinity, though it may move inside the cage, a weaker but robust kind of grasp.
prereqs: [configuration-space, form-closure]
see_also: [force-closure, grasp-synthesis, antipodal-grasp, manipulation-planning, fixture-planning, cooperative-manipulation, minkowski-sum, cell-decomposition]
sources:
  - paper: "Elon Rimon and Andrew Blake, Caging planar bodies by one-parameter two-fingered gripping systems, The International Journal of Robotics Research 18(3), 299-318, 1999 (an earlier version appeared at ICRA 1996)"
    locator: the whole paper (cages of a planar object by two fingers whose opening is one parameter, and the opening at which the cage breaks)
  - paper: doi:10.1177/0278364912442972
    title: Alberto Rodriguez, Matthew T. Mason and Steve Ferry, From caging to grasping, The International Journal of Robotics Research 31(7), 886-900, 2012
    locator: the whole paper (the relation between cages and grasps, and cages from which closing the fingers leads to a grasp)
---

Caging is the placement of fingers or other obstacles around an object so that the object cannot escape, even though it can still move a little. The fingers do not need to touch the object or hold it still. This is the difference from [form closure](/form-closure/) and [force closure](/force-closure/): those immobilize the object, while a cage only traps it in a bounded region. Because nothing has to be exact, a cage is robust to errors in the position of the fingers and in the model of friction, and closing the fingers from a cage is a common way to reach a real grasp.

## In plain words

Put three pegs around a coin on a table, a bit wider apart than needed to touch it, but not wide enough for the coin to slip between two pegs. The coin can rattle inside, but it cannot get out. You have caught it without gripping it. If the pegs then close in, the coin ends up held tight, and it does not matter exactly where it was inside. A cage is a trap, not a grip: it promises that the object stays nearby, not that it stays still.

## The idea

Let $C$ be the [configuration space](/configuration-space/) of the object, for a planar rigid object the poses $(x, y, \theta)$. Fix the fingers. The *free space* $C_{\text{free}}$ is the set of poses in which the object does not overlap a finger. The object is *caged* at a pose $q \in C_{\text{free}}$ if the connected component of $C_{\text{free}}$ that contains $q$ is bounded in the position coordinates. Then every motion of the object that does not pass through a finger keeps it in that bounded set: it cannot escape to infinity.

Some points follow from this definition.

- **No contact needed.** A cage can hold the object with a gap all around. Form closure is the limit case in which the component shrinks to the single pose $q$.
- **No forces.** Caging is purely geometric. It needs no friction coefficient and no model of the contact forces, which is the source of its robustness.
- **A set of poses.** The cage holds for every pose in the component, so a planner can choose finger positions that cage the object for all the poses that its sensors allow.
- **Escape paths.** To show that a placement is not a cage, it is enough to find one path in $C_{\text{free}}$ from $q$ to a far pose. To show that it is a cage, one must show that no such path exists, which is a question about the connectivity of $C_{\text{free}}$, the same question as in exact [motion planning](/motion-planning/) with [cell decomposition](/cell-decomposition/).

Rimon and Blake (1999) studied cages of a planar object by two fingers whose distance is one parameter, as in a parallel-jaw gripper. As the fingers open, the cage persists until a critical opening at which the bounded component meets the rest of the free space, and they characterize that opening. When the fingers close from a cage, the free component shrinks, and the object is driven toward an immobilizing grasp. Rodriguez, Mason and Ferry (2012) studied this link between cages and grasps: they describe cages from which closing the fingers is sure to reach a grasp, so that a cage is a safe first step of grasping.

## Examples

**A disc in three point fingers.** A disc of radius $r$ and three point fingers at the corners of an equilateral triangle with side $s$. The fingers are at distance $s / \sqrt{3}$ from the center of the triangle, so the disc fits at the center if $s \ge \sqrt{3}\, r$. It can leave only between two fingers, and the gap between two fingers is $s$, so it can pass if $s \ge 2r$. So the disc is caged if and only if $\sqrt{3}\, r \le s < 2r$, with the disc's center near the middle of the triangle. With $r = 1$ and $s = 1.8$ it is caged: it fits, since $1.8 / \sqrt{3} \approx 1.04 > 1$, and at the middle of each side the center would be only $0.9$ from both fingers, so it cannot pass. At $s = \sqrt{3}\, r$ the cage is a form closure of the disc's position: the three fingers touch it at 120 degrees and the center cannot move.

**One finger in a ring.** A flat ring with inner radius $r_1$ and one point finger in its hole. The ring can turn freely and slide until the inner edge meets the finger, so its center stays within distance $r_1$ of the finger, and it can never leave. One finger is enough to cage it, although at least four frictionless fingers are needed to hold a planar object in form closure. Shapes with holes and concave parts are the easy cases for caging; for convex shapes more fingers are needed, and their placement is a question of the connectivity of the free space.

**Non-example: a cup over a ball on a table.** An upside-down cup over a ball on a table traps it, but only with the help of the table. A cage in the strict sense needs the fingers alone to bound the free component; with the table as one more obstacle, the same definition applies to the fingers and the table together.

## Where it is used

- **Grasping under uncertainty.** A hand can first form a cage around an object whose pose is not well known and then close the fingers. The cage limits where the object can be, and the closing turns it into a grasp (a heuristic strategy, with guarantees in the cases that Rodriguez, Mason and Ferry analyze).
- **Transport by many robots.** Several mobile robots can surround an object and push it while keeping it caged, so it moves with the group without a firm grip. This is one form of [cooperative manipulation](/cooperative-manipulation/).
- **Fixtures and feeders.** A fixture or a feeder that traps a part loosely can tolerate parts with errors of shape, as in [fixture planning](/fixture-planning/).
- **Planning.** In [manipulation planning](/manipulation-planning/), a cage is a mode in which the object moves with the hand without an exact grasp, which widens the set of motions a planner can use.

## References
