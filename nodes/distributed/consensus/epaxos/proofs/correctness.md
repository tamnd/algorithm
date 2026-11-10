---
title: EPaxos runs interfering commands in the same order at every replica
proves: [correctness]
status: full
---

The model is asynchronous, with $n = 2F + 1$ replicas and crash failures. Messages can be delayed, duplicated and reordered, but not changed. We prove safety for runs in which every instance keeps the replica that created it as its only command leader, which is the protocol on this page and in the code. Recovery by another replica is not covered; Sutra (2020) shows that the published recovery rules need a fix.

**Notation.** For an instance $x$, a replica stores at most one command $cmd(x)$ and attributes $seq(x)$, $deps(x)$, with a status pre-accepted, accepted or committed. Instance $x$ *commits with* $(s, D)$ when its leader runs line L8 with $(s, D)$. Two instances interfere when their commands interfere.

**Lemma 1 (one commit per instance).** Each instance commits at most once, and every replica that marks $x$ committed stores the attributes with which $x$ committed.

*Proof.* Only the leader $L$ of $x$ runs line L8 for $x$, and the phase of $x$ at $L$ moves from pre to accept to committed and never back, so line L8 runs at most once. The Commit message carries the attributes of line L8, and a replica that marks $x$ committed copies them from that message (line L9). $\square$

**Lemma 2 (committed deps contain the quorum's reports).** If $x$ commits with $(s, D)$, there is a set $Q_x$ of at least $F + 1$ replicas, the leader of $x$ included, such that every $R \in Q_x$ pre-accepted $x$ with some deps $D_R \subseteq D$.

*Proof.* The leader $L$ stored deps $D_L$ at line L1. Each reply comes from a replica $R$ that computed $D_R = D_L \cup (\ldots)$ at line L3 and stored it; a duplicate PreAccept is answered with the stored value (line L4), so each reply reports what $R$ stored. Take $Q_x = \{L\}$ plus the senders of the replies that $L$ used. On the fast path (line L5) there are at least $fq - 1 \ge F$ replies, all equal to $D$, and $D_L \subseteq D$. On the slow path (line L6) there are at least $F$ replies and $D$ is the union of $D_L$ and all of them. The Accept phase (lines L7 and L9) does not change $D$. In both cases $|Q_x| \ge F + 1$. $\square$

**Lemma 3 (interfering commands see each other).** If $x \ne y$ interfere and both commit, with deps $D_x$ and $D_y$, then $x \in D_y$ or $y \in D_x$.

*Proof.* By Lemma 2, $|Q_x| + |Q_y| \ge 2F + 2 > n$, so some replica $R$ is in both. $R$ handles the pre-accept of $x$ and of $y$ at two different times (line L1 if $R$ leads the instance, line L3 otherwise). Say it handled $x$ first. Then $x$ was in $R$'s store when it handled $y$, so the set of interfering instances it computed for $y$ contains $x$, and $x \in D_R \subseteq D_y$. The other case gives $y \in D_x$. $\square$

**Lemma 4 (the graph is the same everywhere).** Fix a committed instance $x$. When a replica passes line L10 for $x$, the subgraph that it has reached from $x$ through deps, with its $seq$ values, is the same at every replica that passes line L10 for $x$, apart from instances it already ran.

*Proof.* Line L10 waits until every reachable instance is committed, and by Lemma 1 the committed attributes, and so the edges and $seq$ values, are the same at every replica. Only the set of instances already run can differ, and those are removed from the graph. $\square$

**Lemma 5 (the order of one execution).** Line L11 lists components so that if $u$ reaches $v$ and $v$ does not reach $u$, then the component of $v$ comes first. Line L12 runs each component in the order of $(seq, \text{instance id})$, a total order with no ties since ids are distinct.

*Proof.* This is the output order of Tarjan's algorithm: a component is emitted only after every component reachable from it is emitted. The test checks this property against brute force. $\square$

**Theorem (same order for interfering commands).** If $x$ and $y$ interfere, and two replicas $R_1$ and $R_2$ both run $x$ and $y$, then they run them in the same order.

*Proof.* By Lemma 3, say $x \in deps(y)$. So $y$ reaches $x$ in the committed graph, which is the same at both replicas by Lemma 1.

*Case 1: $x$ does not reach $y$.* Each replica runs $x$ before $y$. When a replica first runs $y$, it runs it as part of the components reachable from some root. If $x$ was not run yet, then $x$ is in that reachable graph, its component differs from $y$'s, and by Lemma 5 it comes first. So $x$ runs first at both replicas.

*Case 2: $x$ and $y$ reach each other.* Then they lie on a cycle of committed instances. Let $C$ be the set of instances that both reach $x$ and are reachable from $x$; this is a set of the committed graph, the same at both replicas. No replica runs an instance of $C$ before line L10 holds for that instance, and then everything reachable from it, which includes all of $C$, is committed. Consider the first time a replica runs any instance of $C$. No instance of $C$ has run yet at that replica, so by Lemma 4 the component that contains it is exactly $C$, and line L12 runs all of $C$ in the order of $(seq, id)$, which is fixed by Lemma 1. So both replicas run $x$ and $y$ in the order of their $(seq, id)$ pairs. $\square$

**Theorem (validity and no duplication).** A replica runs only commands that clients proposed, and runs each instance at most once.

*Proof.* Every instance holds the command given at line L1, copied unchanged in every message. Line L12 skips instances already run, and the code adds each instance to the set of run instances when it runs it. $\square$

**Liveness without failures of leaders.** If every leader stays alive and messages between live replicas are eventually delivered, every instance commits: a leader that does not get $fq - 1$ equal replies still gets replies from at least $F$ of the other $2F$ replicas, because at most $F$ crash. It then takes the slow path and gets $F$ AcceptOK messages in the same way. Once every instance is committed, line L10 holds for every instance, and each replica runs every command. $\blacksquare$

The intersection in Lemma 3 needs only quorums of $F + 1$. The larger fast quorum of $F + \lfloor (F + 1)/2 \rfloor$ is there for recovery: a recovering replica that asks a majority must be able to tell whether a fast commit might have happened, and the overlap of at least $\lfloor (F+1)/2 \rfloor$ replicas, checked by brute force in the tests, is what the recovery rule of the paper relies on.
