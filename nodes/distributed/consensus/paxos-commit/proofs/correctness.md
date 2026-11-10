---
title: Paxos Commit is a correct non-blocking atomic commit protocol
proves: [correctness]
status: full
---

The model is asynchronous, with crash failures and stable storage. There are $N$ RMs, $2F + 1$ acceptors and some leaders. Messages can be delayed, reordered and duplicated but not changed. Ballots are $0$ and pairs $(k, \ell)$ with $k \ge 1$, ordered with $0$ lowest; in instance $r$, ballot 0 belongs to RM $r$ and ballot $(k, \ell)$ belongs to leader $\ell$, which uses it at most once.

A value $v$ is *chosen* in instance $r$ at ballot $b$ when $F + 1$ acceptors have accepted $(b, v)$ in instance $r$.

**Lemma 1 (one value per ballot).** In each instance, all accepted values at one ballot are the same.

*Proof.* At ballot 0 of instance $r$, only RM $r$ sends a 2a message (line L3), with its one vote, which it wrote to stable storage before sending. At ballot $(k, \ell)$, only leader $\ell$ sends 2a messages, once, at line L11. $\square$

**Lemma 2 (phase 1 keeps chosen values).** If $v$ is chosen in instance $r$ at ballot $b$, then every value accepted in $r$ at a ballot $b' > b$ is $v$.

*Proof.* By induction on $b'$. The leader of $b'$ received 1b messages from a set $P$ of $F + 1$ acceptors, and $F + 1$ acceptors $A$ accepted $(b, v)$. Since $2(F + 1) > 2F + 1$, some $a \in A \cap P$ exists. Acceptor $a$ promised $b' > b$ at line L9 and never accepts a lower ballot afterwards (line L4), so it accepted $(b, v)$ before its 1b and reported a ballot $\ge b$ in instance $r$. The highest ballot $b''$ reported in $r$ then satisfies $b \le b'' < b'$, and its value is $v$: by Lemma 1 if $b'' = b$, and by the induction hypothesis if $b'' > b$. Line L10 picks it. $\square$

**Lemma 3 (one chosen value per instance).** Each instance chooses at most one value.

*Proof.* If $v$ is chosen at $b$ and $w$ at $b' \ge b$, then $w = v$, by Lemma 1 if $b' = b$, and by Lemma 2 otherwise. $\square$

**Lemma 4 (only RM $r$ can be the source of Prepared in $r$).** If Prepared is accepted in instance $r$ at any ballot, then RM $r$ voted Prepared.

*Proof.* By induction on the ballot. At ballot 0, the value is RM $r$'s vote. At a ballot $b > 0$, line L10 proposes Prepared in $r$ only if some acceptor reported Prepared in $r$ at a lower ballot, which by the hypothesis means RM $r$ voted Prepared. $\square$

**Theorem 1 (agreement).** No two leaders decide different outcomes, and so no two RMs learn different outcomes.

*Proof.* A leader decides at line L7 only from values it saw chosen at line L6. By Lemma 3, all leaders see the same chosen value for each instance. Commit needs Prepared chosen in all $N$ instances, and Abort needs Aborted chosen in one; by Lemma 3 both cannot hold. RMs learn the outcome only from leaders (line L12). $\square$

**Theorem 2 (validity).** If the outcome is Commit, every RM voted Prepared.

*Proof.* Commit needs Prepared chosen, so accepted, in every instance. By Lemma 4 every RM voted Prepared. $\square$

**Theorem 3 (non-triviality).** If every RM votes Prepared and no process fails or times out, the outcome is Commit.

*Proof.* Every RM gets Prepare (line L2) and sends Prepared at ballot 0 to $F + 1$ acceptors. Nothing else is accepted because no leader starts phase 1, so each of those acceptors sends one 2b with all $N$ votes (line L5), and the leader sees Prepared chosen in every instance and decides Commit. $\square$

**Theorem 4 (non-blocking).** Suppose at most $F$ acceptors crash, messages between live processes are delivered, and eventually one live leader starts a ballot that no other leader exceeds. Then every live RM learns an outcome.

*Proof.* That leader's 1a reaches the $F + 1$ or more live acceptors, whose promises are below its ballot, so it gets $F + 1$ replies (line L9) and sends 2a for all instances (line L11). The live acceptors accept, since no higher ballot exists, and reply 2b, so every instance chooses a value at that ballot (line L6). The leader decides and sends the outcome to every RM (line L7). $\blacksquare$

When $F = 0$ the only acceptor must be live for Theorem 4, which is the blocking of Two-Phase Commit. Theorems 1 to 3 do not depend on $F$.
