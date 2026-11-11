---
tag: 1VH90X
kind: definition
slug: byzantine-quorum-system
name: Byzantine quorum system
aliases:
- Malkhi-Reiter quorum system
- dissemination quorum system
- masking quorum system
area: distributed/byzantine-agreement
level: advanced
summary: Quorums whose pairwise overlaps outweigh the faulty servers; dissemination needs overlap f + 1 and n > 3f, masking needs 2f + 1 and n > 4f.
prereqs: [quorum, quorum-intersection, byzantine-failure-model]
see_also: [quorum-intersection, quorum, quorum-certificate, pbft, bracha-reliable-broadcast, byzantine-state-machine-replication, digital-signature]
sources:
  - paper: doi:10.1007/s004460050050
    title: Dahlia Malkhi and Michael Reiter, Byzantine quorum systems, Distributed Computing 11(4), 1998
    locator: pages 203 to 213 (fail-prone systems, dissemination and masking quorum systems, the threshold constructions and the bounds n > 3f and n > 4f, opaque quorum systems)
  - paper: "Dahlia Malkhi and Michael Reiter, Byzantine quorum systems, 29th ACM Symposium on Theory of Computing (STOC), 1997"
    locator: the conference version
  - paper: doi:10.1145/571637.571640
    title: Miguel Castro and Barbara Liskov, Practical Byzantine fault tolerance and proactive recovery, ACM Transactions on Computer Systems 20(4), 2002
    locator: the quorums of 2f + 1 among 3f + 1 replicas and their intersection in a correct replica
---

A Byzantine quorum system is a family of sets of servers, the quorums, whose pairwise overlaps are large enough that the faulty servers in an overlap cannot hide or fake the result of an operation. Malkhi and Reiter defined two main kinds in 1998. In a *dissemination* quorum system every two quorums share at least $f + 1$ servers, so at least one correct one; it suits data that clients can check, such as signed data. In a *masking* quorum system every two quorums share at least $2f + 1$ servers, so the correct servers in the overlap outnumber the faulty ones. With quorums of equal size among $n$ servers, dissemination needs $n > 3f$ and masking needs $n > 4f$. The crash-fault version, with an overlap of one server, is on the [quorum intersection](/quorum-intersection/) page.

## Definition

Let $U$ be a set of $n$ servers. A *fail-prone system* $\mathcal{B}$ is a family of subsets of $U$, and in each run the set of faulty servers is contained in some $B \in \mathcal{B}$. In the threshold case $\mathcal{B}$ is all sets of $f$ servers. A *quorum system* $\mathcal{Q}$ is a family of subsets of $U$.

**Dissemination quorum system.** $\mathcal{Q}$ is a dissemination quorum system for $\mathcal{B}$ if:

- **Consistency.** For all $Q_1, Q_2 \in \mathcal{Q}$ and $B \in \mathcal{B}$, $Q_1 \cap Q_2 \not\subseteq B$. In the threshold case, $|Q_1 \cap Q_2| \ge f + 1$.
- **Availability.** For every $B \in \mathcal{B}$ there is $Q \in \mathcal{Q}$ with $Q \cap B = \emptyset$. In the threshold case, some quorum has at most $n - f$ servers.

**Masking quorum system.** $\mathcal{Q}$ is a masking quorum system for $\mathcal{B}$ if:

- **Consistency.** For all $Q_1, Q_2 \in \mathcal{Q}$ and $B_1, B_2 \in \mathcal{B}$, $(Q_1 \cap Q_2) \setminus B_1 \not\subseteq B_2$. In the threshold case, $|Q_1 \cap Q_2| \ge 2f + 1$.
- **Availability.** As above.

The consistency rule for masking says: remove any possible set of faulty servers from the overlap, and what is left is still not a set that could all be faulty. So the correct servers in the overlap, which hold the latest value, outnumber any group of faulty servers that agree on a false value.

**Threshold constructions.** Take all sets of $q$ servers as quorums. Two sets of size $q$ share at least $2q - n$ servers, and two sets can share exactly $\max(0, 2q - n)$, so this is the true minimum. Availability needs $q \le n - f$.

