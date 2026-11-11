# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/yata/. The authors are listed in prov/Y6F20Y.jsonl.

"""YATA (Nicolaescu, Jahns, Derntl and Klamma 2016), the sequence CRDT of Yjs.

Each item has an id (client, clock), the id of the item to its left when it
was made (origin) and the id of the item to its right (right origin). A remote
item is placed between its two origins. When other items sit in that gap, the
loop below decides, item by item, whether the new item goes after them. It
follows the integrate function of the Yjs Item class: items with the same
origin are ordered by client id, and an item whose origin lies inside the
scanned run goes with that run. Deleted items stay as tombstones.
Items must arrive after their origins (Yjs holds back the others).
"""

from typing import Any, NamedTuple

Id = tuple[int, int]  # (client, clock)


class Item(NamedTuple):
    id: Id
    origin: Id | None
    right: Id | None  # the right origin
    value: Any


class Yata:
    """One YATA replica for client id client."""

    def __init__(self, client: int) -> None:
        self.client = client
        self.clock = 0
        self.items: list[Item] = []
        self.dead: set[Id] = set()
        self.ids: set[Id] = set()

    def _pos(self, i: Id | None, default: int) -> int:
        if i is None:
            return default
        for k, it in enumerate(self.items):
            if it.id == i:
                return k
        raise KeyError(i)

    def integrate(self, item: Item) -> None:
        if item.id in self.ids:
            return
        left = self._pos(item.origin, -1)  # @line L1
        right = self._pos(item.right, len(self.items))  # @line L2
        before_origin: set[Id] = set()
        conflicting: set[Id] = set()
        k = left + 1
        while k < right:  # @line L3
            o = self.items[k]
            before_origin.add(o.id)
            conflicting.add(o.id)
            if o.origin == item.origin:  # @line L4
                if o.id[0] < item.id[0]:  # @line L5
                    left = k
                    conflicting.clear()
                elif o.right == item.right:  # @line L6
                    break
            elif o.origin is not None and o.origin in before_origin:  # @line L7
                if o.origin not in conflicting:  # @line L8
                    left = k
                    conflicting.clear()
            else:
                break  # @line L9
            k += 1
        self.items.insert(left + 1, item)  # @line L10
        self.ids.add(item.id)

    def _visible(self) -> list[Item]:
        return [x for x in self.items if x.id not in self.dead]

    def local_insert(self, i: int, value: Any) -> Item:
        vis = self._visible()
        origin = vis[i - 1].id if i > 0 else None
        p = self._pos(origin, -1) + 1
        right = self.items[p].id if p < len(self.items) else None  # the next item, live or not
        self.clock += 1
        item = Item((self.client, self.clock), origin, right, value)
        self.integrate(item)
        return item

    def local_delete(self, i: int) -> tuple[str, Id]:
        op = ("del", self._visible()[i].id)
        self.dead.add(op[1])
        return op

    def apply(self, op: "Item | tuple[str, Id]") -> None:
        if isinstance(op, Item):
            self.integrate(op)
        else:
            self.dead.add(op[1])

    def value(self) -> list[Any]:
        return [x.value for x in self._visible()]

    def order(self) -> list[Id]:
        return [x.id for x in self.items]

    def check_invariant(self) -> None:
        pos = {x.id: k for k, x in enumerate(self.items)}
        assert len(pos) == len(self.items)
        for k, x in enumerate(self.items):
            if x.origin is not None:
                assert pos[x.origin] < k, "an item sits right of its origin"
            if x.right is not None:
                assert pos[x.right] > k, "an item sits left of its right origin"
