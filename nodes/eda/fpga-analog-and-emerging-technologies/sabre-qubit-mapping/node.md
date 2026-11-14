---
tag: 2MX74V
kind: algorithm
slug: sabre-qubit-mapping
name: SABRE
aliases:
- SWAP-based bidirectional heuristic search
area: eda/fpga-analog-and-emerging-technologies
level: research
summary: Li, Ding and Xie's qubit mapper. It adds one SWAP at a time by a lookahead score over the front layer, and finds the initial mapping by forward and backward passes.
solves: [qubit-mapping]
model: word-ram
complexity:
  vars: {n: the number of logical qubits, N: the number of physical qubits, m: the number of coupling edges, g: the number of gates, D: the largest degree of the coupling graph, e: the size of the extended set, l: the limit of SWAPs in a row before the release valve}
  time: {distances: O(N (N + m)), one search step: O(N D (N + e)), one pass: O(g (l + N) N D (N + e))}
  space: {total: O(N^2 + g)}
properties: {deterministic: false, recursive: false, exact: false}
history:
  year: 2019
  people: [Gushu Li, Yufei Ding, Yuan Xie]
  note: SABRE searched SWAPs instead of whole mappings, which made routing fast enough for large circuits, and found the initial mapping by running the circuit forward and backward.
prereqs: [qubit-mapping, cnot-gate, breadth-first-search, directed-acyclic-graph]
see_also: [a-star-search, topological-sort, sorting-by-adjacent-swaps, permutation-routing, greedy-algorithm, quantum-circuit-model, floyd-warshall, reversible-logic-synthesis]
sources:
  - paper: doi:10.1145/3297858.3304023
    title: "Gushu Li, Yufei Ding and Yuan Xie, Tackling the qubit mapping problem for NISQ-era quantum devices, Proceedings of the 24th International Conference on Architectural Support for Programming Languages and Operating Systems (ASPLOS 2019), pages 1001 to 1014 (arXiv:1809.02573)"
    locator: Section IV.A (distance matrix, DAG, front layer), Section IV.B and Algorithm 1 (the SWAP-based search), Section IV.C (search over SWAPs, Figure 5 reverse traversal, the decay effect), Section IV.D and Equation 2 (the heuristic), Section V (IBM Q20 Tokyo, |E| = 20, W = 0.5, δ = 0.001, Table II)
  - paper: doi:10.1109/TCAD.2018.2846658
    title: "Alwin Zulehner, Alexandru Paler and Robert Wille, An efficient methodology for mapping quantum circuits to the IBM QX architectures, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 38(7), 2019, pages 1226 to 1236"
    locator: the layered A* search that SABRE compares with, BKA in its tables (general locator)
  - paper: doi:10.1145/3168822
    title: "Marcos Yukio Siraichi, Vinícius Fernandes dos Santos, Sylvain Collange and Fernando Magno Quintão Pereira, Qubit allocation, Proceedings of CGO 2018, pages 113 to 125"
    locator: Theorem 3.1 (Qubit Assignment is NP-complete), the hardness that SABRE cites as its reason for a heuristic
  - paper: arxiv:2409.08368
    title: "Henry Zou, Matthew Treinish, Kevin Hartman, Alexander Ivrii and Jake Lishman, LightSABRE, a lightweight and enhanced SABRE algorithm, arXiv:2409.08368, 2024"
    locator: Section II.7 (the release valve), and the 18.9% fewer SWAPs than SABRE in the abstract
---

SABRE (SWAP-based BidiREctional heuristic search) is a heuristic for [qubit mapping](/qubit-mapping/), by Gushu Li, Yufei Ding and Yuan Xie (ASPLOS 2019). It takes a quantum circuit and a coupling graph and inserts SWAP gates so that every two-qubit gate runs on coupled physical qubits. It walks the dependence graph of the circuit, runs every gate it can, and when it is stuck adds the one SWAP that most lowers a score: the mean distance of the gates that are waiting, plus a smaller weight times the mean distance of the next gates. It finds a good initial mapping by running the same search forward over the circuit, then backward over the reversed circuit, and taking the final mapping as the new start. Each step looks only at SWAPs next to waiting qubits, not at whole mappings, so it scales to large devices.

