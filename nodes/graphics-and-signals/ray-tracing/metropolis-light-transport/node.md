---
tag: 6R7C43
kind: algorithm
slug: metropolis-light-transport
name: Metropolis light transport
aliases:
- MLT
area: graphics-and-signals/ray-tracing
level: research
summary: Run a Metropolis-Hastings chain over light paths with a density proportional to their contribution, and make the image from the time the chain spends in each pixel.
solves: [global-illumination]
model: real-ram
complexity:
  vars: {M: the number of mutations, n: the number of bootstrap paths, K: the maximum number of edges of a path, c: the cost of one ray query, P: the number of pixels}
  time: {worst: Θ((n + M) K c + P)}
  space: {extra: Θ(P + n K)}
properties: {deterministic: false, recursive: false, online: true, in_place: false}
history:
  year: 1997
  people: [Eric Veach, Leonidas Guibas]
  note: Veach and Guibas presented Metropolis light transport at SIGGRAPH 97, with bidirectional mutations and lens and caustic perturbations. Kelemen and coauthors moved the chain to the space of the random numbers in 2002.
prereqs: [path-integral-formulation, metropolis-hastings, bidirectional-path-tracing]
see_also: [path-tracing, path-guiding, vertex-connection-and-merging, photon-mapping, detailed-balance, markov-chain, parallel-tempering, importance-sampling]
sources:
  - paper: doi:10.1145/258734.258775
    title: Eric Veach and Leonidas J. Guibas, Metropolis light transport, SIGGRAPH 97, 1997, 65 to 76
    locator: the Metropolis sampling of path space, the mutations, and the elimination of start-up bias
  - url: https://graphics.stanford.edu/papers/veach_thesis/
    title: Eric Veach, Robust Monte Carlo Methods for Light Transport Simulation, PhD thesis, Stanford University, 1997
    locator: Chapter 11, Metropolis Light Transport
  - paper: doi:10.1111/1467-8659.t01-1-00703
    title: Csaba Kelemen, László Szirmay-Kalos, György Antal and Ferenc Csonka, A simple and robust mutation strategy for the Metropolis light transport algorithm, Computer Graphics Forum 21(3), 2002
    locator: the chain over primary samples, with large steps and small steps
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Section 16.4 Metropolis Light Transport
---

Metropolis light transport renders an image with a Markov chain whose states are whole light paths, from a light to the camera. The chain moves by small changes, called mutations, and accepts or rejects each one with the [Metropolis-Hastings](/metropolis-hastings/) rule, so that in the long run it visits each path with a probability proportional to the light that the path carries. The brightness of a pixel is then the total of all paths times the fraction of time the chain spends in that pixel. Once the chain finds a path that carries light through a hard route, such as a keyhole or a caustic seen in a mirror, it explores the nearby paths by small changes instead of finding each one again by chance. This makes it strong where [path tracing](/path-tracing/) and [bidirectional path tracing](/bidirectional-path-tracing/) find the important paths only rarely.

## In plain words

Think of a person walking in the dark across a field to find where it is bright. At each step they try a small move, or sometimes a jump to a random place. If the new place is brighter, they always go there. If it is darker, they go there only sometimes, more often when it is only a little darker.

After a long walk, the person has spent the most time in the brightest places, in proportion to how bright they are. A record of where they stood is then a map of the light.

Metropolis light transport does this with light paths. A path is a route of light from a lamp to the eye. The method changes the route a little at each step, keeps the change by the rule above, and counts how long it stays on routes that end in each pixel.

## The problem

The scene, the [rendering equation](/rendering-equation/) and the [path integral form](/path-integral-formulation/) are as for [bidirectional path tracing](/bidirectional-path-tracing/). Each path $\bar x$ with $f_j(\bar x) > 0$ falls in exactly one pixel $j(\bar x)$, so the scalar function $f(\bar x) = f_{j(\bar x)}(\bar x)$ holds all of them, and

$$I_j = \int \mathbf 1[j(\bar x) = j]\, f(\bar x)\, d\mu(\bar x), \qquad b = \int f(\bar x)\, d\mu(\bar x) = \sum_j I_j.$$

For colors, the chain uses a scalar $F$ such as the luminance, and each recorded value is multiplied by $f / F$. If $\bar X$ has the density $f / b$, then $I_j = b \cdot P(j(\bar X) = j)$. The output is an estimate of every $I_j$.

## The algorithm

```pseudo id=main
MLT(M, n)
L1  draw n paths y1 … yn from a density T;  wi ← f(yi) / T(yi);  b ← (w1 + … + wn) / n
L2  x ← one of the yi, chosen with the probability wi / (w1 + … + wn)
L3  for i ← 1 to M
L4      propose y: with the probability p a new path from T, else a small change of x
L5      a ← min(1, f(y) T(y → x) / (f(x) T(x → y)))
L6      add a to the pixel of y and 1 − a to the pixel of x
L7      with the probability a: x ← y
L8  for each pixel j: Ij ← b / M · (the sum of the values added to pixel j)
```

