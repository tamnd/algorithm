---
title: The exact intra-block route succeeds if and only if a legal configuration exists, so every block that AAPack outputs is legal, and the blocks partition the netlist
proves: [correctness]
status: full
---

We use the block model of the page. The block has slots $0, \ldots, N - 1$; slot $s$ has a LUT with inputs $0, \ldots, K - 1$ and a flip-flop if $\mathrm{ff}(s)$ holds. It has input pins $0, \ldots, I - 1$. LUT input $j$ of slot $s$ can be driven by the sources in $\mathrm{conn}(s, j)$, where a source is an input pin or the output of a slot. A set $C$ of BLEs and an injective map $\sigma$ from $C$ to the slots are given. Let $\mathrm{ext}(C)$ be the set of nets that a member reads and no member drives.

A **configuration** for $(C, \sigma)$ is a pair $(\pi, \mu)$ where

1. $\pi$ maps $\mathrm{ext}(C)$ injectively to the input pins;
2. for each $b \in C$, $\mu_b$ maps the distinct input nets of $b$ injectively to the LUT inputs of slot $\sigma(b)$;
3. for each $b \in C$ and each input net $x$ of $b$, the source of $x$ is in $\mathrm{conn}(\sigma(b), \mu_b(x))$, where the source of $x$ is the output of slot $\sigma(d)$ if a member $d$ drives $x$, and the pin $\pi(x)$ otherwise;
4. every registered member is in a slot with a flip-flop.

$(C, \sigma)$ is **legal** if a configuration exists. This is the model's statement that the block, with its members in these slots, can be routed: each external net enters on one pin, each LUT input carries one net, and each net reaches every LUT input that needs it through a switch that exists.

**Lemma 1 (one slot).** Fix $\pi$, and so the source of every net. For a member $b$, a map $\mu_b$ that meets conditions 2 and 3 exists if and only if the bipartite graph $H_b$, with the input nets of $b$ on one side, the LUT inputs of $\sigma(b)$ on the other, and an edge $(x, j)$ when the source of $x$ is in $\mathrm{conn}(\sigma(b), j)$, has a matching that covers every net. The procedure of the implementation finds such a matching whenever one exists.

*Proof.* A map $\mu_b$ with conditions 2 and 3 is exactly an injective choice of an edge of $H_b$ at each net, which is a matching that covers the nets. The procedure is Kuhn's algorithm: it tries an [augmenting path](/augmenting-path/) from each net in turn. Kuhn's algorithm returns a [maximum matching](/maximum-matching/) of a bipartite graph, by [Berge's lemma](/berge-lemma/): a matching is maximum if and only if no augmenting path exists. If some net finds no augmenting path, the maximum matching leaves a net uncovered, so no covering matching exists, and returning failure is right. Otherwise the result covers every net. $\square$

**Lemma 2 (the route is exact).** For fixed $(C, \sigma)$ that meet condition 4, ROUTE-CLUSTER returns a configuration if and only if $(C, \sigma)$ is legal, and what it returns is a configuration.

*Proof.* Soundness. The search gives each net of $\mathrm{ext}(C)$ a pin that no earlier net holds, so $\pi$ is injective (condition 1). Each $\mu_b$ comes from a covering matching of $H_b$, which gives conditions 2 and 3 by Lemma 1. Condition 4 is assumed.

Completeness. Let $(\pi^*, \mu^*)$ be a configuration. The search tries every injective map from $\mathrm{ext}(C)$ to the pins, in a fixed order, so it reaches $\pi^*$ unless it returns earlier with another configuration. With $\pi = \pi^*$, the maps $\mu^*_b$ are covering matchings of the graphs $H_b$. The graphs of different members use the LUT inputs of different slots, so the members do not compete for LUT inputs, and the choices for different members are independent. By Lemma 1 the procedure finds a covering matching for every member, so the search returns a configuration. $\square$

**Theorem 3 (legality and partition).** Assume that every BLE is legal alone in some slot of an empty block. Then AAPack stops, every block that it outputs comes with a configuration, every block has at most $N$ BLEs and at most $I$ external nets, and every BLE is in exactly one block. This holds in both modes.

*Proof.* In detailed mode, the predicate LEGAL is the counting check of conditions 4, the slot limit and $|\mathrm{ext}| \le I$, followed by ROUTE-CLUSTER. By Lemma 2 it is true exactly for legal $(C, \sigma)$. Line L3 places the seed in a slot where LEGAL holds; one exists by the assumption. Line L7 adds a BLE only where LEGAL holds for the new block. So, at every step, the current block with its slots is legal. When the loop ends, line L9 routes that block, and by Lemma 2 the route succeeds.

In speculative mode, line L7 tests only the counting checks. If line L9 then finds a route, the block is legal by Lemma 2. If not, line L10 grows the block again from the same seed in detailed mode, which ends with a legal block as above, and its route succeeds. So every output block has a configuration, and a configuration uses distinct slots and distinct pins, so the block has at most $N$ BLEs and at most $I$ external nets.

Each pass of the outer loop removes the BLEs of its block from the unclustered set, at least the seed, so there are at most $n$ passes. Each pass of the inner loop places a BLE in a free slot or ends the block, so it ends after at most $N - 1$ additions. The BLEs of a block are taken from the unclustered set and then removed from it, so the blocks are disjoint, and the outer loop ends only when every BLE is in a block. $\square$

**Theorem 4 (maximality for fixed slots).** In detailed mode, when line L8 ends a block $(C, \sigma)$, then for every BLE $b$ that is still unclustered and every free slot $s$, $(C \cup \{b\}, \sigma \cup \{b \mapsto s\})$ is not legal.

*Proof.* Line L8 is reached only after line L7 has tested every pair of an unclustered BLE and a free slot and found LEGAL false for each. By Lemma 2, LEGAL is false exactly when the block is not legal. $\blacksquare$

Theorem 4 keeps the slots of the members fixed. A BLE may still fit if the members moved to other slots; the page gives a two-BLE netlist where this happens, and AAPack then uses two blocks where one suffices. So nothing here bounds the number of blocks.
