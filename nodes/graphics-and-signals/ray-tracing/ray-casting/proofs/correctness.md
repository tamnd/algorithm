---
title: Correctness of ray casting
proves: [correctness]
status: full
---

**Claim.** For each pixel, RAY-CAST stores the index of the visible object, that is the first object in scene order among those with the smallest hit parameter $t > 0$ on the pixel's ray, or NONE when the ray hits nothing; and it stores the gray value defined by the problem for that point. This holds in exact arithmetic, given intersection tests that return the smallest hit of their object in the interval they are given, and an any-hit query that answers whether some object is hit in the interval.

**The loop of line L4.** Fix a pixel and its ray $(o, d)$ from line L2. For each object $k$ let $t_k$ be its smallest hit parameter in $(0, \infty)$, or $\infty$ if it has none. We show by induction on $k$ that after the objects $0, \ldots, k - 1$ have been processed,

$$\mathrm{tmax} = \min_{j < k} t_j, \qquad \mathrm{best} = \min\{\,j < k : t_j = \mathrm{tmax}\,\} \text{ if } \mathrm{tmax} < \infty, \text{ and NONE otherwise.}$$

*Start.* Before any object, the minimum over the empty set is $\infty$ and best is NONE, as set by line L3.

*Step.* Object $k$ is tested on the interval $(0, \mathrm{tmax})$. It returns a hit $t$ exactly when $t_k < \mathrm{tmax}$, and then $t = t_k$, because the test returns the smallest hit in the interval and every hit of $k$ smaller than $t_k$ would contradict the definition of $t_k$. In that case the new minimum is $t_k$, it is attained by $k$ and by no earlier object, so best $= k$ is the first object that attains it, and line L4 sets tmax and best so. Otherwise $t_k \ge \mathrm{tmax}$; the minimum does not change, and the first object that attains it does not change either, since a later object with an equal value is not first. Line L4 changes nothing. So the invariant holds after object $k$.

After all $n$ objects, best is the visible object of the problem and tmax its hit parameter, or best is NONE. Line L5 handles NONE.

**The shading of lines L6 to L9.** The point $p = o + \mathrm{tmax}\,d$ is the visible point. The normal is turned so that $n \cdot d \le 0$, which is the side the viewer sees. With $L = \ell - p$, the segment from $p$ to the light is the set $p + t L$ for $t \in [0, 1]$. If $n \cdot L \le 0$, the light is behind the surface and the problem gives $k_a$. Otherwise the any-hit query on $(\varepsilon, 1 - \varepsilon)$ answers whether an object blocks the open segment, leaving out the end points, where the surface and the light are; as $\varepsilon \to 0$ this interval exhausts the open segment $(0, 1)$, and the problem's condition "the segment meets no object" is the case of a NO answer. Then line L9 evaluates $k_a + (1 - k_a)\,(n \cdot L) / (|n|\,|L|)$, which is $k_a + (1 - k_a) \cos \alpha$, and line L8 gives $k_a$ in the shadowed case.

So every pixel gets the visible object and the gray value of the problem. $\blacksquare$
