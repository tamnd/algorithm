---
tag: 3WR03W
kind: theorem
slug: registers-have-consensus-number-one
name: Atomic registers have consensus number one
aliases:
- register consensus impossibility
- consensus number of registers
area: concurrency/lock-free-structures
level: advanced
summary: No wait-free protocol solves consensus for two processes with atomic read/write registers only. The proof is a bivalence argument on the next steps of the two processes.
prereqs: [consensus-number, flp-impossibility]
see_also: [consensus-number, flp-impossibility, cas-has-infinite-consensus-number, read-modify-write, atomic-snapshot, wait-freedom, obstruction-freedom, test-and-set]
sources:
  - paper: doi:10.1145/114005.102808
    title: Maurice Herlihy, Wait-free synchronization, ACM Transactions on Programming Languages and Systems 13(1), 1991
    locator: pages 124 to 149 (the theorem that read/write registers have consensus number 1, by a valence argument)
  - book: isbn:9780124159501
    title: Maurice Herlihy, Nir Shavit, Victor Luchangco and Michael Spear, The Art of Multiprocessor Programming, second edition, Morgan Kaufmann, 2020
    locator: Chapter 5, the sections on consensus protocols and atomic registers (the textbook proof with critical states)
  - paper: doi:10.1145/3149.214121
    title: Michael J. Fischer, Nancy A. Lynch and Michael S. Paterson, Impossibility of distributed consensus with one faulty process, Journal of the ACM 32(2), 1985
    locator: pages 374 to 382 (the message passing theorem whose method this proof follows)
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 12 (consensus in asynchronous shared memory with read/write registers)
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations, and Advanced Topics, second edition, Wiley, 2004
    locator: the chapter on wait-free simulations of arbitrary objects (the impossibility of consensus with registers)
---

## Statement

**Model.** Two processes $p$ and $q$ communicate only through atomic read/write registers, any number of them, with any initial values. Each process is a deterministic state machine with an input. A step of a process is one read or one write of one register, followed by a local change of state that depends only on the old state and, for a read, the value read. A process may *decide* a value once. Processes are asynchronous: any interleaving of steps is possible, and a process may stop (crash) at any point.

A *wait-free consensus protocol* for 2 processes satisfies three conditions in every run:

- **Agreement.** The two processes do not decide different values.
- **Validity.** A decided value is the input of $p$ or of $q$.
- **Wait-free termination.** A process that takes infinitely many steps decides; equivalently, each process decides after a finite number of its own steps, whatever the other one does.

**Theorem (Herlihy 1991; Loui and Abu-Amara 1987).** No wait-free consensus protocol for 2 processes uses only atomic read/write registers, even for binary inputs. So the [consensus number](/consensus-number/) of read/write registers is 1.

## In plain words

Two processes must agree on one of their two inputs, and neither may wait for the other, because the other may have stopped. With only reads and writes, this is impossible.

The proof follows the outcome along a run. At first, it depends on who moves first. Somewhere, a single next step decides it: if $p$ moves next the result is 0, and if $q$ moves next the result is 1. Look at those two steps. If one of them is a read, the other process cannot see it, so it cannot tell which world it is in, but it must decide differently in the two worlds. If both are writes to different registers, the order does not matter, so both worlds are the same state. If both write the same register, the second write hides the first one from the second writer. Every case ends in a contradiction.

## Proof

Fix a wait-free consensus protocol for $p$ and $q$ that uses only registers, and suppose it is correct. We derive a contradiction.

**Configurations and valence.** A *configuration* $C$ is the local state of each process and the value of each register. For a process $r$, $r(C)$ is the configuration after $r$ takes its next step from $C$; it is defined if $r$ has not decided. For a configuration $C$, let $V(C)$ be the set of values decided in configurations reachable from $C$. Call $C$ *bivalent* if $V(C) = \{0, 1\}$, and *$v$-valent* (univalent) if $V(C) = \{v\}$.

