---
title: Correctness of counting networks
proves: [correctness, linearizability, progress]
status: sketch
---

This is a sketch. It follows the pseudocode on the main page, with the line labels L1 to L11, in the model of that page: asynchronous processes that may stop, an atomic TOGGLE for each balancer, and an atomic fetch-and-add for each output counter. That a given network counts (the step property for every input) is proved for the bitonic network on its own page; for the periodic network we cite Aspnes, Herlihy and Shavit and do not repeat their proof.

## Balancers in a quiescent state

**Lemma 1.** Take a balancer $b$ in any state of a run, and let $t$ be the number of TOGGLE steps done on $b$ so far. Then $\lceil t/2 \rceil$ of these tokens were sent to $b.\mathit{top}$ and $\lfloor t/2 \rfloor$ to $b.\mathit{bottom}$.

*Proof sketch.* The toggle starts at 0, and each TOGGLE (L3) returns the bit and flips it in one atomic step. So the $i$-th TOGGLE ($i = 0, 1, \ldots$) returns $i \bmod 2$, and L4 sends the token to the top wire exactly when $i$ is even. ∎

A state is *quiescent* if no token is inside the network: every call that has started has returned.

**Lemma 2.** In a quiescent state, the number of tokens that have left on each output depends only on the numbers $x_0, \ldots, x_{w-1}$ of tokens that have entered on each input, and not on the order of the steps.

*Proof sketch.* Process the balancers in layer order. In a quiescent state, every token that reached a wire in front of $b$ has also passed $b$, so the number $t$ of TOGGLE steps on $b$ is the sum of the numbers of tokens on its two input wires. By Lemma 1 the numbers on its outputs are $\lceil t/2 \rceil$ and $\lfloor t/2 \rfloor$, a function of the numbers on its inputs. By induction over the layers, every wire count is a function of $x$. ∎

So a network *counts* if and only if, for every vector $x$ of natural numbers, the output counts that Lemma 2 gives have the step property. That is a statement about numbers only, and the tests check it by computing the counts.

## From the step property to a counter

**Lemma 3.** Let $y_0, \ldots, y_{w-1}$ have the step property with sum $m$. Then the sets $V_j = \{ j + k w : 0 \le k < y_j \}$ are disjoint and their union is $\{0, 1, \ldots, m - 1\}$.

*Proof sketch.* Write $m = q w + r$ with $0 \le r < w$. By the step property, $y_j = q + 1$ for $j < r$ and $y_j = q$ for $j \ge r$. A number $v < m$ has a unique form $v = j + k w$ with $0 \le j < w$, and $v < m$ holds exactly when $k < q$, or $k = q$ and $j < r$, that is, when $k < y_j$. ∎

**Theorem 1 (counting).** In a quiescent state of a counting network after $n$ calls have returned, the values returned are exactly $0, 1, \ldots, n - 1$.

*Proof sketch.* A call that leaves on output $j$ does a fetch-and-add on $c[j]$ (L6). The fetch-and-add steps on $c[j]$ return $0, 1, \ldots$, so the $y_j$ calls that left on $j$ return the set $V_j$ of Lemma 3 (L7). In a quiescent state the counts have the step property, because the network counts, and the sum of the counts is $n$. Lemma 3 finishes the proof. ∎

**Theorem 2 (quiescent consistency).** Every history of the counter is quiescently consistent: there is a sequential history of a counter with the same values in which, for any two calls separated by a quiescent state, the earlier call comes first.

*Proof sketch.* Cut the history at its quiescent states $Q_1, Q_2, \ldots$, and let $n_i$ be the number of calls completed at $Q_i$. By Theorem 1 the calls completed before $Q_i$ returned exactly $0, \ldots, n_i - 1$. So the calls between $Q_{i-1}$ and $Q_i$ returned exactly $n_{i-1}, \ldots, n_i - 1$. Order all calls by their values. This is a sequential counter history, and a call before $Q_i$ has a smaller value than a call after $Q_i$. For calls after the last quiescent state, the values are distinct (Lemma 3's sets are disjoint for any counts), and putting them in value order after the others, and leaving out pending calls, gives the rest of the order. ∎

**Theorem 3 (not linearizable).** The counter on a counting network of width 2 has a history that is not linearizable.

*Proof.* The run on the main page: $A$ toggles and stops; $B$ returns 1; $C$, invoked after $B$ returned, returns 0; $A$ returns 2. In any linearization $B$ precedes $C$, but a counter that returns 1 before 0 would have to have counted down. ∎

The same idea works for any counting network of width $w \ge 2$: stop a token after its last toggle and before its fetch-and-add, and let other tokens leave on later outputs first. Herlihy, Shavit and Waarts study this in general.

## Progress

**Theorem 4 (wait-free, $d + 1$ steps).** A call of GET-AND-INCREMENT ends after exactly $d + 1$ of its own steps, whatever the other processes do.

*Proof sketch.* The construction (L8 to L11) puts a perfect matching of the wires in each layer: in a block, the first layer joins every wire with its mirror, and the two half blocks start at the same layer and have the same depth. So every wire has exactly one balancer in each of the $d$ layers, and the loop L2 to L4 does $d$ TOGGLE steps, each of which succeeds at once. Then L6 is one more step. Nothing in the code waits for or retries after another process. ∎

The test `test_solo_steps_are_bounded` stops other tokens at random points and checks that a call alone takes exactly $d + 1$ steps, for both networks at widths 2 to 16.

## Cited

**Theorem 5 (Aspnes, Herlihy and Shavit).** Periodic$[w]$ is a counting network for every $w = 2^k$.

We do not prove it here. The tests check the step property for all input vectors with entries below 6, 4 and 3 at $w = 2, 4, 8$, and for random inputs at $w = 16$ and $32$.
