# sla_ecs Tasks

Update this file whenever a task is completed. Do not mark a task done until the relevant implementation and verification command have both passed.

## Phase 1: Sla Compiler Unblockers

- [x] Confirm current baseline: all `src/*.sla` prototype tests pass, while `examples/movement_demo.sla` fails on a Sla codegen cleanup issue.
- [x] Add compiler regression for chained `array-of-struct` field access inside control flow.
- [x] Fix Sla codegen cleanup for expressions like `game.positions.values[i].x`.
- [x] Run the focused new compiler regression with `zig build local-cli -- sla test tests/test_unit_array_struct_field_cleanup.sla` or equivalent.
- [x] Fix assignment move cleanup for `target = local_owner` and `holder.field = local_owner` patterns.
- [x] Add regressions for assignment move cleanup, field assignment move cleanup, and struct-field scalar reads not moving the owner.
- [x] Rebuild and reinstall the Sla plugin after Sla feature/compiler changes: `SA_PLUGIN_DEV=1 sa plugin install --dev /home/vscode/projects/sa_plugins/sa_plugin_sla`.
- [x] Verify `SA_PLUGIN_DEV=1 sa sla test examples/movement_demo.sla` passes after plugin reinstall.
- [x] Improve `.sla` import expansion so non-`.sla` imports inside imported files resolve relative to the imported file, not the root source file.
- [x] Verify nested `.sla` import contract resolution with `zig build local-cli -- sla check tests/test_unit_sla_import_nested_contract.sla`.
- [x] Add and verify wildcard `.sla` imports: `@import "path/*.sla"` and bare `@import path/*.sla`; reinstall dev plugin after the fix.
- [x] Add and verify Sla `Vec<T>` index assignment, including `Vec` fields inside loops; reinstall dev plugin after the fix.
- [x] Fix nested generic close parsing so `Vec<Vec<T>>` and `Vec<Pair<A, B>>` do not require a spacing workaround before `>>`.
- [x] Fix Sla codegen cleanup for method calls on `Vec` fields such as `query.items.push(...)`.
- [x] Fix Sla monomorphization for generic impl protocol methods so `impl Query<T> { iter_len/iter_at }` supports `for item in query`; regression: `test_unit_generic_for_in_protocol.sla`.
- [x] Fix Sla function pointer values so systems can be stored and passed as `fn(World) -> World`; regression: `test_unit_fn_ptr_value.sla`.
- [x] Fix Sla top-level scalar constant codegen so command tags like `const KIND: i32 = 1` work without illegal numeric SA `@const` output; regression: `test_unit_top_level_numeric_const.sla`.
- [x] Keep Sla compiler `@derive(...)` support language-neutral: arbitrary derive names parse as annotations, with no Bevy/ECS keyword semantics in Zig; regression: `test_unit_derive_component.sla`.
- [x] Remove compiler-bound ECS derive metadata and `@component(storage = ...)`; move `component_type_id`, `component_storage_kind`, `resource_type_id`, `message_type_id`, and `event_type_id` to ordinary `sla_ecs` `impl` methods.
- [x] Fix expanded relative `.sai` / `.sal` contract import resolution after `.sla` import expansion; regression fixture: `tests/import_fixtures/nested/uses_contract.sla`.
- [x] Fix Sla global scalar const call-argument cleanup across loop branches so call args like `matches(i, GLOBAL_MARKER)` do not leave active temporaries at branch merge. Regression: `test_unit_global_const_call_arg_cleanup.sla`; dev plugin reinstalled.
- [x] Rebuild and reinstall the Sla plugin after generic impl protocol and function pointer fixes: `SA_PLUGIN_DEV=1 sa plugin install --dev /home/vscode/projects/sa_plugins/sa_plugin_sla`.
- [x] Rebuild and reinstall the Sla plugin after top-level scalar constant codegen fix: `SA_PLUGIN_DEV=1 sa plugin install --dev /home/vscode/projects/sa_plugins/sa_plugin_sla`.
- [x] Rebuild and reinstall the Sla plugin after language-neutral derive annotation and contract import resolver fixes: `SA_PLUGIN_DEV=1 sa plugin install --dev /home/vscode/projects/sa_plugins/sa_plugin_sla`.
- [x] Audit current source tree after resumed work: current tree contains `lib/*.sla` and `examples/*.sla`; old `src/*.sla` prototypes are not present on disk.

