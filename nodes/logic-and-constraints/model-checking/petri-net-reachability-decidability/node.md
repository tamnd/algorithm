---
tag: 1VCG6N
kind: theorem
slug: petri-net-reachability-decidability
name: Decidability of Petri net reachability
aliases:
- Mayr's theorem
- VAS reachability theorem
- Mayr-Kosaraju theorem
area: logic-and-constraints/model-checking
level: research
summary: Whether a Petri net can reach a given marking exactly is decidable (Mayr 1981, Kosaraju 1982). The problem is Ackermann-complete.
prereqs: [petri-net, coverability, presburger-arithmetic]
see_also: [karp-miller-tree, reachability-problem, ackermann-function, primitive-recursive-function, undecidability, halting-problem]
sources:
  - paper: "Ernst W. Mayr, An algorithm for the general Petri net reachability problem, 13th ACM Symposium on Theory of Computing (STOC 1981), pages 238 to 246"
    title: An algorithm for the general Petri net reachability problem
    locator: the first decision procedure for reachability; journal version in SIAM Journal on Computing 13(3), 1984
  - paper: "S. Rao Kosaraju, Decidability of reachability in vector addition systems, 14th ACM Symposium on Theory of Computing (STOC 1982), pages 267 to 281"
    title: Decidability of reachability in vector addition systems
    locator: the decomposition into generalized sequences and the decision procedure
  - paper: "Jean-Luc Lambert, A structure to decide reachability in Petri nets, Theoretical Computer Science 99(1), 1992, pages 79 to 104"
    title: A structure to decide reachability in Petri nets
    locator: the simplified decomposition that is the basis of the later complexity analyses
  - paper: "Jérôme Leroux, Vector addition system reachability problem: a short self-contained proof, 38th ACM Symposium on Principles of Programming Languages (POPL 2011)"
    title: "Vector addition system reachability problem: a short self-contained proof"
    locator: the theorem that every unreachable target is separated from the initial marking by a Presburger inductive invariant
  - paper: "Jérôme Leroux and Sylvain Schmitz, Reachability in vector addition systems is primitive-recursive in fixed dimension, 34th IEEE Symposium on Logic in Computer Science (LICS 2019)"
    title: Reachability in vector addition systems is primitive-recursive in fixed dimension
    locator: the Ackermann upper bound for reachability
  - paper: "Wojciech Czerwiński, Sławomir Lasota, Ranko Lazić, Jérôme Leroux and Filip Mazowiecki, The reachability problem for Petri nets is not elementary, 51st ACM Symposium on Theory of Computing (STOC 2019)"
    title: The reachability problem for Petri nets is not elementary
    locator: the tower lower bound; journal version in Journal of the ACM 68(1), 2021
  - paper: "Wojciech Czerwiński and Łukasz Orlikowski, Reachability in vector addition systems is Ackermann-complete, 62nd IEEE Symposium on Foundations of Computer Science (FOCS 2021)"
    title: Reachability in vector addition systems is Ackermann-complete
    locator: the Ackermann lower bound
  - paper: "Jérôme Leroux, The reachability problem for Petri nets is not primitive recursive, 62nd IEEE Symposium on Foundations of Computer Science (FOCS 2021)"
    title: The reachability problem for Petri nets is not primitive recursive
    locator: an independent Ackermann lower bound
  - paper: "Michel Hack, Decidability questions for Petri nets, PhD thesis, Massachusetts Institute of Technology, 1976"
    title: Decidability questions for Petri nets
    locator: the reductions between reachability, liveness and submarking reachability
  - paper: "Mojżesz Presburger, Über die Vollständigkeit eines gewissen Systems der Arithmetik ganzer Zahlen, in welchem die Addition als einzige Operation hervortritt, Comptes Rendus du I congrès de Mathématiciens des Pays Slaves, Warsaw, 1929"
    title: Über die Vollständigkeit eines gewissen Systems der Arithmetik ganzer Zahlen
    locator: the decidability of the first-order theory of the integers with addition
---

