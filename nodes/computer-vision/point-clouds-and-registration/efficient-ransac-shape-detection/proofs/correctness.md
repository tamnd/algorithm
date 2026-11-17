---
title: The minimal fits recover exact shapes, the extracted shapes are disjoint connected sets of compatible points, and the search stops
proves: [correctness]
status: full
---

Write $R$ for the set of remaining points, $\varepsilon$ for the distance tolerance, $\alpha$ for the angle tolerance, $\beta$ for the connectivity distance, $\tau \ge 3$ for the least support and $p_t < 1$ for the wanted probability. A point $p$ with unit normal $\mathbf{n}$ is *compatible* with a shape when its distance to the shape is at most $\varepsilon$ and $|\mathbf{n} \cdot \mathbf{s}| \ge \cos \alpha$, where $\mathbf{s}$ is the unit normal of the shape at the closest point. RANSAC methods do not find the true shapes with certainty, so the statements below are of two kinds: exact properties of every run, and the probability argument behind the stop rule.

## The fits of line L5

**Lemma 1 (exact minimal fits).** Let three points with unit normals lie exactly on a shape, with the true normals of the shape.

1. If the shape is a plane and the points are not collinear, the plane fit returns it.
2. If the shape is a sphere and the first two normals are not parallel, the sphere fit returns it.
3. If the shape is a cylinder and the first two normals are not parallel, the cylinder fit returns it.

*Proof.* (1) The vector $(p_2 - p_1) \times (p_3 - p_1)$ is nonzero and orthogonal to two independent directions of the plane, so it is a multiple of the plane normal $\mathbf{n}$, and $\mathbf{n} \cdot p_1 = d$. Every point has distance 0 and normal $\pm \mathbf{n}$, so the check passes.

(2) The normal of a sphere with center $c$ at $p_i$ is $\pm (p_i - c)/r$, so the line $p_i + t \mathbf{n}_i$ passes through $c$. Two lines with nonparallel directions that meet have exactly one common point, which is then the closest pair of points of both lines, so both closest points equal $c$ and their midpoint is $c$. Both distances to $c$ are $r$, so the radius is $r$, and all three points pass the check.

(3) The normal of a cylinder with axis $c + t \mathbf{a}$ at $p_i$ is the unit radial vector, which is orthogonal to $\mathbf{a}$. Two nonparallel vectors orthogonal to $\mathbf{a}$ have a cross product parallel to $\mathbf{a}$, so the fit finds the axis direction up to sign. Project along $\mathbf{a}$ onto the plane through the origin orthogonal to it. The axis becomes one point $\bar c$, and the projected normal line of $p_i$ passes through $\bar c$, because the radial vector runs from the axis to $p_i$. As in (2), the two projected lines meet only at $\bar c$, so the fit gets a point on the axis, and both axis distances are $r$. $\square$

With noise the fits are not exact, and the check of all three sample points against $\varepsilon$ and $\alpha$ rejects samples that do not fit one shape. The third point of a sphere or cylinder sample does not take part in the fit and serves only for this check.

## The lazy score of lines L6 and L7

The subsets $S_1, \ldots, S_r$ of line L1 are a partition of the points.

**Lemma 2 (the score becomes exact).** After a candidate is scored on all $r$ subsets, its score is the number of points of $R$ compatible with it.

*Proof.* Each refinement counts the points of one subset that are in $R$ and compatible. The subsets are disjoint and cover all points, and $R$ does not change while candidates are kept (the candidates are cleared at every extraction), so after all $r$ subsets the count is the exact count over $R$, and the code then sets the expected value and both ends of the interval to it. $\square$

**Lemma 3 (the refinement of line L7 stops).** The loop of line L7 ends, and it returns a candidate $m$ of largest expected score such that every other candidate either has an interval entirely below the lower end of the interval of $m$, or has been scored on all subsets, as has $m$.

*Proof.* Each round that does not return refines at least one candidate by one subset. A candidate can be refined at most $r$ times, and no candidate is added during the loop, so there are at most $r |C|$ rounds. The loop returns exactly when there is no rival with an upper end at or above the lower end of $m$, or when $m$ and every such rival are exact; this is the stated condition. $\square$

When the intervals are valid confidence intervals, a returned $m$ that has no rival is the candidate with the largest score with the probability of those intervals. When all the overlapping candidates are exact, $m$ has the largest score among them for certain.

## The extraction of lines L8 to L11

**Theorem 1 (the output).** Every shape in the output has at least $\tau$ points; each of its points was in $R$ when it was extracted and is compatible with it; its points are connected by steps of length at most $\beta$ between its own points; and the point sets of different shapes are disjoint.

*Proof.* Line L9 takes the set $I$ of points of $R$ compatible with $m$ and returns the largest connected component of the graph on $I$ with an edge for every pair at distance at most $\beta$. The search by grid cells of side $\beta$ finds every such pair, since two points at distance at most $\beta$ have cell coordinates that differ by at most 1 on each axis. Line L10 accepts the component only when it has at least $\tau$ points, and then removes it from $R$. Later shapes take their points from the smaller $R$, so they cannot take these points again. $\square$

## The stop rule of line L12

**Lemma 4 (missing a shape).** Let a shape have $n$ compatible points in $R$, and suppose each draw puts all three sample points among them with probability at least $q > 0$, independently of the other draws. Then the probability that none of $s$ draws does so is at most $(1 - q)^s$.

*Proof.* The draws are independent, so the probability that all $s$ fail is the product of the $s$ failure probabilities, each at most $1 - q$. $\square$

For three points drawn uniformly and independently from $R$, with replacement, $q = (n / |R|)^3$, and the function of lines L8 and L12 is $1 - (1 - q)^s$. Line L8 extracts the best candidate once a shape of its estimated size would have been hit with probability at least $p_t$: then it is unlikely that a larger shape was never drawn. Line L12 stops once a shape of $\tau$ points would have been hit with probability at least $p_t$ and no shape was extracted. The localized draws of line L4 are not uniform: they raise the chance for a compact shape that fills the cells it meets, and lower it for a shape spread thinly over many cells. So for this implementation the two tests are estimates, not bounds. Schnabel and his coauthors give a bound for localized sampling in an octree, which can replace $q$.

**Theorem 2 (termination).** If $p_t < 1$, the main loop ends.

*Proof.* Each extraction removes at least $\tau \ge 3$ points, so there are at most $n / 3$ extractions. Between two extractions, each pass of the loop adds 1 to the draw count $s$. While the loop runs, $|R| \ge \tau$, so $q_\tau = (\tau / |R|)^3 > 0$, and $1 - (1 - q_\tau)^s$ grows to 1 as $s$ grows. Once it reaches $p_t$, the next pass without an extraction stops the loop at line L12. The refinements inside a pass end by Lemma 3, and the sampling at line L4 always succeeds, because level 0 of the octree holds all of $R$, which has at least $\tau \ge 3$ points. $\blacksquare$
