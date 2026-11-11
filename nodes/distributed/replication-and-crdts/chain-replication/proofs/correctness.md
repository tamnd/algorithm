---
title: Chain replication is linearizable and live with up to n - 1 crashes
proves: [correctness]
status: full
---

**Setting.** Servers run lines L1 to L11 in the asynchronous model with reliable FIFO links. Servers are fail-stop: a server stops at a crash, and the master removes a server from the chain only after it has crashed, and eventually does so for every crashed server. The master is reliable and applies each change of the chain as one step that all servers see. At most $n - 1$ of the $n$ servers crash. Clients do not crash in the statement of liveness, and each client retries an operation, with the same request id, until it gets a reply.

Number the servers of the current chain $1, \dots, m$ from the head. For a server $i$ let $H_i$ be the sequence of entries in $\mathrm{Hist}_i$ and $\mathrm{Sent}_i$ the sequence in its Sent list. Write $a \preceq b$ when $a$ is a prefix of $b$.

**Lemma 1 (contiguity).** For every server, the sequence numbers in $H_i$ are $1, 2, \dots, \mathrm{last}_i$ in order, and $\mathrm{Sent}_i$ is a suffix of $H_i$.

*Proof.* Line L2 uses $\mathrm{last} + 1$ and line L3 accepts only $\mathrm{last} + 1$, so $H_i$ grows by one number at a time. Line L6 appends to Sent what line L4 appended to Hist, and line L7 removes a prefix of Sent, since it removes every entry up to a number. Line L10 empties Sent. $\square$

**Lemma 2 (update propagation).** At all times, if $i < j$ then $H_j \preceq H_i$.

*Proof.* It suffices to show $H_{i+1} \preceq H_i$ for neighbours. In the initial state all histories are empty. Consider the events that change a history or the chain.

- *Line L2 at the head.* It extends $H_1$, which keeps $H_2 \preceq H_1$.
- *Line L3 at server $i + 1$.* The entry $e$ comes from server $i$ over a FIFO link, so it is an entry of $H_i$, and $i$ sent its entries in the order of $H_i$. By Lemma 1, $e.\mathrm{seq} = \mathrm{last}_{i+1} + 1$ means that $e$ is the entry of $H_i$ that follows $H_{i+1}$. So $H_{i+1} \cdot e \preceq H_i$. Messages from a server that is no longer the predecessor are ignored.
- *A head or tail removal.* It removes the first or the last server, and the remaining neighbour pairs are unchanged.
- *A middle removal of $S$ between $S^-$ and $S^+$.* Before the removal, $H_{S^+} \preceq H_S \preceq H_{S^-}$, so the new pair satisfies $H_{S^+} \preceq H_{S^-}$. $\square$

**Lemma 3 (inprocess requests).** At all times, every entry of $H_i$ that is not in $\mathrm{Sent}_i$ is in $H_m$, the history of the tail.

*Proof.* An entry leaves $\mathrm{Sent}_i$ only by line L7 or line L10. Line L7 runs when an ACK($s$) comes from the successor; acks start at the tail at line L5 or at line L10, for an entry the tail has, and pass up the chain. When ACK($s$) was created, the tail held every entry with number up to $s$, by Lemma 1. A tail's history only grows, and by Lemma 2 a new tail's history extends the old one, so the current tail holds these entries too. Line L10 empties the Sent list of the tail itself. Entries never in Sent are entries of the tail itself (line L5). $\square$

**Lemma 4 (middle repair).** After a middle removal and the resend of line L11, every entry of $H_{S^-}$ eventually reaches $H_{S^+}$, unless $S^-$ or $S^+$ crashes, in which case a later repair applies the same argument to the new neighbours.

*Proof.* By Lemma 3 applied to $S^-$, an entry of $H_{S^-}$ not in $\mathrm{Sent}_{S^-}$ is in the tail's history, hence, by Lemma 2, in $H_{S^+}$. The entries of $\mathrm{Sent}_{S^-}$ are sent in order before any new forward, over a FIFO link, and by Lemma 1 they form a suffix of $H_{S^-}$ with consecutive numbers that starts no later than $\mathrm{last}_{S^+} + 1$. So line L3 at $S^+$ ignores the ones it has and applies the rest in order. $\square$

**Theorem 1 (linearizability).** Every history of the clients is linearizable, for the object type that the servers apply.

*Proof.* Define the tail sequence $\Theta$ as follows. While a server is the tail, entries are added to $\Theta$ when the server appends them at line L4. When the tail changes at line L9 because the tail $T$ crashed, the new tail $T^-$ has $H_T \preceq H_{T^-}$ by Lemma 2, and the entries of $H_{T^-}$ beyond $H_T$ are added to $\Theta$, in order, at that moment. When the tail does not change, $\Theta$ is unchanged. By induction on events, $\Theta$ equals the history of the current tail at every time, and it only grows.

Each update operation has at most one entry in $\Theta$, by the check of line L1 and because the request id is in the entry: a retry that reaches the head while the entry is in the head's history is ignored, and if the entry was lost with a crashed head, it was never in $\Theta$. Linearize each update whose entry is in $\Theta$ at the moment the entry is added, and each query at the moment line L8 runs at the tail. Drop the updates that never enter $\Theta$; none of them got a reply, since replies are sent only at line L5 or line L10 for entries of the tail's history.

These points lie inside the operation intervals. An entry is created after the client sent the request and is added to $\Theta$ before the reply is sent, by line L5 or line L10 at the same moment or later. A query is answered at line L8 after the client sent it and before the client gets the reply.

The order of the points is a legal sequential run. The tail applies the entries of $\Theta$ in order to its state, starting from the initial state, and a new tail has applied exactly the entries of its history, so at every moment the tail's state is the result of applying $\Theta$. A query at line L8 therefore returns the answer for the state after exactly the updates linearized before it. Since the points respect the real-time order of non-overlapping operations, the history is linearizable. $\square$

**Theorem 2 (liveness).** Every operation of a correct client completes.

*Proof.* At least one server never crashes, so the chain is never empty, and since the master removes each crashed server, eventually every server in the chain is up until the next crash; there are at most $n - 1$ crashes, so eventually the chain stops changing and all its servers are up. Consider an operation that is still pending at that time. A query retry reaches the tail and is answered. For an update, the client's retry reaches the head. If the head has no entry with this id, it creates one. Otherwise the entry is in the head's history. In both cases the entry is in $H_1$, and by the forwards of line L6, the resends of line L11 (Lemma 4) and FIFO links, it reaches the tail, which replies at line L5; if it was already in the tail's history, the tail replied at line L5 or line L10. A reply sent to a correct client arrives. $\square$

**Why the tail must serve queries.** If a server $i < m$ answers a query, it may return the state after an entry of $H_i$ that is not yet in $\Theta$. A later query at the tail returns the state without it, and the history is not linearizable. The tests of the code find such histories when queries go to random servers.
