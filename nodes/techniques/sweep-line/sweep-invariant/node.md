---
tag: S9SGS5
kind: concept
slug: sweep-invariant
name: Sweep line invariant
aliases:
- sweep status invariant
area: techniques/sweep-line
level: intro
summary: At each event, the status structure holds exactly the objects currently crossed by the sweep line, in the correct order.
prereqs: [loop-invariant, sweep-line-technique, event-point]
see_also: [sweep-status-structure, event-queue, degeneracy-in-sweeps, bentley-ottmann-algorithm, shamos-hoey-algorithm, invariant]
sources:
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition
    locator: Chapter 2, Section 2.1, Line Segment Intersection (the invariant that all intersection points above the sweep line have been computed, and the proof that the sweep finds every intersection point)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 33.2, Determining whether any pair of segments intersects (the correctness proof of ANY-SEGMENTS-INTERSECT)
  - paper: "J. L. Bentley and T. A. Ottmann, Algorithms for reporting and counting geometric intersections, IEEE Transactions on Computers C-28(9) (1979), doi:10.1109/TC.1979.1675432"
    locator: pages 643 to 647
---

The sweep invariant is the [loop invariant](/loop-invariant/) of a [sweep line](/sweep-line-technique/) algorithm. Before each [event](/event-point/) is processed, the [status structure](/sweep-status-structure/) holds exactly the objects that cross the sweep line, in their order along it, every output item that lies to the left of the line has been reported, and the [event queue](/event-queue/) holds every event to the right that the next steps need. Proving that one pass of the main loop keeps these three facts is the whole correctness proof of a sweep.

## In plain words

A sweep moves a line across the drawing and stops at a list of places. At each stop, the program has a picture of the line in memory: which shapes the line cuts, and in which order from bottom to top. The invariant says that this picture is right, and that all the work for the part of the drawing behind the line is done.

If the picture is right at one stop and nothing happens until the next stop, then a correct update at the next stop makes the picture right again. When the line has passed all the shapes, the part behind the line is the whole drawing, so all the work is done. The proof also needs the list of stops to be complete: a change that the program does not know about would make the picture wrong without any warning.

## The idea

Take a set $S$ of objects in the plane, each meeting every vertical line in at most one connected piece, and a vertical line $\ell_x = \{(x, y) : y \in \mathbb{R}\}$ that moves from left to right. Assume a tie rule that gives all events distinct keys (see [degeneracy in sweeps](/degeneracy-in-sweeps/)). For a position $x$ define

$$A(x) = \{ s \in S : s \cap \ell_x \ne \emptyset \},$$

the *active* objects, and the order $<_x$ on $A(x)$ by the $y$-coordinate of $s \cap \ell_x$. For segments, $s <_x t$ means $y_s(x) < y_t(x)$.

Let $x$ be the key of the next event in the queue, and let $x^-$ be any position between the previous event key and $x$. The **sweep invariant** at the test of the main loop is the conjunction of three parts.

1. **Status.** The status $T$ holds exactly $A(x^-)$, ordered by $<_{x^-}$.
2. **Output.** Every output item whose key is less than $x$ has been reported, and no other item has been reported.
3. **Queue.** The queue $Q$ holds every static event whose key is at least $x$, and, for each pair of objects that are neighbors in $T$, the event where they next interact, if that event has key at least $x$.

For [segment intersection](/bentley-ottmann-algorithm/), part 2 is "every intersection point to the left of the line has been reported". De Berg et al. sweep a horizontal line from top to bottom and write it as "all intersection points above the sweep line have been computed correctly". Part 3 says that each pair of neighbors that cross to the right of the line has its crossing in $Q$.

**The invariant gives correctness.** It is a loop invariant for the loop `while Q is not empty` of the [template](/sweep-line-technique/).

