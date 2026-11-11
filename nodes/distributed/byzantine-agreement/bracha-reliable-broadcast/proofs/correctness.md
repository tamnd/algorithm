---
title: Bracha reliable broadcast has validity, integrity, consistency and totality when n > 3t
proves: [correctness]
status: full
---

**Claim.** In the asynchronous model with $n$ processes, reliable authenticated point-to-point links and at most $t$ Byzantine processes, with $n > 3t$, BRACHA-RBC with sender $s$ has these properties in every run. (Validity) If $s$ is honest and broadcasts $m$, every honest process delivers $m$. (No duplication) An honest process delivers at most once. (Integrity) If $s$ is honest, an honest process delivers only the message $m$ of $s$. (Consistency) If honest $p$ delivers $v$ and honest $q$ delivers $v'$, then $v = v'$. (Totality) If some honest process delivers, every honest process delivers.

The links are reliable: every message between honest processes arrives after a finite but unbounded delay. They are authenticated: a receiver knows the true sender. The scheduler and the faulty processes can be the same adversary, which sees all messages. The proof uses no timing.

**Setup.** Let $t' \le t$ be the number of faulty processes and $H$ the set of honest ones. An honest process echoes once (line L2), sends ready at most once (lines L3 and L4), and delivers at most once (line L5). This gives no duplication at once. All thresholds count different senders.

**Lemma 1 (echo quorums meet in an honest process).** Two sets of more than $(n + t)/2$ processes each have more than $t$ processes in common, so at least one honest process in common.

*Proof.* $|A \cap B| \ge |A| + |B| - n > (n + t) - n = t \ge t'$. $\square$

**Lemma 2 (one ready value).** All ready messages sent by honest processes carry the same value.

*Proof.* First take the readys sent at line L3. If honest $p$ sends ready$(w)$ there and honest $q$ sends ready$(w')$ there, then $p$ got echo$(w)$ and $q$ got echo$(w')$ from sets of more than $(n + t)/2$ senders each. By Lemma 1 one honest process is in both sets, and it echoed both $w$ and $w'$. An honest process echoes once, so $w = w'$. Call this value $v^*$.

Now order all ready messages sent by honest processes by the time they are sent, and show by induction that each carries $v^*$. A ready sent at line L3 carries $v^*$ by the first part. A ready$(w)$ sent at line L4 needs ready$(w)$ from $t + 1$ senders, so from at least one honest sender, whose ready was sent earlier. By induction it carries $v^*$, so $w = v^*$. In particular the first honest ready is sent at line L3, so $v^*$ is defined whenever an honest process sends ready. $\square$

**Lemma 3 (consistency).** Every value that an honest process delivers is $v^*$.

*Proof.* Line L5 needs ready$(w)$ from $2t + 1$ senders, so from at least $t + 1 \ge 1$ honest ones. By Lemma 2, $w = v^*$. $\square$

**Lemma 4 (totality).** If an honest process $p$ delivers $v$, every honest process delivers $v$.

*Proof.* $p$ got ready$(v)$ from at least $2t + 1 - t' \ge t + 1$ honest processes. Each of them sent ready$(v)$ to all processes, and the links are reliable, so each honest $q$ gets these $t + 1$ messages. If $q$ has not sent ready yet, line L4 fires and it sends ready$(v)$; if it has, the ready was for $v$ by Lemma 2. So all $n - t'$ honest processes send ready$(v)$ to all. Since $n > 3t$, $n - t' \ge 2t + 1$, so every honest process gets ready$(v)$ from $2t + 1$ senders and delivers. By Lemma 3 it delivers $v$. $\square$

**Lemma 5 (validity and integrity).** If $s$ is honest and broadcasts $m$, every honest process delivers $m$ and nothing else.

*Proof.* The links are authenticated, so the only initial message from $s$ that an honest process accepts is initial$(m)$, and every honest process gets it. So every honest process echoes $m$ and nothing else. For $w \ne m$, at most $t' \le t$ processes send echo$(w)$, and $t \le (n + t)/2$, so no honest process sends ready$(w)$ at line L3, and $v^* = m$ if $v^*$ is defined. Every honest process gets echo$(m)$ from all $n - t' \ge n - t$ honest processes, and $n - t > (n + t)/2$ exactly when $n > 3t$. So each honest process sends a ready, either at line L3 or earlier at line L4, and by Lemma 2 it is ready$(m)$. Then every honest process gets ready$(m)$ from $n - t' \ge 2t + 1$ senders and delivers. By Lemma 3 it delivers $m$. $\square$

**Theorem.** BRACHA-RBC has validity, no duplication, integrity, consistency and totality when $n > 3t$.

*Proof.* Lemmas 3, 4 and 5, and the setup for no duplication. $\blacksquare$

**Where n > 3t is used.** Lemma 1 holds for every $n$, so consistency does not depend on the bound. Validity needs $n - t > (n + t)/2$, and totality needs $n - t \ge 2t + 1$; both are $n > 3t$. With $n = 3t$ and silent faulty processes, an honest sender gets only $2t$ echoes, which is not more than $(n + t)/2 = 2t$, so no process delivers. The test of the implementation runs this case.
