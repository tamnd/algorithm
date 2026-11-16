---
tag: N97VRM
kind: algorithm
slug: random-shortcut-path-smoothing
name: Random shortcut path smoothing
aliases:
- path shortcutting
area: robotics/trajectory-generation
level: core
summary: "Shortens a planned path by picking two random points on it and replacing the part between them by a straight segment if it is free."
solves: [trajectory-generation-problem]
model: real-ram
complexity:
  vars: {N: "the number of iterations", n: "the number of vertices of the input path", k: "the number of obstacles"}
  time: {worst: Θ(N (n + N + k))}
  space: {extra: Θ(n + N)}
properties: {deterministic: false, randomized: true, online: false, exact: false}
prereqs: [motion-planning, collision-detection]
see_also: [rapidly-exploring-random-tree, probabilistic-roadmap, rrt-connect, elastic-bands, chomp, visibility-graph, euclidean-shortest-path, online-trajectory-generation]
sources:
  - paper: doi:10.1177/0278364907079280
    title: "Roland Geraerts and Mark H. Overmars, Creating high-quality paths for motion planning, The International Journal of Robotics Research 26(8), 2007, 845-863"
    locator: "the whole paper (shortcut heuristics, including random shortcuts between points on the path, compared on test scenes)"
  - paper: doi:10.1109/ROBOT.2010.5509683
    title: "Kris Hauser and Victor Ng-Thow-Hing, Fast smoothing of manipulator trajectories using optimal bounded-acceleration shortcuts, IEEE International Conference on Robotics and Automation, 2010, 2493-2498"
    locator: "the whole paper (shortcuts made of time-optimal trajectories under velocity and acceleration bounds)"
  - book: isbn:9781107156302
    title: "Kevin M. Lynch and Frank C. Park, Modern Robotics, Mechanics, Planning, and Control, Cambridge University Press, 2017"
    locator: "Section 10.8 (smoothing)"
---

Random shortcut path smoothing takes a collision-free path, usually the jagged output of a sampling-based [motion planner](/motion-planning/) such as a [rapidly-exploring random tree](/rapidly-exploring-random-tree/) or a [probabilistic roadmap](/probabilistic-roadmap/), and makes it shorter. In each iteration it picks two random points on the current path. If the straight segment between them is free of obstacles, it replaces the part of the path between the two points by that segment. The path stays free, keeps its end points, and never gets longer; these are theorems. How close it gets to the shortest path is not guaranteed: in practice a few hundred iterations remove most of the detours, and the measurements below show this on one scene. The method is a heuristic, very simple to implement, and uses only the [collision checker](/collision-detection/) that the planner already has. It is the most common post-processing step for sampling-based planners.

## In plain words

A planner that finds paths by random search finds paths that wander: they zigzag and take detours, because the search was random. To clean such a path, pick two places on it at random. If you can walk straight from one to the other without hitting anything, do that, and drop the part of the path in between. Repeat many times. Each successful straight cut makes the path shorter, and a failed try changes nothing. After a few hundred tries the path is mostly straight lines that touch the corners of obstacles. It may still be the long way around an obstacle, because the method only cuts corners of the path it has.

## The problem

Input: a free polyline path $P = (x_0, \dots, x_n)$ from a start to a goal, a test for whether a straight segment is free, a number $N$ of iterations, and a random number generator. Output: a free polyline from $x_0$ to $x_n$ that is as short as possible. The code works in the plane with $k$ axis-aligned rectangular obstacles, whose open interiors are forbidden; a robot uses its own collision checker on the segment in configuration space instead.

## The algorithm

```pseudo id=main
SHORTCUT(P, obstacles, N, rng)
L1  repeat N times
L2      compute the cumulative lengths of the segments of P
L3      draw s1, s2 uniform in [0, length(P)] and sort them
L4      a ← the point at arc length s1, on segment i;  b ← the point at arc length s2, on segment j
        if i = j then continue                     ▷ same segment, nothing to gain
L5      if the segment ab is free then
L6          P ← (x0, ..., xi, a, b, x(j+1), ..., xn)
L7  return P
```

Line L3 picks the two points uniformly along the path, which is the choice that the measurements on this page use. Line L4 finds them by searching the cumulative lengths. Line L5 is the only call to the collision checker. In the code it is an exact slab test against each rectangle. Line L6 splices the shortcut into the path: the vertices strictly between $a$ and $b$ disappear, and $a$ and $b$ become vertices.

## Example

The scene has one wall, the rectangle $[4, 6] \times [-9, 8]$, and the path goes around it the long way: $(0, 0) \to (0, 9) \to (10, 9) \to (10, 0)$, of length 28. The shortest path goes over the top corners of the wall, $(0, 0) \to (4, 8) \to (6, 8) \to (10, 0)$, of length $2\sqrt{80} + 2 \approx 19.889$. With seed 1 the code measured:

