---
title: The bridge search and the stored chains of the dynamic convex hull are correct
proves: [correctness, termination]
status: full
---

**Claim.** After every INSERT and DELETE, each node $v$ of the base treap stores in $\mathrm{up}(v)$ the upper chain and in $\mathrm{low}(v)$ the lower chain of the set $S_v$ of points in its subtree, as treaps in lexicographic order. So line L28 returns the vertices of the convex hull of the current set $S$ in counterclockwise order from the lexicographically smallest point. Every call of BRIDGE stops after at most $\operatorname{depth}(A) + \operatorname{depth}(B) + 1$ rounds of its loop, and every operation stops.

**Notation.** $D(p, q, r) = (q_x - p_x)(r_y - p_y) - (q_y - p_y)(r_x - p_x)$. Points are distinct and $<$ is the lexicographic order: $p < q$ when $p_x < q_x$, or $p_x = q_x$ and $p_y < q_y$. For a finite set $X$, the **upper chain** $U(X)$ and the **lower chain** $\Lambda(X)$ are the lists that Andrew's monotone chain makes from $X$ sorted by $<$: the upper chain pops while $D \ge 0$ and the lower chain pops while $D \le 0$. A chain treap holds the points of a chain as keys in the order $<$, with the heap order on priorities. In BRIDGE, $A$ and $B$ are the chains $U(L)$ and $U(R)$ (or $\Lambda(L)$ and $\Lambda(R)$ when $s = -1$) of two sets with $x < y$ for all $x \in L$, $y \in R$. For a chain point $c$, $c^-$ and $c^+$ are its neighbors in its own chain, if they exist.

**Step 1: reduction to distinct $x$-coordinates and to $s = +1$.** Let $\varphi_\varepsilon(x, y) = (x + \varepsilon y, y)$. It is linear with determinant 1, so $D(\varphi p, \varphi q, \varphi r) = D(p, q, r)$ for all points, and it maps lines to lines and intersection points to intersection points. Let $Z$ be the finite set of all current points and of all intersection points of two lines through two current points each. For $\varepsilon > 0$ small enough, two points of $Z$ satisfy $p < q$ exactly when the first coordinate of $\varphi_\varepsilon p$ is smaller than that of $\varphi_\varepsilon q$. The algorithm uses only $D$, the order $<$ and the intersection of line L27, so it does the same steps on $\varphi_\varepsilon(S)$ as on $S$. So we may assume that all points of $Z$ have distinct $x$-coordinates, that $<$ is the order by $x$, and that no chain has a vertical edge. Then the reflection $(x, y) \mapsto (x, -y)$ keeps the order, changes the sign of $D$, and maps lower chains to upper chains, so the case $s = -1$ is the case $s = +1$ for the reflected points. From now on $s = +1$, "above the line $ab$" means $D(a, b, q) > 0$, and slopes are finite.

**Step 2: facts about upper chains.** With distinct $x$-coordinates, $U(X)$ is the list, by increasing $x$, of the points $p \in X$ through which some line passes with all other points of $X$ strictly below it, as shown on the [upper and lower hull](/upper-and-lower-hull/) page. Its consecutive slopes decrease strictly. For a point $c$ of a chain $C$ let $\sigma^-(c)$ be the slope of the edge $c^- c$, or $+\infty$ if $c$ is first, and $\sigma^+(c)$ the slope of $c\, c^+$, or $-\infty$ if $c$ is last; so $\sigma^-(c) > \sigma^+(c)$, and $\sigma^+(c) = \sigma^-(c^+)$. Every point of $X$ lies on or below the line of every edge of $U(X)$. A line through a chain point $c$ with slope $\mu$ has all of $X$ on or below it exactly when $\sigma^-(c) \ge \mu \ge \sigma^+(c)$. We call such a line a **support** of $X$ at $c$.

**Step 3: the bridge.** Let $\ell^*$ be a line that supports $L \cup R$ and passes through a point of $L$ and a point of $R$, and let $s^*$ be its slope. It exists: take the edge of $U(L \cup R)$ from its last point in $L$ to its first point in $R$. It is unique: if two such lines $\ell^*, \ell'$ differ, $f = \ell^* - \ell'$ is linear, $f \le 0$ at the $x$-coordinate of a point of $L$ on $\ell^*$ and $\ge 0$ at one on $\ell'$, and the same with $R$, which forces $f \equiv 0$. Let $l$ be the leftmost point of $L$ on $\ell^*$ and $r$ the rightmost point of $R$ on $\ell^*$. Then $l$ is a point of $A$ and $r$ a point of $B$, and

$$\sigma^-(l) > s^* \ge \sigma^+(l), \qquad \sigma^-(r) \ge s^* > \sigma^+(r). \tag{1}$$

