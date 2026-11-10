---
tag: MSG4TW
kind: algorithm
slug: raft
name: Raft
aliases:
- Raft consensus
area: distributed/consensus
level: core
summary: A consensus algorithm for a replicated log. A leader, elected for a numbered term, copies its log to the other servers, and an entry commits when a majority stores it.
solves: [consensus-problem, total-order-broadcast]
model: asynchronous-model
complexity:
  vars: {n: the number of servers}
  time: {best: Θ(1)}
  messages: {best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: false, recursive: false}
history:
  year: 2014
  people: [Diego Ongaro, John Ousterhout]
  note: Ongaro and Ousterhout presented Raft at USENIX ATC 2014 as a consensus algorithm designed to be easy to understand, and Ongaro gave the full design in his Stanford thesis of the same year.
prereqs: [consensus-problem, replicated-state-machine, quorum, crash-failure, asynchronous-model]
see_also: [paxos, multi-paxos, viewstamped-replication, zab, log-compaction, cluster-reconfiguration, leader-lease, split-brain]
sources:
  - url: https://www.usenix.org/conference/atc14/technical-sessions/presentation/ongaro
    title: Diego Ongaro and John Ousterhout, In search of an understandable consensus algorithm, USENIX Annual Technical Conference (ATC), 2014
    locator: Section 5 (5.2 leader election, 5.3 log replication, 5.4 safety with the election restriction, Figure 8 and the safety argument), Figure 2 (the summary of the rules), Figure 3 (the five safety properties), Section 6 (membership changes), Section 7 (log compaction)
  - paper: "Diego Ongaro, Consensus: bridging theory and practice, PhD thesis, Stanford University, 2014"
    locator: Chapter 3 (basic Raft), Chapter 4 (cluster membership changes), Chapter 5 (log compaction)
  - paper: "Heidi Howard and Richard Mortier, Paxos vs Raft: have we reached consensus on distributed consensus?, Workshop on Principles and Practice of Consistency for Distributed Data (PaPoC), 2020"
    locator: the comparison of leader election in Paxos and Raft
---

Raft is a [consensus](/consensus-problem/) algorithm that keeps a [replicated log](/replicated-log/) on $n$ servers, which feed it to a [replicated state machine](/replicated-state-machine/). Time is cut into numbered terms, each term has at most one leader, and only the leader adds entries to the log. An entry commits when a majority of servers store it, and a server can become leader only when its log is at least as up to date as the logs of a majority. These two rules keep all committed entries in every later leader, so all servers apply the same commands in the same order, in the [asynchronous model](/asynchronous-model/) with [crash failures](/crash-failure/) and restarts.

## In plain words

A group of servers keeps one shared list of commands. Clients send commands to the leader. The leader adds each command to the end of its list and sends it to the others. When more than half of the servers store a command, it is final, and all servers run it.

If the leader stops, the others stop hearing from it. After a short random wait, a server asks to become leader for a new, larger period number. Each server gives one vote in each period, and it refuses a server whose list is older than its own. A server with more than half of the votes leads. Any two halves share a server, so the new leader has every final command. A server whose list disagrees with the leader's list throws away its different part and copies the leader's part.

## The problem

There are $n$ servers, each with a deterministic state machine. Clients send commands. The goal is a sequence of committed commands that only grows, such that every server applies exactly this sequence, in order. This is [total-order broadcast](/total-order-broadcast/), and it is the same as solving the [consensus problem](/consensus-problem/) once for each index of the log.

The model for safety is the [asynchronous model](/asynchronous-model/). Messages can be delayed without bound, lost, duplicated and reordered, but not changed. A server can crash and later restart. Each server keeps three variables on stable storage: currentTerm, votedFor and the log. It writes them before it sends a message that depends on them, and a crash loses only the other variables. There is no Byzantine behavior. For liveness the model is [partial synchrony](/partial-synchrony/) with a majority of servers up.

## The algorithm

The log of a server is an array of entries $(t, x)$, where $t$ is the term in which a leader created the entry and $x$ is a command. Index 0 holds a sentinel of term 0. Here lastIndex is the last index of the log and lastTerm is the term of the entry there. A server is a follower, a candidate or a leader. A server that sees a larger term in any message moves to that term and becomes a follower (STEP-DOWN).

