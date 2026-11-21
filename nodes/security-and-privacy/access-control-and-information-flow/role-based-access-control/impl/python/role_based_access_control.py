# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/role-based-access-control/. The authors are listed in prov/VWXVF2.jsonl.

"""Role-based access control with a role hierarchy and separation of duty.

The state follows the NIST model (Ferraiolo et al. 2001): users, roles,
permissions, the user assignment UA, the permission assignment PA, a role
hierarchy RH given by its immediate senior-to-junior edges, static and
dynamic separation of duty constraints, and sessions with active roles.

A senior role inherits every permission of its juniors. A user is
authorized for the roles assigned to it and all their juniors. A session
may activate only authorized roles. A static constraint (rs, n) says that
no user is authorized for n or more roles of rs; a dynamic constraint
(rs, n) says the same for the active roles of one session.
"""

from collections.abc import Hashable, Iterable

User = Hashable
Role = Hashable
Perm = Hashable
Session = Hashable


class RBAC:
    """One RBAC state.

    check_access takes O(a + e) time in the worst case, where a is the number
    of roles below the active roles and e the number of hierarchy edges among
    them; permission tests are hash lookups. The changes that can break a
    static constraint recompute the authorized roles of the users concerned.
    """

    def __init__(self) -> None:
        self._roles: set[Role] = set()
        self._ua: dict[User, set[Role]] = {}
        self._pa: dict[Role, set[Perm]] = {}
        self._juniors: dict[Role, set[Role]] = {}
        self._ssd: list[tuple[frozenset[Role], int]] = []
        self._dsd: list[tuple[frozenset[Role], int]] = []
        self._sessions: dict[Session, tuple[User, set[Role]]] = {}

    # Roles, assignments and the hierarchy.

    def add_role(self, role: Role) -> None:
        self._roles.add(role)
        self._pa.setdefault(role, set())
        self._juniors.setdefault(role, set())

    def below(self, roles: Iterable[Role]) -> set[Role]:
        """Return the given roles and every role junior to one of them."""
        seen: set[Role] = set()
        stack = list(roles)
        while stack:
            x = stack.pop()
            if x not in seen:
                seen.add(x)
                stack.extend(self._juniors.get(x, ()))
        return seen

    def authorized_roles(self, u: User) -> set[Role]:
        return self.below(self._ua.get(u, ()))

    def _ssd_ok(self, roles: set[Role]) -> bool:
        return all(len(roles & rs) < n for rs, n in self._ssd)

    def _dsd_ok(self, roles: set[Role]) -> bool:
        return all(len(roles & rs) < n for rs, n in self._dsd)

    def add_inheritance(self, senior: Role, junior: Role) -> bool:
        """Make senior inherit junior. Refuse a cycle or a broken static constraint."""
        if senior not in self._roles or junior not in self._roles:
            return False
        if senior in self.below([junior]):
            return False
        self._juniors[senior].add(junior)
        if all(self._ssd_ok(self.authorized_roles(u)) for u in self._ua):
            return True
        self._juniors[senior].discard(junior)
        return False

    def assign_user(self, u: User, role: Role) -> bool:
        """Add (u, role) to UA unless a static constraint forbids it."""
        if role not in self._roles:
            return False
        if not self._ssd_ok(self.below(self._ua.get(u, set()) | {role})):
            return False
        self._ua.setdefault(u, set()).add(role)
        return True

    def deassign_user(self, u: User, role: Role) -> None:
        """Remove (u, role) from UA and drop roles the user is no longer authorized for."""
        self._ua.get(u, set()).discard(role)
        allowed = self.authorized_roles(u)
        for owner, active in self._sessions.values():
            if owner == u:
                active &= allowed

    def grant_permission(self, p: Perm, role: Role) -> None:
        self._pa[role].add(p)

    def revoke_permission(self, p: Perm, role: Role) -> None:
        self._pa[role].discard(p)

    def add_ssd(self, roles: Iterable[Role], n: int) -> bool:
        """Add a static constraint unless some user already breaks it."""
        rs = frozenset(roles)
        if n < 2 or n > len(rs):
            return False
        if any(len(self.authorized_roles(u) & rs) >= n for u in self._ua):
            return False
        self._ssd.append((rs, n))
        return True

    def add_dsd(self, roles: Iterable[Role], n: int) -> bool:
        """Add a dynamic constraint unless some session already breaks it."""
        rs = frozenset(roles)
        if n < 2 or n > len(rs):
            return False
        if any(len(active & rs) >= n for _, active in self._sessions.values()):
            return False
        self._dsd.append((rs, n))
        return True

    # Sessions.

    def create_session(self, u: User, sid: Session) -> None:
        self._sessions[sid] = (u, set())

    def add_active_role(self, sid: Session, role: Role) -> bool:
        """Activate role in the session, if the user may and no dynamic constraint forbids it."""
        u, active = self._sessions[sid]
        if role not in self.authorized_roles(u):  # @line L9
            return False
        if not self._dsd_ok(active | {role}):  # @line L10
            return False
        active.add(role)  # @line L11
        return True

    def drop_active_role(self, sid: Session, role: Role) -> None:
        self._sessions[sid][1].discard(role)

    def active_roles(self, sid: Session) -> set[Role]:
        return set(self._sessions[sid][1])

    def check_access(self, sid: Session, p: Perm) -> bool:
        """Return True when an active role of the session, or a junior of one, has p."""
        seen: set[Role] = set()  # @line L1
        stack = list(self._sessions[sid][1])
        while stack:  # @line L2
            x = stack.pop()  # @line L3
            if x in seen:  # @line L4
                continue
            seen.add(x)  # @line L5
            if p in self._pa.get(x, ()):  # @line L6
                return True
            stack.extend(self._juniors.get(x, ()))  # @line L7
        return False  # @line L8

    # Views.

    def user_permissions(self, u: User) -> set[Perm]:
        """Return the flattened relation for u: the permissions of all authorized roles."""
        out: set[Perm] = set()
        for x in self.authorized_roles(u):
            out |= self._pa.get(x, set())
        return out

    def check_invariant(self) -> None:
        """Raise AssertionError unless the hierarchy is acyclic and every constraint holds."""
        for x in self._roles:
            for y in self._juniors[x]:
                assert x not in self.below([y]), "a cycle in the role hierarchy"
        for u in self._ua:
            assert self._ssd_ok(self.authorized_roles(u)), "a static constraint is broken"
        for u, active in self._sessions.values():
            assert active <= self.authorized_roles(u), "an active role the user may not have"
            assert self._dsd_ok(active), "a dynamic constraint is broken"
