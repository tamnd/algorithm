---
title: Extended free-form deformation is the identity at rest on embedded points, reproduces affine maps, and is continuous across shared faces
proves: [correctness]
status: full
---

We use the notation of the page.
A chunk $b$ has the degree $(l, m, n)$ and the map $B_b(w; P) = \sum_{ijk} \beta_{ijk}(w)P_{g_b(i,j,k)}$, with $\beta_{ijk}(w) = B_i^l(w_1)B_j^m(w_2)B_k^n(w_3)$.
We say that line L7 accepts $(b, w)$ for $X$ if $|B_b(w; P) - X| < \text{tol}$ and $w \in [0, 1]^3$.

## What the algorithm returns

**Lemma 1.** If the algorithm returns a point for $X$, it returns $B_b(w; P')$ for a chunk $b$ and a parameter $w \in [0, 1]^3$ with $|B_b(w; P) - X| < \text{tol}$.

*Proof.*
Line L8 runs only after line L7 accepts $(b, w)$, and nothing changes $b$ or $w$ between the two lines. $\square$

So the result is a point of chunk $b$ of the edited lattice, at the parameter of a point of chunk $b$ of the rest lattice that is within tol of $X$.

## Identity and affine invariance

**Theorem 1.** If $P' = P$, the returned point $X'$ satisfies $|X' - X| < \text{tol}$.

*Proof.*
By Lemma 1, $X' = B_b(w; P)$ and $|B_b(w; P) - X| < \text{tol}$. $\square$

**Theorem 2.** If $P'_g = A(P_g)$ for an affine map $A(Y) = MY + c$ and every global index $g$, then $X' = A(B_b(w; P))$, so $|X' - A(X)| < \|M\|\,\text{tol}$.

*Proof.*
$\sum_{ijk}\beta_{ijk}(w) = 1$ for every $w$, by the binomial theorem in each variable.
So $B_b(w; P') = \sum \beta_{ijk}(w)(MP_{g_b(i,j,k)} + c) = MB_b(w; P) + c$.
Then $|X' - A(X)| = |M(B_b(w; P) - X)| \le \|M\|\,\text{tol}$. $\square$

## Continuity across a shared face

**Theorem 3.** Let chunk $a$ and chunk $b$ share a face: for all $j, k$, $g_a(l, j, k) = g_b(0, j, k)$, and both have the degrees $m, n$ in the other two variables. Then for every edited lattice $P'$ and all $(w_2, w_3)$, $B_a((1, w_2, w_3); P') = B_b((0, w_2, w_3); P')$.

*Proof.*
$B_i^l(1) = 1$ if $i = l$ and 0 otherwise, and $B_i^{l'}(0) = 1$ if $i = 0$ and 0 otherwise.
So $B_a((1, w_2, w_3); P') = \sum_{jk}B_j^m(w_2)B_k^n(w_3)P'_{g_a(l,j,k)}$ and $B_b((0, w_2, w_3); P') = \sum_{jk}B_j^m(w_2)B_k^n(w_3)P'_{g_b(0,j,k)}$, which are the same sum. $\square$

Two points just on each side of the face have parameters close to $(1, w_2, w_3)$ in chunk $a$ and $(0, w_2, w_3)$ in chunk $b$, so by the continuity of each polynomial they map to nearby points: the deformation has no tear at the face.
The first derivative across the face is $l(P'_{g_a(l,\cdot)} - P'_{g_a(l-1,\cdot)})$ on one side and $l'(P'_{g_b(1,\cdot)} - P'_{g_b(0,\cdot)})$ on the other, so the deformation is $C^1$ only if these agree; an edit that moves one inner layer alone breaks this, which is the crease of the Pitfalls.

## The embedding

Newton's method for $F(w) = B_b(w; P) - X = 0$ converges quadratically to a root $w^*$ if $J_b(w^*)$ is invertible, $J_b$ is Lipschitz near $w^*$, and the start is close enough to $w^*$ (the local convergence theorem for Newton's method on systems; see [Newton's method for systems](/newton-method-for-systems/)).
$B_b$ is a polynomial, so $J_b$ is Lipschitz on bounded sets.
The theorem says nothing about a start at $(1/2, 1/2, 1/2)$ far from the root, and the algorithm makes no claim there.
There are three ways the embedding can miss:
1. Newton's method does not converge within $K$ steps, or meets a singular $J_b$.
2. It converges to a root outside $[0, 1]^3$, which line L7 rejects, while another root inside the cube exists.
3. The rest chunk folds, so two parameters in the cube map to $X$, and the one found depends on the start.

In cases 1 and 2 the algorithm can return NOT FOUND for a point inside the lattice, and in case 3 the result is one of several valid answers.
If the rest chunk is one to one on $[0, 1]^3$ with an invertible Jacobian, case 3 cannot occur, and every root in the cube is the unique parameter of $X$.
The tests use a lattice of this kind, where the arc map $w_1 \mapsto (1 - w_1^2, 2w_1 - w_1^2)$ times the radius has a strictly increasing angle, so each chunk is one to one.
