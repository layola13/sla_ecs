# sla_ecs Core ECS Implementation Plan

## Goal

Build `sla_ecs` into a real Sla/SA ECS runtime that matches the core semantics shown in Bevy ECS' README: entities, components, world storage, resources, queries, systems, schedules, messages, and change detection. This is not a documentation-only task and not a fixed-capacity demo. Compiler or Sla syntax gaps must be fixed when they block the Bevy-shaped API.

The first deliverable is **Bevy Core ECS parity**, not the entire `bevy_ecs` crate. Full Bevy internals such as observers, reflection, hierarchy, relationships, deferred command queues, and parallel executors are later phases unless they block README-level semantics.

## Current Baseline

- `src/*.sla` remains a passing prototype/regression layer across entity, storage, world, movement, health, full demo, and query probes.
- `lib/` now contains reusable Entity, dynamic Entity allocator, fixed ComponentStore, Vec-backed DynamicComponentStore, Vec-backed SparseComponentStore, component metadata registry, resources, messages, fixed-capacity World, and dynamic Vec-backed DynamicWorld.
- `examples/movement_demo.sla`, `examples/world_movement_demo.sla`, and `examples/dynamic_world_movement_demo.sla` pass with the installed Sla dev plugin.
- `lib/world_dynamic.sla` removes the old fixed-capacity limit for the current two-component owner shape and verifies dynamic entities, components, change ticks, resources, messages, pair query, and writeback.
- `lib/world_dynamic.sla` also tracks resource added/changed ticks and exposes `Res<T>` / `ResMut<T>` wrappers for Bevy-style resource systems.
- `lib/world_dynamic3.sla` extends the typed dynamic owner to three component columns and verifies bundle spawn, triple query, third-component filters, and C-component change detection.
- `lib/query_dynamic.sla` adds verified Bevy-shaped query wrappers for the current dynamic A/B world: `Query<T>`, `Query<Mut<T>>`, entity-bearing items, pair mutable items, `With/Without/Added/Changed`, `for in`, and explicit `Mut<T>` writeback.
- `lib/schedule_dynamic.sla` adds verified Bevy-shaped sequential scheduling for the current dynamic A/B world: stored `fn(World) -> World` systems, `schedule_default`, `schedule_add_systems`, `schedule_run`, and access conflict tracking.
- The next runtime step is replacing these fixed typed-column shapes with a registry-driven component column owner, then broadening examples and parallel scheduling.
- `sa_plugin_sla` remains part of the implementation surface when Sla syntax/codegen blocks ECS semantics; recent fixes include wildcard `.sla` imports, nested generic `>>` parsing, `Vec<T>` index assignment, `Vec` field method-call cleanup, generic impl protocol monomorphization for `for in`, and function pointer value codegen for schedules.

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

- `SA_PLUGIN_DEV=1 sa sla test examples/movement_demo.sla` passes.
- All old `src/*.sla` tests keep passing.
- New Bevy Core examples pass through `sa sla test` and exercise the public ECS API rather than private demo-specific storage.
- Compiler fixes have focused regression tests under `sa_plugin_sla/tests/`.
- README does not claim support for Bevy features that are not implemented.
