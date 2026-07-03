# sla_ecs Current Plan — Bevy ECS Parity (per-dimension)

Last updated: 2026-07-03

## Overall Status
- Per-dimension completion (see README.md "Bevy ECS Parity Assessment"): API surface parity ~93–96%, behavioral parity ~82–87%. Not 100%: a general dynamic multithreaded executor and full runtime reflection remain incomplete (see README ⚠️ / ❌).
- Counts (measured 2026-07-03): 232 lib `.sla` modules; 158 `tests/*.sla` files; 90 `examples/*.sla`; 7,011 `@test` annotations total across lib/tests/examples. (Earlier statements of "1795/92/170" and "1415/76" were stale and understated.)
- Tests verified on the SA backend (SAB hits a codegen limitation on large-file imports — known compiler limitation; SA is the verified fallback).
- Every bevy_ecs module has isolated parity tests covering its public API surface, except the two genuinely incomplete areas noted above.

## Completed (verified on SA backend) — see README "Bevy ECS Parity Assessment"; counts measured 2026-07-03: 198 lib / 121 tests / 7,011 @test total. Sub-list below is historical per-area summary
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
18. Tarjan SCC (full algorithm) + NonSend storage (16)
19. Message Iterator types + MessageUpdateSystems (21)
20. BatchingStrategy + BevyError/Severity/ErrorContext + EntityHashSet + Spawn/SpawnableList (38)
21. Query Access (read/write/archetypal/inversion/compatibility/subset) + Schedule Stepping (31)
22. EntityDisabling + Intern/Interned + Name/HashedStr + Relationship Query Iterators (21)
23. RequiredComponents + ComponentCloneBehavior + Event/EntityEvent/EventKey + QueryState + Entity Unique Collections (33)
24. SystemMeta/FunctionSystem + ComponentInfo/Descriptor + WorldId/CommandQueue + ComponentHooks + Reflect Registries (31)
25. Archetype (entities/edges/components/table_row) + Lifecycle (EventKey/RemovedComponent) + Hierarchy (Children/Parent) + Resource (25)
26. Clone isolated (1 — limited by SA compiler file-size on large imports, logic verified)

## bevy_ecs Module Coverage Audit
- src/archetype.rs ✓ (Archetype, Edges, ArchetypeId, ArchetypeRow)
- src/batching.rs ✓ (BatchingStrategy)
- src/bundle/ ✓ (BundleInfo)
- src/change_detection/ ✓ (DetectChanges, Tick, MaybeLocation, ComponentTickCells, ContiguousComponentTicksRef/Mut)
- src/component/ ✓ (ComponentInfo, ComponentDescriptor, ComponentHooks, RequiredComponents, ComponentCloneBehavior, register, constants)
- src/entity/ ✓ (Entity, EntityHashSet, UniqueVec, EntityMapper, hash)
- src/entity_disabling.rs ✓ (DefaultQueryFilters, Disabled)
- src/error/ ✓ (BevyError, Severity, ErrorContext, CommandOutput, FallbackErrorHandler)
- src/event/ ✓ (Event, EntityEvent, EventKey, trigger)
- src/hierarchy.rs ✓ (Children, Parent)
- src/intern.rs ✓ (Interner, Interned)
- src/label.rs ✓ (SystemSet, ScheduleLabel)
- src/lifecycle.rs ✓ (Add/Insert/Discard/Remove/Despawn, EventKey, RemovedComponent)
- src/message/ ✓ (Messages, MessageReader/Writer/Cursor/Mutator, iterators, update systems)
- src/name.rs ✓ (Name, HashedStr)
- src/observer/ ✓ (ObserverDescriptor, centralized/distributed storage, condition, runner)
- src/query/ ✓ (Access, QueryState, QueryBuilder, fetch, filter, iter, par_iter, world_query)
- src/reflect/ ✓ (AppTypeRegistry, AppFunctionRegistry)
- src/relationship/ ✓ (Relationship, RelationshipTarget, source collection, query iterators, related methods)
- src/resource.rs ✓ (Resource, IS_RESOURCE)
- src/schedule/ ✓ (Schedule, ScheduleConfig, SystemSet, DAG, graph, executor, stepping, node, set, condition, pass)
- src/spawn.rs ✓ (Spawn, SpawnableList, RelatedSpawner)
- src/traversal.rs ✓ (Traversal trait, unit/relationship impls, PropagateDirection)
- src/world/identifier.rs ✓ (WorldId, WorldIdAllocator)
- src/world/deferred_world.rs ✓ (DeferredWorld)
- src/entity/map_entities.rs ✓ (MapEntities, SceneEntityMapper, EntityHashMap)
- src/entity/clone_entities.rs ✓ (EntityCloner + EntityClonerBuilder OptIn/OptOut)
- src/system/adapter_system.rs ✓ (Adapt, AdapterSystem, Not/Map/Chain adapters)
- src/system/system_name.rs ✓ (SystemName, DebugName)
- src/system/exclusive_function_system.rs ✓ (ExclusiveFunctionSystem)
- src/world/entity_fetch.rs ✓ (EntityFetcher, WorldEntityFetch)
- src/world/filtered_resource.rs ✓ (FilteredResources, FilteredResourcesMut)
- src/observer/system_param.rs ✓ (On<E> trigger context, TriggerContext)
- src/query/access_iter.rs ✓ (EcsAccessType, AccessConflictError, has_conflicts)
- src/query/builder.rs ✓ (QueryBuilder data/with/without/or/optional/transmute/build)
- src/query/fetch.rs ✓ (SpawnDetails, Entity/Read/Ref/Write/Option/Has fetches, AnyOf, NestedQuery)
- src/system/builder.rs ✓ (ParamBuilder, BuilderSystem, ParamSetBuilder, DynParamBuilder)
- src/storage/blob_array.rs ✓ (BlobArray)
- src/storage/thin_array_ptr.rs ✓ (ThinArrayPtr)
- src/storage/table/column.rs ✓ (Column)
- src/schedule/config.rs ✓ (ScheduleConfig, ScheduleConfigs, GraphInfo)
- src/schedule/set.rs ✓ (SystemSet, AnonymousSet, SystemTypeSet)
- src/system/input.rs ✓ (SystemInput, In/InRef/InMut, StaticSystemInput)
- src/world/command_queue.rs ✓ (CommandQueue)
- src/observer/centralized_storage.rs ✓ (Observers catalog, CachedObservers)
- src/observer/distributed_storage.rs ✓ (Observer node, ObserverDescriptor)
- src/system/commands/entity_command.rs ✓ (EntityCommand, EntityCommandError)
- src/schedule/executor/ ✓ (SingleThreadedExecutor, MultiThreadedExecutor)
- src/system/exclusive_system_param.rs ✓ (ExclusiveSystemParam)
- src/schedule/graph/graph_map.rs ✓ (Graph directed/undirected)
- src/reflect/resource.rs ✓ (ReflectResource)
- src/schedule/schedule.rs ✓ (Schedules collection)
- src/schedule/pass.rs ✓ (ScheduleBuildPass, FlattenedDependencies, toposort)
- src/system/system.rs ✓ (System, SystemStateFlags, RunSystemOnce)
- src/storage/sparse_set.rs ✓ (SparseSet, ComponentSparseSet)
- src/bundle/writer.rs ✓ (BundleScratch, BundleWriter)
- src/reflect/component.rs ✓ (ReflectComponent)
- src/reflect/bundle.rs ✓ (ReflectBundle)
- src/reflect/event.rs ✓ (ReflectEvent)
- src/reflect/message.rs ✓ (ReflectMessage)
- src/reflect/from_world.rs ✓ (FromWorld)
- src/reflect/map_entities.rs ✓ (ReflectMapEntities)
- src/reflect/entity_commands.rs ✓ (ReflectEntityCommands)
- src/world/reflect.rs ✓ (ReflectWorld)
- src/query/state.rs ✓ (QueryState)
- src/query/world_query.rs ✓ (WorldQuery)
- src/query/par_iter.rs ✓ (QueryParIter)
- src/system/function_system.rs ✓ (SystemMeta, FunctionSystem)
- src/system/schedule_system.rs ✓ (WithInputWrapper)
- src/system/observer_system.rs ✓ (ObserverSystem)
- src/system/commands/command.rs ✓ (Command)
- src/world/entity_access/except.rs ✓ (Except)
- src/relationship/related_methods.rs ✓ (RelatedMethods)
- src/error/command_handling.rs ✓ (CommandOutput, ErrorHandler)
- src/error/handler.rs ✓ (FallbackErrorHandler)
- src/component/register.rs ✓ (ComponentIds, ComponentsRegistrator)
- src/message/update.rs ✓ (MessageUpdateSystems)
- src/world/spawn_batch.rs ✓ (SpawnBatchIter)
- src/world/entity_access/component_fetch.rs ✓ (EntityComponentFetch)
- src/bundle/remove.rs ✓ (BundleRemover)
- src/intern.rs ✓ (Interner, Interned)
- src/name.rs ✓ (Name, HashedStr, NameOrEntity)
- src/lifecycle.rs ✓ (ComponentHooks, HookContext, RemovedComponent)
- src/entity_disabling.rs ✓ (Disabled, DefaultQueryFilters)
- src/event/trigger.rs ✓ (GlobalTrigger, EntityTrigger, PropagateEntityTrigger)
- src/relationship/relationship_query.rs ✓ (RelationshipQuery, AncestorWalker)
- src/relationship/relationship_source_collection.rs ✓ (RelationshipSourceCollection, RelationshipHookMode)
- src/relationship/mod.rs ✓ (RelationshipCloneBehavior)
- src/component/info.rs ✓ (ComponentInfo, ComponentId, ComponentDescriptor)
- src/component/constants.rs ✓ (ADD/INSERT/DISCARD/REMOVE/DESPAWN/IS_RESOURCE)
- src/component/required.rs ✓ (RequiredComponents, RequiredComponentsRegistrator)
- src/system/combinator.rs ✓ (CombinatorSystem, PipeSystem, Combine)
- src/system/system_registry.rs ✓ (SystemId, RegisteredSystem, SystemHandle)
- src/message/message_cursor.rs ✓ (MessageCursor)
- src/message/message_mutator.rs ✓ (MessageMutator)
- src/message/message_registry.rs ✓ (MessageRegistry, ShouldUpdateMessages)
- src/message/mut_iterators.rs ✓ (MessageMutIterator, MessageMutParIter)
- src/message/message_reader.rs ✓ (MessageReader, PopulatedMessageReader)
- src/message/message_writer.rs ✓ (MessageWriter)
- src/message/messages.rs ✓ (Messages buffer)
- src/message/iterators.rs ✓ (MessageIterator, MessageParIter)
- src/storage/ ✓ (Table, Column, BlobArray, ThinArrayPtr, SparseSet, NonSend)
- src/system/ ✓ (System, SystemMeta, FunctionSystem, SystemState, combinator, adapter, builder, input, system_name, system_registry, commands, query, observer_system)
- src/world/ ✓ (World, WorldId, CommandQueue, DeferredWorld, EntityRef, EntityWorldMut, filtered_resource, spawn_batch, entity_fetch, identifier)
- src/traversal.rs ✓ (Traversal trait)
- src/template.rs ✓ (Template, TemplateContext, SceneEntityReferences, EntityTemplate, FnTemplate, OptionTemplate, VecTemplate)

