---
tag: YP4N92
kind: theorem
slug: vector-clock-characterization
name: Vector clock characterization of causality
aliases:
- Fidge-Mattern theorem
area: distributed/clocks-and-ordering
level: core
summary: For events e and f, e happened before f iff the vector timestamp of e is componentwise less than that of f. One entry suffices to test it, and n entries are needed in general.
history:
  year: 1988
  people: [Colin Fidge, Friedemann Mattern]
  note: Fidge (1988) and Mattern (1989) published vector time independently and showed that it captures happened-before exactly.
prereqs: [vector-clocks, happened-before]
see_also: [vector-clocks, happened-before, concurrent-events, lamport-clock-condition, consistent-cut, causal-broadcast, version-vectors, matrix-clocks]
sources:
  - paper: "Colin J. Fidge, Timestamps in message-passing systems that preserve the partial ordering, Proceedings of the 11th Australian Computer Science Conference, 1988"
    title: Colin J. Fidge, Timestamps in message-passing systems that preserve the partial ordering
    locator: pages 56 to 66
  - paper: "Friedemann Mattern, Virtual time and global states of distributed systems, in Parallel and Distributed Algorithms, Cosnard et al. (eds.), North-Holland, 1989"
    title: Friedemann Mattern, Virtual time and global states of distributed systems
    locator: pages 215 to 226 (vector time, its relation to causality, and consistent cuts)
  - paper: doi:10.1007/BF02277859
    title: Reinhard Schwarz and Friedemann Mattern, Detecting causal relationships in distributed computations, in search of the holy grail, Distributed Computing 7(3), 1994
    locator: the sections on causal histories and vector time
  - paper: doi:10.1016/0020-0190(91)90055-M
    title: Bernadette Charron-Bost, Concerning the size of logical clocks in distributed systems, Information Processing Letters 39(1), 1991
    locator: the main theorem, that n entries are needed
  - book: isbn:9780521876346
    title: Ajay D. Kshemkalyani and Mukesh Singhal, Distributed Computing, Principles, Algorithms, and Systems, Cambridge University Press, 2008
    locator: Chapter 3, Section 3.4 (vector time and its strong consistency)
  - book: isbn:9780471453246
    title: Hagit Attiya and Jennifer Welch, Distributed Computing, Fundamentals, Simulations and Advanced Topics, second edition, Wiley, 2004
    locator: Chapter 6, Section 6.1 (vector clocks)
---

The vector clock characterization says that [vector clocks](/vector-clocks/) capture [happened-before](/happened-before/) exactly: an event $e$ happened before an event $f$ if and only if the vector timestamp of $e$ is less than that of $f$ in every entry and different in at least one. Fidge and Mattern found this independently in 1988 and 1989. The proof shows that entry $j$ of $V(e)$ counts the events of process $j$ in the causal history of $e$. The same fact gives a test that reads only one entry, and a test for [consistent cuts](/consistent-cut/).

## Statement

**Setting.** A run has $n$ processes $P_1, \ldots, P_n$. Each process $P_i$ keeps a vector $V_i \in \mathbb{N}^n$, at first all zero, and applies these rules:

- at a local event or a send, set $V_i[i] \gets V_i[i] + 1$; a send attaches the new $V_i$ to the message;
- at the receipt of a message with vector $W$, set $V_i[k] \gets \max(V_i[k], W[k])$ for all $k$, then $V_i[i] \gets V_i[i] + 1$.

$V(e)$ is the value of $V_i$ just after the event $e$. For vectors, $V \le W$ means $V[k] \le W[k]$ for all $k$, and $V < W$ means $V \le W$ and $V \ne W$.

**Theorem.** For all events $e$ and $f$ of the run:

1. $e \to f \iff V(e) < V(f)$;
2. $e \parallel f \iff$ neither $V(e) \le V(f)$ nor $V(f) \le V(e)$.

**Corollary (one-entry test).** Let $e$ be an event of $P_i$ and $f \ne e$. Then $e \to f \iff V(e)[i] \le V(f)[i]$.

**Corollary (two-entry concurrency test).** Let $e$ be an event of $P_i$ and $f$ an event of $P_j$ with $f \ne e$. Then $e \parallel f \iff V(e)[i] > V(f)[i]$ and $V(f)[j] > V(e)[j]$.

