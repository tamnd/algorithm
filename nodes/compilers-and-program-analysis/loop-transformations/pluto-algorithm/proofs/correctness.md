---
title: The Pluto algorithm terminates and returns a legal transformation whose bands can be tiled, with the stated bound on dependence distances
proves: [correctness]
status: full
---

**Setting.** We use the notation of the page. The program is a static control program with integer parameters $N$ in the context $K$. Statement $S$ has depth $d_S$ and a domain $D_S$. Each edge $e : S \to T$ of the input set $E_0$ has a polyhedron $P_e$, given by affine constraints $c_{e,i}(\vec{s}, \vec{t}, N) \ge 0$ that include the domains and the context. As on the [Feautrier scheduling](/feautrier-scheduling/) page, the edges are the memory-based dependences split by depth, and each edge has a *position* $\pi(e)$ in the original schedule vector $\Omega_S(\vec{s}) = (\beta^S_0, s_1, \beta^S_1, \dots, s_{d_S}, \beta^S_{d_S})$: $\pi(e) = 2l$ for an edge of depth $l$, and $\pi(e) = 2c + 1$ for a "same iteration" edge with $c$ common loops. For a dimension $\phi$ (an affine form per statement) and an edge $e$, write $\delta_e\phi(\vec{s}, \vec{t}) = \phi_T(\vec{t}) - \phi_S(\vec{s})$. The dimension $\phi$ *weakly satisfies* $e$ if $\delta_e\phi \ge 0$ on the integer points of $P_e$, and *strongly satisfies* it if $\delta_e\phi \ge 1$ there.

**Claim.** The loop stops. Let $\Phi = (\phi^1, \dots, \phi^m)$ be the list of dimensions it returns, and let the bands be its lists of hyperplanes.

1. *Legality.* For every $e \in E_0$, every $N \in K$ and every integer pair $(\vec{s}, \vec{t}) \in P_e$, $\Phi_S(\vec{s}) <_{\mathrm{lex}} \Phi_T(\vec{t})$.
2. *One to one.* For each $S$, the linear parts of the hyperplanes of $S$ contain $d_S$ linearly independent rows, so $\Phi_S$ is one to one on $D_S$.
3. *Tiling.* For any integer tile size $\tau \ge 1$, the vector $\Phi^\tau$ obtained by inserting $\lfloor \phi^k / \tau \rfloor$ for $k$ in a band $B$ in front of the hyperplanes of $B$, for every band with two or more hyperplanes, still satisfies claim 1.
4. *The cost bound.* If $\phi^k$ was found at line L3 with bound $(u, w)$, then $0 \le \delta_e\phi^k \le u \cdot N + w$ on $P_e$ for every edge $e$ that was in $E$ at that time. Every pair $(\vec{s}, \vec{t})$ of an edge in $E_0$ on which the dimensions before the band of $\phi^k$ are equal belongs to such an edge.

### Step 1: the linear constraints are sound

**Lemma 1 (affine Farkas lemma).** Let $P = \{x : c_i(x) \ge 0,\ i = 1, \dots, m\}$ be a nonempty polyhedron, with affine $c_i$. An affine form $\psi$ is nonnegative on all of $P$ if and only if $\psi \equiv \lambda_0 + \sum_i \lambda_i c_i$ for some $\lambda_0, \dots, \lambda_m \ge 0$.

This is Corollary 7.1h of Schrijver's book. $\square$

Line L3 writes $\delta_e\phi$ and $u \cdot N + w - \delta_e\phi$ in the form of Lemma 1, with new multipliers $\lambda \ge 0$ for each edge and each of the two forms, and matches the coefficients of $\vec{s}$, $\vec{t}$, $N$ and the constant. These equations are linear in the unknowns. For the correctness claims we need only the "if" part of Lemma 1, which holds for every $P$, empty or not: each term $\lambda_i c_i$ is nonnegative on $P$. So any solution of line L3 has

$$0 \le \delta_e\phi \le u \cdot N + w \quad \text{on } P_e, \text{ for every } e \text{ in the current } E. \tag{1}$$

The "only if" part says that line L3 misses no legal hyperplane within the coefficient bounds; this matters for the quality of the result, not for its correctness.

**Lemma 2.** The test of strong satisfaction is sound: if the rational minimum $\mu$ of $\delta_e\phi$ over $P_e$ exists and is positive, then $\delta_e\phi \ge 1$ on the integer points of $P_e$.

*Proof.* Every dimension that the algorithm builds has integer coefficients: the integer program asks for integers, the scalar dimension uses component indices, and lines L7 and L8 use components of $\Omega$ and unit vectors. So at an integer point, with integer $N$, $\delta_e\phi$ is an integer. It is at least $\mu > 0$, so it is at least 1. $\square$

### Step 2: every dimension weakly satisfies the current edges