## Phase 2: Bevy-Style Core Runtime

- [x] Implement reusable Bevy-style `Entity` identity in `lib/`: index + generation, placeholder, bit conversion, stale rejection, free-list reuse.
- [x] Implement verified dynamic `DynamicEntityAllocator`: Vec-backed generations/free-list/live occupancy, grows beyond 16 entities, rejects stale/fabricated generations.
- [x] Add verified fixed-capacity generic `ComponentStore<T>` behavior tests: insert/get/has/slot/write/swap-remove.
- [x] Add verified `DynamicComponentStore<T>` backed by `sa_std Vec`: grows past 16 components, get/has/slot/write/swap-remove.
- [ ] Replace fixed-capacity demo storage with reusable component storage backed by dynamic `sa_std Vec` where compiler support permits.
- [x] Add component registration metadata and storage-kind selection: table default, sparse-set opt-in.
- [x] Implement verified registry-driven arbitrary component id membership index: registration, insert/remove membership, despawn cleanup, With/Without entity queries, Added/Changed ticks, and `for in` query iteration.
- [x] Attach typed A/B component value stores to registry-driven component ids for a verified registry-bound typed value owner.
- [x] Replace A/B-specific value ownership for homogeneous component groups with registry-owned arbitrary typed value columns.
- [x] Add verified registry-owned homogeneous value pair joins: pair query, pair `Without` filter, `Added` query, and pair-mut first-component writeback.
- [x] Add verified registry-owned type-erased column store spanning arbitrary concrete component types with boxed raw pointers, per-component drop functions, typed get/query, `Without`, Added/Changed, pair joins, writeback, resources/messages, and despawn cleanup.
- [x] Add verified registry archetype grouping sidecar: component-id signatures, entity locations, add/remove migration, despawn cleanup, and archetype-backed component query.
- [x] Add verified archetype-backed homogeneous value world: component values tied to archetype locations, add/remove migration, replacement/writeback without archetype move, filters, Added/Changed, resources/messages, and despawn cleanup.
- [x] Add verified archetype-backed resource tick tracking: `Res<T>`, `ResMut<T>`, added/changed helpers, `ResMut` writeback, and resource removal semantics.
- [x] Add verified archetype table-row homogeneous value world: component values stored inside archetype columns by entity row, row migration on add/remove/despawn, row-preserving writeback, queries, Added/Changed, resources, and messages.
- [x] Add verified archetype table-row type-erased heterogeneous value world: boxed component payloads stored inside archetype columns by entity row, row migration on add/remove/despawn, typed get/query, pair-mut writeback, Added/Changed, resources, messages, and cleanup.
- [x] Add verified table-row type-erased pair-mut `Without` query helper for `Query<(Mut<A>, B), Without<C>>`-style movement systems. Verification: `SA_PLUGIN_DEV=1 sa sla test lib/world_table_erased.sla`.
- [x] Add verified table-row type-erased `With<T>` and `Added<T>` value query helpers plus type-id auto lookup variants. Verification: `SA_PLUGIN_DEV=1 sa sla test lib/world_table_erased.sla`.
- [x] Add verified table-row type-erased pair query `Without<T>`, `With<T>`, `Added<T>`, and `Changed<T>` helpers plus type-id auto lookup variants. Verification: `SA_PLUGIN_DEV=1 sa sla test lib/world_table_erased.sla`.
- [x] Add verified table-row type-erased pair-mut query `With<T>`, `Added<T>`, and `Changed<T>` helpers plus type-id auto lookup variants, extending the existing pair-mut `Without<T>` path. Verification: `SA_PLUGIN_DEV=1 sa sla test lib/world_table_erased.sla`.
- [x] Add verified homogeneous table-row `With<T>` value query helper. Verification: `SA_PLUGIN_DEV=1 sa sla test lib/world_table_value.sla`.
- [x] Add verified archetype-backed homogeneous `With<T>` value query helper. Verification: `SA_PLUGIN_DEV=1 sa sla test lib/world_archetype_value.sla`.
- [x] Add verified table-row type-erased relationship wrapper in `lib/world_table_erased_relationship.sla`: synchronized `TableErasedWorld` + `RelationshipWorld` entity allocation, component storage, relation source/target queries, linked despawn cleanup, and allocator free-list order preservation. Verification: `SA_PLUGIN_DEV=1 sa sla test lib/world_table_erased_relationship.sla`.
- [x] Add verified table-row Commands, Schedule, and system-param adapters over `TableValueWorld<T, R, M>`.
- [x] Add verified table-row type-erased Commands and Schedule over `TableErasedWorld<R, M>`.
- [x] Add verified ordered table-row type-erased relationship Commands in `lib/commands_table_erased_relationship.sla`: reserve/spawn-related, component insert, relationship mutation, linked despawn, and clear-after-apply in one ordered command list. Verification: `SA_PLUGIN_DEV=1 sa sla test lib/commands_table_erased_relationship.sla`.
- [x] Extend verified ordered table-row type-erased relationship Commands with deferred resource insertion and message writing in the same ordered command list. Verification: `SA_PLUGIN_DEV=1 sa sla test lib/commands_table_erased_relationship.sla`.
- [x] Add verified table-row type-erased relationship Schedule in `lib/schedule_table_erased_relationship.sla`: component access, relationship-kind access, resource/message access, conflict counting, batch selection, sequential run, and planned run. Verification: `SA_PLUGIN_DEV=1 sa sla test lib/schedule_table_erased_relationship.sla`.
- [x] Add verified table-row type-erased relationship system-param adapters in `lib/system_param_table_erased_relationship.sla`: pair-mut query writeback, relationship query + resource param, relationship Commands param, ResMut, MessageWriter, and MessageReader. Verification: `SA_PLUGIN_DEV=1 sa sla test lib/system_param_table_erased_relationship.sla`.
- [x] Add verified table-row type-erased observer wrapper in `lib/world_table_erased_observer.sla`: targeted entity events plus component lifecycle events for add/insert/replace/remove/despawn over `TableErasedWorld`. Verification: `SA_PLUGIN_DEV=1 sa sla test lib/world_table_erased_observer.sla`.
- [x] Add verified table-row type-erased observer Commands in `lib/commands_table_erased_observer.sla`: deferred insert/remove/despawn/resource/message/explicit-event commands that trigger lifecycle/events during apply. Verification: `SA_PLUGIN_DEV=1 sa sla test lib/commands_table_erased_observer.sla`.
- [x] Add verified table-row type-erased observer Schedule in `lib/schedule_table_erased_observer.sla`: component access, event-type access, resource/message access, conflict counting, batch selection, sequential run, and planned run. Verification: `SA_PLUGIN_DEV=1 sa sla test lib/schedule_table_erased_observer.sla`.
- [x] Add verified table-row type-erased observer system-param adapters in `lib/system_param_table_erased_observer.sla`: pair-mut query writeback, observer Commands param, ResMut, MessageWriter, MessageReader, resource/message params, and explicit event trigger param. Verification: `SA_PLUGIN_DEV=1 sa sla test lib/system_param_table_erased_observer.sla`.
- [x] Add verified table-row type-erased system-param adapters over `TableErasedWorld<R, M>`.
- [x] Add verified no-conflict parallel batch planning over `TableErasedSchedule<R, M>`.
- [x] Add verified runtime type-id metadata lookup helpers for `TableErasedWorld<R, M>`: component-id lookup by type id, auto insert/get/query/filters/Changed/remove, type-id Commands insert, type-id schedule access declarations, and type-id system-param adapters.
- [x] Add verified table-erased component bundle helpers: type-id bundle constructors, spawn bundle, insert bundle, duplicate component rejection, and metadata-driven component registration.
- [x] Add ECS component metadata contract files (`.sal` / `.sai`) and verify impl-provided component type ids integrate with `TableErasedWorld<R, M>` registration and lookup.
- [x] Add verified `sla_ecs`-owned metadata descriptor helpers in `lib/ecs_metadata.sla`: stable type-id composition, explicit drop-function plumbing, component/resource/message/event/relationship descriptors, and runtime adapters without compiler engine keywords. Verification: `SA_PLUGIN_DEV=1 sa sla test lib/ecs_metadata.sla`.
- [x] Add verified generic Bevy relationship runtime in `lib/relationship.sla`: relationship kind metadata, one-to-many and one-to-one target collections, source/target synchronization, ordered source insertion with Bevy Vec swap semantics, invalid/self relation policy, replace/detach, and linked despawn. Verification: `SA_PLUGIN_DEV=1 sa sla test lib/relationship.sla`.
- [x] Add verified generic relationship `replace_related_with_difference` in `lib/relationship.sla`, including no-duplicate/disjoint/subset invariants and final target collection ordering. Verification: `SA_PLUGIN_DEV=1 sa sla test lib/relationship.sla`.
- [x] Add verified generic relationship traversal helpers in `lib/relationship.sla`: query len/at/contains, ancestors, root ancestor, breadth-first descendants, depth-first descendants, siblings, and leaves. Verification: `SA_PLUGIN_DEV=1 sa sla test lib/relationship.sla`.
- [x] Add verified generic relationship command queue in `lib/commands_relationship.sla`: deferred spawn-related, add, ordered insert, remove, replace, difference replacement, detach-all, despawn-related, and linked despawn over `RelationshipWorld`. Verification: `SA_PLUGIN_DEV=1 sa sla test lib/commands_relationship.sla`.
- [x] Add verified generic relationship related-spawner command helpers in `lib/commands_relationship.sla`: target-bound batch spawning and existing-entity relation enqueue before apply. Verification: `SA_PLUGIN_DEV=1 sa sla test lib/commands_relationship.sla`.
- [x] Add verified generic relationship one-to-one command replacement coverage in `lib/commands_relationship.sla`. Verification: `SA_PLUGIN_DEV=1 sa sla test lib/commands_relationship.sla`.
- [x] Add verified typed hierarchy relationship facade over the generic runtime in `lib/hierarchy_relationship_adapter.sla`, proving concrete relationship wrappers can live in `sla_ecs` instead of the compiler. Verification: `SA_PLUGIN_DEV=1 sa sla test lib/hierarchy_relationship_adapter.sla`.
- [x] Add verified typed hierarchy traversal facade helpers in `lib/hierarchy_relationship_adapter.sla`: ancestors, root ancestor, BFS/DFS descendants, siblings, and leaves over `RelationshipWorld`. Verification: `SA_PLUGIN_DEV=1 sa sla test lib/hierarchy_relationship_adapter.sla`.
- [x] Add verified deferred typed hierarchy commands in `lib/hierarchy_commands.sla`: add, insert, remove, replace-with-difference, despawn children, and linked despawn over the generic hierarchy facade. Verification: `SA_PLUGIN_DEV=1 sa sla test lib/hierarchy_commands.sla`.
- [x] Add verified typed one-to-one relationship facade in `lib/relationship_one_adapter.sla`, including source replacement, retarget, removal, and linked despawn. Verification: `SA_PLUGIN_DEV=1 sa sla test lib/relationship_one_adapter.sla`.
- [x] Add verified Bevy hierarchy relationship runtime in `lib/hierarchy.sla`: `ChildOf` source relation, synchronized `Children` target collection, reparenting, ordered insert/replace, detach, traversal queries, invalid/self relation discard, and recursive child despawn. Verification: `SA_PLUGIN_DEV=1 sa sla test lib/hierarchy.sla`.
- [x] Add verified Bevy hierarchy ordering and difference helpers in `lib/hierarchy.sla`: `Children` swap, stable/key/cached-key/unstable sort API surface via function pointers, and `replace_children_with_difference`. Verification: `SA_PLUGIN_DEV=1 sa sla test lib/hierarchy.sla`.
- [x] Implement fixed-capacity `World` as the owner of entities, component storage, resources, change ticks, and message queues.
- [x] Implement dynamic `DynamicWorld` owner with dynamic entity allocation, dynamic A/B component stores, dynamic change ticks, resources, messages, pair query, and writeback.
- [x] Implement verified `DynamicWorld3` owner with dynamic A/B/C component stores, spawn bundle helper, triple query, third-component filters, C change detection, and despawn cleanup.
- [x] Add focused fixed-capacity World tests for spawn/despawn, generation bumping, stale entity rejection, component insert/remove, query pair writeback, resources, and messages.
- [x] Add focused tests for spawn/despawn, generation bumping, stale entity rejection, table insert/remove, and sparse-set insert/remove.

