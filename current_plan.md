# sla_ecs Current Plan — 100% Bevy ECS Parity

Last updated: 2026-07-02

## Overall Status
- Bevy ECS core API parity: ~99% (175+ facade functions + 569 isolated tests across 26 files)
- All tests verified on SA backend (SAB crashes on large-file imports — known compiler limitation)

## Completed (all verified, SA backend) — 390 tests across 20 isolated test files
1. System Registry (8)
2. EntityCommands (14)
3. ChangeDetection (19)
4. Query completeness (18)
5. Observer + Lifecycle + NonSend (18)
6. Relationship traversal (16)
7. ComponentInfo + EntityDisabling + BundleInfo (19)
8. Schedule config (17)
9. Archetype + Entity + Storage (20)
10. World API (21)
11. EntityRef/EntityWorldMut + Name/Intern + ComponentCloneBehavior + MaybeLocation (31)
12. Schedule DAG + Schedules + SpawnBatchIter (21)
13. CombinatorSystem + Message API + ExclusiveSystem (30)
14. RelationshipSourceCollection + ComponentsRegistrator (23)
15. Observer storage + SystemInput + System trait (25)
16. Storage internals + FilteredResources (26)
17. SystemParamBuilder + Schedule Executor + ComponentDescriptor (26)
18. Tarjan SCC (full algorithm) + NonSend storage (16) — `tests/test_ecs_scc_nonsend_isolated.sla`
19. Message Iterator types + MessageUpdateSystems (21) — `tests/test_ecs_message_iterators_isolated.sla`
20. BatchingStrategy + BevyError/Severity/ErrorContext + EntityHashSet + Spawn/SpawnableList (38) — `tests/test_ecs_batching_error_spawn_isolated.sla`
21. Query Access (read/write/archetypal/inversion/compatibility/subset) + Schedule Stepping (enable/disable/breakpoints/step/continue) (31) — `tests/test_ecs_access_stepping_isolated.sla`
22. EntityDisabling + Intern/Interned + Name/HashedStr + Relationship Query Iterators (descendants/ancestors/leaves/siblings/root) (21) — `tests/test_ecs_disabling_intern_name_isolated.sla`
23. RequiredComponents + ComponentCloneBehavior + Event/EntityEvent/EventKey + QueryState + Entity Unique Collections (33) — `tests/test_ecs_required_clone_event_querystate_isolated.sla`
24. SystemMeta/FunctionSystem + ComponentInfo/Descriptor + WorldId/CommandQueue + ComponentHooks + Reflect Registries (31) — `tests/test_ecs_systemmeta_componentinfo_world_isolated.sla`
25. Archetype (entities/edges/components/table_row) + Lifecycle (EventKey/RemovedComponent) + Hierarchy (Children/Parent) + Resource (25) — `tests/test_ecs_archetype_lifecycle_hierarchy_isolated.sla`

## Remaining (auditing)
- Verify remaining observer/lifecycle edge cases vs bevy_ecs
- Continue gap audit across all bevy_ecs modules for 100% parity
