---
tag: VWXVF2
kind: model
slug: role-based-access-control
name: Role-based access control
aliases:
- RBAC
- NIST RBAC model
area: security-and-privacy/access-control-and-information-flow
level: intro
summary: Assigns permissions to roles and roles to users, with role hierarchies and constraints, so that access follows job functions.
model: word-ram
prereqs: [access-control-matrix, directed-acyclic-graph]
see_also: [separation-of-duty, role-mining-problem, attribute-based-access-control, access-control-matrix, discretionary-access-control, mandatory-access-control, principle-of-least-privilege, transitive-closure]
sources:
  - paper: doi:10.1109/2.485845
    title: Ravi S. Sandhu, Edward J. Coyne, Hal L. Feinstein and Charles E. Youman, Role-based access control models, IEEE Computer 29(2), 1996
    locator: pages 38 to 47 (the family RBAC0 to RBAC3, role hierarchies, constraints and sessions)
  - paper: doi:10.1145/501978.501980
    title: David F. Ferraiolo, Ravi Sandhu, Serban Gavrila, D. Richard Kuhn and Ramaswamy Chandramouli, Proposed NIST standard for role-based access control, ACM Transactions on Information and System Security 4(3), 2001
    locator: pages 224 to 274 (core RBAC, hierarchical RBAC, static and dynamic separation of duty, and the functional specification)
  - paper: "American National Standards Institute, Information technology, role based access control, ANSI INCITS 359-2004, 2004"
    locator: the reference model with its four components and the functional specification
  - paper: doi:10.1145/354876.354878
    title: Sylvia Osborn, Ravi Sandhu and Qamar Munawer, Configuring role-based access control to enforce mandatory and discretionary access control policies, ACM Transactions on Information and System Security 3(2), 2000
    locator: pages 85 to 106 (RBAC configurations that enforce lattice-based mandatory policies and discretionary policies)
  - paper: doi:10.1145/1237500.1237501
    title: Ninghui Li, Mahesh V. Tripunitara and Ziad Bizri, On mutually exclusive roles and separation-of-duty, ACM Transactions on Information and System Security 10(2), 2007
    locator: the complexity of checking separation of duty policies and constraints on mutually exclusive roles
  - paper: doi:10.1145/1187441.1187442
    title: Ninghui Li and Mahesh V. Tripunitara, Security analysis in role-based access control, ACM Transactions on Information and System Security 9(4), 2006
    locator: pages 391 to 420 (security analysis questions about reachable RBAC states under administrative changes)
  - paper: "Matt Bishop, Computer Security: Art and Science, second edition, Addison-Wesley, 2018, ISBN 9780321712332"
    locator: Chapter 8, Section 8.4 (role-based access control)
---

Role-based access control (RBAC) puts a layer of roles between users and permissions: an administrator assigns permissions to roles, such as "teller" or "auditor", and assigns users to roles, and a user gets the permissions of its roles. A senior role in a hierarchy inherits the permissions of its juniors, and constraints such as [separation of duty](/separation-of-duty/) forbid some combinations of roles. Sandhu, Coyne, Feinstein and Youman (1996) gave the family of models RBAC0 to RBAC3, and Ferraiolo and others (2001) gave the NIST model, which became the standard ANSI INCITS 359-2004. Composing the user assignment, the hierarchy and the permission assignment gives an [access control matrix](/access-control-matrix/) of users and permissions. RBAC stores that matrix in a factored form that follows the structure of an organization: a new employee needs one role, not a hundred cells.

## The machine

**State.** An RBAC state has:

- sets $U$ of users, $\mathit{Roles}$ of roles, and $P$ of permissions, where a permission is a pair of an operation and an object, for example (write, account);
- the user assignment $UA \subseteq U \times \mathit{Roles}$ and the permission assignment $PA \subseteq P \times \mathit{Roles}$;
- a role hierarchy $RH \subseteq \mathit{Roles} \times \mathit{Roles}$, a partial order written $x \ge y$ ("$x$ is senior to $y$"), stored by its immediate edges as a [directed acyclic graph](/directed-acyclic-graph/);
- constraints: static separation of duty pairs $(rs, n)$ with $rs \subseteq \mathit{Roles}$ and $2 \le n \le |rs|$, and dynamic pairs of the same form;
- sessions: each session belongs to one user and has a set of active roles.

A user $u$ is *authorized* for role $y$ when $(u, x) \in UA$ for some $x \ge y$. A session may activate only roles its user is authorized for. A static pair $(rs, n)$ holds when no user is authorized for $n$ or more roles of $rs$; a dynamic pair holds when no session has $n$ or more roles of $rs$ active.

**The family.** RBAC0 has users, roles, permissions, $UA$, $PA$ and sessions. RBAC1 adds the hierarchy, RBAC2 adds constraints, and RBAC3 has both. The NIST model has the same parts under the names core RBAC, hierarchical RBAC, static separation of duty (SSD) and dynamic separation of duty (DSD).

**Decision.** A request of a session for permission $p$ is allowed when some active role, or a role junior to an active role, has $p$:

```pseudo id=main
CHECK-ACCESS(sess, p)
L1  seen ← ∅; stack ← the active roles of sess
L2  while stack is not empty do
L3      x ← pop stack
L4      if x ∈ seen then continue
L5      add x to seen
L6      if (p, x) ∈ PA then return true
L7      push the juniors of x
L8  return false

ADD-ACTIVE-ROLE(sess, x)
L9  if the user of sess is not authorized for x then return false
L10 if (the active roles of sess) ∪ {x} breaks a dynamic pair then return false
L11 add x to the active roles of sess; return true
```

