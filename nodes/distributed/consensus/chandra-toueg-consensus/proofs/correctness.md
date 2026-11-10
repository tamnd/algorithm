---
title: The Chandra-Toueg algorithm solves consensus with diamond-S and a majority of correct processes
proves: [correctness, termination]
status: full
---

**Claim.** In the asynchronous model with $n$ processes, reliable links, at most $f$ crashes with $n > 2f$, and a failure detector of class $\Diamond\mathcal{S}$, each run of the algorithm has these properties. (Uniform agreement) No two processes decide different values. (Validity) Each decision is the input of some process. (Termination) Each correct process decides.

**Setup.** The failure detector gives each process $p$ a set of suspected processes at each time. Class $\Diamond\mathcal{S}$ means two things. *Strong completeness*: there is a time after which every crashed process is suspected by every correct process for ever. *Eventual weak accuracy*: there is a correct process $\ell$ and a time after which no correct process suspects $\ell$. A process never suspects itself; this costs nothing, because a process can remove itself from the output.

Reliable broadcast of the decision is built at line L14: a process that gets $(\text{decide}, v)$ for the first time sends it to all others, and only then decides. It has two properties. (Integrity) A process decides $v$ only if some coordinator sent $(\text{decide}, v)$ at line L13. (Uniform delivery) If any process decides, every correct process decides. Proof of uniform delivery: let $p$ decide. Process $p$ decides only after it has sent the message to all others, so its relay is complete. Links are reliable, so every correct process gets the message from $p$ and decides when it gets it.

The *majority* is $\lceil (n+1)/2 \rceil = \lfloor n/2 \rfloor + 1$. Two sets of a majority size intersect. Since $n > 2f$, the correct processes form a majority. The coordinator of round $r$ is $c_r = (r \bmod n) + 1$. The pair $(est, ts)$ of a process is its estimate and the round in which it last took that estimate from a proposal, with $ts = 0$ for the input.

**Fact 1.** In each round $r$, the coordinator $c_r$ sends at most one proposal, at line L7. A process sets $(est, ts) = (v, r)$ at line L9 only when $v$ is that proposal. So every pair with $ts = t \ge 1$ has as its estimate the proposal of round $t$.

**Fact 2.** The value of $ts$ at a process never decreases: it is set to the current round, and rounds increase.

**Lemma 1 (validity of estimates).** Every estimate, proposal and decision is the input of some process.

*Proof.* By induction on time. Inputs are inputs. A proposal is an estimate that the coordinator received (line L7). An estimate changes only to a proposal (line L9). A decision is an estimate of a coordinator (line L13) passed on unchanged at line L14. $\square$

**Lemma 2 (locking).** Let $r$ be a round in which the coordinator sends $(\text{decide}, v)$ at line L13. Then for every round $r' \ge r$, the proposal of round $r'$, if any, is $v$.

*Proof.*

1. The coordinator $c_r$ sent the decision because a majority $A$ of processes replied ack in round $r$ (line L13). A process acks in round $r$ only after it sets $(est, ts) = (u, r)$ at line L9, where $u$ is the proposal of round $r$. The coordinator also acks its own proposal, because it never suspects itself, so its estimate at line L13 is $u$. So $u = v$, and every process in $A$ has $ts \ge r$ from round $r$ on, by Fact 2.
2. Induction on $r'$. For $r' = r$, the proposal is $u = v$.
3. Let $r' > r$, and assume that the proposals of rounds $r, \ldots, r' - 1$ are $v$. The coordinator of round $r'$ chose its proposal from the estimates of a majority $B$ of processes, sent at line L4 of round $r'$ (lines L6 and L7). Since $A \cap B \ne \emptyset$, some $q \in A$ sent an estimate in round $r'$. Process $q$ sent it after it completed round $r$, so its $ts$ is at least $r$ and at most $r' - 1$. The coordinator takes an estimate with the largest $ts$ among those it received, so the chosen pair has some $ts = t$ with $r \le t \le r' - 1$. By Fact 1 its estimate is the proposal of round $t$, which is $v$ by the induction hypothesis. So the proposal of round $r'$ is $v$. $\square$

**Agreement.** Let $r$ be the smallest round in which a coordinator sends $(\text{decide}, v)$. A coordinator of a round $r' \ge r$ that sends a decision sends its own estimate, which is the proposal of round $r'$ (step 1 of Lemma 2), so it sends $v$ by Lemma 2. By integrity, every decision is one of these values, so every decision is $v$. This holds also for a process that decides and then crashes.

**Validity.** By Lemma 1.

**Lemma 3 (no correct process blocks).** If no correct process ever decides, then every correct process completes every round.

*Proof.* By induction on $r$. Assume every correct process completed round $r - 1$, or let $r = 1$. Every correct process sends its estimate of round $r$ to $c_r$.

1. *Line L6.* If $c_r$ is correct, it gets estimates from all correct processes, which form a majority.
2. *Line L8.* Let $p$ be correct. If $c_r$ is correct, by step 1 it sends its proposal to all, and $p$ gets it. If $c_r$ crashes, by strong completeness $p$ suspects it from some time on. Either way $p$ passes line L8, then replies at line L9 or L10.
3. *Line L12.* If $c_r$ is correct, it gets a reply from each correct process, which form a majority.

So every correct process completes round $r$. $\square$

**Termination.** By uniform delivery of the decision, it is enough to show that some correct process decides. Assume that no correct process ever decides.

1. Choose a time $T$ such that all faulty processes have crashed by $T$, every crashed process is suspected by every correct process from $T$ on, and the correct process $\ell$ is suspected by no correct process from $T$ on. Such a $T$ exists, because there are finitely many faulty processes and both properties of $\Diamond\mathcal{S}$ hold from some time on.
2. At time $T$, each process is in some round. Let $R$ be the largest of these rounds over all processes, the crashed ones included. Each process has sent only finitely many messages by $T$, all of rounds at most $R$.
3. By Lemma 3, every correct process goes through every round. Choose a round $r > R$ with $c_r = \ell$; one exists among any $n$ consecutive rounds.
4. Every message of round $r$ is sent after $T$, and only by correct processes, because the faulty ones have crashed by $T$ and never reached round $r$.
5. $\ell$ is correct, so by Lemma 3 it gets a majority of estimates and sends its proposal to all. Each correct process $p$ waits at line L8 for the proposal or a suspicion of $\ell$. It is after $T$, so $p$ does not suspect $\ell$, and it waits until the proposal arrives. Then it replies ack.
6. Every reply of round $r$ comes from a correct process after $T$, so every reply is an ack. At line L12, $\ell$ gets a majority of acks and no nack, and sends $(\text{decide}, est)$ at line L13. Since $\ell$ is correct, the message reaches $\ell$ itself and all others, and $\ell$ decides at line L14.

This contradicts the assumption. So some correct process decides, and then every correct process decides. $\blacksquare$
