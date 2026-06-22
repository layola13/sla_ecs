# sla_ecs Core ECS Implementation Plan

## Goal

Build `sla_ecs` into a real Sla/SA ECS runtime that matches the core semantics shown in Bevy ECS' README: entities, components, world storage, resources, queries, systems, schedules, messages, and change detection. This is not a documentation-only task and not a fixed-capacity demo. Compiler or Sla syntax gaps must be fixed when they block the Bevy-shaped API.

The first deliverable is **Bevy Core ECS parity**, not the entire `bevy_ecs` crate. Full Bevy internals such as reflection and true parallel executors are later phases unless they block README-level semantics. Observers, deferred command queues, observer schedules/system-param adapters, library-owned metadata descriptors, generic relationship bookkeeping/traversal, generic relationship command queues and related spawner helpers, typed relationship facades, typed one-to-one facades, relationship difference replacement, and the canonical hierarchy relationship including `Children` ordering helpers now have verified `sla_ecs` slices, but broader derive/macro generation remains pending.

## Current Baseline

- The current tree contains the reusable `lib/` runtime and verified `examples/`; the old `src/` prototype directory is not present on disk.
- `lib/` now contains reusable Entity, dynamic Entity allocator, fixed ComponentStore, Vec-backed DynamicComponentStore, Vec-backed SparseComponentStore, component metadata registry, registry-driven component id membership, registry archetype grouping, archetype-backed homogeneous value storage plus Commands/Schedule/system-param adapters, archetype table-row homogeneous value storage plus Commands/Schedule/system-param adapters, archetype table-row type-erased heterogeneous value storage plus bundle helpers and pair-mut `Without` filtering, table-erased relationship wrapper/commands/schedule/system-param adapters with synchronized entity allocation and relationship-aware access tracking, table-erased observer wrapper/commands/schedule/system-param adapters with component lifecycle, targeted entity event triggering, component/event access tracking, and no-conflict batch planning, `ecs_metadata.sla` library-owned descriptors for stable numeric ids, explicit drop-function plumbing, resources/messages/events, and relationship shapes, registry-bound typed A/B value ownership, registry-owned homogeneous typed multi-column storage, registry-owned type-erased heterogeneous component storage, registry-owned deferred Commands and sequential Schedule for homogeneous and erased registry worlds, resources, typed and type-erased messages, type-erased event observers, generic relationship bookkeeping with traversal and difference replacement, deferred generic relationship commands plus related spawner helpers, a typed hierarchy facade and deferred hierarchy commands backed by the generic relationship runtime, a typed one-to-one relationship facade, Bevy-style hierarchy relationships with ordering helpers, fixed-capacity World, and dynamic Vec-backed DynamicWorld.
- `examples/archetype_system_param_demo.sla`, `examples/archetype_schedule_commands_demo.sla`, `examples/archetype_value_world_demo.sla`, `examples/table_value_world_demo.sla`, `examples/table_erased_world_demo.sla`, `examples/table_erased_schedule_commands_demo.sla`, `examples/table_erased_system_param_demo.sla`, `examples/table_erased_auto_metadata_demo.sla`, `examples/table_erased_bundle_demo.sla`, `examples/table_erased_observer_demo.sla`, `examples/table_erased_observer_system_param_demo.sla`, `examples/ecs_metadata_descriptor_demo.sla`, `examples/bevy_readme_parity_table_erased_demo.sla`, `examples/table_erased_relationship_demo.sla`, `examples/table_erased_relationship_commands_demo.sla`, `examples/table_erased_relationship_system_param_demo.sla`, `examples/table_erased_derive_component_demo.sla`, `examples/message_derive_multi_demo.sla`, `examples/event_observer_demo.sla`, `examples/relationship_runtime_demo.sla`, `examples/relationship_commands_demo.sla`, `examples/relationship_one_to_one_demo.sla`, `examples/relationship_multi_kind_demo.sla`, `examples/hierarchy_generic_relationship_demo.sla`, `examples/hierarchy_commands_demo.sla`, `examples/hierarchy_relationship_demo.sla`, `examples/table_system_param_demo.sla`, `examples/world_movement_demo.sla`, `examples/dynamic_world_movement_demo.sla`, `examples/dynamic_world3_bundle_demo.sla`, `examples/dynamic_schedule_demo.sla`, `examples/dynamic_resource_change_demo.sla`, `examples/dynamic_commands_demo.sla`, `examples/registry_archetype_demo.sla`, `examples/registry_world_demo.sla`, `examples/registry_typed_world_demo.sla`, `examples/registry_value_world_demo.sla`, `examples/registry_erased_world_demo.sla`, `examples/registry_erased_schedule_commands_demo.sla`, and `examples/bevy_readme_parity_demo.sla` pass with the installed Sla dev plugin.
- `lib/world_dynamic.sla` removes the old fixed-capacity limit for the current two-component owner shape and verifies dynamic entities, components, change ticks, resources, messages, pair query, and writeback.
- `lib/world_dynamic.sla` and `lib/world_archetype_value.sla` track resource added/changed ticks and expose `Res<T>` / `ResMut<T>` wrappers for Bevy-style resource systems. `lib/resource_erased.sla` now adds the Bevy resource identity rule directly: multiple resource types coexist in one owner, with at most one value per `resource_type_id()` impl metadata id.
- `lib/world_dynamic3.sla` extends the typed dynamic owner to three component columns and verifies bundle spawn, triple query, third-component filters, and C-component change detection.
- `lib/query_dynamic.sla` adds verified Bevy-shaped query wrappers for the current dynamic A/B world: `Query<T>`, `Query<Mut<T>>`, entity-bearing items, pair mutable items, `With/Without/Added/Changed`, `for in`, and explicit `Mut<T>` writeback.
- `lib/schedule_dynamic.sla` adds verified Bevy-shaped sequential scheduling for the current dynamic A/B world: stored `fn(World) -> World` systems, `schedule_default`, `schedule_add_systems`, `schedule_run`, and access conflict tracking.
- `lib/commands_dynamic.sla` adds verified Bevy-style deferred commands for the current dynamic A/B world: reserve entity, insert A/B, despawn, insert resource, write message, ordered apply, and clear-after-apply.
- `lib/world_registry.sla` adds verified registry-driven arbitrary component id membership, With/Without entity queries, Added/Changed ticks, despawn cleanup, and `for in` entity iteration.
- `lib/world_registry_typed.sla` binds typed A/B value stores to registered component ids and uses `RegistryWorld` membership/ticks as the source of truth. `lib/world_registry_erased.sla` adds a single registry-owned type-erased value store spanning multiple concrete component types.
- `lib/world_registry_store.sla` owns arbitrary component value columns for a homogeneous Sla value type `T`, removing the fixed A/B value-column shape for same-type component groups; registry value Commands and Schedule now run over component ids.
- `lib/commands_registry_erased.sla` and `lib/schedule_registry_erased.sla` move deferred mutation and sequential scheduling onto the type-erased registry world.
- The table-erased runtime now has verified runtime type-id metadata lookup helpers for insert/get/query/filter/added/changed/remove, component bundle spawn/insert helpers, deferred Commands with explicit spawn-location propagation, schedule access declarations, and system-param adapters. The main heterogeneous table-row path covers `Query<Entity>`, query-level and world-level `single`/`get`/ordered `get_many`/`iter_many` helpers, K=2..10 query combination helpers, `With`, `Without`, `Added`, `Changed`, and `Spawned` value/entity query filters, pair/pair-mut filtered queries, Bevy README-style `(With<T>, Without<U>)` tuple filters, binary `Or<...>` and `And` filter helpers for `With`/`Without`/`Added`/`Changed`, optional component query data in either tuple slot, optional tuple query data, `Query<(A, Has<B>)>` query data, `SpawnDetails` tick and explicit `spawned_by` metadata, binary/ternary/quaternary `AnyOf` query data, entity/filter/query-data query-resource system params, `Single`, `Option<Single>`, and `Populated` system-param gates, and filtered/spawned pair-mut system params, including auto type-id variants. Component/resource/message/event metadata is currently supplied by ordinary `sla_ecs` `impl` methods, while `@derive(...)` remains only a language-neutral annotation marker until a generic macro/derive facility exists.
- `sa_plugin_sla` remains part of the implementation surface when Sla syntax/codegen blocks ECS semantics, but it must stay engine-agnostic. Recent fixes include wildcard `.sla` imports, nested generic `>>` parsing, `Vec<T>` index assignment, `Vec` field method-call cleanup, generic impl protocol monomorphization for `for in`, function pointer value codegen for schedules and observers, top-level scalar const codegen, global scalar const call-argument cleanup across loop branches, field comparison after dot access, nested indexed length expressions such as `len(world.archetypes[archetype_slot].entity_ids)`, language-neutral `@derive(...)` annotations, and expanded relative `.sai` / `.sal` import resolution. Bevy/ECS metadata belongs in `sla_ecs`, not in compiler keyword branches.

