---
tag: RK8BNF
kind: concept
slug: energy-landscape
name: Energy landscape and folding funnel
aliases:
- Folding funnel
- Free energy landscape
area: biology/structure-prediction
level: advanced
summary: The energy of a molecule as a function of its conformation, with its minima, basins and barriers. A funnel-shaped landscape slopes toward the native state and explains fast folding.
prereqs: [levinthal-paradox, energy-function]
see_also: [hp-model, rna-folding-kinetics, local-optimum, fitness-landscape, simulated-annealing, parallel-tempering, partition-function, molecular-dynamics]
sources:
  - paper: doi:10.1002/prot.340210302
    title: Joseph D. Bryngelson, José Nelson Onuchic, Nicholas D. Socci and Peter G. Wolynes, Funnels, pathways, and the energy landscape of protein folding, a synthesis, Proteins 21(3), 1995, 167-195
    locator: the folding funnel, the principle of minimal frustration, and the folding and glass temperatures
  - paper: doi:10.1038/nsb0197-10
    title: Ken A. Dill and Hue Sun Chan, From Levinthal to pathways to funnels, Nature Structural Biology 4(1), 1997, 10-19
    locator: the pictures of smooth, rugged and funnel-shaped landscapes, and the parallel routes of folding
  - paper: doi:10.1002/pro.5560040401
    title: Ken A. Dill et al., Principles of protein folding, a perspective from simple exact models, Protein Science 4(4), 1995, 561-602
    locator: the landscapes of lattice models computed by exact enumeration
  - paper: doi:10.1073/pnas.89.1.20
    title: Robert Zwanzig, Attila Szabo and Biman Bagchi, Levinthal's paradox, PNAS 89(1), 1992, 20-22
    locator: the energy bias that makes the search short
---

