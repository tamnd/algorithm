---
tag: G0KNYR
kind: model
slug: discretionary-access-control
name: Discretionary access control
aliases:
- DAC
- owner-controlled access
area: security-and-privacy/access-control-and-information-flow
level: intro
summary: An access control model in which a subject that holds a right, usually the owner of the object, decides who else may access the object and may pass rights on.
model: word-ram
prereqs: [access-control-matrix]
see_also: [mandatory-access-control, access-control-list, harrison-ruzzo-ullman-model, take-grant-model, role-based-access-control, confinement-problem, bell-lapadula-model, capability-list]
sources:
  - paper: "Department of Defense, Trusted Computer System Evaluation Criteria, DoD 5200.28-STD, December 1985"
    locator: the glossary entry for discretionary access control, and the discretionary access control requirements of the classes of division C
  - paper: doi:10.1145/1478873.1478928
    title: G. Scott Graham and Peter J. Denning, Protection, principles and practice, AFIPS Spring Joint Computer Conference, 1972
    locator: pages 417 to 429 (the owner and control rights, the copy flag, and the rules that create, grant, transfer and delete rights)
  - paper: doi:10.1145/775265.775268
    title: Butler W. Lampson, Protection, Proceedings of the 5th Princeton Conference on Information Sciences and Systems, 1971, reprinted in ACM SIGOPS Operating Systems Review 8(1), 1974
    locator: pages 18 to 24 of the reprint (the owner of an object and the copy flag on a right)
  - paper: doi:10.1145/360303.360333
    title: Michael A. Harrison, Walter L. Ruzzo and Jeffrey D. Ullman, Protection in operating systems, Communications of the ACM 19(8), 1976
    locator: pages 461 to 471 (commands and the safety question, and its undecidability for arbitrary command sets)
  - paper: doi:10.1109/SP.2005.14
    title: Ninghui Li and Mahesh V. Tripunitara, On safety in discretionary access control, IEEE Symposium on Security and Privacy, 2005
    locator: pages 96 to 109 (safety in the Graham-Denning scheme is decidable by an efficient algorithm)
  - paper: doi:10.1145/354876.354878
    title: Sylvia Osborn, Ravi Sandhu and Qamar Munawer, Configuring role-based access control to enforce mandatory and discretionary access control policies, ACM Transactions on Information and System Security 3(2), 2000
    locator: pages 85 to 106 (variants of discretionary policies and their simulation in role-based access control)
  - paper: "Matt Bishop, Computer Security: Art and Science, second edition, Addison-Wesley, 2018, ISBN 9780321712332"
    locator: Chapter 4, Section 4.4 (types of access control, discretionary and mandatory) and Chapter 2 (copying and owning rights)
---

Discretionary access control (DAC) is the class of access control policies in which the subjects that hold rights decide who else gets them. The Trusted Computer System Evaluation Criteria (TCSEC, 1985) define it as "a means of restricting access to objects based on the identity of subjects and/or groups to which they belong", discretionary "in the sense that a subject with a certain access permission is capable of passing that permission (perhaps indirectly) on to any other subject (unless restrained by mandatory access control)". In the usual form the creator of an object becomes its owner, and the owner grants and revokes rights on it. The model is the [access control matrix](/access-control-matrix/) with a command set of this kind. It is the policy of Unix file permissions and of most file systems. Its counterpart is [mandatory access control](/mandatory-access-control/): the two differ in who may change the policy, the users or only the system.

## The machine

**State.** A protection state $(S, O, A)$ as in the [access control matrix](/access-control-matrix/), with a right *own* in $R$, and for each right $r$ a copy flag: a subject that holds $r^*$ on an object holds $r$ and may pass it on. Write $s$, $o$ and $r$ for the numbers of subjects, objects and rights.

**Transitions.** A command set is discretionary when each command that changes the column of an object $o$ is run by a subject $x$ and has a condition on the rights of $x$ on $o$: *own*, or the copy flag of the right it passes. A typical set, close to the rules of Graham and Denning, is:

```pseudo id=main
command CREATE(x, o)
L1  create object o
L2  enter own into A[x, o]                ▷ the creator is the owner

command GRANT(x, y, o, r)
L3  if own in A[x, o] then enter r into A[y, o]

command COPY(x, y, o, r)
L4  if r* in A[x, o] then enter r into A[y, o]

command REVOKE(x, y, o, r)
L5  if own in A[x, o] then delete r from A[y, o]

command GIVE-AWAY(x, y, o)
L6  if own in A[x, o] then
L7      enter own into A[y, o]; delete own from A[x, o]
```

