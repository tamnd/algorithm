---
title: The projection step, the straight self-consistent lines and the recovery of a segment
proves: [correctness]
status: full
---

We use the notation of the page. A curve $f$ is *self-consistent* for a random vector $X$ if $f(\lambda) = E[X \mid \lambda_f(X) = \lambda]$ for almost every $\lambda$, where the *projection index* $\lambda_f(x)$ is the largest $\lambda$ at which $\|x - f(\lambda)\|$ is smallest. The Hastie and Stuetzle algorithm alternates a projection step and a conditional expectation step, the latter estimated by a local linear smoother. There is no general proof that this loop converges, so we prove the parts that hold exactly.

## Part 1: the projection step

The curve is a polygon with vertices $v_1, \ldots, v_m$. For a segment $[a, b]$ with $a \ne b$ and a point $x$, let $t^* = \operatorname{clip}\big(\langle x - a, b - a\rangle / \|b - a\|^2,\ 0,\ 1\big)$.

**Lemma 1.** $a + t^*(b - a)$ is the unique nearest point of the segment to $x$.

*Proof.* $g(t) = \|x - a - t(b - a)\|^2$ is a quadratic in $t$ with leading coefficient $\|b - a\|^2 > 0$, so it is strictly convex with its minimum on $\mathbb{R}$ at the unclipped value. On $[0, 1]$ a strictly convex function has a unique minimizer, which is the clip of the free minimizer. $\square$

The nearest point of the polygon is the nearest of the $m - 1$ segment answers, and its arc length is the length of the earlier segments plus $t^* \|b - a\|$. On ties the implementation keeps the last one, which has the largest arc length, as the definition of $\lambda_f$ asks. So the projection step computes $\lambda_f(x_i)$ exactly, and for a fixed curve it gives each point its smallest possible distance. In particular it never increases $D^2 = \sum_i \|x_i - f(\lambda_i)\|^2$.

## Part 2: straight self-consistent lines are principal components

Let $X$ have mean $\mu$ and covariance $\Sigma$, and let $f(\lambda) = \mu + \lambda v$ with $\|v\| = 1$. Then $\lambda_f(x) = v^\top (x - \mu)$.

**Theorem 1.** If the line $f$ is self-consistent, then $\Sigma v = \operatorname{Var}(\lambda_f(X))\, v$: $v$ is an eigenvector of $\Sigma$.

*Proof.* Write $\Lambda = v^\top(X - \mu)$. By self-consistency $E[X - \mu \mid \Lambda] = \Lambda v$. Then

$$\Sigma v = E[(X - \mu)(X - \mu)^\top v] = E[(X - \mu)\Lambda] = E\big[E[X - \mu \mid \Lambda]\,\Lambda\big] = E[\Lambda^2]\, v,$$

and $E[\Lambda^2] = \operatorname{Var}(\Lambda)$ since $E[\Lambda] = 0$. $\square$

So the only straight principal curves are lines along eigenvectors of $\Sigma$, which is why the algorithm starts from the first principal component line. Conversely, for an elliptical distribution every principal component line is self-consistent, but not every distribution has a self-consistent first component line.

## Part 3: the smoother reproduces lines

The conditional expectation step fits, for each target $\lambda_0$, the weighted least squares line of each coordinate of $x$ on $\lambda$, with weights $w_i \ge 0$, and evaluates it at $\lambda_0$.

**Lemma 2.** If $x_i = c + \lambda_i u$ for all points with $w_i > 0$, and at least two such points have different $\lambda_i$, the fit returns $c + \lambda_0 u$.

*Proof.* For each coordinate, the line with intercept $c_k$ and slope $u_k$ has zero weighted squared error, which is the least possible. The minimizer is unique because the weighted design matrix with columns $1$ and $\lambda$ has full rank when two weighted points have different $\lambda$. $\square$

With tricube weights over the $q \ge 3$ nearest points in $\lambda$, all but the farthest of them have positive weight, so the condition holds unless almost all of the points share one $\lambda$.

## Part 4: points on a segment give the segment

**Theorem 2.** Let all points lie on the segment from $a$ to $b \ne a$, with both endpoints among them and at least three distinct points. Then the algorithm stops after one round, the curve is the segment from $a$ to $b$, and each $\lambda_i$ is the arc length of $x_i$ from one end, up to a shift.

*Proof.* The points lie on the line $a + s(b - a)$, so the covariance has rank 1 with range spanned by $b - a$, and the start line is the line through $a$ and $b$. The start index $\lambda_i = v^\top(x_i - \bar x)$ is then the signed position of $x_i$ on that line, shifted. The points satisfy $x_i = c + \lambda_i v$ exactly, so by Lemma 2 the smoother returns $f(\lambda_i) = x_i$ at each $\lambda_i$. The new polygon has the points themselves as vertices, in order along the segment, so it is the segment from $a$ to $b$. Each $x_i$ is a vertex, at distance 0, and the projection gives it the arc length of its own position. Then $D^2 = 0$ both before and after the round, and the stopping test holds. $\square$

## What is not claimed

The conditional expectation step uses a smoother, not the exact conditional expectation, so it does not minimize $D^2$ for fixed $\lambda$, and $D^2$ can rise a little from one round to the next. Hastie and Stuetzle note that the loop is not proved to converge for data. They also show that principal curves are biased: for data spread around a circle, the self-consistent curve is a circle of larger radius than the true one, and the smoother adds a second bias toward the center. Kégl, Krzyżak, Linder and Zeger (2000) avoid these problems with a different definition: a curve of length at most $L$ that minimizes the expected squared distance. That curve always exists, and their polygonal line algorithm estimates it.
