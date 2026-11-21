---
tag: JG0PJJ
kind: model
slug: decentralized-label-model
name: Decentralized label model
aliases:
- DLM
- Myers-Liskov label model
area: security-and-privacy/access-control-and-information-flow
level: advanced
summary: Labels data with policies of several owners, each naming its allowed readers, so that each owner can declassify only its own policy.
model: word-ram
prereqs: [denning-lattice-model, discretionary-access-control, security-type-system]
see_also: [declassification, join-semilattice, noninterference, trust-management, mandatory-access-control, biba-integrity-model, principle-of-least-privilege, access-control-list]
sources:
  - paper: doi:10.1145/268998.266669
    title: Andrew C. Myers and Barbara Liskov, A decentralized model for information flow control, Proceedings of the 16th ACM Symposium on Operating Systems Principles (SOSP 1997)
    locator: pp. 129 to 142, the first presentation of the model and of its static checking
  - paper: doi:10.1145/363516.363526
    title: Andrew C. Myers and Barbara Liskov, Protecting privacy using the decentralized label model, ACM Transactions on Software Engineering and Methodology 9(4), 2000
    locator: "pp. 410 to 442; Section 3.1 (principals and acts-for), 3.2 (labels and their readers), 3.3 (safe incremental relabelings), 3.4 (the complete relabeling rule), 3.5 (the join of labels), 3.6 (declassification), Section 4 (integrity labels)"
  - paper: doi:10.1109/SECPRI.1998.674834
    title: Andrew C. Myers and Barbara Liskov, Complete, safe information flow with decentralized labels, Proceedings of the 1998 IEEE Symposium on Security and Privacy
    locator: pp. 186 to 197, the formal semantics of labels and the proof that the relabeling rule is sound and complete
  - paper: doi:10.1109/JSAC.2002.806121
    title: Andrei Sabelfeld and Andrew C. Myers, Language-based information-flow security, IEEE Journal on Selected Areas in Communications 21(1), 2003
    locator: pp. 5 to 19, the decentralized label model and Jif in the survey
---

The decentralized label model (DLM), from Andrew Myers and Barbara Liskov (1997), labels each value with the privacy policies of several owners. Each policy names an owner and the readers that this owner allows, and a reader must be allowed by every policy. Labels are ordered so that a relabeling is allowed only when it keeps or tightens every policy, and the join of two labels is their union. An owner can relax its own policy, a [declassification](/declassification/), but not the policy of anyone else. The model keeps the [lattice model](/denning-lattice-model/) of flows, so a [security type system](/security-type-system/) can check it statically; the language Jif does this.

## The machine

**Principals.** There is a set of principals: users, groups and roles. The *acts-for* relation $p \succeq q$, "$p$ acts for $q$", says that $p$ may use all the authority of $q$. It is reflexive and transitive, and it is called the principal hierarchy. It can change at run time.

**Policies and labels.** A *policy* $I$ has an owner $o(I)$ and a set of readers $r(I)$, written $o: r_1, \dots, r_k$. A *label* is a finite set of policies, for example

$$\{\mathit{alice}: \mathit{alice}, \mathit{hr};\ \mathit{bob}: \mathit{bob}, \mathit{hr}\}.$$

The *effective readers* of a policy are the principals that act for one of its readers:

$$R(I) = \{p : p \succeq p' \text{ for some } p' \in r(I)\}.$$

A principal may read a value only if it is in $R(I)$ for every policy $I$ of the label. An owner that is not in the label puts no limit. In the semantics of the journal paper, an owner is not a reader of its own policy unless it is listed.

**Transitions.** A program moves values from one labeled variable or channel to another, and it computes new values. These are the transitions.

- **Relabeling.** A value may move from label $L_1$ to label $L_2$ if $L_1 \sqsubseteq L_2$. For two policies, $I \sqsubseteq J$ if $o(J) \succeq o(I)$ and $R(J) \subseteq R(I)$: the new policy has the same owner or one that acts for it, and allows no new readers. For labels,

$$L_1 \sqsubseteq L_2 \iff \text{for each } I \in L_1 \text{ there is a } J \in L_2 \text{ with } I \sqsubseteq J.$$

- **Computation.** A value computed from values with labels $L_1$ and $L_2$ gets the join $L_1 \sqcup L_2 = L_1 \cup L_2$: it keeps the policies of both. Implicit flows are handled with a label for the program counter, as in the [security type system](/security-type-system/).
- **Declassification.** A process that runs with the authority of a set $A$ of principals may relabel a value from $L_1$ to $L_2$ if

$$L_1 \sqsubseteq L_2 \sqcup L_A, \qquad L_A = \{p : \ \mid p \in A\},$$

where "$p :$" is the policy of owner $p$ with no readers. Each policy of $L_1$ owned by a principal in $A$ is matched by $L_A$, so it may be weakened or removed; every other policy must still be matched in $L_2$.

