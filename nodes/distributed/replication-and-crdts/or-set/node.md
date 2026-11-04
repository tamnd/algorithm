---
tag: DDH0TH
kind: data-structure
slug: or-set
name: OR-Set
aliases:
- observed-remove set
- add-wins set
area: distributed/replication-and-crdts
level: core
summary: Set CRDT where each add is tagged uniquely, so a remove cancels only the adds it observed and concurrent adds win.
---

Set CRDT where each add is tagged uniquely, so a remove cancels only the adds it observed and concurrent adds win.
