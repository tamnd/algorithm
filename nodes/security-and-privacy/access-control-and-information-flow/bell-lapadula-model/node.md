---
tag: ZK7BZV
kind: model
slug: bell-lapadula-model
name: Bell-LaPadula model
aliases:
- BLP model
- no read up no write down
area: security-and-privacy/access-control-and-information-flow
level: core
summary: A confidentiality model with security levels in which a subject may not read an object above its level nor write to an object below it.
model: word-ram
prereqs: [access-control-matrix, join-semilattice]
see_also: [basic-security-theorem, mandatory-access-control, biba-integrity-model, denning-lattice-model, noninterference, covert-channel, reference-monitor, harrison-ruzzo-ullman-model]
sources:
  - url: "https://csrc.nist.gov/files/pubs/conference/1998/10/08/proceedings-of-the-21st-nissc-1998/final/docs/early-cs-papers/bell76.pdf"
    title: "D. Elliott Bell and Leonard J. LaPadula, Secure Computer System: Unified Exposition and Multics Interpretation, MITRE MTR-2997 Rev. 1 (ESD-TR-75-306), March 1976"
    locator: "Section II, Description of the Model, pp. 9 to 29 (access attributes, the state (b, M, f, H), the ss-property, the *-property, the ds-property, rules); Section III, the Multics rules; Section IV, trusted subjects; Appendix, pp. 86 to 94 (formal definitions, Theorems A1 to A3 and Corollary A1)"
  - paper: doi:10.1109/SP.1987.10020
    title: "John McLean, Reasoning about security models, Proceedings of the 1987 IEEE Symposium on Security and Privacy"
    locator: System Z and the argument that a definition of security based only on secure states is not adequate
  - book: isbn:9780321712332
    title: "Matt Bishop, Computer Security: Art and Science, second edition, Addison-Wesley, 2018"
    locator: "Chapter 5, Confidentiality Policies"
  - book: isbn:9781119642787
    title: "Ross Anderson, Security Engineering, third edition, Wiley, 2020"
    locator: "Chapter 9, Multilevel Security, Section 9.3.2 (the Bell-LaPadula model) and Section 9.3.3 (the standard criticisms)"
---

The Bell-LaPadula (BLP) model is a state machine model of confidentiality for a computer system that holds data at several security levels. Each subject and each object has a level, and two rules hold in every state: a subject may observe only objects at or below its level (the *simple security property*, "no read up"), and a subject that is not trusted may alter only objects at or above its current level (the *\*-property*, "no write down"). A third rule, the *discretionary property*, requires each access to be allowed by an access matrix as well. Bell and LaPadula wrote the model at MITRE between 1973 and 1976 for a secure version of Multics. It is the main model of the class [mandatory access control](/mandatory-access-control/), and its [basic security theorem](/basic-security-theorem/) is the result that every transition that keeps the three properties keeps the system secure.

## The machine

The definitions follow the Unified Exposition of 1976.

**Levels.** A *security level* is a pair $(c, K)$ of a classification $c$ from a totally ordered set, such as unclassified < confidential < secret < top secret, and a set $K$ of categories, such as $\{\text{NATO}, \text{NUC}\}$. Level $(c_1, K_1)$ *dominates* $(c_2, K_2)$, written $(c_1, K_1)\ \text{dom}\ (c_2, K_2)$, if $c_1 \ge c_2$ and $K_1 \supseteq K_2$. Dom is a partial order. The levels form a lattice: the join of two levels is $(\max(c_1, c_2), K_1 \cup K_2)$ and the meet is $(\min(c_1, c_2), K_1 \cap K_2)$, so the set of levels is a [join-semilattice](/join-semilattice/) and also a meet-semilattice. In the flow reading used in the information flow pages, $\ell_1 \le \ell_2$ means that information may flow from $\ell_1$ to $\ell_2$; for BLP this is $\ell_2\ \text{dom}\ \ell_1$.

**Access attributes.** There are four: $e$ (execute: neither observe nor alter), $r$ (read: observe only), $a$ (append: alter only) and $w$ (write: observe and alter). The model gives them only these meanings, and each real access mode must be mapped to the attribute with the same effect.

**State.** A state is $v = (b, M, f, H)$:

- $b$ is the *current access set*, a set of triples $(S, O, x)$: subject $S$ now has access $x$ to object $O$;
- $M$ is the access permission matrix, with $M[S, O]$ a set of attributes, as in the [access control matrix](/access-control-matrix/);
- $f = (f_s, f_o, f_c)$ gives the maximum level $f_s(S)$ of each subject (its clearance), the level $f_o(O)$ of each object, and the *current level* $f_c(S)$ of each subject, with $f_s(S)\ \text{dom}\ f_c(S)$;
- $H$ is a hierarchy of the objects, a forest, used for the directories of Multics.

**Trusted subjects.** The set of subjects is split into $S'$, the subjects that must obey the \*-property, and the *trusted subjects* $S_T = S \setminus S'$, which are trusted not to move information down even though the rules allow them to.

**Transitions.** Inputs are requests and outputs are decisions from $\{yes, no, error, ?\}$. A *rule* is a function $\rho$ from a request and a state to a decision and a next state. The system $\Sigma(R, D, W, z_0)$ is the set of all sequences of requests, decisions and states that start in $z_0$ and in which each step $(x_t, y_t, z_t, z_{t-1})$ is in the relation $W$. Section III of the report gives eleven rules for Multics, among them get-read, get-append, get-write, release, give, rescind, create-object, delete-object-group and change-subject-current-security-level.