- **Initialization.** Before the first event, $x$ is the smallest key. Every object starts at a static event, so no object crosses the line to the left of all events: $A(x^-) = \emptyset$ and $T$ is empty. No output item has a key less than the first start, so the empty output is right. $Q$ holds all static events and $T$ has no neighbors, so part 3 holds.
- **Maintenance.** Assume the invariant before the event at $x$. By part 3, all events with key $x$ are in $Q$, so the update at $x$ sees every object that starts, ends or crosses at $x$. Inserting the objects that start, deleting those that end and reversing the order of those that cross turns $T$ into $A(x^+)$ in the order $<_{x^+}$, where $x^+$ is a position just right of $x$. The report at $x$ adds the output items with key $x$. The pairs that are neighbors in $T$ after the update and were not neighbors before are exactly the pairs that the check tests, and the check adds their next interaction to $Q$; the other neighbor pairs already have theirs in $Q$. So part 3 holds for the new $T$. Let $x'$ be the smallest key now in $Q$. Suppose that the active set or the order changes at some $z$ with $x < z < x'$, and take the smallest such $z$. A start or an end at $z$ is a static event, so it is in $Q$, which contradicts $z < x'$. A crossing at $z$ is, by the [event point](/event-point/) lemma, a crossing of two objects that are neighbors in the order just left of $z$, which is the order of $T$; by part 3 its event is in $Q$, again a contradiction. So nothing changes between $x$ and $x'$, $T$ holds $A(x'^-)$ in order, and no output item has a key strictly between $x$ and $x'$. This is the invariant before the event at $x'$.
- **Termination.** The loop stops when $Q$ is empty. By part 3, no static event remains, so every object has ended and $T$ is empty. Part 2 with $x = +\infty$ says that every output item has been reported, and nothing else.

Termination of the loop itself needs a bound on the number of events: each static event is removed once, and each dynamic event (a crossing point) is inserted at most once if the check skips events already in $Q$. So the loop runs at most $2n + k$ times for $n$ segments with $k$ crossing points.

**A too weak invariant.** "The status holds the active objects", without the order, holds at every event. But it does not support the step that tests only neighbors: without the order there are no neighbors. The same holds for part 3. Without it, the maintenance step cannot show that the next event in $Q$ is the next change, and the proof fails.

## Examples

### Bentley-Ottmann on three segments

Take the segments $a$ from $(0, 0)$ to $(8, 4)$, $b$ from $(1, 5)$ to $(9, 1)$ and $c$ from $(3, 0)$ to $(7, 5)$. The pairs cross at

$$a \cap c = (5, 5/2), \quad b \cap c = (37/7, 20/7) \approx (5.286, 2.857), \quad a \cap b = (11/2, 11/4).$$

The table shows the state after each event. The status lists the segments from bottom to top. "Dynamic events in $Q$" are the crossings that are waiting.

| event | key $x$ | new neighbor pairs tested | status after | dynamic events in $Q$ after | reported |
|---|---|---|---|---|---|
| start $a$ | 0 | none | $a$ | none | |
| start $b$ | 1 | $(a, b)$: crossing at $x = 5.5$, added | $a, b$ | $a \cap b$ | |
| start $c$ | 3 | $(c, a)$: crossing at $x = 5$, added | $c, a, b$ | $a \cap c$, $a \cap b$ | |
| $a \cap c$ | 5 | $(c, b)$: crossing at $x = 37/7$, added | $a, c, b$ | $b \cap c$, $a \cap b$ | $(5, 5/2)$ |
| $b \cap c$ | 37/7 | $(a, b)$: already in $Q$ | $a, b, c$ | $a \cap b$ | $(37/7, 20/7)$ |
| $a \cap b$ | 11/2 | $(a, c)$: they crossed at $x = 5$, to the left, ignored | $b, a, c$ | none | $(11/2, 11/4)$ |
| end $c$ | 7 | none | $b, a$ | none | |
| end $a$ | 8 | none | $b$ | none | |
| end $b$ | 9 | none | empty | none | |

Check part 1 between events. At $x = 4$, between the keys 3 and 5, the $y$-values are $y_c = 1.25$, $y_a = 2$ and $y_b = 3.5$, which is the status $c, a, b$. At $x = 5.1$ they are $y_a = 2.55$, $y_c = 2.625$, $y_b = 2.95$, the status $a, c, b$. At $x = 5.4$ they are $y_a = 2.7$, $y_b = 2.8$, $y_c = 3$, the status $a, b, c$. At $x = 6$ they are $y_b = 2.5$, $y_a = 3$, $y_c = 3.75$, the status $b, a, c$.

Check part 3. At $x = 3$, $c$ is inserted below $a$, so $a$ and $b$ are no longer neighbors, but the crossing $a \cap b$ stays in $Q$. At $x = 37/7$ they are neighbors again, and the test finds the same crossing a second time. A variant that deletes the crossing of a pair when it stops being neighbors keeps $Q$ at $O(n)$ size; it must then insert the crossing again at $x = 37/7$. Both versions keep part 3, which is about the current neighbors only.

Check part 2. Before the event at $x = 37/7$, the reported set is $\{(5, 5/2)\}$, and it is exactly the set of crossings with $x < 37/7$.

### Maximum overlap of intervals

For closed intervals on a line, the status is a counter $c$ and the output is a running maximum $m$. At equal keys, starts come before ends. The invariant before each event is: $c$ is the number of intervals whose start has been processed and whose end has not, and $m$ is the largest value that $c$ has had. Under the tie rule, for every point $z$, the value of $c$ right after the last start at $z$ (or at a position just left of $z$, if no interval starts at $z$) equals the number of intervals that contain $z$, so at the end $m$ is the maximum overlap. With the intervals $[1, 3]$ and $[3, 5]$, after the start of $[3, 5]$ at $x = 3$ we have $c = 2$ and $m = 2$: both intervals contain the point 3. The [degeneracy](/degeneracy-in-sweeps/) page shows what goes wrong with the opposite tie rule.

### Shamos-Hoey

The [Shamos-Hoey](/shamos-hoey-algorithm/) detection sweep stops at the first crossing it finds, so its invariant is weaker in part 2: "no two segments cross to the left of the line". Its part 3 is replaced by a lemma: if two segments cross, the two segments of the leftmost crossing are neighbors in $T$ after some event before that crossing, so a neighbor test sees them. The proof in CLRS Section 33.2 has this form.

## Where it is used

Every sweep has an invariant of this shape. The [Bentley-Ottmann algorithm](/bentley-ottmann-algorithm/) and [Shamos-Hoey](/shamos-hoey-algorithm/) use it for segments, the [rectangle intersection sweep](/rectangle-intersection-sweep/) and the [rectangle union sweep](/rectangle-union-sweep/) for rectangles, the [skyline sweep](/skyline-sweep/) for buildings, and [Fortune's algorithm](/fortunes-algorithm/) for the beach line of a [Voronoi diagram](/voronoi-diagram/). In the [rotational sweep](/rotational-sweep/) the line is a ray and the order is by distance from the center. In an [event-driven simulation](/event-driven-simulation/) the same three parts appear in time: the state is right at the current time, the past is done, and the queue holds the next event of each pair that can interact.

## References
