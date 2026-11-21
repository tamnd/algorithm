---
tag: KBTQA8
kind: model
slug: clark-wilson-model
name: Clark-Wilson model
aliases:
- Clark-Wilson integrity model
area: security-and-privacy/access-control-and-information-flow
level: core
summary: A commercial integrity model in which constrained data items change only through certified transformation procedures run by authorized users.
model: word-ram
prereqs: [access-control-matrix, separation-of-duty]
see_also: [biba-integrity-model, separation-of-duty, role-based-access-control, reference-monitor, rice-theorem, bell-lapadula-model, chinese-wall-model, safety-property]
sources:
  - paper: doi:10.1109/SP.1987.10001
    title: "David D. Clark and David R. Wilson, A comparison of commercial and military computer security policies, Proceedings of the 1987 IEEE Symposium on Security and Privacy, pages 184 to 194"
    locator: "well-formed transactions and separation of duty; CDIs, UDIs, IVPs and TPs; the certification rules C1 to C5 and the enforcement rules E1 to E4"
  - book: isbn:9780321712332
    title: "Matt Bishop, Computer Security: Art and Science, second edition, Addison-Wesley, 2018"
    locator: "Chapter 6, Integrity Policies (the Clark-Wilson integrity model and its comparison with the Biba model)"
---

The Clark-Wilson model is a model of integrity for commercial systems. Its main idea is that users never change important data directly. They change it only by running certified programs, the *transformation procedures*, each of which takes the data from a valid state to a valid state, and the system records which user may run which program on which data. A second idea, *separation of duty*, splits each critical task between different people, so that one person alone cannot commit a fraud. Clark and Wilson gave the model in 1987 and argued that bookkeeping practice, not the lattice of levels in [Bell-LaPadula](/bell-lapadula-model/) or [Biba](/biba-integrity-model/), is the right base for commercial integrity.

## The machine

**Data.** The data items are of two kinds.

- *Constrained data items* (CDIs) are the data whose integrity the model protects, such as account balances.
- *Unconstrained data items* (UDIs) are inputs from outside, such as a form typed by a clerk. The model makes no promise about them.

**Procedures.** Two kinds of program act on the data.

- An *integrity verification procedure* (IVP) checks that the CDIs are in a valid state, for example that the books balance.
- A *transformation procedure* (TP) is a program that changes CDIs. It is the only way to change a CDI. A TP that works correctly is a *well-formed transaction*.

**Relations.** The system keeps two lists:

- the certified relations $(\mathit{TP}, \{\mathit{CDI}_1, \ldots, \mathit{CDI}_k\})$: the CDIs that each TP is certified to change;
- the access triples $(\mathit{user}, \mathit{TP}, \{\mathit{CDI}_1, \ldots, \mathit{CDI}_k\})$: which user may run which TP on which CDIs.

The triples are a restriction of the [access control matrix](/access-control-matrix/) in which the right to change a data item is held by a pair of a user and a program, not by a user alone.

**Rules.** Clark and Wilson give nine rules. The *certification* rules (C) are checked by people, the security officer and the auditors. The *enforcement* rules (E) are checked by the system.

| rule | text |
|---|---|
| C1 | Every IVP, when it runs, makes sure that all CDIs are in a valid state. |
| C2 | Every TP is certified to take a valid set of CDIs to a valid set. For each TP the security officer gives the set of CDIs it may change. |
| E1 | The system keeps the list of C2 and makes sure that a CDI changes only through a TP, and only as some certified relation allows. |
| E2 | The system keeps the list of access triples and makes sure that a user runs a TP on CDIs only as some triple allows. |
| C3 | The list of E2 is certified to meet the separation of duty requirement. |
| E3 | The system authenticates each user who tries to run a TP. |
| C4 | Every TP is certified to write to an append-only CDI, the log, all the information needed to reconstruct what it did. |
| C5 | Every TP that takes a UDI as input is certified to perform only valid changes, or no change, for every possible value of the UDI: it turns the UDI into a CDI or rejects it. |
| E4 | Only the agent allowed to certify an entity may change the lists of E1 and E2 for it, and an agent who can certify an entity has no right to run it. |