## Implementation Phases

### Phase 1: Unblock Sla Compiler

Fix the compiler issues needed by the reusable ECS layer before expanding runtime code.

- Add a regression for `array-of-struct` chained field access inside branches and loops.
- Fix codegen cleanup so temporaries from expressions like `store.values[i].field` are released before branch merge.
- Verify the existing `examples/movement_demo.sla` passes.
- Follow the existing Bevy syntax-gap decision docs: do not make Rust `mut` the core ECS write model. Use `Mut<T>` / `ResMut<T>` wrappers plus Referee write inference. Parse/strip Rust `mut` only as compatibility sugar when necessary for copied examples.
- Prioritize the documented Bevy blockers: operator overload, struct update `..default()`, `Default` derive, `where` bounds, `Mut<T>` wrappers, trait default methods, associated types only if a chosen API slice truly requires them.

### Phase 2: Reusable Core Runtime

Replace the fixed-demo center of gravity with reusable `lib/` modules.

- Implement Bevy-style `Entity` identity with index + generation, `PLACEHOLDER`, bit conversion helpers, stale entity rejection, spawn/despawn generation bumping, and free-list reuse.
- Implement dynamic component stores using `sa_std Vec` where possible; keep fixed-array fallback only for compiler-gap isolation tests.
- Add component registration by Sla type metadata and storage kind: table by default, sparse-set when requested.
- Add `sla_ecs`-owned metadata descriptor helpers for explicit component/resource/message/event/relationship declarations while keeping automatic derive/macro generation out of the compiler until a general language mechanism exists.
- Implement generic Bevy relationship bookkeeping in `sla_ecs`: relationship kind metadata, source-of-truth source entries, synchronized target source collections, one-to-many and one-to-one targets, self-reference policy, replacement/detach, `replace_related_with_difference`, and linked despawn.
- Implement generic relationship traversal helpers in `sla_ecs`: ancestors, root ancestor, breadth-first descendants, depth-first descendants, siblings, leaves, and query contains/len/at helpers.
- Implement generic Bevy-style relationship command queues in `sla_ecs`: deferred spawn-related, add, ordered insert, remove, replace, difference replacement, detach-all, despawn-related, and linked despawn over `RelationshipWorld`.
- Implement typed relationship facades in `sla_ecs` over the generic relationship runtime, proving concrete relationship API names can be library-owned wrappers rather than compiler keywords.
- Integrate generic relationships with table-erased component storage in `sla_ecs`: synchronized entity allocation/free-list ordering, relationship-aware linked despawn cleanup, and ordered commands that mix component inserts, relationship mutations, and despawn.
- Add schedule and system-param support for table-erased relationship worlds: component + relationship access tracking, batch planning, query params, relationship params, Commands params, resources, and messages.
- Add schedule and system-param support for table-erased observer worlds: component + event access tracking, batch planning, pair-mut query params, Commands params, resources, messages, and explicit event-trigger params.
- Implement the canonical Bevy hierarchy relationship in `sla_ecs`: `ChildOf` source relation, synchronized `Children` target collection, reparenting, detach, ordered insert/replace, `replace_children_with_difference`, `Children` swap/sort helpers, traversal helpers, and linked recursive child despawn.
- Implement `World` as the owner of entity locations, component storage, resource storage, change ticks, and message queues.
- Keep all mutation expressed through SA-safe linear value flow or verified exclusive access paths.