$T(x \to y)$ is the density with which the mutation of line L4 proposes $y$ from $x$. For the new path from $T$ it is $T(y)$, which does not depend on $x$; this is the large step that keeps the chain from being stuck in one region. For the small change it is often symmetric, $T(x \to y) = T(y \to x)$, and the ratio cancels. Line L6 records the expected value of the next state instead of the state itself: the pixel of $y$ gets the probability $a$ that the chain goes there, and the pixel of $x$ gets the rest. This gives the same mean with less noise, and it lets rejected proposals still add to the image.

The implementation works on scenes of Lambertian spheres. A path is a list of up to $K$ surface points plus the pinhole. $T$ takes a uniform number of edges and each vertex uniform over the total area. The small change moves one vertex on its sphere by a uniform step in the height $z$ and the azimuth, reflected at the poles. Both proposals are densities with respect to the area measure, the same measure as $f$, so the ratio in line L5 is correct.

## Example

The scene is a unit sphere seen from its center, cut by the planes $z = -\tfrac12, 0, \tfrac12$ into four zones with albedo $\tfrac12, \tfrac14, \tfrac34, \tfrac12$ from the bottom, and the top zone emits radiance $4$. Pixel $j$ shows zone $j$. With paths of at most $K = 3$ edges, the Neumann series cut after two reflections gives

$$I = (0.75,\ 0.375,\ 1.125,\ 4.75), \qquad b = 7.$$

So the chain should spend the fractions $(0.107, 0.054, 0.161, 0.679)$ of its time in the four pixels. A chain of 20000 mutations with $p = 0.3$ and a step of $0.2$ (seed 7) spent $(0.116, 0.077, 0.159, 0.647)$. The large steps were accepted with the mean probability $0.17$ and the small steps with $0.91$: a small change of a good path is usually a good path, while a random path usually carries little light.

The mean of 16 independent chains, each with $n = 2000$ bootstrap paths (seed 1):

| $M$ per chain | pixel 0 | pixel 1 | pixel 2 | pixel 3 |
|---|---|---|---|---|
| 500 | $0.876 \pm 0.153$ | $0.428 \pm 0.077$ | $1.074 \pm 0.177$ | $4.764 \pm 0.233$ |
| 2000 | $0.862 \pm 0.069$ | $0.416 \pm 0.046$ | $1.127 \pm 0.062$ | $4.737 \pm 0.122$ |
| 8000 | $0.740 \pm 0.025$ | $0.392 \pm 0.029$ | $1.107 \pm 0.041$ | $4.904 \pm 0.068$ |
| exact | $0.75$ | $0.375$ | $1.125$ | $4.75$ |

The errors are the standard deviation over the chains divided by $\sqrt{16}$. The states of one chain are correlated, so their own spread says little about the error. The error falls roughly as $1 / \sqrt M$. This scene is easy, and MLT has no advantage here: its strength is in scenes where most random paths carry no light at all.

## Correctness

The chain of lines L3 to L7 is a [Metropolis-Hastings](/metropolis-hastings/) chain. For each of the two proposals, the acceptance of line L5 gives [detailed balance](/detailed-balance/) with respect to $f$: for $x \ne y$, $f(x)\, T(x \to y)\, a(x \to y) = \min(f(x) T(x \to y), f(y) T(y \to x))$, which is symmetric in $x$ and $y$. A mixture of kernels that each satisfy detailed balance satisfies it too, so $f / b$ is a stationary density. The large step proposes every path with $f > 0$, so the chain is irreducible on that set, and it is aperiodic because it can reject.

The image is unbiased for every $M$, not only in the limit. Line L2 draws the first state by resampling: for any function $g$, $E[b\, g(x_0)] = E[\tfrac1n \sum_i w_i g(y_i)] = \int f g\, d\mu$. Since the kernel $K$ of one step keeps $f$ fixed, $E[b\, g(x_m)] = \int f\, (K^m g)\, d\mu = \int f g\, d\mu$ for every $m$, and the expected value recording of line L6 has the same mean as $g(x_{m+1})$. With $g = \mathbf 1[\text{pixel } j]$, the mean of line L8 is $I_j$. This is the start-up bias elimination of Veach and Guibas. A chain that starts at an arbitrary path instead is consistent but biased for finite $M$. The full proof is in the proofs folder.

## Complexity