**Cost.** In the word RAM model, with levels stored as a classification and a bit set of categories, one dom test costs $O(1 + |K|/w)$ for word size $w$ bits, and checking one requested access against the three properties costs one or two dom tests and one matrix lookup.

## What it counts

The model decides whether a state is *secure* and whether a system keeps secure states. A state $v = (b, M, f, H)$ is secure if it has all three properties.

- **Simple security property (ss-property).** If $(S, O, x) \in b$ and $x \in \{r, w\}$, then $f_s(S)\ \text{dom}\ f_o(O)$. Only the attributes that observe are restricted: a subject may append to an object it may not read.
- **\*-property, relative to $S'$.** For each $S \in S'$: if $(S, O, a) \in b$ then $f_o(O)\ \text{dom}\ f_c(S)$; if $(S, O, w) \in b$ then $f_o(O) = f_c(S)$; if $(S, O, r) \in b$ then $f_c(S)\ \text{dom}\ f_o(O)$. So an untrusted subject that observes $O_1$ and alters $O_2$ at the same time has $f_o(O_2)\ \text{dom}\ f_o(O_1)$, which blocks a program from copying high data into a low object.
- **Discretionary security property (ds-property).** If $(S, O, x) \in b$ then $x \in M[S, O]$.

A system is secure if every state of every run is secure. The adversary of the model is a malicious program running as an untrusted subject, a Trojan horse, that tries to move information from a high object to a lower one through the accesses it is granted. The model protects containers, not information: it does not cover flows through timing, shared resources or the existence of objects, which are [covert channels](/covert-channel/), and it trusts the subjects in $S_T$ completely.

**Example.** Take classifications U < C < S < TS and a subject with $f_s = f_c = (S, \{\text{NATO}\})$. The table gives what the three level rules allow (the matrix $M$ is assumed to allow everything).

| object | level | read ($r$) | append ($a$) | write ($w$) |
|---|---|---|---|---|
| $o_1$ | (C, {NATO}) | yes | no | no |
| $o_2$ | (S, {NATO, NUC}) | no | yes | no |
| $o_3$ | (TS, {NATO}) | no | yes | no |
| $o_4$ | (U, {}) | yes | no | no |
| $o_5$ | (S, {NATO}) | yes | yes | yes |

The subject cannot read $o_2$ although its classification is equal, because it lacks the category NUC. If the subject lowers its current level to $f_c = (C, \{\text{NATO}\})$, it may write $o_1$, but it can no longer read $o_5$, since the \*-property for $r$ uses the current level. This is why the current level exists: a cleared user works at a lower level to produce lower-level output.

## Relation to other models

- **Mandatory access control.** [Mandatory access control](/mandatory-access-control/) is the class of policies in which a system-wide rule, not the owner, decides access. BLP is its standard model for confidentiality; the ds-property adds a [discretionary](/discretionary-access-control/) layer below the mandatory one.
- **Biba.** The [Biba integrity model](/biba-integrity-model/) is the dual of BLP for integrity: it forbids reading down and writing up in an order of trust.
- **Denning's lattice model.** The [Denning lattice model](/denning-lattice-model/) states the same flow rule, "information flows only up the lattice", for variables of a program instead of subjects and objects, and it covers implicit flows that BLP does not see.
- **Noninterference.** BLP restricts accesses. [Noninterference](/noninterference/) (Goguen and Meseguer 1982) restricts what low users can observe of the behavior of high users, which also rules out many covert channels. A system can satisfy the BLP properties and still leak through a channel that noninterference forbids.
- **HRU.** The [HRU model](/harrison-ruzzo-ullman-model/) asks whether some sequence of commands reaches a state, which is undecidable in general. BLP fixes the rules and asks whether each rule keeps an invariant, which can be checked rule by rule.
- **Reference monitor.** BLP is meant to be enforced by a [reference monitor](/reference-monitor/): the security kernel checks each request against the rules.

## Known results in the model

- **Basic security theorem** (Bell and LaPadula, Corollary A1 of the 1976 report; theorem). $\Sigma(R, D, W, z_0)$ is secure if and only if $z_0$ is secure and each transition that occurs keeps the ss-, \*- and ds-properties. Theorem A4 and its companions give the practical form: if each rule preserves the three properties, the system built from those rules is secure. See [basic security theorem](/basic-security-theorem/).
- **The critique of McLean** (1985, 1987). The basic security theorem holds for any property of states, by induction, so it says little about security by itself. McLean's System Z has one rule that, on any request, lowers every subject and object to the lowest level and then grants the access. Every state of System Z is secure in the BLP sense, yet it releases all data. The content of BLP is in its rules, not in the theorem.
- **Tranquility.** The answer to System Z is the tranquility principle. *Strong tranquility* says that levels never change while the system runs. *Weak tranquility* allows a change only if it does not violate the properties in the spirit of the policy. Neither is part of the 1976 definition of a secure state.
- **Trusted subjects.** The \*-property does not apply to $S_T$. Downgrading and many system services must run as trusted subjects, and the model gives no rule for what they may do. Section IV of the report discusses this gap.
- **Checking a state.** Whether a given state is secure can be checked in $O(|b|)$ dom tests and matrix lookups in the word RAM model.

## References
