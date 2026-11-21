---
tag: EFKQSM
kind: model
slug: mandatory-access-control
name: Mandatory access control
aliases:
- nondiscretionary access control
area: security-and-privacy/access-control-and-information-flow
level: intro
summary: An access control model in which a system-wide policy on labels of subjects and objects decides access, and users cannot override it.
model: word-ram
prereqs: [access-control-matrix, discretionary-access-control]
see_also: [discretionary-access-control, bell-lapadula-model, biba-integrity-model, denning-lattice-model, basic-security-theorem, covert-channel, reference-monitor, role-based-access-control]
sources:
  - paper: "Department of Defense, Trusted Computer System Evaluation Criteria, DoD 5200.28-STD, December 1985"
    locator: the glossary entries for mandatory access control and sensitivity labels, and the mandatory access control requirements of the classes of division B
  - paper: "D. Elliott Bell and Leonard J. LaPadula, Secure computer system, unified exposition and Multics interpretation, MITRE technical report MTR-2997, 1976"
    locator: the simple security property, the star property and the discretionary security property
  - paper: doi:10.1145/354876.354878
    title: Sylvia Osborn, Ravi Sandhu and Qamar Munawer, Configuring role-based access control to enforce mandatory and discretionary access control policies, ACM Transactions on Information and System Security 3(2), 2000
    locator: pages 85 to 106 (lattice-based mandatory policies as role-based configurations)
  - paper: doi:10.1109/PROC.1975.9939
    title: Jerome H. Saltzer and Michael D. Schroeder, The protection of information in computer systems, Proceedings of the IEEE 63(9), 1975
    locator: pages 1278 to 1308 (controls that a user cannot change, and the compartments of a system)
  - paper: "Matt Bishop, Computer Security: Art and Science, second edition, Addison-Wesley, 2018, ISBN 9780321712332"
    locator: Chapter 4, Section 4.4 (types of access control, discretionary and mandatory)
---

Mandatory access control (MAC) is the class of access control policies in which a rule fixed for the whole system decides access, from labels attached to subjects and objects, and no ordinary user can change the rule or the labels. In the TCSEC (1985), the rule restricts access by the sensitivity of the information in an object, given by its label, and the formal authorization, the clearance, of the subject. The owner of a file cannot grant a reader who lacks the clearance, and a program cannot copy secret data into a public file, even when every discretionary right allows it. MAC is the counterpart of [discretionary access control](/discretionary-access-control/): the two differ in who may change the policy. The [Bell-LaPadula model](/bell-lapadula-model/) is the main model of the class for confidentiality and the [Biba model](/biba-integrity-model/) for integrity; MAC is the class, and these are models in it.

## The machine

**State.** A protection state $(S, O, A)$ as in the [access control matrix](/access-control-matrix/), and in addition:

- a finite set $L$ of labels with a partial order *dom* ("dominates"), usually a lattice;
- a label function $\mathrm{lab}$ that maps each subject and each object to a label.

A common label is a pair $(\ell, C)$ of a level $\ell$ from a total order, such as unclassified < confidential < secret < top secret, and a set $C$ of categories, such as {crypto, nuclear}. Then $(\ell_1, C_1)$ dom $(\ell_2, C_2)$ exactly when $\ell_1 \ge \ell_2$ and $C_1 \supseteq C_2$. The labels with this order form a lattice, the [Denning lattice](/denning-lattice-model/) of security classes.

**Decision.** A request $(s, o, r)$ is allowed when the discretionary matrix allows it and the mandatory rule allows it. For the confidentiality rule of Bell and LaPadula, with the rights read and write:

```pseudo id=main
CHECK(s, o, r)
L1  if r ∉ A[s, o] then return false             ▷ the discretionary part
L2  if r = read then return lab(s) dom lab(o)     ▷ no read up
L3  if r = write then return lab(o) dom lab(s)    ▷ no write down
L4  return false
```

