---
tag: B88YSH
kind: concept
slug: degeneracy-in-sweeps
name: Degeneracy in sweep algorithms
aliases:
- degenerate cases in sweeps
- event tie-breaking
area: techniques/sweep-line
level: core
summary: Handling of vertical segments, coincident events and multiple events at one point by a fixed tie-breaking rule.
prereqs: [sweep-line-technique, event-point, general-position]
see_also: [sweep-invariant, event-queue, sweep-status-structure, orientation-test, bentley-ottmann-algorithm, skyline-sweep, rectangle-intersection-sweep, floating-point-arithmetic]
sources:
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition
    locator: Chapter 2, Section 2.1 (the event order by y and then by x, horizontal segments, and the handling of all segments through one event point together)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 33.2, Determining whether any pair of segments intersects (the assumptions that no segment is vertical and no three segments meet at one point, and the rule that left endpoints come before right endpoints at equal x)
  - paper: "H. Edelsbrunner and E. P. Mücke, Simulation of simplicity: a technique to cope with degenerate cases in geometric algorithms, ACM Transactions on Graphics 9(1) (1990), doi:10.1145/77635.77639"
    locator: pages 66 to 104
---

A degeneracy in a sweep is an input in which events or objects coincide in a way that the plain description of the sweep does not decide: several events with the same coordinate, a vertical segment, three or more segments through one point, collinear segments that overlap, or objects that only touch. A [sweep](/sweep-line-technique/) handles them with fixed rules: a total order on the [events](/event-point/) that breaks ties, a rule for the order of start and end events at the same coordinate, a single step for all segments through one point, or a symbolic perturbation of the input. The rules are part of the specification: they decide whether touching objects count as meeting, and a wrong rule gives a wrong answer, not only a slower one.

## In plain words

The textbook picture of a sweep has every interesting place at its own spot: no two segments begin at the same position, no three lines cross at one point, no segment stands straight up. Real input does not behave like that. Buildings stand side by side, rectangles share an edge, a grid of segments has many crossings on one vertical line.

At such a place, the sweep has several things to do at once, and the order matters. If one rectangle ends exactly where another begins, a program that removes the first before it adds the second never sees them together and reports that they do not touch. The fix is to decide, once and for all, which kind of event goes first, and to make this choice match the question: do touching shapes count as meeting or not?

## The idea

### The degenerate cases

For a left-to-right sweep over segments, the plain algorithm assumes [general position](/general-position/) in this form: all endpoints and crossing points have distinct $x$-coordinates, no segment is vertical, no three segments pass through one point, and no two segments overlap. CLRS Section 33.2 states the two middle assumptions for its segment sweep. Each one fails often in practice:

1. **Several events with the same $x$.** Two endpoints, or an endpoint and a crossing, on one vertical line.
2. **A vertical segment.** Both endpoints have the same $x$, so the segment is not a function of $x$ and the comparator $y_s(x)$ divides by zero.
3. **Several segments through one point.** One point is the crossing of $\binom{m}{2}$ pairs, and the order of all $m$ segments must reverse at once.
4. **An endpoint on another segment**, or two segments that share an endpoint.
5. **Overlapping collinear segments.** Their intersection is a segment, not a point, and the comparator ties on a whole interval.
6. **Touching objects.** Closed intervals or rectangles that share a boundary point, edge or corner.

### Rule 1: a total order on events, which is a tilted line

Order event points lexicographically: $(x_1, y_1)$ comes before $(x_2, y_2)$ when $x_1 < x_2$, or $x_1 = x_2$ and $y_1 < y_2$. Distinct points then have distinct keys, and this order is the order of a slightly tilted sweep line.

**Claim.** Let $P$ be a finite set of points. Let $\varepsilon > 0$ be smaller than $(x_j - x_i) / |y_i - y_j|$ for every pair with $x_i < x_j$ and $y_i \ne y_j$. Then $p_i$ comes before $p_j$ in the lexicographic order if and only if $x_i + \varepsilon y_i < x_j + \varepsilon y_j$.

*Proof.* If $x_i < x_j$ and $y_i \ne y_j$, then $\varepsilon (y_i - y_j) \le \varepsilon |y_i - y_j| < x_j - x_i$, so $x_i + \varepsilon y_i < x_j + \varepsilon y_j$. If $x_i < x_j$ and $y_i = y_j$ this is immediate. If $x_i = x_j$, the inequality reduces to $y_i < y_j$. These cases cover all pairs of distinct points, and both orders are total, so they agree. $\blacksquare$