$V(C)$ is never empty: from $C$, let one process run alone. By wait-freedom it decides. If some process has decided $v$ in $C$, then $C$ is $v$-valent, by agreement. So in a bivalent configuration neither process has decided, and both can take a step.

**Lemma 1 (a bivalent start).** The initial configuration $C_0$ with input 0 for $p$ and input 1 for $q$ is bivalent.

*Proof.* Let $p$ run alone from $C_0$. By wait-freedom it decides. This solo run is also a run from the initial configuration where both inputs are 0, because the input of $q$ is only in the local state of $q$, and $q$ takes no step. There, validity forces 0, so $p$ decides 0 here too. In the same way, $q$ running alone from $C_0$ decides 1. So $V(C_0) = \{0, 1\}$. $\square$

**Lemma 2 (a critical configuration).** There is a reachable configuration $C$ that is bivalent, while $p(C)$ is univalent and $q(C)$ is univalent, one 0-valent and the other 1-valent.

*Proof.* Start at $C_0$. While the current configuration is bivalent and has a bivalent successor, move to that successor. If this never stops, it builds an infinite run in which every configuration is bivalent, so no process ever decides, but some process takes infinitely many steps. That breaks wait-free termination. So it stops at a bivalent $C$ whose successors $p(C)$ and $q(C)$ (both defined, since nobody has decided in $C$) are univalent. Every run from $C$ passes through $p(C)$ or $q(C)$, so $V(C) = V(p(C)) \cup V(q(C))$. Since $C$ is bivalent, one of them is 0-valent and the other is 1-valent. $\square$

From now on, rename the processes so that $p(C)$ is 0-valent and $q(C)$ is 1-valent. Let $a$ be the next step of $p$ and $b$ the next step of $q$ in $C$. We use one fact many times:

**Fact (indistinguishable states).** If two configurations $D$ and $E$ give a process $r$ the same local state and give every register the same value, then $r$ running alone takes the same steps from $D$ and from $E$ and decides the same value. (Its steps depend only on its state and on the values it reads.) By wait-freedom, $r$ does decide in both solo runs.

**Case 1: one of the steps is a read.** Say $a$ is a read; the case where $b$ is a read is the same with the names swapped. The read changes only the local state of $p$. So $p(C)$ and $C$ give $q$ the same state and give every register the same value. Run $q$ alone from $p(C)$ and from $C$. By the fact, $q$ decides the same value in both. From $C$, the solo run of $q$ starts with $b$, so it passes through $q(C)$, which is 1-valent: $q$ decides 1. From $p(C)$, which is 0-valent, $q$ decides 0. Contradiction.

**Case 2: both steps are writes, to different registers.** Then the two writes commute: $q(p(C)) = p(q(C))$. Each write changes only its own register and the local state of its own process, and neither reads anything. But $q(p(C))$ is reachable from $p(C)$, so it is 0-valent, and $p(q(C))$ is reachable from $q(C)$, so it is 1-valent. One configuration cannot be both. Contradiction.

**Case 3: both steps write the same register $R$.** Compare $D = q(p(C))$ and $E = q(C)$. In both, the last write to $R$ is the one of $q$, so $R$ has the same value; every other register is as in $C$; and $q$ has the same local state, since its step $b$ is a write and does not depend on $R$. Only the state of $p$ differs. By the fact, $q$ running alone decides the same value from $D$ and from $E$. But $D$ is reachable from $p(C)$, so it is 0-valent, and $E = q(C)$ is 1-valent. Contradiction.

The three cases cover all pairs of next steps, since each step is a read or a write. So the critical configuration of Lemma 2 cannot exist, and neither can the protocol. $\blacksquare$

**From 2 processes to $n$.** A wait-free protocol for $n \ge 2$ processes gives one for 2: let only $p$ and $q$ take steps, and give the other processes the input of $p$. The others never move, so wait-freedom still applies to $p$ and $q$, and validity still restricts the decision to the inputs of $p$ and $q$. So registers solve consensus for no $n \ge 2$.

