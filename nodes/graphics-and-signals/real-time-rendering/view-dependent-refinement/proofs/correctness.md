---
title: Faces of a selectively refined mesh are present exactly when their creating vertex is split, force_vsplit ends with the vertex split, and the squared screen-space test equals the projected-length test
proves: [correctness]
status: full
---

We use the notation of the page. The progressive mesh is built by $N$ half-edge collapses, and the vertex hierarchy is the binary forest of these collapses: a collapse of the edge $(v_t, v_u)$ creates the parent $v_s$. The vsplit order lists the inner vertices from coarse to fine, and $\mathrm{idx}(v)$ is the position of $v$ in it. A vsplit of $v_s$ creates the two faces $f_l$ and $f_r$; we call $v_s$ their *creator*. The faces of the full mesh that are not created by any vsplit are the base faces. The record of $v_s$ also holds the four neighbor faces $f_{n0}, \ldots, f_{n3}$: the faces across the four outer edges of $f_l$ and $f_r$ in the mesh just after the vsplit of $v_s$ in the vsplit order.

The *front* $A$ is the set of active vertices: a set that meets each root to leaf path of the forest exactly once. The representative $\mathrm{rep}(w)$ of a vertex $w$ is the unique member of $A$ on the path from $w$ to its root, if $w$ is below or at the front. A vertex $v$ is *split* when it lies strictly above the front: no ancestor of $v$, and not $v$ itself, is in $A$. A face of the full mesh with the corners $(a, b, c)$ is *present* in the selectively refined mesh when $\mathrm{rep}(a)$, $\mathrm{rep}(b)$ and $\mathrm{rep}(c)$ are distinct, and it then has these corners.

## Which faces are present

**Lemma 1.** A face is present if and only if it is a base face or its creator is split.

*Proof.* Let $f$ be created by $v_s$ with the children $v_t$ and $v_u$, and let $f$ have the corners $v_t, v_u, x$ in the mesh just after the vsplit of $v_s$. Its corners in the full mesh are leaves $a$, $b$ and $c$ below $v_t$, $v_u$ and $x$. The vertices $v_s$ and $x$ are both vertices of the mesh at that moment, so their subtrees are disjoint, and $x$ is not an ancestor of $v_s$.

If $v_s$ is not split, then $v_s$ or one of its ancestors is in $A$, and it is the representative of both $a$ and $b$, so $f$ is not present.

If $v_s$ is split, then no vertex on the path from $v_s$ to its root is in $A$. So $\mathrm{rep}(a)$ lies in the subtree of $v_t$ and $\mathrm{rep}(b)$ in the subtree of $v_u$, and these are different. The representative of $c$ lies in the subtree of $x$ or is an ancestor of $x$. An ancestor of $x$ that is also an ancestor of $v_s$ is not in $A$. So $\mathrm{rep}(c)$ is outside the subtree of $v_s$, and the three representatives are distinct.

For a base face, the three corners are below three distinct roots, so their representatives are in three disjoint subtrees. $\square$

So the legality test of line L1, "all four neighbor faces are present", says that the creators of these faces are split. Each neighbor face exists in the mesh at the vsplit of $v_s$ in the vsplit order, so it is a base face or its creator comes earlier: $\mathrm{idx}(\mathrm{creator}(f_{nj})) < \mathrm{idx}(v_s)$.

## force_vsplit

**Theorem 2.** For an inner vertex $v_0$, FORCE-VSPLIT$(v_0)$ (lines L3 to L8) ends, and at its end $v_0$ is split. Every vsplit that it makes is legal in the sense of line L1, and it makes no edge collapse.

*Proof.* Each pass looks at the top $v$ of the stack and does one of four things: it pops $v$ if $v$ is split (L5); it pushes the parent of $v$ if $v$ is neither split nor active (L6); it pops $v$ and makes a legal vsplit of $v$ (L7); or it pushes the creators of the neighbor faces of $v$ that are not present (L8).

A pushed vertex is never split at the moment it is pushed. In L6, $v$ is neither split nor active, so an ancestor of $v$ is in $A$, and the parent of $v$ is that ancestor or lies below it; so it is not split. In L8, the pushed vertex is the creator of a face that is not present, and by Lemma 1 it is not split. Also each pushed vertex has a smaller index than $v$: a parent is split before its child in the vsplit order, and the creators of the neighbor faces come before $v$ by the remark after Lemma 1.

