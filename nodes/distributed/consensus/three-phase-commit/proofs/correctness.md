---
title: Three-phase commit is safe and non-blocking with crash failures in a synchronous system
proves: [correctness]
status: sketch
---

This is a proof sketch. It follows the structure of Skeen's argument and the lines L1 to L12 of the page. The steps that are only outlined are marked.

**Model.** Lock-step synchronous rounds. A message sent in round $r$ arrives at the start of round $r+1$. A process can crash in some round; then it sends only some of its messages of that round and stops for good. The failure detector is perfect: at the start of round $r+1$ every live process knows the set of processes that crashed in rounds $1$ to $r$. The network never partitions. In each round a process first handles its inbox, then acts as leader if it is one.

**Lemma 1 (one leader at a time).** In each round all live processes agree on the leader, which is the live process with the smallest id. A leader stays leader until it crashes, and each new leader is live in the round it takes over.

*Proof.* Every live process computes the same set of live processes at the start of a round, and line L7 takes its minimum. Live sets only shrink, so the minimum changes only when the current minimum crashes. $\square$

So the run splits into reigns: the coordinator, then a sequence of termination leaders $\ell_1 < \ell_2 < \cdots$. Only the leader of the current reign sends PRE-COMMIT, COMMIT or ABORT, and it is in state p, c or a when it sends them. A participant moves to p, c or a on such a message, and to a also when it votes no.

**Lemma 2 (validity).** If a process enters p or c, then every participant voted yes.

*Proof.* The first process to enter p does it in line L3, since line L12 needs an earlier p and a PRE-COMMIT message needs a sender in p. Line L3 needs YES from all participants. The first process to enter c does it in line L5, which needs an earlier p. $\square$

**Lemma 3 (one transition apart).** At the moment a leader decides in line L3 or in lines L9 to L12, the states it uses are the current states of all live processes, and no PRE-COMMIT, COMMIT or ABORT is in flight.

*Sketch.* A new leader sends STATE-REQ in the round it takes over. Any decision message of the crashed leader was sent in the round of the crash, so it arrives in that same round and is handled before the STATE replies are computed in the next round. During the reign no other process sends decision messages (Lemma 1). For the coordinator in line L3, no decision message exists yet. $\square$

**Lemma 4 (concurrency sets).** In every round:

1. If some process, live or crashed, is in c, then every live process is in p or c, or receives PRE-COMMIT or COMMIT in the next round.
2. If some process, live or crashed, is in a, then no live process is in p or c, and no PRE-COMMIT or COMMIT is in flight.

*Sketch, by induction on the rounds.* For part 1, take the first entry into c. It is by line L5 in round $r$, so the same leader sent PRE-COMMIT in round $r-2$ and did not crash in round $r-2$ (it acts in round $r$). So every process live in round $r-1$ received PRE-COMMIT and entered p, unless it was in a; part 2 at round $r-2$ rules that out, because the leader itself was in p. After that, every leader sees c or p in lines L9 to L12 (Lemma 3), and no leader sees a (part 2), so every leader moves the others to c through p. For part 2, an abort comes from a no vote, from line L3 without all yes (then no p exists, by Lemma 2), or from lines L9 and L11, where by Lemma 3 the leader saw no live process in p or c and no message in flight. After that, each later leader sees a or sees no p, and decides abort again. The full induction checks each line against both parts. $\square$

**Theorem 1 (agreement).** No process enters c while another process is in a.

*Proof.* By Lemma 4, a process in a forbids any live process in p or c and any message that leads to them, so no process can enter c later; and a process in c makes every live process move to p or c, so no leader decides abort later (Lemma 3 and lines L9 to L12). $\square$

**Theorem 2 (non-blocking).** If at least one process stays up, every live process enters c or a within a number of rounds that is linear in the number of crashes.

*Proof.* Each reign that does not end in a crash ends after at most 5 rounds with a decision message that reaches every live process. Each leader crash starts a new reign, and there are at most $n$ crashes, since the processes do not recover. $\square$

**Why it fails without the model.** Lemma 3 needs a perfect failure detector. If a partition makes two groups each see the other as crashed, there are two leaders at once, and Lemma 1 fails. The page shows a run where the side with a process in p commits and the side with only w aborts.
