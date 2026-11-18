---
tag: QJ3V2G
kind: algorithm
slug: footskate-cleanup
name: Footskate cleanup
aliases:
- foot sliding removal
area: graphics-and-signals/character-animation
level: advanced
summary: "Remove the sliding of planted feet in edited motion by moving the root, changing the leg joint angles with analytic inverse kinematics, and stretching the legs a little if needed."
model: real-ram
complexity:
  vars: {f: the number of frames}
  time: {cleanup: O(f^2), cleanup_with_sweep: O(f)}
  space: {extra: O(f)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2002
  people: [Lucas Kovar, John Schreiner, Michael Gleicher]
  note: "Kovar, Schreiner and Gleicher presented footskate cleanup at the Symposium on Computer Animation in 2002."
prereqs: [two-bone-inverse-kinematics, skeletal-animation]
see_also: [motion-retargeting, inverse-kinematics, motion-blending, motion-graph, motion-warping, registration-curves, character-skeleton]
sources:
  - paper: doi:10.1145/545261.545277
    title: "Lucas Kovar, John Schreiner and Michael Gleicher, Footskate cleanup for motion capture editing, ACM SIGGRAPH/Eurographics Symposium on Computer Animation, 2002, 97 to 104"
    locator: "the footplant constraints, the change of the root position and of the leg joint orientations by analytic inverse kinematics, the small change of bone lengths, and the blend of the changes around the constraints"
  - paper: doi:10.1145/566654.566605
    title: "Lucas Kovar, Michael Gleicher and Frederic Pighin, Motion graphs, ACM Transactions on Graphics 21(3) (SIGGRAPH 2002), 473 to 482"
    locator: the transitions whose blends cause footskate
  - book: isbn:9780124158429
    title: "Rick Parent, Computer Animation, Algorithms and Techniques, 3rd edition, Morgan Kaufmann, 2012"
    locator: the chapter on kinematic linkages (inverse kinematics)
---

Footskate cleanup removes the small sliding of feet that should stand still.
Blends, transitions, [retargeting](/motion-retargeting/) and filters all change the joint angles a little, and a small change at the hip or knee moves the foot on the floor; this is footskate.
The method takes the motion and a list of footplants, the frames at which each foot should be planted.
For each plant it chooses one target place for the foot; on each planted frame it moves the root as little as needed so that the targets are in reach, solves each planted leg with [two-bone inverse kinematics](/two-bone-inverse-kinematics/), and lets the bones stretch a little if a leg must be nearly straight.
Near the start and the end of each plant the changes blend smoothly to zero, so that the motion has no jump.
Kovar, Schreiner and Gleicher (2002) presented the method; the code here is a planar version with its own choices, listed below.

## In plain words

A captured walk is changed, and now the feet slide a bit on the floor while they should stand still.
You mark the moments when each foot should be on the ground.
For each such moment, you pick one spot on the floor where that foot must stay.
Then, on each of those frames, you bend the hip and the knee so that the foot reaches its spot.
If the spot is a bit too far, you move the hips a little toward it, and as a last step you let the leg get a bit longer.
Just before and after the foot is down, you fade the changes in and out, so nobody sees a jump.

## The problem

The input is a motion of $f$ frames, a list of footplants (for each leg, runs of frames during which the foot must not move), the bone lengths $l_1$ (thigh) and $l_2$ (shin), an allowed stretch $\epsilon \ge 0$ and a blend length $b$.
In the planar code, a frame is the root (hip) position $h$ and, for each leg, the thigh angle $\varphi$ and the knee angle $\kappa$, with the ankle at $h + l_1 e(\varphi) + l_2 e(\varphi + \kappa)$ for $e(\varphi) = (\sin\varphi, -\cos\varphi)$.

The output is a motion in which:

- every planted ankle is at one fixed place for the whole plant;
- each bone length changes by a factor in $[1, 1 + \epsilon]$;
- a motion that has no footskate is not changed;
- frames far from every plant are not changed, and the change fades in and out smoothly.

Finding the footplants is a separate step, and here they are an input.
They can be marked by hand or found by a test on the height and speed of the foot.

## The algorithm

```pseudo id=main
FOOTSKATE-CLEANUP(frames, plants, l₁, l₂, ε, b)
    for each plant of a leg
L1      c ← the mean ankle position over the plant     ▷ the target, a choice of the code
    for each frame i with at least one planted leg
L2      ĥ ← the point nearest to the root h inside every disk of radius (1 + ε)(l₁ + l₂) around a target
        for each planted leg with target c
L3          s ← max(1, |ĥ - c| / (l₁ + l₂))             ▷ the stretch, at most 1 + ε
L4          (φ, κ) ← two-bone IK from ĥ to c with the bones s l₁ and s l₂, knee on the side of the input
    for each frame j
L5      w ← 1 - u²(3 - 2u) with u = δ / (b + 1), δ the distance to the nearest planted frame i
L6      root, angles and bone lengths of j ← input + w · (the change at frame i)
    return the new frames
```

Line L2 is a projection onto the intersection of one or two disks.
If the root is already in reach of every target, it does not move.
Otherwise the code compares the projection onto each disk and the intersection points of the two circles, and keeps the nearest point that is inside both disks.

Line L4 is the planar law of cosines solution: the angle at the hip between the thigh and the line to the target, and the inner angle at the knee.
Of the two mirror solutions it takes the one with the knee on the same side as in the input, so a knee never flips.
For a straight leg the code returns the straight pose directly, because the arc cosine near $-1$ loses precision.

**Choices of the code.**
The paper changes the root position and the joint orientations, uses analytic inverse kinematics, allows a small change of bone length when the leg is nearly straight, and blends the changes off when a constraint starts or ends.
The following details are the choices of this code, not taken from the paper: the mean ankle as the target, the root moved by the smallest distance, the same stretch factor for both bones of a leg, and the smoothstep weight of line L5.

## Example

The test builds a planar walk of 60 frames with the thigh $l_1 = 0.45$ and the shin $l_2 = 0.50$.
The root moves forward at 0.04 per frame at a height of about 0.85, and each foot is planted for 18 frames in each step of 30 frames, the right foot 15 frames after the left.
During a plant the ankle slides by 0.003 per frame plus a small noise, about 0.053 over the plant; the leg angles come from inverse kinematics on these sliding ankles.

The walk has three full plants: the left foot on frames 0 to 17 and 30 to 47, and the right foot on frames 15 to 32.
With $\epsilon = 0.05$, $b = 4$ and the noise seed 3, the planted ankle moves by at most $4 \cdot 10^{-16}$ in each plant after cleanup.
The root does not move and the bones do not stretch, because the hip is always in reach of the targets.

In a second walk at the height 0.94 with a larger slide (0.006 per frame) and the speed 0.05, the targets are farther away, and both bones of a leg stretch by up to 1.94 percent on some frames, inside the allowed 5 percent.

## Correctness

The proof file works under two assumptions: (A1) on every planted frame the disks of radius $(1 + \epsilon)(l_1 + l_2)$ around the planted targets meet, else the code raises an error; (A2) the new root is not too close to a target, so the target is not inside the inner limit $s |l_1 - l_2|$ of the leg.
Under them it shows:

- Line L2 returns the nearest point of the disk intersection, so the root moves as little as possible.
- The stretch factor of line L3 is in $[1, 1 + \epsilon]$, and the stretched leg reaches the target.
- The angles of line L4 put the ankle exactly on the target, so every planted ankle stays still during its plant (Theorem 1).
- Every bone length changes by a factor in $[1, 1 + \epsilon]$, the same for the thigh and the shin of a leg (Theorem 2).
- A motion whose planted ankles already stand still and are in reach, with bent knees, is returned unchanged (Theorem 3).
- A frame farther than $b$ from every planted frame is unchanged, and the weight goes from 1 to 0 with zero slope at both ends (Theorem 4).

That the result looks right is a visual heuristic.
The change of the root and the knees can be seen as a small dip or bounce, the stretch is a cheat on the skeleton, and the blend length $b$ and the stretch limit $\epsilon$ are tuning.

## Complexity

Lines L1 to L4 cost $O(1)$ per planted frame and leg, plus $O(f)$ in total for the means of line L1.
The code finds the nearest planted frame for each frame by a scan over all planted frames, which costs $O(f^2)$ in the worst case.
Two sweeps over the frames, one forward and one backward, give the nearest planted frame for every frame in $O(f)$, so the whole method can run in $O(f)$ time.
The extra space is $O(f)$ for the changes.
In 3D with a full skeleton, each frame also needs a forward kinematics pass over the joints, which is linear in the number of joints.

## Properties

- **Exact on plants.** The planted feet are on their targets, up to rounding.
- **Minimal root move.** The root moves only if a target is out of reach, and then as little as possible.
- **Bounded stretch.** No bone changes by more than the factor $1 + \epsilon$.
- **Local.** Only planted frames and frames within $b$ of them change.
- **Offline.** The targets need the whole plant, so the method runs on a finished clip.

## Variants and improvements

- **Toe and heel.** Plant the heel and the toe in turn with separate constraints, so the foot can roll.
- **Ground height.** Use the floor height under the target for uneven ground.
- **Online cleanup.** Games run a simpler version every frame: when a foot is planted, keep its last place and solve the leg with [two-bone inverse kinematics](/two-bone-inverse-kinematics/), with no look ahead.
- **Retargeting.** [Motion retargeting](/motion-retargeting/) to a skeleton with other bone lengths always needs a cleanup of this kind; spacetime methods solve the whole motion at once with the contacts as constraints.
- **Automatic plants.** Detect plants from the foot height and speed, or by a classifier trained on marked data.

## When to use it

Use footskate cleanup after every edit that changes the joint angles of a captured motion with contacts: blends, [motion graph](/motion-graph/) transitions, [motion warping](/motion-warping/), filtering and retargeting.
It is fast and changes only what it must.
It does not fix contacts that the edit removed, and it does not keep the balance of the character; for a body that must stay balanced, use a physics based method.

## Pitfalls

- **Wrong plants.** A plant marked too long holds a foot that should lift, and the leg stretches or the root drops.
- **Root steps.** Moving the root only on planted frames can make the root move unevenly; blend the root change over a few frames, and keep $b$ large enough.
- **Knee flips.** The inverse kinematics has two solutions. Without the side test of line L4, a knee can bend backward for one frame.
- **Straight legs.** Near full extension the knee angle is badly conditioned, and small target changes give large knee changes; the stretch limit helps.
- **Feet too far apart.** If two planted feet are farther apart than two stretched legs, no root position works, and the code raises an error.

## Implementations

## History

Lucas Kovar, John Schreiner and Michael Gleicher presented footskate cleanup at the ACM SIGGRAPH/Eurographics Symposium on Computer Animation in 2002, the same year as their [motion graphs](/motion-graph/), whose transitions make the problem common.
Earlier editing methods kept contacts with general constraint solvers, such as per frame inverse kinematics or spacetime optimization; the new step was a fast analytic method that only changes what it must.

## References
