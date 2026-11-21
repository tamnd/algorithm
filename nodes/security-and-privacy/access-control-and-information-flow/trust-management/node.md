---
tag: 3DX18Y
kind: concept
slug: trust-management
name: Trust management
aliases:
- decentralized trust management
area: security-and-privacy/access-control-and-information-flow
level: advanced
summary: Authorization by checking that signed credentials and local policy together prove that a key may perform an action, without a central user list.
prereqs: [digital-signature]
see_also: [authorization-logic, digital-signature, datalog, semi-naive-evaluation, role-based-access-control, attribute-based-access-control, access-control-list, capability-list]
sources:
  - paper: doi:10.1109/SECPRI.1996.502679
    title: "Matt Blaze, Joan Feigenbaum and Jack Lacy, Decentralized trust management, Proceedings of the 1996 IEEE Symposium on Security and Privacy, pages 164 to 173"
    locator: the trust management problem, the PolicyMaker system and its assertions
  - paper: doi:10.1007/BFb0055488
    title: "Matt Blaze, Joan Feigenbaum and Martin Strauss, Compliance checking in the PolicyMaker trust management system, Financial Cryptography 1998, LNCS 1465, pages 254 to 274"
    locator: the proof of compliance problem, its undecidability in general, NP-hardness in restricted cases and a polynomial time special case
  - paper: doi:10.1145/1066100.1066103
    title: "Ninghui Li, John C. Mitchell and William H. Winsborough, Beyond proof-of-compliance: security analysis in trust management, Journal of the ACM 52(3), 2005, pages 474 to 514"
    locator: the RT credentials, their logic program semantics, and the complexity of safety, availability and containment analysis
  - url: "https://www.rfc-editor.org/rfc/rfc2704"
    title: "Matt Blaze, Joan Feigenbaum, John Ioannidis and Angelos D. Keromytis, The KeyNote Trust-Management System Version 2, RFC 2704, 1999"
    locator: "assertions, the Authorizer, Licensees and Conditions fields, and the compliance checker"
  - url: "https://www.rfc-editor.org/rfc/rfc2693"
    title: "Carl Ellison, Bill Frantz, Butler Lampson, Ron Rivest, Brian Thomas and Tatu Ylonen, SPKI Certificate Theory, RFC 2693, 1999"
    locator: authorization certificates, delegation and the reduction of certificate chains
---

Trust management is an approach to authorization in which the service that receives a request does not look the requester up in a local list of users. Instead, the requester sends signed *credentials*, statements by other keys about what a key may do, and the service runs a *compliance checker* that decides whether its own local *policy* together with these credentials authorizes the request. Blaze, Feigenbaum and Lacy named the approach in 1996, with the PolicyMaker system. The idea fits systems without one administrator, such as services on the internet that must accept users from many organizations, because each party states only what it knows and the checker combines the statements.

## In plain words

Think of a shop that gives a discount to students. The shop does not know every student. It knows a few groups it trusts, such as a board that lists real universities. A student brings a signed paper from her university that says she is a student, and the board's signed paper that says the university is real. The shop's rule says that a student of a real university gets the discount. A program at the shop checks the papers against the rule and answers yes or no. Nobody had to put the student into the shop's list beforehand. Each paper must carry a signature that the program can check, so a person cannot simply write a paper for himself. The papers can come from many places, and the shop's own rule decides which of them count.

## The idea

**The trust management problem.** A trust management system answers one kind of question: given a request $r$, a set $C$ of credentials and a local policy $P$, does $C$ prove that $r$ complies with $P$? The checker does not need the identity of the requester in the usual sense. It works with public keys and with what signed statements say about them. This joins authentication and access control in one step.

**Parts.**

- *Principals* are public keys, or names that keys define.
- A *credential* is a statement signed by a principal, for example "key $K_B$ may read the files of project X" or "anyone my key calls a student is a student".
- The *policy* is a set of statements that the checker trusts without a signature, because they are local.
- The *compliance checker* is the algorithm that decides the question above.

**Adversary.** The adversary may send any set of credentials, make new keys and sign any statements with them, and replay credentials it has seen. It cannot forge signatures of keys it does not control; this is the existential unforgeability of the [digital signature](/digital-signature/) scheme under chosen message attack. Under this assumption a statement by a key that the policy never trusts, directly or through a chain, has no effect, and the security of the decision rests on the policy and on the soundness of the checker.

