---
title: Shadow volumes count the occluders between a point and the light
proves: [correctness, termination]
status: full
---

We use the model and the pseudocode of the page. For a triangle $T = (a, b, e)$ let $n_T = (b - a) \times (e - a)$. Each occluder is a closed triangle mesh $M$ in which each directed edge $u \to v$ is in exactly one face and its reverse $v \to u$ is in exactly one other face. $M$ is the boundary of a solid $S_M$, and the normals point out of $S_M$. The light $L$ is outside each solid and in the plane of no face. So $L$ is on the line of no edge. The map $\varphi(v) = v + k(v - L) = L + (1 + k)(v - L)$ with $k > 0$ is a scaling about $L$. Line L2 calls a face $f$ *lit* when $n_f \cdot (L - v_0) > 0$. Let $D^+$ be the set of lit faces, $D^-$ the set of the other faces, and $\sigma$ the set of the directed edges that line L3 selects: an edge $u \to v$ of a lit face whose reverse is in an unlit face. The volume $V_M$ is $D^+$, the two triangles $(v, u, u')$ and $(v, u', v')$ for each $u \to v \in \sigma$ with $x' = \varphi(x)$, and $\varphi(D^-)$.

**Chains and winding numbers.** We treat a set of oriented triangles as a 2-chain and a set of directed edges as a 1-chain, with $-(u \to v) = (v \to u)$. For a triangle $T$ and a point $X \notin T$, let $\Omega_T(X)$ be the signed solid angle of $T$ seen from $X$, positive when $X$ is on the side of $T$ against $n_T$. We use these standard facts:

- (W1) If a chain $V$ has $\partial V = 0$, then $w_V(X) = \sum_{T \in V} \Omega_T(X) / 4\pi$ is an integer for each $X$ off $V$. It is constant on each connected region of the complement of $V$.
- (W2) If $V$ is bounded, then $w_V = 0$ outside a ball that contains $V$.
- (W3) $\Omega_T / 4\pi$ is continuous off $T$. Across the relative interior of $T$, it increases by $1$ when a point moves in a direction $d$ with $n_T \cdot d < 0$, and it decreases by $1$ when $n_T \cdot d > 0$.

Thus, if a segment from $A$ to $B$, with $A$ and $B$ off $V$, meets $V$ only in the relative interiors of triangles and is not parallel to them, then $w_V(B) - w_V(A)$ is the sum over these crossings of $+1$ when $n_T \cdot (B - A) < 0$ and $-1$ when $n_T \cdot (B - A) > 0$. Call a crossing with $n_T \cdot d < 0$ an *entry* and the other kind an *exit*. For the mesh $M$ itself, $w_M = 1$ in the interior of $S_M$ and $0$ outside.

**Termination.** Lines L2 to L4 do $O(1)$ work for each face and for each directed edge, with a table of edges. So line L1 makes $O(t)$ triangles for $t$ occluder triangles. Lines L5 to L10 do $O(1)$ work for each pair of a visible point and a volume triangle. All loops are over finite lists, so SHADOW-VOLUMES stops after $O(t + mt)$ steps.

**Lemma 1.** $\partial V_M = 0$. So $V_M$ is a closed, consistently oriented surface.

*Proof.* Each directed edge of $M$ is in one face and its reverse in another, so $\partial M = 0$ and $\partial D^+ = -\partial D^-$. In $\partial D^+$, an edge whose two faces are both lit cancels with its reverse. What is left is exactly the edges of lit faces whose reverse is in an unlit face, so $\partial D^+ = \sigma$. Because $\partial \sigma = \partial \partial D^+ = 0$, each vertex $x$ has as many edges of $\sigma$ that leave it as edges that enter it. The two triangles of the edge $u \to v$ have the boundary
$$(v \to u) + (u \to u') + (u' \to v) + (v \to u') + (u' \to v') + (v' \to v),$$
and the two diagonal terms cancel. Summed over $\sigma$, the first terms give $-\sigma$ and the terms $u' \to v'$ give $\varphi(\sigma)$. The other terms give $\sum_x (\text{out}(x) - \text{in}(x))\,(x \to x') = 0$. The map $\varphi$ is affine, so $\partial \varphi(D^-) = \varphi(\partial D^-) = -\varphi(\sigma)$. The sum of the three parts is $\sigma - \sigma + \varphi(\sigma) - \varphi(\sigma) = 0$. $\square$

**Lemma 2.** Let $X$ be a point off $V_M$. Let the ray $\rho$ from $L$ through $X$ meet $M$ only in the relative interiors of faces, not parallel to them, and not lie in the plane of a side triangle. Let $|X - L| < (1 + k)\,\mathrm{dist}(L, S_M)$. Then $w_{V_M}(X)$ is the number of entries of $\rho$ into $S_M$ on the segment $(L, X)$.

*Proof.* Let $d = X - L$. At a point $Y$ of a face $f$ on $\rho$, we have $n_f \cdot (L - v_0) = n_f \cdot (L - Y) = -\lambda\, n_f \cdot d$ with $\lambda > 0$. So $f$ is lit exactly when $\rho$ enters $S_M$ at $Y$. The four corners of the side triangles of $u \to v$ are of the form $L + s(y - L)$ with $y$ on the edge $uv$, so the triangles lie in the plane through $L$, $u$ and $v$, but do not contain $L$. The ray $\rho$ starts at $L$ and does not lie in that plane, so it does not meet them. The map $\varphi$ sends $\rho$ into itself and back, so $\rho \cap \varphi(f) = \varphi(\rho \cap f)$. Also, $\varphi(f)$ has the normal $(1 + k)^2 n_f$. So on the part of $\rho$ beyond $X$, the crossings of $\rho$ with $V_M$ are these:

- the entries of $\rho$ into $S_M$ beyond $X$, through the lit faces, each one an entry into $V_M$;
- the points $\varphi(Y)$ for each exit $Y$ of $\rho$ from $S_M$, each one an exit from $V_M$.

All these points $\varphi(Y)$ are beyond $X$, because $|\varphi(Y) - L| = (1 + k)|Y - L| \ge (1 + k)\,\mathrm{dist}(L, S_M) > |X - L|$. By (W3), $w(\infty) - w(X)$ is the number of entries of $\rho$ beyond $X$ minus the number of all exits. By Lemma 1 and (W2), $w(\infty) = 0$. Along $\rho$, $w_M$ starts at $0$ at $L$ and ends at $0$, and it takes only the values $0$ and $1$. So the entries and exits alternate, and there are as many exits as entries. Hence $w_{V_M}(X)$ is the number of all entries minus the number of entries beyond $X$, which is the number of entries on $(L, X)$. $\square$

**Lemma 3.** Under the assumptions of Lemma 2, let $X \notin S_M$. The closed segment from $X$ to $L$ meets $S_M$ exactly when $\rho$ has an entry into $S_M$ on $(L, X)$.

*Proof.* An entry at $Y \in (L, X)$ is a point of $M \subseteq S_M$ on the segment. Conversely, let $Y \in S_M$ be on the segment. Then $Y \ne L$ and $Y \ne X$, because both points are outside $S_M$. If $Y \in M$, then $Y$ is a crossing. If $Y$ is in the interior, $w_M(Y) = 1 \ne w_M(L)$. In both cases $\rho$ crosses $M$ on $(L, Y]$. The first crossing after $L$, where $w_M = 0$, is an entry. $\square$

Now let the occluders be $M_1, \dots, M_r$, and let $V = V_{M_1} + \dots + V_{M_r}$. Then $w_V = \sum_i w_{V_{M_i}}$. A visible point $P$ is *in general position* when it is in no solid $S_{M_i}$, it satisfies the assumptions of Lemma 2 for each $M_i$, and the line through the eye $C$ and $P$ meets no edge of $V$. The far cap condition $|P - L| < (1 + k)\,\mathrm{dist}(L, S_{M_i})$ is what the page calls "k large enough". With $k = 1000$, as in the implementation, it holds for each point less than $1001$ times as far from the light as the nearest occluder.

**Theorem 1.** For each visible point $P$ in general position, $w_V(P)$ is the number of occluders that meet the segment from $P$ to $L$. So $w_V(P) \ne 0$ exactly when $P$ is in shadow.

*Proof.* By Lemma 2, each term $w_{V_{M_i}}(P)$ is the number of entries into $S_{M_i}$ on $(L, P)$. By Lemma 3, this number is positive exactly when the segment meets $S_{M_i}$. The number is never negative, so the sum is $0$ exactly when no occluder meets the segment. $\square$

The counts that lines L5 to L10 make are not $1$ for each occluder in shadow. They are the number of entries, as Lemma 2 shows. Only the test $\ne 0$ has meaning.

**Lemma 4.** Let $T = (a, b, e)$, $c = C$, $p = P$, $\delta = p - c$ and $\mathrm{den} = n_T \cdot \delta \ne 0$. The line $c + t\delta$ meets the plane of $T$ at $X = c + t\delta$ with $t = n_T \cdot (a - c) / \mathrm{den}$. If $X$ is not on an edge of $T$, then CROSSING returns a value exactly when $X$ is in the interior of $T$, and the sign is $+1$ exactly when $\mathrm{den} < 0$, that is, at an entry.

*Proof.* The formula for $t$ solves $n_T \cdot (c + t\delta - a) = 0$. Let $\lambda_a, \lambda_b, \lambda_e$ be the barycentric coordinates of $X$ in $T$, with sum $1$. With $a - c = (a - X) + t\delta$ and $b - c = (b - X) + t\delta$, the terms with $\delta$ drop out of the determinant:
$$\delta \cdot \big((a - c) \times (b - c)\big) = \delta \cdot \big((a - X) \times (b - X)\big) = \lambda_e\, n_T \cdot \delta = \lambda_e\,\mathrm{den},$$
because $(a - X) \times (b - X) = \lambda_e\, n_T$ for a point $X$ in the plane. In the same way, the other two edges give $\lambda_a\,\mathrm{den}$ and $\lambda_b\,\mathrm{den}$. $X$ is not on an edge, so no $\lambda$ is $0$ and SIDE never uses its tie rule. The three signs agree exactly when the three $\lambda$ have one sign. Their sum is $1$, so they must all be positive, which means $X$ is in the interior. The sign that CROSSING returns is $+1$ when $\mathrm{den} < 0$. $\square$

If $\mathrm{den} = 0$, the line is parallel to the plane of $T$. A line in general position then does not meet $T$, because a line in the plane that meets $T$ meets an edge. So the result `None` is correct.

**Theorem 2 (z-pass).** Let $P$ be in general position, and let the eye $C$ be off $V$. Line L8 gives $\mathrm{count} = w_V(P) - w_V(C)$. So the z-pass answer is correct when the eye is in no shadow volume, and it can be wrong when the eye is in one.

*Proof.* By Lemma 4, the triangles that line L8 counts are exactly the crossings of $V$ with the open segment $(C, P)$, with the sign $+1$ at entries and $-1$ at exits. ($t = 0$ and $t = 1$ do not occur, because $C$ and $P$ are off $V$.) By Lemma 1 and (W3), the sum is $w_V(P) - w_V(C)$. If $w_V(C) = 0$, Theorem 1 gives the claim. The example on the page, with the eye at $(3, 4, 1)$, has $w_V(C) = 1$, and both of its answers are wrong. $\square$

**Theorem 3 (z-fail).** Let $P$ be in general position, and let $C$ be off $V$. Line L9 gives $\mathrm{count} = w_V(P)$, for each eye position. So the z-fail answer is always correct.

*Proof.* By Lemma 4, the triangles that line L9 meets are exactly the crossings of $V$ with the ray from $P$ in the direction $\delta$, at $t > 1$. Their signs are $+1$ at entries. By (W3), the sum of these signs is $w_V(\infty) - w_V(P)$, and $w_V(\infty) = 0$ by (W2), since $V$ is bounded. Line L9 subtracts each sign, so $\mathrm{count} = w_V(P)$. Theorem 1 gives the claim. $\square$

**The tie rule.** The general position assumption excludes eye lines through the edges of $V$. The implementation still gives a consistent answer for a line through the relative interior of an edge $ab$ that two triangles $T_1 = (a, b, e_1)$ and $T_2 = (b, a, e_2)$ share. SIDE is antisymmetric in its last two arguments, also with the tie rule, because the tie value is $+1$ for $a < b$ and $-1$ for $b < a$. In $T_1$ and $T_2$, the other two signs are those of $\mathrm{den}_1$ and $\mathrm{den}_2$. So $T_1$ counts the line when $s(a, b) = \operatorname{sign} \mathrm{den}_1$, and $T_2$ counts it when $s(a, b) = -\operatorname{sign} \mathrm{den}_2$. If the line crosses the surface at the edge, then $\mathrm{den}_1$ and $\mathrm{den}_2$ have the same sign. Then exactly one of the two triangles counts the crossing, with the correct sign. If the line only touches the surface there, then the signs are opposite. Then both triangles or neither count it, and the net change is $0$. In both cases the edge acts as if the line were moved a small distance to one side of it. The rule does not make such a promise at the vertices of $V$. $\blacksquare$
