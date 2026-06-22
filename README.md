# sla_ecs

SA-native Entity-Component-System runtime written in Sla.

The project is moving from fixed demo prototypes toward Bevy Core ECS parity.
Current reusable infrastructure lives in `lib/`; verified executable examples live
in `examples/`.

## Architecture

An ECS framework built for SA's linear ownership model and Referee safety system. No `mut` keyword — write access is expressed through linear value passing (`fn(World) -> World`).

### Design Principles

- **Linear World** — systems take World by value, return World
- **SoA Storage** — struct-of-arrays layout for cache-friendly iteration
- **For-In Protocol** — query iteration via `iter_len`/`iter_at` methods
- **Typed Queries** — `Query<T>` and `Mut<T>` wrappers with explicit writeback instead of Rust `mut` as the core model
- **Sequential Systems** — systems compose as `let w1 = sys_a(world); let w2 = sys_b(w1);`

### Capacity

`lib/store.sla` and `lib/world.sla` still use fixed 16-slot arrays as a
compatibility/regression layer. The dynamic path is `lib/entity_dynamic.sla`,
`lib/dyn_store.sla`, `lib/sparse_store.sla`, and `lib/world_dynamic.sla`; it is
`sa_std Vec`-backed and has verified growth beyond the old 16-entity/component
cap.

## Components

- `Position { x: i32, y: i32 }`
- `Velocity { x: i32, y: i32 }`
- `Health { current: i32, max: i32 }`
- `Damage { amount: i32, target_id: i32 }`

## Systems

| System | Description |
|--------|-------------|
| `movement_system` | Applies velocity to position for matching entities |
| `damage_system` | Reduces health by damage events, clears damage queue |
| `death_system` | Removes entities with 0 HP (swap-remove) |
| `heal_system` | Regenerates 1 HP per tick up to max |

## Files

