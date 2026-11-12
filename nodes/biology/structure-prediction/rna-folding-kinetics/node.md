---
tag: ZN8CDJ
kind: problem
slug: rna-folding-kinetics
name: RNA folding kinetics
aliases:
- RNA folding pathways
- RNA folding dynamics
- Kinfold simulation
area: biology/structure-prediction
level: research
summary: Model the time course of RNA folding through intermediate structures.
prereqs: [nearest-neighbor-model, markov-chain, detailed-balance]
see_also: [stationary-distribution, metropolis-hastings, energy-landscape, mccaskill-algorithm, rna-secondary-structure-prediction, rna-inverse-folding, simulated-annealing, local-search]
sources:
  - paper: doi:10.1017/S1355838200992161
    title: Christoph Flamm, Walter Fontana, Ivo L. Hofacker and Peter Schuster, RNA folding at elementary step resolution, RNA 6(3), 2000, pages 325 to 338
    locator: the Kinfold program, the move set of single base pair moves, the Metropolis and Kawasaki rates, and the stochastic simulation
  - paper: doi:10.1524/zpch.2002.216.2.155
    title: Christoph Flamm, Ivo L. Hofacker, Peter F. Stadler and Michael T. Wolfinger, Barrier trees of degenerate landscapes, Zeitschrift für Physikalische Chemie 216(2), 2002, pages 155 to 173
    locator: barrier trees by flooding the landscape in order of energy, with degenerate energies
  - paper: doi:10.1088/0305-4470/37/17/005
    title: Michael T. Wolfinger, W. Andreas Svrcek-Seiler, Christoph Flamm, Ivo L. Hofacker and Peter F. Stadler, Efficient computation of RNA folding dynamics, Journal of Physics A 37(17), 2004, pages 4731 to 4741
    locator: the coarse-grained master equation on the basins of a barrier tree (treekin)
  - paper: doi:10.1021/j100540a008
    title: Daniel T. Gillespie, Exact stochastic simulation of coupled chemical reactions, Journal of Physical Chemistry 81(25), 1977, pages 2340 to 2361
    locator: the stochastic simulation algorithm for a continuous-time Markov chain
  - paper: "Ján Maňuch, Chris Thachuk, Ladislav Stacho and Anne Condon, NP-completeness of the energy barrier problem without pseudoknots and temporary arcs, Natural Computing 10(1), 2011, pages 391 to 405"
    title: NP-completeness of the energy barrier problem without pseudoknots and temporary arcs
    locator: hardness of the lowest barrier over direct paths between two structures, in a simple base pair energy model
---

RNA folding kinetics asks how an RNA strand moves from one structure to another in time, not only which [secondary structure](/rna-secondary-structure/) has the lowest energy. The standard model is a continuous-time [Markov chain](/markov-chain/) on the set of all secondary structures of the sequence: each step adds or removes one base pair, and the rate of a step depends on the change of energy in the [nearest-neighbor model](/nearest-neighbor-model/). The Kinfold program of Flamm, Fontana, Hofacker and Schuster (2000) simulates this chain with the stochastic simulation algorithm of Gillespie. Barrier trees (Flamm and others 2002) summarize the landscape by its local minima and the energy of the lowest saddle between them. The rates satisfy [detailed balance](/detailed-balance/), so at long times the chain reaches the Boltzmann distribution that the [McCaskill algorithm](/mccaskill-algorithm/) computes.

## In plain words

An RNA does not jump straight into its best fold. It forms and breaks one pair at a time, many millions of times each second. Each change that lowers the energy happens fast, and each change that raises it happens more slowly, the more so the larger the rise. So the molecule can get stuck in a fold that is good but not the best, behind a hill that it must climb to escape.

The kinetics problem asks how likely each fold is at each time, how long the molecule needs to reach the best fold, and how high the hills between good folds are. We can answer by simulating many random walks over the folds, or, for short strands, by exact calculation over all folds.

## Definition

**The model.** Fix a sequence $s = s_1 \cdots s_n$ over $\{A, C, G, U\}$, allowed pairs AU, GC and GU, a hairpin minimum $\theta = 3$, no pseudoknots, and an energy $E(P)$ for each secondary structure $P$. Kinfold uses the nearest-neighbor energies of the Vienna RNA package; the code on this page uses the integer model $E(P) = a\, |P| - b\, \sigma(P)$, where $\sigma(P)$ is the number of stacked pairs $(i, j)$ with $(i + 1, j - 1) \in P$, and $a = 1$, $b = 3$.

