---
tag: C4CFV8
kind: concept
slug: separation-of-duty
name: Separation of duty
aliases:
- segregation of duties
area: security-and-privacy/access-control-and-information-flow
level: core
summary: The rule that a critical task needs more than one person, so that no single user can complete it alone; RBAC states it on role assignment or per session.
prereqs: [role-based-access-control]
see_also: [clark-wilson-model, role-based-access-control, principle-of-least-privilege, chinese-wall-model, co-np, set-cover, mandatory-access-control]
sources:
  - paper: "David D. Clark and David R. Wilson, A comparison of commercial and military computer security policies, IEEE Symposium on Security and Privacy, 1987"
    locator: well-formed transactions and separation of duty as the two mechanisms of commercial integrity
  - paper: doi:10.1109/CSFW.1997.596811
    title: Richard T. Simon and Mary Ellen Zurko, Separation of duty in role-based environments, IEEE Computer Security Foundations Workshop, 1997
    locator: pages 183 to 194 (a list of the forms of separation of duty, static and dynamic, and those based on objects, operations and history)
  - paper: doi:10.1145/501978.501980
    title: David F. Ferraiolo, Ravi Sandhu, Serban Gavrila, D. Richard Kuhn and Ramaswamy Chandramouli, Proposed NIST standard for role-based access control, ACM Transactions on Information and System Security 4(3), 2001
    locator: pages 224 to 274 (static separation of duty relations, with and without a hierarchy, and dynamic separation of duty relations)
  - paper: doi:10.1145/1237500.1237501
    title: Ninghui Li, Mahesh V. Tripunitara and Ziad Bizri, On mutually exclusive roles and separation-of-duty, ACM Transactions on Information and System Security 10(2), 2007
    locator: separation of duty policies over permissions, constraints on mutually exclusive roles, and the coNP-completeness of checking them
  - paper: doi:10.1109/PROC.1975.9939
    title: Jerome H. Saltzer and Michael D. Schroeder, The protection of information in computer systems, Proceedings of the IEEE 63(9), 1975
    locator: pages 1278 to 1308, Section I (the design principle of separation of privilege)
  - paper: doi:10.1109/2.485845
    title: Ravi S. Sandhu, Edward J. Coyne, Hal L. Feinstein and Charles E. Youman, Role-based access control models, IEEE Computer 29(2), 1996
    locator: pages 38 to 47 (constraints in RBAC2, mutually exclusive roles)
---

Separation of duty (SoD) is the rule that a critical task must need more than one person, so that no single user can do it alone. A clerk who records a payment should not also approve it, and the person who writes a program should not alone move it into production. Fraud then needs two people who agree, and an honest mistake by one person can be caught by the other. Clark and Wilson (1987) made it, with well-formed transactions, one of the two main mechanisms of commercial integrity; it is related to the principle of separation of privilege of Saltzer and Schroeder (1975). In [role-based access control](/role-based-access-control/) it is stated as constraints on roles: statically, on the assignment of users to roles, or dynamically, on the roles active in one session. SoD is broader than these constraints. It can also be about the steps of one transaction or the history of one object, as in the [Clark-Wilson model](/clark-wilson-model/), which this page links to but does not repeat.

## In plain words

Split an important job into steps and give the steps to different people. The person who orders goods should not be the person who approves the order, and neither should be the person who pays the bill. Then nobody can buy something for themselves with the company's money without the help of someone else.

There are two ways to set this up. The strict way never gives one person both jobs. The softer way lets one person hold both jobs, but not use both on the same order, or not in the same working session. The soft way needs fewer staff, but the system must remember who did which step.

## The idea

**Static separation in RBAC.** A static constraint is a pair $(rs, n)$ of a set of roles $rs$ and a number $2 \le n \le |rs|$: no user may be authorized for $n$ or more roles of $rs$. With $n = 2$ the roles of $rs$ are mutually exclusive. The NIST model calls this SSD and checks it on each assignment, and also on each new edge of the role hierarchy, because a senior role makes its user authorized for the juniors.

**Dynamic separation in RBAC.** A dynamic constraint $(rs, n)$ says that no session may have $n$ or more roles of $rs$ active. A user may hold both teller and customer at a bank, but not use both at once. The NIST model calls this DSD.

**Separation over objects and history.** Simon and Zurko (1997) listed further forms. Object-based separation lets a user hold conflicting roles but not act in both on the same object: the person who placed this order cannot approve this order. Operational separation forbids one user from holding all the roles needed for every step of a business task. History-based separation remembers who did which step of each instance of a task. These forms need state beyond the RBAC assignment, and the [Clark-Wilson model](/clark-wilson-model/) states them for its transformation procedures. The [Chinese Wall model](/chinese-wall-model/) is another history-based rule, about conflicts of interest instead of fraud.

**Policies and constraints are different.** Li, Tripunitara and Bizri (2007) separated what an organization wants from how RBAC states it. A policy over permissions says: a set $P$ of permissions, all needed for a task, must not be held by fewer than $k$ users together. A constraint on mutually exclusive roles is a means to that end. Two questions then arise:

- **Does a state satisfy a policy?** The state breaks the policy exactly when some $k - 1$ users together hold every permission of $P$. That is a covering question like [set cover](/set-cover/): choose $k - 1$ users whose permission sets cover $P$. Li, Tripunitara and Bizri showed that checking that no such choice exists is coNP-complete, in the class [co-NP](/co-np/).
- **Do the constraints enforce the policy?** Checking one state against constraints on mutually exclusive roles is efficient: count the roles of each user in each constrained set. But deciding whether a set of such constraints makes every state satisfy a given policy is again coNP-complete.

## Examples

- **Purchasing.** Let $P$ = {create order, approve order, pay invoice} and $k = 2$: no single user may hold all three. Alice holds create and approve, bob holds approve and pay, carol holds pay. No single user holds all of $P$, so the policy holds. With $k = 3$, the policy needs at least three people, and it is broken, because alice and bob together cover $P$.
- **A bank with roles.** In the example of the [RBAC](/role-based-access-control/) page, the static pair ({teller, auditor}, 2) stops carol, an auditor, from becoming a teller, and stops the edge auditor ≥ teller from being added. The dynamic pair ({teller, customer}, 2) lets bob hold both roles but not activate them in one session.
- **The two-person rule.** Some actions, such as opening a vault or launching a weapon, need two people to act at the same time, each with a separate key or code. This is separation of duty in its plainest form.
- **Software releases.** A change to production needs a review by someone other than its author. The version control and deployment systems record the author and the reviewer of each change: a history-based form.

## Where it is used

Separation of duty is a standard internal control in accounting and auditing, and laws and audit rules for public companies ask for it in financial processes. Access control products state it as mutually exclusive roles in RBAC, and identity management tools check the assignments of a whole organization for conflicts, which is the check of a state against constraints described above. Workflow systems apply its object-based and history-based forms, by recording who did each step of each case. In system design it joins the [principle of least privilege](/principle-of-least-privilege/): least privilege makes each person's rights small, and separation of duty makes sure that even all the rights of one person are not enough for a critical task.

## References