```pseudo id=main
SERVER s, with currentTerm, votedFor and log on stable storage
on an election timeout, if s is not leader and the timer was not reset:
L1  currentTerm ← currentTerm + 1; role ← candidate; votedFor ← s
L2  votes ← {s}
L3  send REQUESTVOTE(currentTerm, lastIndex, lastTerm) to all other servers
on REQUESTVOTE(t, li, lt) from c:
L4  if t > currentTerm then STEP-DOWN(t)
L5  upToDate ← lt > lastTerm or (lt = lastTerm and li ≥ lastIndex)
L6  grant ← t = currentTerm and votedFor ∈ {⊥, c} and upToDate
L7  if grant then votedFor ← c; reset the election timer
L8  send VOTE(currentTerm, grant) to c
on VOTE(t, g) from v:
L9  if t > currentTerm then STEP-DOWN(t); return
L10 if role = candidate and t = currentTerm and g then votes ← votes ∪ {v}
L11 if role = candidate and |votes| > n/2 then become leader: nextIndex[j] ← lastIndex + 1 and matchIndex[j] ← 0 for each j, matchIndex[s] ← lastIndex, SEND-APPEND to each j ≠ s
on a command x from a client, if role = leader:
L12 append (currentTerm, x) to log; matchIndex[s] ← lastIndex; SEND-APPEND to each j ≠ s
SEND-APPEND(j)                                    ▷ with no entries, this is a heartbeat
L13 p ← nextIndex[j] − 1
L14 send APPEND(currentTerm, p, log[p].term, log[p+1 ..], commitIndex) to j
on APPEND(t, p, pt, E, lc) from the leader ℓ:
L15 if t > currentTerm then STEP-DOWN(t)
L16 if t < currentTerm then send APPENDREPLY(currentTerm, false, 0) to ℓ; return
L17 role ← follower; reset the election timer
L18 if p > lastIndex or log[p].term ≠ pt then send APPENDREPLY(currentTerm, false, 0) to ℓ; return
L19 for k ← 1 to |E|:  i ← p + k
L20     if i ≤ lastIndex and log[i].term ≠ E[k].term then delete log[i ..]
L21     if i > lastIndex then append E[k] to log
L22 if lc > commitIndex then commitIndex ← max(commitIndex, min(lc, p + |E|))
L23 APPLY; send APPENDREPLY(currentTerm, true, p + |E|) to ℓ
on APPENDREPLY(t, ok, m) from j:
L24 if t > currentTerm then STEP-DOWN(t); return
L25 if role ≠ leader or t ≠ currentTerm then return
L26 if ok then matchIndex[j] ← max(matchIndex[j], m); nextIndex[j] ← matchIndex[j] + 1; ADVANCE-COMMIT; if matchIndex[j] < lastIndex then SEND-APPEND(j)
L27 else nextIndex[j] ← max(1, nextIndex[j] − 1); SEND-APPEND(j)
ADVANCE-COMMIT
L28 for N ← lastIndex down to commitIndex + 1:
L29     if log[N].term = currentTerm and |{j : matchIndex[j] ≥ N}| > n/2 then commitIndex ← N; APPLY; return
APPLY
L30 while lastApplied < commitIndex: lastApplied ← lastApplied + 1; apply log[lastApplied].x to the state machine
STEP-DOWN(t)
L31 currentTerm ← t; role ← follower; votedFor ← ⊥
```

**Terms.** A term is a number that only grows (lines L1 and L31). It acts as a logical clock: a message from an older term is stale and is refused (lines L16 and L25). Each server votes at most once in each term, and votedFor is on stable storage, so a restart cannot give a second vote.

**Leader election (lines L1 to L11).** A follower that hears nothing from a leader for one election timeout starts a new term, votes for itself and asks the others for votes. Each server picks its timeout at random from a fixed interval (150 to 300 ms in the paper), so in most elections one server times out first and wins before the others start. If the votes split and nobody gets a majority, the candidates time out again with new random timeouts.

**The election restriction (line L5).** A voter grants its vote only when the candidate's log is at least as up to date as its own: the last term is larger, or the last terms are equal and the candidate's log is at least as long. This is what makes a new leader hold every committed entry, so the leader never needs to fetch entries from others.

