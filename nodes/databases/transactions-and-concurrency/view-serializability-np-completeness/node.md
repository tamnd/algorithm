---
tag: RBVB1W
kind: theorem
slug: view-serializability-np-completeness
name: NP-completeness of view serializability
aliases:
- Papadimitriou view serializability theorem
area: databases/transactions-and-concurrency
level: advanced
summary: Testing whether a schedule is view serializable is NP-complete, unlike conflict serializability, which a cycle test decides.
prereqs: [view-serializability, np-complete, 3-sat]
see_also: [view-serializability, serializability-theorem, conflict-serializability, polynomial-time-reduction, 3-sat, np-complete, thomas-write-rule, multiversion-serializability]
sources:
  - paper: doi:10.1145/322154.322158
    title: Christos H. Papadimitriou, The serializability of concurrent database updates, Journal of the ACM 26(4), 1979, pages 631 to 653
    locator: the polygraph of a schedule, the NP-completeness of polygraph acyclicity, and the NP-completeness of testing serializability
  - book: isbn:9781558605084
    title: Gerhard Weikum and Gottfried Vossen, Transactional Information Systems, Morgan Kaufmann, 2001
    locator: Chapter 3 (view serializability, the polygraph characterization and the complexity of the test)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, W. H. Freeman, 1979
    locator: the appendix list of NP-complete problems, the entry on serializability of database histories
---

Deciding whether a [schedule](/transaction-schedule/) is [view serializable](/view-serializability/) is [NP-complete](/np-complete/). Papadimitriou proved this in 1979, by showing that view serializability is the same as the acyclicity of a *polygraph*, a graph with some arcs fixed and some arcs given as choices, and that polygraph acyclicity is NP-complete. The contrast with the [serializability theorem](/serializability-theorem/) is the reason why real schedulers aim at conflict serializability: one cycle test decides it, while for view serializability no polynomial test is known, and none exists unless P = NP.

## Statement

A schedule $S$ in which all transactions commit is *view serializable* if some serial schedule of the same transactions is view equivalent to it: every read reads from the same write (or from the initial state in both), and every item has the same final write.

**Theorem (Papadimitriou 1979).** The problem VSR, which asks for a schedule $S$ whether it is view serializable, is NP-complete. It stays NP-complete for schedules without aborts in which every item is accessed at most four times.

Papadimitriou worked in his own model of transactions and proved the hardness through polygraphs and satisfiability. The proof below follows the same plan, polygraph acyclicity in the middle, but it is a self-contained version in the read-write action model of the [schedule page](/transaction-schedule/), with its own gadgets.

## In plain words

When a write is *blind*, that is, when the writing transaction never read the item, the order of that write against other writes can be hidden by a later write. A serial order must still put each writer either before or after each reader that reads from someone else, but which side is free. With many such free choices, a schedule can encode a puzzle in which each choice is a bit, and the puzzle is satisfiable exactly when some serial order exists. The proof builds such a puzzle from a 3-SAT formula.

## Proof

**Membership in NP.** A certificate is a serial order of the $m$ transactions. For the serial schedule $\sigma$, compute for each read the last earlier write of the same item, and for each item its last write. Do the same for $S$, with occurrences of actions as identifiers. This takes time polynomial in the length of $S$, and $\sigma$ is view equivalent to $S$ exactly when the two results agree.

**The ordering problem.** An instance of ORD is a finite set $N$ of nodes and a set of *triples* $(k; j, i)$ of distinct nodes. A *solution* is a linear order $<$ of $N$ such that for every triple

$$j < i \quad\text{and}\quad (k < j \ \text{or}\ i < k),$$

that is, $j$ comes before $i$ and $k$ is not between them. An *arc* $j \to i$ is a constraint $j < i$ alone. This is the polygraph acyclicity problem in the form of linear orders: each triple is a fixed arc $j \to i$ and a choice between the arcs $k \to j$ and $i \to k$.

**Step 1: from ORD to VSR.** Given an instance with nodes $1, \ldots, n$, take transactions $T_1, \ldots, T_n$ and one more transaction $T_F$. For each triple $(k; j, i)$ use a fresh item $g$ and append the actions

$$w_k(g)\ w_j(g)\ r_i(g)\ w_F(g),$$

for each arc $j \to i$ use a fresh item $h$ and append $w_j(h)\ r_i(h)\ w_F(h)$, and end with the commits $c_1 \cdots c_n\, c_F$. Each transaction consists of its actions in the order of the schedule $S$.

*Claim.* $S$ is view serializable if and only if the instance has a solution.