The variants of DAC differ in which of these commands exist:

- **Strict DAC.** Only the owner grants rights (lines L3 and L5). Nobody else can pass a right on, and ownership never moves.
- **Liberal DAC.** Holders of a right may pass it on (line L4). This can be limited to one or two levels of passing, or be unlimited.
- **DAC with a change of owner.** Line L6 lets the owner give the object away. Some systems allow several owners.

Who may revoke, and whether revoking a right also revokes the copies made from it, is another choice. The [capability list](/capability-list/) page shows the cascading form with a derivation tree.

**Example.** Take the matrix of the [access control matrix](/access-control-matrix/) page: alice owns f1, bob owns f2, and bob and carol may write the printer p. GRANT(alice, carol, f1, r) enters r into $A[\text{carol}, \text{f1}]$, because alice owns f1. GRANT(carol, alice, f2, w) does nothing, because carol does not own f2. If alice instead holds $r^*$ on f2, COPY(alice, carol, f2, r) passes the right on without bob's consent: the policy for f2 is now partly in alice's hands.

## What it counts

**The access decision.** For a stored state, a request $(s, o, r)$ is allowed when $r \in A[s, o]$: one lookup, in $O(1)$ time with a full matrix, or a scan of one [access control list](/access-control-list/).

**Safety.** Can a right $r$ reach a cell from a given state, by the commands of the scheme? With the plain HRU definition that this site uses on the [access control matrix](/access-control-matrix/) page, any state with an owner is unsafe for each right, because an owner can always grant it. The useful question is narrower: can subject $y$ get $r$ on $o$ when only some subjects act, for example when the trusted owners do not run commands? Li and Tripunitara (2005) answer this form for the Graham-Denning scheme.

**What DAC does not count: information flow.** DAC controls who may access an object. It does not control where the data go after a read. A program that bob runs has all of bob's rights. Suppose carol owns a file g and grants bob w on it, and bob runs a program from carol. The program reads f1, which alice owns and bob may read, and writes the content into g, which bob may write; then carol reads g. Every access in this sequence is allowed, and carol now has the content of f1, although alice never granted her any right on it. This is the Trojan horse problem. No discretionary command set can stop it, because the program acts with the full authority of its user; this is the reason for [mandatory access control](/mandatory-access-control/) and for the study of the [confinement problem](/confinement-problem/).

## Relation to other models

- **Access matrix and HRU.** A DAC system is an [HRU system](/harrison-ruzzo-ullman-model/) whose commands test ownership or a copy flag. The [Take-Grant model](/take-grant-model/) is a DAC model in graph form, where take and grant are the rights that pass other rights.
- **Mandatory access control.** In [MAC](/mandatory-access-control/), a system-wide policy on labels decides, and no user can change it. Real systems combine the two: an access is allowed only if both the mandatory rule and the discretionary matrix allow it. The [Bell-LaPadula model](/bell-lapadula-model/) has a discretionary matrix as one of its properties.
- **Role-based access control.** In [RBAC](/role-based-access-control/), an administrator assigns users to roles, so the users do not decide. Osborn, Sandhu and Munawer (2000) showed how to configure RBAC so that it enforces discretionary policies, with roles for each object and administrative rights over them.
- **Storage.** DAC is usually stored as [access control lists](/access-control-list/), because the owner must see and edit the list of each object. With [capabilities](/capability-list/), passing a capability is a discretionary act by its holder.

## Known results in the model

- **Decision.** For a stored state the decision is one lookup.
- **Arbitrary commands.** With arbitrary commands the model is the HRU model, and HRU (1976) showed that no algorithm decides safety for every command set. This does not make a fixed DAC scheme undecidable; the result is about the class of all command sets.
- **The Graham-Denning scheme.** Li and Tripunitara (2005) showed that safety in the Graham-Denning scheme is decidable, with an efficient algorithm, so the undecidability of HRU does not carry over to this scheme.
- **Simulation in RBAC.** Osborn, Sandhu and Munawer (2000) gave RBAC configurations that enforce discretionary policies, and also lattice-based mandatory policies.
- **Information flow.** DAC cannot stop a program from passing data to a subject that has no right on the source, as the example in "What it counts" shows. This is a property of the model, not of an implementation.

## References