| iterations | length | vertices |
|---|---|---|
| 0 | 28 | 4 |
| 10 | 26.367 | 6 |
| 30 | 22.202 | 11 |
| 100 | 20.481 | 12 |
| 300 | 20.304 | 15 |
| 1000 | 19.938 | 17 |

After 300 iterations the path is about 2.1 percent longer than the optimum; after 1000, about 0.25 percent. The number of vertices grows, since each shortcut adds two points and often removes only one. In a scene with no obstacles, a zigzag path from $(0, 0)$ to $(4, 0)$ shrank to length $4.0106$ after 200 iterations (seed 3): the last detours near the two end points shrink slowly, because a shortcut must start inside them. These are measurements on one scene each, not bounds.

## Correctness

Theorem: after any number of iterations, for every sequence of random choices, the result is a free path with the same end points as the input and a length at most the input length, with at most $n + 1 + N$ vertices. The [proof](proofs/correctness.md) shows that the slab test is exact, that the new segment is free by the test, that the two partial segments next to it are parts of old free segments, and that the new segment is at most as long as the part it replaces, by the triangle inequality. No claim is made about optimality: if the path goes around a wall on the far side and no free segment joins two of its points past the near side, the method can never switch to the other side.

## Complexity

In the [real RAM](/real-ram/), one iteration costs $\Theta(n')$ for the cumulative lengths, where $n'$ is the current number of vertices, and $\Theta(k)$ for the segment test against $k$ obstacles. The path gains at most one vertex per iteration, so $n' \le n + N$, and $N$ iterations cost $\Theta(N(n + N + k))$ in the worst case. With a real collision checker, the segment test dominates; it is usually a sequence of checks at a fine resolution along the segment, and its cost depends on the scene.

## Properties

- **Anytime.** Every intermediate path is free and no longer than the one before (a theorem), so the method can stop at any time.
- **Local.** It only cuts corners of the current path. It cannot change the homotopy class: a path that goes around the wrong side of an obstacle stays there.
- **Randomized.** The result depends on the seed. Fixed seeds give the same result, which the tests check.
- **Corners touch obstacles.** The result tends to touch obstacle corners, with no clearance. Many systems add a margin to the obstacles for this reason.
- **Geometric only.** The result is a path, not a trajectory; it has corners where the velocity must drop to zero, unless a time scaling with blends is added.

## Variants and improvements

- **Vertex shortcuts.** Try to join two random vertices of the path instead of two random points; this is simpler but leaves more corners. Geraerts and Overmars compare several such variants and report the trade-offs between length, clearance and time.
- **Partial shortcuts.** Shortcut only some of the coordinates of a configuration, which helps for arms with many joints where a full shortcut is rarely free (Geraerts and Overmars).
- **Trajectory shortcuts.** Hauser and Ng-Thow-Hing replace the straight segment by the time-optimal motion between the two states under velocity and acceleration bounds, the same profiles as in [online trajectory generation](/online-trajectory-generation/), so the result is a trajectory with no stops.
- **Deterministic shortcuts.** A greedy pass that joins each vertex to the farthest visible vertex gives a similar result without randomness.
- **Optimization.** [Elastic bands](/elastic-bands/) and [CHOMP](/chomp/) improve a path by gradient steps on a cost that includes clearance and smoothness.
- **Exact shortest path.** In the plane with polygonal obstacles, the [visibility graph](/visibility-graph/) gives the exact [Euclidean shortest path](/euclidean-shortest-path/), which the tests use as the reference.

## When to use it

Use random shortcutting after any sampling-based planner, as the default first post-processing step. It needs only the collision checker, and it never makes the path longer. As a rule of thumb, a few hundred iterations cost little compared with the planning itself. Follow it with a time scaling, such as a [trapezoidal profile](/trapezoidal-velocity-profile/) per segment with blends, or use the trajectory version of Hauser and Ng-Thow-Hing. Use an optimizer instead if clearance or smoothness matter more than length.

## Pitfalls

- **Collision checking by sampling.** A segment test that checks discrete points can miss thin obstacles. Use a resolution that matches the smallest obstacle, or an exact test.
- **Growing vertex count.** Each shortcut adds vertices. Remove collinear vertices and merge very short segments from time to time.
- **No clearance.** The shortest path grazes obstacles. A robot that tracks it with any error collides. Inflate the obstacles first.
- **Stopping too early.** Most of the gain comes in the first few dozen iterations, but long detours near the end points need many more. Check the length, not just the iteration count.
- **Same segment.** If both points fall on one segment, the shortcut is the segment itself; skip it, as the code does, or the path gains useless vertices.

## Implementations

## History

Shortcutting a path by joining points that can see each other is an old idea, used since the early sampling-based planners as their post-processing step. Geraerts and Overmars (2007) studied and compared shortcut heuristics systematically, including random shortcuts between points that are not vertices and partial shortcuts, together with methods that increase clearance. Hauser and Ng-Thow-Hing (2010) made the shortcuts dynamically feasible by using time-optimal bounded-acceleration trajectories. Lynch and Park (2017) discuss this kind of post-processing in their section on smoothing.

## References
