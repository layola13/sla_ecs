# sla_ecs Core ECS Implementation Plan

## Goal

Build `sla_ecs` into a real Sla/SA ECS runtime that matches the core semantics shown in Bevy ECS' README: entities, components, world storage, resources, queries, systems, schedules, messages, and change detection. This is not a documentation-only task and not a fixed-capacity demo. Compiler or Sla syntax gaps must be fixed when they block the Bevy-shaped API.

The first deliverable is **Bevy Core ECS parity**, not the entire `bevy_ecs` crate. Full Bevy internals such as observers, reflection, hierarchy, relationships, deferred command queues, and parallel executors are later phases unless they block README-level semantics.

## Current Baseline

- The current tree contains the reusable `lib/` runtime and verified `examples/`; the old `src/` prototype directory is not present on disk.
- `lib/` now contains reusable Entity, dynamic Entity allocator, fixed ComponentStore, Vec-backed DynamicComponentStore, Vec-backed SparseComponentStore, component metadata registry, registry-driven component id membership, registry-bound typed A/B value ownership, resources, messages, fixed-capacity World, and dynamic Vec-backed DynamicWorld.
- `examples/world_movement_demo.sla`, `examples/dynamic_world_movement_demo.sla`, `examples/dynamic_world3_bundle_demo.sla`, `examples/dynamic_schedule_demo.sla`, `examples/dynamic_resource_change_demo.sla`, `examples/dynamic_commands_demo.sla`, `examples/registry_world_demo.sla`, and `examples/registry_typed_world_demo.sla` pass with the installed Sla dev plugin.
- `lib/world_dynamic.sla` removes the old fixed-capacity limit for the current two-component owner shape and verifies dynamic entities, components, change ticks, resources, messages, pair query, and writeback.
- `lib/world_dynamic.sla` also tracks resource added/changed ticks and exposes `Res<T>` / `ResMut<T>` wrappers for Bevy-style resource systems.
- `lib/world_dynamic3.sla` extends the typed dynamic owner to three component columns and verifies bundle spawn, triple query, third-component filters, and C-component change detection.
- `lib/query_dynamic.sla` adds verified Bevy-shaped query wrappers for the current dynamic A/B world: `Query<T>`, `Query<Mut<T>>`, entity-bearing items, pair mutable items, `With/Without/Added/Changed`, `for in`, and explicit `Mut<T>` writeback.
- `lib/schedule_dynamic.sla` adds verified Bevy-shaped sequential scheduling for the current dynamic A/B world: stored `fn(World) -> World` systems, `schedule_default`, `schedule_add_systems`, `schedule_run`, and access conflict tracking.
- `lib/commands_dynamic.sla` adds verified Bevy-style deferred commands for the current dynamic A/B world: reserve entity, insert A/B, despawn, insert resource, write message, ordered apply, and clear-after-apply.
- `lib/world_registry.sla` adds verified registry-driven arbitrary component id membership, With/Without entity queries, Added/Changed ticks, despawn cleanup, and `for in` entity iteration.
- `lib/world_registry_typed.sla` binds typed A/B value stores to registered component ids and uses `RegistryWorld` membership/ticks as the source of truth. A single registry-owned type-erased value store remains pending.
- The next runtime step is replacing fixed A/B value ownership with registry-owned arbitrary component value columns, followed by broader system params and parallel scheduling.
- `sa_plugin_sla` remains part of the implementation surface when Sla syntax/codegen blocks ECS semantics; recent fixes include wildcard `.sla` imports, nested generic `>>` parsing, `Vec<T>` index assignment, `Vec` field method-call cleanup, generic impl protocol monomorphization for `for in`, function pointer value codegen for schedules, and top-level scalar const codegen.

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
- Implement `World` as the owner of entity locations, component storage, resource storage, change ticks, and message queues.
- Keep all mutation expressed through SA-safe linear value flow or verified exclusive access paths.

### Phase 3: Query, System, Schedule

Expose Bevy-shaped APIs over the runtime.

- Support query forms needed by Bevy README examples using the SA-native wrapper shape: `Query<T>`, `Query<Mut<T>>`, `Query<(Entity, T)>`, `Query<(Mut<A>, B)>`, `With<T>`, `Without<T>`, `Added<T>`, and `Changed<T>`. Rust `&T` / `&mut T` forms are compatibility inputs only, not the internal model.
- Implement query iteration so each matching live entity appears once, stale/despawned entities are excluded, and writeback updates the underlying component storage.
- Implement system adapters so Bevy-shaped system functions lower to the current Sla-safe execution model.
- Implement `Schedule::default`, `add_systems`, and sequential `run`; track read/write component sets for conflict detection and future parallel execution.

### Phase 4: Resources, Messages, Examples

Complete README-level Bevy concepts and examples.

- Implement unique typed resources with insert/get/get_mut/remove semantics.
- Implement `Messages<T>`, `MessageWriter<T>`, and `MessageReader<T>` with per-reader cursor behavior.
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
