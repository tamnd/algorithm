---
tag: 2DMA1Q
kind: algorithm
slug: registration-curves
name: Registration curves
aliases:
- motion registration curves
area: graphics-and-signals/character-animation
level: advanced
summary: "Align motions for blending by a timewarp, a coordinate frame alignment and constraint matches, computed from a dynamic time warping of frame distances."
model: real-ram
complexity:
  vars: {n: the frames of the first motion, m: the frames of the second motion, j: the number of joints, L: the slope limit}
  time: {distances: O(n m j), time_warp: O(n m L), alignment: O((n + m) j)}
  space: {grid: O(n m L)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2003
  people: [Lucas Kovar, Michael Gleicher]
  note: "Kovar and Gleicher presented registration curves at the Symposium on Computer Animation in 2003, building on the frame distance of their motion graphs."
prereqs: [motion-blending, motion-graph]
see_also: [dynamic-time-warping, verbs-and-adverbs, motion-signal-processing, footskate-cleanup, kabsch-algorithm, motion-matching]
sources:
  - paper: doi:10.2312/SCA03/214-224
    title: "Lucas Kovar and Michael Gleicher, Flexible automatic motion blending with registration curves, ACM SIGGRAPH/Eurographics Symposium on Computer Animation, 2003, 214 to 224"
    locator: "the timewarp from dynamic time warping with a slope limit, the alignment curve, the constraint matches, and the blend that uses them"
  - paper: doi:10.1145/566654.566605
    title: "Lucas Kovar, Michael Gleicher and Frederic Pighin, Motion graphs, ACM Transactions on Graphics 21(3) (SIGGRAPH 2002), 473 to 482"
    locator: the point cloud frame distance with the closed form 2D alignment
  - paper: doi:10.1145/218380.218421
    title: "Armin Bruderlin and Lance Williams, Motion signal processing, SIGGRAPH 95, 1995, 97 to 104"
    locator: the timewarping of motions by dynamic programming before a blend
---

A registration curve is the data that makes a [blend](/motion-blending/) of two or more motions work without manual setup.
It has three parts.
The timewarp says which frames of the motions belong together; it is a monotone path through the grid of frame pairs, found by [dynamic time warping](/dynamic-time-warping/) of a frame distance.
The alignment curve gives, for each pair on that path, the rotation about the vertical axis and the ground translation that best place one frame onto the other.
The constraint matches pair the foot plants of the motions, so that the blend knows when each foot of the result is planted.
Kovar and Gleicher (2003) built these from the point cloud distance of [motion graphs](/motion-graph/); with them, motions that differ in speed, heading and timing blend without feet that slide or cross.

## In plain words

Two people walk the same way, but one is slower and one walks along a curve.
You want to mix their walks.
First you find, for each moment of one walk, the moment of the other walk where the person stands most alike; this list of matches never goes back in time.
Then, for each match, you find how to turn and move the second person on the floor so that the two overlap best.
You also note when each foot of each person touches the ground.
With these three lists, you can mix the two walks in any ratio, and the feet still stand where they should.

## The problem

The input is two motions $A$ with $n$ frames and $B$ with $m$ frames, each frame a point cloud of the $j$ joint positions with $y$ up, and a slope limit $L \ge 1$.
The frame distance is the point cloud distance of the [motion graph](/motion-graph/) page, after the best rigid 2D move of $B_j$ onto $A_i$:

$$D_{ij} = \min_{\theta, x_0, z_0} \frac{1}{j} \sum_{\text{joints}} |p - T_{\theta, x_0, z_0}(q)|^2 .$$

An admissible path is a sequence of cells from $(0, 0)$ to $(n - 1, m - 1)$, each step $(1, 1)$, $(1, 0)$ or $(0, 1)$, with at most $L$ steps of the same non-diagonal kind in a row.
The timewarp is the admissible path with the smallest sum of $D$ over its cells.
The alignment curve is the 2D transform for each cell of the path, with the angle unwrapped so that it changes continuously.

The slope limit keeps the path from staying on one frame of a motion for long, which would freeze one of the motions in the blend.
Over any $L + 1$ steps, both motions advance.

## The algorithm

```pseudo id=main
REGISTER(A, B, L)
    D[i][j] ← frame distance of Aᵢ and Bⱼ for all i, j  ▷ the closed form 2D alignment
L1  best[(0, 0, diagonal, 0)] ← D[0][0]                ▷ state: cell, last step kind, run length
L2  for each state (i, j, s, r) in order of i, then j
L3      for each step k in (1, 1), (1, 0), (0, 1)
            r' ← 0 if k is diagonal, r + 1 if k = s, else 1
L4          if r' > L then skip the step              ▷ the slope limit
L5          relax best[(i, j) + k, k, r'] with best[(i, j, s, r)] + D at the new cell
L6  end ← the cheapest state at the cell (n - 1, m - 1)
L7  path ← the cells of the predecessors of end, from (0, 0)
L8  for each (i, j) on path: θ, x₀, z₀ ← best move of Bⱼ onto Aᵢ, θ unwrapped along the path
    return path and the alignment curve
```

The state carries the kind of the last step and how many of that kind came in a row, so the slope limit becomes a condition on single steps (line L4).
Every step increases $i + j$, so the states form a directed acyclic graph and one pass in order of $i$ and $j$ relaxes each state after all its predecessors.

To blend with weight $w$ on $A$, walk the path.
At the cell $(i, j)$ the blended frame is $w A_i + (1 - w)\, T_{ij}(B_j)$, and its time is $w i + (1 - w) j$.
The code blends point clouds to keep the example small; a real system blends joint rotations with [slerp](/spherical-linear-interpolation/) and the root by the alignment curve, and resamples the blended times at a fixed frame rate.

The paper adds two steps that the code leaves out.
It fits a smooth, strictly increasing curve to the path, so that the timewarp has no stairs.
It also finds the constraint matches: the foot plants of the motions that overlap in the timewarp are paired, and the blend plants a foot where the matched plants say so, with a start and end time blended from theirs.

## Example

**By hand.**
Let $D = \begin{pmatrix} 0 & 1 & 4 \\ 3 & 2 & 0 \end{pmatrix}$, $n = 2$, $m = 3$ and $L = 1$.
The admissible paths from $(0, 0)$ to $(1, 2)$ are $(0,0), (0,1), (1,2)$ with cost $0 + 1 + 0 = 1$; $(0,0), (1,1), (1,2)$ with cost 2; and $(0,0), (0,1), (1,1), (1,2)$ with cost 3.
The paths $(0,0), (0,1), (0,2), (1,2)$ and $(0,0), (1,0), (1,1), (1,2)$ have two steps along $j$ in a row and are not admissible for $L = 1$.
The algorithm returns the first path, with cost 1.

The slope limit can change the answer.
For $D = \begin{pmatrix} 0 & 0 & 0 & 5 \\ 5 & 5 & 5 & 0 \end{pmatrix}$, the path $(0,0), (0,1), (0,2), (1,3)$ has cost 0 but two steps along $j$ in a row.
With $L = 2$ it is the answer.
With $L = 1$ the answer is $(0,0), (0,1), (1,2), (1,3)$, with cost 5.

**A slower copy.**
The test makes a walk $A$ with one cycle in 30 frames (31 frames) and the same walk $B$ at two thirds of the speed, one cycle in 45 frames (46 frames).
With $L = 2$, the path stays within 1.5 frames of the line $j = 1.5 i$, the true time relation.

**A rigid move.**
If $B$ is $A$ turned by $2.5$ rad and moved by $(1, -2)$ on the floor, the path is the diagonal, every alignment is the inverse move, and the blend at $w = 0.5$ is $A$ itself.

## Correctness

The proof file shows the following facts, in exact arithmetic.

- Admissible paths are exactly the walks of the state graph from the start state to a state at $(n - 1, m - 1)$, with the same costs.
- The state graph is acyclic, and the order of line L2 handles every state after its predecessors.
- So line L6 finds the smallest cost of an admissible path, line L7 returns such a path, and the code raises an error exactly when no admissible path exists (Theorem 1).
- The path is monotone, and every $L + 1$ steps advance both motions (Theorem 2).
- For a fixed weight, the blended times never decrease along the path (Theorem 3), so the blend never plays backward.
- A rigid copy is recovered exactly (Theorem 4).

The proof does not show that the blend looks good.
The frame distance is a visual heuristic, the slope limit is tuning, and the method assumes that the motions are similar enough in structure to be blended at all, for example with the same sequence of foot contacts.

## Complexity

The distance grid has $n m$ cells and each costs $O(j)$, so it costs $O(n m j)$ time.
The dynamic program has $3 (L + 1)$ states per cell and three steps per state, so it costs $O(n m L)$ time and space.
The alignment curve costs $O(j)$ per cell of the path, and the path has at most $n + m - 1$ cells.
Two clips of 300 frames each, 10 seconds at 30 frames per second, have $9 \cdot 10^4$ cells.
With more than two motions, registering each one to a single reference motion makes the cost grow linearly in the number of motions.

## Properties

- **Exact.** The time warp is an optimal admissible path for the given distance.
- **Monotone.** The path never goes back in either motion, and both motions advance within $L + 1$ steps.
- **Invariant to the ground frame.** The frame distance and the alignment do not change when a motion is turned about the vertical axis or moved on the floor.
- **Offline.** The whole of both motions is needed before the first frame of the blend.

## Variants and improvements

- **Smooth timewarps.** Fit a strictly increasing smooth curve to the path, so that the blended speed has no steps.
- **Many motions.** Register every motion to one reference motion; a point in the timewarp of the reference then gives a frame of every motion, and weights from [verbs and adverbs](/verbs-and-adverbs/) or user input blend them.
- **Transitions.** A transition from one motion to another is a registration over a short window, with a weight that goes from 1 to 0.
- **Plain DTW.** Without the slope limit and the alignment, this is classic [dynamic time warping](/dynamic-time-warping/), as used by [motion signal processing](/motion-signal-processing/) to align motions.
- **Rotation alignment.** A 3D best rotation, as in the [Kabsch algorithm](/kabsch-algorithm/), would also align tilt; for characters on a floor only the vertical axis is wanted.

## When to use it

Use registration curves when many motions of the same action must blend with weights that the user sets, for example walks at different speeds and turns, or reaches to different places.
The setup is automatic once the motions are cut to the same action.
If the motions have different contact sequences, such as a walk and a jump, no registration makes the blend work.

## Pitfalls

- **Unwrapped angles.** The best rotation is found with an arc tangent in $(-\pi, \pi]$. Without the unwrapping of line L8, a motion that turns past $\pi$ jumps by $2\pi$ in the alignment curve, and a blend of the angles spins the character.
- **Stairs.** A raw DTW path has stairs, where one motion waits on a frame. The slope limit bounds them, and a smooth fit removes them.
- **Ends.** The path must start and end at the first and last frames; if the clips start at different phases, cut them first or allow free ends.
- **Cost.** The grid is quadratic in the length. For long clips, restrict the path to a band around the diagonal.
- **Blending positions.** Blending point clouds, as in the code, shortens bones. Blend rotations in a real system.

## Implementations

## History

Lucas Kovar and Michael Gleicher introduced registration curves at the ACM SIGGRAPH/Eurographics Symposium on Computer Animation in 2003.
They used the frame distance of their [motion graphs](/motion-graph/) (2002) inside dynamic time warping, which Bruderlin and Williams had already used to align motions in 1995, and added the alignment curve and the constraint matches.
Dynamic time warping itself comes from speech recognition in the 1970s.

## References