## In plain words

You have people at seats around a table, a script of conversations in order, and the rule that only neighbors can talk. SABRE reads the script and lets every conversation happen whose two people are neighbors and whose earlier lines are done. When nobody waiting can talk, it tries each exchange of seats between a waiting person and a neighbor, and picks the one that brings the waiting pairs closest, with a small bonus for bringing the next few pairs closer as well. Then it repeats.

To choose the first seating, it plays the whole script once from a random seating, then plays it backward from where everyone ended up. The seating at the end of the backward run is good for the start of the script, so it is used for the real run.

## The problem

Given a circuit on $n$ logical qubits and a connected coupling graph $G$ on $N \ge n$ physical qubits, find an initial mapping and a sequence of gates and SWAPs on the edges of $G$ that runs the circuit, with few SWAPs. The [problem page](/qubit-mapping/) defines it, shows that it is NP-complete, and defines SWAP as three CNOTs.

## The algorithm

The search works on the dependence DAG of the circuit: gate $j$ depends on gate $i$ if $i$ is the last gate before $j$ on one of $j$'s qubits. The *front layer* $F$ is the set of gates whose predecessors have all run. The *extended set* $E$ is the next $e$ two-qubit gates after $F$ in the DAG. $D[p][q]$ is the distance of $p$ and $q$ in $G$, so $D - 1$ SWAPs bring two qubits next to each other. With $\pi$ the current mapping, the score of a candidate SWAP (Equation 2 of the paper) is

$$H = \max(\mathrm{decay}(p), \mathrm{decay}(q)) \left( \frac{1}{|F|} \sum_{(a, b) \in F} D[\pi'(a)][\pi'(b)] + \frac{W}{|E|} \sum_{(a, b) \in E} D[\pi'(a)][\pi'(b)] \right),$$

where $\pi'$ is the mapping after the SWAP on $(p, q)$, $0 \le W < 1$, and $\mathrm{decay}$ is $1$ for a qubit not in a recent SWAP and rises by $\delta$ for each recent one, so the search favors SWAPs on other qubits, which can run at the same time.

```pseudo id=main
SABRE(C, G, trials, traversals)
L1  compute the distance matrix D of G by breadth-first search from every vertex
L2  for each trial: choose a random initial mapping π
L3      run SWAP-SEARCH on C from π, then on the reverse of C from the final mapping, and so on for traversals − 1 passes; π is the last final mapping
L4      run SWAP-SEARCH on C from π; keep the output with the fewest SWAPs and its initial mapping π
L5  return the best output, its initial mapping and its final mapping

SWAP-SEARCH(C, π)
L6  F ← the gates of C with no predecessor
L7  while F is not empty:
L8      if some gate of F is ready (one qubit, or its two qubits adjacent under π): run every ready gate, move to F the successors whose predecessors have all run, reset the decay, and continue
L9      if l SWAPs in a row have run no gate: move one qubit of the closest gate of F along a shortest path until the gate is ready (the release valve), and continue
L10     E ← the first e two-qubit gates after F in the DAG
L11     for each SWAP on an edge of G that touches a qubit of a gate in F: compute its score H
L12     apply the SWAP of least score to π (ties at random), emit it, and raise the decay of its two qubits
```

**The reverse traversal.** A circuit read backward has the same dependences reversed, and the mapping at the end of a forward pass suits the last gates. A backward pass from it ends in a mapping that suits the first gates, and it has seen the whole circuit on the way. The paper runs three passes (forward, backward, forward), five times from different random mappings, and keeps the best.

**The release valve.** The paper does not show that SWAP-SEARCH ends, and the score can choose SWAPs that run no gate; LightSABRE (2024) reports such cases and adds a release valve. The code adds a rule of this kind on line L9. After $l$ SWAPs in a row with no gate run ($l = 10N$ by default), it walks one qubit of the closest waiting gate along a shortest path, which makes that gate ready. This bounds the SWAPs, and the proof uses it. In the random tests, it never fired with the default limit.