**Log replication (lines L12 to L27).** The leader appends each new command with its own term and sends APPEND messages. Each APPEND carries the index and term of the entry just before the new entries. The follower accepts only if its log has an entry with that index and term (line L18). This is the consistency check. On a reject, the leader moves nextIndex one step back and tries again (line L27), until the two logs agree at prevIndex. Then the follower deletes its suffix from the first entry whose term differs (line L20) and copies the leader's entries. A follower deletes only on a conflict, so an old, delayed APPEND cannot cut off newer entries.

**The commit rule (lines L28 and L29).** The leader commits index $N$ when a majority store index $N$ and the entry at $N$ has the leader's current term. All earlier entries commit with it. The leader never commits an entry of an older term by counting copies. The run of the next section shows why. Followers learn the commit index from the leaderCommit field of the next APPEND (line L22).

## Example

This is the run of Figure 8 of the paper, with five servers S1 to S5. The cell "1a" means an entry of term 1 with command a at index 1, and "2b 4d" means b of term 2 at index 1 and d of term 4 at index 2.

| step | event | S1 | S2 | S3 | S4 | S5 |
|---|---|---|---|---|---|---|
| a | S1 leads term 1 and copies a to S2 only | 1a | 1a | | | |
| b | S1 crashes. S5 wins term 2 with the votes of S3, S4 and S5, appends b, and crashes | 1a | 1a | | | 2b |
| c | S1 restarts, wins term 3 with S2 and S3, and copies a to S3 | 1a | 1a | 1a | | 2b |
| d | S1 crashes. S5 restarts, wins term 4 with S2, S3 and S4, and copies its log | 1a | 2b 4d | 2b 4d | 2b 4d | 2b 4d |

After step c, the entry a is on three of five servers. A leader that commits by counting copies commits a in step c, and S1 applies a at index 1. In step d, S5 still wins: its last term 2 is larger than the last term 1 of S2 and S3, so line L5 holds for them. S5 then overwrites a with b, and S2 to S5 apply b at index 1. Two servers applied different commands at the same index, which breaks state machine safety.

With line L29, S1 does not commit a in step c, because a has term 1 and S1 leads term 3. No server applies anything at index 1 before step d, and every server later applies b and then d.

If S1 in step c also appends a command c of term 3 and copies it to S2 and S3, then line L29 commits index 2, and index 1 with it. In step d, S2 and S3 now have last term 3, which is larger than 2, so they refuse S5, and S5 gets only the votes of S4 and itself. It cannot win. The committed a and c stay.

## Correctness

The safety proof follows the Raft paper: election safety, log matching, leader completeness, then state machine safety.

- **Election safety.** Each server votes at most once in each term, and two majorities share a server, so each term has at most one leader.
- **Log matching.** If two logs hold entries with the same index and term, the logs are equal up to that index. One leader creates at most one entry for each index in its term, and the consistency check of line L18 extends the property by induction over the steps of the run.
- **Leader completeness.** An entry committed in term $T$ is in the log of every leader of a term above $T$. The majority that stores the entry and the majority that elects a later leader share a voter, and line L5 then forces the leader's log to hold the entry. This step needs the committed entry to have term $T$, which is what line L29 checks.
- **State machine safety.** A server applies only entries up to its commit index, and committed entries are never deleted, so no two servers apply different entries at the same index.

These properties need no timing assumption and hold for any number of crashes and restarts. The full proof is below.

### Liveness

Raft cannot always make progress: by the [FLP impossibility](/flp-impossibility/) result, no algorithm decides in every asynchronous run with one crash. The paper states the timing requirement as broadcastTime ≪ electionTimeout ≪ MTBF, where broadcastTime is the time of one round of messages and MTBF is the mean time between failures of one server. Under [partial synchrony](/partial-synchrony/), with a majority of servers up and connected, random timeouts make each election end with a single winner with a probability that does not depend on the past elections, so a leader is elected after a finite expected number of elections, and from then on each command commits. This liveness argument is a sketch and is not proved on this page.

## Complexity

In the steady state, one command costs one APPEND to each follower and one reply from each: $2(n-1)$ messages. The leader commits after one round trip to the fastest majority, so the latency is one round trip plus one write to stable storage at the leader and at a majority. Followers learn of the commit on the next APPEND, which can carry the next commands. One APPEND can carry many entries, so a batch of $k$ commands also costs $2(n-1)$ messages.

