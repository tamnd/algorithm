---
tag: ZDD3HA
kind: algorithm
slug: iterated-conditional-modes
name: Iterated conditional modes
aliases:
- ICM
area: computer-vision/stereo-and-dense-reconstruction
level: intro
summary: Minimize an MRF energy by setting each variable in turn to its best label given its neighbors, until nothing changes. Fast, but it stops at a local minimum that depends on the order.
solves: [map-inference]
model: real-ram
complexity:
  vars: {n: the number of sites, m: the number of neighbor pairs, L: the number of labels, k: the number of sweeps}
  time: {worst: O(k L (n + m)), average: O(k L (n + m)), best: O(L (n + m))}
  space: {extra: O(n + m)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1986
  people: [Julian Besag]
  note: Besag proposed ICM as a fast deterministic way to restore images under a Markov random field prior, as an alternative to the stochastic relaxation of Geman and Geman.
prereqs: [markov-random-field, map-inference, local-search]
see_also: [gibbs-sampling, simulated-annealing, coordinate-descent, alpha-expansion, alpha-beta-swap, loopy-belief-propagation, potts-model, ising-model]
sources:
  - paper: doi:10.1111/j.2517-6161.1986.tb01412.x
    title: Julian Besag, On the statistical analysis of dirty pictures, Journal of the Royal Statistical Society Series B 48(3), 1986, 259-279 (the paper; the discussion follows)
    locator: the definition of iterated conditional modes as an approximation to the maximum a posteriori estimate, and its use for the restoration of images
  - paper: doi:10.1109/TPAMI.2007.70844
    title: Richard Szeliski, Ramin Zabih, Daniel Scharstein, Olga Veksler, Vladimir Kolmogorov, Aseem Agarwala, Marshall Tappen and Carsten Rother, A comparative study of energy minimization methods for Markov random fields with smoothness-based priors, IEEE Transactions on Pattern Analysis and Machine Intelligence 30(6), 2008, 1068-1080
    locator: ICM as the baseline of the comparison, and its energies against those of graph cuts, loopy belief propagation and TRW-S
  - paper: doi:10.1109/34.969114
    title: Yuri Boykov, Olga Veksler and Ramin Zabih, Fast approximate energy minimization via graph cuts, IEEE Transactions on Pattern Analysis and Machine Intelligence 23(11), 2001, 1222-1239
    locator: Section 3 (standard moves, which change one site at a time, against the large moves of swap and expansion)
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 4, Model fitting and optimization (Markov random fields and their inference)
---

Iterated conditional modes (ICM) is the simplest method to minimize the energy of a [Markov random field](/markov-random-field/), that is, to find an approximate [MAP labeling](/map-inference/). It visits the sites one at a time and gives each site the label of least cost given the current labels of its neighbors, which is the mode of the conditional distribution of that site. It repeats such sweeps until no site changes. Each change lowers the energy, so the method stops, at a labeling that no change of one site can improve. It is [coordinate descent](/coordinate-descent/) on a discrete problem and the zero temperature limit of [Gibbs sampling](/gibbs-sampling/). ICM is fast and needs no condition on the pairwise term, but the local minimum it finds depends on the start and the visiting order, and on vision energies it is usually far worse than [alpha-expansion](/alpha-expansion/) or [loopy belief propagation](/loopy-belief-propagation/).

## In plain words

Each pixel has a label, and it pays for a label that does not fit its data and for every neighbor that has a different label. Go over the pixels one by one. For each pixel, look at its neighbors as they are now, and give it the label that costs least. If no label is cheaper than the one it has, leave it. Go over the image again and again until a full pass changes nothing. The total cost goes down at every change, so the process always ends. But it can get stuck: sometimes two pixels would both have to change at once to make things better, and a pass that changes one pixel at a time never sees that.

## The problem

**Input.** Sites with neighbor pairs $\mathcal{N}$ and weights $w_{pq}$, $L$ labels, data costs $D_p(\ell)$, a pairwise table $V$, a start labeling $f$ and an order of the sites.

**Output.** A labeling $f$ that is a local minimum of

$$E(f) = \sum_p D_p(f_p) + \sum_{(p,q) \in \mathcal{N}} w_{pq}\, V(f_p, f_q)$$

for changes of one site: for every site $p$ and label $\ell$, the labeling with $f_p$ replaced by $\ell$ has energy at least $E(f)$. $V$ need not be symmetric, a metric or submodular.

## The algorithm

```pseudo id=main
ICM(D, V, N, f, order)
L1  repeat
L2      changed ← false
L3      for each site p in the fixed order do
L4          for each label ℓ: c(ℓ) ← D_p(ℓ) + Σ over the neighbors q of p of w_pq V(ℓ, f_q)
L5          ℓ* ← the least label with the least c(ℓ*)
L6          if c(ℓ*) < c(f_p) then f_p ← ℓ*; changed ← true
L7  until changed = false
L8  return f
```

Line L4 uses the labels of the neighbors as they are at that moment, so a site already sees the changes made earlier in the same sweep. Line L6 changes a site only on a strict improvement, which keeps the energy falling and avoids cycling between labels of equal cost. With an asymmetric $V$ the code uses $V(\ell, f_q)$ or $V(f_q, \ell)$ according to the order of the pair.

## Example

Restore a noisy binary row $y = (0, 1, 0, 0, 1, 1, 0, 1, 1, 1)$ with $D_p(\ell) = 2 [\ell \ne y_p]$ and the [Ising](/ising-model/) or Potts term $V(a, b) = 3 [a \ne b]$ on neighbors. Start from $f = y$, with $E = 5 \cdot 3 = 15$ for the five changes along the row.

| site | neighbors | $c(0)$ | $c(1)$ | action |
|---|---|---|---|---|
| 0 | $f_1 = 1$ | 3 | 2 | change to 1 |
| 1 | $f_0 = 1$, $f_2 = 0$ | 5 | 3 | keep 1 |
| 2 to 5 | | | | keep |
| 6 | $f_5 = 1$, $f_7 = 1$ | 6 | 2 | change to 1 |
| 7 to 9 | | | | keep |

After the first sweep $f = (1, 1, 0, 0, 1, 1, 1, 1, 1, 1)$ with $E = 2 + 2 + 2 \cdot 3 = 10$, and the second sweep changes nothing. The optimum is $(0, 0, 0, 0, 1, 1, 1, 1, 1, 1)$ with $E = 7$. To reach it from the result, sites 0 and 1 must both change to 0. Changing site 0 alone costs $c(0) - c(1) = 1$, and changing site 1 alone costs 2, so ICM is stuck. Visiting the sites in the reverse order, site 1 is visited while site 0 is still 0, it changes to 0, and ICM reaches the optimum $E = 7$.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). The key fact is that $c(\ell) - c(f_p)$ equals the change of the total energy when site $p$ alone takes label $\ell$, because all terms that do not touch $p$ cancel. So each change of line L6 lowers $E$ strictly. A labeling cannot repeat, there are finitely many labelings, and so the loop stops. In the last sweep nothing changed, so every site was checked against the final labeling and no single change lowers $E$.