**Cost.** In the word RAM model, with the certified relations and the triples in hash sets, the checks of E1 and E2 for one request cost $O(1 + k)$ expected time for a request that names $k$ CDIs. The cost of the model is in the certification rules, which are not computations of the system.

## What it counts

The model answers two questions: is each run of a TP allowed (E1 to E3), and do the CDIs stay valid (C1, C2, C5)? The adversaries are two. The first is an *insider*: an authorized user who acts alone and tries to change data in a way the business rules forbid, for example to pay money to himself. Rules E2 and C3 defend against him, because every critical task needs the help of a second user. The second is a *program* that tries to change a CDI outside a TP; rule E1 defends against it, if the system enforces it as a [reference monitor](/reference-monitor/). The model gives no protection against all users of a separation of duty constraint acting together, nor against a TP that was certified by mistake.

**Example.** A bank keeps the account balances and the transaction log as CDIs. A paper deposit slip typed in by a clerk is a UDI. The IVP adds up all accounts and compares the result with the totals of deposits and withdrawals in the log; it runs at the end of each day. The TPs are deposit, withdraw and transfer, and each writes a log record (C4). The deposit TP reads the slip, checks that the account exists and the amount is positive, and either changes the balance or rejects the slip (C5). For transfers above a limit there are two TPs, enter-transfer and approve-transfer, and the access triples are certified so that no clerk holds both for the same accounts (C3). A clerk who wants to steal by a large transfer needs a second clerk to approve it, and the log shows both.

## Relation to other models

- **Biba.** [Biba](/biba-integrity-model/) labels data by the trust in its source. Clark-Wilson does not use levels: it asks that changes are made only by certified programs. Its CDIs and UDIs look like two integrity levels, and a TP that turns a UDI into a CDI under C5 is a certified upgrader, which the strict Biba policy has no place for.
- **Separation of duty.** C3 made [separation of duty](/separation-of-duty/), an old practice of accounting, a rule of an access control model. Later work states it as formal constraints on users and roles.
- **Role-based access control.** The access triples bind users to programs, and they are usually managed through roles: a role is a set of TPs, and C3 becomes a constraint on which roles one user may hold. This is one root of [role-based access control](/role-based-access-control/).
- **Chinese Wall.** The [Chinese Wall model](/chinese-wall-model/) is the other main commercial model, for conflicts of interest instead of integrity.
- **Bell-LaPadula.** [Bell-LaPadula](/bell-lapadula-model/) restricts who may read. Clark-Wilson restricts how data may change. Clark and Wilson pointed out that the military model has no notion of a well-formed transaction.

## Known results in the model

- **Validity is an invariant** (theorem). Assume that the CDIs are valid when the IVP has just run (C1), that each TP maps every valid state to a valid state (C2), that each TP that reads a UDI still maps valid states to valid states for every value of the UDI (C5), and that E1 holds. Then the CDIs are valid after every finite sequence of TP runs. The proof is induction on the length of the sequence, as for the [basic security theorem](/basic-security-theorem/), and validity is a [safety property](/safety-property/).
- **Enforcement is a lookup** (theorem). E1 and E2 are membership tests in finite sets, so the system can enforce them in $O(1 + k)$ expected time per request, as above.
- **Certification is undecidable in general** (theorem). By [Rice's theorem](/rice-theorem/), no algorithm decides, for every program and every decidable validity condition, whether the program maps valid states to valid states, because this is a nontrivial property of the function that the program computes. So C2 and C5 cannot be checked by one general tool. For a given TP they are proof tasks, done by review, testing or program verification, and they are the weak point of the model.
- **Separation of duty needs the lists** (theorem). A static separation of duty rule of the form "no user holds both TP $a$ and TP $b$ on the same CDI" can be checked on the list of triples in time linear in its size, with a hash map from each pair of user and CDI to its TPs.
- **The log is a defense in depth** (heuristic). C4 does not prevent a bad change. It lets the auditors find and reverse one, which is the practice of accounting that the model copies.

## References
