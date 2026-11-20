---
tag: 9NV2BH
kind: definition
slug: owen-multilinear-extension
name: "Owen's multilinear extension"
aliases:
- multilinear extension of a game
area: algorithmic-game-theory/cooperative-games
level: advanced
summary: Extends v to the cube by the expected value of a random coalition. The Shapley value is the integral of its gradient along the diagonal.
prereqs: [shapley-value, expected-value]
see_also: [banzhaf-index, shapley-shubik-index, shapley-value-sampling, fourier-analysis-of-boolean-functions, submodular-function, pipage-rounding, gaussian-quadrature, mobius-inversion]
sources:
  - paper: doi:10.1287/mnsc.18.5.64
    title: "Guillermo Owen, Multilinear extensions of games, Management Science 18(5, part 2) (1972), 64-79"
    locator: the definition of the multilinear extension, its derivatives, and the Shapley value as the integral of the gradient along the diagonal
  - paper: doi:10.1002/nav.3800220409
    title: "Guillermo Owen, Multilinear extensions and the Banzhaf value, Naval Research Logistics Quarterly 22(4) (1975), 741-750"
    locator: the Banzhaf value as the gradient of the multilinear extension at the center of the cube
  - book: isbn:9781608456529
    title: Georgios Chalkiadakis, Edith Elkind and Michael Wooldridge, Computational Aspects of Cooperative Game Theory, Morgan and Claypool, 2011
    locator: Chapter 2, Basic concepts (the Shapley value and the Banzhaf index), and Chapter 4, Weighted voting games
---

Owen's multilinear extension turns a TU game, a function on the $2^n$ coalitions, into a polynomial $f$ on the cube $[0, 1]^n$. The value $f(x)$ is the expected worth of a random coalition in which each player $i$ takes part with probability $x_i$, independently. The polynomial is affine in each variable, and it agrees with $v$ at the corners of the cube. Its partial derivatives are expected marginal contributions, and this gives short formulas for both power values: the [Shapley value](/shapley-value/) is the integral of the gradient along the diagonal from $(0, \ldots, 0)$ to $(1, \ldots, 1)$, and the Banzhaf value is the gradient at the center $(1/2, \ldots, 1/2)$.

## Definition

Let $(N, v)$ be a TU game with $N = \{1, \ldots, n\}$ and $v(\emptyset) = 0$. The *multilinear extension* of $v$ is the function $f : [0, 1]^n \to \mathbb{R}$,

$$f(x) = \sum_{S \subseteq N} v(S) \prod_{i \in S} x_i \prod_{i \notin S} (1 - x_i).$$

For $x \in [0, 1]^n$, let $S_x$ be a random coalition that contains each player $i$ with probability $x_i$, independently of the others. The product in the sum is $\Pr[S_x = S]$, so

$$f(x) = \mathbb{E}\big[v(S_x)\big].$$

At a corner $x = \mathbf{1}_S$ of the cube, $S_x = S$ with probability 1, so $f(\mathbf{1}_S) = v(S)$. The function $f$ is the only polynomial that agrees with $v$ on the corners and has degree at most 1 in each variable.

**The form by dividends.** Write $v = \sum_{T \ne \emptyset} d_T\, u_T$ with the Harsanyi dividends $d_T = \sum_{S \subseteq T} (-1)^{|T| - |S|} v(S)$ and the unanimity games $u_T$ (see [Möbius inversion](/mobius-inversion/)). The extension of $u_T$ is $\Pr[T \subseteq S_x] = \prod_{i \in T} x_i$, and $f$ is linear in $v$, so

$$f(x) = \sum_{T \ne \emptyset} d_T \prod_{i \in T} x_i.$$

The coefficients of $f$ in the monomial basis are the dividends.

**Derivatives.** Since $f$ is affine in $x_i$, its partial derivative is the difference of its values at $x_i = 1$ and $x_i = 0$:

$$\partial_i f(x) = \mathbb{E}\big[v(S \cup \{i\}) - v(S)\big],$$

where $S$ is a random subset of $N \setminus \{i\}$ that contains each $j \ne i$ with probability $x_j$. On the diagonal $x = (t, \ldots, t)$, a set $S$ of size $s$ has probability $t^s (1-t)^{n-1-s}$.

**The Shapley value.** For each player $i$,

$$\varphi_i(v) = \int_0^1 \partial_i f(t, \ldots, t)\, dt.$$