**The code.** It follows Algorithm 1 and Equation 2, with $e = 20$, $W = 0.5$ and $\delta = 0.001$ as in the paper, and resets the decay after a gate runs or every 5 SWAPs. One-qubit gates are kept in the DAG and run as soon as they reach $F$. It uses breadth-first search for $D$ instead of Floyd-Warshall, since the graph has no weights. It builds the extended set again at each step, which costs $O(g)$; a real tool keeps it up to date.

## Example

Take the line $q_0 - q_1 - q_2 - q_3$, logical qubits $a, b, c, d$ on $q_0, \dots, q_3$, and the circuit $\mathrm{CNOT}(a, c)$, then $\mathrm{CNOT}(a, d)$. No gate is ready: $F = \{\mathrm{CNOT}(a, c)\}$ at distance 2, and $E = \{\mathrm{CNOT}(a, d)\}$. The candidate SWAPs touch $q_0$ or $q_2$:

| SWAP | $F$ term | $E$ term with $W = 0.5$ | $H$ |
|---|---|---|---|
| $(q_0, q_1)$, $a$ to $q_1$ | 1 | $0.5 \cdot D[q_1][q_3] = 1$ | **2** |
| $(q_1, q_2)$, $c$ to $q_1$ | 1 | $0.5 \cdot D[q_0][q_3] = 1.5$ | 2.5 |
| $(q_2, q_3)$, $c$ to $q_3$ | 3 | $0.5 \cdot D[q_0][q_2] = 1$ | 4 |

SABRE picks $(q_0, q_1)$, runs $\mathrm{CNOT}(a, c)$ on $(q_1, q_2)$, then needs one more SWAP for $\mathrm{CNOT}(a, d)$: 2 SWAPs. Without lookahead ($W = 0$) the first two SWAPs tie at 1, and the second one leads to 3 SWAPs. Neither is the best: the interaction graph is the path $c - a - d$, which fits on the line with $a$ in the middle, so the right initial mapping needs no SWAP. The forward pass ends with $a$ in the middle of $c$ and $d$, for example $c, a, d$ on $q_1, q_2, q_3$, so the backward pass starts from a mapping with no SWAP needed, and the full SABRE returns an output with 0 SWAPs. The test file checks all of this.

## Correctness

The [proof file](proofs/correctness.md) proves three things for the code. First, every pass ends, with at most $g_2 (l + N - 2)$ SWAPs for $g_2$ two-qubit gates, because of the release valve. Second, every two-qubit gate of the output, SWAPs included, acts on an edge of $G$, and every gate of $C$ runs exactly once, after its predecessors. Third, the output is equivalent to $C$ up to the final permutation: with $P_\pi$ the map that puts each logical qubit on its physical qubit $\pi(a)$ and the free physical qubits in $|0\rangle$, the output $C'$ satisfies $C' P_{\pi_0} = P_{\pi_f} C$. The proof uses two facts: a gate on logical qubits under $\pi$ is the same gate on $\pi$'s physical qubits, and a SWAP on $(p, q)$ only changes the mapping. Any order of the gates that respects the DAG gives the same operation, because gates that change places share no qubit and commute. Nothing is proved about the number of SWAPs beyond the upper bound.

## Complexity

Breadth-first search from each vertex gives $D$ in $O(N(N + m))$. In a search step, $F$ holds at most $n/2 \le N$ two-qubit gates, so there are at most $N D$ candidate SWAPs, and each costs $O(|F| + e) = O(N + e)$ to score: $O(N D (N + e))$ per step. Each run of SWAPs between two gate runs has at most $l + N - 2$ SWAPs, and there are at most $g$ runs, so a pass costs $O(g (l + N) N D (N + e))$ in the worst case. The paper argues that a gate needs at most about the diameter of $G$ in SWAPs, $O(\sqrt{N})$ for a 2D grid, which gives its bound of $O(N^{2.5} g)$; that argument assumes every SWAP makes progress, which the score does not promise without a rule like the release valve. Space is $O(N^2)$ for $D$ and $O(g)$ for the DAG.