**Checked on small cases.** The tests in the implementation folder use the interleaving explorer:

- *Write, then read.* Each process writes its input, reads the other register, and decides its own input if the register is empty, or the minimum of the two otherwise. It is wait-free, and the explorer finds that agreement fails on inputs (0, 1) after the schedule $[1, 1, 0, 0]$: $q$ writes 1, reads an empty register and decides 1; $p$ writes 0, reads 1 and decides 0.
- *Wait for the other.* Each process writes its input, then reads the other register until it is not empty, and decides the minimum. It agrees, and the explorer finds a cycle of states after the schedule $[0, 0, 0]$: $p$ reads the empty register again and again while $q$ does not move. It is not wait-free.
- *Every one-round protocol.* "Write my input, read the other register once, decide $f(\text{input}, \text{value read})$", over all $2^6 = 64$ functions $f$ for each process: all $4096$ pairs fail, $2820$ on validity and $1276$ on agreement.

## Consequences

- **No wait-free implementation from registers** exists, for 2 processes, of any object that solves 2-process consensus: [test-and-set](/test-and-set/), swap, [fetch-and-add](/fetch-and-add/), queue, stack, [compare-and-swap](/compare-and-swap/). Each of these is a step up that registers cannot make.
- **What registers can do** without waiting: they can implement every object of consensus number 1 that has a wait-free implementation from registers, for example the [atomic snapshot](/atomic-snapshot/), counters with increment and read, and approximate agreement. And, by the same kind of argument extended to $k + 1$ processes, they cannot solve $k$-set agreement among $k + 1$ processes (Borowsky and Gafni, Herlihy and Shavit, Saks and Zaharoglou, 1993).
- **Mutual exclusion must wait.** A lock from registers (Peterson, the bakery algorithm) is possible, but a process that waits for the lock waits for the holder. The theorem says that this is not an accident of the design.
- **Every weaker progress condition escapes.** [Obstruction-free](/obstruction-freedom/) consensus from registers exists; randomized wait-free consensus from registers exists, with termination with probability 1 (Abrahamson 1988, Aspnes and Herlihy 1990). The theorem needs deterministic processes and wait-freedom (or lock-freedom, which is the same for a one-shot object).

**How this differs from FLP.** The [FLP theorem](/flp-impossibility/) is about message passing: one crash, a buffer of messages, and steps that receive one message. Here the processes share memory, any number of them may crash (wait-freedom), and the steps are reads and writes. The structure of the proof is the same (a bivalent start, a critical configuration, a case analysis on the next steps), but the cases are about the kind of memory step, not about messages. The theorem also holds for one crash among $n$ processes in shared memory, which is the result of Loui and Abu-Amara; the wait-free form for 2 processes is the special case that Herlihy used to start the hierarchy.

## Tightness

- **One process.** Registers solve consensus for 1 process trivially (decide your input), so the consensus number is exactly 1, not 0.
- **One more primitive is enough.** With a single test-and-set bit or a single fetch-and-add word added to the registers, 2-process consensus is possible (see [consensus number](/consensus-number/)). So the gap between registers and these primitives is exactly 1.
- **Every condition is needed.** Without wait-freedom (waiting is allowed), a lock gives consensus. Without determinism, randomized protocols give consensus. Without agreement or validity, the problem is trivial.

## History

Loui and Abu-Amara (1987) proved that consensus in asynchronous shared memory with read/write registers is impossible if one process may crash, by adapting the FLP method to shared memory. Herlihy (1988, journal version 1991) placed the result at the bottom of the consensus hierarchy and used the same critical-state method for read-modify-write operations, queues, $m$-register assignment and compare-and-swap. The textbook proof by cases on the next steps is the one in Herlihy and Shavit's book.

## References
