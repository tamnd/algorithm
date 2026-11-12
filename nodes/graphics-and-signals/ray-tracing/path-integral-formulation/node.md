---
tag: MAM9VT
kind: concept
slug: path-integral-formulation
name: Path integral formulation of light transport
aliases:
- path space formulation
area: graphics-and-signals/ray-tracing
level: advanced
summary: Write each pixel value as one integral over all light paths of all lengths, from a light to the camera, with an area-product measure. Path sampling methods differ only in their path densities.
prereqs: [rendering-equation]
see_also: [bidirectional-path-tracing, metropolis-light-transport, light-tracing, multiple-importance-sampling, path-tracing, vertex-connection-and-merging, monte-carlo-integration, importance-sampling]
sources:
  - url: https://graphics.stanford.edu/papers/veach_thesis/
    title: Eric Veach, Robust Monte Carlo Methods for Light Transport Simulation, PhD thesis, Stanford University, 1997
    locator: Chapter 8, the path integral formulation (path space, the area-product measure, the measurement contribution function, and path sampling with local techniques)
  - paper: doi:10.1145/218380.218498
    title: Eric Veach and Leonidas J. Guibas, Optimally combining sampling techniques for Monte Carlo rendering, SIGGRAPH 95, 1995, 419 to 428
    locator: the pixel value as an integral over paths, and the sampling techniques of bidirectional path tracing as densities on it
  - paper: doi:10.1145/258734.258775
    title: Eric Veach and Leonidas J. Guibas, Metropolis light transport, SIGGRAPH 97, 1997, 65 to 76
    locator: the path integral as the space on which the Markov chain moves
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Section 14.4, The Light Transport Equation (the surface form and the integral over paths)
  - paper: "Paul S. Heckbert, Adaptive radiosity textures for bidirectional ray tracing, Computer Graphics (SIGGRAPH 90) 24(4), 1990"
    locator: the regular expressions over L, D, S and E that classify light paths
---

The path integral formulation writes the value of a pixel as a single integral over *paths*: chains of points $\bar x = x_0 x_1 \cdots x_k$ that start on a light, bounce off surfaces, and end on the camera sensor, for every length $k$ at once. The integrand, the measurement contribution function, is a product of one factor per vertex and one per edge, and the measure is the product of surface areas. Veach (1997) gave it in this form, building on the surface form of the [rendering equation](/rendering-equation/): it is that equation's Neumann series, with each term turned into an integral over the points of a path and all the terms joined into one integral. The form does not solve anything by itself. Its use is that every Monte Carlo method on paths becomes a choice of a probability density on the same space: [path tracing](/path-tracing/) builds paths from the camera, [light tracing](/light-tracing/) from the lights, [bidirectional path tracing](/bidirectional-path-tracing/) from both ends, and [Metropolis light transport](/metropolis-light-transport/) runs a Markov chain over them. Then [multiple importance sampling](/multiple-importance-sampling/) can weigh all of them against each other.

## In plain words

Light reaches the camera along routes: from a lamp to a wall, to the floor, to the lens. Each route is a list of points. A route has a value, which is how much light it carries, and that value is a product: the brightness of the lamp, times how much each surface passes on in the next direction, times a factor for each straight piece that says how well the two ends face each other and how far apart they are.

The picture is the sum of the values of all routes, of every length. There are infinitely many, so it is an integral, not a sum.

Every rendering method that picks random routes is then just a different way to pick them. Some start at the camera, some at the lamp, some at both ends, and some change a good route a little to find more.

## The idea

**Paths and their measure.** Let $M$ be the union of all surfaces. A path of length $k$ is a point $\bar x = x_0 x_1 \cdots x_k$ of $\Omega_k = M^{k+1}$, with $x_0$ on a light and $x_k$ on the sensor. Path space is the union $\Omega = \bigcup_{k \ge 1} \Omega_k$, and its measure $\mu$ is the product of the area measures on each $\Omega_k$, so that $d\mu(\bar x) = dA(x_0)\, dA(x_1) \cdots dA(x_k)$.

**The integral.** For pixel $j$,

$$I_j = \int_\Omega f_j(\bar x)\, d\mu(\bar x) = \sum_{k \ge 1} \int_{M^{k+1}} f_j(x_0 \cdots x_k)\, dA(x_0) \cdots dA(x_k),$$

with the measurement contribution function

$$f_j(\bar x) = L_e(x_0 \to x_1)\, G(x_0 \leftrightarrow x_1) \prod_{i=1}^{k-1} f_s(x_{i-1} \to x_i \to x_{i+1})\, G(x_i \leftrightarrow x_{i+1}) \cdot W_j(x_{k-1} \to x_k).$$

Here $L_e$ is the emitted radiance, $f_s$ the BSDF at each inner vertex, $W_j$ the response of pixel $j$, and $G(x \leftrightarrow y) = V(x, y) \cos\theta_x \cos\theta_y / \lVert x - y \rVert^2$ the geometry term with the visibility $V$. To get it, substitute the surface form of the rendering equation into itself $k - 1$ times; the integral over $\Omega_k$ is the term of the [Neumann series](/neumann-series/) for paths with $k - 1$ reflections.

**Estimators are densities.** Any method that makes a random path $\bar x$ with a density $p(\bar x)$ with respect to $\mu$ gives the unbiased estimate $f_j(\bar x) / p(\bar x)$ of $I_j$, as long as $p > 0$ wherever $f_j \neq 0$. That is [importance sampling](/importance-sampling/) on $\Omega$. A path is built by sampling one vertex after another, usually by choosing a direction with a density $p_\omega$ per solid angle and tracing a ray; the density per area of the point $y$ that the ray hits from $x$ is