So the lexicographic order is a sweep by the lines $x + \varepsilon y = c$, a line rotated by a tiny angle. On this line a vertical segment is no longer special: its lower endpoint is its start and its upper endpoint its end. De Berg et al. sweep a horizontal line downward and order events by decreasing $y$, then by increasing $x$; a horizontal segment then starts at its left endpoint. It is the same trick, rotated.

### Rule 2: handle all segments through one point in one step

With Rule 1, all events at one point $p$ form a single event. Following de Berg et al., let $U(p)$ be the segments that start at $p$, $L(p)$ those that end at $p$ and $C(p)$ those that contain $p$ in their interior. The step is: if $U(p) \cup L(p) \cup C(p)$ has two or more segments, report $p$ with all of them; delete $L(p) \cup C(p)$ from the status; insert $U(p) \cup C(p)$ in their order just right of $p$, which reverses $C(p)$; then test only the new outer pairs: the lowest segment of $U(p) \cup C(p)$ with its lower neighbor and the highest with its upper neighbor, or, if $U(p) \cup C(p)$ is empty, the two segments just below and just above $p$. Comparisons at $p$ tie, so the comparator breaks ties by slope, which is the order just to the right of $p$.

**Example.** Let $s_1$ go from $(0, 0)$ to $(4, 4)$, $s_2$ from $(0, 4)$ to $(4, 0)$ and $s_3$ from $(0, 2)$ to $(4, 2)$. All three pass through $p = (2, 2)$. At $x = 1$ the $y$-values are $1, 3, 2$, so the order from bottom to top is $s_1, s_3, s_2$. At $x = 3$ they are $3, 1, 2$, so the order is $s_2, s_3, s_1$, the reverse. A sweep that handles the crossing as one swap of the pair $(s_1, s_3)$ that it found first gets $s_3, s_1, s_2$, which is wrong at $x = 3$, and from then on it tests the wrong neighbors. The one-step rule reverses the block and reports one point that lies on three segments. The output size counts this as one point, while a list of crossing pairs has 3 pairs.

### Rule 3: starts and ends at the same coordinate

When an object ends at $x$ and another starts at $x$, the order of the two events decides whether the sweep ever has both in the status.

- **Starts before ends**: objects that touch at $x$ are active together. This matches *closed* objects.
- **Ends before starts**: they are never active together. This matches *open* objects, or half-open intervals $[a, b)$.

**Intervals.** For the closed intervals $[1, 3]$ and $[3, 5]$, the point 3 is in both, so the maximum overlap is 2. Starts before ends gives 2. Ends before starts gives 1, which is the right answer for the open intervals $(1, 3)$ and $(3, 5)$ and the wrong one here. The union length is 4 under both rules: between the events at $x = 3$ the line moves by 0, so a measure does not depend on the tie rule. Decisions about touching do.

**Segments sharing an endpoint.** Let $a$ go from $(0, 0)$ to $(2, 2)$ and $b$ from $(2, 2)$ to $(4, 0)$. They meet at $(2, 2)$. A sweep that sorts by $x$ only and puts the end of $a$ before the start of $b$ deletes $a$ before it inserts $b$, never tests the pair, and reports no intersection. CLRS puts all left endpoints with the same $x$ before all right endpoints with that $x$, so $b$ is inserted while $a$ is still there, and the neighbor test finds the common point. With Rule 1 and Rule 2, $(2, 2)$ is one event with $L(p) = \{a\}$ and $U(p) = \{b\}$, and it is reported directly.

**Rectangles.** Two closed rectangles that share a vertical edge must be active together at that $x$, so inserts come before deletes. The [rectangle intersection sweep](/rectangle-intersection-sweep/) page lists this as a pitfall: with the opposite order, two rectangles that share only a vertical edge are never active together, and the pair is missed.

**Skyline.** The [skyline sweep](/skyline-sweep/) keeps the heights of the active buildings and outputs a key point each time the maximum height changes. Take the buildings $(1, 4, 3)$, $(4, 6, 3)$ and $(4, 7, 2)$ as (left, right, height). The skyline is $(1, 3), (6, 2), (7, 0)$: the first two buildings form one flat roof of height 3 from 1 to 6. If the sweep handles the end at $x = 4$ before the two starts there, the lower start first, and outputs a point after each event, the maximum goes $3 \to 0 \to 2 \to 3$ and the output is $(1, 3), (4, 0), (4, 2), (4, 3), (6, 2), (7, 0)$, with three false key points at $x = 4$. The order among starts matters too. For $(0, 3, 2)$ and $(0, 3, 4)$, the lower start first gives $(0, 2), (0, 4), (3, 0)$ instead of $(0, 4), (3, 0)$. Among ends, for $(0, 3, 4)$ and $(1, 3, 2)$, the higher end first gives $(0, 4), (3, 2), (3, 0)$ instead of $(0, 4), (3, 0)$. Two rules fix all three cases:

- Sort by $x$; at equal $x$, starts before ends, starts by decreasing height, ends by increasing height.
- Or process all events with the same $x$ as one batch, and output at most one key point after the batch, if the maximum changed. This rule needs no order inside the batch and is the safer one.

### Rule 4: symbolic perturbation

Instead of writing a rule for each case, move the input by an infinitely small amount so that no degenerate case remains, and decide each test as it would be decided for the moved input. Simulation of simplicity, by Edelsbrunner and Mücke, replaces each coordinate $\pi_{i,j}$ (point $i$, coordinate $j$, in dimension $\delta$) by

$$\pi_{i,j} + \varepsilon^{2^{i \delta - j}}$$

for a positive infinitesimal $\varepsilon$. Each predicate is the sign of a polynomial in the coordinates, such as the determinant of an [orientation test](/orientation-test/). After the perturbation it is a polynomial in $\varepsilon$ that is not identically zero, and its sign is the sign of its lowest-order nonzero coefficient. When the unperturbed value is nonzero, that is the first coefficient, and the result is the usual one; only a degenerate test looks at the further coefficients. The program can then be written for general position.

The cost is in the output: it describes the perturbed input. Three segments through one point may come out as three crossings at the same coordinates, and a closed rectangle that touches another may come out as touching or not, depending on the perturbation. If the question is about touching, a fixed rule as in Rule 3 states the intent more directly.

### Overlapping segments and near-degeneracy

**Collinear overlap.** Let $a$ go from $(0, 0)$ to $(4, 0)$ and $b$ from $(2, 0)$ to $(6, 0)$. On the whole interval $2 \le x \le 4$ the comparator gives $y_a = y_b = 0$, so a tree ordered by $y$ alone sees two equal keys. Break ties by slope and then by an index, so that the order is total, and when two neighbors are collinear with overlapping $x$-ranges, report the common segment from $(2, 0)$ to $(4, 0)$ instead of a point.

**Near-degeneracy.** With floating-point coordinates, a degenerate input becomes an inconsistent one: an intersection point may be computed a little to the left of the line, or three tests on the same three segments may give answers that no real configuration has. Tie rules cannot fix this. Use exact arithmetic for the predicates, for example integer [orientation tests](/orientation-test/) and exact fractions for crossing points, and apply the rules above to the exact values. See [floating-point arithmetic](/floating-point-arithmetic/).

## Examples

The examples are in the rules above, with numbers. In summary:

| input | wrong rule | wrong output | right rule | right output |
|---|---|---|---|---|
| closed intervals $[1, 3]$, $[3, 5]$ | ends before starts | maximum overlap 1 | starts before ends | 2 |
| segments $(0,0)$ to $(2,2)$ and $(2,2)$ to $(4,0)$ | end of $a$ before start of $b$ | no intersection | left endpoints first (CLRS), or one event per point | intersection at $(2, 2)$ |
| three segments through $(2, 2)$ | swap one pair | order $s_3, s_1, s_2$ after $p$ | reverse the block | order $s_2, s_3, s_1$ |
| buildings $(1,4,3)$, $(4,6,3)$, $(4,7,2)$ | ends first, output after each event | 6 key points | batch per $x$ | $(1, 3), (6, 2), (7, 0)$ |

A non-example: for the union length or the [area of a union of rectangles](/area-of-union-of-rectangles/), the tie rule does not change the answer, since a boundary has length or area zero. A sweep that only measures can ignore ties between starts and ends; a sweep that decides touching cannot.

## Where it is used

Every sweep that runs on real data needs these rules. [Bentley-Ottmann](/bentley-ottmann-algorithm/) needs Rules 1 and 2 to report crossings of many segments through one point. [Shamos-Hoey](/shamos-hoey-algorithm/) needs Rule 3 for segments that share endpoints. The [rectangle intersection sweep](/rectangle-intersection-sweep/) and the [skyline sweep](/skyline-sweep/) need Rule 3 and its batch form. [Fortune's algorithm](/fortunes-algorithm/) has its own degenerate cases, such as four sites on one circle, which give several circle events at one point. The [rotational sweep](/rotational-sweep/) has the same issues in angle: several endpoints on one ray from the center. The tie rule is part of the [event queue](/event-queue/) order and the comparator of the [sweep status structure](/sweep-status-structure/), and the [sweep invariant](/sweep-invariant/) assumes that the rule makes all event keys distinct.

## References
