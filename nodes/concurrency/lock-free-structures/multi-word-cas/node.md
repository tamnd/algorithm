---
tag: DFK374
kind: technique
slug: multi-word-cas
name: Multi-word compare-and-swap (MCAS)
aliases:
- MCAS
- k-word CAS
- Harris-Fraser-Pratt MCAS
- CASN
area: concurrency/lock-free-structures
level: advanced
summary: A lock-free k-word CAS built from single-word CAS. A descriptor goes into each word, one CAS decides, and every process that meets a descriptor helps it finish (Harris, Fraser and Pratt 2002).
prereqs: [compare-and-swap, double-compare-and-swap, lock-freedom, linearizability]
see_also: [double-compare-and-swap, helping, compare-and-swap, aba-problem, hazard-pointers, tagged-pointers, universal-construction, lock-freedom]
sources:
  - paper: doi:10.1007/3-540-36108-1_18
    title: Timothy Harris, Keir Fraser and Ian Pratt, A practical multi-word compare-and-swap operation, DISC 2002, LNCS 2508
    locator: pages 265 to 279 (RDCSS, CASN, the descriptors and the address order)
  - paper: doi:10.4230/LIPIcs.DISC.2020.4
    title: Rachid Guerraoui, Alex Kogan, Virendra Marathe and Igor Zablotchi, Efficient multi-word compare and swap, DISC 2020, LIPIcs 179
    locator: article 4 (k+1 CAS per k-word CAS without contention; a lower bound of k CASed locations; a persistent memory version)
  - paper: doi:10.4230/LIPIcs.DISC.2017.4
    title: Maya Arbel-Raviv and Trevor Brown, Reuse, don't recycle, transforming lock-free algorithms that throw away descriptors, DISC 2017, LIPIcs 91
    locator: article 4 (weak descriptors; k-CAS as the main example)
  - paper: doi:10.1145/1007912.1007945
    title: Simon Doherty and others, DCAS is not a silver bullet for nonblocking algorithm design, SPAA 2004
    locator: Section 6 (why a CAS on three words makes a deque simple)
  - book: isbn:9780124159501
    title: Maurice Herlihy, Nir Shavit, Victor Luchangco and Michael Spear, The Art of Multiprocessor Programming, second edition, Morgan Kaufmann, 2020
    locator: the chapters on lock-free data structures and on transactional memory
---

## In plain words

Many lock-free data structures would be simple if a program could change several words at once, each only if it still holds the expected value. Hardware gives a CAS on one word. Multi-word CAS builds the $k$-word version in software. The operation writes a record (a descriptor) that lists every word with its old and new value. It puts a pointer to the record into each word, one at a time. When all words hold the pointer, one CAS on a status field decides success. Then each word gets its new value. Any process that finds such a pointer in a word does not wait: it runs the same steps for the record and finishes the operation. So a stopped process blocks nobody, and the whole change is atomic.

## When it applies

- An update must change two or more words in different places together, for example two links of a doubly linked list, a node and a counter, or the entries of a lock-free tree rotation. If the words are adjacent and fit in 16 bytes, a double-width CAS is enough; see [double-compare-and-swap](/double-compare-and-swap/) for the difference.
- Lock-freedom is enough; wait-freedom is not needed. MCAS of Harris, Fraser and Pratt is lock-free, not wait-free.
- Every access to the shared words goes through MCAS and its read. A plain load can see a descriptor.
- Each word can spare two bits to mark a descriptor, or values can be told apart from descriptors in another way.
- There is a safe way to free descriptors: a garbage collector, [hazard pointers](/hazard-pointers/), epochs, or descriptor reuse.

## The template

**RDCSS.** The first building block is a restricted double-compare single-swap. RDCSS($a_1, o_1, a_2, o_2, n_2$) writes $n_2$ to the data word $a_2$ only if $a_2 = o_2$ and the control word $a_1 = o_1$, and returns the old value of $a_2$. It is not a DCAS: it writes only $a_2$, and $a_1$ is only compared. It works with a small descriptor $d$ that holds the five fields:

```text
RDCSS(d):
  repeat
    r := CMPXCHG(d.a2, d.o2, d)           -- put d in a2 if a2 = o2
    if r is an RDCSS descriptor then COMPLETE(r)   -- help, then retry
  until r is not an RDCSS descriptor
  if r = d.o2 then COMPLETE(d)
  return r

COMPLETE(d):
  if READ(d.a1) = d.o1 then CAS(d.a2, d, d.n2)
  else CAS(d.a2, d, d.o2)

RDCSS_READ(a):
  repeat r := READ(a); if r is an RDCSS descriptor then COMPLETE(r)
  until r is not an RDCSS descriptor
  return r
```

While $d$ is in $a_2$, the logical value of $a_2$ is $o_2$. The control word is read in COMPLETE, after $d$ is in place, so the compare of $a_1$ and the write of $a_2$ act as one step.

