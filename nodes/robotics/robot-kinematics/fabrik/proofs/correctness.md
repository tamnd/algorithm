---
title: FABRIK keeps the chain valid, never increases the error, solves targets out of reach in one step, and can stall on a line
proves: [correctness]
status: full
---

We use the notation of the page, in exact arithmetic.
The chain has the joint positions $p_0, \ldots, p_n$ and the link lengths $d_1, \ldots, d_n > 0$.
A configuration is valid if $|p_i - p_{i-1}| = d_i$ for all $i$ and $p_0 = b$, the base.
For points $a \ne c$ and $d > 0$, $\operatorname{place}(a, c, d) = a + d\,(c - a)/|c - a|$ is the point at distance $d$ from $a$ on the ray towards $c$.

These claims are about what each step does.
They do not show that the iteration reaches a target in reach; Claim 6 shows that it can fail to.

## Claim 1: each placement is a nearest point

For every $x$ with $|x - a| = d$, $|x - c| \ge \big||c - a| - d\big| = |\operatorname{place}(a, c, d) - c|$.

*Proof.*
By the triangle inequality, $|x - c| \ge \big||c - a| - |x - a|\big| = \big||c - a| - d\big|$.
The point $\operatorname{place}(a, c, d)$ lies on the line through $a$ and $c$, on the same side of $a$ as $c$, at distance $d$ from $a$, so its distance to $c$ is $\big||c - a| - d\big|$.
$\square$

If $a = c$, every point at distance $d$ from $a$ is equally near to $c$, and the claims below hold for any choice of the point.
So in the backward pass, each new $p_i$ is the point at distance $d_{i+1}$ from the new $p_{i+1}$ that is nearest to the old $p_i$, and the same holds in the forward pass with the roles swapped.

## Claim 2: the output is a valid configuration

*Proof.*
After the forward pass at line L8, $p_0 = b$, and each $p_{i+1}$ is placed at distance $d_{i+1}$ from $p_i$, in the order $i = 0, \ldots, n - 1$.
Later placements in the same pass move only later points, so all lengths hold at the end of the pass.
The stretched chain of line L3 is built in the same way from $p_0 = b$.
$\square$

The backward pass alone gives $p_n = t$ and all lengths, but $p_0$ may leave the base; the forward pass then gives the base back and may move $p_n$ off the target.
This is why the method alternates.

## Claim 3: for a target out of reach, line L3 gives the best configuration

Let $|t - b| > D = d_1 + \cdots + d_n$.

*Proof.*
For every valid configuration, $|p_n - b| \le \sum_i |p_i - p_{i-1}| = D$, so $|p_n - t| \ge |t - b| - |p_n - b| \ge |t - b| - D > 0$.
At line L3, $|t - p_i| > 0$ at every step, since $p_i$ lies on the segment from $b$ towards $t$ at distance $d_1 + \cdots + d_i < |t - b|$ from $b$.
So every $p_i$ lies on the ray from $b$ to $t$, $p_n = b + D\,(t - b)/|t - b|$, and $|p_n - t| = |t - b| - D$, the lower bound.
$\square$

## Claim 4: the error never increases

Let $e_k = |p_n - t|$ before an iteration and $e_{k+1}$ after it, for a valid configuration.

*Proof.*
First, along one pass the moves of the points never grow.
In the backward pass, write $p_i'$ for the new points.
The point $x = p_i + (p_{i+1}' - p_{i+1})$ is at distance $|p_i - p_{i+1}| = d_{i+1}$ from $p_{i+1}'$, and by Claim 1 the new $p_i'$ is the point at that distance from $p_{i+1}'$ nearest to $p_i$.
So $|p_i' - p_i| \le |x - p_i| = |p_{i+1}' - p_{i+1}|$.
The first move is $|p_n' - p_n| = |t - p_n| = e_k$, so $|p_0' - b| \le e_k$.

In the forward pass, write $p_i''$ for the new points.
The same argument with the roles of $i$ and $i + 1$ swapped gives $|p_{i+1}'' - p_{i+1}'| \le |p_i'' - p_i'|$, and the first move is $|b - p_0'| \le e_k$.
So $e_{k+1} = |p_n'' - t| = |p_n'' - p_n'| \le e_k$.
$\square$

So the errors converge to a limit, but Claim 4 does not say that the limit is 0.

## Claim 5: solutions are fixed points

If a valid configuration has $p_n = t$, one more iteration does not change it.

*Proof.*
The backward pass sets $p_n = t$, which does not change it.
Then for $i = n - 1, \ldots, 0$, the point $p_i$ is at distance $d_{i+1}$ from the unchanged $p_{i+1}$, so $\operatorname{place}(p_{i+1}, p_i, d_{i+1}) = p_i$.
The forward pass is unchanged in the same way, since $p_0 = b$.
$\square$

So line L6 stops at a solution, and an iteration never moves away from one.

## Claim 6: a chain on a line through the base and the target stays on it

If $b$, $t$ and all $p_i$ lie on one line $\ell$, all later iterates lie on $\ell$.

*Proof.*
$\operatorname{place}(a, c, d)$ lies on the line through $a$ and $c$, which is $\ell$ when $a, c \in \ell$, and the passes only place points with $a$ and $c$ already on $\ell$ or equal to $t$ or $b$.
$\square$

For three links of length 1 m on the $x$ axis with $b = 0$, the end can only be at $x \in \{\pm 1, \pm 3\}$ on the line, since it is a sum of three terms $\pm 1$.
The target $(0.1, 0)$ m is in reach of the chain in the plane, but by Claim 6 the error stays at least 0.9 m for every iteration from a straight start.
So a convergence result for targets in reach must exclude such starts.
Section 3.3 of Aristidou, Chrysanthou and Lasenby (2016) states convergence for the unconstrained chain and a target in reach; the page cites it with this exception.