Each mutation evaluates $f$ once, which needs the visibility of each of at most $K$ edges, so it costs $O(K c)$; with the bootstrap, the time is $\Theta((n + M) K c)$, plus $\Theta(P)$ for the image. The memory is $\Theta(P)$ for the image and $\Theta(n K)$ for the bootstrap paths, or $\Theta(K)$ if the first state is chosen as the paths are made, with [weighted reservoir sampling](/weighted-reservoir-sampling/).

No useful bound on the variance holds in general. The variance depends on how fast the chain mixes, which depends on the scene and the mutations. In scenes where the light reaches the camera through a small set of paths, the chain stays in that set and explores it well, and MLT can be much better than independent sampling. In easy scenes it is often worse, because the samples are correlated and the error is uneven over the image: a region that the chain leaves for a long time stays dark, then gets too bright when the chain comes back.

## Properties

- **Unbiased with start-up bias elimination.** Each chain gives an unbiased image. With a fixed first path it is only consistent.
- **Samples in proportion to the brightness.** Bright pixels get many samples and dark pixels few. The relative error of dark pixels is larger than with path tracing at the same work.
- **Correlated samples.** The error estimate must come from independent chains or from batches, not from the spread of the states of one chain.
- **Needs $b$.** The chain gives only the ratios between pixels, so the total $b$ must come from a separate estimate, such as the bootstrap paths of line L1.
- **Local exploration.** A hard path, once found, is followed by its neighbors at the cost of small changes, not of new searches.
- **Mutations must be reversible.** A mutation needs a known $T(y \to x)$ for every move $x \to y$ it can make, and it must be able to undo each move.

## Variants and improvements

- **Veach and Guibas mutations.** Bidirectional mutations that delete a part of the path and make it again with the methods of bidirectional path tracing, lens perturbations that move the camera end of the path, caustic perturbations for paths through mirrors and glass, and multi-chain perturbations.
- **Primary sample space MLT.** Kelemen and coauthors in 2002 ran the chain over the vector of random numbers that a path tracer or a bidirectional path tracer uses to make a path. Mutations are simple changes of those numbers, the large step is a new random vector, and the proposals are symmetric. It is easy to add to an existing renderer.
- **Energy redistribution path tracing.** Cline, Talbot and Egbert in 2005 ran many short chains started from path tracing samples, which spreads the energy of rare paths to their neighbors.
- **Multiplexed MLT.** Hachisuka, Kaplanyan and Dachsbacher in 2014 let the chain also choose the strategy of bidirectional path tracing.
- **Manifold exploration.** Jakob and Marschner in 2012 moved paths with specular vertices along the set of paths that stay valid.
- **Replica exchange.** Several chains at different temperatures exchange states, as in [parallel tempering](/parallel-tempering/), to move between regions that are far apart.

## When to use it

Use Metropolis light transport for scenes where almost all of the light comes through paths that are hard to find: light through a slightly open door, light through glass onto a diffuse surface that is seen through glass, a scene lit only by caustics. Do not use it for animation without care, since the uneven noise flickers from frame to frame, and do not use it for easy scenes, where path tracing gives a more even error for the same work. In production, [path guiding](/path-guiding/) and [vertex connection and merging](/vertex-connection-and-merging/) are more common for the same scenes.

## Pitfalls

- **The wrong ratio.** The acceptance needs $T(y \to x) / T(x \to y)$ in the same measure as $f$. Mixing the solid angle measure and the area measure, or forgetting a Jacobian of a mutation, biases the image without any visible error.
- **Starting from a zero path.** If the first state has $f = 0$, line L5 divides by zero. Choose the first state from paths with $f > 0$, as in line L2.
- **Start-up bias.** A chain started from one fixed path needs a burn-in, and its first states are biased toward that path. Use the resampled start and the weight $b$, or discard a burn-in.
- **Too few large steps.** Without large steps, a chain cannot reach parts of path space that small changes cannot connect, for example light that comes through two separate windows. Then the image is wrong, not only noisy.
- **One long chain.** One chain gives no honest error estimate and is hard to run in parallel. Use many independent chains.
- **Colors.** The chain targets a scalar. If $F$ is $0$ where $f$ is not, as with a pure blue path and $F$ the red channel, that light is lost.

## Implementations

## History

Metropolis, Rosenbluth, Rosenbluth, Teller and Teller gave the Metropolis method in 1953, and Hastings gave the general acceptance rule in 1970. Veach and Guibas applied it to light transport at SIGGRAPH 97, with the path space of Veach's thesis, the mutations above, the expected value recording and the elimination of start-up bias. Kelemen, Szirmay-Kalos, Antal and Csonka moved the chain to the primary sample space in 2002, which made MLT simple to build on top of a path tracer, and much later work, such as manifold exploration and multiplexed MLT, builds on one of these two forms.

## References