## Phase 3: Query, System, Schedule

- [x] Implement verified DynamicWorld query forms using SA-native wrappers: `Query<T>`, `Query<Mut<T>>`, `Query<EntityItem<T>>`, `Query<PairMutItem<A, B>>`; Rust `&T` / `&mut T` parsing is compatibility sugar only. Current surface is bound to `DynamicWorld<A, B, R, M>`'s A/B component shape.
- [x] Implement verified DynamicWorld filters: `With<T>`, `Without<T>`, `Added<T>`, `Changed<T>` for the current A/B world shape.
- [x] Implement verified writeback semantics for `Mut<T>` query items without violating SA Referee ownership rules; `query_mut_a_write` and `query_pair_mut_a_write` update component storage and changed ticks.
- [x] Implement verified DynamicWorld system adapters from Bevy-shaped Sla `fn(World) -> World` functions to the safe runtime execution model using stored function pointers.
- [x] Implement verified sequential `Schedule::default`, `add_systems`, and `run` with component/resource/message read/write access conflict tracking for the current A/B world shape.
- [x] Implement verified deferred `Commands<A, B, R, M>` for the current DynamicWorld A/B shape: reserve entity, insert A/B, despawn, insert resource, write message, ordered apply, and clear-after-apply.
- [x] Implement verified `RegistryValueCommands<T, R, M>` for component-id keyed reserve, insert, despawn, resource, message, ordered apply, and clear-after-apply over `RegistryValueWorld`.
- [x] Implement verified `RegistryValueSchedule<T, R, M>` with stored system function pointers and component-id/resource/message access conflict tracking over `RegistryValueWorld`.
- [x] Implement verified `RegistryErasedCommands<R, M>` for heterogeneous erased component reserve, insert/replace, despawn, resource, message, ordered apply, and clear-after-apply over `RegistryErasedWorld`.
- [x] Implement verified `RegistryErasedSchedule<R, M>` with stored system function pointers and component-id/resource/message access conflict tracking over `RegistryErasedWorld`.
- [x] Implement verified `ArchetypeValueCommands<T, R, M>` for reserve, insert/replace with archetype migration, despawn, resource, message, ordered apply, and clear-after-apply over `ArchetypeValueWorld`.
- [x] Implement verified `ArchetypeValueSchedule<T, R, M>` with stored system function pointers and component-id/resource/message access conflict tracking over `ArchetypeValueWorld`.
- [x] Implement verified archetype-backed system parameter adapters for injected pair-mut query params, resource params, message writer params, adapter writeback, and schedule execution.
- [x] Extend verified archetype-backed system parameter adapters with `ResMut` injection plus `MessageReader` cursor advancement and writeback.
- [x] Extend verified archetype-backed system parameter adapters with `Commands`, standalone `MessageWriter`, and filtered query resource params for `Without`, `Added`, and `Changed`.
- [x] Extend verified archetype-backed system parameter adapters with `With<T>` filtered query resource params. Verification: `SA_PLUGIN_DEV=1 sa sla test lib/system_param_archetype_value.sla`.
- [x] Extend verified homogeneous table-row system parameter adapters with `With<T>`, `Added<T>`, and `Changed<T>` filtered query resource params. Verification: `SA_PLUGIN_DEV=1 sa sla test lib/system_param_table_value.sla`.
- [x] Extend verified table-row type-erased system parameter adapters with `With<T>`, `Added<T>`, and `Changed<T>` filtered query resource params plus auto type-id variants. Verification: `SA_PLUGIN_DEV=1 sa sla test lib/system_param_table_erased.sla`.
- [x] Extend verified table-row type-erased observer system parameter adapters with `With<T>`, `Added<T>`, and `Changed<T>` filtered query resource params plus auto type-id variants. Verification: `SA_PLUGIN_DEV=1 sa sla test lib/system_param_table_erased_observer.sla`.
- [x] Extend verified table-row type-erased pair-mut system adapters with `Without<T>`, `With<T>`, `Added<T>`, and `Changed<T>` filters plus auto type-id variants. Verification: `SA_PLUGIN_DEV=1 sa sla test lib/system_param_table_erased.sla`.
- [x] Extend verified table-row type-erased observer pair-mut system adapters with `Without<T>`, `With<T>`, `Added<T>`, and `Changed<T>` filters plus auto type-id variants. Verification: `SA_PLUGIN_DEV=1 sa sla test lib/system_param_table_erased_observer.sla`.

