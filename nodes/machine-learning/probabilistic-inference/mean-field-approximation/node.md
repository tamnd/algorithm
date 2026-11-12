---
tag: 0P6CAT
kind: algorithm
slug: mean-field-approximation
name: Mean-field approximation
aliases:
- naive mean field
- mean-field variational inference
- naive mean-field updates
area: machine-learning/probabilistic-inference
level: advanced
summary: "Fit a fully factorized q to a Markov random field by coordinate ascent. Each update raises a lower bound on log Z. q seeks one mode, since it minimizes KL(q || p)."
solves: [marginal-inference, partition-function-computation]
model: real-ram
complexity:
  vars: {n: the number of variables, e: the number of edges, t: the number of sweeps}
  time: {worst: "O(t (n + e))"}
  space: {extra: "O(n + e)"}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1907
  people: [Pierre Weiss]
  note: Weiss's molecular field theory of ferromagnetism (1907) replaces the neighbors of a spin by their mean. Peterson and Anderson (1987) used it for Boltzmann machines, and Jordan, Ghahramani, Jaakkola and Saul (1999) placed it in the variational framework.
prereqs: [variational-inference, markov-random-field, partition-function]
see_also: [evidence-lower-bound, ising-model, loopy-belief-propagation, bethe-free-energy, tree-reweighted-belief-propagation, gibbs-sampling, coordinate-descent, potts-model]
sources:
  - paper: doi:10.1561/2200000001
    title: "Martin J. Wainwright and Michael I. Jordan, Graphical models, exponential families, and variational inference, Foundations and Trends in Machine Learning 1(1-2), 2008"
    locator: "Chapter 5 (mean field methods: the lower bound on the log partition function, the naive mean field updates for the Ising model, and the nonconvexity of the mean field problem)"
  - book: isbn:9780262013192
    title: Daphne Koller and Nir Friedman, Probabilistic Graphical Models, MIT Press, 2009
    locator: "Section 11.5 (structured variational approximations, with the mean field approximation and its coordinate ascent updates)"
  - book: isbn:9780521642989
    title: David J. C. MacKay, Information Theory, Inference, and Learning Algorithms, Cambridge University Press, 2003
    locator: "Chapter 33 (variational methods: variational free energy minimization and mean field theory for the Ising model)"
  - paper: doi:10.1023/A:1007665907178
    title: "Michael I. Jordan, Zoubin Ghahramani, Tommi S. Jaakkola and Lawrence K. Saul, An introduction to variational methods for graphical models, Machine Learning 37(2), 1999"
    locator: "the block approach and the mean field approximation for Boltzmann machines"
  - paper: "Carsten Peterson and James R. Anderson, A mean field theory learning algorithm for neural networks, Complex Systems 1(5), 1987, pages 995 to 1019"
    title: Peterson and Anderson 1987
    locator: mean field equations m_i = tanh(sum_j w_ij m_j) in place of sampling for Boltzmann machine learning
  - paper: "Pierre Weiss, L'hypothese du champ moleculaire et la propriete ferromagnetique, Journal de Physique Theorique et Appliquee 6(1), 1907, pages 661 to 690"
    title: Weiss 1907
    locator: the molecular field hypothesis
---

The mean-field approximation replaces a distribution $p$ over many variables, for example a [Markov random field](/markov-random-field/), by the closest fully factorized distribution $q(s) = \prod_i q_i(s_i)$, where "closest" means the smallest $\mathrm{KL}(q \,\|\, p)$. It finds $q$ by coordinate ascent: each update sets one factor $q_i$ to its best value given the others, and raises a lower bound on the log [partition function](/partition-function/). The result gives approximate marginals and a lower bound on $\log Z$. It is the simplest case of [variational inference](/variational-inference/); it has no guarantee of finding the best factorized $q$, and because it minimizes $\mathrm{KL}(q \,\|\, p)$ it tends to lock onto one mode of $p$.

## In plain words

