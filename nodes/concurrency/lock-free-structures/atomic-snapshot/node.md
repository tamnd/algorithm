---
tag: J3M2WS
kind: problem
slug: atomic-snapshot
name: Atomic snapshot
aliases:
- snapshot object
- atomic snapshot problem
- composite register
area: concurrency/lock-free-structures
level: advanced
summary: Build an object with update(i, v) and scan(), where scan returns all n components as they were at one instant, from read/write registers and without locks.
prereqs: [linearizability, lock-freedom]
see_also: [afek-atomic-snapshot, linearizability, wait-freedom, helping, registers-have-consensus-number-one, consensus-number, universal-construction, lock-freedom]
sources:
  - paper: doi:10.1145/153724.153741
    title: Yehuda Afek, Hagit Attiya, Danny Dolev, Eli Gafni, Michael Merritt and Nir Shavit, Atomic snapshots of shared memory, Journal of the ACM 40(4), 1993
    locator: pages 873 to 890 (the definition, the double collect, and the wait-free single-writer and multi-writer algorithms)
  - paper: doi:10.1145/93385.93396
    title: James H. Anderson, Composite registers, PODC 1990
    locator: pages 15 to 29 (the same object under the name composite register)
  - paper: doi:10.1007/bf02242703
    title: James H. Anderson, Composite registers, Distributed Computing 6(3), 1993
    locator: pages 141 to 154 (the journal version)
  - paper: doi:10.1145/97444.97701
    title: James Aspnes and Maurice Herlihy, Wait-free data structures in the asynchronous PRAM model, SPAA 1990
    locator: pages 340 to 349 (a wait-free scannable memory and its uses)
  - paper: doi:10.1137/s0097539795279463
    title: Hagit Attiya and Ophir Rachman, Atomic snapshots in O(n log n) operations, SIAM Journal on Computing 27(2), 1998
    locator: pages 319 to 340
  - book: isbn:9780124159501
    title: Maurice Herlihy, Nir Shavit, Victor Luchangco and Michael Spear, The Art of Multiprocessor Programming, second edition, Morgan Kaufmann, 2020
    locator: Chapter 4, the section on atomic snapshots (the simple snapshot with double collect, and the wait-free snapshot)
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations, and Advanced Topics, second edition, Wiley, 2004
    locator: the chapter on read/write objects (atomic snapshots)
---

## In plain words

Each of $n$ processes owns one memory cell, and writes to it when it likes. Sometimes a process needs to see all $n$ cells at once, as a photograph of one instant. Reading the cells one after another does not give that: while the reader goes along the row, other processes change cells behind it and in front of it, and the result can mix old and new values in a way that never existed. The atomic snapshot problem asks for an object with two operations, *update* (write my cell) and *scan* (return all cells), where every scan returns a vector that was really in memory at one moment during the scan. It must be built from ordinary read/write registers, without locks, so that a stopped process blocks nobody.

## Definition

A **single-writer snapshot object** for $n$ processes has $n$ components $C_0, \ldots, C_{n-1}$, all with an initial value, and two operations:

- **update$_i(v)$**, by process $i$ only: sets $C_i$ to $v$, and returns nothing.
- **scan()**, by any process: returns the vector $(C_0, \ldots, C_{n-1})$.

The implementation must be [linearizable](/linearizability/) against this sequential specification: each operation seems to take effect at one point between its invocation and its response. So a scan returns the values of all components at its linearization point.

The **atomic snapshot problem** is to implement this object from atomic read/write registers, without locks. A solution is **lock-free** if some operation always completes, and **wait-free** if every operation completes in a bounded number of its own steps, whatever the others do. The cost measure is the number of register operations per update and per scan, and the number and size of the registers.

**The problem in one example.** Three processes, all components 0. A scanner reads $C_0 = 0$. Then process 0 sets $C_0 := 1$ and returns. Then process 1 sets $C_1 := 1$ and returns. Then the scanner reads $C_1 = 1$ and $C_2 = 0$ and returns $(0, 1, 0)$. But $C_0$ became 1 before $C_1$ did, and the two updates do not overlap, so the vector $(0, 1, 0)$ was never the state of the object. This history is not linearizable. The tests find exactly this history (see Examples).

## Variants

- **Multi-writer snapshot.** Any process may update any component: update$(j, v)$. Afek et al. also give a wait-free multi-writer algorithm, built on the single-writer one.
- **Bounded registers.** The simple algorithms use sequence numbers that grow without bound. Afek et al. and Anderson give versions with registers of bounded size, at a higher cost.
- **Partial snapshot.** A scan asks for only some of the components, and should cost less when it asks for few.
- **Immediate snapshot.** Update and scan are one operation, with an extra property: the views of operations that run at the same time are ordered by inclusion and each one contains itself. It is used in the topological theory of wait-free computation.
- **Lattice agreement.** Each process proposes a value, and the outputs are comparable in a lattice and contain the inputs. Snapshot and lattice agreement can implement each other.

## Examples

**One collect is not a snapshot.** A *collect* reads $R_0, \ldots, R_{n-1}$ once, one at a time. Used as a scan, it fails. The tests in the implementation folder run the interleaving explorer on the workload "process 0 updates, process 1 updates, process 2 scans". Of 16 distinct histories, one is not linearizable, and it is the one above: the scan returns $(0, 1, 0)$.

