---
tag: PGCFA7
kind: model
slug: authorization-logic
name: Authorization logic
aliases:
- ABLP logic
- speaks-for calculus
area: security-and-privacy/access-control-and-information-flow
level: advanced
summary: A modal logic of principals, says and speaks for, used to reason about who authorized a request in a distributed system.
model: word-ram
prereqs: [kripke-structure, digital-signature]
see_also: [trust-management, kripke-structure, digital-signature, access-control-list, kerberos, needham-schroeder-protocol, datalog, curry-howard-correspondence]
sources:
  - paper: doi:10.1145/155183.155225
    title: "Martin Abadi, Michael Burrows, Butler Lampson and Gordon Plotkin, A calculus for access control in distributed systems, ACM Transactions on Programming Languages and Systems 15(4), 1993, pages 706 to 734"
    locator: "the calculus of principals (and, quoting, roles, delegation), the axioms for says and speaks for, the Kripke semantics, the undecidability of the calculus of principals and the decidable access control cases"
  - paper: doi:10.1145/138873.138874
    title: "Butler Lampson, Martin Abadi, Michael Burrows and Edward Wobber, Authentication in distributed systems: theory and practice, ACM Transactions on Computer Systems 10(4), 1992, pages 265 to 310"
    locator: "the speaks-for relation, channels, certificates, the handoff rule, delegation and their use in the Taos operating system"
  - paper: doi:10.1007/978-3-540-78499-9_16
    title: "Deepak Garg and Martin Abadi, A modal deconstruction of access control logics, Foundations of Software Science and Computation Structures (FoSSaCS) 2008, LNCS, pages 216 to 230"
    locator: the translation of access control logics into the modal logic S4 and the decidability results derived from it
---

An authorization logic is a logic for reasoning about which principal stated or authorized a request in a distributed system. Its two main operators are *says*, for what a principal states, and *speaks for*, for the delegation of authority from one principal to another. A file server can then state its rule as "grant read on $f$ if Alice says read $f$", and prove from signed messages, certificates and its own beliefs that a request on a network channel comes from Alice. The standard form, the speaks-for calculus, comes from Lampson, Abadi, Burrows and Wobber (1992) and from Abadi, Burrows, Lampson and Plotkin (1993), who built it for the Taos operating system at DEC. Later logics of the same kind give it other semantics or a Datalog core.

## The machine

**Principals.** Atomic principals are users, machines, keys, channels and roles. Compound principals are built with two operators.

- $A \wedge B$, "$A$ and $B$": a principal that says only what both $A$ and $B$ say. It models joint authority.
- $A \mid B$, "$A$ quoting $B$": the principal $A$ that says that $B$ says something. It models a request that $A$ passes on for $B$, without proof that $B$ made it.

The papers also define $A$ *as* $R$ (Alice in a role $R$) and $B$ *for* $A$ (delegation) from these two operators and special principals.

**Formulas.** Formulas are built from atomic statements, such as "read $f$", with the connectives of propositional logic, with $A \text{ says } s$, and with $A \Rightarrow B$, "$A$ speaks for $B$".

**Axioms.** The logic has all propositional tautologies and modus ponens, and:

1. $(A \text{ says } (s \supset t)) \supset ((A \text{ says } s) \supset (A \text{ says } t))$;
2. if $s$ is a theorem, then $A \text{ says } s$ is a theorem;
3. $((A \wedge B) \text{ says } s) \equiv ((A \text{ says } s) \wedge (B \text{ says } s))$;
4. $((A \mid B) \text{ says } s) \equiv (A \text{ says } (B \text{ says } s))$;
5. $(A \Rightarrow B) \equiv (A = A \wedge B)$;
6. $(A \Rightarrow B) \supset ((A \text{ says } s) \supset (B \text{ says } s))$;
7. handoff: $(A \text{ says } (B \Rightarrow A)) \supset (B \Rightarrow A)$.

Here $\wedge$ is associative, commutative and idempotent, and $\mid$ is associative and distributes over $\wedge$ on both sides. Axioms 1 and 2 make each "$A$ says" a normal modal operator. Axiom 7 says that a principal may hand its own authority to another.

**Semantics.** A model is a set of worlds, as in a [Kripke structure](/kripke-structure/), with a binary relation $R(A)$ on worlds for each principal. Then $A \text{ says } s$ holds at $w$ if $s$ holds at every $w'$ with $w \mathrel{R(A)} w'$. The operators are $R(A \wedge B) = R(A) \cup R(B)$ and $R(A \mid B) = R(A) \circ R(B)$, the composition, and $A \Rightarrow B$ holds when $R(B) \subseteq R(A)$. The papers treat the handoff axiom apart from these basic rules.

**From messages to formulas.** The connection to the system is by assumptions that the implementation must make true. A message $m$ that verifies under a public key $K$ with a [digital signature](/digital-signature/) scheme gives $K \text{ says } m$. A message that arrives on a secure channel $C$ gives $C \text{ says } m$. A certificate is a signed statement $K_{CA} \text{ says } (K \Rightarrow A)$.