## Remaining (minor)
- Full SAB backend verification once compiler large-file limit is resolved
- Continue refining edge cases as bevy_ecs evolves
- src/never.rs: Never type alias (language-level, no semantic API to test)

## Batch 27 — entity_mut (2026-07-02)
- lib/entity_mut.sla: EcsEntityMut (id/location/archetype/contains/get/get_ref/get_mut/insert/remove/components/reborrow/into_readonly/as_readonly/get_change_ticks_by_id) + EcsFilteredEntityMut (allow/is_allowed/get/id/from_inner/inner/into_filtered)
- 19 tests — test_ecs_lib_entity_mut_isolated.sla
- Tests: 1415 → 1434, lib modules: 154 → 155, test files: 76 → 77
- src/world/entity_access/entity_mut.rs ✓

## Batch 28 — entry (2026-07-02)
- lib/entry.sla: EcsComponentEntry (occupied/vacant/and_modify/insert_entry/or_insert/or_insert_with/or_default/from_state) + EcsOccupiedEntry (get/insert/take/get_mut/into_mut) + EcsVacantEntry (insert) — mirrors world::entity_access::entry.rs
- 21 tests — test_ecs_lib_entry_isolated.sla
- Tests: 1434 → 1455, lib modules: 155 → 156, test files: 77 → 78
- src/world/entity_access/entry.rs ✓

## Batch 29 — filtered_entity (2026-07-02)
- lib/filtered_entity.sla: EcsAccess (add_read/add_write/set_read_all/set_write_all/has_read/has_write/has_read_all/has_write_all/clone) + EcsTryFromFilteredError + EcsEntityComponents + EcsFilteredEntityRef (id/location/archetype/access/contains/contains_id/contains_type_id/get/get_ref/get_by_id/get_change_ticks_by_id/try_into_all/eq/cmp) + EcsFilteredEntityMut2 (get/get_mut/get_mut_by_id/get_change_ticks_by_id/reborrow/into_readonly/as_readonly/try_into_all/eq/cmp) + EcsUnsafeFilteredEntityMut (new_readonly/into_mut) — mirrors world::entity_access::filtered.rs
- 30 tests — test_ecs_lib_filtered_entity_isolated.sla
- Tests: 1455 → 1485, lib modules: 156 → 157, test files: 78 → 79
- src/world/entity_access/filtered.rs ✓

## Batch 29 — filtered_entity (2026-07-02)
- lib/filtered_entity.sla: EcsAccess (add_read/add_write/set_read_all/set_write_all/has_read/has_write/has_read_all/has_write_all/clone) + EcsTryFromFilteredError + EcsEntityComponents + EcsFilteredEntityRef (id/location/archetype/access/contains/get/get_ref/get_by_id/get_change_ticks_by_id/try_into_all/eq/cmp) + EcsFilteredEntityMut2 (get/get_mut/get_mut_by_id/reborrow/into_readonly/as_readonly/try_into_all/eq/cmp) + EcsUnsafeFilteredEntityMut — mirrors world::entity_access::filtered.rs
- 30 tests — test_ecs_lib_filtered_entity_isolated.sla
- Tests: 1455 → 1485, lib modules: 156 → 157, test files: 78 → 79
- src/world/entity_access/filtered.rs ✓

## Batch 30 — world_mut (2026-07-02)
- lib/world_mut.sla: EcsEntityWorldMut2 (id/is_spawned/is_despawned/location/try_location/archetype/try_archetype/spawned_by/spawn_tick/contains/get/get_ref/get_mut/get_by_id/get_mut_by_id/into_borrow/get_change_ticks_by_id/insert/insert_if_new/remove/remove_by_id/remove_with_requires/retain/take/clear/despawn/despawn_no_free/flush/components/clone_and_spawn/clone_components/move_components/into_readonly/as_readonly/into_mutable/as_mutable/entry/insert_resource/get_resource/resource/resource_mut/resource_count/modify_component/update_location) — mirrors world::entity_access::world_mut.rs
- 43 tests — test_ecs_lib_world_mut_isolated.sla
- Tests: 1485 → 1528, lib modules: 157 → 158, test files: 79 → 80
- src/world/entity_access/world_mut.rs ✓
- entity_access/ subdirectory now fully deep-covered (entity_ref/entity_mut/filtered/entry/world_mut/except/component_fetch)

## Batch 31 — entity_commands_conditional (2026-07-02)
- lib/entity_commands_conditional.sla: EcsEntityCommands2 (insert/insert_if/insert_if_new/insert_if_new_and/insert_if_neq/try_insert/try_insert_if/try_insert_if_new/try_insert_if_new_and/remove/remove_if/remove_with_requires/remove_by_id/try_remove/try_remove_if/retain/clear/despawn/try_despawn/entry/queue/reborrow/command_log) — mirrors system::commands::EntityCommands conditional API
- 37 tests — test_ecs_lib_entity_commands_conditional_isolated.sla
- Tests: 1528 → 1565, lib modules: 158 → 159, test files: 80 → 81
- src/system/commands/mod.rs (EntityCommands conditional ops) ✓