**The double collect.** Each register holds a value and a sequence number that the owner increments at each update. A scan collects again and again until two collects in a row have the same sequence numbers, and returns that vector.

```text
update_i(v):  seq := seq + 1; R[i] := (v, seq)           -- one write

scan():
  a := COLLECT()
  loop
    b := COLLECT()
    if a and b have the same sequence numbers then return the values of b
    a := b
```

*Why it is linearizable.* Linearize an update at its write. If the sequence numbers of $R_j$ are the same in $a$ and $b$, then no write to $R_j$ happened between the two reads of $R_j$, because the owner never reuses a sequence number. This holds for every $j$, so between the end of collect $a$ and the start of collect $b$ no register changed, and at any point of that interval memory held exactly the vector $b$. Linearize the scan there.

*Why it is lock-free.* A scan that fails to return saw a change, so some update wrote in the meantime, and that update completed. So some operation always completes.

*Why it is not wait-free.* If an update lands between every pair of collects, the scan never returns. The tests do this with an adversarial schedule: each time the scanner reads $R_1$, process 1 writes once. With $n = 3$, after 10000 reads the scanner has not returned, while process 1 has done 3333 updates. The same happens for $n = 2$ and $n = 4$.

*Checked on small cases.* For four small workloads (an update and a scan; two updates and a scan; two processes that each update and then scan; two updaters and a scanner), the explorer finds 4, 10, 23 and 20 distinct histories with the double collect, all linearizable, and every run of each finite workload ends.

**The wait-free fix.** The double collect fails only because updates keep moving. Afek et al. make every update do a scan first and write the result next to its value. A scanner that sees the same process move twice knows that the second move came from an update that started after the scan began, so it can return the scan that that update wrote. This is the [Afek et al. wait-free snapshot](/afek-atomic-snapshot/), with $O(n^2)$ reads per operation.

## Known algorithms

| algorithm | progress | scan cost | update cost | registers |
|---|---|---|---|---|
| one collect | (not linearizable) | $n$ | 1 | single-writer |
| double collect | lock-free | unbounded | 1 | single-writer, unbounded seq |
| [Afek et al. 1993](/afek-atomic-snapshot/), single-writer | wait-free | $O(n^2)$ | $O(n^2)$ | single-writer, unbounded seq (a bounded version also given) |
| Afek et al. 1993, multi-writer | wait-free | polynomial in $n$ | polynomial in $n$ | from the single-writer object |
| Anderson 1990, composite registers | wait-free | see the paper | see the paper | bounded |
| Aspnes and Herlihy 1990, scannable memory | wait-free | $O(n^2)$ | $O(n^2)$ | unbounded |
| Attiya and Rachman 1998 | wait-free | $O(n \log n)$ | $O(n \log n)$ | single-writer |

Afek et al., Anderson, and Aspnes and Herlihy found wait-free snapshots at about the same time, independently, around 1990. Later work lowered the cost further and studied the multi-writer case, partial snapshots and bounded space; the table only lists the early results.

## Bounds

- **Lower bound for any solution.** A scan must read every component at least once, because it must return each one; with single-writer registers that is $n$ reads in a run where all components have changed. Stronger lower bounds of order $n$ hold for a wide class of objects and primitives (the perturbable objects of Jayanti, Tan and Toueg, 2000), and they include snapshots.
- **Upper bounds.** $O(n^2)$ (Afek et al.) and $O(n \log n)$ (Attiya and Rachman) register operations per operation, from single-writer registers.
- **Consensus.** A snapshot object has [consensus number](/consensus-number/) 1: registers implement it, and [registers have consensus number one](/registers-have-consensus-number-one/). So a snapshot cannot solve consensus for two processes, even though it reads all memory "at once". This is what makes it useful: it is the strongest tool that registers give for free.

## Reductions

- **From registers to snapshots.** The algorithms above. A wait-free snapshot can then replace "read all registers atomically" in any wait-free algorithm, which simplifies many proofs.
- **From snapshots to other objects.** A wait-free counter (each process adds to its own component; a read sums a scan), a max register, lattice agreement, approximate agreement, renaming, and the shared coins of randomized consensus (Aspnes and Herlihy) are all simple once a snapshot is available.
- **From snapshots to everything of consensus number 1?** No: some objects of consensus number 1 have no wait-free implementation from registers at all, so a snapshot is not universal for that level.
- **To the [universal construction](/universal-construction/).** The universal construction needs consensus objects, which snapshots cannot give. The two are the opposite ends: snapshots are what registers can do wait-free; the universal construction is what needs a consensus number of $n$.

## Applications

- **Wait-free algorithms on registers.** Many wait-free algorithms are first written with atomic scans and then the scans are replaced by a snapshot implementation.
- **Randomized consensus and renaming.** Early wait-free randomized consensus and renaming algorithms use snapshots to read the states of all processes.
- **Theory.** Immediate snapshots are the basic step of the iterated models in the topological approach to wait-free computability.
- **Systems.** A consistent view of per-thread counters or per-thread states (for example the epochs or announcements of a memory reclamation scheme) is a snapshot problem. Practical systems often accept a collect, which is weaker, because the algorithm that uses it is designed to tolerate it.

## References