**Corollary (consistent cuts).** Let $e_1, \ldots, e_n$ be events with $e_i$ on $P_i$, and let $S$ be the cut whose events on $P_i$ are $e_i$ and the events before it. Then $S$ is consistent if and only if $V(e_j)[i] \le V(e_i)[i]$ for all $i$ and $j$.

## In plain words

Each entry of a vector clock is a count. Entry $j$ at an event says how many events of process $j$ that event can know about, through its own past and the messages it received. What an event can know about is exactly the set of events that happened before it.

So comparing two vectors entry by entry compares two such sets. One event happened before another exactly when its set fits inside the other's. Because each process does its events in a line, a count tells us which events of that process are in the set, so the counts lose nothing.

A shortcut follows. To see whether an event of process $i$ came before another event, look only at entry $i$ of both: the later event must count at least as far as the earlier one.

## Proof

Let $C(e) = \{g : g \to e\} \cup \{e\}$ be the causal history of $e$, and write $P_j$ also for the set of events of process $j$.

**Lemma 1 (prefixes).** For every event $e$ and process $j$, $C(e) \cap P_j$ is a prefix of the sequence of events of $P_j$.

*Proof.* If $g \in C(e) \cap P_j$ and $h$ comes before $g$ on $P_j$, then $h \to g$, and $g \to e$ or $g = e$, so $h \to e$. Hence $h \in C(e)$. $\square$

**Lemma 2 (counting).** For every event $e$ and every $j$, $V(e)[j] = |C(e) \cap P_j|$.

*Proof.* By induction over the events in the order in which they happen, which is a linear extension of $\to$. Let $e$ be an event of $P_i$, and let $p$ be the event just before $e$ on $P_i$. If $e$ is the first event of $P_i$, read $V(p)$ as the zero vector and $C(p)$ as the empty set.

- *Local event or send.* Here $C(e) = C(p) \cup \{e\}$, since the only immediate predecessor of $e$ is $p$. The event $e$ is not in $C(p)$, because $e \to p$ would contradict local order. So the count rises by one at $P_i$ and stays the same elsewhere, which is what the rule does.
- *Receipt of a message sent at $s$.* Here $C(e) = C(p) \cup C(s) \cup \{e\}$. The message carries $V(s)$, and by induction $V(p)$ and $V(s)$ count $C(p)$ and $C(s)$. By Lemma 1, $C(p) \cap P_k$ and $C(s) \cap P_k$ are both prefixes of $P_k$, so their union is the longer one, and its size is $\max(V(p)[k], V(s)[k])$. The event $e$ is in neither set, because $e \to p$ and $e \to s$ would each give a cycle. So adding $e$ raises the count at $P_i$ by one, which is what the rule does. $\square$

By Lemmas 1 and 2, $V(e)[j]$ determines $C(e) \cap P_j$: it is the first $V(e)[j]$ events of $P_j$. Hence for all events $e$ and $f$,
$$V(e) \le V(f) \iff C(e) \subseteq C(f), \qquad V(e) = V(f) \iff C(e) = C(f).$$

**Part 1.** By Proposition 2 of [happened-before](/happened-before/), $e \to f$ if and only if $e \ne f$ and $C(e) \subsetneq C(f)$. If $e \ne f$, the sets differ, since one of $e$ and $f$ is not in the history of the other or the order would have a cycle. So $e \to f$ if and only if $C(e) \subsetneq C(f)$, which by the equivalences above is $V(e) < V(f)$.

**Part 2.** For $e \ne f$, $e \parallel f$ means $e \not\to f$ and $f \not\to e$. By part 1 this is $V(e) \not< V(f)$ and $V(f) \not< V(e)$. Since $V(e) \ne V(f)$ for distinct events, this is the same as $V(e) \not\le V(f)$ and $V(f) \not\le V(e)$. $\square$

**One-entry test.** Let $e$ be the $k$-th event of $P_i$. Since $C(e) \cap P_i$ is a prefix that ends with $e$, $V(e)[i] = k$. If $V(f)[i] \ge k$, then $C(f)$ contains the first $k$ events of $P_i$, so $e \in C(f)$, and $e \ne f$ gives $e \to f$. Conversely, $e \to f$ gives $V(e) < V(f)$ by part 1, so $V(e)[i] \le V(f)[i]$. $\square$