## Phase 4: Resources, Messages, Examples

- [x] Implement fixed-capacity typed unique resources: insert, get, replace, remove.
- [x] Implement verified DynamicWorld `Res<T>` / `ResMut<T>` wrappers and resource added/changed detection.
- [x] Implement verified type-erased multi-resource storage keyed by `resource_type_id()` impl metadata: unique-per-type insert/get, `Res<T>` / `ResMut<T>`, writeback, remove, and added/changed ticks.
- [x] Implement fixed-capacity `Messages<T>` and reader cursor behavior.
- [x] Add verified `MessageWriter<T>` batching and apply semantics for message system parameters.
- [x] Implement verified type-erased multi-message channels keyed by `message_type_id()` impl metadata: independent channels, batched writer apply, per-reader cursor advancement, and channel clear.
- [x] Implement verified type-erased observer/event triggers keyed by `event_type_id()` impl metadata: immediate observer invocation, non-message reactive semantics, and targeted entity event context.
- [x] Add verified World-based movement/resource/message example: `examples/world_movement_demo.sla`.
- [x] Add verified DynamicWorld movement/resource/message example exceeding the old 16-entity cap: `examples/dynamic_world_movement_demo.sla`.
- [x] Add verified DynamicWorld3 bundle/query/filter example: `examples/dynamic_world3_bundle_demo.sla`.
- [x] Add verified DynamicWorld schedule pipeline example: `examples/dynamic_schedule_demo.sla`.
- [x] Add verified DynamicWorld resource change detection example: `examples/dynamic_resource_change_demo.sla`.
- [x] Add verified DynamicWorld deferred Commands example: `examples/dynamic_commands_demo.sla`.
- [x] Add verified archetype-backed Commands/Schedule pipeline example: `examples/archetype_schedule_commands_demo.sla`.
- [x] Add verified archetype-backed system parameter example: `examples/archetype_system_param_demo.sla`.
- [x] Add verified archetype-backed value storage example: `examples/archetype_value_world_demo.sla`.
- [x] Add verified archetype table-row storage example: `examples/table_value_world_demo.sla`.
- [x] Add verified archetype table-row type-erased heterogeneous storage example: `examples/table_erased_world_demo.sla`.
- [x] Add verified archetype table-row type-erased Commands/Schedule example: `examples/table_erased_schedule_commands_demo.sla`.
- [x] Add verified archetype table-row type-erased system-param example: `examples/table_erased_system_param_demo.sla`.
- [x] Add verified table-erased runtime type-id metadata example: `examples/table_erased_auto_metadata_demo.sla`.
- [x] Extend verified table-erased runtime type-id metadata example with auto `With<T>` and `Added<T>` query/filter system-param paths. Verification: `SA_PLUGIN_DEV=1 sa sla test examples/table_erased_auto_metadata_demo.sla`.
- [x] Add verified table-erased component bundle example: `examples/table_erased_bundle_demo.sla`.
- [x] Add verified table-erased relationship wrapper example: `examples/table_erased_relationship_demo.sla`. Verification: `SA_PLUGIN_DEV=1 sa sla test examples/table_erased_relationship_demo.sla`.
- [x] Add verified ordered table-erased relationship command example: `examples/table_erased_relationship_commands_demo.sla`. Verification: `SA_PLUGIN_DEV=1 sa sla test examples/table_erased_relationship_commands_demo.sla`.
- [x] Add verified table-erased relationship schedule/system-param example: `examples/table_erased_relationship_system_param_demo.sla`. Verification: `SA_PLUGIN_DEV=1 sa sla test examples/table_erased_relationship_system_param_demo.sla`.
- [x] Add verified table-erased observer lifecycle example: `examples/table_erased_observer_demo.sla`. Verification: `SA_PLUGIN_DEV=1 sa sla test examples/table_erased_observer_demo.sla`.
- [x] Add verified table-erased observer schedule/system-param example: `examples/table_erased_observer_system_param_demo.sla`. Verification: `SA_PLUGIN_DEV=1 sa sla test examples/table_erased_observer_system_param_demo.sla`.
- [x] Add verified metadata descriptor demo: `examples/ecs_metadata_descriptor_demo.sla`, covering component registration, explicit drop-function metadata, resources, messages, events, and relationship metadata. Verification: `SA_PLUGIN_DEV=1 sa sla test examples/ecs_metadata_descriptor_demo.sla`.
- [x] Add verified Bevy README parity demo over the table-erased full stack: arbitrary heterogeneous components, sparse `Frozen` filter, `Query<(Mut<Position>, Velocity), Without<Frozen>>`, Commands, Schedule, Resource, Message. Verification: `SA_PLUGIN_DEV=1 sa sla test examples/bevy_readme_parity_table_erased_demo.sla`.
- [x] Update verified Bevy README parity table-erased demo so `Query<(Mut<Position>, Velocity), Without<Frozen>>` runs through the system-param pair-mut adapter instead of hand-written query/writeback. Verification: `SA_PLUGIN_DEV=1 sa sla test examples/bevy_readme_parity_table_erased_demo.sla`.
- [x] Add verified table-erased component metadata example: `examples/table_erased_derive_component_demo.sla`, using project-level derive markers plus ordinary `impl` metadata, including sparse-set storage metadata driving sparse component registration.
- [x] Add verified multi-resource metadata example: `examples/resource_derive_multi_demo.sla`.
- [x] Add verified multi-channel message metadata example: `examples/message_derive_multi_demo.sla`.
- [x] Add verified observer trigger metadata example: `examples/event_observer_demo.sla`.
- [x] Add verified generic relationship runtime example: `examples/relationship_runtime_demo.sla`, covering many relationships, one-to-one replacement, `replace_related_with_difference`, self-reference policy, and linked recursive despawn. Verification: `SA_PLUGIN_DEV=1 sa sla test examples/relationship_runtime_demo.sla`.
- [x] Add verified deferred generic relationship command example: `examples/relationship_commands_demo.sla`, covering add/insert/remove/despawn-related over `RelationshipWorld`. Verification: `SA_PLUGIN_DEV=1 sa sla test examples/relationship_commands_demo.sla`.
- [x] Add verified typed one-to-one relationship facade example: `examples/relationship_one_to_one_demo.sla`. Verification: `SA_PLUGIN_DEV=1 sa sla test examples/relationship_one_to_one_demo.sla`.
- [x] Add verified multi-kind relationship runtime example: `examples/relationship_multi_kind_demo.sla`, covering independent linked and non-linked relationship kinds in one `RelationshipWorld`. Verification: `SA_PLUGIN_DEV=1 sa sla test examples/relationship_multi_kind_demo.sla`.
- [x] Add verified generic-runtime typed hierarchy facade example: `examples/hierarchy_generic_relationship_demo.sla`, covering typed add/insert/difference/despawn over `RelationshipWorld`. Verification: `SA_PLUGIN_DEV=1 sa sla test examples/hierarchy_generic_relationship_demo.sla`.
- [x] Add verified deferred typed hierarchy command example: `examples/hierarchy_commands_demo.sla`. Verification: `SA_PLUGIN_DEV=1 sa sla test examples/hierarchy_commands_demo.sla`.
- [x] Add verified hierarchy relationship example: `examples/hierarchy_relationship_demo.sla`, covering spawn child, relationship sources, reparenting, replace children, `Children` swap/sort, `replace_children_with_difference`, ancestor/root/DFS/leaves queries, and recursive child despawn. Verification: `SA_PLUGIN_DEV=1 sa sla test examples/hierarchy_relationship_demo.sla`.
- [x] Add verified table-row system-param example: `examples/table_system_param_demo.sla`.
- [x] Add verified registry archetype migration example: `examples/registry_archetype_demo.sla`.
- [x] Add verified registry-driven component membership example: `examples/registry_world_demo.sla`.
- [x] Add verified registry-bound typed value world example: `examples/registry_typed_world_demo.sla`.
- [x] Add verified registry-owned multi-column typed value example: `examples/registry_value_world_demo.sla`, including pair joins, `Added`/`Changed`, writeback, resources, messages, and despawn cleanup.
- [x] Add verified registry-owned type-erased heterogeneous component example: `examples/registry_erased_world_demo.sla`.
- [x] Add verified registry-erased Commands/Schedule pipeline example: `examples/registry_erased_schedule_commands_demo.sla`.
- [x] Add verified Bevy README parity example for movement, resources/time, filters, change detection, messages, Commands, and schedule pipeline: `examples/bevy_readme_parity_demo.sla`.
- [x] Verify all current examples with `SA_PLUGIN_DEV=1 sa sla test examples/*.sla` equivalent loop.

## Phase 5: Documentation and Progress

- [x] Rewrite `README.md` around the actual implemented reusable API.
- [x] Update `progress.md` with verified status, test counts, compiler fixes, and known limitations.
- [x] Update `README.md` and `progress.md` to reflect the current tree accurately: verified `lib/` and `examples/`, no present `src/` prototype directory.
- [x] Update `README.md`, `plan.md`, `tasks.md`, and `progress.md` after the observer schedule/system-param batch, including the compiler-boundary note that no engine semantics were added to `sa_plugin_sla`. Verification: full `lib/*.sla` and `examples/*.sla` loops pass, generated `.sa` imports have no absolute `sa_std` path, and `git diff --check` passes.
- [x] Update `README.md`, `plan.md`, `tasks.md`, and `progress.md` after the metadata descriptor batch, including the boundary that descriptor helpers live in `sla_ecs` and automatic drop glue/macro generation remains pending.
- [x] Update `README.md`, `plan.md`, `tasks.md`, and `progress.md` after the table-erased README parity and global scalar const cleanup batch.
- [ ] Restore or intentionally supersede old `src/*.sla` prototype sources if future history requires them.
