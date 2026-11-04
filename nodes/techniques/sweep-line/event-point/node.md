---
tag: 4966MT
kind: concept
slug: event-point
name: Event point
aliases:
- event
area: techniques/sweep-line
level: intro
summary: A position (such as an endpoint or intersection) where the sweep must stop and update the status structure.
prereqs: [sweep-line-technique]
see_also: [event-queue, sweep-status-structure, sweep-invariant, degeneracy-in-sweeps, bentley-ottmann-algorithm, fortunes-algorithm, event-driven-simulation]
sources:
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition
    locator: Chapter 2, Section 2.1 (event points of the segment intersection sweep, and the lemma that two segments that meet are adjacent on the sweep line before their intersection point); Chapter 7 (site events and circle events of Fortune's sweep)
  - paper: "J. L. Bentley and T. A. Ottmann, Algorithms for reporting and counting geometric intersections, IEEE Transactions on Computers C-28(9) (1979), doi:10.1109/TC.1979.1675432"
    locator: pages 643 to 647 (intersection points as events found during the sweep)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 33.2, Determining whether any pair of segments intersects (the endpoints as event points)
---

An event point is a position of the sweep line where the [status structure](/sweep-status-structure/) of a [sweep](/sweep-line-technique/) changes combinatorially: an object starts or stops crossing the line, or two objects change their order along it. A sweep stops only at event points, because between two consecutive event points the set of crossed objects and their order stay the same. Events are *static* when they come from the input, such as endpoints, and *dynamic* when the sweep finds them on the way, such as the crossings of [Bentley-Ottmann](/bentley-ottmann-algorithm/) and the circle events of [Fortune's algorithm](/fortunes-algorithm/). The [event queue](/event-queue/) holds them in sweep order.

## In plain words

Slide a ruler across a drawing of line segments and write down, at each moment, which segments the ruler cuts and in which order. Most of the time, moving the ruler a little does not change this list. The list changes only where a segment begins, where a segment ends, or where two segments cross. These places are the events, and they are the only places where the program has to do work.

Some events are known before you start: the ends of the segments are part of the input. Others are not: you do not know where two segments cross until you compute it. A sweep finds these as it goes, by looking at segments that are next to each other in the list, and adds them to its list of places to stop.

## The idea

Let $S$ be a set of objects in the plane and let $\ell_x$ be the vertical line at position $x$. The *combinatorial state* at $x$ is the set $A(x)$ of objects that meet $\ell_x$ together with their order along $\ell_x$. A position $x$ is an **event point** if the state is not constant on any open interval that contains $x$. An algorithm may also stop at extra positions, such as query positions in an offline sweep, or circle events that turn out to be false; these are events of the algorithm, though not changes of the state.

With ties between events at the same $x$ broken by a fixed rule, each event becomes a point of the plane with a distinct key. For a segment sweep the usual rule is the lexicographic order: $(x_1, y_1)$ comes before $(x_2, y_2)$ when $x_1 < x_2$, or $x_1 = x_2$ and $y_1 < y_2$. See [degeneracy in sweeps](/degeneracy-in-sweeps/).

### Nothing changes between two events

**Lemma 1.** Let $S$ be a set of non-vertical segments, and let $I$ be an open interval of $x$-values that contains no $x$-coordinate of an endpoint and no $x$-coordinate of an intersection point. Then $A(x)$ and the order of $A(x)$ along $\ell_x$ are the same for all $x \in I$.

*Proof.* A segment with endpoints at $x = a$ and $x = b$, $a < b$, meets $\ell_x$ exactly for $x \in [a, b]$. Neither $a$ nor $b$ is in $I$, so each segment meets $\ell_x$ for all $x \in I$ or for none. So $A(x)$ is constant on $I$. Take two segments $s, t \in A(x)$ and let $f(x) = y_s(x) - y_t(x)$ on $I$. It is a linear function, so it is continuous. A zero of $f$ in $I$ is an intersection point of $s$ and $t$ with $x$ in $I$, and there is none. By the intermediate value theorem, $f$ has a constant sign on $I$, so $s$ and $t$ keep their order. $\blacksquare$

The sweep therefore needs no work strictly between consecutive events. This is the step "nothing changes between $x$ and $x'$" in the proof of the [sweep invariant](/sweep-invariant/).

### Dynamic events are found by neighbors

The crossings are not known in advance, so the sweep must find each one before the line reaches it. The next lemma says where to look.

**Lemma 2.** Let $p$ be an intersection point of two or more non-vertical segments, at $x = z$, and suppose $p$ is an interior point of at least two of them. Let $x^-$ be a position less than $z$ such that no event has its $x$-coordinate in $[x^-, z)$. Then the segments that pass through $p$ and meet $\ell_{x^-}$ form a contiguous block of at least two segments in the order along $\ell_{x^-}$. In particular, two of them are neighbors in that order.

*Proof.* A segment that has $p$ as an interior point has its left endpoint at $x < z$, so it meets $\ell_{x^-}$ by the choice of $x^-$. So at least two segments through $p$ meet $\ell_{x^-}$. Let $s$ and $t$ be two of them with $y_s(x^-) < y_t(x^-)$, and let $u$ be a segment with $y_s(x^-) < y_u(x^-) < y_t(x^-)$. If $u$ does not pass through $p$, then $u$ meets $\ell_z$ at a point other than $p$, or not at all; it cannot end in $[x^-, z)$, so it meets $\ell_z$ at a point $q \ne p$. If $q$ is above $p$, then $y_u(x^-) - y_t(x^-) < 0$ and $y_u(z) - y_t(z) > 0$, so by the intermediate value theorem $u$ and $t$ cross at some $x$ in the open interval $(x^-, z)$. If $q$ is below $p$, then $u$ crosses $s$ there in the same way. Both contradict the choice of $x^-$. So every segment between $s$ and $t$ passes through $p$. $\blacksquare$

So if the sweep tests each new pair of neighbors and puts their crossing into the queue, every crossing is in the queue before the line reaches it.

### Static and dynamic events

- **Static events** are known before the sweep: segment endpoints, rectangle edges, polygon vertices, the sites of a Voronoi diagram, query positions. A sweep with only static events sorts them once and reads them from an array.
- **Dynamic events** are computed during the sweep from the status: the crossing of two neighbors in Bentley-Ottmann, the circle event of three consecutive arcs of the beach line in Fortune's algorithm, the next collision of two particles in an [event-driven simulation](/event-driven-simulation/). A sweep with dynamic events needs a [priority queue](/priority-queue/), because new events arrive in the middle of the sweep, but always at keys greater than the current one.
- **Invalid events.** A dynamic event can stop being true before the line reaches it. In Fortune's algorithm a circle event is a *false alarm* when one of its three arcs disappears or is split before the event. In a simulation a predicted collision is cancelled when one of the particles collides with a third one first. The algorithm either deletes the event from the queue, which needs a handle into the queue such as an [indexed priority queue](/indexed-priority-queue/), or marks it and skips it when it comes out.

### How many events

For $n$ input objects:

| sweep | static events | dynamic events | total |
|---|---|---|---|
| [union length or maximum overlap of intervals](/sweep-union-length/) | $2n$ endpoints | none | $2n$ |
| [closest pair](/closest-pair-sweep-line/) | $n$ points | none | $n$ (points leave the window through a second pointer) |
| [Shamos-Hoey](/shamos-hoey-algorithm/) | $2n$ endpoints | none | at most $2n$ (it stops at the first crossing) |
| [rectangle intersection](/rectangle-intersection-sweep/), [rectangle union](/rectangle-union-sweep/), [skyline](/skyline-sweep/) | $2n$ vertical edges | none | $2n$ |
| [monotone partition](/monotone-polygon-partition/) | $n$ vertices | none | $n$ |
| [Bentley-Ottmann](/bentley-ottmann-algorithm/) | $2n$ endpoints | $k$ crossing points | at most $2n + k$ |
| [Fortune](/fortunes-algorithm/) | $n$ sites | the circle events that are processed, one for each [Voronoi](/voronoi-diagram/) vertex in general position, at most $2n - 5$ for $n \ge 3$ | $O(n)$ |
| [rotational sweep](/rotational-sweep/) | $2n$ endpoints, by angle | none | $2n$ |

In Bentley-Ottmann, $k$ counts distinct crossing points, not crossing pairs: three segments through one point give 3 pairs but 1 event. Events at a common point are also merged, so the total can be less than $2n + k$. Since $k \le \binom{n}{2}$, the sweep runs in $O((n + k) \log n)$ time, which is better than the $\Theta(n^2)$ test of all pairs when $k = o(n^2 / \log n)$. In Fortune's algorithm the false alarms are also inserted into the queue, but each site or circle event creates at most a constant number of them, so the queue sees $O(n)$ events in total.

## Examples

### Four segments: static and dynamic events

Take the segments $s_1$ from $(0, 0)$ to $(10, 6)$, $s_2$ from $(0, 6)$ to $(10, 0)$, $s_3$ from $(2, 1)$ to $(9, 5)$ and $s_4$ from $(4, 7)$ to $(7, 2)$.

The 8 static events in lexicographic order are $(0, 0)$ start $s_1$, $(0, 6)$ start $s_2$, $(2, 1)$ start $s_3$, $(4, 7)$ start $s_4$, $(7, 2)$ end $s_4$, $(9, 5)$ end $s_3$, $(10, 0)$ end $s_2$ and $(10, 6)$ end $s_1$. The two events at $x = 0$ and the two at $x = 10$ are ordered by $y$.

Of the 6 pairs, 4 cross, so there are 4 dynamic events:

$$s_1 \cap s_2 = (5, 3), \quad s_2 \cap s_3 = \left(\tfrac{215}{41}, \tfrac{117}{41}\right) \approx (5.244, 2.854),$$

$$s_1 \cap s_4 = \left(\tfrac{205}{34}, \tfrac{123}{34}\right) \approx (6.029, 3.618), \quad s_3 \cap s_4 = \left(\tfrac{290}{47}, \tfrac{159}{47}\right) \approx (6.170, 3.383).$$

The pairs $s_1, s_3$ and $s_2, s_4$ do not meet. The sweep processes $8 + 4 = 12$ events at 10 distinct $x$-values. Between consecutive $x$-values the order along the line is constant (Lemma 1). The table gives it from bottom to top, measured at the midpoint of each open interval, and the event at the right end that changes it.

| open interval of $x$ | order, bottom to top | event at the right end |
|---|---|---|
| $(0, 2)$ | $s_1, s_2$ | start $s_3$ |
| $(2, 4)$ | $s_3, s_1, s_2$ | start $s_4$ |
| $(4, 5)$ | $s_3, s_1, s_2, s_4$ | crossing $s_1 \cap s_2$ |
| $(5, 5.244)$ | $s_3, s_2, s_1, s_4$ | crossing $s_2 \cap s_3$ |
| $(5.244, 6.029)$ | $s_2, s_3, s_1, s_4$ | crossing $s_1 \cap s_4$ |
| $(6.029, 6.170)$ | $s_2, s_3, s_4, s_1$ | crossing $s_3 \cap s_4$ |
| $(6.170, 7)$ | $s_2, s_4, s_3, s_1$ | end $s_4$ |
| $(7, 9)$ | $s_2, s_3, s_1$ | end $s_3$ |
| $(9, 10)$ | $s_2, s_1$ | end $s_2$ and end $s_1$ |

Each crossing swaps two segments that are neighbors in the row above it, as Lemma 2 says. The crossing $s_1 \cap s_2$ is found at $x = 0$, when $s_2$ is inserted next to $s_1$. The crossings $s_2 \cap s_3$ and $s_1 \cap s_4$ are found at $x = 5$, when the swap of $s_1$ and $s_2$ makes $s_3, s_2$ and $s_1, s_4$ new neighbor pairs. The crossing $s_3 \cap s_4$ is found at $x = 205/34$, when the swap of $s_1$ and $s_4$ makes $s_3$ and $s_4$ neighbors.

### Intervals: the same position, several events

For the closed intervals $[1, 3]$ and $[3, 5]$, the position $x = 3$ carries two events, the end of $[1, 3]$ and the start of $[3, 5]$. The state changes there: just left of 3 the line meets one interval, at 3 it meets two, and just right of 3 it meets one. The order in which the sweep handles the two events decides whether it ever sees the count 2; the [degeneracy](/degeneracy-in-sweeps/) page treats this.

## Where it is used

Every [sweep line](/sweep-line-technique/) algorithm is driven by its events, kept in an [event queue](/event-queue/). The [Bentley-Ottmann algorithm](/bentley-ottmann-algorithm/) and [Fortune's algorithm](/fortunes-algorithm/) are the standard examples of dynamic events. The [rotational sweep](/rotational-sweep/) uses events ordered by angle. An [event-driven simulation](/event-driven-simulation/) uses events in time, mostly dynamic, with many invalid ones, and a [time-driven simulation](/time-driven-simulation/) is the alternative that steps at fixed times instead of at events. Lemma 1 is the reason the [sweep invariant](/sweep-invariant/) can be checked only at events.

## References
