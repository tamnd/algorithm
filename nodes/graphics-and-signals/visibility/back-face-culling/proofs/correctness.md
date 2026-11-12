---
title: Back-face culling keeps each visible point of a closed surface
proves: [correctness, termination]
status: full
---

We use the model and the pseudocode of the page. The faces are triangles that form a closed surface $\Sigma$, the boundary of a solid $S$, and the normal $n_f = (v_1 - v_0) \times (v_2 - v_0)$ of each face $f$ points out of $S$. Let $P_f$ be the plane of $f$. The eye $E$ is not in $S$. A point $X \in \Sigma$ is *visible* when the open segment from $E$ to $X$ meets no point of $\Sigma$. The set $K$ is the union of the faces that line L4 keeps.

**Termination.** The loop of line L2 has $F$ steps of $O(1)$ work each, so BACK-FACE-CULL stops after $\Theta(F)$ steps.

**Lemma 1.** Line L4 keeps $f$ exactly when $E$ is strictly on the outer side of $P_f$, that is, on the side to which $n_f$ points.

*Proof.* The points $Y$ of $P_f$ satisfy $n_f \cdot (Y - v_0) = 0$, and the outer side is the set where $n_f \cdot (Y - v_0) > 0$. Line L4 tests this sign at $Y = E$. $\square$

**Lemma 2.** Each point of the open segment $(E, X)$ to a visible point $X$ lies outside $S$.

*Proof.* The half-open segment $[E, X)$ is connected, it meets no point of $\Sigma = \partial S$, and its point $E$ is outside $S$. A connected set that does not meet the boundary of $S$ is wholly inside or wholly outside $S$, so it is outside. $\square$

**Theorem 1.** Let $X$ be a visible point in the relative interior of a face $f$, and let $E \notin P_f$. Then line L4 keeps $f$.

*Proof.* Let $d = X - E$. Because $X$ is in the relative interior of $f$ and $\Sigma$ is a closed surface whose normals point out, there is a ball $B$ around $X$ such that $B \cap S$ is the part of $B$ on the closed inner side of $P_f$. The line through $E$ and $X$ is not in $P_f$, because $E \notin P_f$, so it crosses $P_f$ only at $X$. For a small $\varepsilon > 0$ the point $Y = X - \varepsilon d$ is in $B$ and on the segment $(E, X)$. By Lemma 2, $Y \notin S$, so $Y$ is strictly on the outer side of $P_f$: $n_f \cdot (Y - v_0) > 0$. Since $n_f \cdot (X - v_0) = 0$, this gives $-\varepsilon\, n_f \cdot d > 0$, so $n_f \cdot d < 0$. Now $E = X - d$, so
$$n_f \cdot (E - v_0) = n_f \cdot (X - v_0) - n_f \cdot d = -\,n_f \cdot d > 0,$$
and line L4 keeps $f$. $\square$

**Theorem 2.** Let a ray from $E$ meet $\Sigma$, and let $X$ be its first point on $\Sigma$. Then $X \in K$. So the first point of the ray on the kept faces is $X$, the same as on all faces.

*Proof.* The point $X$ is visible. Let $N$ be the set of points $Z$ of $\Sigma$ such that $Z$ is on an edge, or $E \in P_f$ for a face $f$ that contains $Z$. Such a set lies in a finite union of segments and of faces seen edge on, so its projection from $E$ onto a sphere around $E$ has area zero. Hence there are points $Z_m \in \Sigma$ with $Z_m \to X$ such that the ray from $E$ through $Z_m$ meets $\Sigma$ first at a point $Q_m \notin N$. The point $Q_m$ is on the segment $[E, Z_m]$. Each $Q_m$ is visible and in the relative interior of a face $f_m$ with $E \notin P_{f_m}$, so $Q_m \in K$ by Theorem 1.

The points $Q_m$ lie in a bounded set, so a subsequence tends to a point $Q$. The segments $[E, Z_m]$ tend to $[E, X]$, so $Q \in [E, X]$. The surface $\Sigma$ is closed, so $Q \in \Sigma$, and since $X$ is the first point of $\Sigma$ on the ray, $Q = X$. The set $K$ is a finite union of closed triangles, so it is closed, and $X = \lim Q_m \in K$. No point of $K \subseteq \Sigma$ comes before $X$ on the ray, so $X$ is also the first point of the ray on $K$. $\square$

So at each pixel the nearest face hit by the pixel ray is the same with or without the dropped faces, and a depth test gives the same image.

**Theorem 3.** If $S$ is convex, then each point of each kept face is visible, and each face that has a visible point in its relative interior and is not seen edge on is kept. So the kept faces are exactly the faces with a visible point in their interior.

*Proof.* Let $f$ be kept and $X \in f$. Because $S$ is convex, $S$ lies on the closed inner side of $P_f$. By Lemma 1, $E$ is strictly on the outer side. Each point $(1 - \lambda) E + \lambda X$ with $0 \le \lambda < 1$ has $n_f \cdot ((1 - \lambda) E + \lambda X - v_0) = (1 - \lambda)\, n_f \cdot (E - v_0) > 0$, so it is strictly on the outer side and not in $S$. So the segment $[E, X)$ meets no point of $S \supseteq \Sigma$, and $X$ is visible. The second claim is Theorem 1. $\square$

**Remark.** The conditions are necessary. If $\Sigma$ is not closed, a face can be visible from its inner side, and if $E \in S$, each visible face has its inner side toward $E$; in both cases line L4 drops a visible face, as the tests show. If $S$ is not convex, Theorem 3 fails: a kept face of a far solid can be hidden by a near one. $\blacksquare$
