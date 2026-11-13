---
tag: Q40QQ0
kind: data-structure
slug: quantum-random-access-memory
name: Quantum random access memory
aliases:
- QRAM
area: quantum/quantum-primitives
level: advanced
summary: "A memory of N classical bits that a quantum computer reads at a superposition of addresses in one query, built as a binary tree of routers."
model: quantum-circuit-model
complexity:
  vars: {N: the number of memory cells, n: the number of address qubits (N = 2^n)}
  time: {query: O(n), serial: Θ(n^2), write: Θ(1)}
  space: {total: Θ(N)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [quantum-oracle, quantum-circuit-model, binary-tree]
see_also: [grover-search, element-distinctness, random-access-machine, array, uncomputation, phase-kickback, block-encoding, quantum-threshold-theorem]
sources:
  - paper: doi:10.1103/PhysRevLett.100.160501
    title: Vittorio Giovannetti, Seth Lloyd and Lorenzo Maccone, Quantum random access memory, Physical Review Letters 100, 160501, 2008
    locator: the bucket-brigade architecture, the comparison with the fanout architecture, and the O(log N) routers that are active in one memory call instead of N
  - paper: doi:10.1103/PhysRevA.78.052310
    title: Vittorio Giovannetti, Seth Lloyd and Lorenzo Maccone, Architectures for a quantum random access memory, Physical Review A 78, 052310, 2008
    locator: the detailed bucket-brigade and fanout schemes, the qutrit routers, the gate count of order 2^n per call with only of order n gates active, and the effect of noise
  - paper: doi:10.1038/nphys3272
    title: Scott Aaronson, Read the fine print, Nature Physics 11(4), 2015, pages 291 to 293
    locator: the caveats of quantum machine learning, among them the cost of loading data and of QRAM, which can remove the claimed speedup
  - paper: doi:10.22331/q-2025-12-02-1922
    title: "Samuel Jaques and Arthur G. Rattew, QRAM: A Survey and Critique, Quantum 9, 1922, 2025"
    locator: the whole survey; the terms QRACM and QRAQM, the architectures, and the cost models under which QRAM speedups hold or fail
---

A quantum random access memory (QRAM) stores $N = 2^n$ classical bits $x_0, \ldots, x_{N-1}$ and answers a query on an address register in superposition: $|i\rangle|b\rangle \mapsto |i\rangle|b \oplus x_i\rangle$, which is the bit [quantum oracle](/quantum-oracle/) of the table $x$. The bucket-brigade design of Giovannetti, Lloyd and Maccone (2008) puts $N - 1$ three-state routers in a [binary tree](/binary-tree/) with the cells at the leaves. A query routes a bus qubit down the path that the address selects, so that only $n = \log_2 N$ routers are active in each branch and the query takes $O(n)$ time steps. The hardware still has $\Theta(N)$ parts, and much of the debate about QRAM is about whether this cost removes the speedups that assume it.

## In plain words

A normal memory takes one address and returns one stored bit. A quantum memory takes a quantum address, which can be many addresses at the same time, and returns, for each of them, the bit stored there, all in one call and with the different answers still able to interfere.

The bucket brigade builds this as a tree of switches. Each switch waits until a piece of the address reaches it. The first piece sets the top switch to left or right, the next piece goes through it and sets the switch below, and so on. After this the switches form one path from the top to a single cell. A messenger goes down the path, picks up the bit, and comes back. Then the address pieces go back out, and every switch returns to waiting, so that no trace of the address stays in the tree.

## The abstract type

A QRAM is a static [array](/array/) of $N$ bits with three operations.

- `write(i, v)`: a classical write of bit $v$ to cell $i$, done between queries.
- `read(i)`: a classical read of cell $i$, as in the [random-access machine](/random-access-machine/).
- `query`: the unitary $O_x$ on an address register of $n$ qubits and one bus qubit,

$$O_x \sum_{i, b} \alpha_{i,b} |i\rangle|b\rangle = \sum_{i, b} \alpha_{i,b} |i\rangle|b \oplus x_i\rangle .$$

The bus is qubit $0$ and the address is on qubits $1$ to $n$, so in the ket the bus is the rightmost symbol, as on [quantum state](/quantum-state/). $O_x$ is a permutation of the basis and is its own inverse. With the bus in $|-\rangle$ it gives the phase oracle $|i\rangle \mapsto (-1)^{x_i} |i\rangle$ by [phase kickback](/phase-kickback/). In the [quantum query model](/quantum-oracle/) a call of $O_x$ costs one query; QRAM is a proposal for what one query costs in hardware and time.

## Representation

The memory is a [complete binary tree](/complete-binary-tree/) of depth $n$, numbered as in a [binary heap](/binary-heap/).

- **Routers.** The internal nodes $1, \ldots, N - 1$ each hold a qutrit $r_k$ with the basis states $W$ (wait), $0$ (route left) and $1$ (route right). Node $k$ has the children $2k$ and $2k + 1$.
- **Cells.** A child number $c \ge N$ is the memory cell $c - N$, which holds the classical bit $x_{c-N}$.
- **Address slots.** The $n$ address qubits enter at the root, the most significant bit first. Slot $j$ holds address bit $n - 1 - j$.
- **Bus.** One qubit that travels down the tree and back.

**Invariant (R).** Between queries every router is in $|W\rangle$. During a query, in each basis branch, the routers that are not $W$ are exactly the nodes of the path from the root toward the addressed cell that has been built so far, at most one per level.

## Operations

The query is the same short program applied to every basis branch at once. A hop moves a qubit from a node to the child that the node's router selects, so the path of a qubit depends on the router states, which are quantum. Each line is a fixed unitary on the whole tree, not a classical branch.

```text
QRAM-QUERY(slots s[0..n-1], bus b, routers r[1..N-1], cells x[0..N-1])
Q1   for j = 0 to n - 1                       // load, most significant bit first
Q2       v = 1
Q3       repeat j times: v = 2v + r[v]        // hop along the active routers
Q4       swap s[j] and r[v]                   // r[v] was W; now it routes
Q5   v = 1
Q6   repeat n times: v = 2v + r[v]            // the bus goes down to a cell
Q7   b = b xor x[v - N]                       // the cell flips the bus, which then goes back up
Q8   for j = n - 1 down to 0                  // unload, in reverse order
Q9       v = 1
Q10      repeat j times: v = 2v + r[v]
Q11      swap s[j] and r[v]                   // the address bit leaves, r[v] is W again
```

Line Q4 takes a router out of $W$ only at the end of the current path, so at most $n$ routers are active. Lines Q8 to Q11 undo lines Q1 to Q4: they are the [uncomputation](/uncomputation/) of the load, and they are what makes the routers end in a state that does not depend on $i$. A classical `write` changes one cell and needs no quantum operation, because the cells are classical.

## Example

Take $n = 2$, $N = 4$ and $x = (x_0, x_1, x_2, x_3) = (0, 1, 1, 0)$. Query the basis input with address $i = 2 = (10)_2$ and bus $b = 0$. The routers are $r_1$ (root), $r_2$ (left child) and $r_3$ (right child).

| step | action | $r_1$ | $r_2$ | $r_3$ | slots $s_0 s_1$ | bus |
|---|---|---|---|---|---|---|
| start | | $W$ | $W$ | $W$ | $1\,0$ | $0$ |
| Q1 to Q4, $j = 0$ | bit $1$ goes into the root | $1$ | $W$ | $W$ | $W\,0$ | $0$ |
| Q1 to Q4, $j = 1$ | bit $0$ hops to node $2 \cdot 1 + 1 = 3$ | $1$ | $W$ | $0$ | $W\,W$ | $0$ |
| Q5 to Q7 | path $1 \to 3 \to 6$, cell $6 - 4 = 2$, $x_2 = 1$ | $1$ | $W$ | $0$ | $W\,W$ | $1$ |
| Q8 to Q11, $j = 1$ | bit $0$ leaves node 3 | $1$ | $W$ | $W$ | $W\,0$ | $1$ |
| Q8 to Q11, $j = 0$ | bit $1$ leaves the root | $W$ | $W$ | $W$ | $1\,0$ | $1$ |

So $|2\rangle|0\rangle \mapsto |2\rangle|1\rangle$. The steps are $1 + 2$ for the load, $2 + 1 + 2$ for the bus and $2 + 1$ for the unload, $11$ in all, which is $n(n+1) + 2n + 1$ for $n = 2$.

Now query $\frac{1}{\sqrt 2}(|0\rangle + |2\rangle)|0\rangle$. In the middle of the query the branch $i = 0$ has $r_1 = 0$, $r_2 = 0$, $r_3 = W$, and the branch $i = 2$ has $r_1 = 1$, $r_2 = W$, $r_3 = 0$. The routers are entangled with the address at this point. After the unload both branches have $r = (W, W, W)$ again, and the output is $\frac{1}{\sqrt 2}(|0\rangle|0\rangle + |2\rangle|1\rangle)$, with the routers in a product state.

## Correctness

Each of the load steps, the copy step and the unload steps is an involution of the basis configurations: a load step reads only routers above the level that it writes, so a second application finds the same node and swaps back. So the query is a permutation of the basis, and its linear extension is unitary. By induction on $j$, after $j$ load steps the active routers are the first $j$ nodes of the path whose binary labels are $1$ followed by the top $j$ address bits, so after $n$ steps the path ends at child $2^n + i$, which is cell $i$. The bus takes the value $b \oplus x_i$, and the unload, being the inverse of the load, which does not touch the bus, restores the address slots and sets every router back to $W$. The full proof, with the step count, is in the proof file.

## Complexity

| quantity | bucket brigade |
|---|---|
| routers (qutrits) and cells | $N - 1$ and $N$, so $\Theta(N)$ hardware |
| routers active in one branch | $n$, one per level |
| steps of one query, address bits one at a time | $n(n+1) + 2n + 1 = \Theta(n^2)$ |
| time of one query with the address bits pipelined | $O(n) = O(\log N)$ |
| gates of one query written as a circuit | $\Theta(N)$ |
| classical write or read | $\Theta(1)$ |

The serial count is the one of the proof: load step $j$ needs $j$ hops and one swap. The address bits do not have to wait for each other. If bit $j$ enters the root two steps after bit $j - 1$, it reaches each router after that router has been set, and the load ends after about $3n$ steps, so the query takes $O(n)$ steps. A circuit that simulates the tree has to act on every router that could be on the path, because the path is in superposition; GLM count gates of order $2^n$ per call, of which only order $n$ change the state in a given branch. This is the reason for the claim that the bucket brigade is less sensitive to noise than a design in which all routers are entangled with the address.

## Variants

- **Fanout QRAM.** Address bit $j$ controls all $2^j$ routers on level $j$ at once. The depth is again $O(n)$, but every router becomes entangled with the address, so a fault on any router can spoil the query. GLM introduce the bucket brigade as the improvement of this scheme.
- **Words.** Cells of $w$ bits use $w$ bus qubits, or $w$ trees that share the address, and give $|i\rangle|y\rangle \mapsto |i\rangle|y \oplus x_i\rangle$ with $y$ of $w$ bits.
- **QRACM and QRAQM.** The memory here holds classical bits (quantum random access classical memory). If the cells hold qubits, the copy of line Q7 is replaced by a swap of the bus with the cell, and the structure is a quantum random access quantum memory. The survey of Jaques and Rattew uses these names.
- **Lookup circuits.** Without special hardware, the same unitary can be built from [Toffoli](/toffoli-gate/) and [CNOT](/cnot-gate/) gates that loop over all $N$ addresses. This uses $\Theta(N)$ gates but few extra qubits, and it needs no hardware beyond a general fault-tolerant machine.

## When to use it

Use the QRAM model when an algorithm needs oracle access to a large classical table and its cost is stated as a number of queries. Examples are [Grover search](/grover-search/) over a stored list, the quantum walk for [element distinctness](/element-distinctness/), [quantum walk search](/quantum-walk-search/) on stored graphs, and [block encodings](/block-encoding/) of matrices whose entries are read from memory. A speedup in time holds only if a query really costs $O(\log N)$ time, and if the $\Theta(N)$ hardware is already built and is reused for many queries.

## Pitfalls

- **The hardware is $\Theta(N)$.** A QRAM for $N$ bits has $N - 1$ routers, and filling it takes $\Theta(N)$ writes. Aaronson's "Read the fine print" lists the cost of loading the data as a main caveat of quantum machine learning. Compare with equal hardware: a classical machine with $N$ processors searches $N$ items in $O(\log N)$ time, which is faster than a single run of Grover search with $O(\sqrt N)$ queries.
- **Active routers are not the cost.** Only $n$ routers change state in one branch, but in a circuit or with error correction all $\Theta(N)$ routers must be controlled and protected. The [threshold theorem](/quantum-threshold-theorem/) needs error correction on every router, also on the routers that wait.
- **Reset the routers.** If the unload is left out, the routers keep a copy of the path, so they are entangled with the address and the interference that the algorithm needs is lost. The tests check that the $N$ addresses give $N$ different router states in the middle of a query.
- **Classical data, quantum address.** A QRAM query gives $\sum_i \alpha_i |i\rangle|x_i\rangle$. It does not prepare a state whose amplitudes are the stored numbers; that needs more work, and a careless cost model hides it.
- **Bit order.** The address enters with its most significant bit at the root, while the index $i$ uses the [qubit](/qubit/) order with qubit $0$ least significant. Mixing the two reads the bit-reversed cell.

## Implementations

The Python module simulates the bucket brigade exactly on a sparse state $\{(i, b): \alpha\}$. The class `QRAM` keeps the routers as a heap-ordered list with $W = 2$, and `_branch` follows lines Q1 to Q11 for one basis configuration, so that `query` is the linear extension of a permutation. It also returns the number of steps and of active routers. The tests compare `query` with the oracle for every memory and every basis input with $n \le 3$, and with the permutation in `qsim.py` on random superpositions up to $n = 5$. They also check that two queries give the identity, the phase oracle with the bus in $|-\rangle$, that $n$ routers are active and hold the address, the step count $n(n+1) + 2n + 1$, and 300 random writes, reads and queries against a dictionary.

## History

Giovannetti, Lloyd and Maccone introduced the bucket-brigade QRAM in 2008 in Physical Review Letters. They compared it with the fanout scheme, in which all $N$ routers are entangled with the address, and showed that in their design only $O(\log N)$ routers are active in a call. Their paper in Physical Review A of the same year gives the architectures in detail. Many proposed quantum speedups, in particular in quantum machine learning, assume such a memory. Aaronson's 2015 comment in Nature Physics pointed out that the cost of loading data into QRAM and of building it can cancel these speedups. The 2025 survey of Jaques and Rattew reviews the hardware proposals and the cost models, and separates classical-data and quantum-data QRAM.

## References