**CASN.** A CASN descriptor $cd$ has a status word (UNDECIDED, SUCCEEDED or FAILED) and the entries $(a_i, o_i, n_i)$, **sorted by address**:

```text
CASN(cd):
  if READ(cd.status) = UNDECIDED then
    s := SUCCEEDED
    for i := 1 to k while s = SUCCEEDED do        -- phase 1: install
      v := RDCSS(cd.status, UNDECIDED, a_i, o_i, cd)
      if v is a CASN descriptor then
        if v ≠ cd then CASN(v); retry this i      -- help the other one
      else if v ≠ o_i then s := FAILED
    CAS(cd.status, UNDECIDED, s)                  -- the decision
  ok := (READ(cd.status) = SUCCEEDED)
  for i := 1 to k do                              -- phase 2: release
    CAS(a_i, cd, if ok then n_i else o_i)
  return ok

CASN_READ(a):
  repeat r := RDCSS_READ(a); if r is a CASN descriptor then CASN(r)
  until r is not a CASN descriptor
  return r
```

The owner and every helper run the same CASN($cd$). The fields of a descriptor never change after it is published, except the status, which changes once.

**Why it is linearizable.** Give each word a logical value: a plain value is itself; a word that holds $cd$ has the value $n_i$ if $cd$ succeeded and $o_i$ otherwise; a word that holds an RDCSS descriptor has its $o_2$.

1. A descriptor $cd$ goes into a word only through RDCSS with control (status, UNDECIDED), so only while $cd$ is undecided, and only over the expected old value. So it never changes the logical value.
2. $cd$ leaves a word only in phase 2, after the decision, and is replaced by the logical value it stood for. So phase 2 does not change logical values either.
3. The status changes once, by one CAS. A CAS to SUCCEEDED happens only after some process put $cd$ in every word, in order, and $cd$ cannot leave a word before the decision. So at that moment every word holds $cd$ and its logical value is $o_i$. The CAS changes all of them to $n_i$ at once. This CAS is the linearization point of a successful CASN.
4. A failed CASN is linearized at the step of the deciding process that found a value other than $o_i$. At that step $cd$ was still undecided, and that word had a different logical value.
5. A read is linearized where CASN_READ finds a plain value.

**Why it is lock-free.** A process retries only after it found another descriptor and helped it to the end, so every retry follows the completion of some other RDCSS or CASN. The address order bounds the helping chain: if $cd$ meets $cd'$ at address $a$, then $cd'$ is already in $a$, so a helper of $cd'$ continues at addresses after $a$. Along a chain of helping the addresses increase, so no chain comes back to the first descriptor. Without the order, two CASNs on $\{x, y\}$ that start at different ends can help each other in a cycle without end (see the tests).

**Cost.** With no contention, a $k$-word CASN takes $3k + 1$ CAS steps: $k$ installs and $k$ completes in phase 1, one decision, $k$ releases. It also reads the status $k + 2$ times. It allocates a CASN descriptor and $k$ RDCSS descriptors. Under contention a process also pays for the operations that it helps. There is no bound on the steps of one operation: it is not wait-free.

## Classic examples

**A trace with help (two CASNs on the same words).** $x = y = 0$. Process $p$ runs CASN($x$: 0→1, $y$: 0→1) and process $q$ runs CASN($x$: 0→2, $y$: 0→2).

1. $p$ puts its descriptor $cd_p$ in $x$ (RDCSS install and complete). Then $p$ stops.
2. $q$ tries $x$ and finds $cd_p$. It helps: it puts $cd_p$ in $y$, sets the status of $cd_p$ to SUCCEEDED, and releases: $x = 1$, $y = 1$.
3. $q$ retries $x$, reads 1, which is not 0, and decides FAILED for its own descriptor. Its release CASes find no $cd_q$ and change nothing. $q$ returns false.
4. $p$ wakes up at entry $y$. Its RDCSS reads 1, not 0, so its local $s$ becomes FAILED. Its decision CAS fails, since the status is already SUCCEEDED. It reads the status and returns true.

The local variable $s$ is only a proposal; the status word is the decision. The test explores every interleaving of this workload (850 states, 10 distinct histories), and exactly one CASN succeeds in each.

**Why RDCSS and not a CAS.** Suppose phase 1 used a plain CAS($a_i$, $o_i$, $cd$). A slow helper could put $cd$ into $y$ after $cd$ was decided and released, if $y$ had come back to $o_i$ in between. Then $cd$ would stay in $y$, or a later reader would apply it a second time. RDCSS puts $cd$ in only while the status is UNDECIDED, and its COMPLETE takes $cd$ out again otherwise.

**Doubly linked lists and deques.** A pop from a deque that unlinks a node and marks it in one 3-word CAS has its whole effect in one atomic step. Doherty et al. (2004) use this to show how much simpler a deque becomes with a 3-word CAS than with [DCAS](/double-compare-and-swap/). MCAS makes this design possible on hardware with only single-word CAS.