The *decidability of Petri net reachability* is the theorem that there is an algorithm which, given a [Petri net](/petri-net/), an initial marking and a target marking, decides whether the target can be reached exactly. Ernst Mayr gave the first proof in 1981, and Rao Kosaraju a second one in 1982; Jean-Luc Lambert simplified it in 1992, and Jérôme Leroux gave a different proof by inductive invariants in 2009 to 2011. For forty years the complexity was open between an EXPSPACE lower bound and a non-primitive-recursive upper bound. It is now known that the problem is complete for the Ackermann level of the fast-growing hierarchy. This page states the theorem and proves it from Leroux's separation theorem. The easier [coverability problem](/coverability/), solved by the [Karp-Miller tree](/karp-miller-tree/), asks only for a marking at least as large as the target.

## Statement

A Petri net is $N = (P, T, \mathrm{pre}, \mathrm{post})$ with $\mathrm{pre}(t), \mathrm{post}(t) \in \mathbb{N}^P$. A transition $t$ is enabled in $M \in \mathbb{N}^P$ when $M \ge \mathrm{pre}(t)$, and it gives $M + C_t$ with $C_t = \mathrm{post}(t) - \mathrm{pre}(t)$. $R(N, M_0)$ is the set of markings reachable from $M_0$.

**Theorem (Mayr 1981, Kosaraju 1982).** There is an algorithm that, given $N$, $M_0$ and $M_T$, decides whether $M_T \in R(N, M_0)$.

**Theorem (complexity).** The reachability problem is Ackermann-complete: it is in the class $\mathbf{F}_\omega$ of problems solvable in time bounded by the Ackermann function composed with a primitive recursive function (Leroux and Schmitz 2019), and it is hard for this class under primitive recursive reductions (Czerwiński and Orlikowski 2021; Leroux 2021). An earlier result showed that it is not elementary (Czerwiński, Lasota, Lazić, Leroux and Mazowiecki 2019).

The same holds for vector addition systems and vector addition systems with states, which reduce to and from Petri nets.

## In plain words

A Petri net moves tokens between places by firing transitions. Can you get from this exact state to that exact state? The number of states you can reach is usually infinite, so you cannot list them all. The theorem says an algorithm still exists. One proof runs two searches side by side. The first search tries all firing sequences, longer and longer; if the target can be reached, it finds a way. The second search tries all descriptions of sets of states written with plus, equals and "for all" or "exists" over whole numbers. It looks for a set that holds the start, does not hold the target, and is closed under every transition. If it finds one, the target cannot be reached. The hard part of the proof is that such a set always exists when the target cannot be reached.

## Proof

The proof below follows Leroux (2011). It has three parts: a semi-algorithm for reachable targets, a semi-algorithm for unreachable targets, and a separation theorem which shows that the second one always succeeds. The first two parts are proved in full. The third is the deep part, and we state it with its source.

**Presburger formulas.** A Presburger formula is a first-order formula over the natural numbers with $0$, $1$, $+$, $=$ and $\le$. A set $S \subseteq \mathbb{N}^P$ is *Presburger* when $S = \{x : \varphi(x)\}$ for a formula $\varphi$ with free variables $x = (x_p)_{p \in P}$. By Presburger's theorem (1929), the truth of a Presburger sentence is decidable; see [Presburger arithmetic](/presburger-arithmetic/).

**Definition.** A set $S \subseteq \mathbb{N}^P$ is an *inductive invariant* of $N$ when for each $M \in S$ and each $t$ enabled in $M$, also $M + C_t \in S$. It *separates* $M_0$ from $M_T$ when $M_0 \in S$ and $M_T \notin S$.

**Lemma 1 (soundness of separators).** If an inductive invariant $S$ separates $M_0$ from $M_T$, then $M_T \notin R(N, M_0)$.

*Proof.* We show by induction on $k$ that each marking reached from $M_0$ by $k$ firings is in $S$. For $k = 0$ this is $M_0 \in S$. If $M \in S$ is reached in $k$ firings and $M \xrightarrow{t} M'$, then $t$ is enabled in $M$, so $M' = M + C_t \in S$ by inductiveness. So $R(N, M_0) \subseteq S$, and $M_T \notin S$ gives $M_T \notin R(N, M_0)$. $\square$

**Lemma 2 (checking a candidate).** Given a Presburger formula $\varphi$, it is decidable whether $\{x : \varphi(x)\}$ is an inductive invariant that separates $M_0$ from $M_T$.

*Proof.* The three conditions are the Presburger sentences

