---
tag: DJBX02
kind: algorithm
slug: cheap-paxos
name: Cheap Paxos
area: distributed/consensus
level: research
summary: Tolerates f failures with f+1 main processors and f auxiliaries used only during reconfiguration.
solves: [consensus-problem]
model: asynchronous-model
complexity:
  vars: {f: the number of failures tolerated, k: the number of commands}
  time: {best: Θ(1)}
  messages: {best: Θ(f k)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false}
history:
  year: 2004
  people: [Leslie Lamport, Mike Massa]
  note: Presented at the DSN 2004 conference.
prereqs: [multi-paxos, quorum, cluster-reconfiguration]
see_also: [paxos, flexible-paxos, vertical-paxos, primary-backup-replication, quorum-intersection, replicated-state-machine]
sources:
  - paper: doi:10.1109/DSN.2004.1311900
    title: Leslie Lamport and Mike Massa, Cheap Paxos, International Conference on Dependable Systems and Networks (DSN 2004), 307-314, 2004
    locator: Section 2.3 (dynamic Paxos and the window α), Section 3.1 (the quorums of Cheap Paxos and the steps after a main processor fails)
  - paper: "Leslie Lamport, Paxos made simple, ACM SIGACT News 32(4), 51-58, December 2001"
    locator: Section 3 (state machines, and changing the set of servers with a command that takes effect α instances later)
  - paper: doi:10.1145/1582716.1582783
    title: Leslie Lamport, Dahlia Malkhi and Lidong Zhou, Vertical Paxos and primary-backup replication, PODC 2009, 312-313
    locator: the comparison with Cheap Paxos, which keeps f + 1 full replicas
---

Cheap Paxos is a form of [Multi-Paxos](/multi-paxos/) that tolerates $f$ crashed processors with only $f + 1$ main processors that store the state, plus $f$ auxiliary processors that work only when a main processor fails. The set of all main processors is a [quorum](/quorum/) by itself, so in normal operation the auxiliaries get no messages. When a main fails, the leader uses the auxiliaries to finish the open instances, then [reconfigures](/cluster-reconfiguration/) the system to remove the failed main, and after that the auxiliaries can rest and forget again. The model is [asynchronous](/asynchronous-model/) with [crash failures](/crash-failure/).

## In plain words

To survive one broken computer, Paxos normally needs three full copies of the data, because a decision needs a majority of three. Cheap Paxos uses two full copies and one small helper machine.

As long as both full copies work, they decide alone: "both of them" counts as a group that always overlaps any other group that may decide. The helper does nothing and stores nothing.

When one full copy breaks, the remaining copy and the helper form a majority, so they can still decide. They use that majority for one important decision: to remove the broken machine from the group. After that, the single remaining copy is the whole group of main machines, and the helper can throw away what it stored.

## The problem

**Model.** Processors fail by [crashing](/crash-failure/), timing is [asynchronous](/asynchronous-model/), and messages can be lost, duplicated and reordered. Main processors keep their state on stable storage. Lamport and Massa write $f$ for the number of failures to tolerate, with $f + 1$ main and $f$ auxiliary processors.

**Goal.** A [replicated state machine](/replicated-state-machine/) with agreement in every slot in every run, as in Multi-Paxos, using cheap machines for all but $f + 1$ of the $2f + 1$ processors.

**Configurations.** A configuration $C$ has a set $M$ of main processors and a set $A$ of auxiliary processors, with $G = M \cup A$. Its quorums are:

- the set $M$ itself, and
- each majority of $G$ that holds at least one main processor.

Any two of these quorums meet. Two majorities of $G$ meet. The set $M$ meets each majority of $G$ when $|M| \ge \lceil |G|/2 \rceil$. At the start $|M| = f + 1$ and $|G| = 2f + 1$, so this holds, and every majority of $G$ even holds a main, because only $f$ processors are auxiliary.

**Dynamic Paxos.** Each slot $s$ of the log is one Paxos instance with its own configuration $C(s)$. A command chosen in slot $s$ may change the configuration, and the change takes effect $\alpha$ slots later: $C(s + \alpha)$ depends on the commands of slots up to $s$. So a leader can work on slot $s$ only when slot $s - \alpha$ is decided. Here we take $\alpha = 1$.