An energy landscape is the energy of a molecule as a function of its conformation, seen as a surface over the space of conformations, together with its minima, basins and barriers. A folding funnel is a landscape that slopes toward the native state from most of the space, with only small bumps on the way. The funnel picture of Bryngelson, Onuchic, Socci and Wolynes (1995) and of Dill and Chan (1997) is the standard answer to [Levinthal's paradox](/levinthal-paradox/): the chain does not search a flat space, it goes downhill on many parallel routes. The landscape is also the object that every search algorithm for structure prediction explores.

## In plain words

Think of every possible shape of a protein chain as a point on a huge map, and give each point a height: its energy. Nearby points are shapes that differ by a small move. The result is a landscape of hills and valleys. The native shape is the lowest valley.

If the map were a flat plain with one small hole, a random walker would need forever to find the hole. A protein landscape looks more like a funnel: from almost everywhere the ground slopes down toward the native shape, so the chain falls toward it by many paths. The funnel walls are not smooth. Small dips can hold the chain for a while, and a bad landscape has deep side valleys that trap it. A search program on a computer faces the same hills and dips.

## The idea

**The landscape as a graph.** For a computer, a landscape is a triple $(\Omega, \mathcal{N}, E)$: a set $\Omega$ of conformations, a move set that gives each $x \in \Omega$ a set $\mathcal{N}(x)$ of neighbours, and an [energy function](/energy-function/) $E : \Omega \to \mathbb{R}$. The move set is part of the landscape. The same energy with a different move set has different minima.

- A conformation $x$ is a *local minimum* when $E(y) \ge E(x)$ for each $y \in \mathcal{N}(x)$. See [local optimum](/local-optimum/).
- The *basin* of a minimum is the set of conformations from which steepest descent ends at that minimum.
- The *barrier* from $x$ to $y$ is the smallest value, over all paths from $x$ to $y$ in the move graph, of the highest energy on the path, minus $E(x)$. At temperature $T$, the time to cross a barrier $B$ grows roughly as $e^{B/k_B T}$.

In a continuous model such as [molecular dynamics](/molecular-dynamics/), the minima are the points where $\nabla E = 0$ and the Hessian is positive definite, and the lowest saddle points of index one between two minima are the transition states.

**Energy and entropy.** Let $g(E)$ be the number of conformations of energy $E$, the density of states. The entropy of the energy level is $S(E) = k_B \ln g(E)$, and its free energy is

$$F(E) = E - T S(E).$$

At equilibrium the probability of the level $E$ is proportional to $e^{-F(E)/k_B T}$. At a high temperature the many conformations of high energy win, and the chain is unfolded. At a low temperature the native level wins. For a coarse picture, folding studies use an order parameter in place of $E$, often the fraction $Q$ of the native contacts that a conformation has, and plot $F(Q)$.

**The funnel.** A landscape is funnel-shaped when the energy falls, on average, as the conformation becomes more similar to the native one, so that $E$ and $Q$ are strongly correlated. Bryngelson and Wolynes call a sequence *minimally frustrated* when its native interactions are much more favourable than its non-native ones, so that few local interactions conflict with the native fold. For such a sequence, the folding temperature $T_f$, where the native state and the unfolded states are equally probable, is well above the glass temperature $T_g$, where the chain freezes into whichever deep minimum it reaches. Random sequences are frustrated: their landscapes are rugged, and their $T_g$ is close to or above $T_f$.

**Search.** A [local search](/local-search/) that only goes down stops at the first local minimum. Methods for rugged landscapes accept uphill moves: Metropolis Monte Carlo, [simulated annealing](/simulated-annealing/) and [parallel tempering](/parallel-tempering/). The barriers between basins decide how long they take. A [fitness landscape](/fitness-landscape/) in optimization and evolution is the same object with the sign reversed: there the search goes up.

## Examples

**An exact landscape in the HP model.** Take the sequence HPHPPHHPHH in the 2D [HP model](/hp-model/). Write a fold as a word over $\{L, S, R\}$ of length 8: the first bond points along $+x$, and each letter says whether the chain turns left, goes straight or turns right at the next residue. Of the $3^8 = 6561$ words, 4067 are self-avoiding. A move changes one letter, which rotates the rest of the chain about one residue (a pivot move). A fold has on average 13.0 valid neighbours out of 16.

| energy $E$ | 0 | $-1$ | $-2$ | $-3$ | $-4$ |
|---|---|---|---|---|---|
| folds $g(E)$ | 2323 | 1448 | 256 | 34 | 6 |
| local minima | 65 | 314 | 144 | 24 | 6 |

Only the 6 folds at $-4$ are global minima, so 547 folds are local minima that trap a descent. Steepest descent, which moves to the lowest neighbour until no neighbour is lower, taking the first word in alphabetical order when several neighbours tie, reaches $E = -4$ from only 617 of the 4067 folds, that is 15.2 percent. This toy landscape is rugged under pivot moves, so a search needs uphill moves or restarts.

**Energy against entropy.** With $k_B = 1$ and the contact energy as the unit, the free energies and the probabilities of the levels are:

| $T$ | $F(-4)$ | $F(-3)$ | $F(-2)$ | $F(-1)$ | $F(0)$ | probability of $E = -4$ |
|---|---|---|---|---|---|---|
| 0.25 | $-4.448$ | $-3.882$ | $-3.386$ | $-2.819$ | $-1.938$ | 0.893 |
| 0.41 | $-4.735$ | $-4.446$ | $-4.274$ | $-3.984$ | $-3.178$ | 0.500 |
| 1.00 | $-5.792$ | $-6.526$ | $-7.545$ | $-8.278$ | $-7.751$ | 0.036 |

At $T = 1$ the level $-1$ has the lowest free energy, because it has 1448 folds. Near $T = 0.41$ the native level holds half of the probability. This is the folding temperature of the toy chain.

**A longer chain.** For HHPPHPPHPPHH, with 12 residues, there are 30,073 self-avoiding words. The 2 words at the minimum $-5$ are one fold and its mirror image. Under pivot moves there are 3,905 local minima that are not global, and steepest descent reaches $-5$ from only 204 folds, 0.7 percent. A unique ground state does not make a funnel for this move set.

## Where it is used

- **Folding theory.** The funnel explains fast folding, the parallel routes seen in experiments, and why designed or natural sequences fold while most random sequences do not. See [Levinthal's paradox](/levinthal-paradox/).
- **RNA.** RNA secondary structures have a discrete landscape with a move set of adding or removing one base pair. Its minima and barriers can be computed exactly for short chains. See [RNA folding kinetics](/rna-folding-kinetics/).
- **Structure prediction.** [Fragment assembly](/fragment-assembly/) and [Rosetta](/rosetta/) explore the landscape of a coarse energy first, because it is smoother, and then the rugged landscape of an all-atom energy. The choice of moves changes the landscape, which is why fragment moves work better than random angle changes.
- **Simulation methods.** Parallel tempering, umbrella sampling and other methods for molecular simulation exist to cross the barriers of a landscape in a feasible time.
- **Optimization.** The same picture of basins, barriers and funnels is used to explain when [simulated annealing](/simulated-annealing/) and other [local search](/local-search/) methods work.

## References