**Monotonicity** (theorem for the languages below). In PolicyMaker, KeyNote, SPKI and RT, adding credentials can only change a "no" into a "yes", never the reverse. So an adversary gains nothing by hiding credentials, and the checker may stop as soon as it has a proof. The price is that the languages have no negative statements, and revocation is outside the core model. Systems handle it by expiry dates and by checks outside the compliance checker.

**Compliance checking is hard in general** (Blaze, Feigenbaum and Strauss 1998; theorem). In PolicyMaker, assertions can be arbitrary programs, so the proof of compliance problem is undecidable. It stays NP-hard under several natural restrictions, and the paper gives a polynomial time algorithm for a restricted class of monotone assertions. Later languages were designed so that compliance checking is efficient by construction.

**Languages with logic program semantics.** The RT family of Li, Mitchell and Winsborough writes credentials as role statements. In RT0 there are four forms, where $A.r$ is the role $r$ defined by principal $A$:

1. $A.r \leftarrow B$: $B$ is in $A.r$;
2. $A.r \leftarrow B.s$: every member of $B.s$ is in $A.r$;
3. $A.r \leftarrow A.s.t$: every member of $B.t$, for each $B$ in $A.s$, is in $A.r$ (a *linked role*);
4. $A.r \leftarrow B_1.s_1 \cap B_2.s_2$: every member of both roles is in $A.r$.

Each form is one [Datalog](/datalog/) rule over a predicate $\mathit{member}(A, r, X)$. For example, form 3 becomes $\mathit{member}(A, r, X) \leftarrow \mathit{member}(A, s, B), \mathit{member}(B, t, X)$. The meaning of a set of credentials is the least model of the program, so membership is decidable in polynomial time, for example by [semi-naive evaluation](/semi-naive-evaluation/).

**Security analysis** (Li, Mitchell and Winsborough 2005; theorem). Beyond a single request, an owner may ask what can happen when other principals add or remove credentials, within limits that the owner fixes. Questions such as "can a role ever contain an untrusted principal?" (safety) and "will a role always contain a given principal?" (availability) are decidable efficiently in RT0 by logic programs. *Containment*, "is every member of one role always a member of another?", is decidable but intractable.

## Examples

**Credential chain in RT0.** A store gives a discount to students of accredited universities. Its policy and the credentials are:

1. $\text{Store}.\text{discount} \leftarrow \text{Store}.\text{university}.\text{student}$ (policy);
2. $\text{Store}.\text{university} \leftarrow \text{ABU}.\text{accredited}$ (policy: the store trusts the accreditation board ABU);
3. $\text{ABU}.\text{accredited} \leftarrow \text{StateU}$ (signed by ABU);
4. $\text{StateU}.\text{student} \leftarrow \text{Alice}$ (signed by StateU).

From 3 and 2, StateU is in $\text{Store}.\text{university}$. With 4, Alice is in $\text{StateU}.\text{student}$, so by the linked role in 1 she is in $\text{Store}.\text{discount}$. The store never knew Alice or StateU. If credential 3 is missing, no rule derives StateU as a university, and the answer is no. A credential "$\text{StateU}.\text{student} \leftarrow \text{Mallory}$" signed by a key Mallory made has no effect, because only the key of StateU can sign statements about $\text{StateU}.\text{student}$.

**KeyNote.** In KeyNote, an assertion has an Authorizer, a set of Licensees and Conditions on the attributes of the action. A policy assertion has the Authorizer "POLICY". The checker computes, for a request with given attributes, a compliance value from an ordered set such as {false, true}, by following delegation from POLICY to the keys that signed the request.

## Where it is used

- **Systems in the original line.** PolicyMaker (1996), KeyNote (RFC 2704) and SPKI/SDSI (RFC 2693), in which authorization certificates delegate rights from key to key and a chain of certificates is reduced to one statement.
- **Logic-based languages.** RT, Binder, SecPAL and later Datalog-based policy languages, and the [authorization logics](/authorization-logic/) of the speaks-for line, which give the same reasoning a modal semantics.
- **Attribute-based systems.** [Attribute-based access control](/attribute-based-access-control/) across organizations, where attributes come as signed assertions from identity providers.
- **Contrast with lists.** An [access control list](/access-control-list/) names the users at the service. A trust management credential is closer to a [capability](/capability-list/) that carries its own proof, and [role-based access control](/role-based-access-control/) becomes decentralized when each principal defines its own roles, as in RT.

## References
