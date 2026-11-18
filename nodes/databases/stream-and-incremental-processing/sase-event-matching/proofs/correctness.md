---
title: The stack-based matcher reports every match once, at the arrival of its last event
proves: [correctness, time.worst]
status: full
---

We use the line numbers of the pseudocode. The pattern is $\mathrm{SEQ}(E_1, \dots, E_k)$ WITHIN $W$ with the skip-till-any-match selection. The events arrive in stream order $x^1, x^2, \dots$ with timestamps that never decrease, and we write $p(x)$ for the position of event $x$. A *match* is a tuple $(e_1, \dots, e_k)$ of events with $p(e_1) < \cdots < p(e_k)$, the type of $e_i$ equal to $E_i$, $e_k.ts - e_1.ts \le W$, all events in the same partition when there is an equivalence test, no event of a negated type of the same partition strictly between the neighbours of the negation, and the predicate true. Without the last two conditions we call the tuple a *window match*.

The stacks of one partition see only the events of that partition, so we fix one partition and drop it from the notation. A stack entry is an event with its RIP. Pruning removes entries from the bottom of a stack only, and the absolute index of an entry never changes, so "the entries at or below index $r$" is well defined.

**Lemma 1 (RIP).** Let $y$ be an entry of stack $i \ge 2$ with RIP $r$. The entries of stack $i - 1$ with an index at most $r$ are exactly the entries that were pushed onto stack $i - 1$ before $y$ arrived.

*Proof.* Stack $i - 1$ receives its entries in stream order, and line L5 sets $r$ to its top when $y$ is pushed. An event of type $E_{i-1} = E_i$ is pushed onto both stacks, but line L3 goes from the last position down, so it is pushed onto stack $i$, with $r$ taken, before it is pushed onto stack $i - 1$. So it is not below its own RIP. $\square$

**Lemma 2 (window matches are in the stacks).** Let $(e_1, \dots, e_k)$ be a window match. Then, when $e_k$ is processed and after the pruning of line L2, every $e_i$ is an entry of stack $i$.

*Proof.* For every $i$ and every time $\tau \le e_k.ts$, we have $e_i.ts \ge e_1.ts \ge e_k.ts - W \ge \tau - W$, so line L2 never removes $e_i$ up to the processing of $e_k$. We show by induction on $i$ that $e_i$ is pushed onto stack $i$. Line L4 always lets an event of type $E_1$ onto stack 1. For $i \ge 2$, the event $e_{i-1}$ is on stack $i - 1$ when $e_i$ arrives, by the induction hypothesis and because it is not pruned; so the stack is not empty and line L5 pushes $e_i$ onto stack $i$. $\square$

**Lemma 3 (liveness is monotone).** Call an entry *live* if a path that steps from each entry to a present entry at or below its RIP leads from it to stack 1. If an entry $y'$ of stack $i$ is live and the entry $y$ is above $y'$ in the same stack, then $y$ is live.

*Proof.* By induction on $i$. Every entry of stack 1 is live. For $i \ge 2$, the entry $y$ arrived after $y'$, and the top of stack $i - 1$ only grows, so $\mathrm{RIP}(y) \ge \mathrm{RIP}(y')$. A present live entry $z'$ at or below $\mathrm{RIP}(y')$ is then also at or below $\mathrm{RIP}(y)$, so $y$ is live. $\square$

**Lemma 4 (construction).** When the current event $e$ is pushed onto stack $k$, line L7 produces each window match that ends with $e$ exactly once, and nothing else.

*Proof.* The search starts at the entry of $e$, which line L5 has just put on top of stack $k$. From an entry of stack $i$, it tries the present entries of stack $i - 1$ at or below the RIP, from the newest down, and it stops at the first one from which it finds no path. By Lemma 3, the live candidates are a top segment of this range, so the search visits all of them and then stops; and by induction on $i$, the search from an entry finds a path exactly when the entry is live, and then it finds all its paths. So line L7 produces every path from $e$ to stack 1, each once, because a path is a sequence of distinct entries.

Each path is a window match: by Lemma 1 the positions decrease along the path, the stacks give the types, and every present entry has a timestamp at least $e.ts - W$ after line L2, so $e_1.ts \ge e.ts - W$. Conversely, let $(e_1, \dots, e_k)$ be a window match with $e_k = e$. By Lemma 2 each $e_i$ is a present entry of stack $i$, and $e_{i-1}$ was pushed before $e_i$ arrived, so it is at or below the RIP of $e_i$ by Lemma 1. So the tuple is a path. $\square$

**Theorem 1.** Over the whole stream, the matcher emits every match exactly once, and it emits it while it processes the last event of the match.

*Proof.* A search starts only at the current event, so a tuple can be produced only while its last event is processed, and by Lemma 4 the window matches that end with $e$ are produced exactly once then. Line L8 keeps a window match if and only if it is a match. The window test is exact. For a negation between positions $i - 1$ and $i$, the matcher keeps the events of the negated types of the partition, pruned like the stacks. Any such event strictly between $e_{i-1}$ and $e_i$ has a timestamp at least $e_1.ts \ge e.ts - W$, so it has not been pruned, and the test sees it. The predicate is checked as given. $\blacksquare$

**Theorem 2 (cost of a construction).** Let $M$ be the number of window matches that end with the current event. The search visits at most $k^2 M + k$ entries.

*Proof.* A live entry that the search visits lies on a path that the search produces, and each path has $k$ entries, so at most $k M$ live entries are visited. A live entry makes at most one call on a candidate that is not live, the one where it stops. A call on an entry that is not live tries only its top candidate, which is also not live by Lemma 3, so it follows a single chain of at most $k - 1$ further entries. This gives at most $k M + k M (k - 1) = k^2 M$ visits when $M \ge 1$, and at most $k$ when $M = 0$, where the start entry itself is not live. $\square$

The other work per event is $O(k)$ for lines L3 to L5 and, amortized, $O(1)$ per entry for the pruning of line L2, because each entry is pruned once. The negation test of line L8 costs at most the number of stored negated events per match. The tests count the visits of the search and check the bound.