## The algorithm

```pseudo id=main
LEADER p (a main processor), with ballot b and current slot s
L1  on becoming leader or a timeout:  b ← a fresh ballot (r, p); s ← the first slot not known decided; send PREPARE(b, s) to M(s)
L2  on PROMISE(b, votes, decisions) from processor a:  add a to the promisers
L3  when the promisers contain a quorum of C(s):
L4      v ← the decision for s if one is reported, else the value of the vote with the largest ballot for s, else a pending "remove" command, else the next client command
L5      send ACCEPT(b, s, v) to M(s), or to all of G(s) once a main has failed
L6  on ACCEPTED(b, s) from a quorum of C(s):  decided[s] ← v; send DECIDE(s, v) to M(s)
L7  on a timeout with nothing in flight:  mark each main of M(s) that has not answered as failed (queue "remove" for it); resend the current phase to all of G(s)
L8  after a decision:  s ← s + 1; C(s) ← C(s - 1) changed by v; if the promisers hold no quorum of C(s), go back to phase 1 for s
L9      if C(s) ≠ C(s - 1):  send all decisions to the new M(s), then FORGET(s) to the auxiliaries of C(s - 1)

PROCESSOR a (main or auxiliary)
L10 on PREPARE(b, s0):  if b ≥ promised and s0 is not forgotten then promised ← b; send PROMISE(b, votes and decisions for slots ≥ s0)
L11 on ACCEPT(b, s, v):  if b ≥ promised then promised ← b; votes[s] ← (b, v); send ACCEPTED(b, s)
L12 on DECIDE(s, v):  decided[s] ← v
L13 on FORGET(s) at an auxiliary:  forget all votes and decisions for slots below s, and refuse to promise for them
```

**Normal operation.** Lines L1 to L6 are Multi-Paxos with $M(s)$ as the quorum. A stable leader runs phase 1 once, and each command then takes one ACCEPT round with the $f + 1$ mains. The auxiliaries see nothing.

**A main fails.** The leader times out (line L7), resends to all of $G(s)$, and gets a quorum that is a majority of $G(s)$ with at least one main. It then proposes the command "remove the failed main" (line L4). Once that command is decided, the next slot uses the new configuration (line L8). The leader sends the state to the new mains, and the auxiliaries forget their votes (lines L9 and L13). The paper lists these steps as a sequence of seven: a new leader if needed, finishing the open instances with the help of the auxiliaries, the reconfiguration, $\alpha$ no-ops so that it takes effect, bringing the mains up to date, and letting the auxiliaries forget. With $\alpha = 1$ no no-ops are needed.

**The new configuration.** Removing a main $m$ gives $M' = M \setminus \{m\}$. If $|M'| < \lceil |G'|/2 \rceil$, an auxiliary is also dropped, so that $M'$ still meets every majority of $G'$. From $f + 1$ mains and $f$ auxiliaries, one removal gives $f$ mains and $f$ auxiliaries. A leader never asks to remove itself, and a command that would remove the last main changes nothing.

## Example

Take $f = 1$: mains $p_0$ (the leader) and $p_1$, auxiliary $p_2$.

| step | event | quorum used | $p_2$ stores |
|---|---|---|---|
| 1 | slots 0 to 3: ACCEPT to $p_0, p_1$; both answer | $\{p_0, p_1\} = M$ | nothing |
| 2 | $p_1$ crashes; the ACCEPT of slot 4 gets no answer from $p_1$ | | nothing |
| 3 | timeout: resend slot 4 to $p_0, p_1, p_2$; $p_0$ and $p_2$ answer | $\{p_0, p_2\}$, a majority with a main | the vote of slot 4 |
| 4 | slot 5: the command "remove $p_1$", accepted by $p_0, p_2$ | $\{p_0, p_2\}$ | the votes of slots 4 and 5 |
| 5 | from slot 6: $M = \{p_0\}$, $G = \{p_0, p_2\}$; FORGET(6) to $p_2$ | | nothing |
| 6 | slots 6 and later: ACCEPT to $p_0$ only | $\{p_0\} = M$ | nothing |

