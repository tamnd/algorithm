---
title: SABRE ends and its output is equivalent to the input circuit
proves: [correctness]
status: full
---

This file proves, for the code of this page, that every pass of SWAP-SEARCH ends with a bounded number of SWAPs, that every two-qubit operation of its output acts on a coupling edge, and that the output computes the input circuit up to the initial and final permutations. Nothing here is about how many SWAPs SABRE uses compared with the optimum.

**Setting.** The input is a circuit $C = (c_1, \dots, c_g)$ on logical qubits $\{0, \dots, n-1\}$, each gate on one or two qubits, and a connected coupling graph $G$ on physical qubits $\{0, \dots, N-1\}$ with $N \ge n$. A *mapping* is an injective $\pi : \{0, \dots, n-1\} \to \{0, \dots, N-1\}$. Gate $c_j$ *depends* on $c_i$ if $i < j$ and $c_i$ is the last gate before $c_j$ on one of $c_j$'s qubits; this gives the DAG. $g_2$ is the number of two-qubit gates, $D$ is the distance in $G$, and $l$ is the limit of the release valve.

## Termination

**Lemma 1 (SWAPs touch occupied qubits).** Every candidate SWAP of line L11 is an edge of $G$ with at least one end that holds a logical qubit.

*Proof.* Line L11 takes the edges $\{p, q\}$ of $G$ where $p = \pi(a)$ for a qubit $a$ of a gate in $F$. ∎

**Lemma 2 (when SWAPs happen, F holds only waiting two-qubit gates).** Whenever lines L9 to L12 run, every gate of $F$ is a two-qubit gate whose qubits are at distance at least 2.

*Proof.* Line L8 runs before them in the same iteration and runs every ready gate. If any gate of $F$ were ready, L8 would have run it and gone to the next iteration. A one-qubit gate is always ready. ∎

**Theorem 3 (every pass ends).** SWAP-SEARCH ends after at most $g$ gate runs and at most $g_2 (l + N - 2)$ SWAPs.

*Proof.* Each gate enters $F$ once, when its last predecessor runs, and leaves it once, when it runs; so there are $g$ gate runs. Call a *stall* a maximal run of iterations in which no gate runs. During a stall, the counter of SWAPs in a row grows by one at each L12. When it reaches $l$, line L9 takes the gate $(a, b)$ of $F$ of least distance $d = D[\pi(a)][\pi(b)] \ge 2$ (Lemma 2), and moves $a$ along a shortest path: each SWAP is on an edge $\{p, q\}$ with $D[q][\pi(b)] = D[p][\pi(b)] - 1$, and such a $q$ exists on every shortest path. After $d - 1 \le \mathrm{diam}(G) - 1 \le N - 2$ SWAPs, $a$ and $b$ are adjacent, and since no other gate ran, the gate is still in $F$, so the next L8 runs it. So every stall has at most $l + N - 2$ SWAPs and ends with a gate run. By Lemma 2, $F$ holds a two-qubit gate during each stall, and this gate or another two-qubit gate runs at its end, so there are at most $g_2$ stalls. While $F$ is not empty and no stall is going on, line L8 runs a gate in each iteration. So the loop ends after at most $g$ iterations of L8 and $g_2 (l + N - 2)$ SWAPs. ∎

SABRE runs SWAP-SEARCH a fixed number of times (trials times traversals), so it ends as well.

## The output is valid

**Lemma 4 (order).** The gates of $C$ run in an order that is a linear extension of the DAG, each exactly once.

*Proof.* A gate enters $F$ only when its count of predecessors not yet run reaches 0, so it runs after all of them. By Theorem 3 and the end condition $F = \emptyset$, every gate enters and leaves $F$, so every gate runs exactly once. ∎

**Lemma 5 (edges).** Every SWAP of the output is on an edge of $G$, and every two-qubit gate of $C$ runs on physical qubits joined by an edge.

*Proof.* SWAPs come from line L11 (Lemma 1) or from the shortest-path walk of L9, which uses edges of $G$. Line L8 runs a two-qubit gate on $(\pi(a), \pi(b))$ only when $D[\pi(a)][\pi(b)] = 1$, that is, when they are joined by an edge. ∎

## The output is equivalent

Take the state space of the $N$ physical qubits. For a mapping $\pi$, let $P_\pi$ be the linear map from the $n$ logical qubits to the $N$ physical qubits that puts logical qubit $a$ on physical qubit $\pi(a)$ and the other physical qubits in $|0\rangle$:
$$P_\pi\, |x_0 x_1 \dots x_{n-1}\rangle = |y\rangle, \quad y_{\pi(a)} = x_a, \quad y_p = 0 \text{ for } p \notin \pi(\{0, \dots, n-1\}).$$
For a gate $U$ on logical qubits $A$, write $U_A$ for it on the logical register and $U_{\pi(A)}$ for the same gate on the physical qubits $\pi(A)$, in the same order.