For a chain point $c$ of $A$, the slopes are monotone: $c \le l$ gives $\sigma^-(c) \ge \sigma^-(l) > s^*$, and $c \ge l$ gives $\sigma^+(c) \le \sigma^+(l) \le s^*$. The same holds in $B$ with $r$.

**Lemma 1 (merge).** $U(L \cup R)$ is the part of $A$ up to $l$ followed by the part of $B$ from $r$. So line L17 is correct.

*Proof.* Let $p \in L$. If $p$ is a point of $U(L \cup R)$, a line with all other points strictly below it shows that $p$ is a point of $A$. Let $p$ be a point of $A$ with $p < l$. Then $p$ is strictly below $\ell^*$, because $l$ is the leftmost point of $L$ on it. Take a line $\lambda$ through $p$ with slope $\mu$ strictly between $\sigma^+(p)$ and $\sigma^-(p)$, so all of $L \setminus \{p\}$ is strictly below $\lambda$. At $x = l_x$, $\lambda$ is strictly above $l$, so above $\ell^*$, and $\mu > \sigma^+(p) \ge \sigma^-(l) > s^*$, so $\lambda$ stays strictly above $\ell^*$ for $x \ge l_x$, where $R$ lies. So $p \in U(L \cup R)$. For $p = l$ take $\mu$ with $s^* < \mu < \sigma^-(l)$: $L \setminus \{l\}$ is strictly below the line, and for $x > l_x$ the line is strictly above $\ell^*$. Now let $p$ be a point of $A$ with $p > l$. Then $l_x < p_x < r_x$ and $p$ is on or below $\ell^*$, so on or below the segment $lr$. A line through $p$ with $l$ and $r$ strictly below it would pass strictly above the segment $lr$ at $p_x$, which is impossible. So $p \notin U(L \cup R)$. The points of $R$ are symmetric. $\square$

**Invariant of the descent.** At the start of each round of the loop at line L19, $l$ is in the subtree of $\alpha$ and $r$ in the subtree of $\beta$; $a_{\mathrm{pred}}$ and $a_{\mathrm{succ}}$ are the points of $A$ just before and just after the subtree of $\alpha$, if they exist, and the same for $\beta$. The second part holds at the start, and moving to a child keeps it, as the code sets the new outer neighbor to the point just left. So $a^-$, the predecessor of $a$ in $A$, is the last point of the left subtree of $\alpha$ if it is not empty, and $a_{\mathrm{pred}}$ otherwise; the code computes $a^-$, $a^+$, $b^-$ and $b^+$ this way. Let $\mu$ be the slope of $ab$.

**Lemma 2 (line L22).** If $a^-$ is on or above the line $ab$, then $l < a$.

*Proof.* Suppose $a \le l$. By Lemma 1, $a$ is a point of $U(L \cup R)$ and its predecessor there is $a^-$. Its successor there has slope $\sigma^+_*(a) < \sigma^-(a)$, and every point to the right of $a$, in particular $b$, is on or below the line of that edge, so $\mu \le \sigma^+_*(a) < \sigma^-(a)$. Then $a^-$, which is left of $a$, is strictly below the line $ab$. $\square$

**Lemma 3 (line L23).** If $b^+$ is on or above the line $ab$, then $r > b$. This is Lemma 2 with left and right exchanged.

**Lemma 4 (when lines L22 and L23 do not apply).** Assume that $a^-$, if it exists, is strictly below $ab$, and that $b^+$, if it exists, is strictly below $ab$.

- (a) If also $a^+$ is not strictly above $ab$, the line $ab$ supports $L$ at $a$ and $\mu \le s^*$. If $b^-$ is not strictly above $ab$, the line $ab$ supports $R$ at $b$ and $\mu \ge s^*$.
- (b) If neither $a^+$ nor $b^-$ is strictly above $ab$ (line L24), then $a = l$ and $b = r$.
- (c) If $a^+$ is strictly above $ab$ and $b^-$ is not (line L25), then $l > a$.
- (d) If $b^-$ is strictly above $ab$ and $a^+$ is not (line L26), then $r < b$.

*Proof.* (a) The conditions say $\sigma^-(a) > \mu \ge \sigma^+(a)$, so the line supports $L$ at $a$. Let $g = \ell^* - \overline{ab}$, a linear function of $x$. Then $g(a_x) \ge 0$ and $g(b_x) \ge 0$, as $a$ and $b$ are on or below $\ell^*$, and $g(l_x) \le 0$, as $l$ is on or below $\overline{ab}$. If $l_x > a_x$, then $a_x < l_x < b_x$ forces $g \equiv 0$. If $l_x \le a_x < b_x$, then $g$ does not decrease, so $\mu \le s^*$. The second part is the mirror image.

(b) By (a) the line $ab$ supports both $L$ and $R$, so it is $\ell^*$ by uniqueness. The point $a^-$ is strictly below it, so by concavity no point of $A$ left of $a$ is on it, and $a = l$. In the same way $b = r$.