## Complexity

The model is the real RAM.

- **One sweep.** Line L4 costs $O(L(1 + \deg p))$ for site $p$, so a sweep costs $O(L(n + m))$.
- **Number of sweeps.** With integer costs, each sweep except the last lowers the energy by at least 1, so $k \le E(f_0) - \min E + 1$. In general only $k \le L^n$ is known. On image energies a few sweeps usually suffice; this is an observation, not a bound.
- **Space.** $O(n + m)$ for the labeling and the neighbor lists.

## Properties

- **Monotone.** The energy never rises.
- **Local.** The output is a local minimum for changes of one site, the weakest of the usual notions. Local minima of [swap](/alpha-beta-swap/) and [expansion](/alpha-expansion/) are also ICM local minima, but not the other way.
- **Order and start dependent.** Different orders or starts give different results, as in the example.
- **No condition on $V$.** Any table works, which makes ICM a fallback for energies that no cut can handle.
- **Exact without pair terms.** If $V = 0$, one sweep gives the label of least data cost at each site, the global minimum.
- **No quality bound.** Its energy can be far above the optimum. In the benchmark of Szeliski et al. (2008) it was the weakest method on most energies.

## Variants and improvements

- **Better starts.** Start from the best data label, or from the output of a faster or coarser method.
- **Coding and checkerboard order.** Sites that are not neighbors can be updated in parallel. On a 4-connected grid, update all black squares, then all white squares; each half-sweep is still a valid ICM step.
- **Stochastic versions.** [Gibbs sampling](/gibbs-sampling/) draws the label from the conditional distribution instead of taking its mode, and [simulated annealing](/simulated-annealing/) lowers a temperature so that the method ends as ICM.
- **Block ICM.** Optimize a whole row or a small block at a time, exactly by dynamic programming on a chain. This escapes some of the traps of single sites.
- **Large moves.** [Alpha-expansion](/alpha-expansion/) and [alpha-beta swap](/alpha-beta-swap/) change many sites at once by a minimum cut, and are the usual replacement.

## When to use it

Use ICM as a baseline, to polish the output of another method, or when the energy has a pairwise term that no other method accepts and speed matters more than quality. For Potts or truncated linear terms, use [alpha-expansion](/alpha-expansion/); for general terms, [loopy belief propagation](/loopy-belief-propagation/) or TRW-S.

## Pitfalls

- **Synchronous updates.** Updating all sites at once from the old labeling is not ICM and can oscillate. Two neighbors with labels 0 and 1 and a strong Potts term swap their labels at each step forever. Update in place.
- **Ties.** Change a site only on a strict improvement, or the method can cycle between labels of equal energy.
- **Blaming the model.** When ICM gives a poor result, the cause can be the optimizer and not the energy. A small group of noisy sites can hold each other in place, as sites 0 and 1 do in the example. Compare with a method with large moves before you conclude that the model is bad.
- **Reading the result as MAP.** The result is a local minimum. Do not report it as the MAP estimate.

## Implementations

## History

Besag (1986) proposed ICM in his paper on the statistical analysis of "dirty pictures", as a fast deterministic alternative to the stochastic relaxation of Geman and Geman (1984), and used it to restore images under Markov random field priors. Its strict local moves were the motivation for the large moves of Boykov, Veksler and Zabih (2001). In the benchmark of Szeliski et al. (2008), ICM served as the baseline against which graph cuts, belief propagation and TRW-S were measured.

## References