- *Dissemination.* We need $2q - n \ge f + 1$ and $q \le n - f$. The smallest $q$ is $\lceil (n + f + 1)/2 \rceil$. Both hold for some $q$ exactly when $2(n - f) - n \ge f + 1$, that is $n \ge 3f + 1$. With $n = 3f + 1$, $q = 2f + 1$.
- *Masking.* We need $2q - n \ge 2f + 1$ and $q \le n - f$. The smallest $q$ is $\lceil (n + 2f + 1)/2 \rceil$. Both hold exactly when $2(n - f) - n \ge 2f + 1$, that is $n \ge 4f + 1$. With $n = 4f + 1$, $q = 3f + 1$.

*Proof of the bounds for any quorum system.* Let availability hold. For a fail-prone set $B$ with $|B| = f$ there is a quorum $Q_1 \subseteq U \setminus B$. For another set $B'$ of $f$ servers inside $Q_1$ (if $|Q_1| \ge f$) there is a quorum $Q_2$ that avoids $B'$. Then $Q_1 \cap Q_2 \subseteq Q_1 \setminus B'$, which has at most $n - 2f$ servers. Dissemination asks for at least $f + 1$, so $n - 2f \ge f + 1$; masking asks for $2f + 1$, so $n - 2f \ge 2f + 1$. (If $|Q_1| < f$, then $Q_1 \cap Q_2$ has fewer than $f$ servers and fails both rules.) So every threshold dissemination quorum system needs $n \ge 3f + 1$, and every threshold masking quorum system needs $n \ge 4f + 1$.

These sizes were checked by counting all pairs of $q$-sets for $3 \le n \le 10$ and every $f$: the smallest quorum size that meets each rule is the one above, and none exists below the bound.

| $n$ | $f$ | dissemination $q$ | smallest overlap | masking $q$ | smallest overlap |
|---|---|---|---|---|---|
| 4 | 1 | 3 | 2 | none | none |
| 5 | 1 | 4 | 3 | 4 | 3 |
| 7 | 2 | 5 | 3 | none | none |
| 9 | 2 | 6 | 3 | 7 | 5 |

## Examples and non-examples

- **PBFT quorums.** With $n = 3f + 1$, the quorums of $2f + 1$ replicas in [PBFT](/pbft/) form a threshold dissemination quorum system: two quorums share at least $f + 1$ replicas. Signed messages make the data self-verifying, so one correct replica in the overlap is enough. A [quorum certificate](/quorum-certificate/) is a proof that one such quorum voted.
- **Masking with $n = 5$, $f = 1$.** Quorums of 4 servers meet in at least 3. A client reads from a quorum and keeps a value that at least $f + 1 = 2$ servers report with the highest timestamp. The latest write reached a quorum, so the overlap holds it at at least $3 - 1 = 2$ correct servers, and the one faulty server cannot make a false value reach 2 reports.
- **Non-example: majorities.** With $n = 4$, $f = 1$, quorums of 3 servers meet in 2 servers, so they form a dissemination system but not a masking one. Plain majorities of 3 out of 5 meet in only 1 server, which may be the faulty one, so they form neither, although they work for crash faults.
- **Non-example: $n = 3f$.** With $n = 3$ and $f = 1$, a quorum that avoids one server has at most 2 servers, and two such quorums can meet in 1 server, which may be faulty. No threshold dissemination quorum system exists.
- **Opaque quorum systems.** Malkhi and Reiter also define opaque quorum systems, in which a client can find the latest value without knowing which servers are faulty, even with unsigned data written by honest clients; the threshold form needs $n > 5f$.

## Related definitions

- [Quorum intersection](/quorum-intersection/): the crash-fault rule, an overlap of one server.
- [Quorum](/quorum/): the general notion in consensus protocols.
- [Quorum certificate](/quorum-certificate/): a set of $2f + 1$ signed votes, the proof that a quorum of a dissemination system voted for one value.
- [Bracha reliable broadcast](/bracha-reliable-broadcast/) uses echo quorums of more than $(n + f)/2$ servers, the smallest size whose overlap exceeds $f$.
- [Byzantine resilience bound](/byzantine-resilience-bound/): the bound $n > 3f$ for agreement without signatures, which has the same counting at its core.

## References