**Lemma 6 (gates move through the mapping).** $U_{\pi(A)}\, P_\pi = P_\pi\, U_A$.

*Proof.* $P_\pi$ is a relabeling of tensor factors followed by adding factors in $|0\rangle$. Under it, the factors of $A$ become the factors of $\pi(A)$, so a gate on $A$ before the map is the same gate on $\pi(A)$ after it, and the added factors are not touched. ∎

**Lemma 7 (a SWAP only changes the mapping).** Let $\{p, q\}$ be an edge and $\tau$ the transposition of $p$ and $q$. Then $\mathrm{SWAP}_{pq}\, P_\pi = P_{\tau \circ \pi}$.

*Proof.* $\mathrm{SWAP}_{pq}$ exchanges the values of qubits $p$ and $q$ in every basis state. Applied to $P_\pi |x\rangle$, the value that was on $p$ (logical $x_a$ if $\pi(a) = p$, or 0 if $p$ is free) moves to $q = \tau(p)$, and the other way round, so the result puts logical qubit $a$ on $\tau(\pi(a))$ and keeps the free qubits in $|0\rangle$. That is $P_{\tau \circ \pi} |x\rangle$, and both sides are linear. ∎

This is the same update the code makes in `apply_swap`, so after each SWAP the variable `layout` is $\tau \circ \pi$. Lemma 7 also holds for SWAP written as three CNOTs, since the [CNOT page](/cnot-gate/) proves that $\mathrm{CNOT}_{pq}\mathrm{CNOT}_{qp}\mathrm{CNOT}_{pq} = \mathrm{SWAP}_{pq}$.

**Lemma 8 (reordering).** Let $\sigma$ be the order in which the gates of $C$ run. Then $c_{\sigma(g)} \cdots c_{\sigma(1)} = c_g \cdots c_1$ as operators.

*Proof.* By Lemma 4, $\sigma$ is a linear extension of the DAG, and so is the original order. Any two linear extensions of a partial order are joined by a series of exchanges of two adjacent elements that are not comparable (bubble sort one into the other: when two adjacent gates are out of order with respect to the target, the target puts them in the other order, so neither precedes the other in the partial order). Two gates not comparable in the DAG share no qubit, since two gates on a common qubit are joined by the chain of gates on that qubit. Gates on disjoint qubits commute. So each exchange keeps the product, and the two products are equal. ∎

**Theorem 9 (equivalence up to the final permutation).** Let $C'$ be the output of SWAP-SEARCH from $\pi_0$, with final mapping $\pi_f$, as an operator on the physical qubits. Then
$$C'\, P_{\pi_0} = P_{\pi_f}\, C.$$

*Proof.* Write the output as operations $o_1, \dots, o_k$, with mappings $\pi_0, \pi_1, \dots, \pi_k = \pi_f$, where $\pi_t$ is the mapping after $o_t$. Let $L_t$ be the product, in run order, of the gates of $C$ among $o_1, \dots, o_t$. We show $o_t \cdots o_1 P_{\pi_0} = P_{\pi_t} L_t$ by induction on $t$. For $t = 0$ both sides are $P_{\pi_0}$. If $o_t$ is a SWAP on $\{p, q\}$, then $\pi_t = \tau \circ \pi_{t-1}$, $L_t = L_{t-1}$, and Lemma 7 gives $o_t P_{\pi_{t-1}} L_{t-1} = P_{\pi_t} L_t$. If $o_t$ runs gate $U$ on $A$, the code emits it on $\pi_{t-1}(A)$, the mapping does not change, and Lemma 6 gives $U_{\pi_{t-1}(A)} P_{\pi_{t-1}} L_{t-1} = P_{\pi_{t-1}} U_A L_{t-1} = P_{\pi_t} L_t$. At $t = k$, $L_k$ is the product of all gates of $C$ in run order, which equals $C$ by Lemma 8. ∎

So the output, started with logical qubit $a$ on $\pi_0(a)$ and the free qubits in $|0\rangle$, ends with the state that $C$ produces, with logical qubit $a$ on $\pi_f(a)$ and the free qubits back in $|0\rangle$. A measurement of logical qubit $a$ reads physical qubit $\pi_f(a)$. This holds for every pass, including the backward ones, since a backward pass is SWAP-SEARCH on the reversed circuit; SABRE returns the output of a forward pass, so it is the circuit $C$.

## What the tests check

The test file checks the statements of Lemmas 4 and 5 on random circuits on lines, stars, grids and trees, and checks Theorem 9 directly: for CNOT and X circuits it compares the output, with each SWAP expanded into three CNOTs, against $P_{\pi_f} C$ on every basis state, which decides the equality since both sides map basis states to basis states; for circuits with H, T and CNOT it compares every column of the two operators by state vector simulation. It also checks the bound of Theorem 3 with several limits $l$, including $l = 0$, where the search is the plain walk along shortest paths.
