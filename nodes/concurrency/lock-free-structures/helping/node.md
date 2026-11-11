---
tag: 4QNG5W
kind: technique
slug: helping
name: Helping technique
aliases:
- cooperative helping
area: concurrency/lock-free-structures
level: advanced
summary: A process that finds an unfinished operation of another process finishes it, so that no process must wait for a slow or crashed one. The usual path to lock-free and wait-free designs.
prereqs: [lock-freedom, wait-freedom]
see_also: [michael-scott-queue, universal-construction, afek-atomic-snapshot, multi-word-cas, kogan-petrank-queue, harris-linked-list, wait-freedom, flat-combining]
sources:
  - paper: doi:10.1145/248052.248106
    title: Maged M. Michael and Michael L. Scott, Simple, fast, and practical non-blocking and blocking concurrent queue algorithms, PODC 1996
    locator: pages 267 to 275 (the lock-free queue, where any operation moves a lagging Tail)
  - paper: doi:10.1145/114005.102808
    title: Maurice Herlihy, Wait-free synchronization, ACM Transactions on Programming Languages and Systems 13(1), 1991
    locator: pages 124 to 149 (the universal construction with an announce array)
  - paper: doi:10.1145/2767386.2767415
    title: Keren Censor-Hillel, Erez Petrank and Shahar Timnat, Help!, PODC 2015
    locator: pages 241 to 250 (the definition of help-freedom; Theorems 4.18 and 5.1)
  - paper: doi:10.1145/2145816.2145835
    title: Alex Kogan and Erez Petrank, A methodology for creating fast wait-free data structures, PPoPP 2012
    locator: the fast-path-slow-path method, where helping is used only on the slow path
  - paper: doi:10.1145/153724.153741
    title: Yehuda Afek, Hagit Attiya, Danny Dolev, Eli Gafni, Michael Merritt and Nir Shavit, Atomic snapshots of shared memory, Journal of the ACM 40(4), 1993
    locator: pages 873 to 890 (updates that embed a scan, which a scan can borrow)
  - book: isbn:9780124159501
    title: Maurice Herlihy, Nir Shavit, Victor Luchangco and Michael Spear, The Art of Multiprocessor Programming, second edition, Morgan Kaufmann, 2020
    locator: Chapter 6 (the wait-free universal construction and its announce array); Chapter 10 (the lock-free queue)
---

## In plain words

In a lock-free or wait-free object, no process may wait for another one, because the other one may be slow or may have crashed. But an operation often needs several steps, and another process can find it half done. Helping is the rule for that case: instead of waiting, or undoing the work, the process that finds the unfinished operation completes it, and then goes on with its own work.

For this to work, every operation must leave a record in shared memory that says what it wants to do, and every step must be safe to do twice. Then any process can finish any operation, and it does not matter who does it. A design that only helps when an operation is in the way is usually lock-free. A design where each process also helps the others in a fair order can be wait-free.

## When it applies

- An operation changes more than one word, and a single atomic step cannot do all of it. Between the steps, the object is in an intermediate state that other processes can see. Examples: an enqueue that links a node and then moves Tail; a multi-word CAS; a delete that marks a node and then unlinks it.
- You need [wait-freedom](/wait-freedom/), and a process can lose every CAS race. Then the winners must do the work of the loser, or the loser can starve.
- The intent of an operation fits in a record (a descriptor) that other processes can read: the addresses, the old and new values, and a status.

It does not apply, or costs too much, when the intermediate state cannot be described in a record, or when a hot path cannot afford to read the records of other processes.

## The template

```text
operation op(args) by process p:
  d := new descriptor(op, args, status = ACTIVE)       // the intent, in shared memory
  publish d                                            // install it, or write it to announce[p]
  loop
    x := the record that the next step of d must change
    if x holds a descriptor e of another operation:
      help(e)                                          // finish e first
    else:
      do the next step of d with one CAS               // fails if someone else did it
    until d.status != ACTIVE
  return the result stored in d

help(e):
  repeat the same steps for e; each step is a CAS from an expected value,
  so a step that some other process has done already fails and does no harm
```

Four rules make the template correct:

1. **The intent is public.** The descriptor holds everything needed to finish the operation. A helper does not need the local variables of the owner.
2. **Every step is idempotent.** Each change is a CAS from the value the step expects. If two processes try the same step, one succeeds and the other fails without effect. So it does not matter how many helpers there are.
3. **There is one decision.** Where an operation can succeed or fail (as in a multi-word CAS), one CAS on the status field decides it, and all helpers then follow that decision.
4. **The result is stored, not returned by the helper.** The owner reads its result from the descriptor, so it gets the same answer whoever did the work.

For wait-freedom, add a fifth rule: **help in a fair order.** Each process, before or during its own operation, also helps the announced operation of one other process, chosen in turn (for example process $i \bmod n$ at the $i$-th operation), or helps every announced operation older than its own. Then every announced operation is helped within a bounded number of operations of the others, as in the wait-free [universal construction](/universal-construction/).

## Classic examples

**The Michael and Scott queue: moving a lagging Tail.** An enqueue links its node after the last node with one CAS (the linearization point), and then moves Tail with a second CAS. Between the two, Tail points one node behind. Any enqueue or dequeue that sees the lag moves Tail itself with CAS(Tail, t, next). The intent here needs no descriptor: the lag itself is the record.

The implementation folder has the queue with and without this rule. The numbers come from its tests, which run the interleaving explorer and the linearizability checker from [linearizability](/linearizability/):

