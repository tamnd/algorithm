---
tag: 8VMJTE
kind: concept
slug: levinthal-paradox
name: Levinthal's paradox
aliases:
- Levinthal paradox
area: biology/structure-prediction
level: intro
summary: A protein chain has so many conformations that a random search would take longer than the age of the universe, yet proteins fold in seconds or less, so folding must be a guided search.
prereqs: [thermodynamic-hypothesis, combinatorial-explosion]
see_also: [energy-landscape, protein-structure-prediction, ab-initio-protein-folding, hp-folding-np-completeness, birth-death-process, search-space, rna-folding-kinetics]
sources:
  - paper: "Cyrus Levinthal, How to fold graciously, in P. Debrunner, J. C. M. Tsibris and E. Münck (eds.), Mössbauer Spectroscopy in Biological Systems, Proceedings of a meeting held at Allerton House, Monticello, Illinois, University of Illinois Press, 1969, pages 22 to 24"
    title: How to fold graciously
    locator: the count of 10^300 configurations for a chain of 150 residues, the bound of about 10^8 trials in the folding time, and the proposal of folding by local nucleation
  - paper: "Cyrus Levinthal, Are there pathways for protein folding?, Journal de Chimie Physique 65, 1968, pages 44 to 45"
    title: Are there pathways for protein folding?
    locator: the argument that folding follows a pathway and is under kinetic control
  - paper: doi:10.1073/pnas.89.1.20
    title: Robert Zwanzig, Attila Szabo and Biman Bagchi, Levinthal's paradox, PNAS 89(1), 1992, 20-22
    locator: the model of independent residues with an energy bias of a few kT, which makes the search time biologically short
  - paper: doi:10.1038/nsb0197-10
    title: Ken A. Dill and Hue Sun Chan, From Levinthal to pathways to funnels, Nature Structural Biology 4(1), 1997, 10-19
    locator: the random search argument, the pathway view and the funnel view of folding
---

Levinthal's paradox is the observation that a protein cannot find its native structure by a random search over its conformations, because there are far too many, and yet proteins fold in seconds or less. Cyrus Levinthal made the argument in 1968 and 1969. It is not a contradiction: it shows that folding is a biased search, guided by the energy of the partial structures. The usual resolution is the [energy landscape](/energy-landscape/) with a funnel shape, and Zwanzig, Szabo and Bagchi (1992) showed with a simple model that a small bias is enough.

## In plain words

A protein chain can bend at each of its links, and each link has a few possible positions. The number of shapes of the whole chain is the product of the choices at each link, so it grows exponentially with the length. For a chain of a hundred links, the count is so large that trying one shape in each tiny fraction of a second would take far longer than the age of the universe. But real proteins reach their one correct shape in seconds or less.

So the chain does not try shapes at random. A link that reaches a good local position tends to stay there, because that position has a lower energy. Small advantages at each link add up, and they cut the search from impossible to fast.

## The idea

**Levinthal's numbers.** Levinthal (1969) took a protein of 150 residues with about 450 degrees of freedom: 300 rotations about backbone bonds and 150 bond angles. He wrote that even if these angles were known to better than a tenth of a radian, there would be $10^{300}$ possible configurations. A protein folds in a few seconds, so it "would have time to try on the order of $10^8$ different conformations at most". He concluded that folding is "speeded and guided by the rapid formation of local interactions". He also asked whether the native state must be the global minimum of free energy, or only a metastable state in a deep enough well.

**The textbook version.** Give each of $N$ residues $\nu$ states, of which one is correct. The chain has $\nu^N$ conformations. A blind search that tries conformations in random order, with no memory and no energy guidance, needs on average about $\nu^N$ trials, because each trial hits the native state with probability $\nu^{-N}$. For $N = 100$ and $\nu = 3$:

$$3^{100} \approx 5.15 \times 10^{47}.$$

At $10^{-13}$ s per trial, the search takes $5.15 \times 10^{34}$ s, which is about $1.6 \times 10^{27}$ years. The age of the universe is about $1.4 \times 10^{10}$ years.

**What is wrong with the blind search.** It gives each conformation the same weight, so the energy plays no role until the native state is hit. A real chain feels the energy at each step: a residue in a locally favourable state is more likely to stay there. The search is then over a landscape with a slope toward the native state, not over a flat set. This is a statement about the search, and it fits the [thermodynamic hypothesis](/thermodynamic-hypothesis/), which is about the end state.