In a magnet, each small magnet feels the pull of its neighbors, and the neighbors feel its pull in turn. To work out the exact behavior you must track every combination at once, which is too much work for a large system.

Mean field makes one simple guess: each small magnet reacts only to the average pull of its neighbors, not to their exact states. You keep one number per magnet, its average direction. You visit the magnets one at a time and set each number to the best reply to the current averages of its neighbors. You repeat until nothing changes.

Each visit makes a score better, and the score is a guaranteed underestimate of a hard quantity of the model. The answer can still be wrong: when the true system is equally likely to point up or down, mean field picks one side.

## The problem

**The model.** An [Ising model](/ising-model/) on a graph with $n$ spins $s_i \in \{-1, +1\}$ and $e$ edges:

$$p(s) = \frac{1}{Z} \exp\Bigl(\sum_i h_i s_i + \sum_{(i, j) \in E} J_{ij} s_i s_j\Bigr), \qquad Z = \sum_{s} \exp\Bigl(\sum_i h_i s_i + \sum_{(i, j) \in E} J_{ij} s_i s_j\Bigr).$$

The queries are the marginals $p(s_i)$, written by the means $\mathbb{E}_p[s_i]$, and $\log Z$. Both are #P-hard to compute exactly in general. The method extends to any [pairwise](/markov-random-field/) or [Potts](/potts-model/) model; the Ising case shows all its parts.

**The family.** A fully factorized $q(s) = \prod_i q_i(s_i)$ is fixed by the means $m_i = \mathbb{E}_q[s_i] \in [-1, 1]$, with $q_i(s_i = \pm 1) = (1 \pm m_i)/2$.

**The objective.** Under $q$ the spins are independent, so $\mathbb{E}_q[s_i s_j] = m_i m_j$. The [evidence lower bound](/evidence-lower-bound/) for the unnormalized model is

$$L(m) = \sum_i h_i m_i + \sum_{(i, j) \in E} J_{ij} m_i m_j + \sum_i H_b(m_i), \qquad H_b(m) = -\tfrac{1+m}{2} \log \tfrac{1+m}{2} - \tfrac{1-m}{2} \log \tfrac{1-m}{2},$$

and $\log Z = L(m) + \mathrm{KL}(q \,\|\, p)$. So $L(m) \le \log Z$ for every $m$, and to maximize $L$ is to minimize $\mathrm{KL}(q \,\|\, p)$ over the family.

## The algorithm

```pseudo id=main
MEAN-FIELD(h, J, m, ε, T)                  ▷ m: initial means in [−1, 1]^n
L1  for t ← 1 to T do
L2      δ ← 0
L3      for i ← 1 to n do                   ▷ sequential: use the newest m_j
L4          new ← tanh(h_i + Σ_{j ∈ N(i)} J_ij m_j)
L5          δ ← max(δ, |new − m_i|);  m_i ← new
L6      if δ < ε then break
L7  return m and L(m)
```

Line L4 is the general CAVI rule $q_i \propto \exp(\mathbb{E}_{-i}[\log p])$ for a spin: $\mathbb{E}_{-i}[\log \tilde p(s)] = s_i (h_i + \sum_j J_{ij} m_j) + \text{const}$, so $q_i(s_i) \propto \exp(s_i \phi_i)$ with the *mean field* $\phi_i = h_i + \sum_j J_{ij} m_j$, and its mean is $\tanh \phi_i$. A start at $m = 0$ is common, but $m = 0$ is a fixed point when all $h_i = 0$, so a symmetric model needs a random start.

## Example

**Two spins.** Take $h_1 = h_2 = 0$ and $J_{12} = 2$. Exactly, $Z = 2e^2 + 2e^{-2}$, so $\log Z \approx 2.7113$, and both exact means are 0 by symmetry. Start from $m = (0, 0.1)$, where $L = 1.3813$:

| update | $m_1$ | $m_2$ | $L(m)$ |
|---|---|---|---|
| $i = 1$ | 0.1974 | 0.1 | 1.4012 |
| $i = 2$ | 0.1974 | 0.3754 | 1.4427 |
| $i = 1$ | 0.6357 | 0.3754 | 1.5729 |
| $i = 2$ | 0.6357 | 0.8542 | 1.8217 |
| $i = 1$ | 0.9364 | 0.8542 | 2.0017 |
| $i = 2$ | 0.9364 | 0.9539 | 2.0371 |
| $i = 1$ | 0.9569 | 0.9539 | 2.0393 |

The run converges to $m_1 = m_2 \approx 0.9575$, the positive root of $m = \tanh(2m)$, with $L \approx 2.0393$. The bound is below $\log Z$ by $\mathrm{KL}(q \,\|\, p) \approx 0.6720$. The exact distribution puts mass $e^2 / Z \approx 0.4955$ on each of $(+,+)$ and $(-,-)$; $q$ covers only the first one. A start with $m_2 = -0.1$ gives the mirror solution. The point $m = 0$ is also a fixed point, with $L = 2 \log 2 \approx 1.3863$, which is worse.

**A loop with fields.** On the 4-cycle $1 - 2 - 4 - 3 - 1$ with $J_{ij} = 0.5$ on each edge and $h = (0.3, -0.2, 0.1, 0)$, mean field from $m = 0$ converges in 44 sweeps (with $\varepsilon = 10^{-10}$) to $m \approx (0.617, 0.297, 0.542, 0.397)$ with $L \approx 2.8922$. Enumeration of the 16 states gives $\log Z \approx 3.3433$ and exact means $(0.242, -0.004, 0.176, 0.066)$. Mean field overestimates the order: spin 2 has a negative field and an exact mean near 0, but its neighbors pull it to $0.297$.

## Correctness

Three facts hold for any Ising model and any start. The full proofs are in the correctness proof.

- **The bound.** $L(m) = \mathbb{E}_q[\log \tilde p] + H(q)$ with $\tilde p = Z p$, so $\log Z - L(m) = \mathrm{KL}(q \,\|\, p) \ge 0$.
- **Monotone ascent.** As a function of $m_i$ alone, $L$ is a linear term plus $H_b(m_i)$. Since $H_b''(m) = -1/(1 - m^2) \le -1$, $L$ is strictly concave in $m_i$, and its derivative $\phi_i - \operatorname{artanh}(m_i)$ is 0 exactly at $m_i = \tanh \phi_i$. So line L4 is the unique maximizer in $m_i$, and $L$ rises by at least $\frac12 (\text{new} - m_i)^2$.
- **Termination.** The rises add up to at most $\log Z - L(m^{(0)})$. So at most $2 (\log Z - L(m^{(0)})) / \varepsilon^2$ updates move a coordinate by $\varepsilon$ or more, and line L6 stops the loop after at most that many sweeps plus one. At the end, each $m_i$ differs from $\tanh \phi_i$ by at most $\varepsilon \sum_j |J_{ij}|$.

What does not hold: $L$ is not concave in $m$ as a whole, so the fixed point can be a local maximum or a saddle, and different starts give different answers (the two-spin example has three fixed points).

## Complexity

In the [real RAM](/real-ram/) model, line L4 costs $O(\deg(i))$, so a sweep costs $O(n + e)$ and $t$ sweeps cost $O(t(n + e))$. Memory is $O(n + e)$ for the graph and the means. The number of sweeps has the worst case bound $1 + 2(\log Z - L(m^{(0)}))/\varepsilon^2$ from the termination argument, which is weak; in practice it depends on the coupling strength. Near a phase transition it is large: the two-spin model with $J_{12} = 1$, which is the critical value for $m = \tanh(J m)$, did not reach $\varepsilon = 10^{-10}$ in 10000 sweeps, because the iteration approaches $m = 0$ only polynomially fast there.

