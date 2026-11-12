---
title: What DENCLUE guarantees about its attractors, its noise and its clusters
proves: [correctness]
status: full
---

DENCLUE is a heuristic. It has no guarantee that it finds all modes of the density or the true basins of attraction. This proof states what the pseudocode of the page does guarantee.

Let $x_1, \ldots, x_n \in \mathbb{R}^d$ be the data, $\sigma > 0$, $\delta > 0$ and $\xi \ge 0$. The density is

$$f(x) = \sum_{i=1}^n \exp\!\Big(-\frac{\lVert x - x_i \rVert^2}{2 \sigma^2}\Big),$$

the sum of the Gaussian influence functions of the data points, as in Hinneburg and Keim (1998), without a normalizing constant. So $\xi$ is in the units of this sum: a point alone, far from the others, has density about 1 at its own position.

**Lemma 1 (the direction of a step).** The vector $g(x) = \sum_i (x_i - x) \exp(-\lVert x - x_i \rVert^2 / (2\sigma^2))$ of line L4 equals $\sigma^2 \nabla f(x)$. So line L6 moves a distance $\delta$ along the direction of steepest ascent of $f$.

*Proof.* Differentiate each term: $\nabla \exp(-\lVert x - x_i \rVert^2 / (2\sigma^2)) = \exp(\ldots) \cdot (x_i - x) / \sigma^2$. $\square$

**Lemma 2 (each climb rises and stops at a local top at scale $\delta$).** Let $y_0 = x_j, y_1, \ldots, y_K$ be the points accepted by line L8 in one climb, and $x^* = y_K$ its end. Then $f(y_0) \le f(y_1) \le \cdots \le f(y_K)$, each move has length exactly $\delta$, and either $\nabla f(x^*) = 0$ or $f(x^* + \delta u) < f(x^*)$ for the unit gradient direction $u$ at $x^*$.

*Proof.* Line L7 rejects a step that lowers $f$, and a rejected step ends the climb, so every accepted step does not lower $f$. Line L6 adds $\delta$ times a unit vector. The climb ends at line L5 when the gradient is 0, or at line L7 when the next step would lower $f$, which is the stated condition. This is the stopping rule of Hinneburg and Keim: the climb stops at step $k$ when $f(x^{k+1}) < f(x^k)$, and $x^k$ is the density attractor. $\square$

**Lemma 3 (in one dimension the end is within $\delta$ of a mode).** Let $d = 1$, and suppose the climb ends at line L7 at $x^*$ with $f'(x^*) > 0$, and let $m$ be the first stationary point of $f$ to the right of $x^*$. Then $m$ is a local maximum and $m - x^* < \delta$. The case $f'(x^*) < 0$ is the mirror image.

*Proof.* $f'$ is positive on $[x^*, m)$, so $f$ increases there, and $m$ is a local maximum. If $m \ge x^* + \delta$, then $f(x^* + \delta) > f(x^*)$, so line L7 would not stop the climb. $\square$

In more dimensions the end of a climb is a point where one more step of length $\delta$ along the gradient lowers the density. For a small $\delta$ this is close to a local maximum, but a step can also jump across a valley to another hill, and a climb can stop near a saddle. These are the reasons the method is a heuristic.

**Termination.** Each accepted step does not lower $f$, and $f \le n$. The paper gives no bound on the number of steps, and in exact arithmetic a climb could move along a level set of $f$. The implementation caps the number of steps, so it always ends. With the DENCLUE 2.0 step $x \leftarrow \sum_i w_i x_i / \sum_i w_i$, which is the Gaussian mean shift step, the density does not decrease and the gain at each step is at least a positive constant times the squared length of the step; the proof is on the page on [mean shift](/mean-shift/). So the steps tend to 0, the relative gain tends to 0, and the stopping test of Hinneburg and Gabriel (2007) is met after finitely many steps.

**Theorem (the labels).** Let the ends of the climbs be grouped by line L10, where an end joins the first earlier group whose representative is within the merge distance. Then:

1. A point gets NOISE if and only if the density at the end of its own climb is below $\xi$. This is the outlier rule of the paper: a point attracted to an attractor $x^*$ with $f(x^*) < \xi$ is an outlier.
2. With center-defined clusters, two points that are not noise have the same label if and only if their ends are in the same group.
3. With arbitrary-shape clusters, two points that are not noise have the same label if and only if their groups are joined by a chain of groups in which each two consecutive representatives pass the segment test of line L11: the density is at least $\xi$ at each of the $s + 1$ equally spaced points of the straight segment between them.

*Proof.* Line L12 gives NOISE exactly in the case of part 1, and otherwise the name of the union-find set of the group. Without line L11 each group is its own set, which gives part 2. Line L11 joins the sets of two groups whose representatives pass the test, and union-find keeps exactly the connected components of the graph of these edges, which gives part 3. $\square$

**Relation to the definition of the paper.** Hinneburg and Keim call a set of points an arbitrary-shape cluster if its attractors have density at least $\xi$ and each two of them are joined by a path on which the density is at least $\xi$. A segment that passes the test is such a path, up to the sampling of $s + 1$ points. So each cluster of part 3 meets the definition when the samples are dense enough. The converse fails: two attractors joined only by a curved path of high density are not joined by the test. The segment test is therefore sufficient, not necessary. Other tests of the path condition, for example through chains of data points of high density, find more paths, and they are heuristics as well.

**Cost.** Each evaluation of $f$ or of $g$ costs $\Theta(n d)$. With at most $T$ steps for each climb, the climbs take $O(T n^2 d)$ time. Line L10 compares each end with at most $m$ representatives, where $m$ is the number of groups. Line L11 makes $O(m^2)$ segment tests of $s + 1$ evaluations each, $O(m^2 s n d)$ time.