**A biased search model.** Zwanzig, Szabo and Bagchi (1992) gave each residue an energy $U$ (in units of $k_B T$) when it is in one of its $\nu - 1$ incorrect states and energy 0 when it is correct. The residues are independent. Consider the version where one step picks a residue uniformly at random, proposes one of its other states uniformly at random, and accepts the move with the [Metropolis criterion](/metropolis-criterion/). Let $j$ be the number of incorrect residues. Then $j$ is a [birth-death process](/birth-death-process/): in one step it goes down with probability $d_j$ and up with probability $b_j$, where

$$d_j = \frac{j}{N} \cdot \frac{1}{\nu - 1}, \qquad b_j = \frac{N - j}{N} \, e^{-U}.$$

A move down picks an incorrect residue and proposes its correct state, and is always accepted. A move up picks a correct residue, always proposes an incorrect state, and is accepted with probability $e^{-U}$. Let $T_j$ be the expected number of steps to go from $j$ to $j - 1$ incorrect residues. A first-step analysis gives $T_j = 1 + (1 - b_j - d_j) T_j + b_j (T_{j+1} + T_j)$, because a step up must later come back down to $j$. Solve for $T_j$:

$$T_N = \frac{1}{d_N}, \qquad T_j = \frac{1 + b_j T_{j+1}}{d_j} \quad (1 \le j < N),$$

and the mean time from the fully wrong chain to the native state is $T_N + T_{N-1} + \cdots + T_1$. At equilibrium, the probability of the native state is $(1 + (\nu - 1) e^{-U})^{-N}$.

## Examples

For $N = 100$ and $\nu = 3$, the recurrence gives these mean first passage times, from the state with all residues incorrect:

| bias $U$ (in $k_B T$) | mean steps to the native state | time at $10^{-13}$ s per step | equilibrium probability of the native state |
|---|---|---|---|
| 0 | $5.18 \times 10^{47}$ | $5.2 \times 10^{34}$ s | $1.94 \times 10^{-48}$ |
| 1 | $2.45 \times 10^{24}$ | $2.5 \times 10^{11}$ s | $1.1 \times 10^{-24}$ |
| 2 | $1.95 \times 10^{11}$ | 0.019 s | $4.0 \times 10^{-11}$ |
| 3 | $3.03 \times 10^{5}$ | $3.0 \times 10^{-8}$ s | $7.5 \times 10^{-5}$ |
| 4 | 3,545 | $3.5 \times 10^{-10}$ s | 0.027 |
| 5 | 1,412 | $1.4 \times 10^{-10}$ s | 0.26 |

With no bias, the search time is close to the blind count $3^{100}$. A bias of $2 k_B T$ per residue brings it down to a fraction of a second, which is the conclusion of Zwanzig, Szabo and Bagchi: a bias of a few $k_B T$ against locally wrong states is enough. The last column shows a second point. In this model the native state is the most probable single conformation for each $U > 0$, but it is a stable majority only when the bias is large, because the unfolded side has many more conformations. Real proteins add cooperativity, which the independent model does not have, and which makes the native state stable at a smaller bias per residue.

The model is an illustration. The numbers depend on the move set and on the time per step, and they are not measured folding times.

## Where it is used

- **Energy landscape theory.** The paradox is the starting point of the funnel picture, in which the landscape slopes toward the native state. See [energy landscape](/energy-landscape/) and Dill and Chan (1997).
- **Structure prediction.** The same count shows why a program cannot enumerate conformations. [Ab initio](/ab-initio-protein-folding/) methods must bias their search, for example by [fragment assembly](/fragment-assembly/), which proposes local structures that are common in known proteins.
- **Complexity of folding.** [HP folding is NP-complete](/hp-folding-np-completeness/), but nature folds fast. Both statements hold, because the hardness is for the worst case over all sequences, while natural sequences are selected to have a funnel-shaped landscape.
- **Teaching.** It is a standard example of [combinatorial explosion](/combinatorial-explosion/) in a physical system. The same argument applies to RNA, where the [folding kinetics](/rna-folding-kinetics/) of a chain can be modelled exactly on small instances.

## References