$$p_A(y) = p_\omega(\omega)\, \frac{\lvert \cos\theta_y \rvert}{\lVert x - y \rVert^2}.$$

So all methods can be compared, and combined, in one measure.

**Sampling techniques.** A path of length $k$ has $k + 1$ vertices. Take $s$ of them from a walk that starts at a light and $t = k + 1 - s$ from a walk that starts at the camera, and join the two ends with a shadow ray. The $k + 2$ choices $s = 0, \dots, k + 1$ are the techniques of bidirectional path tracing; $s = 0$ is path tracing that hits a light by chance, $t = 1$ is light tracing, and each technique has its own density $p_{s,t}$. Because they are densities on the same space, the balance heuristic $p_{s,t} / \sum_{s'} p_{s',k+1-s'}$ weights them.

**Paths as strings.** Heckbert (1990) labeled vertices by $L$ (light), $D$ (diffuse or glossy), $S$ (specular) and $E$ (eye), and classes of paths by regular expressions: $L D E$ is direct diffuse light, $L S^+ D E$ a caustic, and $L (D \mid S)^* E$ all paths. A specular vertex makes $f_s$ a Dirac delta, so the density must also have a delta there, and a path with a point light, a pinhole camera and the pattern $L S D S E$ has density zero for every local technique.

**Markov chains on paths.** Since $\Omega$ is one space, a Markov chain can move on it with a stationary density proportional to $f_j$, or to a sum over pixels. That is the basis of Metropolis light transport, which uses [Metropolis-Hastings](/metropolis-hastings/) with mutations that add, delete or move vertices.

## Examples

**The zoned sphere, by path length.** Inside a sphere of radius $R$, both cosines between two points equal $\lVert x - y \rVert / (2R)$, so $G = 1/(4R^2)$ for every pair. The sphere of the rendering equation page has four zones of equal area, the emission $(0, 0, 0, 4)$ in the top zone, and the albedo $\rho = (\tfrac12, \tfrac14, \tfrac34, \tfrac12)$, all Lambertian, $f_s = \rho / \pi$. Measure the radiance that leaves a point of zone $j$. A path with one reflection contributes

$$\int_{\text{zone 4}} L_e \, G \, \frac{\rho_j}{\pi} \, dA = 4 \cdot \frac{1}{4R^2} \cdot \frac{\rho_j}{\pi} \cdot \pi R^2 = \rho_j,$$

because the top zone has the area $\pi R^2$. Each further reflection adds one more integral over the whole sphere of $G \rho / \pi$, which is the mean albedo $\tfrac12$. So paths with $r$ reflections contribute $\rho_j (\tfrac12)^{r - 1}$ for $r \ge 1$, and the emission itself for $r = 0$:

| reflections $r$ | 0 | 1 | 2 | 3 | 4 | all |
|---|---|---|---|---|---|---|
| zone 1 ($\rho = \tfrac12$) | 0 | 0.5 | 0.25 | 0.125 | 0.0625 | 1 |
| zone 3 ($\rho = \tfrac34$) | 0 | 0.75 | 0.375 | 0.1875 | 0.09375 | 1.5 |
| zone 4 ($\rho = \tfrac12$, emits 4) | 4 | 0.5 | 0.25 | 0.125 | 0.0625 | 5 |

The sums are the exact solution $(1, \tfrac12, \tfrac32, 5)$ that the linear system gives. The tests of path tracing, light tracing, bidirectional path tracing and Metropolis light transport use zoned spheres like this one, solved exactly with fractions, as their reference.

**The change of measure.** From a point $x$ on a floor, sample a direction with the cosine density $p_\omega = \cos\theta_x / \pi$ and let it hit a ceiling at the height $h$. At the hit point $y$ at the distance $d$, both cosines are $h / d$, so $p_A(y) = \frac{h}{\pi d} \cdot \frac{h}{d} \cdot \frac{1}{d^2} = \frac{h^2}{\pi d^4}$. With $d^2 = h^2 + \varrho^2$ for the distance $\varrho$ along the ceiling, $\int_0^\infty \frac{h^2}{\pi (h^2 + \varrho^2)^2}\, 2\pi\varrho\, d\varrho = 1$, as it must be: every ray up hits the ceiling.

**Counting techniques.** A path of length $k = 3$, with four vertices $x_0 x_1 x_2 x_3$, can be made in $5$ ways: $s = 0, 1, 2, 3, 4$ light vertices. For the path $L D D E$, all five have positive densities. For $L S D E$ with a point light and a pinhole camera, the technique $s = 0$ must hit the point light by chance, $s = 4$ must hit the pinhole by chance, and $s = 1$ and $s = 2$ must join the two halves at the specular vertex, where the BSDF is a delta. All four have zero density. Only $s = 3$, which follows the light through the specular bounce to the diffuse point and connects that point to the camera, carries the path. This is why caustics come from light tracing.

## Where it is used

- **Bidirectional methods.** [Bidirectional path tracing](/bidirectional-path-tracing/) defines its techniques and their MIS weights on path space; [vertex connection and merging](/vertex-connection-and-merging/) extends the space to include the merging of [photon mapping](/photon-mapping/).
- **Markov chain methods.** [Metropolis light transport](/metropolis-light-transport/) and its relatives run on path space, or on the random numbers that make paths.
- **Combining estimators.** [Multiple importance sampling](/multiple-importance-sampling/) needs all densities in the same measure, which the area-product measure provides.
- **Learning and reuse.** [Path guiding](/path-guiding/) learns densities for path vertices, and the path versions of [ReSTIR](/restir/) move whole paths between pixels with a change of variables in path space.
- **Analysis.** It shows which paths a method can sample at all, which explains why [light tracing](/light-tracing/) renders caustics that [path tracing](/path-tracing/) finds only by chance.

## References