$$\varphi(M_0), \qquad \neg \varphi(M_T), \qquad \forall x \Big( \varphi(x) \wedge x \ge \mathrm{pre}(t) \rightarrow \varphi\big(x - \mathrm{pre}(t) + \mathrm{post}(t)\big) \Big) \text{ for each } t \in T.$$

Here $M_0$, $M_T$, $\mathrm{pre}(t)$ and $\mathrm{post}(t)$ are constant vectors, so each term is built from variables, constants and $+$. The subtraction is harmless: under the hypothesis $x \ge \mathrm{pre}(t)$, we can write $x = \mathrm{pre}(t) + y$ and quantify over $y$ instead, so the sentence uses only addition. Each sentence is decidable by Presburger's theorem, and there are $|T| + 2$ of them. $\square$

**Lemma 3 (two semi-algorithms).** (a) There is a procedure that stops if and only if $M_T \in R(N, M_0)$. (b) There is a procedure that stops if and only if some Presburger inductive invariant separates $M_0$ from $M_T$.

*Proof.* (a) Enumerate the finite sequences of transitions in order of length; for each, simulate it from $M_0$ and stop when one is fireable and ends in $M_T$. If $M_T$ is reachable, a witness sequence has some finite length, and it is found. If not, no sequence is a witness, and the procedure never stops. (b) Enumerate all Presburger formulas with free variables $x$, which form a countable, effectively listed set, and apply Lemma 2 to each. It stops exactly when some formula passes. $\square$