An election costs $n-1$ requests and $n-1$ replies for each candidate. A lagging follower costs one round trip for each step back of nextIndex in line L27, so a follower that differs in $k$ entries can need $k$ round trips. The paper describes an optimization: the follower returns the term of the conflicting entry and the first index of that term, which cuts this to one round trip for each conflicting term.

The leader keeps nextIndex and matchIndex for each follower, which is $\Theta(n)$ extra space. Each server keeps its full log, which grows without bound until [log compaction](/log-compaction/) replaces a prefix with a snapshot.

## Properties

- Strong leader: entries flow only from the leader to the followers, and a leader never deletes or overwrites its own entries (Leader Append-Only).
- The five safety properties of Figure 3 of the paper are election safety, leader append-only, log matching, leader completeness and state machine safety.
- It tolerates $f$ crashed servers when $n \ge 2f + 1$, and it needs a majority up to make progress.
- Safety holds in the asynchronous model, and liveness needs partial synchrony.
- A server that falls behind is repaired by the leader without a separate recovery protocol.

## Variants and improvements

- **Membership changes.** Changing the set of servers in one step can make two disjoint majorities, one of the old and one of the new set. The paper uses joint consensus, and the thesis adds a simpler change of one server at a time. See [cluster reconfiguration](/cluster-reconfiguration/).
- **Log compaction.** A server replaces a committed prefix of its log by a snapshot of the state machine, and a leader sends InstallSnapshot to a follower that needs entries it has deleted. See [log compaction](/log-compaction/).
- **Reads.** A leader that answers reads from its own state can be deposed without knowing it and return stale data. The leader must first confirm with a majority that it still leads, or hold a [leader lease](/leader-lease/), which needs bounded clock drift.
- **PreVote and CheckQuorum.** The thesis describes extensions: a server first checks that it could win before it raises its term, so a server that was cut off does not depose a working leader when it returns.
- **Relation to Paxos.** Raft is close to [Multi-Paxos](/multi-paxos/) and to [Viewstamped Replication](/viewstamped-replication/). Its term is a [ballot number](/ballot-number/). Howard and Mortier show that the main difference is leader election: a Raft voter refuses a candidate with an older log, while a Paxos leader collects the accepted entries from a majority and re-proposes them.

## When to use it

Use Raft when a small group of servers (usually three or five) must keep one consistent log or configuration store under crash failures, for example a metadata service, a lock service or the replicas of one shard. Use it when readers of the code must be able to check it: the rules fit on one page (Figure 2 of the paper). Do not use it against Byzantine servers: see [PBFT](/pbft/) and [Byzantine state machine replication](/byzantine-state-machine-replication/). One leader handles all writes, so throughput is bound by one server and its network link. Systems that need more split the data into many Raft groups.

## Pitfalls

- **Committing an old entry by counting copies.** This is the Figure 8 error. Commit only entries of the current term, and earlier entries commit with them.
- **Not writing votedFor and currentTerm to stable storage before a reply.** A server that restarts and forgets its vote can vote twice in one term, and two leaders can follow.
- **Truncating the log on every APPEND.** A follower must delete only from the first conflicting entry. An old, reordered APPEND that is a prefix of the log must not cut off later entries.
- **Equal election timeouts.** Without randomness, candidates can split the votes again and again.
- **Stale reads.** A deposed leader that answers reads from its own state returns old data. See the read variant above and [split-brain](/split-brain/).
- **Duplicate client commands.** A client that retries after a timeout can make a command run twice. The paper gives each command a client id and a serial number, and the state machine ignores repeats.
- **Changing many servers at once.** This can make two leaders in one term. Use joint consensus or one change at a time.

## Implementations

## History

Diego Ongaro and John Ousterhout presented Raft at the 2014 USENIX Annual Technical Conference. Their goal was a consensus algorithm that is easier to understand than Paxos, so they split the problem into leader election, log replication and safety, and they reduced the number of states. The paper reports a user study in which students answered questions about Raft and Paxos, and it gives a safety argument, with a formal specification and proof in Ongaro's thesis of the same year. The thesis adds membership changes of one server at a time, log compaction and client interaction.

## References