**Lemma 3.** Each dimension appended while the current set is $E$ weakly satisfies every edge of $E$. The dimension of line L6 strongly satisfies each edge that line L6 removes, and the dimension of line L7 strongly satisfies at least one edge of $E$.

*Proof.* *Line L3.* This is (1).

*Line L6.* Let $\mathrm{ord}(S)$ be the index of the strongly connected component of $S$, in the graph whose arcs are the edges of $E$, with the components in topological order. For an arc $S \to T$, either both lie in one component, and $\delta_e = 0$, or the component of $S$ comes before that of $T$, and $\delta_e = \mathrm{ord}(T) - \mathrm{ord}(S) \ge 1$. The second case is exactly the set of edges that line L6 removes.

*Line L7.* Let $p = \min_{e \in E} \pi(e)$ and let $\phi_S$ be component $p$ of $\Omega_S$ (0 if $\Omega_S$ is shorter). For each edge $e \in E$, $p \le \pi(e) \le 2c_e + 1$, so place $p$ lies in the common prefix of the two vectors, where both have the same kind of entry. By Lemma 4 of the Feautrier scheduling proof, the places before $\pi(e)$ are equal on $P_e$ and place $\pi(e)$ grows by at least 1. So $\delta_e\phi = 0$ on $P_e$ if $\pi(e) > p$, and $\delta_e\phi \ge 1$ if $\pi(e) = p$, which holds for at least one edge. The rational minimum of $\delta_e\phi$ over $P_e$ is then at least 1, so the test of line L7 removes that edge.

*Line L8.* It runs only when $E$ is empty, and the claim is empty. $\square$

**Lemma 4.** An edge leaves $E$ only at lines L5, L6 and L7, and only when some dimension appended while it was in $E$ strongly satisfies it.

*Proof.* Line L5 removes an edge when some hyperplane of the band being closed passes the test of Lemma 2. Those hyperplanes were appended after the band began, and edges leave $E$ only at lines L5, L6 and L7, none of which runs while a band is open (line L5 closes it, and lines L6 and L7 run only when the band is empty). So the edge was in $E$ when each of them was appended. For lines L6 and L7, use Lemma 3. $\square$

### Step 3: termination and rank

Let $r = \sum_S \operatorname{rank} H_S$, the total rank of the hyperplane rows recorded for the statements.

**Lemma 5.** Each success of line L3 raises the rank of every statement that is not full. Each run of line L8 does the same.

*Proof.* Let $S$ be a statement with $\operatorname{rank} H_S < d_S$, and $c_S$ the linear part of the new $\phi_S$. If $H_S$ is empty, the constraint $\sum_j c_{S,j} \ge 1$ gives $c_S \ne 0$. Otherwise each row $h$ of $H_S^\perp = I - H_S^T (H_S H_S^T)^{-1} H_S$ (or a positive multiple of it) is orthogonal to every row of $H_S$, because $H_S H_S^\perp = 0$. The constraints $h \cdot c_S \ge 0$ for every row and $\sum_h h \cdot c_S \ge 1$ force $h \cdot c_S > 0$ for some row $h$. If $c_S$ were a combination of the rows of $H_S$, every $h \cdot c_S$ would be 0. So $c_S$ is independent of $H_S$. Line L8 appends a unit vector $e_x$ for the first counter $x$ with $\operatorname{rank}(H_S, e_x) = \operatorname{rank} H_S + 1$. Such an $x$ exists, because the unit vectors span the whole space and $H_S$ does not. $\square$

*Termination.* Every round of the loop does one of the following.

- A success of line L3 or a run of line L8. It raises $r$, which is at most $\sum_S d_S \le s d$. A run of line L8 happens only when some statement is not full, because the loop runs with $E$ empty only in that case.
- A run of line L5. It empties the band, which only a success or a run of line L8 fills. So there are at most $s d$ such rounds.
- A run of line L6 or L7. It removes at least one edge (Lemma 3), and no edge is ever added. So there are at most $|E_0|$ such rounds.

So the loop stops after at most $2 s d + |E_0|$ rounds. It stops only when $E$ is empty and every $H_S$ has rank $d_S$, which with Lemma 5 gives claim 2: the rows of $H_S$ are the linear parts of hyperplanes of $S$, and a map whose linear part has rank $d_S$ is one to one on $\mathbb{Z}^{d_S}$.

### Step 4: legality

Take $e \in E_0$ and an integer pair $(\vec{s}, \vec{t}) \in P_e$. At the end $E$ is empty, so $e$ left $E$ at some round. Let $r$ be the index of the last dimension appended up to the end of that round, and by Lemma 4 let $q \le r$ be the index of a dimension appended while $e$ was in $E$ that strongly satisfies it. By Lemma 3, every dimension $\phi^k$ with $k \le r$ weakly satisfies $e$, so $\delta_e\phi^k \ge 0$ for $k \le r$, and $\delta_e\phi^q \ge 1$. The first nonzero entry of $\Phi_T(\vec{t}) - \Phi_S(\vec{s})$ is at some place at most $q$, and it is positive. This is claim 1.

