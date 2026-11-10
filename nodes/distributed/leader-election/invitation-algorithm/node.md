---
tag: 2ZVXPK
kind: algorithm
slug: invitation-algorithm
name: Invitation algorithm
aliases:
- Garcia-Molina's invitation algorithm
- Group merging election
area: distributed/leader-election
level: advanced
summary: Election for asynchronous systems that can split. Processes form groups, each with one coordinator, and coordinators merge groups by invitation. Groups stay consistent; one leader is not promised.
model: asynchronous-model
complexity:
  vars: {k: the number of processes in the groups that merge}
  time: {worst: O(1)}
  messages: {worst: O(k)}
  space: {extra: O(k)}
properties: {deterministic: true, recursive: false}
history:
  year: 1982
  people: [Hector Garcia-Molina]
  note: Gave a weaker but achievable goal for elections when time bounds and a connected network cannot be assumed.
prereqs: [bully-algorithm, asynchronous-model, explicit-leader-election]
see_also: [bully-algorithm, omega-failure-detector, raft, paxos, consensus-problem, synchronous-model]
sources:
  - paper: doi:10.1109/TC.1982.1675885
    title: Hector Garcia-Molina, Elections in a Distributed Computing System, IEEE Transactions on Computers C-31(1), 1982
    locator: pages 48 to 59 (the assertions for the asynchronous case with partitions, and the Invitation Algorithm)
---

The invitation algorithm is Garcia-Molina's election algorithm for systems in which messages can be slow without bound and the network can split into parts. In such a system no algorithm can make sure that there is exactly one leader, because a slow process cannot be told apart from a crashed one. So the algorithm promises less: the processes form *groups*, each group has one coordinator, and all members of a group agree on who it is. Coordinators look for other coordinators from time to time and merge their groups into one by sending invitations. When the network is stable and fast, the groups merge into one group in each connected part.

## In plain words

People work in teams, and each team has one leader. Messages can be very slow, and sometimes the building is split so that people in different parts cannot talk.

From time to time, each team leader calls around to find other team leaders. If it finds some, it waits a short time (higher-ranked leaders wait less) and then invites the other leaders and its own team into a new, bigger team. A leader who accepts passes the invitation on to its own team. Everyone who accepts joins the new team, and the inviting leader confirms who is in it.

Team members check from time to time that their leader is still there. If the leader does not answer, they start a team of one. So teams can break up and join again, but in each team everyone agrees on the leader.

## The problem

There are $n$ processes with distinct priorities. The system is [asynchronous](/asynchronous-model/): messages can take any time and can be lost when the network splits into parts, called partitions. Processes can crash and recover. Each process $p$ has a state (*normal*, *election* or *reorganizing*), a group number $\mathit{gid}_p$, and a coordinator $\mathit{coord}_p$.

The goal is Garcia-Molina's weaker form of election:

- **Safety.** At all times, if two processes are in the normal state with the same group number, they have the same coordinator. A normal member is in the member list of its coordinator while the coordinator is still normal in that group.
- **Progress.** If the network and the set of live processes stop changing and messages are timely, the processes in each connected part eventually form one group.

The goal is not that the whole system has one leader. Each partition can have its own group, and even in one partition two groups can exist for a while.

## The algorithm

A group number is a pair $(c, i)$ of a counter and the identifier of the coordinator that made it, so it is unique. Each process starts as the coordinator of a group of one.

```pseudo id=main
INVITATION(i)                                ▷ the code of process i
L1  RECOVER: counter ← counter + 1; gid ← (counter, i); coord ← i; members ← {i}; state ← normal
L2  every period, if normal and coord = i: send AYC to all; answer AYC with yes if coordinator
L3  on a yes from j: found ← found ∪ {j}; set a merge time after the other answers can arrive,
        plus a wait that is shorter for a higher priority
L4  MERGE at that time, if still a normal coordinator: gid ← (counter + 1, i); state ← election
        accepted ← {i}; send INVITE(gid) to found ∪ members; start a timer
L5  on INVITE(g) from c, if state = normal:
L6      if coord = i then send INVITE(g) to each of my members         ▷ pass it on
L7      state ← reorganizing; gid ← g; coord ← c; send ACCEPT(g) to c; start a timer
L8  on ACCEPT(g) from j, if state = election and gid = g: accepted ← accepted ∪ {j}
L9  on the election timer: members ← accepted; state ← normal; send READY(g) to all members
L10 on READY(g), if state = reorganizing and gid = g: state ← normal
L11 every period, if normal and coord ≠ i: send AYT(gid) to coord, who answers yes only if
        it is a normal coordinator of gid with i in members
L12 on a no answer, or no answer in time, or the reorganizing timer: RECOVER
```

AYC means "are you coordinator?" and AYT means "are you there?". Process states other than normal ignore invitations, so a process takes part in at most one merge at a time.

