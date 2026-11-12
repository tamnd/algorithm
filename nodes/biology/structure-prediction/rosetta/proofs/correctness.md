---
title: The Rosetta protocol returns a clash-free structure with its exact energy, and the structure is a local minimum of the single moves
proves: [correctness]
status: full
---

We use the pseudocode of the page and the lattice model of its implementation. A structure is a pair $(w, r)$ of a word $w \in \{L, S, R\}^{n-2}$ and a rotamer vector $r \in \{0, 1, 2, 3\}^n$. It is *valid* when its $2n$ beads, $n$ on the backbone and $n$ side chains, are on distinct sites. $E_\text{fa}(w, r)$ is minus the number of pairs of H side-chain beads at distance 1 when $(w, r)$ is valid, and $+\infty$ otherwise. The implementation computes $E_\text{fa}$ exactly: it returns $+\infty$ when the set of the $2n$ sites has fewer than $2n$ elements, and otherwise it counts each pair $\{i, j\}$ of H side chains at distance 1 once, from the smaller index, by a lookup in a hash table of the side-chain sites.

**Lemma 1 (a lower bound on the energy).** For each valid $(w, r)$, $E_\text{fa}(w, r) \ge -\lfloor 3n/2 \rfloor$.

*Proof.* The side chain of residue $i$ is on a lattice neighbour of the backbone bead of $i$, so one of the 4 lattice neighbours of the side chain is that backbone bead, which is not a side-chain bead in a valid structure. So each side-chain bead has at most 3 side-chain beads at distance 1. Summing over the $n$ side chains counts each contact twice, so there are at most $3n/2$ contacts. $\square$

**Claim 1 (PACK).** PACK$(s, w)$ returns NIL exactly when no $r$ makes $(w, r)$ valid. Otherwise it returns $r$ with $(w, r)$ valid and with $E_\text{fa}(w, r) \le E_\text{fa}(w, r')$ for each $r'$ that differs from $r$ in one entry. It terminates in all cases.

*Proof.* *Backtracking.* The search keeps a prefix $r_0, \ldots, r_{i-1}$ of side chains that occupy distinct sites, none of them on the backbone, and a counter $c$ for the next rotamer of residue $i$. It extends the prefix with $c$ when that site is free, and it removes the last entry when $c = 4$. This is a depth-first search of the tree of all prefixes, in the order of the counters, that cuts a branch only when its last side chain is on a used site. Such a branch has no valid completion, because sites stay used in each extension. So the search reaches a full vector exactly when a valid vector exists, and it returns NIL only after the counter of the root reaches 4, that is, after it has cut or completed every branch. The tree is finite and no prefix is visited twice, so the search terminates.

*Rotamer trials.* Start from the valid vector of the backtracking, with energy $e$. A trial replaces $r$ by a vector $r'$ that differs in one entry only when $E_\text{fa}(w, r') < e$, which is finite, so $(w, r')$ is valid. So $r$ stays valid. Each change lowers the integer $e$ by at least 1, $e \le 0$ at the start, and $e \ge -\lfloor 3n/2 \rfloor$ by Lemma 1, so there are at most $\lfloor 3n/2 \rfloor$ changes, and the loop ends after a full pass with no change. In that pass every residue $i$ and every rotamer of $i$ was tried with the final $r$, and none lowered $e$. $\square$

**Claim 2 (the state before the descent).** After line L6, $(w, r)$ is valid and $E = E_\text{fa}(w, r)$. After each step of the refinement, the current state is valid with energy $E$, and $best$ is a valid state of energy $best.E$ equal to the minimum of the energies of the states visited since line L6.

*Proof.* If PACK of line L4 returns NIL, line L5 packs the extended chain. That chain has its backbone at $(i, 0)$ for $i = 0, \ldots, n - 1$, and with every rotamer equal to 1 the side chains are at $(i, 1)$, so a valid vector exists and Claim 1 gives one. So line L6 starts from a valid state with its exact energy. In the refinement, line L11 accepts only when $E' \le E$ or $\text{random}() < e^{-(E' - E)/T}$, and both are false when $E' = +\infty$ (the second because $e^{-\infty} = 0$). So an accepted state is valid, and line L11 stores its exact energy. Line L12 keeps the minimum, as in the proof for [simulated annealing](/simulated-annealing/). $\square$

**Claim 3 (the output).** Lines L13 to L17 terminate and return a valid $(w, r)$ with $E = E_\text{fa}(w, r)$, with $E \le best.E$, and such that no single move of line L15 has a lower energy.

*Proof.* Line L13 starts from $best$, which is valid with its exact energy by Claim 2. Line L16 moves only to a state with $E_\text{fa}(w', r') < E$, which is finite, so the state stays valid with its exact energy, and $E$ falls by at least 1. By Lemma 1 there are at most $E_\text{start} + \lfloor 3n/2 \rfloor$ such moves, and $E_\text{start} \le 0$, so the loop ends. It ends only after a round in which line L15 scanned every single move, one letter of $w$ to another letter or one entry of $r$ to another rotamer, and none had a lower energy. The energy only falls, so $E \le best.E$. $\square$

**What is not claimed.** The output need not be a global minimum of $E_\text{fa}$, and PACK need not find the best rotamers for its backbone. The example of the page has both failures: rotamer trials give $-1$ on the backbone SLLS, whose best packing has $-2$, and for PHHPPPH most seeds stop at $-1$ while the minimum is $-2$. The decision problem of the centroid phase alone is NP-complete, see [NP-completeness of HP folding](/hp-folding-np-completeness/).
