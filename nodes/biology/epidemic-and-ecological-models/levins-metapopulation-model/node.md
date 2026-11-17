---
tag: 73C1JM
kind: model
slug: levins-metapopulation-model
name: Levins metapopulation model
aliases:
- Levins model
area: biology/epidemic-and-ecological-models
level: core
summary: The fraction p of occupied habitat patches follows dp/dt = c p (1 - p) - e p, so the metapopulation persists only if c > e.
history:
  year: 1969
  people: [Richard Levins]
  note: Levins (1969) wrote the equation for the share of occupied patches in a study of the biological control of insect pests.
prereqs: [logistic-growth-model]
see_also: [sis-epidemic-model, basic-reproduction-number, metapopulation-epidemic-model, birth-death-process, markov-chain, percolation, competitive-exclusion-principle, lotka-volterra-competition]
sources:
  - paper: doi:10.1093/besa/15.3.237
    title: Richard Levins, Some demographic and genetic consequences of environmental heterogeneity for biological control, Bulletin of the Entomological Society of America 15(3), 1969
    locator: pages 237 to 240 (the equation for the fraction of occupied sites, with a rate of colonization and a rate of local extinction)
---

The Levins metapopulation model follows a species that lives in many separate patches of habitat. It does not count individuals. It counts only the fraction $p$ of the patches that are occupied. Occupied patches send out colonists that settle empty patches, at the rate $c\,p\,(1 - p)$, and each local population dies out at the rate $e$. The equation $\dot p = c p (1 - p) - e p$ is a [logistic equation](/logistic-growth-model/) in disguise. The species persists in the landscape if and only if $c > e$, and then the occupied fraction tends to $1 - e/c$, even though every local population is doomed.

## The machine

**The state.** $p(t) \in [0, 1]$ is the fraction of habitat patches that hold a population of the species at time $t$.

**The parameters.**

- $c > 0$, in 1 per time: the colonization rate. An empty patch becomes occupied at the rate $c p$, in proportion to the share of patches that send out colonists.
- $e > 0$, in 1 per time: the extinction rate of a local population. An occupied patch becomes empty at the rate $e$.

**The equation.**

$$\frac{dp}{dt} = c\,p\,(1 - p) - e\,p.$$

**The assumptions.**

- There are very many patches, all of the same quality, so $p$ is a continuous quantity.
- Every patch is equally close to every other patch: colonists from any occupied patch reach any empty patch with the same chance. There is no distance and no map.
- A patch is either empty or occupied. The size of a local population does not matter, and its growth to the local capacity is instant.
- Local extinctions are independent of each other and of the state. A drought that hits many patches at once is outside the model.
- Colonization of an occupied patch has no effect, so the gain is $c p$ times the empty share $1 - p$.

## What it counts

- The persistence threshold $c > e$, written also as $c / e > 1$.
- The equilibrium occupancy $p^* = 1 - e/c$.
- The time course $p(t)$, in closed form, and the time scale $1/(c - e)$ of the approach to $p^*$.
- The effect of the loss of habitat on $p^*$ and on persistence.
- In the version with a finite number of patches, the mean time until the whole metapopulation dies out.

**An example.** Take $c = 0.5$ and $e = 0.2$ per year. Then $c > e$, and $p^* = 1 - 0.2/0.5 = 0.6$: in the long run, 60 percent of the patches are occupied and 40 percent are empty at any time. The rate is $r = c - e = 0.3$ per year. From $p(0) = 0.05$:

| $t$ (years) | 0 | 5 | 10 | 20 | $\infty$ |
|---|---|---|---|---|---|
| $p(t)$ | 0.05 | 0.1737 | 0.3877 | 0.5841 | 0.6 |

The value at $t = 5$ is $0.6 / (1 + 11 e^{-1.5}) = 0.6 / 3.4544 = 0.1737$, from the closed form below.

## Relation to other models

- **[Logistic growth](/logistic-growth-model/).** The right side is $(c - e)\,p\,(1 - p/K)$ with $K = 1 - e/c$. So every result of the logistic model applies, with the growth rate $r = c - e$ and the capacity $K = 1 - e/c$.
- **[The SIS epidemic model](/sis-epidemic-model/).** Read the patches as hosts and the occupied patches as infected hosts. Then $c$ is the transmission rate, $e$ the recovery rate, and the equation is the SIS model $\dot i = \beta i (1 - i) - \gamma i$. The threshold $c/e$ is the [basic reproduction number](/basic-reproduction-number/) $R_0$: the number of new patches that one occupied patch colonizes during its life, when all other patches are empty. The equilibrium is $p^* = 1 - 1/R_0$, as for the endemic level of an SIS infection.
- **Finite numbers of patches.** With $n$ patches, the number of occupied patches is a [birth-death process](/birth-death-process/), a continuous-time [Markov chain](/markov-chain/) on $\{0, 1, \ldots, n\}$ with the birth rate $c k (n - k)/n$ and the death rate $e k$ in state $k$. The Levins equation is its limit for large $n$.
- **Maps of patches.** If colonists can reach only nearby patches, as in a contact process on a lattice, the threshold is higher than $c > e$, because colonists often land on patches that are already occupied near their source. The [percolation](/percolation/) page covers the related geometric threshold.
- **[Metapopulation epidemic models](/metapopulation-epidemic-model/).** These couple local epidemic models in patches by travel between patches. The Levins model is the simplest case, in which each patch is only on or off.
- **[Competition](/lotka-volterra-competition/).** With two species, the patch version of competition lets a weak competitor that colonizes fast persist next to a strong one; see the results below and the [competitive exclusion principle](/competitive-exclusion-principle/).

