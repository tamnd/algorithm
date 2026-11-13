---
title: The bucket-brigade query maps |i>|b> to |i>|b xor x_i>, resets every router, and stops after a fixed number of steps
proves: [correctness, termination]
status: full
---

**Setting.** Let $n \ge 1$, $N = 2^n$, and let $x_0, \ldots, x_{N-1} \in \{0, 1\}$ be the stored bits. The routers are the nodes $1, \ldots, N - 1$ of a [complete binary tree](/complete-binary-tree/) in heap order: node $k$ has the children $2k$ (direction $0$) and $2k + 1$ (direction $1$), and a child number $c \ge N$ is the memory cell $c - N$. A basis configuration is a tuple $(s, b, r)$ with address slots $s_0, \ldots, s_{n-1} \in \{0, 1, W\}$, a bus bit $b \in \{0, 1\}$ and router values $r_1, \ldots, r_{N-1} \in \{0, 1, W\}$. For an address $i = (a_{n-1} \ldots a_0)_2$ the input configuration is $s_j = a_{n-1-j}$, $b$ arbitrary, and $r_k = W$ for all $k$. The query is the composition

$$Q = L_0 \circ L_1 \circ \cdots \circ L_{n-1} \circ C \circ L_{n-1} \circ \cdots \circ L_1 \circ L_0,$$

applied right to left: first $L_0$, last $L_0$ again. Here, for a configuration $(s, b, r)$:

- $\mathrm{path}_j(r)$ starts at node $1$ and takes $j$ hops, each to child $2k + r_k$. It is defined when the $j$ routers it passes are not $W$.
- $L_j$ (load or unload of slot $j$): if $\mathrm{path}_j(r)$ is defined and reaches node $v$, swap the values of $s_j$ and $r_v$; else do nothing.
- $C$ (copy): if $\mathrm{path}_n(r)$ is defined and reaches the child number $c$, replace $b$ by $b \oplus x_{c - N}$; else do nothing.

**Lemma 1 (each step is a permutation).** $L_j$ and $C$ are involutions of the set of basis configurations, so $Q$ is a permutation of this set, and its linear extension is a permutation matrix, which is unitary.

*Proof.* $\mathrm{path}_j(r)$ reads only routers of depth less than $j$. $L_j$ writes only $s_j$ and one router of depth exactly $j$. So after $L_j$ the same path is defined and reaches the same node $v$, and a second $L_j$ swaps the same two values back. $C$ reads all routers and writes only $b$, so a second $C$ adds $x_{c-N}$ again and restores $b$. An involution is a bijection, and a composition of bijections is a bijection. $\blacksquare$

**Lemma 2 (load invariant).** Start from the input configuration of address $i$. For $0 \le j \le n$, after $L_0, \ldots, L_{j-1}$:

> **(P)** $\mathrm{path}_j(r)$ is defined and visits the nodes $v_0 = 1, v_1, \ldots, v_{j-1}$ with $r_{v_t} = a_{n-1-t}$ and $v_{t+1} = 2v_t + a_{n-1-t}$. Every other router is $W$. The slots $s_0, \ldots, s_{j-1}$ are $W$ and $s_t = a_{n-1-t}$ for $t \ge j$. The bus is unchanged.

*Proof.* For $j = 0$ the path is empty, all routers are $W$ and all slots hold the address. Assume (P) for $j < n$. The path of length $j$ is defined and reaches $v_j = 2v_{j-1} + a_{n-j}$ (or node $1$ when $j = 0$). This node is not on the path, so $r_{v_j} = W$. $L_j$ swaps $s_j = a_{n-1-j}$ into $r_{v_j}$ and $W$ into $s_j$. Now $\mathrm{path}_{j+1}$ is defined, it visits $v_0, \ldots, v_j$ with the stated values, the other routers are still $W$, and the slots match (P) for $j + 1$. $\blacksquare$

**Lemma 3 (the bus reaches cell $i$).** With (P) for $j = n$, the child reached by $\mathrm{path}_n$ is $c = 2^n + i$.

*Proof.* By induction on $t$, $v_t$ has the binary form $1\,a_{n-1} \ldots a_{n-t}$, because $v_{t+1} = 2v_t + a_{n-1-t}$ appends one bit. After $n$ hops the number is $1\,a_{n-1} \ldots a_0$ in binary, which is $2^n + i$. $\blacksquare$

**Theorem.** For every address $i$ and bus value $b$, $Q$ maps the input configuration of $(i, b)$ to the input configuration of $(i, b \oplus x_i)$. So on the subspace where all routers are $W$, $Q$ acts as $|i\rangle|b\rangle \mapsto |i\rangle|b \oplus x_i\rangle$, and for a superposition

$$Q \sum_{i, b} \alpha_{i,b} |i\rangle|b\rangle|W \ldots W\rangle = \Big(\sum_{i, b} \alpha_{i,b} |i\rangle|b \oplus x_i\rangle\Big) \otimes |W \ldots W\rangle.$$

*Proof.* By Lemmas 2 and 3, after the load the path is complete and ends at cell $i$, so $C$ sets the bus to $b \oplus x_i$. $C$ changes neither the slots nor the routers. Let $T = L_{n-1} \circ \cdots \circ L_0$ be the load. Each $L_j$ ignores the bus: whether it acts and what it swaps depend only on $s$ and $r$. Write $T(s, b, r) = (s', b, r')$. Then $C(s', b, r') = (s', b \oplus x_i, r')$, and $T^{-1} = L_0 \circ \cdots \circ L_{n-1}$ by Lemma 1, so the unload gives $T^{-1}(s', b \oplus x_i, r') = (s, b \oplus x_i, r)$, the input configuration with the new bus value. The router part of the output is $W \ldots W$ for every branch, so it is a product factor, and the linear extension gives the display by linearity. $\blacksquare$

**Why the unload is needed.** By Lemma 2, after the load the routers hold the path to cell $i$, and different addresses give different router configurations. If the query stopped after $C$, the address register would be entangled with the routers, and the interference that algorithms such as [Grover search](/grover-search/) need would be lost. The unload is the [uncomputation](/uncomputation/) of the load.

**Termination and step count.** $Q$ is a fixed composition of $2n + 1$ maps, with no loop that depends on the data, so it stops. If one hop of a qubit between neighbouring nodes and one swap or flip each count one step, $L_j$ costs $j$ hops and one swap, and $C$ costs $n$ hops down, one flip and $n$ hops back. The total is $2 \sum_{j=0}^{n-1} (j + 1) + 2n + 1 = n(n + 1) + 2n + 1$, the same for every branch. At most $n$ routers are not $W$ at any time, one on each level of the path. The implementation checks the theorem exactly for all memories and all basis inputs with $n \le 3$, and on random superpositions up to $n = 5$.