```
lib/
├── entity.sla        — Reusable Entity handle + allocator, generation checks, bit roundtrip
├── entity_dynamic.sla — Vec-backed dynamic entity allocator with live/stale checks
├── store.sla         — Generic fixed-capacity ComponentStore<T>
├── dyn_store.sla     — Generic Vec-backed table-style DynamicComponentStore<T>
├── sparse_store.sla  — Generic Vec-backed SparseComponentStore<T>
├── component.sla     — Component registry metadata: table default, sparse-set opt-in
├── component_metadata.sal — ECS component metadata ABI constants
├── component_metadata.sai — ECS component metadata interface contract placeholder
├── ecs_metadata.sla — sla_ecs-owned metadata descriptors for stable ids, explicit drop functions, resources/messages/events, and relationships
├── resource_erased.sla — Type-erased multi-resource owner keyed by `resource_type_id()` impl metadata
├── world_registry.sla — Registry-driven arbitrary component id membership, filters, and ticks
├── archetype_registry.sla — RegistryWorld archetype signatures and entity locations
├── world_archetype_value.sla — Archetype-backed homogeneous value storage, query filters, resources, and messages
├── world_table_value.sla — Archetype table-row homogeneous value storage with row migration and query filters
├── commands_table_value.sla — TableValueWorld deferred Commands with table-row migration
├── schedule_table_value.sla — TableValueWorld sequential Schedule with access tracking
├── system_param_table_value.sla — TableValueWorld query/resource/Commands/ResMut/message system-param adapters
├── commands_archetype_value.sla — ArchetypeValueWorld deferred Commands with migration
├── schedule_archetype_value.sla — ArchetypeValueWorld sequential Schedule with access tracking
├── system_param_archetype_value.sla — ArchetypeValueWorld query/resource/Commands/ResMut/message system-param adapters
├── world_registry_typed.sla — Registry-bound typed A/B value owner and queries
├── world_registry_store.sla — Registry-owned arbitrary homogeneous typed value columns with joins
├── world_registry_erased.sla — Registry-owned type-erased heterogeneous component columns
├── world_table_erased.sla — Archetype table-row type-erased heterogeneous component storage with type-id metadata lookup, `Query<Entity>`, query `single`/`get`/ordered `get_many`/`iter_many` helpers, K=2..10 query combinations, query filters, binary `Or`/`And` filters, `Spawned` filters, `SpawnDetails::spawned_by` metadata, `Option`/`Has` query data, direct and nested `AnyOf` query data up to four branches, and optional tuple query data
├── world_table_erased_relationship.sla — TableErasedWorld + RelationshipWorld wrapper with synchronized entity allocation and linked despawn
├── world_table_erased_observer.sla — TableErasedWorld + erased observer wrapper with component lifecycle and targeted entity events
├── bundle_table_erased.sla — TableErasedWorld component bundle constructors plus spawn/insert helpers
├── commands_registry_erased.sla — RegistryErasedWorld deferred Commands carrying erased payloads
├── schedule_registry_erased.sla — RegistryErasedWorld sequential Schedule with component-id access tracking
├── commands_table_erased.sla — TableErasedWorld deferred Commands carrying erased payloads, including type-id insert helpers
├── commands_table_erased_relationship.sla — Ordered table-erased component + indexed/remove/detach/replace relationship/resource/message commands
├── commands_table_erased_observer.sla — Deferred table-erased observer commands with lifecycle/event triggering during apply
├── schedule_table_erased_relationship.sla — TableErasedRelationshipWorld Schedule with component/relationship access tracking and batch planning
├── system_param_table_erased_relationship.sla — TableErasedRelationshipWorld query/relationship/Commands/ResMut/message system-param adapters
├── schedule_table_erased_observer.sla — TableErasedObserverWorld Schedule with component/event access tracking and batch planning
├── system_param_table_erased_observer.sla — TableErasedObserverWorld entity/filter/query-data/Single/Populated/Commands/ResMut/message/event-trigger system-param adapters
├── schedule_table_erased.sla — TableErasedWorld Schedule with type-id access tracking and parallel batch planning
├── system_param_table_erased.sla — TableErasedWorld entity/filter/query-data/Single/Populated/resource/Commands/ResMut/message system-param adapters, including type-id helpers
├── resource.sla      — Generic ResourceSlot<T>
├── messages.sla      — Generic fixed-capacity Messages<T>, MessageWriter<T>, and reader cursor
├── messages_erased.sla — Type-erased multi-message channels keyed by `message_type_id()` impl metadata
├── event_observer_erased.sla — Type-erased Event observer registry with immediate trigger support
├── relationship.sla — Generic Bevy-style relationship runtime with one-to-many, one-to-one, traversal, difference replacement, self-policy, and linked despawn
├── commands_relationship.sla — Deferred RelationshipWorld commands and related spawner helpers for spawn/add/insert/remove/replace/detach/despawn relation mutations
├── hierarchy_relationship_adapter.sla — Typed ChildOf/Children-style facade backed by generic RelationshipWorld, including traversal helpers
├── hierarchy_commands.sla — Deferred commands for the typed hierarchy facade
├── relationship_one_adapter.sla — Typed one-to-one relationship facade backed by generic RelationshipWorld
├── hierarchy.sla    — Bevy-style ChildOf/Children relationship runtime with traversal, Children swap/sort helpers, and recursive despawn
├── world.sla         — Generic fixed-capacity World<A, B, R, M> owner + pair query/writeback
├── world_dynamic.sla — Vec-backed DynamicWorld<A, B, R, M> owner + pair query/writeback
├── world_dynamic3.sla — Vec-backed DynamicWorld3<A, B, C, R, M> with triple bundle/query/filter support
├── query_dynamic.sla — Bevy-shaped DynamicWorld Query<T>, Mut<T>, filters, and writeback
├── schedule_dynamic.sla — Sequential Schedule with stored system functions and access tracking
├── commands_dynamic.sla — Deferred Commands queue for reserve/insert/despawn/resource/message apply
├── schedule_registry_value.sla — RegistryValueWorld sequential Schedule with component-id access tracking
└── commands_registry_value.sla — RegistryValueWorld deferred Commands keyed by component id

examples/
├── archetype_system_param_demo.sla — Archetype-backed query/resource/message param demo
├── archetype_schedule_commands_demo.sla — Archetype-backed Commands + Schedule pipeline demo
├── archetype_value_world_demo.sla    — Archetype-backed value movement/migration demo
├── table_value_world_demo.sla      — Archetype table-row value migration demo
├── table_erased_world_demo.sla     — Type-erased heterogeneous archetype table-row demo
├── table_erased_schedule_commands_demo.sla — Type-erased table-row Commands + Schedule pipeline demo
├── table_erased_system_param_demo.sla — Type-erased table-row system-param demo
├── table_erased_auto_metadata_demo.sla — Type-id metadata lookup demo over the table-erased path
├── table_erased_bundle_demo.sla — Component bundle spawn/insert demo over the table-erased path
├── bevy_readme_parity_table_erased_demo.sla — Bevy README flow over the table-erased full stack
├── table_erased_observer_demo.sla — Table-erased component lifecycle and targeted observer demo
├── table_erased_relationship_demo.sla — Table-erased component storage plus generic relationship wrapper demo
├── table_erased_relationship_commands_demo.sla — Ordered table-erased component + relationship collection commands demo
├── table_erased_relationship_system_param_demo.sla — Table-erased relationship schedule/system-param demo
├── table_erased_observer_system_param_demo.sla — Table-erased observer schedule/system-param demo
├── ecs_metadata_descriptor_demo.sla — Library-owned metadata descriptor demo for components/resources/messages/events/relationships
├── table_erased_derive_component_demo.sla — Project-level component marker + `impl` metadata demo
├── resource_derive_multi_demo.sla — Resource identity metadata demo
├── message_derive_multi_demo.sla — Multi-channel message metadata demo
├── event_observer_demo.sla       — Immediate observer trigger metadata demo
├── relationship_runtime_demo.sla — Generic relationship runtime demo for many/one-to-one/difference/self/linked semantics
├── relationship_commands_demo.sla — Deferred generic relationship command queue demo
├── relationship_one_to_one_demo.sla — Typed one-to-one relationship facade demo
├── relationship_multi_kind_demo.sla — Multiple relationship kinds in one RelationshipWorld demo
├── hierarchy_generic_relationship_demo.sla — Typed hierarchy facade over the generic relationship runtime
├── hierarchy_commands_demo.sla — Deferred typed hierarchy command facade demo
├── hierarchy_relationship_demo.sla — Parent/child relationship traversal, sorting, difference replacement, and recursive despawn demo
├── table_system_param_demo.sla      — Table-row schedule/system-param/Commands demo
├── world_movement_demo.sla        — Fixed World movement/resource/message demo
├── dynamic_world_movement_demo.sla — DynamicWorld demo with 20 entities
├── dynamic_world3_bundle_demo.sla  — DynamicWorld3 bundle/query/filter demo
├── dynamic_schedule_demo.sla       — DynamicWorld Schedule pipeline demo
├── dynamic_resource_change_demo.sla — DynamicWorld Res/ResMut change detection demo
├── dynamic_commands_demo.sla        — DynamicWorld deferred Commands demo
├── bevy_readme_parity_demo.sla      — Combined Bevy README ECS flow over registry APIs
├── registry_archetype_demo.sla       — Archetype signature migration demo
├── registry_world_demo.sla          — Arbitrary component id registry/membership demo
├── registry_typed_world_demo.sla    — Registry-bound typed value world demo
├── registry_value_world_demo.sla    — Registry-owned multi-column typed value join demo
├── registry_erased_world_demo.sla   — Type-erased heterogeneous component value demo
└── registry_erased_schedule_commands_demo.sla — Erased Commands + Schedule pipeline demo
```