## Batch 32 — entity_entry_commands (2026-07-02)
- lib/entity_entry_commands.sla: EcsEntityEntryCommands (and_modify/reborrow/or_insert/or_try_insert/or_insert_with/or_try_insert_with/or_default/or_from_world/commands/resolve/pending_value/ops_log) — mirrors system::commands::EntityEntryCommands
- 24 tests — test_ecs_lib_entity_entry_commands_isolated.sla
- Tests: 1565 → 1589, lib modules: 159 → 160, test files: 81 → 82
- src/system/commands/mod.rs (EntityEntryCommands) ✓

## Batch 33 — commands_world (2026-07-02)
- lib/commands_world.sla: EcsCommands (spawn_empty/spawn/spawn_batch/entity/get_entity/insert_entity/insert_batch/insert_batch_if_new/get_component/has_component/insert_resource/init_resource/insert_resource_if_neq/remove_resource/get_resource/register_system/unregister_system/run_system/run_schedule/queue/queue_handled/queue_silenced/append/write_message) — mirrors system::commands::Commands
- 32 tests — test_ecs_lib_commands_world_isolated.sla
- Tests: 1589 → 1621, lib modules: 160 → 161, test files: 82 → 83
- src/system/commands/mod.rs (Commands world-level API) ✓

## Batch 34 — world_resource_api (2026-07-02)
- lib/world_resource_api.sla: EcsWorldResource (insert/init/get_or_insert_with/remove/contains/get/value/is_added/is_changed/get_change_ticks/modify/tick/count + non_send init/insert/remove/contains/get/count + resource_scope) — mirrors world::mod.rs resource management API
- 28 tests — test_ecs_lib_world_resource_api_isolated.sla
- Tests: 1621 → 1649, lib modules: 161 → 162, test files: 83 → 84
- src/world/mod.rs (resource management) ✓

## Batch 35 — world_error (2026-07-02)
- lib/world_error.sla: EcsTryRunScheduleError + EcsTryInsertBatchError + EcsEntityDespawnError + EcsEntityComponentError + EcsEntityMutableFetchError + EcsResourceFetchError — mirrors world::error.rs
- 18 tests — test_ecs_lib_world_error_isolated.sla
- Tests: 1649 → 1667, lib modules: 162 → 163, test files: 84 → 85
- src/world/error.rs ✓

## Batch 36 — schedule_condition_advanced (2026-07-02)
- lib/schedule_condition_advanced.sla: EcsConditionChangedState (condition_changed/condition_changed_to) + 10 combinator types (and_then/and_eager/or_else/or_eager/nand_then/nand_eager/nor_then/nor_eager/xor_then/xor_eager) + not + combine_by_kind + resource_exists_and — mirrors schedule::condition.rs advanced condition state
- 22 tests — test_ecs_lib_schedule_condition_advanced_isolated.sla
- Tests: 1667 → 1689, lib modules: 163 → 164, test files: 85 → 86
- src/schedule/condition.rs (condition_changed/condition_changed_to/combinators) ✓

## Batch 37 — schedule_auto_insert_deferred (2026-07-02)
- lib/schedule_auto_insert_deferred.sla: EcsAutoInsertApplyDeferredPass (add_dependency/is_no_sync/get_sync_point/add_auto_sync/should_insert_sync/build) — mirrors schedule::auto_insert_apply_deferred.rs
- 16 tests — test_ecs_lib_schedule_auto_insert_deferred_isolated.sla
- Tests: 1689 → 1705, lib modules: 164 → 165, test files: 86 → 87
- src/schedule/auto_insert_apply_deferred.rs ✓

## Batch 38 — schedule_build_settings (2026-07-02)
- lib/schedule_build_settings.sla: LogLevel (Ignore/Warn/Error) + EcsScheduleBuildSettings2 (ambiguity_detection/hierarchy_detection/auto_insert_apply_deferred/use_shortnames/report_sets) + EcsScheduleBuildMetadata (warning_count/edges_added) — mirrors schedule::schedule.rs ScheduleBuildSettings + LogLevel + ScheduleBuildMetadata
- 14 tests — test_ecs_lib_schedule_build_settings_isolated.sla
- Tests: 1705 → 1719, lib modules: 165 → 166, test files: 87 → 88
- src/schedule/schedule.rs (ScheduleBuildSettings/LogLevel/ScheduleBuildMetadata) ✓

## Batch 39 — system_param_special (2026-07-02)
- lib/system_param_special.sla: EcsSystemBuffer (push/apply/queue/clear/get/len/is_applied) + EcsDeferred (push/apply/reborrow/clear/has_deferred) + EcsExclusiveMarker + EcsNonSendMarker + EcsRemovedComponentsParam (add/next/len/is_empty/clear) + EcsRunSystemOnceResult + EcsSystemParamValidationError — mirrors system::system_param.rs special params
- 21 tests — test_ecs_lib_system_param_special_isolated.sla
- Tests: 1719 → 1740, lib modules: 166 → 167, test files: 88 → 89
- src/system/system_param.rs (Deferred/SystemBuffer/ExclusiveMarker/NonSendMarker/RemovedComponents/RunSystemOnce) ✓

## Batch 40 — query_lens (2026-07-02)
- lib/query_lens.sla: EcsQueryLens (new/has_access/has_write/transmute/transmute_filtered/join/join_filtered/get/is_empty/as_query_lens/into_query_lens/query/filter_count) — mirrors system::query.rs QueryLens + transmute + join
- 15 tests — test_ecs_lib_query_lens_isolated.sla
- Tests: 1740 → 1755, lib modules: 167 → 168, test files: 89 → 90
- src/system/query.rs (QueryLens/transmute_lens/join) ✓

## Batch 41 — observer_condition (2026-07-02)
- lib/observer_condition.sla: EcsObserverCondition (new/initialize/check/last_result) + EcsObserverWithCondition (new/run_if/check/initialize/take_conditions) + conditions helpers (all_true/any_true/count/true_count) — mirrors observer::condition.rs
- 22 tests — test_ecs_lib_observer_condition_isolated.sla
- Tests: 1755 → 1777, lib modules: 168 → 169, test files: 90 → 91
- src/observer/condition.rs ✓

## Batch 42 — archetype_edges (2026-07-02)
- lib/archetype_edges.sla: EcsArchetypeId/EcsArchetypeRow/ComponentStatus/EcsArchetypeAfterBundleInsert/EcsArchetypeEdges (insert/remove/take cache+get) /EcsArchetypeEntity — mirrors archetype.rs Edges + ArchetypeAfterBundleInsert + ArchetypeEntity
- 18 tests — test_ecs_lib_archetype_edges_isolated.sla
- Tests: 1777 → 1795, lib modules: 169 → 170, test files: 91 → 92
- src/archetype.rs (Edges/ArchetypeAfterBundleInsert/ArchetypeEntity) ✓

## Batch 43 — entities_collection (2026-07-02)
- lib/entities_collection.sla: EcsEntityLocation (new/archetype/table/table_row/eq) + EcsEntities (alloc/free/free_many/contains/contains_spawned/is_index_spawned/get_spawned/get/set_location/resolve_from_index/get_spawn_tick/get_despawn_tick/len/is_empty/count_spawned/any_spawned/clear/tick) — mirrors entity/mod.rs Entities struct
- 19 tests — test_ecs_lib_entities_collection_isolated.sla
- Tests: 1795 → 1814, lib modules: 170 → 171, test files: 92 → 93
- src/entity/mod.rs (Entities/EcsEntityLocation) ✓

## Batch 44 — unique_vec (2026-07-02)
- lib/unique_vec.sla: EcsUniqueEntityVec (new/with_capacity/from_vec/into_inner/as_slice/len/is_empty/get/first/last/contains/index_of/push/insert/swap_remove/remove/pop/clear/truncate/retain/split_off/extend_from_slice/from_entity_iter/eq/dedup) — mirrors entity/unique_vec.rs
- 23 tests — test_ecs_lib_unique_vec_isolated.sla
- Tests: 1814 → 1837, lib modules: 171 → 172, test files: 93 → 94
- src/entity/unique_vec.rs (UniqueEntityEquivalentVec) ✓

## Batch 45 — unique_slice (2026-07-02)
- lib/unique_slice.sla: EcsUniqueEntitySlice (new/empty/as_slice/into_inner/len/is_empty/get/first/last/get_sub_slice/contains/index_of/rindex_of/swap/reverse/rotate_left/rotate_right/sort/starts_with/ends_with/to_vec/eq/count_greater_than/min/max) — mirrors entity/unique_slice.rs
- 24 tests — test_ecs_lib_unique_slice_isolated.sla
- Tests: 1837 → 1861, lib modules: 172 → 173, test files: 94 → 95
- src/entity/unique_slice.rs (UniqueEntityEquivalentSlice) ✓

