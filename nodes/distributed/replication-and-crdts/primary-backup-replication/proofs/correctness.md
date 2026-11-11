---
title: Primary-backup replication with a perfect failure detector is linearizable and live
proves: [correctness]
status: full
---

**Statement.** Assume the synchronous model, crash failures of servers, at most $n - 1$ crashes among $n$ servers, reliable links between correct processes, and a view service that installs views $1, 2, 3, \ldots$ with these rules: view $v + 1$ is installed only after the primary or a backup of view $v$ has crashed (accuracy), every crash of a member of the current view leads to a new view within a known time (completeness), and each new view keeps exactly the live members of the old one, with the smallest live member as primary. Each request has a unique id, and a client retries a request with the same id until it gets a reply. Then (a) every history of the protocol is linearizable, and (b) every request of a correct client completes.

**Setup.** Write $p_v$ for the primary of view $v$ and $B_v$ for its backups. Say that $p_v$ is *serving* from the moment all of $B_v$ have acked its STATE message (line L9) until it crashes or view $v + 1$ is installed. Say that a write is *in flight* at $p_v$ from its run of line L4 until its run of line L8.

**Lemma 1 (one primary).** At any time at most one server is serving.

*Proof.* A server serves only in a view in which it is primary. By accuracy, view $v + 1$ is installed only after a member of view $v$ has crashed. If that member is $p_v$, then $p_v$ has stopped. If it is a backup, then $p_{v+1} = p_v$, and the server is the same. In both cases no server of view $v$ other than $p_{v+1}$ still acts as primary once view $v + 1$ exists, and a server ignores requests of older views (it compares the view number in each message). $\square$

**Lemma 2 (backup invariant).** Whenever $p_v$ is serving and has no write in flight, every live backup $b \in B_v$ has the same state $s$ and the same cache as $p_v$.

*Proof.* At the moment $p_v$ starts to serve, every $b \in B_v$ has acked STATE$(v, s, \mathit{cache})$, and $p_v$ has not changed $s$ since it sent that message, because it serves no request before the acks. A backup that has acked STATE$(v, \ldots)$ changes its state again only on an UPDATE of view $v$ (line L10), since messages of other views are ignored. Now consider a write $w$ handled by $p_v$ while serving. Line L4 changes $s$ at $p_v$, and line L5 sends the new $s$ and the id of $w$ to every backup. The primary serves the next request only after line L7, that is, after every backup has acked, and a backup acks only after line L10 has set its state to the new $s$. Reads (line L3) and cache hits (line L2) change no state. So the invariant holds again when $w$ leaves the in-flight state, and by induction on the requests of view $v$ it holds whenever there is no write in flight. $\square$

**Lemma 3 (what survives a view change).** Let view $v + 1$ follow view $v$. The state of $p_{v+1}$ at the start of view $v + 1$ is the state of $p_v$ after the last write $w$ that $p_v$ completed (ran line L8 for), possibly followed by one more write $w'$ that $p_v$ had in flight. No client has received a reply for $w'$ from $p_v$.

*Proof.* If $p_{v+1} = p_v$, the claim is trivial. Otherwise $p_v$ crashed, and $p_{v+1} \in B_v$. By Lemma 2 applied just after $w$ left the in-flight state, $p_{v+1}$ then had the state after $w$. Since then $p_v$ started at most one more write $w'$ (it serves one at a time), so $p_{v+1}$ received either no UPDATE for $w'$ or the one UPDATE for $w'$. A reply for $w'$ is sent only at line L8, after all acks, and $p_v$ crashed before that, or $w'$ would be complete. $\square$

**Proof of (a).** We give a linearization. Line L9 overwrites every backup of view $v + 1$ with the state of $p_{v+1}$, so after the view change all members share one state $\sigma_{v+1}$. By Lemma 3, $\sigma_{v+1}$ is the state after the completed writes of view $v$, perhaps with the one in-flight write $w'$.

Build a sequence $L$ of operations as follows. Go through the views in order. In view $v$, list the operations that $p_v$ executes while serving (lines L2, L3 and L4), in the order in which $p_v$ executes them. For an in-flight write $w'$ at a crash, keep it in $L$ if $\sigma_{v+1}$ contains it, and drop this execution otherwise. A retry that hits the cache (line L2) is not a new operation; it returns the output stored for the first kept execution.

1. *Each write appears in $L$ at most once.* The cache stores the id at line L4 and at line L10, and state transfer copies the cache. So once a write is part of a shared state, every later primary finds its id at line L2. An execution that is dropped is in no surviving state and no surviving cache.
2. *Each operation in $L$ lies inside the interval of its call.* An execution at line L3 or L4 happens after the request was sent. It happens before the reply, because the reply comes from line L3, line L8, or a later cache hit. For a write kept from a crashed primary, the client had no reply at the time of line L4 (Lemma 3), so its interval was still open.
3. *$L$ respects real time.* If operation $a$ returns before operation $b$ is called, then $a$ was executed before $b$ was received by any server. By Lemma 1 the executions happen at one serving primary at a time, so the execution of $a$ comes first in $L$.
4. *Each read returns the value that $L$ gives.* A read at line L3 runs while $p_v$ is serving with no write in flight, because $p_v$ handles its queue one request at a time and waits at line L7. By Lemma 2 and Lemma 3 the state of $p_v$ at that moment is $s_0$ followed by the writes before the read in $L$, and no dropped write is part of it.

So $L$ is a legal sequential history that contains every completed operation, keeps the real-time order and gives each call its returned value. This is linearizability. $\square$

**Proof of (b).** A correct client sends its request to the primary of the current view and retries after a timeout. If the primary is correct, it serves the request after at most the requests ahead of it in its queue, each of which completes after one round of UPDATE and ACK to correct backups, or after a view change if a backup crashes (completeness removes the backup, and line L9 lets the primary serve again). If the primary crashes, completeness installs a new view within the known detection time, and the new primary serves after one round trip of STATE and ACK. There are at most $n - 1$ crashes, so after finitely many view changes the views stop changing, and the primary of the last view is correct. The client's next retry reaches it and completes. $\square$

**Remark (why accuracy is needed).** Drop accuracy, and let a server take over when it stops hearing the primary. With two servers and a cut link, both can serve at once, so Lemma 1 fails. The split brain run on the page then gives a read that returns 1 although the write of 2 completed before the read began, which no sequential history allows.