## Running

```bash
SA_PLUGIN_DEV=1 sa sla test lib/entity.sla
SA_PLUGIN_DEV=1 sa sla test lib/entity_dynamic.sla
SA_PLUGIN_DEV=1 sa sla test lib/store.sla
SA_PLUGIN_DEV=1 sa sla test lib/dyn_store.sla
SA_PLUGIN_DEV=1 sa sla test lib/sparse_store.sla
SA_PLUGIN_DEV=1 sa sla test lib/component.sla
SA_PLUGIN_DEV=1 sa sla test lib/ecs_metadata.sla
SA_PLUGIN_DEV=1 sa sla test lib/resource_erased.sla
SA_PLUGIN_DEV=1 sa sla test lib/world_registry.sla
SA_PLUGIN_DEV=1 sa sla test lib/archetype_registry.sla
SA_PLUGIN_DEV=1 sa sla test lib/world_archetype_value.sla
SA_PLUGIN_DEV=1 sa sla test lib/world_table_value.sla
SA_PLUGIN_DEV=1 sa sla test lib/commands_table_value.sla
SA_PLUGIN_DEV=1 sa sla test lib/schedule_table_value.sla
SA_PLUGIN_DEV=1 sa sla test lib/system_param_table_value.sla
SA_PLUGIN_DEV=1 sa sla test lib/commands_archetype_value.sla
SA_PLUGIN_DEV=1 sa sla test lib/schedule_archetype_value.sla
SA_PLUGIN_DEV=1 sa sla test lib/system_param_archetype_value.sla
SA_PLUGIN_DEV=1 sa sla test lib/world_registry_typed.sla
SA_PLUGIN_DEV=1 sa sla test lib/world_registry_store.sla
SA_PLUGIN_DEV=1 sa sla test lib/world_registry_erased.sla
SA_PLUGIN_DEV=1 sa sla test lib/world_table_erased.sla
SA_PLUGIN_DEV=1 sa sla test lib/world_table_erased_relationship.sla
SA_PLUGIN_DEV=1 sa sla test lib/world_table_erased_observer.sla
SA_PLUGIN_DEV=1 sa sla test lib/bundle_table_erased.sla
SA_PLUGIN_DEV=1 sa sla test lib/commands_registry_erased.sla
SA_PLUGIN_DEV=1 sa sla test lib/schedule_registry_erased.sla
SA_PLUGIN_DEV=1 sa sla test lib/commands_table_erased.sla
SA_PLUGIN_DEV=1 sa sla test lib/commands_table_erased_relationship.sla
SA_PLUGIN_DEV=1 sa sla test lib/commands_table_erased_observer.sla
SA_PLUGIN_DEV=1 sa sla test lib/schedule_table_erased_relationship.sla
SA_PLUGIN_DEV=1 sa sla test lib/system_param_table_erased_relationship.sla
SA_PLUGIN_DEV=1 sa sla test lib/schedule_table_erased_observer.sla
SA_PLUGIN_DEV=1 sa sla test lib/system_param_table_erased_observer.sla
SA_PLUGIN_DEV=1 sa sla test lib/schedule_table_erased.sla
SA_PLUGIN_DEV=1 sa sla test lib/system_param_table_erased.sla
SA_PLUGIN_DEV=1 sa sla test lib/resource.sla
SA_PLUGIN_DEV=1 sa sla test lib/messages.sla
SA_PLUGIN_DEV=1 sa sla test lib/messages_erased.sla
SA_PLUGIN_DEV=1 sa sla test lib/event_observer_erased.sla
SA_PLUGIN_DEV=1 sa sla test lib/relationship.sla
SA_PLUGIN_DEV=1 sa sla test lib/commands_relationship.sla
SA_PLUGIN_DEV=1 sa sla test lib/hierarchy_relationship_adapter.sla
SA_PLUGIN_DEV=1 sa sla test lib/hierarchy_commands.sla
SA_PLUGIN_DEV=1 sa sla test lib/relationship_one_adapter.sla
SA_PLUGIN_DEV=1 sa sla test lib/hierarchy.sla
SA_PLUGIN_DEV=1 sa sla test lib/world.sla
SA_PLUGIN_DEV=1 sa sla test lib/world_dynamic.sla
SA_PLUGIN_DEV=1 sa sla test lib/world_dynamic3.sla
SA_PLUGIN_DEV=1 sa sla test lib/query_dynamic.sla
SA_PLUGIN_DEV=1 sa sla test lib/schedule_dynamic.sla
SA_PLUGIN_DEV=1 sa sla test lib/commands_dynamic.sla
SA_PLUGIN_DEV=1 sa sla test lib/schedule_registry_value.sla
SA_PLUGIN_DEV=1 sa sla test lib/commands_registry_value.sla
SA_PLUGIN_DEV=1 sa sla test examples/archetype_system_param_demo.sla
SA_PLUGIN_DEV=1 sa sla test examples/archetype_schedule_commands_demo.sla
SA_PLUGIN_DEV=1 sa sla test examples/archetype_value_world_demo.sla
SA_PLUGIN_DEV=1 sa sla test examples/table_value_world_demo.sla
SA_PLUGIN_DEV=1 sa sla test examples/table_erased_world_demo.sla
SA_PLUGIN_DEV=1 sa sla test examples/table_erased_schedule_commands_demo.sla
SA_PLUGIN_DEV=1 sa sla test examples/table_erased_system_param_demo.sla
SA_PLUGIN_DEV=1 sa sla test examples/table_erased_auto_metadata_demo.sla
SA_PLUGIN_DEV=1 sa sla test examples/table_erased_bundle_demo.sla
SA_PLUGIN_DEV=1 sa sla test examples/table_erased_observer_demo.sla
SA_PLUGIN_DEV=1 sa sla test examples/table_erased_relationship_demo.sla
SA_PLUGIN_DEV=1 sa sla test examples/table_erased_relationship_commands_demo.sla
SA_PLUGIN_DEV=1 sa sla test examples/table_erased_relationship_system_param_demo.sla
SA_PLUGIN_DEV=1 sa sla test examples/table_erased_observer_system_param_demo.sla
SA_PLUGIN_DEV=1 sa sla test examples/ecs_metadata_descriptor_demo.sla
SA_PLUGIN_DEV=1 sa sla test examples/bevy_readme_parity_table_erased_demo.sla
SA_PLUGIN_DEV=1 sa sla test examples/table_erased_derive_component_demo.sla
SA_PLUGIN_DEV=1 sa sla test examples/resource_derive_multi_demo.sla
SA_PLUGIN_DEV=1 sa sla test examples/message_derive_multi_demo.sla
SA_PLUGIN_DEV=1 sa sla test examples/event_observer_demo.sla
SA_PLUGIN_DEV=1 sa sla test examples/relationship_runtime_demo.sla
SA_PLUGIN_DEV=1 sa sla test examples/relationship_commands_demo.sla
SA_PLUGIN_DEV=1 sa sla test examples/relationship_one_to_one_demo.sla
SA_PLUGIN_DEV=1 sa sla test examples/relationship_multi_kind_demo.sla
SA_PLUGIN_DEV=1 sa sla test examples/hierarchy_generic_relationship_demo.sla
SA_PLUGIN_DEV=1 sa sla test examples/hierarchy_commands_demo.sla
SA_PLUGIN_DEV=1 sa sla test examples/hierarchy_relationship_demo.sla
SA_PLUGIN_DEV=1 sa sla test examples/table_system_param_demo.sla
SA_PLUGIN_DEV=1 sa sla test examples/bevy_readme_parity_demo.sla
SA_PLUGIN_DEV=1 sa sla test examples/world_movement_demo.sla
SA_PLUGIN_DEV=1 sa sla test examples/dynamic_world_movement_demo.sla
SA_PLUGIN_DEV=1 sa sla test examples/dynamic_world3_bundle_demo.sla
SA_PLUGIN_DEV=1 sa sla test examples/dynamic_schedule_demo.sla
SA_PLUGIN_DEV=1 sa sla test examples/dynamic_resource_change_demo.sla
SA_PLUGIN_DEV=1 sa sla test examples/dynamic_commands_demo.sla
SA_PLUGIN_DEV=1 sa sla test examples/registry_archetype_demo.sla
SA_PLUGIN_DEV=1 sa sla test examples/registry_world_demo.sla
SA_PLUGIN_DEV=1 sa sla test examples/registry_typed_world_demo.sla
SA_PLUGIN_DEV=1 sa sla test examples/registry_value_world_demo.sla
SA_PLUGIN_DEV=1 sa sla test examples/registry_erased_world_demo.sla
SA_PLUGIN_DEV=1 sa sla test examples/registry_erased_schedule_commands_demo.sla
```