## Properties

**What is proved.** Each pass ends with at most $g_2 (l + N - 2)$ SWAPs; every two-qubit operation of the output is on a coupling edge; and the output equals the input circuit up to the initial and final permutations. The proof file has the details.

**What is cited.** Li, Ding and Xie (Section V) test on the 20-qubit IBM Q20 Tokyo coupling graph against BKA, the layered A* method of Zulehner, Paler and Wille. On small benchmarks, SABRE finds mappings with no or few added gates: the added gates fall by 91% or vanish, against BKA. On large ones, it adds about 10% fewer gates on average, and runs where BKA runs out of memory. With the decay parameter, the depth of the output varies by about 8% against the number of gates.

**What is measured.** On 150 random circuits of 5 to 8 gates on devices of 4 or 5 qubits (seed 0), SABRE with 5 trials and 3 passes uses the fewest possible SWAPs, by an exhaustive breadth-first search over every initial mapping, on 147, and one more than that on the other 3. Every output passes a check that each two-qubit gate is on an edge and that the gates run in a legal order, and the outputs agree with the input circuit on every basis state, for CNOT and X circuits after the SWAPs are expanded into three CNOTs, and for H, T and CNOT circuits by state vectors. On 30 random circuits of 40 gates on a $3 \times 3$ grid (seed 7), three passes instead of one cut the total SWAPs from 505 to 397, 21% fewer. On 3,000 random circuits on random trees with extra edges, with $W$ in $\{0, 0.5, 0.9\}$, $\delta$ in $\{0, 0.001\}$ and $e$ in $\{1, 5, 20\}$, no pass ever made $4N + 20$ SWAPs in a row, so the release valve never fired; the tests do not show that the plain score can cycle, only that the code ends either way.

## Variants and improvements

- **Fidelity and time.** Later versions weigh each coupling by its error rate or gate time, so the distance in $D$ is a cost, not a hop count.
- **LightSABRE** (Zou, Treinish, Hartman, Ivrii and Lishman, 2024), the version in Qiskit, speeds up the search, runs many trials, and adds a release valve for the cases where the original score makes no progress. It reports 18.9% fewer SWAPs than the original SABRE on the same benchmarks.
- **Bridges and commutation.** Some routers also use bridge gates or move commuting gates into the front layer, so fewer SWAPs are needed.
- **Exact or layered search.** For small circuits, an exact method by satisfiability finds the fewest SWAPs, and [A* search](/a-star-search/) per layer, as in Zulehner, Paler and Wille, finds the best SWAPs for each layer of gates. SABRE trades these guarantees for speed.

## When to use it

Use SABRE, or a descendant of it, as the default router for circuits of tens to thousands of qubits on a sparse coupling graph. Run several trials and keep the best, since the result depends on the random start and on ties. For a circuit small enough, run an exact method to know how far the heuristic is from the best.

## Pitfalls

- **No termination proof in the paper.** The score can prefer SWAPs that run no gate; a router should have a rule that forces progress.
- **The final mapping.** The output ends in a different mapping than it starts; the measured bits must be read from the final places, or the compiler must add SWAPs to undo it.
- **Random ties.** Two runs with different seeds can give different SWAP counts; report the seed and the number of trials.
- **Even number of passes.** The last pass must be forward, over the real circuit, or the output runs the circuit backward.
- **Directed couplings.** On a device with one-way CNOTs, a CNOT in the wrong direction needs four Hadamard gates, which the plain score does not count.

## Implementations

## History

Before 2018, qubit mapping was studied for 1D and 2D grids, often with a nearest-neighbor cost. When IBM opened its devices with irregular coupling graphs, Siraichi et al. (CGO 2018) and Zulehner, Paler and Wille (DATE 2018, then TCAD 2019) gave exact and A*-based methods. Those searched over whole mappings, which grows exponentially with the number of qubits. In 2019, Li, Ding and Xie published SABRE, which searched over single SWAPs near the waiting gates and found the initial mapping by reverse traversal. Its speed made it the base of many later routers, including those in Qiskit.

## References