For a general pairwise model with $k$ states per variable, $q_i$ is a vector of $k$ probabilities, line L4 becomes $q_i(a) \propto \exp(\theta_i(a) + \sum_j \sum_b \theta_{ij}(a, b) q_j(b))$, and a sweep costs $O(k^2 e + k n)$.

## Properties

- **Lower bound on $\log Z$.** At any $m$, not only at convergence.
- **Mode seeking.** $\mathrm{KL}(q \,\|\, p)$ is infinite if $q$ puts mass where $p$ has none, and it is cheap for $q$ to miss a mode of $p$. So $q$ fits one mode. On the 4-cycle with $J = 1$ and no field, 20 random starts all ended at all four means above 0.9 in absolute value with a common sign, both signs occurred, and the exact means are all 0.
- **Overconfident marginals.** The factorized $q$ ignores the correlations that the couplings create, and the means are often too large in absolute value, as in the 4-cycle example.
- **Exact without couplings.** If all $J_{ij} = 0$, then $p$ is itself factorized, line L4 gives $m_i = \tanh h_i$ at once, and $L = \log Z$.
- **Deterministic** for a fixed start and order.

## Variants and improvements

- **Structured mean field.** Let $q$ factor over trees or chains instead of single variables. Each block update runs exact inference on the block, and the bound is tighter, because the family is larger.
- **Damped or parallel updates.** Updating all spins at the same time from the old means can oscillate (see the pitfalls); damping $m \leftarrow (1-\lambda)\tanh(\phi) + \lambda m$ helps, but only the sequential version has the monotone guarantee.
- **TAP and higher-order corrections.** The Thouless-Anderson-Palmer equations add an Onsager reaction term $-m_i \sum_j J_{ij}^2 (1 - m_j^2)$ to the mean field $\phi_i$. They are more accurate at weak coupling but lose the bound.
- **Other approximations.** [Loopy belief propagation](/loopy-belief-propagation/) uses pairwise beliefs and the [Bethe free energy](/bethe-free-energy/); it is often more accurate but gives no bound. [Tree-reweighted belief propagation](/tree-reweighted-belief-propagation/) gives an upper bound on $\log Z$, so with mean field it brackets $\log Z$. [Gibbs sampling](/gibbs-sampling/) uses the same local conditional, but samples $s_i$ from it instead of averaging.

## When to use it

Use mean field when you need a fast approximation of the marginals of a large model, a guaranteed lower bound on $\log Z$, or a step inside a larger learning loop where speed matters more than accuracy. Prefer loopy BP or sampling when the couplings are strong, when the marginals must be calibrated, or when $p$ has several important modes.

## Pitfalls

- **Parallel updates.** With $h = 0$ and $J_{12} = -2$, the parallel update from $m = (0.5, 0.5)$ goes to $(-0.762, -0.762)$, then $(0.909, 0.909)$, and swings between $\pm(0.9575, 0.9575)$ forever. The sequential update from the same start converges to $(-0.9575, 0.9575)$.
- **The symmetric start.** With zero fields, $m = 0$ is a fixed point, and a run from $m = 0$ never leaves it, even when it is a poor saddle. Start at random.
- **Reading $q$ as calibrated.** The means are often too far from 0, and the KL direction hides other modes.
- **Comparing $L$ across models.** $L$ is a bound with a gap that depends on the model; a larger $L$ does not prove a larger $\log Z$.
- **Underflow in $H_b$.** At $m = \pm 1$ use $0 \log 0 = 0$.

## Implementations

## History

Weiss introduced the molecular field, the ancestor of mean field theory, in 1907 to explain ferromagnetism. Peterson and Anderson in 1987 used the mean field equations in place of slow sampling to train Boltzmann machines. Jordan, Ghahramani, Jaakkola and Saul in 1999 presented mean field as the simplest member of a general class of variational methods for graphical models, and Wainwright and Jordan in 2008 described it as the optimization over a nonconvex inner approximation of the marginal polytope.

## References