Lines L1 to L8 are a search of the hierarchy below the active roles, as in [graph reachability](/graph-reachability/). Lines L9 to L11 are the only way to add an active role, so every session keeps its dynamic constraints.

**Transitions.** Administrative operations add and remove users, roles, permissions, edges of $RH$ and pairs of $UA$ and $PA$. An operation that would break a static pair is refused: adding $(u, x)$ to $UA$, and also adding an edge to $RH$, because a new edge can make a user authorized for more roles. Who may run these operations is a policy of its own; in the basic model only a security administrator may.

**Example.** A bank has the roles employee, teller, auditor, manager and customer, with teller ≥ employee, auditor ≥ employee and manager ≥ teller. The permissions are (read, handbook) for employee, (write, account) for teller, (read, log) for auditor, (approve, loan) for manager and (read, statement) for customer. There is a static pair ({teller, auditor}, 2), so nobody both handles accounts and audits them, and a dynamic pair ({teller, customer}, 2), so a teller who is also a customer of the bank does not act as both at once. Alice is a manager, bob is a teller and a customer, and carol is an auditor. The flattened relation is:

| user | authorized roles | permissions |
|---|---|---|
| alice | manager, teller, employee | (approve, loan), (write, account), (read, handbook) |
| bob | teller, customer, employee | (write, account), (read, statement), (read, handbook) |
| carol | auditor, employee | (read, log), (read, handbook) |

Assigning carol to teller is refused by the static pair. So is assigning alice to auditor, because alice is already authorized for teller through manager; and so is the edge auditor ≥ teller, because it would make carol a teller. In a session, bob can activate teller, but then not customer. Alice can open a session with only employee active; then CHECK-ACCESS for (approve, loan) is false until she activates manager. Activating only the roles a task needs is the [principle of least privilege](/principle-of-least-privilege/) inside the model.

## What it counts

**The access decision.** The search of lines L1 to L8 visits each role below the active roles at most once, so it takes $O(a + e)$ time, where $a$ is the number of those roles and $e$ the number of hierarchy edges among them, with $PA$ in a hash table. A system can instead store the [transitive closure](/transitive-closure/) of $RH$, or the flattened relation itself, and answer in $O(1)$ expected time, at the price of recomputing it after each administrative change.

**The flattened relation.** The users' permissions are the relation $UA \circ RH^* \circ PA$, where $RH^*$ is the reflexive and transitive closure of the hierarchy: $u$ has $p$ when there are roles $x \ge y$ with $(u, x) \in UA$ and $(p, y) \in PA$. This is the access matrix with users as rows and permissions as columns. Its size can be $|U| \cdot |P|$, while the factored form has size $|UA| + |PA| + |RH|$; the gain of RBAC is this difference.

**Administration and analysis.** The cost of checking constraints and of asking what a sequence of administrative changes can reach is the subject of the known results below.

## Relation to other models

- **Access matrix.** RBAC is a factored matrix. Each role is a set of permissions, and each user's row is the union of the sets of its roles. [Role mining](/role-mining-problem/) goes the other way: it looks for a small set of roles that factors a given user to permission matrix.
- **DAC and MAC.** In RBAC an administrator, not the owner, decides, so it is not [discretionary](/discretionary-access-control/). Osborn, Sandhu and Munawer (2000) showed that RBAC can be configured to enforce lattice-based [mandatory](/mandatory-access-control/) policies and discretionary policies, so RBAC is at least as expressive as both in this sense.
- **Separation of duty.** The static and dynamic pairs are the RBAC form of [separation of duty](/separation-of-duty/). That page also covers forms that RBAC pairs cannot state, such as constraints on the steps of one transaction.
- **ABAC.** [Attribute-based access control](/attribute-based-access-control/) treats the role as one attribute of a user among many, and adds attributes of objects and of the environment. RBAC is the case where the rules test only the user's roles.

## Known results in the model

- **Decision.** CHECK-ACCESS is reachability in the hierarchy below the active roles, $O(a + e)$ time, or $O(1)$ expected with a stored closure.
- **Flattening is exact.** A session with every authorized role active has exactly the permissions of the flattened relation $UA \circ RH^* \circ PA$. The Python code on this page checks this on 600 random states with up to 4 users, 5 roles and 12 permissions over 4 objects and 3 rights, against a closure computed by Warshall's method; it also checks that every refused assignment, edge and constraint is one that the brute force oracle refuses.
- **Separation of duty.** Li, Tripunitara and Bizri (2007) showed that checking whether an RBAC state satisfies a static separation of duty policy, stated over the permissions a task needs, is coNP-complete. Checking a state against constraints on mutually exclusive roles, as in the static pairs above, is efficient, but deciding whether a set of such constraints is enough to enforce a given policy is again coNP-complete. See [separation of duty](/separation-of-duty/) and [co-NP](/co-np/).
- **Security analysis.** Li and Tripunitara (2006) studied questions such as "can user $u$ ever get permission $p$?" under administrative changes, and found that the answer depends on which changes the model allows; for some forms the questions are efficiently decidable and for others they are hard.
- **Expressiveness.** RBAC can simulate lattice-based MAC and DAC (Osborn, Sandhu and Munawer 2000).

## References