## Known results in the model

**The closed form.** For $c \ne e$ and $p(0) = p_0 > 0$, with $r = c - e$ and $K = 1 - e/c$,

$$p(t) = \frac{K}{1 + (K/p_0 - 1)\,e^{-r t}}.$$

*Proof.* $c p (1 - p) - e p = (c - e) p - c p^2 = r p (1 - p / K)$, since $c / r = 1/K$. This is the logistic equation, and the formula is its solution. $\square$

**The threshold.** If $c > e$, every solution with $p_0 > 0$ tends to $p^* = 1 - e/c$, and the approach is like $e^{-(c - e) t}$ near the end. If $c < e$, every solution tends to $0$ like $e^{-(e - c) t}$. If $c = e$, then $\dot p = -c p^2$ and $p(t) = p_0 / (1 + c p_0 t)$, which tends to $0$ slowly.

*Proof.* For $c > e$, $K \in (0, 1)$ and $r > 0$, so the closed form tends to $K$. For $c < e$, both $r < 0$ and $K < 0$, and the closed form is $p(t) = |K| p_0 e^{r t} / (|K| + p_0 (1 - e^{r t}))$, which tends to $0$ at the rate $e^{r t}$. For $c = e$, the equation $\dot p = -c p^2$ is separable. $\square$

So the metapopulation persists only if a patch, during its expected life $1/e$, colonizes on average more than one patch when the landscape is empty: $c \cdot (1/e) > 1$.

**The share of empty patches is fixed.** At equilibrium, the empty share is $1 - p^* = e/c$, which does not depend on how the patches were filled at the start. A species that colonizes well (large $c$) leaves few patches empty.

**Loss of habitat.** Destroy a fraction $D$ of the patches for good. Colonists that land on a destroyed patch are lost, so the equation becomes

$$\frac{dp}{dt} = c\,p\,(1 - D - p) - e\,p,$$

with the equilibrium $p^* = 1 - D - e/c$. The species dies out in the whole landscape when $D \ge 1 - e/c$, although a fraction $1 - D > 0$ of the habitat is left. With $c = 0.5$ and $e = 0.2$, the loss of $D = 0.3$ halves $p^*$ from $0.6$ to $0.3$, and the loss of $D = 0.6$ causes extinction, with 40 percent of the habitat still present. The good patches that are empty make up the share $1 - D - p^* = e/c$ of all patches, as before the loss: the number of empty good patches stays the same, and the loss comes out of the occupied ones.

*Proof.* The same algebra as above, with $1 - D$ in place of $1$: $r = c(1 - D) - e$ and $K = 1 - D - e/c$. The species persists if and only if $r > 0$. $\square$

**Coexistence of a good competitor and a good colonizer.** Let species 1 be the better competitor: it takes over patches of species 2 and is not affected by it. Let both species have the extinction rate $e$, and let $c_1$ and $c_2$ be their colonization rates. Then

$$\dot p_1 = c_1 p_1 (1 - p_1) - e p_1, \qquad \dot p_2 = c_2 p_2 (1 - p_1 - p_2) - e p_2 - c_1 p_1 p_2.$$

Species 1 alone settles at $p_1^* = 1 - e/c_1$. Species 2 can invade, and so persist, if and only if $c_2 > c_1^2 / e$.

*Proof.* Species 1 does not see species 2, so $p_1 \to p_1^*$. When $p_2$ is small, its per capita growth is $c_2 (1 - p_1^*) - e - c_1 p_1^* = c_2 e / c_1 - e - (c_1 - e) = c_2 e / c_1 - c_1$, which is positive if and only if $c_2 > c_1^2 / e$. $\square$

With $c_1 = 0.5$ and $e = 0.2$, species 2 needs $c_2 > 1.25$, two and a half times the colonization rate of species 1. So in a patchy landscape, two species that compete for the same patches can coexist, which they cannot do in one well-mixed habitat.

**A finite number of patches dies out.** With $n$ patches, the chain above reaches the state $0$ with probability $1$ from every start, whatever $c$ and $e$ are.

*Proof.* From every state $k \ge 1$, the chain can go to $0$ by $k$ extinctions in a row, with a probability of at least some $q > 0$ that does not depend on $k$ or on the time. The state $0$ is absorbing, because no occupied patch is left to send colonists. A finite chain in which the absorbing state can be reached from every state with a probability of at least $q$ in a bounded number of steps is absorbed with probability $1$, because the chance to avoid it for $m$ such rounds is at most $(1 - q)^m$. $\square$

The time to extinction is long when $c > e$. The mean time, from $k = 0.6\,n$ occupied patches with $c = 0.5$ and $e = 0.2$, comes from the linear equations $(\lambda_k + \mu_k)\tau_k - \lambda_k \tau_{k+1} - \mu_k \tau_{k-1} = 1$ with $\tau_0 = 0$:

| patches $n$ | 10 | 20 | 40 | 80 |
|---|---|---|---|---|
| mean time to extinction (years) | 130.7 | 2023 | $7.34 \times 10^5$ | $1.57 \times 10^{11}$ |

The time grows exponentially in $n$. Between $n = 40$ and $n = 80$ its logarithm grows by $0.307$ per patch, close to the value $\ln R_0 - 1 + 1/R_0 = 0.316$ for $R_0 = c/e = 2.5$ that a large-$n$ estimate of this chain gives. So for many patches above the threshold the Levins equilibrium is a good description for a very long time, and below the threshold the extinction is fast.

## References
