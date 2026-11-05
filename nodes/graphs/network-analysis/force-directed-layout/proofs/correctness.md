---
title: Each round of the Fruchterman-Reingold layout is a capped descent step on an energy, and its fixed points are the balanced drawings
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be an undirected simple graph with $n$ vertices, let $k > 0$, and let $p = (p_v)_{v \in V}$ be a drawing in $\mathbb{R}^2$ in which no two vertices share a point. Define

$$E(p) = \sum_{\{u,v\} \in E} \frac{\lVert p_u - p_v \rVert^3}{3k} - \sum_{\{u,v\} \subseteq V,\ u \ne v} k^2 \ln \lVert p_u - p_v \rVert .$$

**Lemma 1 (the displacement is the force).** After lines L3 to L5, $\mathrm{disp}[v] = -\nabla_{p_v} E(p)$ for every vertex $v$.

*Proof.* For $\delta = p_v - p_u \ne 0$ and $d = \lVert \delta \rVert$, the gradient of $d$ with respect to $p_v$ is $\delta/d$. So the gradient with respect to $p_v$ of the edge term $d^3/(3k)$ is $(d^2/k)(\delta/d)$, and that of $-k^2 \ln d$ is $-(k^2/d)(\delta/d)$. With respect to $p_u$ the signs flip, since $\delta$ changes sign. A pair term depends only on $p_u$ and $p_v$, so $-\nabla_{p_v} E$ is the sum, over all $u \ne v$, of $(k^2/d)$ times the unit vector from $u$ to $v$, plus the sum, over the neighbours $u$ of $v$, of $-(d^2/k)$ times the same unit vector. Line L4 adds exactly the first sum to $\mathrm{disp}[v]$, with the pair $\{u, v\}$ written in either order, and line L5 adds exactly the second. $\square$

**Lemma 2 (step length).** In line L6 of round $r$, each vertex moves by $\min(\lVert -\nabla_{p_v} E \rVert, t_r)$ in the direction of $-\nabla_{p_v} E$, where $t_r = t_0 (1 - (r - 1)/T)$; a vertex with zero force does not move.

*Proof.* Line L1 sets $t = t_0$, and line L7 at the end of round $r - 1$ sets $t = t_0(1 - (r-1)/T)$, so $t = t_r$ during round $r$. Line L6 moves $p_v$ by the unit vector of $\mathrm{disp}[v]$ times $\min(\lVert \mathrm{disp}[v] \rVert, t)$, and Lemma 1 identifies $\mathrm{disp}[v]$. $\square$

**Lemma 3 (fixed points).** Let $t > 0$. A round leaves the drawing $p$ unchanged if and only if $\nabla E(p) = 0$.

*Proof.* If $\nabla E(p) = 0$, every $\mathrm{disp}[v]$ is 0 by Lemma 1 and line L6 moves nothing. If some $\nabla_{p_v} E(p) \ne 0$, Lemma 2 moves $v$ by $\min(\lVert \nabla_{p_v} E \rVert, t) > 0$. $\square$

**Lemma 4 (two balance distances).** A single edge $\{u, v\}$ with no other vertex is balanced exactly when $\lVert p_u - p_v \rVert = k$. A path $a - b - c$ with $b$ at the midpoint of $a$ and $c$ on the segment between them is balanced exactly when $\lVert p_a - p_b \rVert = (3/2)^{1/3} k$.

*Proof.* For the edge, the force on $v$ along the unit vector from $u$ is $k^2/d - d^2/k$, which is zero exactly when $d^3 = k^3$. For the path, let $d = \lVert p_a - p_b \rVert = \lVert p_b - p_c \rVert$. By symmetry, the forces on $b$ from $a$ and from $c$ cancel. All forces on $c$ lie on the line, and along the unit vector from $b$ to $c$ they are $k^2/d$ from $b$, $k^2/(2d)$ from $a$ and $-d^2/k$ from the edge $\{b, c\}$. The sum is zero exactly when $d^3 = \frac32 k^3$, and the case of $a$ is the mirror image. $\square$

**Theorem.** FORCE-DIRECTED-LAYOUT stops after $T$ rounds. In round $r$ every vertex takes a step of length at most $t_r$ along the negative gradient of $E$ with respect to its own position, so it ends within distance $\sum_{r=1}^{T} t_r$ of its start. A drawing with distinct points is left unchanged by a round with positive temperature exactly when it is a critical point of $E$.

*Proof.* The loop of line L2 runs $T$ times, and each round does a finite amount of work. The step claims are Lemma 2, and the bound on the total distance follows by the triangle inequality. The last claim is Lemma 3. $\square$

∎