**Integrity.** Section 4 of the journal paper adds integrity labels, whose policies name the principals that trust the data. They use the dual order: a value becomes less trusted when it is combined with untrusted data.

## What it counts

The model decides whether a flow is allowed: whether $L_1 \sqsubseteq L_2$, whether a principal may read a value, and whether a process with authority $A$ may declassify. Let $n$ be the number of policies in a label, $k$ the number of readers in a policy and $s$ the number of principals.

- With the acts-for relation stored as its transitive closure, an $s \times s$ table of $O(s^2)$ space, each test $p \succeq q$ takes $O(1)$ time in the [word-RAM](/word-ram/).
- $R(J) \subseteq R(I)$ holds if and only if each listed reader of $J$ acts for some listed reader of $I$, by transitivity. So $I \sqsubseteq J$ takes $O(k^2)$ time.
- $L_1 \sqsubseteq L_2$ takes $O(n^2 k^2)$ time, the join takes $O(n k)$ time, and a declassification check costs the same as a relabeling.

**Worked example.** Principals alice, bob, eve and hr, with bob $\succeq$ hr. Let $L = \{\mathit{alice}: \mathit{alice}, \mathit{hr}\}$, so $R = \{\mathit{alice}, \mathit{hr}, \mathit{bob}\}$.

| question | check | result |
|---|---|---|
| $L \sqsubseteq \{\mathit{alice}: \mathit{alice}\}$? | same owner, $\{\mathit{alice}\} \subseteq R$ | yes (a reader removed) |
| $L \sqsubseteq \{\mathit{alice}: \mathit{alice}, \mathit{bob}\}$? | bob acts for hr, so $\{\mathit{alice}, \mathit{bob}\} \subseteq R$ | yes (a reader that acts for a reader added) |
| $L \sqsubseteq \{\mathit{alice}: \mathit{alice}, \mathit{eve}\}$? | eve is not in $R$ | no |
| readers of $L \sqcup \{\mathit{hr}: \mathit{hr}, \mathit{bob}\}$ | $R \cap \{\mathit{hr}, \mathit{bob}\}$ | hr and bob |
| alice declassifies $\{\mathit{alice}: \mathit{alice}\}$ to $\{\mathit{alice}: \mathit{alice}, \mathit{eve}\}$? | the policy is matched by "alice :" in $L_A$ | yes |
| bob declassifies the same? | bob does not act for alice | no |

## Relation to other models

- **[Lattice model](/denning-lattice-model/).** The relation $\sqsubseteq$ is a preorder on labels. Two labels are equivalent if each is below the other, and the classes of equivalent labels form a lattice with the union as join, a [join-semilattice](/join-semilattice/) with a least element (the empty label). So the DLM is an instance of Denning's model with a large, structured lattice.
- **[Declassification](/declassification/).** Declassification is the general question of which releases are allowed. The DLM answers its *who* dimension: the owner of a policy, or a principal that acts for it, may release the data that the policy protects. It says nothing about *what* is released or *when*.
- **[Discretionary access control](/discretionary-access-control/).** As in DAC, each owner decides about its data. Unlike DAC, the policy follows the information into each copy and each computed value, so a reader cannot pass the data on to a principal the owner did not allow.
- **[Mandatory access control](/mandatory-access-control/).** MAC has one central policy and one authority. The DLM has many owners who do not trust each other, and no central authority.
- **[Trust management](/trust-management/).** The acts-for relation is a delegation relation, like the delegation of rights in trust management systems.
- **[Biba](/biba-integrity-model/).** The integrity labels of Section 4 play the role of Biba levels, with several owners.

## Known results in the model

- **Soundness and completeness of relabeling.** Myers and Liskov (1998) give a formal meaning to a label as the set of flows it allows, and prove that the rule $L_1 \sqsubseteq L_2$ above is sound (each allowed relabeling keeps every policy) and complete (each relabeling that keeps every policy is allowed by the rule).
- **Incremental rules.** Each allowed relabeling is a sequence of four safe steps (journal paper, Section 3.3): remove a reader, add a policy, add a reader that acts for an existing reader, and replace an owner by a principal that acts for it.
- **Join.** The join of two labels is their union (Section 3.5), and it is the least upper bound in the order $\sqsubseteq$.
- **Declassification rule.** The rule $L_1 \sqsubseteq L_2 \sqcup L_A$ lets a process weaken only the policies of the principals it acts for (Section 3.6).
- **Static checking.** Jif (formerly JFlow) checks the labels of a Java-like program at compile time, with label inference inside methods. Its rules extend the program counter rules of the [security type system](/security-type-system/). The papers cited here do not prove [noninterference](/noninterference/) for the whole of Jif; the proofs are for the label model and for small core languages.

## References