### Phase 3: Query, System, Schedule

Expose Bevy-shaped APIs over the runtime.

- Support query forms needed by Bevy README examples using the SA-native wrapper shape: `Query<T>`, `Query<Entity>`, `Query<Mut<T>>`, `Query<(Entity, T)>`, `Query<(Mut<A>, B)>`, `With<T>`, `Without<T>`, `Added<T>`, `Changed<T>`, and `Spawned`. Rust `&T` / `&mut T` forms are compatibility inputs only, not the internal model. The table-erased path now has these value/entity filters, query-resource system-param adapters, pair/pair-mut filtered query forms, the README tuple-filter shape `(With<T>, Without<U>)`, binary `Or` and `And` filter coverage, query `single`/`get`/ordered `get_many`/`iter_many` access helpers, Bevy `Single` / `Option<Single>` / `Populated` system-param gates, K=2..10 query combination helpers, optional component query data in either tuple slot, optional tuple query data, `Has<T>` query data, `SpawnDetails` tick and explicit `spawned_by` metadata, deferred Commands spawn-location propagation, and binary/ternary/quaternary `AnyOf` query data; remaining query work is arbitrary generated query combinations beyond the current K=2..10 helpers, tuple/query-data arity and nesting beyond `AnyOf4` plus current hand-written shapes, more generated combinator coverage beyond the current hand-written query-data/filter shapes, and automatic caller capture.
- Implement query iteration so each matching live entity appears once, stale/despawned entities are excluded, and writeback updates the underlying component storage.
- Implement system adapters so Bevy-shaped system functions lower to the current Sla-safe execution model.
- Implement `Schedule::default`, `add_systems`, and sequential `run`; track read/write component sets for conflict detection and future parallel execution.