## Batch 46 — unique_array (2026-07-02)
- lib/unique_array.sla: EcsUniqueEntityArray (new/from_array/into_inner/as_slice/len/is_empty/is_full/capacity/get/first/last/contains/index_of/set/push/swap/reverse/eq/sum/map_doubled) — mirrors entity/unique_array.rs
- 19 tests — test_ecs_lib_unique_array_isolated.sla
- Tests: 1861 → 1880, lib modules: 173 → 174, test files: 95 → 96
- src/entity/unique_array.rs (UniqueEntityEquivalentArray) ✓

## Batch 47 — clone_entities (2026-07-02)
- lib/clone_entities.sla: EcsSourceComponent + EcsEntityMapper + EcsComponentCloneCtx + EcsEntityClonerState — mirrors entity/clone_entities.rs
- 29 tests — test_ecs_lib_clone_entities_isolated.sla
- Tests: 1880 → 1909, lib modules: 174 → 175, test files: 96 → 97
- src/entity/clone_entities.rs (SourceComponent/ComponentCloneCtx/EntityMapper/EntityClonerState) ✓

## Batch 48 — table_column (2026-07-02)
- lib/table_column.sla: EcsColumn (with_capacity/component_id/size/capacity/has_drop/len/is_empty/get_data/get_added_tick/get_changed_tick/get_changed_by/get_ticks/initialize/replace/swap_remove/clear/check_change_ticks/realloc/drop_last/get_drop/count_matching) — mirrors storage/table/column.rs
- 20 tests — test_ecs_lib_table_column_isolated.sla
- Tests: 1909 → 1929, lib modules: 175 → 176, test files: 97 → 98
- src/storage/table/column.rs (Column) ✓

## Batch 49 — blob_array (2026-07-02)
- lib/blob_array.sla: EcsBlobArray (with_capacity/new/item_size/item_align/is_zst/get_drop/len/is_empty/get/get_sub_slice/initialize/replace/swap_remove/swap_remove_and_drop/clear/drop_last/drop_all/get_ptr/count) — mirrors storage/blob_array.rs
- 19 tests — test_ecs_lib_blob_array_isolated.sla
- Tests: 1929 → 1948, lib modules: 176 → 177, test files: 98 → 99
- src/storage/blob_array.rs (BlobArray) ✓

## Batch 50 — thin_array_ptr (2026-07-02)
- lib/thin_array_ptr.sla: EcsThinArrayPtr (with_capacity/empty/alloc/realloc/capacity/initialize/get/swap_remove/swap_remove_nonoverlapping/clear_elements/drop/as_slice/len/is_empty) — mirrors storage/thin_array_ptr.rs
- 15 tests — test_ecs_lib_thin_array_ptr_isolated.sla
- Tests: 1948 → 1963, lib modules: 177 → 178, test files: 99 → 100
- src/storage/thin_array_ptr.rs (ThinArrayPtr) ✓

## Batch 51 — executor_single_threaded (2026-07-02)
- lib/executor_single_threaded.sla: EcsSingleThreadedExecutor (new/init/set_apply_final_deferred/mark_completed/is_completed/mark_set_evaluated/is_set_evaluated/mark_unapplied/is_unapplied/run_system/skip_system/apply_deferred/finish/completed_count/unapplied_count) — mirrors schedule/executor/single_threaded.rs
- 13 tests — test_ecs_lib_executor_single_threaded_isolated.sla
- Tests: 1963 → 1976, lib modules: 178 → 179, test files: 100 → 101
- src/schedule/executor/single_threaded.rs (SingleThreadedExecutor) ✓

## Batch 52 — executor_multi_threaded (2026-07-02)
- lib/executor_multi_threaded.sla: EcsMultiThreadedExecutor + EcsExecutorState (new/init/set_apply_final_deferred/mark_starting/is_starting + state init/set_dependencies/get_dependencies/mark_ready/is_ready/start_system/is_running/complete_system/is_completed/skip_system/is_skipped/apply_deferred_system/is_unapplied/num_running/local_thread_running/exclusive_running/completed_count/ready_count/unapplied_count) — mirrors schedule/executor/multi_threaded.rs
- 18 tests — test_ecs_lib_executor_multi_threaded_isolated.sla
- Tests: 1976 → 1994, lib modules: 179 → 180, test files: 101 → 102
- src/schedule/executor/multi_threaded.rs (MultiThreadedExecutor/ExecutorState) ✓

## Batch 53 — observer_distributed_storage (2026-07-02)
- lib/observer_distributed_storage.sla: EcsObserver + EcsObservedBy (Observer new/with_dynamic_runner/with_entity/watch_entity/watch_entities/with_component/with_components/with_event_key/with_error_handler/run_if/set_name/watches_entity/watches_component + ObservedBy new/add/get/count/remove/len) — mirrors observer/distributed_storage.rs
- 20 tests — test_ecs_lib_observer_distributed_storage_isolated.sla
- Tests: 1994 → 2014, lib modules: 180 → 181, test files: 102 → 103
- src/observer/distributed_storage.rs (Observer/ObserverDescriptor/ObservedBy) ✓

## Batch 54 — system_schedule (2026-07-03)
- lib/system_schedule.sla: EcsSystemSchedule + ApplyDeferred + default_executor (new/add_system/add_set/get_system_id/get_system_conditions/get_system_dependencies/get_set_id/mark_run/mark_skip/reset/clear/is_empty/total_conditions/total_dependencies + is_apply_deferred + default_executor_kind) — mirrors schedule/executor/mod.rs
- 16 tests — test_ecs_lib_system_schedule_isolated.sla
- Tests: 2014 → 2030, lib modules: 181 → 182, test files: 103 → 104
- src/schedule/executor/mod.rs (SystemSchedule/ApplyDeferred/default_executor) ✓

## Batch 55 — observer_centralized_storage (2026-07-03)
- lib/observer_centralized_storage.sla: EcsObservers + EcsCachedObservers + EcsCachedComponentObservers (lifecycle constants + archetype flags + CachedComponentObservers add/get/count + CachedObservers add_global/add_component/add_entity/get/is_empty + Observers new/get/get_or_create/add_global/is_archetype_cached) — mirrors observer/centralized_storage.rs
- 21 tests — test_ecs_lib_observer_centralized_storage_isolated.sla
- Tests: 2030 → 2051, lib modules: 182 → 183, test files: 104 → 105
- src/observer/centralized_storage.rs (Observers/CachedObservers/CachedComponentObservers) ✓

## Batch 56 — reflect_type_data (2026-07-03)
- lib/reflect_type_data.sla: ReflectFromWorld + ReflectEvent + ReflectMapEntities + ReflectCommand — mirrors reflect/{from_world,event,map_entities,entity_commands}.rs
- 10 tests — test_ecs_lib_reflect_type_data_isolated.sla
- Tests: 2051 → 2061, lib modules: 183 → 184, test files: 105 → 106
- src/reflect/from_world.rs (ReflectFromWorld) ✓
- src/reflect/event.rs (ReflectEvent) ✓
- src/reflect/map_entities.rs (ReflectMapEntities) ✓
- src/reflect/entity_commands.rs (ReflectCommandExt) ✓

## Batch 57 — table_mod (2026-07-03)
- lib/table_mod.sla: EcsTable + EcsTableId + EcsTableRow + EcsTables (TableId/TableRow new/value/index + Table new/add_column/allocate/get/set/get_added_tick/get_changed_tick/swap_remove/get_entity_at_row/has_column/get_column_index + Tables new/get/create) — mirrors storage/table/mod.rs
- 23 tests — test_ecs_lib_table_mod_isolated.sla
- Tests: 2061 → 2084, lib modules: 184 → 185, test files: 106 → 107
- src/storage/table/mod.rs (Table/TableId/TableRow/Tables) ✓