Now suppose that from some pass on, no vsplit happens. Then the front does not change, a vertex that is not split stays not split, and no pass pops a pushed vertex (L5 pops only split vertices, and L7 makes a vsplit). So each pass after that pushes, and the top of the stack is always the last vertex pushed. Its index strictly decreases from pass to pass. This cannot go on forever, so a vsplit happens. A vsplit only moves the front down, so at most $N$ vsplits can happen, and the loop ends.

The vertex $v_0$ is at the bottom of the stack. It leaves the stack by L5, when it is split, or by L7, when it is split there. $\square$

Hoppe's conditions make sure that a vsplit adds $f_l$ and $f_r$ between the right neighbor faces. They do not make sure that the faces keep their orientation: the test of the page found 12 of 1200 random states in which a face of the selectively refined height field is folded over in the domain. The tests check, on random sequences of legal vsplits and edge collapses, that the mesh stays an oriented manifold with boundary that covers the domain (each directed edge once, each border edge once, Euler characteristic 1). This is tested, not proved; the paper gives no proof of it.

## adapt_refinement

**Proposition 3.** If a pass of ADAPT-REFINEMENT (lines L9 to L11) makes no change, then every active inner vertex $v$ has $\mathrm{qrefine}(v)$ false, and every legal edge collapse of an active pair has $\mathrm{qrefine}$ of the parent true.

*Proof.* A pass visits each vertex that is active at the start. If it makes no change, it changes no state, so each test runs on the final front. A vertex with children and $\mathrm{qrefine}$ true would cause a change at L10. A vertex with a parent $p$ for which the collapse is legal and $\mathrm{qrefine}(p)$ is false would cause a change at L11. Both children of $p$ are active when the collapse is legal, so the pass visits them. $\square$

This is a fixed point, not an optimum: a forced vsplit can split vertices that $\mathrm{qrefine}$ does not ask for, and such vertices stay split as long as the collapse is not legal. The paper runs one pass per frame and makes no claim of convergence; the test observes that repeated passes reach a fixed point on its examples.

## The screen-space test

Let $e$ be the eye, $v$ a vertex at $p$, $w = p - e$ and $d = |w|$. The deviation space of $v$ is given by $\mu_v \ge 0$ and $\delta_v \ge 0$ with the unit normal $\hat n_v$. The squared test of Hoppe (Section 4, with $\kappa = \tau \tan(\varphi / 2) / 2$, that is $\kappa^2 = (2 \cot(\varphi/2))^{-2} \tau^2$) is

$$\mu_v^2 \ge \kappa^2 d^2 \quad \text{or} \quad \delta_v^2 \left(d^2 - (w \cdot \hat n_v)^2\right) \ge \kappa^2 d^4.$$

**Proposition 4.** For $d > 0$, the squared test holds if and only if $\max(\mu_v,\ \delta_v |\hat n_v \times w| / d) / d \ge \kappa$.

*Proof.* For a unit vector $\hat n$, $|\hat n \times w|^2 = |w|^2 - (\hat n \cdot w)^2$ (Lagrange's identity). The first part is $\mu_v / d \ge \kappa$, because both sides are nonnegative. The second part is $\delta_v^2 |\hat n_v \times w|^2 \ge \kappa^2 d^4$, which is $\delta_v |\hat n_v \times w| / d^2 \ge \kappa$ for the same reason. The maximum of two numbers is at least $\kappa$ exactly when one of them is. $\square$

The value $\delta_v |\hat n \times w| / d$ is the largest length that a segment $\delta_v \hat n$ shows across the line of sight, and dividing by $d$ gives its angular size, so the test compares the angular size of the deviation with $\kappa$. The values $\mu_v$ and $\delta_v$ that the code uses ($\mu_v = 0$, and $\delta_v$ the largest height jump of a split below $v$) are heuristics, not the bounds of the paper, which come from the fitted deviation of the surface. The bounding sphere radius $r_v$ and the normal cone in lines L12 and L13 are bounds over the leaf positions and the full-mesh face normals below $v$, which are a heuristic for the faces of the current mesh.