The integral of $t^s (1-t)^{n-1-s}$ over $[0, 1]$ is the Beta integral $\frac{s!\,(n-1-s)!}{n!}$, which is exactly the weight of a set of size $s$ in the subset formula of the Shapley value. In words: draw a uniform $t$, then let each other player join before $i$ with probability $t$. The set before $i$ then has the same distribution as $P_i^\pi$ for a uniform order $\pi$.

**The Banzhaf value.** For each player $i$,

$$\beta_i(v) = \partial_i f(1/2, \ldots, 1/2) = \frac{1}{2^{n-1}} \sum_{S \subseteq N \setminus \{i\}} \big(v(S \cup \{i\}) - v(S)\big),$$

because at $t = 1/2$ every subset of $N \setminus \{i\}$ has the same probability $2^{-(n-1)}$. This is the raw [Banzhaf index](/banzhaf-index/) on simple games (Owen 1975).

## Examples and non-examples

**The check game $[51; 50, 49, 1]$.** A coalition wins if it holds player 1 and at least one of players 2 and 3. So

$$f(x) = x_1 \big(1 - (1 - x_2)(1 - x_3)\big) = x_1 x_2 + x_1 x_3 - x_1 x_2 x_3.$$

The coefficients are the dividends: $d_{\{1,2\}} = d_{\{1,3\}} = 1$ and $d_{\{1,2,3\}} = -1$. The derivatives are $\partial_1 f = x_2 + x_3 - x_2 x_3$ and $\partial_2 f = x_1 (1 - x_3)$, and $\partial_3 f$ is $\partial_2 f$ with $x_2$ and $x_3$ swapped. On the diagonal, $\partial_1 f = 2t - t^2$ and $\partial_2 f = \partial_3 f = t - t^2$. The integrals over $[0, 1]$ are $1 - 1/3 = 2/3$ and $1/2 - 1/3 = 1/6$, so the Shapley-Shubik index is $(2/3, 1/6, 1/6)$. At $t = 1/2$ the derivatives are $3/4$ and $1/4$, so the raw Banzhaf index is $(3/4, 1/4, 1/4)$, with swing counts $3, 1, 1$ out of $2^2 = 4$ sets.

**A game with two pair dividends.** For $v = 4u_{\{1,2\}} + 2u_{\{1,3\}}$ (the example on the [Shapley value](/shapley-value/) page), $f(x) = 4x_1x_2 + 2x_1x_3$. On the diagonal, $\partial_1 f = 6t$, $\partial_2 f = 4t$ and $\partial_3 f = 2t$. Both the integrals and the values at $t = 1/2$ are $(3, 2, 1)$: when $f$ has only terms of degree 2, the derivatives are linear in $t$, and the mean of a linear function on $[0, 1]$ is its value at $1/2$.

**Non-example: the value of $f$ on the diagonal.** The number $f(t, \ldots, t)$ is the expected worth of a random coalition. It is not a payoff of any player, and $\int_0^1 f(t, \ldots, t)\, dt$ is not a solution concept.

**Non-example: other extensions.** A set function has many continuous extensions. The Lovász extension is piecewise linear, and it is convex if and only if the set function is submodular. The multilinear extension is neither convex nor concave in general, even for a [submodular function](/submodular-function/); it is concave only along nonnegative directions in that case. Do not mix the two when you use results from submodular optimization.

## Related definitions

- **[Shapley value](/shapley-value/)** and **[Banzhaf index](/banzhaf-index/)**: the integral of $\nabla f$ on the diagonal and $\nabla f$ at the center.
- **Influence of a variable.** For a simple game, $v$ is a monotone Boolean function, and $\partial_i f(1/2, \ldots, 1/2)$ is the influence of the variable $i$ in [Fourier analysis of Boolean functions](/fourier-analysis-of-boolean-functions/): the probability that flipping $i$ changes the output on a uniform input.
- **Exact quadrature.** On the diagonal, $\partial_i f(t, \ldots, t)$ is a polynomial in $t$ of degree at most $n - 1$. [Gauss-Legendre quadrature](/gaussian-quadrature/) with $\lceil n/2 \rceil$ nodes integrates it exactly, so $\lceil n/2 \rceil$ values of the derivative give the Shapley value of player $i$.
- **Sampling.** The integral form gives a [Monte Carlo estimate](/shapley-value-sampling/): draw $t$, draw $S$ with the probability $t$ for each player, and average the marginal contribution. For a weighted voting game with many small players, $w(S)$ for this random $S$ is close to a normal variable, which gives a quick estimate of $\partial_i f$; Owen used this idea for large voting games.
- **Submodular maximization.** The same extension is the relaxation used in continuous methods for maximizing a monotone submodular function under a matroid constraint, with rounding such as [pipage rounding](/pipage-rounding/).

## References
