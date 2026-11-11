---
tag: KGSNTB
kind: algorithm
slug: afek-atomic-snapshot
name: Afek et al. wait-free atomic snapshot
aliases:
- wait-free snapshot
- Afek-Attiya-Dolev-Gafni-Merritt-Shavit snapshot
- embedded-scan snapshot
area: concurrency/lock-free-structures
level: research
summary: Wait-free single-writer snapshot from registers. Each update embeds a scan; a scan that sees a process move twice borrows that scan. At most 2n² reads per operation.
solves: [atomic-snapshot]
complexity:
  vars: {n: the number of processes}
  steps: {scan: O(n^2), update: O(n^2)}
  space: {shared: Θ(n^2)}
properties: {deterministic: true, wait_free: true, linearizable: true, single_writer: true, bounded_registers: false}
history:
  year: 1990
  people: [Yehuda Afek, Hagit Attiya, Danny Dolev, Eli Gafni, Michael Merritt, Nir Shavit]
  note: First presented at PODC 1990, journal version in JACM 1993. Anderson, and Aspnes and Herlihy, found wait-free snapshots independently at about the same time.
prereqs: [atomic-snapshot, wait-freedom, helping]
see_also: [atomic-snapshot, helping, linearizability, linearization-point, wait-freedom, registers-have-consensus-number-one, universal-construction, lock-freedom]
sources:
  - paper: doi:10.1145/153724.153741
    title: Yehuda Afek, Hagit Attiya, Danny Dolev, Eli Gafni, Michael Merritt and Nir Shavit, Atomic snapshots of shared memory, Journal of the ACM 40(4), 1993
    locator: pages 873 to 890 (the unbounded single-writer algorithm with embedded scans, its proof, the bounded version and the multi-writer version)
  - book: isbn:9780124159501
    title: Maurice Herlihy, Nir Shavit, Victor Luchangco and Michael Spear, The Art of Multiprocessor Programming, second edition, Morgan Kaufmann, 2020
    locator: Chapter 4, the section on atomic snapshots (the wait-free snapshot, where a scan that sees a thread move twice returns that thread's snapshot)
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations, and Advanced Topics, second edition, Wiley, 2004
    locator: the chapter on read/write objects, the section on atomic snapshots
  - paper: doi:10.1137/s0097539795279463
    title: Hagit Attiya and Ophir Rachman, Atomic snapshots in O(n log n) operations, SIAM Journal on Computing 27(2), 1998
    locator: pages 319 to 340 (a faster algorithm, for comparison)
---

The Afek et al. snapshot is a [wait-free](/wait-freedom/) solution of the [atomic snapshot](/atomic-snapshot/) problem from single-writer read/write registers. It is due to Afek, Attiya, Dolev, Gafni, Merritt and Shavit (PODC 1990, JACM 1993). The simple double collect scan can be starved for ever by updates that keep moving. The fix is a form of [helping](/helping/): every update first takes a scan and writes the result, its *view*, next to its value. A scan that sees the same process move twice knows that the second move came from an update that ran entirely inside the scan, so it returns the view of that update. Every scan and every update ends after at most $2n^2$ reads, whatever the other processes do.

## In plain words

You want a photograph of $n$ cells while other people keep writing to them. You read all cells twice. If nothing changed between the two passes, the second pass is a true photograph, and you are done. If someone changed a cell, you note who. That person is busy; you read again.

Now the trick. Before anyone writes to their cell, they must first take a photograph themselves and pin it next to the new value. If you see the same person change their cell a second time, then that person did a whole update while you were reading, including a whole photograph. That photograph was taken while you were busy, so it is a correct answer for you too. You take it and stop. Each person can surprise you only once before you can take their photograph, so you never read for ever.

## The problem

There are $n$ processes. Process $i$ may call update$_i(v)$, which sets component $i$ to $v$, and any process may call scan(), which returns the vector of all $n$ components. The implementation must be [linearizable](/linearizability/) and wait-free, and it may use only atomic read/write registers. Here each process $i$ has one register $R[i]$ that only it writes. See [atomic snapshot](/atomic-snapshot/) for the problem, its variants and the other solutions.

## The algorithm

Register $R[i]$ holds a triple $(val, seq, view)$: the value of component $i$, the number of updates of $i$ so far, and the view that $i$ took in its last update. Initially $R[i] = (v_0, 0, (v_0, \ldots, v_0))$. A collect reads $R[0], \ldots, R[n-1]$ one at a time, in any order, and returns the $n$ triples. Process $i$ keeps its own update count $seq_i$ in a local variable.

```pseudo id=main
UPDATE_i(v)
L1  view ← SCAN()                                   ▷ the embedded scan
L2  seq_i ← seq_i + 1; R[i] ← (v, seq_i, view)      ▷ one atomic write

SCAN()
L3  moved[0 .. n-1] ← false
L4  loop
L5      a ← COLLECT()
L6      b ← COLLECT()
L7      if a[j].seq = b[j].seq for every j then
L8          return (b[0].val, ..., b[n-1].val)      ▷ a clean double collect
L9      for each j with a[j].seq ≠ b[j].seq do
L10         if moved[j] then
L11             return b[j].view                    ▷ j moved twice: borrow its view
L12         moved[j] ← true
```

A scan that returns in line L8 is a *direct* scan; one that returns in line L11 is a *borrowed* scan. The sequence numbers only tell whether a register was written between two reads; the values may repeat, so comparing values would not be enough.

## Example

Take $n = 3$, all components 0. Process 0 scans. Process 1 updates again and again with the values $1, 2, 3, \ldots$, and process 2 is idle. The scheduler is hostile: each time process 0 finishes its first collect of an iteration, it lets process 1 run one complete update before process 0 reads again.

| step | process 0 (scanner) | process 1 | registers after the step |
|---|---|---|---|
| 1 | iteration 1, L5: collect $a$, $seq = (0, 0, 0)$ | | $R[1] = (0, 0, \cdot)$ |
| 2 | | update(1): its own scan returns $(0, 0, 0)$; writes | $R[1] = (1, 1, (0,0,0))$ |
| 3 | L6: collect $b$, $seq = (0, 1, 0)$ | | |
| 4 | L7 fails; L9: $j = 1$; L10: moved[1] is false; L12: moved[1] ← true | | |
| 5 | iteration 2, L5: collect $a$, $seq = (0, 1, 0)$ | | |
| 6 | | update(2): its own scan returns $(0, 1, 0)$; writes | $R[1] = (2, 2, (0,1,0))$ |
| 7 | L6: collect $b$, $seq = (0, 2, 0)$ | | |
| 8 | L9: $j = 1$; L10: moved[1] is true; L11: return $(0, 1, 0)$ | | |

The scan returns $(0, 1, 0)$ after $4n = 12$ reads. That vector was the state of the object during the embedded scan of update(2), and that embedded scan ran between steps 5 and 7, inside process 0's scan. So $(0, 1, 0)$ is a correct answer: the scan is linearized at the point where the borrowed scan was linearized. The plain double collect, under the same schedule, never returns: in the tests it has done 5000 reads after process 1 has done 833 updates.

## Correctness

The full proof is in the proofs folder. The two parts are these.

*Linearizability.* Linearize an update at its write in line L2. A direct scan: equal sequence numbers in $a[j]$ and $b[j]$ mean that no write of $R[j]$ happened between those two reads, because sequence numbers never repeat. This holds for every $j$, so at any time between the end of collect $a$ and the start of collect $b$, the registers held exactly $b$. Linearize the scan there. A borrowed scan: process $j$ wrote twice during the scan, so the update whose write the scan saw the second time started after the first write, and so after the scan started; and its embedded scan ended before that write, so before the scan ended. The embedded scan lies inside the borrowing scan. Linearize the borrowing scan at the point of the embedded scan. By induction on the end time of scans, every scan returns the state of the object at a point inside its own interval.

*Wait-freedom.* While process $p$ scans, it does not write $R[p]$ (the write of an update comes after its scan), so $moved[p]$ never becomes true. Each iteration that does not return sets a new entry of $moved$, and there are only $n - 1$ entries to set. So the scan returns within $n$ iterations of $2n$ reads each.

## Complexity

- **Scan:** at most $n$ iterations of two collects, so at most $2n^2$ reads. A scan with no concurrent updates takes one iteration, $2n$ reads.
- **Update:** one scan and one write: at most $2n^2 + 1$ register operations.
- **Space:** $n$ registers. Each holds a value, an unbounded sequence number and a view of $n$ values, so a register is $n + 2$ words wide. A register of that width must still be read and written atomically.

The bound $2n^2$ is reached. In the tests, the interleaving explorer runs every schedule of small workloads and records the cost of each operation. For two processes that each update and then scan, the worst scan takes $8 = 2 \cdot 2^2$ reads; for three processes, two of which update while the third scans, the worst scan takes $18 = 2 \cdot 3^2$ reads.

## Properties

- **Wait-free**, with a bound that does not depend on the schedule.
- **Linearizable** (Afek et al. use the name *atomic*).
- **Single-writer:** register $R[i]$ is written only by process $i$, and update$_i$ changes only component $i$.
- **Unbounded registers:** the sequence numbers grow for ever. The bounded version of the paper replaces them with handshake bits.
- **Uses helping:** a scan can return only because an update took a scan for it. In the terms of Censor-Hillel, Petrank and Timnat (see [helping](/helping/)), the embedded scan is a help step, and a snapshot is a global view type, so some help of this kind is unavoidable for a wait-free snapshot from registers.

## Variants and improvements

- **Bounded registers.** Afek et al. give a version in which a scanner and an updater share handshake bits, and each register also has a toggle bit, so that a register has bounded size. The cost stays polynomial.
- **Multi-writer snapshot.** Afek et al. also build a multi-writer snapshot, where any process may update any component, from the single-writer one.
- **The lock-free double collect.** Drop the views and the $moved$ array: the scan returns only in line L8. One write per update, but a scan can be starved for ever. It is the simple snapshot of Herlihy and Shavit, Chapter 4.
- **Faster snapshots.** Attiya and Rachman (1998) need only $O(n \log n)$ operations per scan or update, with lattice agreement inside.
- **Other early solutions.** Anderson's composite registers and the scannable memory of Aspnes and Herlihy (both 1990) solve the same problem with other methods.

## When to use it

Use it when you need a wait-free snapshot and only registers, or when you want a snapshot that is easy to prove correct, as a building block for another wait-free algorithm (a counter, a max register, lattice agreement, or randomized consensus). The cost of $O(n^2)$ reads per operation and registers of $n + 2$ words limits it to a small number of processes. If an update must be cheap and starvation of scans is acceptable, the double collect costs one write per update. If hardware gives a multi-word atomic read, or a [universal construction](/universal-construction/) is available, other methods can be faster.

## Pitfalls

- **Comparing values instead of sequence numbers.** Two collects can return the same values even though writes happened between them (the ABA case: a value written, then written back). The scan would then return a vector that never existed. The sequence number is what makes Lemma 1 of the proof true.
- **Borrowing after one move.** A scan that borrows the view of a process that moved only once is wrong: that update may have started before the scan, and its view may be older than the start of the scan.
- **Registers that are not atomic.** The triple $(val, seq, view)$ must be written and read as one atomic unit. On real hardware, write a pointer to an immutable record instead, and reclaim records safely.
- **Counting the own register.** The proof of the bound uses that the scanner does not write during its scan. In a variant where a process can update in the middle of its own scan (for example, by interrupting it), the bound changes.

## Implementations

## History

Afek, Attiya, Dolev, Gafni, Merritt and Shavit presented atomic snapshots at PODC 1990, and the journal version appeared in JACM in 1993. It gives the unbounded algorithm on this page, a bounded version, and a multi-writer version. At the same time, Anderson (composite registers, PODC 1990) and Aspnes and Herlihy (wait-free data structures in the asynchronous PRAM model, SPAA 1990) gave other wait-free solutions. The idea of the embedded scan, where an update does a scan to help later scans, became a standard example of helping. Attiya and Rachman (1993, journal version 1998) lowered the cost to $O(n \log n)$.

## References