## Batch 58 — non_send_storage (2026-07-03)
- lib/non_send_storage.sla: EcsNonSendData + EcsNonSends (NonSendData new/insert/remove/is_present/get_data/get_ticks/get_added_tick/get_changed_tick/get_changed_by/set_changed + NonSends new/len/is_empty/get/get_or_insert/insert/remove/clear/contains/count_present) — mirrors storage/non_send.rs
- 19 tests — test_ecs_lib_non_send_storage_isolated.sla
- Tests: 2084 → 2103, lib modules: 185 → 186, test files: 107 → 108
- src/storage/non_send.rs (NonSendData/NonSends) ✓

## Batch 59 — observer_entity_cloning (2026-07-03)
- lib/observer_entity_cloning.sla: EcsObserverCloneState (new/set_add_observers/register_clone/get_source/get_target/queue_observer/has_queued_observer/queue_event_key/queue_component/clear) — mirrors observer/entity_cloning.rs
- 15 tests — test_ecs_lib_observer_entity_cloning_isolated.sla
- Tests: 2103 → 2118, lib modules: 186 → 187, test files: 108 → 109
- src/observer/entity_cloning.rs (EntityClonerBuilder::add_observers/component_clone_observed_by) ✓

## Batch 60 — parallel_scope (2026-07-03)
- lib/parallel_scope.sla: EcsParallelCommands + EcsParallelCommandQueue (ParallelCommandQueue new/command/len/count_for_thread/get_commands_for_thread/get_all_commands/clear/is_empty + ParallelCommands new/command_scope/total_commands/queue_count/clear/is_empty) — mirrors system/commands/parallel_scope.rs
- 11 tests — test_ecs_lib_parallel_scope_isolated.sla
- Tests: 2118 → 2129, lib modules: 187 → 188, test files: 109 → 110
- src/system/commands/parallel_scope.rs (ParallelCommands) ✓

## Batch 61 — change_detection_params (2026-07-03)
- lib/change_detection_params.sla: Res + ResMut + NonSend + NonSendMut + Ref + Mut + MutUntyped — mirrors change_detection/params.rs
- 22 tests — test_ecs_lib_change_detection_params_isolated.sla
- Tests: 2129 → 2151, lib modules: 188 → 189, test files: 110 → 111
- src/change_detection/params.rs (Res/ResMut/NonSend/NonSendMut/Ref/Mut/MutUntyped) ✓

## Batch 62 — change_detection_traits (2026-07-03)
- lib/change_detection_traits.sla: DetectChangesExt (new/last_changed/changed_by/set_last_changed/set_last_added/bypass_change_detection/set_if_neq/replace_if_neq/clone_from_if_neq/is_added/is_changed/is_added_after/is_changed_after/added/this_run/last_run/set_changed_by) — mirrors change_detection/traits.rs
- 16 tests — test_ecs_lib_change_detection_traits_isolated.sla
- Tests: 2151 → 2167, lib modules: 189 → 190, test files: 111 → 112
- src/change_detection/traits.rs (DetectChanges/DetectChangesMut) ✓

## Batch 63 — schedule_node_sets (2026-07-03)
- lib/schedule_node_sets.sla: Systems extensions (get_mut/get_conditions_mut/iter/remove/initialize/is_initialized/uninit) + SystemSets (new/len/is_empty/contains/get/get_key/get_key_or_insert/has_conditions/get_conditions/get_conditions_mut/iter/remove/initialize/is_initialized/set_is_system_type/check_type_set_ambiguity) + ConflictingSystems (new/len/push/check_if_not_empty/get/a/b/conflicts) + EcsSystemAccess (is_compatible/get_conflicts) + AmbiguousSystemConflictsWarning + SystemTypeSetAmbiguityError — mirrors src/schedule/node.rs
- 32 tests — test_ecs_lib_schedule_node_sets_isolated.sla
- Tests: 2167 → 2199, lib modules: 189 → 190, test files: 112 → 113
- src/schedule/node.rs (SystemSets, ConflictingSystems, Systems::get_mut/get_conditions_mut/iter/initialize) ✓

## Batch 64 — system_registry_template (2026-07-03)
- lib/system_registry_template.sla: SystemHandleTemplate + SystemHandleValue + CachedSystemId + EcsCachedSystemRegistry (register/unregister/run/run_with) + EcsTrackedSystem + EcsStrippedSystemHandle + EcsTemplateContext — mirrors src/system/system_registry.rs (templates extension)
- 24 tests — test_ecs_lib_system_registry_template_isolated.sla
- Tests: 2199 → 2223, lib modules: 190 → 191, test files: 113 → 114
- src/system/system_registry.rs (SystemHandleTemplate, SystemHandleValue, CachedSystemId, register_system_cached/unregister_system_cached/run_system_cached/run_system_cached_with, register_tracked_system/register_tracked_boxed_system) ✓

## Batch 65 — world_mod (2026-07-03)
- lib/world_mod.sla: World struct comprehensive surface (~140 pub fns from src/world/mod.rs) — WorldId/EntityLocation/SpawnBatchIter/CheckChangeTicks/World covering spawn/spawn_at/spawn_batch, register_component/register_resource(dedup)/init/insert/remove, resource_getters (with scope), non_send complete surface, despawn/try_despawn/no_free, clear_trackers, query/try_query, removed, insert_batch(_if_new)/try_insert_batch(_if_new), write_message(_default/_batch), change_tick APIs (read/change/last/scope/check), clear_all/clear_entities/clear_resources/clear_non_send, add/get/contains/remove/run schedules, allow_ambiguous_*, register_required_components(_with)/get_required_components, register_bundle(_dynamic), modify_component(_by_id), modify_resource(_by_id), inspect_entity.
- 52 tests — test_ecs_lib_world_mod_isolated.sla
- Tests: 2223 → 2275, lib modules: 191 → 192, test files: 114 → 115
- src/world/mod.rs (World pub API — ~140 methods) ✓

## Batch 66 — commands_mod_extension (2026-07-03)
- lib/commands_mod_extension.sla: Commands + EntityCommands extension methods (register_boxed_system / unregister_system_cached / run_system_cached(_with) / trigger / trigger_with / add_observer / write_message / run_schedule / get_spawned_entity; entry / queue_handled / queue_silenced / log_components / commands(_mut) / observe / trigger / clone_with_opt_out / clone_with_opt_in / clone_and_spawn(_with_opt_out/_with_opt_in) / clone_components / move_components) — mirrors src/system/commands/mod.rs
- 35 tests — test_ecs_lib_commands_mod_extension_isolated.sla
- Tests: 2275 → 2310, lib modules: 192 → 193, test files: 115 → 116
- src/system/commands/mod.rs (Commands/EntityCommands pub method gaps) ✓

## Batch 67 — schedule_dag_analysis (2026-07-03)
- lib/schedule_dag_analysis.sla: DagAnalysis + DagGroups + 3 error types — mirrors src/schedule/graph/dag.rs
- 23 tests — test_ecs_lib_schedule_dag_analysis_isolated.sla
- Tests: 2310 → 2333, lib modules: 193 → 194, test files: 116 → 117
- src/schedule/graph/dag.rs (DagAnalysis, DagGroups, DagRedundancyError, DagCrossDependencyError, DagOverlappingGroupError) ✓

## Batch 68 — function_system_extras (2026-07-03)
- lib/function_system_extras.sla: SystemState<Param> + FunctionSystemV2 + IsFunctionSystem/HasSystemInput markers — mirrors src/system/function_system.rs
- 23 tests — test_ecs_lib_function_system_extras_isolated.sla
- Tests: 2333 → 2356, lib modules: 194 → 195, test files: 117 → 118
- src/system/function_system.rs (SystemState, FunctionSystem, IsFunctionSystem, HasSystemInput) ✓

## Batch 69 — system_param_extras (2026-07-03)
- lib/system_param_extras.sla: Deferred / If<T> / StaticSystemParam<T> / DynSystemParam / SystemParamValidationErrorV2 — mirrors src/system/system_param.rs
- 24 tests — test_ecs_lib_system_param_extras_isolated.sla
- Tests: 2356 → 2380, lib modules: 195 → 196, test files: 118 → 119
- src/system/system_param.rs (Deferred, If, StaticSystemParam, DynSystemParam, SystemParamValidationError) ✓