### Phase 4: Resources, Messages, Examples

Complete README-level Bevy concepts and examples.

- Implement unique typed resources with insert/get/get_mut/remove semantics.
- Implement `Messages<T>`, `MessageWriter<T>`, and `MessageReader<T>` with per-reader cursor behavior.
- Integrate observers with the table-erased world path: targeted entity events plus component lifecycle add/insert/replace/remove/despawn events, including deferred command apply semantics.
- Add Bevy README parity examples: movement, resources/time, query filters, change detection, messages, and schedule pipeline.
- Keep old `src/` prototype demos passing until the new `lib/` examples supersede them.

### Phase 5: Documentation and Progress

Update docs only after behavior is implemented and verified.

- Rewrite `README.md` around the actual reusable API, not the old prototype-only layout.
- Update `progress.md` with verified test counts and known limitations.
- Keep `tasks.md` current: every completed implementation task must be checked off when it lands.

## Acceptance Criteria

- All current `lib/*.sla` and `examples/*.sla` pass through `sa sla test` and exercise the public ECS API rather than private demo-specific storage.
- If old `src/*.sla` prototype sources are restored, they must either pass or be intentionally superseded by equivalent `lib/`/`examples/` coverage.
- Compiler fixes have focused regression tests under `sa_plugin_sla/tests/`.
- README does not claim support for Bevy features that are not implemented.