## Compiler Fix

This project required several Sla compiler fixes in `sa_plugin_sla`:

- `typeSize(.array)` now returns pointer size (`8`) because arrays in structs are heap-backed pointers.
- Chained array-of-struct field access such as `store.values[i].x` now releases temporary registers correctly.
- Moving a local owner into an assignment target now avoids double cleanup; scalar field reads such as `entity.id` do not move the owner.
- Nested `.sla` imports now resolve non-`.sla` imports relative to the imported file.
- Wildcard `.sla` imports are supported as `@import "path/*.sla"` and bare `@import path/*.sla`.
- `Vec<T>` index assignment is supported, including `Vec` fields used inside loops; this unblocks dynamic component writeback.
- Method-call cleanup for `Vec` fields such as `query.items.push(...)` now releases receiver temporaries correctly.
- Nested generic closes such as `Vec<Vec<i32>>` and `Vec<Pair<A, B>>` parse without spacing workarounds.
- Generic impl protocol methods now monomorphize correctly, so `impl Query<T> { iter_len/iter_at }` supports `for item in query`.
- Function pointer values can be stored and passed, which lets schedules keep real `fn(World) -> World` system adapters.
- Top-level scalar constants such as `const KIND: i32 = 1` lower correctly by inlining scalar literals at use sites; this unblocks command kind tags.
- Use-after-move diagnostics now include the consumed identifier name.
- Field comparisons and nested indexed length expressions such as `len(world.archetypes[archetype_slot].entity_ids)` lower correctly, so table-row storage can use the direct Bevy-shaped expression instead of a workaround.
- `@derive(...)` is now language-neutral in the Sla compiler: arbitrary derive names parse as annotations, but the compiler does not hard-code Bevy/ECS keywords or generate ECS metadata methods.
- ECS metadata lives in `sla_ecs` code. Component/resource/message/event type ids and component storage kind are ordinary static `impl` methods such as `Type::component_type_id()` and `Type::component_storage_kind()`.
- Engine-specific `@component(storage = "SparseSet")` compiler support was removed; sparse/table storage metadata is exposed by `sla_ecs` impl methods instead.
- Expanded relative `.sai` / `.sal` imports are resolved correctly after `.sla` import expansion, while generated `sa_std/...` imports remain global relative paths.