**Cost.** In the word RAM model, a proof is a list of formulas, each an axiom instance or the result of a rule applied to earlier lines. With formulas stored as syntax trees, checking that each line is an axiom instance or follows by a rule costs time polynomial in the total size of the proof, and linear when the principals are kept in a normal form for the laws of $\wedge$ and $\mid$. The signature checks for the messages it uses come on top.

## What it counts

The logic decides whether the beliefs of a server, together with the statements it has received, prove that a principal on its access list authorized a request. An access list entry "Alice may read $f$" becomes the rule "if a principal that speaks for Alice says read $f$, grant it".

**Adversary.** The adversary controls the network: it reads, replays, delays and injects messages, and it has keys and channels of its own. It cannot forge signatures under keys it does not hold. Under this assumption a formula $K \text{ says } m$ that the server derives from a signature check is true. The soundness statement of the logic is then: if every premise is true, every derived formula is true, so a derived "Alice says read $f$" means that Alice, or a principal she chose to let speak for her, made the request. Replays of an old signed request are outside the logic; the papers handle them with timestamps and nonces in the statements.

**Example.** A file server holds the access list entry "Alice may read $f$". Its premises are:

1. $K_{CA} \Rightarrow \text{CA}$ (the server knows the key of the certification authority);
2. $(\text{CA} \text{ says } (K_A \Rightarrow \text{Alice})) \supset (K_A \Rightarrow \text{Alice})$ (the server trusts CA on the keys of users);
3. $K_{CA} \text{ says } (K_A \Rightarrow \text{Alice})$ (a certificate that verifies under $K_{CA}$);
4. $K_W \text{ says } (\text{read } f)$ (a request that verifies under the key $K_W$ of Alice's workstation);
5. $K_A \text{ says } (K_W \Rightarrow K_A)$ (Alice's key delegates to the workstation key).

From 1 and 3 by axiom 6, CA says $(K_A \Rightarrow \text{Alice})$, so by 2, $K_A \Rightarrow \text{Alice}$. By handoff on 5, $K_W \Rightarrow K_A$. Two uses of axiom 6 on 4 give $K_A \text{ says read } f$ and then $\text{Alice} \text{ says read } f$, and the access list grants the request. Without 5, nothing links $K_W$ to Alice, and the server refuses. A statement $K_M \text{ says } (K_M \Rightarrow \text{Alice})$ under the adversary's key $K_M$ does not help it: handoff needs Alice, or a principal that speaks for her, to say it.

## Relation to other models

- **Access control lists.** The logic explains what an [access control list](/access-control-list/) entry means when the requester is a key or a channel and not a local user: the request is granted if its source speaks for a principal on the list.
- **Trust management.** [Trust management](/trust-management/) systems answer the same question, whether credentials and policy authorize a request, with a checker instead of a logic. Many later logics of this kind, such as Binder and SecPAL, are close to Datalog and so are also trust management languages.
- **Logics of authentication.** The logic of Burrows, Abadi and Needham (1989) reasons about beliefs in authentication protocols such as [Kerberos](/kerberos/) and the [Needham-Schroeder protocol](/needham-schroeder-protocol/). The speaks-for calculus reasons about the authority of principals once the channels are known.
- **Modal logic.** Each "$A$ says" is a box operator of a normal modal logic, with one accessibility relation per principal, as in multi-agent epistemic logic.
- **Proofs as objects.** In *proof-carrying authorization* (Appel and Felten 1999), the requester sends a proof in the logic and the server only checks it. The proofs are terms in the style of the [Curry-Howard correspondence](/curry-howard-correspondence/), which several later constructive authorization logics use.

## Known results in the model

- **The calculus of principals is undecidable** (Abadi, Burrows, Lampson and Plotkin 1993; theorem). With the equations for $\wedge$ and $\mid$, the set of valid formulas of the calculus of principals is not recursive. The same paper gives decision procedures for the restricted questions that access control asks, where the access list and the premises have a simple form.
- **Embedding into S4** (Garg and Abadi 2008; theorem). Several access control logics, among them constructive ones with says and speaks for, translate into the modal logic S4 in a way that is sound and complete. Known decision procedures for S4 then give decidability results for those logics.
- **Datalog cores have polynomial data complexity** (theorem). When the logic is a Datalog program with says as an extra argument of each predicate, as in Binder, the derivable facts for a fixed policy can be computed in time polynomial in the number of credentials, by the least fixpoint of [Datalog](/datalog/).
- **Proof checking is cheap** (theorem). Checking a given proof takes time polynomial in its size, plus the signature checks, as above. This is why proof-carrying authorization moves the search for a proof to the requester, where the search may be hard, and leaves only the check to the server.
- **Practice.** The Taos operating system used the speaks-for calculus to authenticate requests across machines, channels and delegations (Lampson, Abadi, Burrows and Wobber 1992). The rules there are the same as above, with channels, timeouts and group membership added.

## References