Line L2 lets a subject read only objects at or below its own label. Line L3 lets it write only objects at or above its label, so that it cannot copy what it read into a place with a lower label. The Biba rule for integrity turns both tests around: read only at or above, write only at or below.

**Transitions.** Users change the matrix $A$ by discretionary commands, as on the [DAC](/discretionary-access-control/) page. No user command changes $\mathrm{lab}$ or the order *dom*. Only a trusted subject, such as a security officer, may set a label, or lower the label of an object (declassify it); the [reference monitor](/reference-monitor/) applies the rule at each access.

**Example.** Take two labels, low and high, with high dom low. Bob is high, carol is low, f1 is high and the file g of carol is low. The Trojan horse of the [DAC](/discretionary-access-control/) page runs as bob: it reads f1, which line L2 allows because high dom high, and tries to write g. Line L3 denies this, because low does not dominate high, whatever rights the matrix gives. The same program run by carol cannot read f1 at all, by line L2. The data of f1 can reach carol only through a declassification by a trusted subject, or through a [covert channel](/covert-channel/), which the access rule does not see.

## What it counts

**The access decision.** One lookup in the matrix and one test of *dom*. With $c$ categories stored as a bit mask of $c$ bits, the test is one comparison of levels and one subset test, so it takes $O(1)$ time in the [word RAM](/word-ram/) when $c$ fits in a word, and $O(c)$ bit operations in general. The label of each subject and object costs $O(\log \lambda + c)$ bits, where $\lambda$ is the number of levels.

**Safety.** The question changes from "can a right leak?" to "can information flow from a high label to a lower one?". For Bell-LaPadula with no trusted subjects, each access that the rule allows moves information only upward in *dom*, so no sequence of allowed accesses moves it down; this is the content of the [basic security theorem](/basic-security-theorem/). The discretionary part can still leak rights, but a leaked right cannot pass the mandatory test.

## Relation to other models

- **DAC.** In [DAC](/discretionary-access-control/) the holders of rights change the policy; in MAC only the system does. Most systems apply both, as line L1 shows: MAC limits what DAC can grant.
- **Bell-LaPadula and Biba.** The [Bell-LaPadula model](/bell-lapadula-model/) is MAC for confidentiality with the rule above, and the [Biba model](/biba-integrity-model/) is MAC for integrity with the dual rule. Using both with the same labels allows reads and writes only at the same label.
- **Lattice models of flow.** The [Denning lattice model](/denning-lattice-model/) explains why the labels form a lattice: the label of data computed from two inputs is their join. [Noninterference](/noninterference/) states the goal of MAC as a property of the whole system, not of single accesses.
- **RBAC.** Osborn, Sandhu and Munawer (2000) showed how to configure [role-based access control](/role-based-access-control/) so that it enforces lattice-based MAC, with a role for each label and separate roles for reading and for writing. RBAC shares the main trait of MAC: the administrator, not the user, assigns roles.
- **Other mandatory rules.** Type enforcement, as in SELinux, labels each process with a domain and each object with a type, and a fixed table says which domain may do what to which type. The table has no order, so it is MAC without a lattice.

## Known results in the model

- **Decision.** One matrix lookup and one *dom* test, $O(1)$ time in the word RAM for labels that fit in a word.
- **No flow downward.** For a Bell-LaPadula system with no trusted subjects, every reachable state is secure if the initial state is and every transition keeps the two properties; see the [basic security theorem](/basic-security-theorem/).
- **Simulation.** RBAC with suitable constraints can enforce lattice-based MAC (Osborn, Sandhu and Munawer 2000).
- **Limits.** The rule is about single accesses. It does not stop flows through shared resources that are not objects, such as timing or the state of a disk arm; the TCSEC asks for an analysis of these [covert channels](/covert-channel/) in its higher classes, and the [confinement problem](/confinement-problem/) states the general question.

## References