## Batch 70 — bundle_info_extras (2026-07-03)
- lib/bundle_info_extras.sla: BundleId::index + contributed_components split + Bundles registry — mirrors src/bundle/info.rs
- 20 tests — test_ecs_lib_bundle_info_extras_isolated.sla
- Tests: 2380 → 2400, lib modules: 196 → 197, test files: 119 → 120
- src/bundle/info.rs (BundleId::index, BundleInfo contributed/explicit/required components + iter_*, Bundles registry get/get_id/is_empty/iter) ✓

## Batch 71 — component_info_extras (2026-07-03)
- lib/component_info_extras.sla: ComponentInfo accessors + Components registry — mirrors src/component/info.rs
- 25 tests — test_ecs_lib_component_info_extras_isolated.sla
- Tests: 2400 → 2425, lib modules: 197 → 198, test files: 120 → 121
- src/component/info.rs (ComponentInfo accessors + Components registry get_id/get_valid_id/get_resource_id/get_valid_resource_id/iter_registered + queued counts) ✓

## Batch 72 — query_state_extras (2026-07-03)
- lib/query_state_extras.sla: StorageSwitch + fetch wrappers + QueryState static surface — mirrors src/query/state.rs + src/query/fetch.rs
- 22 tests — test_ecs_lib_query_state_extras_isolated.sla
- Tests: 2425 → 2447, lib modules: 198 → 199, test files: 121 → 122
- src/query/state.rs (QueryState component_access / matched_* / validate_world / matches_component_set / transmute_filtered / join_filtered + read/write access queries) + src/query/fetch.rs (StorageSwitch + ReadFetch/WriteFetch/RefFetch) ✓

## Batch 73 — system_combinator (2026-07-03)
- lib/system_combinator.sla: CombinatorSystem / PipeSystem / IntoPipeSystem / IsPipeSystemMarker + assert helpers — mirrors src/system/combinator.rs + src/system/mod.rs
- 21 tests — test_ecs_lib_system_combinator_isolated.sla
- Tests: 2447 → 2468, lib modules: 199 → 200, test files: 122 → 123
- src/system/combinator.rs (CombinatorSystem, PipeSystem, IntoPipeSystem, IsPipeSystemMarker) + src/system/mod.rs (assert_is_system/assert_is_read_only_system/assert_system_does_not_conflict) ✓

## Batch 74 — schedule_stepping (2026-07-03)
- lib/schedule_stepping.sla: Stepping controller — mirrors src/schedule/stepping.rs
- 23 tests — test_ecs_lib_schedule_stepping_isolated.sla
- Tests: 2468 → 2491, lib modules: 200 → 201, test files: 123 → 124
- src/schedule/stepping.rs (Stepping + Action + SystemBehavior + schedules + cursor + add/remove/clear schedule + enable/disable + step/continue frame + always_run/never_run/set/clear breakpoint/clear node + skipped_systems) ✓

## Batch 75 — entity_lifecycle (2026-07-03)
- lib/entity_lifecycle.sla: DefaultQueryFilters + ComponentHooks + RemovedComponents — mirrors src/entity_disabling.rs + src/lifecycle.rs
- 25 tests — test_ecs_lib_entity_lifecycle_isolated.sla
- Tests: 2491 → 2516, lib modules: 201 → 202, test files: 124 → 125
- src/entity_disabling.rs (DefaultQueryFilters empty/register_disabling_component/disabling_ids) + src/lifecycle.rs (ComponentHooks on_*/try_on_*, RemovedComponents write/read/read_with_id/messages/len/clear) ✓

## Batch 76 — archetype_info (2026-07-03)
- lib/archetype_info.sla: Archetype struct surface + ArchetypeFlags bitmask — mirrors src/archetype.rs
- 21 tests — test_ecs_lib_archetype_info_isolated.sla
- Tests: 2516 → 2537, lib modules: 202 → 203, test files: 125 → 126
- src/archetype.rs (Archetype id/table_id/components/contains/get_storage_type/len/is_empty/component_count/entity_table_row/has_*_hook/has_*_observer/edges/generation + ArchetypeFlags bitmask) ✓

## Batch 77 — archetypes_registry (2026-07-03)
- lib/archetypes_registry.sla: plural Archetypes collection + ArchetypeRecord + ComponentIndex — mirrors src/archetype.rs
- 19 tests — test_ecs_lib_archetypes_registry_isolated.sla
- Tests: 2537 → 2556, lib modules: 203 → 204, test files: 126 → 127
- src/archetype.rs (Archetypes new/len/empty/get/iter/generation/spawn_table/clear_entities/component_index + ArchetypeRecord + ComponentIndex component_id->{archetype_id,column}) ✓

## Batch 78 — sparse_set_extras (2026-07-03)
- lib/sparse_set_extras.sla: ComponentSparseSet tick accessors + ImmutableSparseSet + SparseSets collection — mirrors src/storage/sparse_set.rs
- 26 tests — test_ecs_lib_sparse_set_extras_isolated.sla
- Tests: 2556 → 2582, lib modules: 204 → 205, test files: 127 → 128
- src/storage/sparse_set.rs (ComponentSparseSet contains/get/get_added_tick/get_changed_tick/get_ticks/get_changed_by/get_drop + ImmutableSparseSet with_capacity/capacity/insert/get/get_mut/remove/clear/contains + SparseSets collection get_or_insert) ✓

## Batch 79 — resource_mod (2026-07-03)
- lib/resource_mod.sla: IsResource marker + ResourceEntities + IS_RESOURCE flag — mirrors src/resource.rs
- 16 tests — test_ecs_lib_resource_mod_isolated.sla
- Tests: 2582 → 2598, lib modules: 205 → 206, test files: 128 → 129
- src/resource.rs (IsResource new/resource_component_id + ResourceEntities new/get/insert/iter + IS_RESOURCE constant) ✓

## Batch 80 — event_mod (2026-07-03)
- lib/event_mod.sla: EventKey + World event registry facade — mirrors src/event/mod.rs
- 11 tests — test_ecs_lib_event_mod_isolated.sla
- Tests: 2598 → 2609, lib modules: 206 → 207, test files: 129 → 130
- src/event/mod.rs (EventKey new/component_id + World register_event_key/event_key) ✓

## Batch 81 — component_register (2026-07-03)
- lib/component_register.sla: ComponentIdRegistrator iterator + ComponentsQueuedRegistrator facade — mirrors src/component/register.rs
- 14 tests — test_ecs_lib_component_register_isolated.sla
- Tests: 2609 → 2623, lib modules: 207 → 208, test files: 130 → 131
- src/component/register.rs (ComponentIdRegistrator peek/next/peek_mut/next_mut/len/is_empty/as_queued/apply_queued_registrations/any_queued_mut/num_queued_mut + queue_register_component|resource|non_send + register_component_with_descriptor) ✓

## Batch 82 — observer_descriptor_extras (2026-07-03)
- lib/observer_descriptor_extras.sla: ObserverDescriptor v2 + Observer run state + ObserverV2 combined — mirrors src/observer/distributed_storage.rs
- 17 tests — test_ecs_lib_observer_descriptor_extras_isolated.sla
- Tests: 2623 → 2640, lib modules: 208 → 209, test files: 131 → 132
- src/observer/distributed_storage.rs (ObserverDescriptor with_event_keys|with_components|with_entities + event_keys()|components()|entities() accessor parity + Observer last_trigger_id/despawned_watched_entities/run + with_error_handler/with_name) ✓

## Batch 83 — query_builder_extras (2026-07-03)
- lib/query_builder_extras.sla: QueryBuilder id-by-id variants + World mut + access view + transmute/build gap — mirrors src/query/builder.rs
- 15 tests — test_ecs_lib_query_builder_extras_isolated.sla
- Tests: 2640 → 2655, lib modules: 209 → 210, test files: 132 → 133
- src/query/builder.rs (QueryBuilder with_id/without_id/world_mut/access + transmute/transmute_filtered + build) ✓


## Batch 84 — world_extras (2026-07-03)
- lib/world_extras.sla: try_register_required_components[_with] + get_required_components_by_id + modify_component[_by_id] + modify_resource[_by_id] + spawn_at/empty_at/batch + EntityAllocator + ResourceEntities + components_queue/registrator + as_unsafe_world_cell facades — mirrors src/world/mod.rs gaps not in lib/ecs_world.sla
- 35 tests — test_ecs_lib_world_extras_isolated.sla
- Tests: 2655 → 2690, lib modules: 208 → 209, test files: 133 → 134
- src/world/mod.rs (try_register_required_components/try_register_required_components_with/get_required_components_by_id/modify_component[_by_id]/modify_resource[_by_id]/spawn_at/spawn_empty_at/spawn_batch/components_queue/components_registrator/entity_allocator/resource_entities/as_unsafe_world_cell_readonly + RequiredComponentsError {DuplicateRegistration,CyclicRequirement,ArchetypeExists} + SpawnError {Invalid,AlreadySpawned} + EntityMutableFetchError {NotSpawned,AliasedMutability}) ✓