*Proof.* Look at the item $g$ of a triple. In $S$, the read $r_i(g)$ reads from $w_j(g)$, and the final write of $g$ is $w_F(g)$. In a serial schedule $\sigma$, the writers of $g$ are $T_k$, $T_j$ and $T_F$, and the read of $T_i$ sees the last of them that comes before $T_i$. So $\sigma$ agrees with $S$ on $g$ exactly when $T_F$ is the last of the three writers, and $T_j$ is the last writer before $T_i$. The second condition means $T_j <_\sigma T_i <_\sigma T_F$, because $T_F$ comes after $T_j$, and that $T_k$ is not between $T_j$ and $T_i$. The first condition then only adds $T_k <_\sigma T_F$. For the item $h$ of an arc, the same argument gives $T_j <_\sigma T_i <_\sigma T_F$. If $\sigma$ is view equivalent to $S$, its order on $T_1, \ldots, T_n$ is therefore a solution. If $<$ is a solution, the serial schedule in the order $<$ followed by $T_F$ meets all these conditions, item by item. $\square$

**Step 2: from 3-SAT to ORD.** Let $\varphi$ be a [3-SAT](/3-sat/) formula with variables $v_1, \ldots, v_n$ and clauses $C_1, \ldots, C_m$, each with three literals. Say that a node $y$ *has range* $(a, b)$ if the instance holds the arcs $a \to y$ and $y \to b$.

*The spine.* A chain of arcs fixes the order of these nodes:

$$\mathrm{BEGIN},\ O_1, L_1, \ldots, O_n, L_n,\ \text{the clause cells},\ R_1, O'_1, \ldots, R_n, O'_n,\ \mathrm{END}.$$

The clause cells are, for $c = 1, \ldots, m$ in turn, the nodes $W_{c,1}$ and then $S_{c,t}, K_{c,t}, E_{c,t}, W_{c,t+1}$ for $t = 1, 2, 3$. Call everything before the first cell the *left zone* and everything after the last cell the *right zone*. In what follows, $c$ is fixed and we drop it from the names.

