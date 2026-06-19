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
- [x] Rebuild and reinstall the Sla plugin after generic impl protocol and function pointer fixes: `SA_PLUGIN_DEV=1 sa plugin install --dev /home/vscode/projects/sa_plugins/sa_plugin_sla`.
- [x] Rebuild and reinstall the Sla plugin after top-level scalar constant codegen fix: `SA_PLUGIN_DEV=1 sa plugin install --dev /home/vscode/projects/sa_plugins/sa_plugin_sla`.
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

## Phase 4: Resources, Messages, Examples

- [x] Implement fixed-capacity typed unique resources: insert, get, replace, remove.
- [x] Implement verified DynamicWorld `Res<T>` / `ResMut<T>` wrappers and resource added/changed detection.
- [x] Implement fixed-capacity `Messages<T>` and reader cursor behavior.
- [x] Add verified World-based movement/resource/message example: `examples/world_movement_demo.sla`.
- [x] Add verified DynamicWorld movement/resource/message example exceeding the old 16-entity cap: `examples/dynamic_world_movement_demo.sla`.
- [x] Add verified DynamicWorld3 bundle/query/filter example: `examples/dynamic_world3_bundle_demo.sla`.
- [x] Add verified DynamicWorld schedule pipeline example: `examples/dynamic_schedule_demo.sla`.
- [x] Add verified DynamicWorld resource change detection example: `examples/dynamic_resource_change_demo.sla`.
- [x] Add verified DynamicWorld deferred Commands example: `examples/dynamic_commands_demo.sla`.
- [x] Add verified archetype-backed Commands/Schedule pipeline example: `examples/archetype_schedule_commands_demo.sla`.
- [x] Add verified archetype-backed system parameter example: `examples/archetype_system_param_demo.sla`.
- [x] Add verified archetype-backed value storage example: `examples/archetype_value_world_demo.sla`.
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
- [ ] Restore or intentionally supersede old `src/*.sla` prototype sources if future history requires them.