## Batch 85 — query_state_read_api (2026-07-03)
- lib/query_state_read_api.sla: QueryState read API gaps — single/single_mut + is_empty + contains + get/get_mut + get_many[_mut/_unique/_unique_mut] + iter_many[_mut/_unique/_unique_mut] + try_new + from_builder + update_archetypes + QueryEntityError + QuerySingleError markers — mirrors src/query/state.rs gaps not in lib/query_state_extras.sla
- 27 tests — test_ecs_lib_query_state_read_api_isolated.sla
- Tests: 2690 → 2717, lib modules: 209 → 210, test files: 134 → 135
- src/query/state.rs (single/single_mut + is_empty + contains + get/get_manual/get_mut + get_many/get_many_mut/get_many_unique/get_many_unique_mut + iter_many/iter_many_mut/iter_many_unique/iter_many_unique_mut + try_new + from_builder + update_archetypes + QueryEntityError {QueryDoesNotMatch,NotSpawned,AliasedMutability} + QuerySingleError {NoEntities,MultipleEntities}) ✓


## Batch 86 — world_observer_trigger (2026-07-03)
- lib/world_observer_trigger.sla: World::trigger/trigger_with/trigger_ref/trigger_ref_with + add_observer + observer registry bookkeeping — mirrors src/observer/mod.rs (gaps not in lib/observer_*.sla or lib/deferred_world.sla)
- 15 tests — test_ecs_lib_world_observer_trigger_isolated.sla
- Tests: 2717 → 2732, lib modules: 210 → 211, test files: 135 → 136
- src/observer/mod.rs (trigger + trigger_with + trigger_ref + trigger_ref_with + add_observer) ✓


## Batch 87 — entity_ref_extras (2026-07-03)
- lib/entity_ref_extras.sla: EntityRef pub surface not in lib/entity_access.sla — into_filtered + location + archetype + contains_id/_type_id + get_ref + get_change_ticks[_by_id] + get_changed_by + get_by_id + components (count reduce) + get_components (all-or-none) + spawned_by + spawn_tick — mirrors src/world/entity_access/entity_ref.rs (gaps not in lib/entity_access.sla)
- 20 tests — test_ecs_lib_entity_ref_extras_isolated.sla
- Tests: 2732 → 2752, lib modules: 211 → 212, test files: 136 → 137
- src/world/entity_access/entity_ref.rs (location/archetype/contains_id/contains_type_id/get_ref/get_change_ticks/get_changed_by/get_change_ticks_by_id/get_by_id/components/get_components/into_filtered/spawned_by/spawn_tick) ✓


## Batch 88 — deferred_world_extras (2026-07-03)
- lib/deferred_world_extras.sla: DeferredWorld pub surface not in lib/deferred_world.sla — get_mut + get_entity_mut + query + non_send_resource_mut + get_resource_mut_by_id + get_non_send_mut_by_id — mirrors src/world/deferred_world.rs (gaps not in lib/deferred_world.sla)
- 20 tests — test_ecs_lib_deferred_world_extras_isolated.sla
- Tests: 2752 → 2772, lib modules: 212 → 213, test files: 137 → 138
- src/world/deferred_world.rs (get_mut + get_entity_mut + query + non_send_resource_mut + get_resource_mut_by_id + get_non_send_mut_by_id) ✓


## Batch 89 — query_sort_iter (2026-07-03)
- lib/query_sort_iter.sla: QueryIter sort family — sort/sort_unstable/sort_by/sort_unstable_by/sort_by_key/sort_unstable_by_key/sort_by_cached_key + QuerySortedIter + sort_impl panic-if-consumed — mirrors src/query/iter.rs (gaps not in lib/query_iter.sla)
- 19 tests — test_ecs_lib_query_sort_iter_isolated.sla
- Tests: 2772 → 2791, lib modules: 213 → 214, test files: 138 → 139
- src/query/iter.rs (sort + sort_unstable + sort_by + sort_unstable_by + sort_by_key + sort_unstable_by_key + sort_by_cached_key + QuerySortedIter fetch_next) ✓


## Batch 90 — query_access_ops (2026-07-03)
- lib/query_access_ops.sla: query/access.rs gaps — ComponentIdSet ops + AccessConflicts + Access get_conflicts/extend/intersection/union/remove_conflicting_access + FilteredAccess matches_everything/nothing/extend_access/get_conflicts/is_disjoint/access — mirrors src/query/access.rs (gaps not in lib/query_access.sla)
- 30 tests — test_ecs_lib_query_access_ops_isolated.sla
- Tests: 2791 → 2821, lib modules: 214 → 215, test files: 139 → 140
- src/query/access.rs (FilterSet union/intersection/union_with/intersect_with/is_disjoint/is_clear/is_empty + AccessConflicts + Access get_conflicts/extend/intersection/union/remove_conflicting_access + FilteredAccess matches_everything/matches_nothing/extend_access/get_conflicts/is_disjoint) ✓


## Batch 91 — query_filtered_set (2026-07-03)
- lib/query_filtered_set.sla: FilteredAccessSet (gap surface) — mirrors src/query/access.rs
- 19 tests — test_ecs_lib_query_filtered_set_isolated.sla
- Tests: 2821 → 2840, lib modules: 215 → 216, test files: 140 → 141
- src/query/access.rs (FilteredAccessSet new/combined_access/filtered_accesses/is_compatible/get_conflicts/get_conflicts_single/add/add_resource_read/_write/add_unfiltered_read_all_components/add_unfiltered_write_all_components/extend/read_all/write_all/clear + Access::is_compatible helper) ✓


## Batch 92 — filtered_resource_builders (2026-07-03)
- lib/filtered_resource_builders.sla: FilteredResourcesBuilder + FilteredResourcesMutBuilder — mirrors src/world/filtered_resource.rs (gaps not in lib/filtered_resource.sla or lib/system_builder.sla)
- 12 tests — test_ecs_lib_filtered_resource_builders_isolated.sla
- Tests: 2840 → 2852, lib modules: 216 → 217, test files: 141 → 142
- src/world/filtered_resource.rs (FilteredResourcesBuilder new/access/add_read_all/add_read[_by_id]/build + FilteredResourcesMutBuilder new/access/add_read_all/add_read[_by_id]/add_write_all/add_write[_by_id]/build) ✓


## Batch 93 — schedule_configs_extras (2026-07-03)
- lib/schedule_configs_extras.sla: IntoScheduleConfigs/ScheduleConfigs gaps — chain/chain_ignore_deferred/distributive_run_if/run_if/ambiguous_with/ambiguous_with_all/before_ignore_deferred/after_ignore_deferred/into_configs — mirrors src/schedule/config.rs (gaps not in lib/schedule_config.sla)
- 16 tests — test_ecs_lib_schedule_configs_extras_isolated.sla
- Tests: 2852 → 2868, lib modules: 217 → 218, test files: 142 → 143
- src/schedule/config.rs (IntoScheduleConfigs chain/chain_ignore_deferred/distributive_run_if/run_if/ambiguous_with/ambiguous_with_all/before_ignore_deferred/after_ignore_deferred/into_configs + ScheduleConfigs.apply_deferred_on_edges + before/after _ignore_deferred_inner + distributive_run_if_inner + ambiguous_with_inner/ambiguous_with_all_inner + chain_ignore_deferred_inner) ✓


## Batch 94 — required_components_dynamic (2026-07-03)
- lib/required_components_dynamic.sla: RequiredComponents register_by_id + register_dynamic_with + the _mut builder variants + EcsRequiredComponentsRegistratorDyn facade (new/target/components_next_id/register_required_by_id/_dynamic_with + last_ok/last_err_kind/_required_direct_count/_required_all_count/_required_direct_at/_required_all_at) — mirrors src/component/required.rs dynamic-registration gaps not in lib/component_required.sla
- 16 tests — test_ecs_lib_required_components_dynamic_isolated.sla
- Tests: 2868 → 2884, lib modules: 218 → 219, test files: 143 → 144
- src/component/required.rs (RequiredComponents::register_by_id + register_dynamic_with + register_dynamic_with_mut/register_by_id_mut + RequiredComponentsRegistrator::register_required_by_id + register_required_dynamic_with + components_registrator accessor + register_inherited_required_components_unchecked id-prepend-to-all model) ✓