**Lock-free trees and skip lists.** Fraser's lock-free data structures and many later trees use $k$-word CAS (or its relative, a small software transaction) to change several pointers in one step.

**What the tests check.** The implementation follows the pseudocode above, with descriptors as tagged tuples. For four small workloads (the trace above, two CASNs that share one word, a CASN with a reader of both words, and two CASNs that list the words in opposite order), it checks with the interleaving explorer and the Wing and Gong checker that:

| workload | states | distinct histories | all linearizable | every run ends |
|---|---|---|---|---|
| same two words | 850 | 10 | yes | yes |
| one shared word | 660 | 10 | yes | yes |
| CASN and reader | 453 | 14 | yes | yes |
| opposite order | 850 | 10 | yes | yes |

"Every run ends" means that the explorer found no cycle of states and no run longer than 300 steps. On a finite workload this is lock-freedom: an infinite run would have infinitely many steps but only finitely many operations to complete. A three-process case (two overlapping CASNs and a reader, 22161 states, 98 histories) also passed once, but takes about two minutes, so it is not in the test suite. The tests also check that:

- a solo CASN on $k = 1, 2, 3, 4$ words takes $3k + 1$ CAS steps and $k + 2$ reads;
- without the address order, the "opposite order" workload has a run that helps without end (a run longer than 200 steps);
- it is not wait-free: a reader of $x$ and a process that changes $x$ and $y$ in a loop. When the reader is about to read $x$, the schedule lets the writer run until a new descriptor is in $x$. After 1000 rounds the reader has taken 909 steps, helped all the time, and not returned, while 91 CASNs of the writer succeeded.

## Variations

- **Fewer CAS steps.** Guerraoui, Kogan, Marathe and Zablotchi (2020) give a $k$-word CAS with $k + 1$ CAS steps when there is no contention. Earlier methods use at least $2k + 1$. They also show that the information for a $k$-word CAS cannot be put into fewer than $k$ CASed locations. Their algorithm also has a durable form for persistent memory.
- **Reuse descriptors.** The original algorithm allocates at least $k + 1$ new descriptors per operation, and freeing them safely is costly. Arbel-Raviv and Brown (2017) define weak descriptors and transform the $k$-CAS so that each process reuses two descriptors. The memory use drops a lot and the speed goes up.
- **Wait-free versions.** A wait-free $k$-word CAS adds an announce array and helping in turn, as in the [universal construction](/universal-construction/); for example Sundell (2011). They pay more per operation.
- **From LL/SC.** Earlier constructions (for example Israeli and Rappoport, 1994) build multi-word operations from [load-linked/store-conditional](/load-linked-store-conditional/) and aim at disjoint-access parallelism: operations on disjoint words do not touch common memory.
- **Hardware transactions.** A short hardware transaction can do a $k$-word CAS when it commits. It needs a software fallback, often MCAS itself.
- **Double-width CAS.** If the two words are adjacent, one CMPXCHG16B does it, without descriptors.

## Pitfalls

- **Plain reads.** A word can hold a descriptor at any time. Every read of a shared word must use CASN_READ (or decode the logical value), and plain values must never look like descriptors.
- **No address order.** Two operations that install in different orders can help each other in a cycle without end. Sort the entries by address, once, in the descriptor.
- **Taking the local result as the decision.** In phase 1 the local result can be FAILED while a helper has already made the operation succeed (step 4 of the trace). Always read the status after the decision CAS.
- **Freeing a descriptor too early.** A slow helper may still hold a pointer to a descriptor and CAS with it. If its memory is reused as a new descriptor at the same address, that CAS can succeed by mistake (the [ABA problem](/aba-problem/)). Use a garbage collector, [hazard pointers](/hazard-pointers/), epochs, or the reuse scheme of Arbel-Raviv and Brown.
- **The same word twice.** An operation that lists one address twice installs its descriptor once and then finds it again; decide what that means, or forbid it.
- **Expecting wait-freedom.** One process can help others for ever and never finish its own operation.
- **Cost.** About $3k + 1$ CAS steps and $k + 1$ allocations per operation. For $k = 1$, use a plain CAS.

## Exercises

1. Count the CAS steps of a solo 3-word CASN by hand. Where are the 10 CAS steps?
2. In COMPLETE, the control word is read after the descriptor is in $a_2$. Give a run that goes wrong if RDCSS reads $a_1$ first and then does one CAS on $a_2$.
3. Find the run without end for CASN($x$, $y$) and CASN($y$, $x$) when the entries are not sorted. How deep does the helping recursion become after $m$ steps?
4. Can CASN_READ return the logical value without helping (read the status of the descriptor it finds, and return $n_i$ or $o_i$)? Where would you put its linearization point?
5. Prove that a word holds at most one CASN descriptor at a time, and that the descriptor in it is undecided or is about to be released.
6. Use MCAS to write a lock-free doubly linked list delete. Which words does the CASN change, and what must a concurrent insert next to the node do?

## References