*Variable gadget.* For each variable $v$, a node $x_v$ with range $(O_v, O'_v)$ and the triple $(x_v; L_v, R_v)$. In a solution, $x_v$ lies between $O_v$ and $L_v$ or between $R_v$ and $O'_v$. Read the first case as $v$ false and the second as $v$ true.

*Clause gadget.* For each clause, a node $z$ with range $(S_1, E_3)$ and the triples $(z; E_1, S_2)$ and $(z; E_2, S_3)$. In a solution, $z$ lies in one of the three *gaps* $(S_t, E_t)$: it is after $S_1$ and before $E_3$, and it can be neither between $E_1$ and $S_2$ nor between $E_2$ and $S_3$.

*Literal gadget.* For the literal $\ell$ of cell $t$, on the variable $u$, four nodes:

- $p$ with range $(\mathrm{BEGIN}, E_t)$ and $p'$ with range $(S_t, \mathrm{END})$;
- $q'$ with range $(W_t, K_t)$, $q$ with range $(K_t, W_{t+1})$, and the arc $q' \to q$;
- the triples $(q; p, E_t)$, $(q'; S_t, p')$ and $(z; q', q)$;
- if $\ell = u$, the triples $(p; x_u, O'_u)$ and $(p'; x_u, O'_u)$; if $\ell = \neg u$, the triples $(p; O_u, x_u)$ and $(p'; O_u, x_u)$.

The instance has $O(n + m)$ nodes and constraints, and it is built in polynomial time.

**Lemma (a false literal closes its gap).** In a solution, if the literal of cell $t$ is false under the assignment read from the variable gadgets, then $z$ is not in the gap $(S_t, E_t)$.

*Proof.* Take $\ell = u$ with $u$ false, so $x_u < L_u$. The node $p$ is before $E_t$, so it is not after $O'_u$, and the triple $(p; x_u, O'_u)$ forces $p < x_u$: $p$ is in the left zone. Then $p < K_t < q$, so the triple $(q; p, E_t)$ forces $q > E_t$. The node $p'$ is after $S_t$, so it is not before $x_u$, and its triple forces $p' > O'_u$: $p'$ is in the right zone. Then $q' < K_t < p'$, so the triple $(q'; S_t, p')$ forces $q' < S_t$. Now $q' < S_t$ and $q > E_t$, and the triple $(z; q', q)$ says that $z$ is not between $q'$ and $q$, so $z$ is not in $(S_t, E_t)$. For $\ell = \neg u$ with $u$ true, $x_u > R_u$, and the triples $(p; O_u, x_u)$ and $(p'; O_u, x_u)$ again push $p$ before $O_u$ into the left zone and $p'$ after $x_u$ into the right zone. The rest is the same. $\square$

*Soundness.* Let the instance have a solution. Read the assignment from the variable gadgets. For each clause, $z$ lies in some gap $(S_t, E_t)$, so by the lemma the literal of cell $t$ is true. So $\varphi$ is satisfied.

*Completeness.* Let an assignment satisfy $\varphi$. Keep the spine order and place the other nodes as follows.

- Put $x_v$ right after $O_v$ if $v$ is false, and right after $R_v$ if $v$ is true.
- In a cell whose literal is false, put $p$ right after BEGIN, $p'$ right before END, $q'$ right after $W_t$ and $q$ right after $E_t$.
- In a cell whose literal is true, use the order $S_t,\ p',\ q',\ K_t,\ q,\ p,\ E_t$.
- For each clause, choose a cell $t^*$ with a true literal and put $z$ right after $S_{t^*}$, before $p'$.

All arcs hold. The variable triples hold by the placement of $x_v$. The clause triples hold because $z$ is in a gap. The triple $(q; p, E_t)$ holds with $q < p$ in a true cell and with $q > E_t$ in a false cell; the triple $(q'; S_t, p')$ holds with $q' > p'$ in a true cell and with $q' < S_t$ in a false cell. The triple $(z; q', q)$ holds in the cell $t^*$ because $z < q'$, and in every other cell of the clause because there $q'$ and $q$ lie between $W_t$ and $W_{t+1}$, while $z$ lies outside that interval. For the literal triples: in a false cell, $p$ is before all of $O_u$, $x_u$ and $O'_u$, and $p'$ is after all of them. In a true cell with $\ell = u$, $x_u$ is in the right zone, so $p < x_u$ and $p' < x_u$. In a true cell with $\ell = \neg u$, $x_u$ is in the left zone, so $p > x_u$ and $p' > x_u$. So every constraint holds. $\square$

**Conclusion.** Steps 1 and 2 give a [polynomial-time reduction](/polynomial-time-reduction/) from 3-SAT to VSR. In the schedule of Step 1, every item has at most four actions and no transaction aborts. With membership in NP, VSR is NP-complete. $\blacksquare$

## Consequences

- **Schedulers use conflict serializability.** It is a subclass of VSR that the [serializability theorem](/serializability-theorem/) decides with one cycle test, and that is closed under prefixes. View serializability is neither easy to test nor closed under prefixes, so an online scheduler could not use it even with unlimited time per step.
- **Exact view tests are exponential in the worst case.** A test can try all $m!$ serial orders, or search over the choices of the polygraph. Both are fine for a handful of transactions and hopeless in general.
- **Rules that exploit blind writes are local.** The [Thomas write rule](/thomas-write-rule/) accepts some schedules that are view serializable but not conflict serializable. It does so by a fixed rule on timestamps, not by solving the hard problem.
- **The same method gives other hardness results.** Polygraph acyclicity is the core of several later proofs, for example for [multiversion serializability](/multiversion-serializability/), where the version function adds more freedom of the same kind.

## Tightness

- **Blind writes are needed.** If every transaction reads each item before it writes it, view serializability coincides with conflict serializability, and the test is polynomial. The hard instances above rely on writes such as $w_k(g)$ that no read precedes.
- **A fixed number of transactions is easy.** For $m$ transactions the brute force test takes $O(m! \cdot N)$ time on a schedule of $N$ actions, which is polynomial for each fixed $m$. The hardness needs a growing number of transactions.
- **NP-hardness, not more.** The problem is in NP, so it is not PSPACE-hard unless NP = PSPACE.
- **The model matters.** The statement is about the read-write action model with view equivalence. Papadimitriou proved his result in a model of his own, and a change of model, for example a different notion of equivalence, needs its own proof.

## History

Papadimitriou (1979) studied the serializability of schedules of read and write steps, introduced the polygraph of a schedule, and proved that testing serializability is NP-complete, by a reduction from satisfiability through polygraph acyclicity. The same paper compared this class with the class that the precedence graph decides, which is a polynomial subclass. Garey and Johnson (1979) included serializability of database histories in their list of NP-complete problems. Later textbooks, such as Weikum and Vossen (2001), separate final-state, view and conflict serializability and present the hardness of the view test as the reason for the practical focus on conflict serializability.

## References