**Two-entry test.** Apply the one-entry test in both directions: $e \not\to f$ is $V(e)[i] > V(f)[i]$, and $f \not\to e$ is $V(f)[j] > V(e)[j]$. $\square$

**Consistent cuts.** A cut is consistent if it is closed downward under $\to$. Every event of $S$ on $P_j$ is in $C(e_j)$, so $S$ is closed downward if and only if $C(e_j) \subseteq S$ for every $j$. Both sets meet $P_i$ in a prefix, so this inclusion holds if and only if $|C(e_j) \cap P_i| \le |S \cap P_i|$ for all $i$, that is, $V(e_j)[i] \le V(e_i)[i]$. $\square$

## Consequences

- **Concurrency can be read off timestamps.** This is what [Lamport clocks](/lamport-clocks/) cannot do. Uses include conflict detection with [version vectors](/version-vectors/) and race detection in debuggers.
- **Causal delivery.** [Causal broadcast](/causal-broadcast/) holds back a message until the receiver's vector covers the message vector in all entries except the sender's. Its correctness proof uses the counting lemma.
- **Snapshots and predicates.** The cut test lets an observer decide from vectors alone whether a set of local states forms a [global snapshot](/global-snapshot/), which is what [weak conjunctive predicate detection](/weak-conjunctive-predicate-detection/) checks.
- **Size of the causal history.** By Lemma 2, $\sum_j V(e)[j] = |C(e)|$.
- **Matrix clocks.** Each row of a [matrix clock](/matrix-clocks/) is a vector clock, so the theorem applies to the row of the owner.

## Tightness

- **The number of entries.** Charron-Bost proved in 1991 that for every $n \ge 2$ there is a run of $n$ processes in which no map into $\mathbb{R}^k$ with the componentwise order captures $\to$ unless $k \ge n$. So the $n$ entries of vector clocks cannot be reduced in general. The proof, with the run that forces the bound, is on the page of [Lamport's clock condition](/lamport-clock-condition/). This page uses it and does not prove it again.
- **One scalar is not enough.** A total order of timestamps cannot keep concurrent events incomparable. In the running example, Lamport clocks give $b = 2 < 3 = e$, but $b \parallel e$.
- **The rules matter.** If a receive does not take the maximum, Lemma 2 fails and so does the theorem. For example, if the receive at $g$ only increments its own entry, $V(g) = (0,0,2)$, and the test no longer shows $a \to g$.
- **Fixed sets of processes.** The theorem needs every process to own one entry. When processes join and leave, [interval tree clocks](/interval-tree-clocks/) keep the same order test with a changing structure.

**Running example.** $P_1$ has $a$ (send to $P_2$) and $b$; $P_2$ has $c$, $d$ (receive from $a$) and $e$ (send to $P_3$); $P_3$ has $f$ and $g$ (receive from $e$). The vectors are $a = (1,0,0)$, $b = (2,0,0)$, $c = (0,1,0)$, $d = (1,2,0)$, $e = (1,3,0)$, $f = (0,0,1)$ and $g = (1,3,2)$.

- $d \to g$: the one-entry test reads $V(d)[2] = 2 \le 3 = V(g)[2]$.
- $b \parallel g$: $V(b)[1] = 2 > 1 = V(g)[1]$ and $V(g)[3] = 2 > 0 = V(b)[3]$.
- $\sum_j V(g)[j] = 6 = |\{a, c, d, e, f, g\}| = |C(g)|$.
- The cut with last events $b$, $d$, $f$ is consistent. The cut with last events $a$, $c$, $g$ is not, because $V(g)[2] = 3 > 1 = V(c)[2]$: $g$ knows of $d$ and $e$, which the cut leaves out.

A script checks part 1 and the one-entry test on all 42 ordered pairs, and checks that of the 12 cuts with one or more events on every process, the vector test marks exactly the 8 that are closed downward as consistent.

## History

Fidge (1988) and Mattern (1989) introduced vector timestamps independently and stated that they capture the causal order exactly. Mattern also gave the test for consistent cuts. Schwarz and Mattern (1994) presented vector time as a compact form of causal histories, which is the view of the proof above, and surveyed related work. Charron-Bost (1991) showed that the size $n$ is needed. Similar vectors were used earlier to compare the versions of replicated files, as [version vectors](/version-vectors/), but those order replica states, not single events.

## References