(c) Suppose $l \le a$. Then $\sigma^+(a) \le s^*$ by the monotone slopes, and $\mu \ge s^*$ by (a) for $R$. But $a^+$ is right of $a$ and strictly above $ab$, so $\sigma^+(a) > \mu \ge s^*$, a contradiction. (d) is the mirror image. $\square$

**Lemma 5 (line L27).** Assume that $a^-$ and $b^+$ are not on or above $ab$, and that $a^+$ and $b^-$ are both strictly above $ab$. Let $\lambda_a$ be the line $a a^+$, $\lambda_b$ the line $b^- b$, and $r_0$ the first point of $B$. The lines cross at one point $z$. If $z < r_0$ then $l > a$, and otherwise $r < b$.

*Proof.* The slope of $\lambda_a$ is $\sigma^+(a) > \mu$ and that of $\lambda_b$ is $\sigma^-(b) < \mu$, so the lines are not parallel, and $h = \lambda_a - \lambda_b$ is strictly increasing and zero at $z_x$. By step 2, $L$ is on or below $\lambda_a$ and $R$ on or below $\lambda_b$.

Let $z < r_0$ and suppose $l \le a$. Then $s^* \ge \sigma^+(a)$, and $\ell^*(a_x) \ge a_y = \lambda_a(a_x)$, so $\ell^* \ge \lambda_a$ for all $x \ge a_x$. The point $r$ has $r_x \ge (r_0)_x > z_x$ and $r_x > a_x$, so
$$\ell^*(r_x) \ge \lambda_a(r_x) > \lambda_b(r_x) \ge r_y = \ell^*(r_x),$$
a contradiction. Let $z \ge r_0$ and suppose $r \ge b$. Then $s^* \le \sigma^-(b)$ and $\ell^*(b_x) \ge \lambda_b(b_x)$, so $\ell^* \ge \lambda_b$ for $x \le b_x$. The point $l$ has $l_x < (r_0)_x \le z_x$ and $l_x < b_x$, so $\ell^*(l_x) \ge \lambda_b(l_x) > \lambda_a(l_x) \ge l_y = \ell^*(l_x)$, a contradiction. $\square$

**Lemma 6 (BRIDGE returns $(l, r)$ and stops).** The cases of lines L21 to L27 cover all possibilities. By Lemmas 2 to 5, each move goes to the child of $\alpha$ that holds $l$, or to the child of $\beta$ that holds $r$, so the invariant is kept, and $\alpha$ and $\beta$ never become empty. Each round that does not return moves at least one of them one level down, so after at most $\operatorname{depth}(A) + \operatorname{depth}(B)$ such rounds the loop must reach line L24, where Lemma 4(b) gives $(a, b) = (l, r)$. $\square$

**Lemma 7 (chain treaps).** CHAIN-UPTO, CHAIN-FROM and CONCAT are the split and the merge of a treap with path copying, as on the [treap split](/treap-split/) and [treap merge](/treap-merge/) pages. They never change an existing node, so the chains that other nodes share stay valid. Each node keeps its key and its priority, so the results are treaps in the order $<$ with the heap order, and the fields $\mathrm{lo}$ and $\mathrm{hi}$ are set from the children when a node is made.

**Lemma 8 (base nodes).** Line L13 makes a node for $p$ with children $\ell$ and $\rho$, where every point of $S_\ell$ is less than $p$ and every point of $S_\rho$ is greater. If the children store their chains correctly, the new node does too.

*Proof.* $U(\{p\}) = \langle p \rangle$. By Lemmas 1, 6 and 7, the inner MERGE gives $U(S_\ell \cup \{p\})$ and the outer one $U(S_\ell \cup \{p\} \cup S_\rho)$, as each pair of sets is separated in the order $<$. The lower chain is the same with $s = -1$. Line L15 handles an empty side. $\square$

**Main result.** Every base node is made only by line L13, and its children were made before it, so by induction on the time of creation every base node stores the chains of its subtree. SPLIT and JOIN are the usual treap operations with path copying, so after line L3 or L5 the base treap is a treap of $S \cup \{p\}$ or $S \setminus \{p\}$, and $S_{\mathrm{root}}$ is the current set. By step 1, the upper and lower chains of $S$ are, after the shear, the upper and lower hulls with their strictly convex vertices, from the smallest to the largest point. Line L28 lists the lower chain and then the upper chain backwards without its two end points, which are the end points of the lower chain. This is the hull in counterclockwise order from the smallest point, as on the [upper and lower hull](/upper-and-lower-hull/) page. If all points are on one line, both chains are the two end points and the result is these two points; for one point it is that point.

**Termination.** BRIDGE stops by Lemma 6. Each recursive call of SPLIT, JOIN, CHAIN-UPTO, CHAIN-FROM and CONCAT goes one level down in a finite tree, so they stop, and line L13 calls MERGE four times. $\blacksquare$