**States and moves.** The states are the secondary structures $\Omega(s)$. A move adds one allowed pair to $P$, if the result is still a secondary structure, or removes one pair. The move set is symmetric: $Q$ is a neighbor of $P$ if and only if $P$ is a neighbor of $Q$.

**Rates.** With $\beta = 1/RT$ and $\Delta = E(Q) - E(P)$ for a move from $P$ to $Q$, the Metropolis rate is

$$k(P \to Q) = k_0 \min(1, e^{-\beta \Delta}),$$

and the Kawasaki rate is $k_0\, e^{-\beta \Delta / 2}$. The constant $k_0$ sets the unit of time. Both rules give $e^{-\beta E(P)}\, k(P \to Q) = e^{-\beta E(Q)}\, k(Q \to P)$, which is detailed balance with respect to the Boltzmann weights.

**The master equation.** Let $p(t)$ be the row vector of the probabilities of the states at time $t$, and $\mathbf{Q}$ the generator with $\mathbf{Q}_{PQ} = k(P \to Q)$ for $P \ne Q$ and $\mathbf{Q}_{PP} = -\sum_{Q \ne P} k(P \to Q)$. Then $dp/dt = p\, \mathbf{Q}$ and $p(t) = p(0)\, e^{t \mathbf{Q}}$. Since the move graph is connected (each structure reaches the open chain by removing pairs) and detailed balance holds, the unique [stationary distribution](/stationary-distribution/) is $\pi(P) = e^{-\beta E(P)} / Z$.

**The questions.**

- **Occupancy.** Given $p(0)$, usually the open chain, and a time $t$, compute $p(t)$, or the probability of a target structure at time $t$.
- **First passage.** The expected time $\tau(P)$ to reach a target $T$ from $P$. It solves the linear system $\sum_{Q} k(P \to Q) (\tau(P) - \tau(Q)) = 1$ for $P \ne T$, with $\tau(T) = 0$.
- **Barriers.** For two structures $A$ and $B$, the saddle energy is the smallest $h$ such that a path of moves from $A$ to $B$ has all energies at most $h$. The barrier of a local minimum $A$ is the saddle energy to the nearest structure of lower energy, minus $E(A)$.

**Cost model.** Time on the [word RAM](/word-ram/) as a function of $n$ and of the number of states $N = |\Omega(s)|$. The number $N$ grows exponentially in $n$, about as $2.29^n$ for $\theta = 3$ when any two bases can pair (see [RNA secondary structure](/rna-secondary-structure/)).

## Variants

- **Shift moves.** Kinfold can also move one end of a pair to another base in one step. This joins states that would otherwise need a pair to be broken first.
- **Helix moves.** Coarser models add or remove whole helices, which gives fewer states and larger steps.
- **Co-transcriptional folding.** The chain grows from its $5'$ end at the speed of transcription, and folds while it grows, so the first structures to form can trap the molecule.
- **Coarse graining.** The states are grouped into the basins of the local minima of a barrier tree, and the master equation is solved on the basins (treekin, Wolfinger and others 2004).
- **Direct paths.** Paths that only remove pairs of $A$ and add pairs of $B$. The lowest barrier over these paths is NP-hard to find, even in a simple base pair energy model (Maňuch, Thachuk, Stacho and Condon 2011), so programs such as findpath use heuristics.
- **Temperature and ligands.** Changing $\beta$ or adding a bonus for a structure that binds a ligand changes the rates and models riboswitches.

## Examples

Take $s = $ GGGAAACCC ($n = 9$), the integer model with $a = 1$ and $b = 3$, and Metropolis rates with $k_0 = 1$ and $e^{-\beta} = 1/2$, so that a move up by $\Delta$ has rate $2^{-\Delta}$.