### Step 5: the bands can be tiled

**Lemma 6.** The hyperplanes of a band have consecutive indices. Let $B$ be a band, and let $e \in E_0$ and $(\vec{s}, \vec{t}) \in P_e$ be such that $\delta_e\phi^k = 0$ at this pair for every $k$ before the first index of $B$. Then $e$ was in $E$ during the whole band, and $\delta_e\phi^k \ge 0$ on $P_e$ for every $k \in B$.

*Proof.* While a band is open, only lines L3 and L8 append dimensions, and both append them to the band. Line L8 runs only when the band is empty, and then $E$ is empty. So a band is a run of consecutive dimensions. If $e$ had left $E$ before the band began, by Lemma 4 some dimension before the band would strongly satisfy it, and its $\delta_e$ would be at least 1 at the pair, not 0. Edges leave $E$ only when the band closes, so $e$ is in $E$ while each hyperplane of $B$ is appended. If $B$ began at line L8, then $E$ was empty and this cannot happen, so $B$ consists of hyperplanes from line L3, and (1) gives the inequality. $\square$

*Proof of claim 3.* Fix $e \in E_0$ and an integer pair in $P_e$, and let $k_0$ be the first place where $\Delta = \Phi_T(\vec{t}) - \Phi_S(\vec{s})$ is nonzero. By claim 1, $\Delta_{k_0} > 0$. The tiled vector $\Phi^\tau$ keeps all entries of $\Phi$ in the same order and adds tile entries in front of the bands of two or more hyperplanes. The tile entry of a dimension $k < k_0$ has difference 0, because $\phi^k$ takes the same value at the two points. If $k_0$ is not in a band with tile entries, the first nonzero entry of the difference of the tiled vectors is the entry of $\phi^{k_0}$, which is positive. Otherwise let $B$ be the band of $k_0$. Every $k$ before $B$ has $\Delta_k = 0$, so by Lemma 6, $\Delta_k \ge 0$ for every $k \in B$. The floor function is nondecreasing, so every tile entry of $B$ has a difference $\lfloor \phi^k_T(\vec{t}) / \tau \rfloor - \lfloor \phi^k_S(\vec{s}) / \tau \rfloor \ge 0$. If one of them is positive, the first nonzero entry is a positive tile entry. If all are 0, the entries that follow are those of $\Phi$ from the start of $B$ on, and the first nonzero one is $\Delta_{k_0} > 0$. In both cases $\Phi^\tau_S(\vec{s}) <_{\mathrm{lex}} \Phi^\tau_T(\vec{t})$. $\square$

### Step 6: the cost bound and what it measures

The first part of claim 4 is (1). For the second part, take a pair of an edge $e \in E_0$ on which the dimensions before the band $B$ of $\phi^k$ are equal. By Lemma 6, $e$ was in $E$ when $\phi^k$ was appended, so (1) applies to $e$.

The two readings of the bound in the paper of Bondhugula and others (CC 2008) follow from it. Let $b = u \cdot N + w$ and cut the space along $\phi$ into slabs of width $\tau$, $a\tau \le \phi < (a + 1)\tau$, for an integer $a$.

- *Communication.* Suppose $\phi$ is a parallel dimension, so that the slabs run on different processors. A value moves between processors along a dependence pair only if $\lfloor \phi_S(\vec{s}) / \tau \rfloor < \lfloor \phi_T(\vec{t}) / \tau \rfloor$. Let $a$ be the slab of the source. Then $\phi_T(\vec{t}) \ge (a + 1)\tau$, and $\phi_S(\vec{s}) = \phi_T(\vec{t}) - \delta_e\phi \ge (a + 1)\tau - b$. So every source that sends a value out of its slab lies in the last $b$ layers $\phi = (a + 1)\tau - b, \dots, (a + 1)\tau - 1$ of the slab. The number of values that a slab sends along $e$ is at most the number of points of $D_S$ in those $b$ layers. When $u = 0$ this does not grow with $N$ along $\phi$, and when $u = w = 0$ no value moves.
- *Reuse.* Suppose $\phi$ is a sequential dimension. The target $T(\vec{t})$ runs at most $b$ values of $\phi$ after the source $S(\vec{s})$, so $b$ bounds the reuse distance of the dependence, counted in hyperplanes $\phi = \text{const}$.

The integer program minimizes $(u, w)$ first in lexicographic order, so among the legal, independent hyperplanes within the coefficient bounds it picks one with the smallest such bound. This is a statement about the bound only. The number of points in a layer, the tile shape and the machine are not in the objective, so the minimum bound is a locality heuristic and not a proof of the fastest code. $\blacksquare$