## Batch 95 — removed_component_messages (2026-07-03)
- lib/removed_component_messages.sla: world-level RemovedComponentMessages storage + RemovedComponentReader reader API — mirrors src/lifecycle.rs (RemovedComponentMessages + RemovedComponentReader gaps not in lib/ecs_world.sla (write-only) or lib/entity_lifecycle.sla (per-component-level))
- 23 tests — test_ecs_lib_removed_component_messages_isolated.sla
- Tests: 2884 → 2907, lib modules: 219 → 220, test files: 144 → 145
- src/lifecycle.rs (RemovedComponentMessages::new/update/iter/get/write + RemovedComponentReader::new/read/read_with_id/len/is_empty/clear + cursor/drained accessors + iter_pair/entity_at helpers + SparseSet-as-flat-Vec model) ✓


## Batch 96 — query_par_many_iter (2026-07-03)
- lib/query_par_many_iter.sla: QueryParManyIter + QueryParManyUniqueIter — mirrors src/query/par_iter.rs (gaps not in lib/query_par_iter.sla)
- 21 tests — test_ecs_lib_query_par_many_iter_isolated.sla
- Tests: 2907 → 2928, lib modules: 220 → 221, test files: 145 → 146
- src/query/par_iter.rs (QueryParManyIter::batching_strategy/for_each/for_each_init + QueryParManyUniqueIter::batching_strategy/for_each/for_each_init + len/is_empty/batch_count + UniqueEntityEquivalentVec de-dup model + Fn-over-items closure-as-func_id parameterization) ✓


## Batch 97 — entity_cloner_builder_extras (2026-07-03)
- lib/entity_cloner_builder_extras.sla: EntityClonerBuilder remaining pub surface (with_default_clone_fn + override_clone_behavior_with_id + remove_clone_behavior_override_with_id + without_required_components scope + without_required_by_components scope) — mirrors src/entity/clone_entities.rs lines 817-1004 (gaps not in lib/entity_cloner.sla)
- 13 tests — test_ecs_lib_entity_cloner_builder_extras_isolated.sla
- Tests: 2928 → 2941, lib modules: 221 → 222, test files: 146 → 147
- src/entity/clone_entities.rs (EntityClonerBuilder::with_default_clone_fn + override_clone_behavior_with_id + remove_clone_behavior_override_with_id + without_required_components [OptIn scope] + without_required_by_components [OptOut scope] + ComponentCloneFn-as-id + ComponentCloneBehavior-as-id) ✓


## Batch 98 — relationship_methods_extras (2026-07-03)
- lib/relationship_methods_extras.sla: EntityWorldMut/EntityCommands related-methods gaps (add_one_related + detach_all_related + despawn_related + despawn_children + with_related + with_related_entities + insert_recursive + remove_recursive) — mirrors src/relationship/related_methods.rs (gaps not in lib/relationship_related_methods.sla)
- 21 tests — test_ecs_lib_relationship_methods_extras_isolated.sla
- Tests: 2941 → 2962, lib modules: 222 → 223, test files: 147 → 148
- src/relationship/related_methods.rs (EntityWorldMut::add_one_related + detach_all_related + despawn_related + despawn_children + insert_recursive + remove_recursive + EntityCommands::with_related + with_related_entities + Relationship<generic = relationship_id i32> + Fn<bundle> =bundle_id i32 + BFS-tree-descendants traversal + restore of accidentally-deleted lib/*.test.sa artifacts) ✓


## Batch 99 — system_trait_extras (2026-07-03)
- lib/system_trait_extras.sla: System trait gaps (is_send + system_type + refresh_hotpatch + queue_deferred + check_change_tick + default_system_sets add/lookup + get_last_run/set_last_run + run_readonly + run_without_applying_deferred) — mirrors src/system/system.rs (gaps not in lib/system_trait.sla)
- 20 tests — test_ecs_lib_system_trait_extras_isolated.sla
- Tests: 2962 → 2982, lib modules: 223 → 224, test files: 148 → 149
- src/system/system.rs (System::is_send + system_type + refresh_hotpatch + queue_deferred + check_change_tick + default_system_sets + get_last_run + set_last_run + run_readonly + run_without_applying_deferred + TypeId-as-i64 model + non_send-bit-is_send negation) ✓


## Batch 100 — relationship_replace_insert (2026-07-03)
- lib/relationship_replace_insert.sla: insert_related + replace_related + replace_related_with_difference — mirrors src/relationship/related_methods.rs (reorder/replace-with-difference pub fns not in lib/relationship_related_methods.sla + lib/relationship_methods_extras.sla)
- 16 tests — test_ecs_lib_relationship_replace_insert_isolated.sla
- Tests: 2982 → 2998, lib modules: 224 → 225, test files: 149 → 150
- src/relationship/related_methods.rs (EntityWorldMut::insert_related + replace_related + replace_related_with_difference + OrderedRelationshipSourceCollection place/place_most_recent mirror + EntityHashSet collect/set-difference + newly_related ⊂ relate invariant + keep-existing-collection-in-place-on-empty-diff) ✓


## Batch 101 — relationship_source_collection_ordered (2026-07-03)
- lib/relationship_source_collection_ordered.sla: OrderedRelationshipSourceCollection trait surface (insert/remove_at/insert_stable/remove_at_stable/sort/insert_sorted/place/place_most_recent/push_front) + with_capacity/reserve/shrink_to_fit/extend_from_iter/source_to_remove_before_add — mirrors src/relationship/relationship_source_collection.rs (gaps not in lib/relationship_source_collection.sla)
- 29 tests — test_ecs_lib_relationship_source_collection_ordered_isolated.sla
- Tests: 2998 → 3027, lib modules: 225 → 226, test files: 150 → 151
- src/relationship/relationship_source_collection.rs (OrderedRelationshipSourceCollection::insert/remove_at/insert_stable/remove_at_stable/sort/insert_sorted/place_most_recent/place + push_front + RelationshipSourceCollection::with_capacity/reserve/shrink_to_fit/extend_from_iter/source_to_remove_before_add/is_empty) ✓


## Batch 102 — entity_generation_extras (2026-07-03)
- lib/entity_generation_extras.sla: EntityGeneration gap surface (FIRST + to_bits/from_bits + after_versions wrapping_add + after_versions_and_could_alias overflowing_add + cmp_approx Ordering) + Entity::try_from_bits + EntityIndex::from_raw_u32 (NonMaxU32 validation) — mirrors src/entity/mod.rs (gaps not in lib/entity.sla)
- 25 tests — test_ecs_lib_entity_generation_extras_isolated.sla
- Tests: 3027 → 3052, lib modules: 226 → 227, test files: 151 → 152
- src/entity/mod.rs (EntityGeneration::FIRST/to_bits/from_bits/after_versions/after_versions_and_could_alias/cmp_approx + Entity::try_from_bits + EntityIndex::from_raw_u32 + DIFF_MAX=2^31 cmp_approx boundary + NonMaxU32 rejects u32::MAX + u32-wrapping arithmetic as i64-modulo-2^32) ✓


## Batch 103 — entity_allocator_extras (2026-07-03)
- lib/entity_allocator_extras.sla: EntityAllocator pub-surface (alloc/free/free_many/alloc_many/build_remote_allocator/has_remote_allocator/restart) + RemoteAllocatorProxy snapshot — mirrors src/entity/mod.rs EntityAllocator 706-810 (gaps not in lib/remote_allocator.sla)
- 18 tests — test_ecs_lib_entity_allocator_extras_isolated.sla
- Tests: 3052 → 3070, lib modules: 227 → 228, test files: 152 → 153
- src/entity/mod.rs (EntityAllocator::alloc/free/free_many/alloc_many/build_remote_allocator/has_remote_allocator/restart + RemoteAllocator generation-stability check + AllocEntitiesIterator-emulated single-result + LIFO recycled-stack alloc) ✓