After changing Sla compiler features, reinstall the dev plugin:

```bash
SA_PLUGIN_DEV=1 sa plugin install --dev /home/vscode/projects/sa_plugins/sa_plugin_sla
```

## Current Gaps

- `messages.sla` now includes `MessageWriter<T>` batching plus `MessageReader<T>`-style cursor reads. `world_registry.sla` verifies arbitrary component id registration, membership, With/Without filtering, change ticks, and despawn cleanup. `world_registry_typed.sla` binds typed A/B value stores to registry component ids and uses registry ticks as the source of truth. `world_registry_store.sla` owns any number of registry component columns for a homogeneous Sla value type `T`, including pair joins, pair `Without` filters, Added/Changed queries, and pair-mut writeback. `world_registry_erased.sla` stores heterogeneous component values behind erased boxed pointers with per-component drop functions. `world_table_erased.sla` stores those heterogeneous erased values directly in archetype table columns aligned by entity row, with add/remove/despawn migration, typed queries, `Query<Entity>`, query-level and world-level `single`/`get`/ordered `get_many`/`iter_many` helpers for entity, component, pair, and pair-mut shapes, K=2..10 query combination helpers, `With`/`Without`/`Added`/`Changed`/`Spawned` filters, Bevy-shaped `(With<T>, Without<U>)` tuple filters, binary `Or` and `And` filters, `Query<(A, Option<B>)>` and `Query<(Option<A>, B)>` query data, `Query<(A, Has<B>)>` query data, `Query<(AnyOf<(A, B, C)>, Option<(D, E)>)>`-style optional tuple query data, `SpawnDetails` tick and explicit `spawned_by` metadata, binary/ternary/quaternary `AnyOf` query data, nested binary/ternary/quaternary `AnyOf` tuple query data, pair and pair-mut filtered queries, pair-mut writeback, resources, messages, cleanup, and runtime type-id metadata lookup. `commands_registry_value.sla` / `schedule_registry_value.sla`, `commands_registry_erased.sla` / `schedule_registry_erased.sla`, and `commands_table_erased.sla` / `schedule_table_erased.sla` add deferred mutation and ordered system execution over registry-owned and table-row value paths.
- `DynamicWorld<A, B, R, M>` and `DynamicWorld3<A, B, C, R, M>` remain verified typed-column compatibility steps while the registry-bound runtime matures.
- The fixed `World` remains in the tree for regression coverage while dynamic APIs mature.
- Bevy-style dynamic query wrappers, filters, `Res<T>` / `ResMut<T>`, resource change detection, system adapters, sequential schedules, and deferred `Commands` are implemented for the current A/B world shape; the registry-owned homogeneous, type-erased, and archetype-backed value paths now also have component-id queries, commands, schedules, resources/messages, and demos. `archetype_registry.sla` verifies Bevy-style entity location migration between component-signature archetypes, `world_archetype_value.sla` connects those locations to real homogeneous component value columns and tracks resource added/changed ticks, `world_table_value.sla` stores homogeneous component values directly inside archetype table rows with row migration, and `world_table_erased.sla` extends that table-row path to heterogeneous boxed component values plus type-id lookup helpers. The archetype/table/table-erased system-param paths now cover Bevy-style `With`, `Without`, `Added`, and `Changed` query-resource filters where the underlying world supports them; the table-erased path also covers `Query<Entity>` and filtered entity-query system params, query-level and world-level `single`/`get`/ordered `get_many`/`iter_many` helpers, K=2..10 query combinations, pair and pair-mut filtered query/system-param forms, the README tuple filter shape `(With<T>, Without<U>)`, binary `Or` and `And` filters, `Spawned` filters, optional component query data in either tuple slot, optional tuple query data, `Has<T>` query data, `SpawnDetails` tick and explicit `spawned_by` metadata, `Single`, `Option<Single>`, and `Populated` system-param gates, binary/ternary/quaternary `AnyOf` item-query resource params, and nested binary/ternary/quaternary `AnyOf` tuple query-data params. `world_table_erased_relationship.sla` wraps table-erased component storage with generic relationships while keeping entity allocation/free-list order synchronized, including linked despawn cleanup. `world_table_erased_observer.sla` wraps the same table-erased path with erased observers, targeted entity events, and component lifecycle events for add/insert/replace/remove/despawn. `commands_table_value.sla` / `schedule_table_value.sla` / `system_param_table_value.sla` run deferred commands, schedules, and injected params over the homogeneous table-row path; `commands_table_erased.sla` / `schedule_table_erased.sla` / `system_param_table_erased.sla` now cover deferred commands, explicit spawn-location propagation, schedules, injected params, type-id helper APIs, entity/query-data query-resource params, `Single` / `Option<Single>` / `Populated` params, filtered pair-mut params, spawned pair-mut params, tuple/AND/OR filter params, and no-conflict parallel batch planning for heterogeneous table rows. `commands_table_erased_relationship.sla` / `schedule_table_erased_relationship.sla` / `system_param_table_erased_relationship.sla` add ordered component/resource/message commands, indexed ordered relationship insertion, relationship remove/detach/replace/difference commands, explicit spawn-location propagation for root and related spawns, component+relationship access tracking, batch planning, and query/relationship/Commands/ResMut/message params over the table-erased relationship world. `commands_table_erased_observer.sla` / `schedule_table_erased_observer.sla` / `system_param_table_erased_observer.sla` now cover deferred observer-world mutations, explicit spawn-location propagation, lifecycle/event triggering during apply, component+event access tracking, batch planning, pair-mut writeback, entity/query-data query-resource params, `Single` / `Option<Single>` / `Populated` params, filtered pair-mut params, spawned pair-mut params, tuple/AND/OR filter params, Commands, ResMut, MessageWriter, MessageReader, resource/message params, and explicit event-trigger params over the table-erased observer world. Automatic Rust-style caller capture remains pending; explicit `spawn_with_location` metadata and deferred Commands spawn-location propagation are verified. Arbitrary generated query combinations beyond the current K=2..10 helpers, broad generated query combinators, query-data arity/nesting beyond `AnyOf4` and current hand-written shapes, and true multi-threaded World execution are not complete.
- Component registration has runtime Sla metadata IDs plus verified type-id lookup helpers. The current path uses project-level derive markers plus ordinary `impl` methods for component/resource/message/event type identity and table/sparse-set storage kind; those methods feed the table-erased, resource-erased, message-erased, event observer, and table-erased observer runtimes. `ecs_metadata.sla` now centralizes library-owned metadata descriptors, stable numeric id composition, explicit drop-function plumbing, and relationship shape declarations without compiler ECS keywords. `bundle_table_erased.sla` adds Bevy-style bundle spawn/insert helpers over the table-erased path. Automatic metadata generation through a generic language macro/derive facility, generated drop glue, and fully namespace-derived type identity from source names remain pending.
- `lib/relationship.sla` implements Bevy's generic relationship bookkeeping as data: relationship kind registration, one-to-many target collections, one-to-one target replacement, invalid/self relation policy, source/target synchronization, target source queries, ancestors/root/descendants/siblings/leaves traversal, replace/detach, `replace_related_with_difference`, and linked recursive despawn. `commands_relationship.sla` adds deferred Bevy-style relationship commands plus related spawner helpers over that runtime for spawn-related, add, ordered insert, remove, replace, difference replacement, detach-all, despawn-related, one-to-one replacement, and linked despawn. Derive/macro sugar for declaring user relationship component pairs remains pending.
- `lib/hierarchy_relationship_adapter.sla` proves typed relationship facades can be built over the generic relationship runtime in `sla_ecs`: `GenericChildOf` / `GenericChildren` wrappers expose add/insert/reparent/detach/replace-with-difference/despawn/traversal behavior without compiler engine keywords. `hierarchy_commands.sla` adds deferred child mutation commands over the typed facade, while `relationship_one_adapter.sla` verifies a typed one-to-one facade.
- `lib/hierarchy.sla` now implements the canonical Bevy `ChildOf`/`Children` relationship shape in `sla_ecs`: source/target synchronization, reparenting, ordered insert/replace, `replace_children_with_difference`, `Children` swap and function-pointer sort helpers, detach, relationship source queries, ancestors, root ancestor, breadth-first descendants, depth-first descendants, siblings, leaves, and linked recursive child despawn. A generic user-defined relationship derive/macro layer is still pending.
- The project follows the SA-native Bevy plan: use `Mut<T>` / `ResMut<T>` wrappers and Referee write inference instead of making Rust `mut` the core model.