From step 5 on, the system tolerates no more failure of $p_0$, since $p_0$ alone holds the state. A real deployment then adds a new main, with another reconfiguration command.

## Correctness

**Safety.** Each slot is a single-decree Paxos instance whose quorums come from $C(s)$, and any two quorums of one configuration meet. So the Paxos proof applies to each slot. All processors agree on $C(s)$, because it is a function of the commands chosen in slots before $s$, and those are unique by induction on $s$. A promise for ballot $b$ covers all later slots, as in Multi-Paxos. An auxiliary that has forgotten a slot never promises for it (line L13), so a forgotten vote can never be missing from a quorum's reports. The full proof is below.

**Liveness.** Progress needs a stable leader, as in Paxos, and a live quorum of the current configuration. Lamport and Massa assume that the set of nonfaulty processors does not change too fast: after a failure, the system must have time to finish the reconfiguration before the next failure. Two mains that fail at once, with $f = 1$, stop the system, since then only the auxiliary is up.

## Complexity

Let $k$ be the number of commands, with a stable leader.

- **No failure.** Each command costs $f + 1$ ACCEPT messages and $f + 1$ answers, so $\Theta(fk)$ messages in all. Paxos with $2f + 1$ acceptors sends $2f + 1$ of each. The auxiliaries get zero messages.
- **Latency.** Two message delays from the leader to the decision, as in Multi-Paxos. The leader must wait for all $f + 1$ mains, so one slow main slows every command.
- **A main fails.** One timeout, then the open slots and the reconfiguration command are decided with $2f + 1$ processors, plus the state transfer to the new mains.
- **Hardware.** $f + 1$ machines with full storage and $f$ machines that store only the votes of the last few slots.

## Properties

- **Same safety as Paxos.** No timing assumption is needed for agreement.
- **Unanimity of mains in the steady state.** The quorum $M$ needs every main. This is the cost of using fewer full copies.
- **Auxiliaries are stateless in the long run.** They hold state only between a failure and the end of the reconfiguration.
- **Needs reconfiguration.** Without the "remove" command, one failed main would force the auxiliaries to work forever.

## Variants and improvements

- **[Vertical Paxos](/vertical-paxos/).** An external master sets the configuration of each ballot, so the replicas need only $f + 1$ machines plus a master service.
- **[Flexible Paxos](/flexible-paxos/).** A phase 2 quorum of all $f + 1$ mains needs a phase 1 quorum of only $f + 1$ out of $2f + 1$.
- **[Primary-backup replication](/primary-backup-replication/).** With $f + 1$ replicas and an external service for reconfiguration, it has the same resource cost.

## When to use it

Use Cheap Paxos when machines that store the full state are expensive, failures are rare, and a short pause after a failure is acceptable. A typical case is a small cluster of two big servers with one small witness machine. It is a poor choice when the network is slow or a main is often slow, because each command waits for all mains.

## Pitfalls

- **Forgetting too early.** Line L13 may run only after line L9 has given the decisions to the new mains. An auxiliary that forgets earlier can lose a chosen value.
- **Promising for forgotten slots.** Line L10 must refuse a PREPARE for a slot that the auxiliary has forgotten. A processor that reports "no vote" instead lets a stale leader choose a second value with a quorum of auxiliaries and itself.
- **A configuration with too few mains.** Line L8 must keep $|M| \ge \lceil |G|/2 \rceil$. Removing a main without dropping an auxiliary can make $M$ and a majority of $G$ disjoint.
- **Starting a slot too early.** The leader may work on slot $s$ only when $C(s)$ is known, so with window $\alpha$ only when slot $s - \alpha$ is decided. Line L8 moves to the next slot only after the decision.
- **A slow main taken for a failed one.** Line L7 removes a slow main. This keeps safety, but each wrong removal reduces the fault tolerance until a new main joins.

## Implementations

## History

Lamport and Massa presented Cheap Paxos at DSN 2004. It builds on the dynamic Paxos of the same paper, in which the configuration is part of the state of the machine and a change takes effect $\alpha$ instances later, an idea already sketched in Paxos Made Simple.

## References