- **States.** The sequence has $N = 20$ secondary structures: the open chain (energy 0), nine structures with one pair (energy $+1$), nine with two pairs (energy $-1$ for the four stacked pairs, $+2$ for the five unstacked ones), and (((...))) with energy $-3$.
- **Equilibrium.** $Z = \sum_P 2^{-E(P)} = 91/4$, and the stationary distribution, found by an exact solve of $\pi \mathbf{Q} = 0$, is $2^{-E(P)}/Z$. The structure (((...))) has probability $32/91 \approx 0.352$, each two-pair stack $8/91$, and the open chain $4/91$.
- **Barrier tree.** The local minima are (((...))) at $-3$, ((....)). and .((....)) at $-1$, and the open chain at $0$. All three merge with the basin of (((...))) at saddle energy $+1$, because each path between them passes through a structure with one lone pair. So the two shifted hairpins have a barrier of 2, and the open chain a barrier of 1.
- **Folding time.** The exact mean first passage time from the open chain to (((...))) is $11375/929 \approx 12.24$ time units. The mean of 2000 Gillespie runs with seed 7 is $12.25$.

## Known algorithms

- **Stochastic simulation (Kinfold).** From the current structure $P$, list its neighbors and their rates, draw the waiting time from an exponential distribution with the total rate $K(P)$, and pick a neighbor with probability proportional to its rate (Gillespie 1977). Each step lists $O(n^2)$ candidate pairs in the worst case; Kinfold updates the energies of the neighbors locally. The number of steps to reach equilibrium can be exponential in $n$ when the landscape has high barriers. Averages over many runs estimate $p(t)$ and first passage times, with a statistical error that falls as one over the square root of the number of runs.
- **Exact master equation.** For small $N$, build $\mathbf{Q}$ and compute $p(t) = p(0) e^{t \mathbf{Q}}$ by diagonalization. Detailed balance makes $\mathbf{Q}$ similar to a symmetric matrix, so the eigenvalues are real. This takes $O(N^3)$ time and $O(N^2)$ space, and first passage times take one linear solve of the same cost.
- **Barrier trees.** Sort the states by energy and add them one by one, with a union-find structure over the move graph. A state with no added neighbor is a new local minimum; a state that joins two basins is the saddle where they merge (Flamm and others 2002, the program barriers). This takes $O(N \log N + M\, \alpha(N))$ time for $M$ moves, after the states are listed. In practice the states are listed in order of energy up to a cutoff with the suboptimal folding of Wuchty and others.
- **Coarse-grained kinetics (treekin).** Rates between basins are computed from the barrier tree, and the master equation is solved on the basins, with far fewer states than $\Omega(s)$.
- **Path heuristics.** Greedy and breadth-limited searches over direct paths estimate the barrier between two given structures.

## Bounds

- **State space.** $N$ grows exponentially in $n$ in the worst case, so any method that lists all states is exponential. Exact solutions are practical only for short sequences, or for the states below an energy cutoff.
- **Simulation.** Each step is polynomial in $n$, but the expected number of steps to reach a target can be exponential in the height of the barriers, by a factor of about $e^{\beta h}$ for a barrier $h$.
- **Barriers.** The lowest barrier over direct paths between two structures is NP-hard (Maňuch and others 2011). Over all paths it can be found by flooding, in time polynomial in $N$ but exponential in $n$.

## Reductions

- **To a Markov chain on a graph.** The problem is the transient analysis of a reversible continuous-time Markov chain on the move graph. The stationary part is the Boltzmann distribution, whose [partition function](/partition-function/) the McCaskill algorithm computes in $O(n^3)$ time without listing the states.
- **To Metropolis sampling.** The chain with Metropolis rates is the continuous-time form of the [Metropolis-Hastings](/metropolis-hastings/) method: each neighbor is proposed at rate $k_0$ and accepted with probability $\min(1, e^{-\beta \Delta})$. The jump chain, which records only the sequence of states, has the stationary distribution proportional to $\pi(P)\, K(P)$, not $\pi$; the waiting times, with mean $1/K(P)$, correct the difference.
- **To bottleneck paths.** The saddle energy of two states is a minimax path problem on the move graph, with the energy of a path the largest energy on it, which flooding solves as a minimum spanning tree does.

## Applications

- Riboswitches and RNA thermometers, whose function depends on two alternative structures and the barrier between them.
- Design of multistable RNAs, together with [RNA inverse folding](/rna-inverse-folding/), where a design must have two good structures and a given barrier.
- Co-transcriptional folding of long RNAs, where the structure that forms first can differ from the minimum free energy structure.
- Interpretation of folding experiments, such as single molecule pulling and temperature jumps.

## References