**Theorem 4 (Leroux's separation theorem).** If $M_T \notin R(N, M_0)$, then some Presburger inductive invariant separates $M_0$ from $M_T$.

This is the deep part of the proof. The reachability set $R(N, M_0)$ itself is in general not Presburger: Hopcroft and Pansiot (1979) gave a vector addition system in dimension 6 whose reachability set is not semilinear, and the Presburger sets are exactly the semilinear sets (Ginsburg and Spanier 1966). So the invariant must be a strict over-approximation in general. Leroux proves that the reachability relation is a finite union of *almost semilinear* relations, built from periodic sets that are well behaved under the transitions, and from this he derives a semilinear separator by a geometric argument on the limits of these periodic sets. This argument is long, and we do not repeat it here; it is the main content of Leroux (2011).

**Proof of the theorem.** Run the procedures of Lemma 3 (a) and (b) in parallel, one step of each in turn. If $M_T$ is reachable, (a) stops. If it is not, Theorem 4 gives a separator, so (b) stops. So at least one of them stops on every input. The two cannot both stop: if (b) stops with a separator, then by Lemma 1, $M_T$ is not reachable, and (a) never stops. Answer "reachable" if (a) stops and "not reachable" if (b) stops. $\blacksquare$

**The classical proof.** Mayr, Kosaraju and Lambert proved the theorem in a different way, which also gives the complexity upper bounds. In outline:

- A *marked graph-transition sequence* (MGTS) is a sequence of strongly connected graphs of $\omega$-markings, like pieces of a [Karp-Miller](/karp-miller-tree/) graph, joined by transitions. It describes a set of runs that pass through the pieces in order.
- To each MGTS belongs a *characteristic system*, a system of linear equations and inequalities over the integers whose solutions count how often each edge is used and give the markings at the joins. It contains the state equation $M = M_0 + C x$ for each piece.
- An MGTS is *perfect* when its characteristic system has solutions in which each edge of each piece is used arbitrarily often and each place that is $\omega$ in a piece is arbitrarily large. Kosaraju's key lemma says that a perfect MGTS has an actual run from its start to its end; the proof pumps cycles that increase the $\omega$ places and then uses cycles that decrease them.
- If an MGTS is not perfect, it can be replaced by finitely many MGTS that are smaller in a well-founded order and together describe the same runs. The order is on tuples of the numbers of $\omega$ places and of edges in the pieces, compared lexicographically, so the decomposition stops.
- The start is the MGTS with one piece, the full net, from $M_0$ to $M_T$. The target is reachable if and only if one of the final perfect MGTS has a solution of its characteristic system, which is an integer linear programming question.

Leroux and Schmitz (2019) bounded the number of decomposition steps by a function at the level $\omega$ of the fast-growing hierarchy, which gives the Ackermann upper bound.

## Consequences

- **Submarking reachability.** Given a subset $Q \subseteq P$ and a vector on $Q$, can the net reach a marking that equals it on $Q$, with any values outside $Q$? Add, for each $p \notin Q$, a transition that removes one token from $p$. Then the answer is yes if and only if the target, extended by 0 outside $Q$, is reachable in the new net. Removals can be moved to the end of a run without disabling any other transition, as for [coverability](/coverability/). So submarking reachability is decidable.
- **Liveness.** A net is live when from each reachable marking each transition can fire again in the future. Hack (1976) showed that liveness and reachability are recursively equivalent, so liveness is decidable.
- **Reachability of semilinear sets.** Since a Presburger set is a finite union of linear sets, and each linear set can be reached by adding transitions that subtract its periods, reachability of a Presburger set of target markings is decidable too.
- **Model checking.** Many verification questions for nets, such as LTL model checking of firing sequences, reduce to reachability, and so become decidable.
- **Other models.** The theorem extends to vector addition systems with states and with one zero test, and it is the base of decidability results for many models that count processes or messages without order.

## Tightness

- **Complexity.** The Ackermann bound is tight in the sense of completeness. Before 2019, the best lower bound was EXPSPACE, from Lipton's 1976 proof for coverability. The 2019 tower lower bound and the 2021 Ackermann lower bounds closed the gap. In fixed dimension $d$ the problem is primitive recursive (Leroux and Schmitz 2019), but the bound grows with $d$.
- **Zero tests.** With two places that can be tested for zero, or with inhibitor arcs, nets simulate two-counter machines, and reachability becomes undecidable by the undecidability of the [halting problem](/halting-problem/) for those machines.
- **Resets and transfers.** Nets with arcs that empty a place (reset nets) or move all its tokens (transfer nets) have undecidable reachability, while their coverability stays decidable.
- **No exact Presburger description.** The reachability set need not be semilinear, as above, so a proof cannot just compute $R(N, M_0)$ as a Presburger formula. The separator of Theorem 4 depends on $M_T$.
- **Equivalence and inclusion.** Whether two nets have the same reachability set is undecidable, so reachability is a sharp edge between decidable and undecidable questions about nets.

## History

Karp and Miller (1969) decided coverability and boundedness but left reachability open. Hack (1976) showed that many problems, such as liveness, are recursively equivalent to it. Sacerdote and Tenney (1977) announced a proof that was incomplete. Mayr gave the first complete proof at STOC 1981, with a journal version in 1984, and Kosaraju gave another at STOC 1982. Lambert (1992) simplified the structure of these proofs. Leroux (2009, 2011) found the proof by Presburger inductive invariants, which also gave a simple algorithm and certificates for non-reachability. Leroux and Schmitz (2015) gave the first explicit upper bound, at a cubic Ackermann level, and lowered it to the Ackermann level in 2019. Czerwiński, Lasota, Lazić, Leroux and Mazowiecki (2019) proved the problem is not elementary, and Czerwiński and Orlikowski (2021) and Leroux (2021) independently proved that it is Ackermann-hard.

## References

- Ernst W. Mayr, An algorithm for the general Petri net reachability problem, STOC 1981, pages 238 to 246.
- S. Rao Kosaraju, Decidability of reachability in vector addition systems, STOC 1982, pages 267 to 281.
- Jean-Luc Lambert, A structure to decide reachability in Petri nets, Theoretical Computer Science 99(1), 1992, pages 79 to 104.
- Jérôme Leroux, Vector addition system reachability problem: a short self-contained proof, POPL 2011.
- Jérôme Leroux and Sylvain Schmitz, Reachability in vector addition systems is primitive-recursive in fixed dimension, LICS 2019.
- Wojciech Czerwiński, Sławomir Lasota, Ranko Lazić, Jérôme Leroux and Filip Mazowiecki, The reachability problem for Petri nets is not elementary, STOC 2019.
- Wojciech Czerwiński and Łukasz Orlikowski, Reachability in vector addition systems is Ackermann-complete, FOCS 2021.
- Jérôme Leroux, The reachability problem for Petri nets is not primitive recursive, FOCS 2021.
- Michel Hack, Decidability questions for Petri nets, PhD thesis, MIT, 1976.
- Mojżesz Presburger, Über die Vollständigkeit eines gewissen Systems der Arithmetik ganzer Zahlen, 1929.