## Example

Take six processes $0, \ldots, 5$ with priority equal to the identifier, all as groups of one. In the first period each coordinator calls the others and gets five yes answers. Process 5 has the highest priority and the shortest wait, so it merges first. It sends INVITE to $0, \ldots, 4$, each of which is a normal coordinator of a group of one, so each one becomes *reorganizing* and sends ACCEPT. When its timer ends, process 5 sends READY to the five members, and they become normal in group $(2, 5)$. The merge uses $5$ INVITE, $5$ ACCEPT and $5$ READY messages. When the other processes reach their merge times, they are no longer coordinators, so they do not merge. In the seeded run in the tests, with delays of 1 to 3 ticks, this is done at tick 29.

Now split the network into $\{0, 2, 4\}$ and $\{1, 3, 5\}$. The members $0, 2, 4$ get no answer from 5, so each starts a group of one by line L12, and then 4 merges them. The result is two groups, one in each part, each with its own coordinator. When the parts join again, coordinators 4 and 5 find each other and 5 merges the two groups.

## Correctness

**Safety.** The group number of a normal process names its coordinator: a process sets $\mathit{gid}$ and $\mathit{coord}$ together, either to $(\cdot, i)$ and $i$ in lines L1, L4 and L9, or to $g$ and the sender $c$ of an invitation for $g$ in line L7, and an invitation for $g$ always comes from, or is passed on for, the process named in $g$. So two normal processes with the same group number have the same coordinator. A member becomes normal in $g$ only by READY$(g)$, which its coordinator sends only to the members in its final list, and the coordinator never changes that list while it stays in $g$. This holds for any message delays, because it uses no timeouts.

**Termination of each step.** The election and reorganizing states end by a timer, so no process stays out of the normal state for ever.

**Progress.** The higher a coordinator's priority, the sooner it merges. When the system is stable, the coordinator with the highest priority in a part finds the others and invites them before they act, and they and their members join. This is a sketch, and the [proof of correctness](proofs/correctness/) states the assumptions it needs. Garcia-Molina does not promise more than this.

## Complexity

**Messages per merge.** Suppose a coordinator merges groups with $k$ processes in total, and nothing fails. Each of the other $k - 1$ processes gets exactly one INVITE, either from the merging coordinator or passed on by its own coordinator, and sends one ACCEPT, and the merging coordinator sends one READY to each. That is $3(k - 1)$ messages. For six groups of one, this is $15$.

**Background messages.** Each coordinator sends $n - 1$ AYC messages in each period, and each member sends one AYT and gets one answer. This cost goes on all the time, because the algorithm must notice changes. In the six process run of the example, the AYC and AYT traffic is much larger than the merge itself.

**Time.** In a stable system with delays at most $\delta$, a merge takes three hops for INVITE, the passed-on INVITE and ACCEPT, then the timer, and one more hop for READY.

## Properties

- **Works without time bounds.** Safety does not depend on timeouts. Timeouts only decide when to give up and start again.
- **Partition tolerant.** Each part keeps working with its own group.
- **Weaker guarantee.** There can be more than one coordinator in the system, even in one connected part for a while.
- **Not tied to the largest identifier.** Any coordinator that merges first becomes the coordinator of the new group. Priorities only make it likely that a high one wins.

## Variants and improvements

- **The bully algorithm.** In a synchronous system without partitions, the [bully algorithm](/bully-algorithm/) gives one global coordinator.
- **Majority groups.** If only a group with a majority of the processes may act, at most one group acts at a time. This is the idea behind the terms of [Raft](/raft/) and the ballots of [Paxos](/paxos/), which add [consensus](/consensus-problem/) on top.
- **Group membership services.** Later work on view-synchronous group membership grew from the same need to agree on who is in a group when the network can split.

## When to use it

Use it when the system must keep working in every part of a split network, and when each part can do useful work under its own coordinator. Do not use it when two coordinators at the same time would be harmful, for example when they could both write to the same data. In that case use a majority based method.

## Pitfalls

- **Reading it as a leader election.** The algorithm does not promise one leader. Two coordinators can exist, and code that runs on the coordinator must allow for that.
- **Merging at the same time.** If two coordinators invite each other at once, both are in the election state and both ignore the other's invitation. The priority wait in line L3 makes this rare but cannot rule it out.
- **Old messages.** A READY or AYT answer from an older group must be ignored. The group number in each message does this.
- **The cost of checking.** The periodic AYC and AYT messages run all the time and can cost much more than the merges.

## Implementations

## History

Garcia-Molina gave the invitation algorithm in 1982, in the same paper as the [bully algorithm](/bully-algorithm/). He argued that in a system where messages can be slow and the network can split, the strong election assertions cannot be met, and he gave weaker assertions about groups. The idea of groups that split and merge became a basis for later work on group membership.

## References
