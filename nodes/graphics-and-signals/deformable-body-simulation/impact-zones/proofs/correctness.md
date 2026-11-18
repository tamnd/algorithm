---
title: A rigid zone keeps its momentum and has no internal collision, so the zones stop growing after at most n - 1 passes
proves: [correctness]
status: full
---

We use the notation of the page, in 2D. Node $i$ has mass $m_i > 0$, start position $\mathbf x_i$ and velocity $\mathbf v_i$, and moves on $\mathbf x_i(s) = \mathbf x_i + s\, \Delta t\, \mathbf v_i$ for $s \in [0, 1]$. A *contact* at time $s$ is a node on an edge that does not contain it. We assume that the start state has no contact. All statements are in exact arithmetic.

## The rigid motion of a zone

For a zone $Z$ with $m = \sum_{i \in Z} m_i$, let $\mathbf x_{cm} = \frac1m \sum m_i \mathbf x_i$, $\mathbf v_{cm} = \frac1m \sum m_i \mathbf v_i$, $\mathbf r_i = \mathbf x_i - \mathbf x_{cm}$, $L = \sum m_i\, \mathbf r_i \times (\mathbf v_i - \mathbf v_{cm})$ (the scalar cross product) and $I = \sum m_i |\mathbf r_i|^2$. Lines L7 to L10 set $\omega = L/I$, $\varphi = \Delta t\, \omega$, the end position $\mathbf y_i = \mathbf x_{cm} + \Delta t\, \mathbf v_{cm} + R(\varphi) \mathbf r_i$ and the new velocity $\mathbf v_i' = (\mathbf y_i - \mathbf x_i)/\Delta t$. This is the formula of Bridson, Fedkiw and Anderson (2002, Section 7.5) in the plane, where the component along the axis of rotation is empty. If $|\varphi| \ge \pi$, the code uses $\varphi = 0$.

**Lemma 1.** (a) If the velocities are rigid, $\mathbf v_i = \mathbf u + \omega_0 J (\mathbf x_i - \mathbf c)$ with $J$ the rotation by $\pi/2$, then $\omega = \omega_0$. (b) $\sum m_i \mathbf v_i' = \sum m_i \mathbf v_i$. (c) The end positions are a rigid image of the start positions: $|\mathbf y_i - \mathbf y_j| = |\mathbf x_i - \mathbf x_j|$. (d) The angular momentum about $\mathbf x_{cm}$ of the new velocities is $L \sin \varphi / \varphi$ (and $L$ if $\varphi = 0$ because $L = 0$ or $I = 0$), not $L$.

*Proof.* (a) With $\sum m_i \mathbf r_i = 0$, $\mathbf v_i - \mathbf v_{cm} = \omega_0 J \mathbf r_i$, and $\mathbf r \times J\mathbf r = |\mathbf r|^2$, so $L = \omega_0 I$.
(b) $\sum m_i (\mathbf y_i - \mathbf x_i) = m\, \Delta t\, \mathbf v_{cm} + R(\varphi) \sum m_i \mathbf r_i - \sum m_i \mathbf r_i = m\, \Delta t\, \mathbf v_{cm}$.
(c) $\mathbf y_i - \mathbf y_j = R(\varphi)(\mathbf r_i - \mathbf r_j)$, and $R$ keeps lengths.
(d) $\mathbf v'_{cm} = \mathbf v_{cm}$ by (b), so the angular momentum is $\sum m_i \mathbf r_i \times (R(\varphi)\mathbf r_i - \mathbf r_i)/\Delta t = \sum m_i |\mathbf r_i|^2 \sin \varphi / \Delta t = I \sin\varphi / \Delta t = L \sin\varphi/\varphi$. For the fallback $\varphi = 0$ with $L \ne 0$, the new angular momentum is $0$. $\square$

So the zone keeps the linear momentum exactly, and the angular momentum up to the factor $\sin\varphi/\varphi = 1 - O(\varphi^2)$. This is the $O(\Delta t)$ error in the rotation that Bridson et al. accept when they hold $\omega$ constant over the step.

## No collision inside a rigid zone

**Lemma 2.** If $|\varphi| < \pi$, the straight paths of the nodes of a rigid zone have no contact among the nodes and edges of the zone at any $s \in [0, 1]$.

*Proof.* For a node of the zone, $\mathbf x_i(s) = (1 - s) \mathbf x_i + s \mathbf y_i = \mathbf x_{cm} + s\, \Delta t\, \mathbf v_{cm} + T_s \mathbf r_i$ with $T_s = (1 - s) I_2 + s R(\varphi)$. The same map $\mathbf r \mapsto \mathbf x_{cm} + s \Delta t \mathbf v_{cm} + T_s \mathbf r$ moves all nodes of the zone. Its determinant is $\big((1 - s) + s \cos\varphi\big)^2 + (s \sin \varphi)^2$. This is zero only if $s \sin\varphi = 0$ and $(1 - s) + s\cos\varphi = 0$; for $s = 0$ the second term is $1$, and for $\sin\varphi = 0$ with $|\varphi| < \pi$ we have $\varphi = 0$ and the second term is $1$. So the map is an invertible affine map for every $s$. An invertible affine map sends segments to segments and points on a segment to points on its image, and its inverse does the same. A contact of the zone at time $s$ would then give a contact at $s = 0$, which the start state does not have. $\square$

For the fallback $\varphi = 0$, $T_s = I_2$, so the lemma holds too.

## Termination

**Theorem 3.** The loop L2 to L10 ends after at most $n - 1$ passes that find collisions, and at the end the paths of all nodes have no contact.

*Proof.* At the start of every pass, each zone is a single node or has the rigid motion of its last merge, because a zone that is not touched keeps its velocities. Take a collision of the pass: node $i$ and edge $(a, b)$ with $i \notin \{a, b\}$. If $i$, $a$ and $b$ were all in one zone, that zone would have at least 3 nodes, so it is rigid, and Lemma 2 says that it has no internal contact. So the three nodes lie in at least two zones, and line L5 merges at least two zones. Each pass with a collision lowers the number of zones by at least one. There are $n$ zones at the start, so after at most $n - 1$ such passes there is one zone, which is rigid and has no contact by Lemma 2. The loop stops at the first pass with no collision, which is the claim. $\square$

**Corollary 4.** The end state has no two crossing edges and no node on an edge. A change in whether two segments meet needs a moment at which an endpoint of one lies on the other, which is a contact on the paths. The start state has none, so the end state has none.

**The zones are the components.** Line L5 unites the zones of $i$, $a$ and $b$ for each collision, and the disjoint-set structure only unites. So the final zones are the connected components of the graph whose edges join the three nodes of every collision found in every pass. The test compares them with a search of that graph.

## What is not claimed

The method does not give the motion that the cloth would have, and the page does not claim it does. It gives up all relative motion inside a zone, so cloth that is grouped this way freezes into clumps, as Bridson et al. note, and it does not keep the angular momentum exactly (Lemma 1 (d)). In floating point, Lemma 2 holds up to rounding, so a production code adds a small thickness. The tests use generic scenes, check the paths with the floating-point test, and check the end state with an exact rational test.