| test | with help | without help |
|---|---|---|
| p0 enqueues and stops after its link CAS; p1 then enqueues alone | p1 finishes | p1 loops for ever |
| 2 enqueues; all runs | 104 states, 6 histories, all linearizable, every run ends | a cycle of states after 13 steps |
| enqueue and dequeue | 59 states, 10 histories | a cycle |
| 2 processes, each enqueue then dequeue | 532 states, 110 histories | a cycle |
| 2 enqueues and 1 dequeue in 3 processes | 1228 states, 198 histories | a cycle |

Without help, one stopped process blocks all the others, so the queue is not even lock-free. With help, it is lock-free.

**Announce arrays: the universal construction.** In Herlihy's wait-free universal construction, process $p$ writes its operation in announce[$p$]. Each process, when it proposes the next operation to apply, proposes the announced operation of a process chosen in turn, if that operation is still pending, and its own otherwise. An announced operation is applied after at most about $n$ more rounds, whatever the scheduler does. See [universal construction](/universal-construction/).

**Embedded scans: the atomic snapshot.** In the snapshot of Afek et al., every update first takes a scan and writes it next to its value. A scan that sees some process move twice can return the scan embedded in that process's update. The update has helped the scan to finish. See [Afek atomic snapshot](/afek-atomic-snapshot/).

**Descriptors: multi-word CAS.** In the multi-word CAS of Harris, Fraser and Pratt, an operation writes a pointer to its descriptor into each word. A process that finds a descriptor in a word finishes that whole operation before it goes on. See [multi-word CAS](/multi-word-cas/).

**Marked pointers: the Harris list.** A delete first marks the next pointer of the node, and then unlinks the node. Any traversal that meets a marked node unlinks it. See [Harris linked list](/harris-linked-list/).

## Variations

- **Helping on contention only (lock-free).** Help only the operation that is in the way. Cheap, but a process can still starve. The queue and the list above work this way.
- **Helping in a fair order (wait-free).** An announce array and a turn order, or phase numbers that give priority to the oldest operation. The [Kogan and Petrank queue](/kogan-petrank-queue/) uses phase numbers.
- **Fast path and slow path.** Kogan and Petrank (2012): run the plain lock-free code, and only after a fixed number of failures announce the operation and ask for help. The cost of helping is paid only under contention.
- **Recursive helping.** A helper that meets a third operation helps that one first. A fixed order (for example, by address in a multi-word CAS) stops cycles.
- **Combining.** One process does the operations of many others at once. [Flat combining](/flat-combining/) does this under a lock, so it is a blocking form of the same idea.

**What "help" means in theory.** Censor-Hillel, Petrank and Timnat (2015) gave an exact definition. Fix a linearization function for the implementation. An operation $o_1$ is *decided before* an operation $o_2$ in a run if $o_1$ comes before $o_2$ in the linearization of every extension of the run. A step of process $p$ is a *help step* if it makes some $o_1$ decided before some $o_2$, where $o_1$ is not an operation of $p$, and that was not so before the step. An implementation is *help-free* if it has a linearization function under which no step is a help step.

Their results (Theorems 4.18 and 5.1 of the paper) state that a linearizable implementation of a wait-free *exact order type* or a wait-free *global view type* using READ, WRITE and CAS, or a lock-free max register using READ and WRITE, cannot be help-free. An exact order type is one where the order of operations must be recorded exactly; queues and stacks are examples. A global view type is one with an operation whose result depends on all earlier operations; a snapshot and a counter with a read are examples. They also showed that with fetch-and-add, some global view types have help-free wait-free implementations, while exact order types still do not.

Under this definition, the Tail move of the Michael and Scott queue is not a help step. It does not decide the order of any two operations; the link CAS of the enqueuer already did that. The embedded scan of the Afek snapshot is a help step: a scan can be linearized only because an update took a scan for it. So "helping" in the practical sense (finishing the steps of another operation) and "help" in the sense of the theorem are not the same thing.

## Pitfalls

- **A late helper.** A helper can read a descriptor, stop, and wake up after the operation is over and its words are reused. Its CAS must then fail. Use a status field that is decided once, and guard against the [ABA problem](/aba-problem/) with descriptors that are never reused while a helper may hold them, or with [tagged pointers](/tagged-pointers/).
- **Freeing descriptors.** A helper can hold a pointer to a descriptor after the owner has returned. Free it only with a safe scheme such as [hazard pointers](/hazard-pointers/).
- **Cycles of helping.** If $A$ helps $B$ and $B$ helps $A$, both can loop. Order the words or the operations so that helping always goes one way.
- **Two results.** If the helper and the owner each compute a result, they can disagree. Store the result in the descriptor, once.
- **The cost on the fast path.** Reading the announce array costs $O(n)$ steps per operation. Under low contention this can make a wait-free object several times slower than a lock-free one; the fast-path-slow-path method exists for this reason.
- **Helping is not enough for wait-freedom.** Helping only the operation that is in the way still allows starvation. Wait-freedom also needs a fair order of helping.

## Exercises

1. In the Michael and Scott queue, a dequeue that finds Head = Tail and a non-null next moves Tail before it retries. Show a run where, without this rule, a dequeue returns a node that Tail still points to, and explain what goes wrong for the next enqueue.
2. Give a run of the wait-free universal construction with $n = 3$ in which process 2 is slow, and count how many operations of processes 0 and 1 can complete before the announced operation of process 2 is applied.
3. Show that the push of the [Treiber stack](/treiber-stack/) is help-free in the sense of Censor-Hillel, Petrank and Timnat: which step decides the order of two concurrent pushes, and whose step is it? Why does this not contradict their theorem about stacks?
4. Write the descriptor for a two-word CAS. Which field must be decided by a single CAS, and why can the second word not be written before that decision?

## References
