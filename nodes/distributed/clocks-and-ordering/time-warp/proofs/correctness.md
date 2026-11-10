---
title: When Time Warp comes to rest, every LP has run the events of the sequential simulation, and no rollback goes below the global virtual time
proves: [correctness]
status: full
---

We use the model and the pseudocode of the page. Keys are unique and the same in every run of the same event. Running an event is a deterministic function of the LP state and the event, and every event that it schedules has a larger timestamp, so a larger key. A *run* of an event is one execution of line L2 for it; an event can be run, undone by a rollback, and run again. The run of the whole system *comes to rest* when no LP has a pending event and no message is in transit. For an LP, its *history* is its committed events followed by its processed events.

**Lemma 1 (order).** At every moment, at every LP, the history is in increasing key order, every pending key is larger than every key in the history, and the state of the LP is the result of running the history, in order, from the initial state.

*Proof.* By induction over the steps. At the start the history is empty. Line L1 moves the least pending event to the end of the history, and line L2 runs it on the current state; the remaining pending keys are larger. In RECEIVE, a positive message with a key below the last processed key first causes ROLLBACK to its key $k$. ROLLBACK removes the processed events with key at least $k$ from the end of the history, the latest first, restoring the state saved before each; so afterwards the state is the result of the shorter history, all history keys are below $k$, and the removed events, now pending, have keys of at least $k$. Adding the message, of key $k$, keeps the claim. A positive message with a larger key keeps it too. An antimessage either causes ROLLBACK, as above, or removes a pending event. Line L8 moves events from the processed list to the committed list without changing the history. Lemma 4 below shows that no rollback reaches a committed event. $\square$

**Lemma 2 (cancellation).** Let a run $r$ of an event schedule the event $x$. Then $r$ is undone at some time if and only if $x$ is cancelled: deleted from the pending events, deleted with its antimessage, or rolled back and then deleted.

*Proof.* Line L5 sends the antimessage of $x$ exactly when $r$ is undone, and nothing else sends it. Messages are reliable, so the antimessage arrives. If $x$ is pending, line L7 deletes it. If it has been processed, line L6 rolls it back and line L7 then deletes it. If it has not arrived, the antimessage waits, and the two are deleted together when $x$ arrives. If $r$ is never undone, no antimessage of $x$ exists, and $x$ is never deleted. $\square$

**Theorem 1 (the result).** When the run comes to rest, each LP has run, in key order, exactly the events of the sequential simulation for that LP, and its final state is the sequential one.

*Proof.* At rest, no events are pending and no messages are in transit, so by Lemma 2 the history of each LP holds exactly its initial events and the events scheduled by runs that were never undone. A run that is never undone is the last run of an event in some history. So each LP has run exactly the events scheduled for it by the final runs of the events in the histories, and by Lemma 1 it ran them in key order, each on the state left by its predecessors. This is the hypothesis of the theorem on the page on [parallel discrete event simulation](/parallel-discrete-event-simulation/), which then gives the sequential events and states. $\square$

**Global virtual time.** At a moment $\tau$, let $\mathrm{GVT}(\tau)$ be the least timestamp of all pending events and all messages in transit, positive or negative.

**Lemma 3 (new things are not below GVT).** Every pending event, message or antimessage that exists at a moment $\tau' \ge \tau$ has a timestamp of at least $\mathrm{GVT}(\tau)$.

*Proof.* By induction over the steps after $\tau$. Things that existed at $\tau$ are at least $\mathrm{GVT}(\tau)$ by definition. A delivered message keeps its timestamp. Line L2 runs a pending event, of timestamp at least $\mathrm{GVT}(\tau)$ by induction, and the events it schedules have larger timestamps. A rollback is caused by a message or antimessage of key $k$, whose timestamp is at least $\mathrm{GVT}(\tau)$ by induction; it puts back into the pending events only events with key at least $k$, and the antimessages of line L5 have the timestamps of events scheduled by those events, which are larger still. $\square$

**Lemma 4 (no rollback below GVT).** After the moment $\tau$, no rollback undoes an event with timestamp below $\mathrm{GVT}(\tau)$. So fossil collection with any $g \le \mathrm{GVT}(\tau)$ is safe, and $\mathrm{GVT}$ never decreases.

*Proof.* A rollback after $\tau$ is caused by a message or antimessage that exists after $\tau$, so by Lemma 3 its key $k$ has timestamp at least $\mathrm{GVT}(\tau)$. It undoes only events with key at least $k$, whose timestamps are at least $\mathrm{GVT}(\tau)$. The last claim is Lemma 3 applied to the things that define $\mathrm{GVT}(\tau')$. $\square$

**Lemma 5 (progress).** Let $x$ be the pending event or message with the least key in the system at some moment. Once $x$ is run, that run is never undone.

*Proof.* Every rollback is caused by a message with a key below the undone events, and by the argument of Lemma 3 with keys in place of timestamps, every message that exists from now on has a key of at least $\mathrm{key}(x)$. A rollback of the run of $x$ would need a message with a key below $\mathrm{key}(x)$, or the antimessage of $x$; the antimessage exists only if the run that scheduled $x$ is undone, and that run has a smaller key, so it cannot be undone either, for the same reason. $\square$

So each step of the least key is final, and the least key moves up. Jefferson's paper argues from this that GVT advances in every finite simulation; the seeded tests check that every run comes to rest with the sequential result.
