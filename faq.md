# sla_ecs FAQ — 给 codex 的指导建议

> 本文件由进度巡检线程每 10 分钟更新。todo 形式记录:Sla 语言陷阱、编译器 bug、架构忠实度建议。
> codex 写代码,本线程只读巡检 + 在此留指导。
> 最近更新:2026-06-19 06:34

---

## A. Sla 语言已知陷阱(写代码时务必遵守)

- [x] **跨文件导入已可用**:`@import "x.sla"` 现已支持(本会话修了 parser 预扫描 + plugin dirname)。被导入文件的 struct/enum 类型名在主文件可直接用作字面量。
- [ ] **嵌套 struct 字段访问要先 let**:`total + item.pos.x` 易触发 PhiStateConflict / MemoryLeak。写成 `let p = item.pos; total = total + p.x;`。
- [ ] **`x = func(x)` 触发 UseAfterMove**:给同一变量重新赋值时,若右侧函数消费了它,会报错。用新 `let` 绑定:`let x2 = func(x);`。
- [ ] **impl 方法内 while 循环里 `return self` 可能 TypeMismatch**:复杂的带提前返回的循环方法,改用自由函数 `fn op(store: T, ...) -> T`。
- [ ] **泛型 `impl<T>` 方法不工作**:`impl<T> Foo<T> { fn m() }` 解析失败。泛型操作一律用泛型自由函数 `fn op<T>(...)`,已验证可单态化。
- [ ] **`Type.static_method()` 关联函数不工作**:用自由构造函数 `fn type_new() -> Type` 代替。
- [ ] **函数指针不能存进 struct 字段**:`struct S { f: fn(i32)->i32 }` 取用会 UndefinedCall。函数指针只能作函数参数传递。schedule 存系统已验证可行(说明有特例,注意写法)。
- [ ] **大数组字面量 + 多 struct 同文件**:曾见 `[0;64]` 级字面量在多 storage 结构体同文件时 TypeMismatch。优先用 Vec 动态存储,避免巨型固定数组。

## B. 编译器 bug 状态(sa_plugin_sla)

- [x] **typeSize(.array) bug 已修**:结构体内数组按指针(8字节)算偏移,循环内访问 struct 字段数组不再 segfault。回归测试 `test_unit_struct_field_array_loop.sla`。
- [x] **跨文件 .sla import 已修**:parser 预扫描导入类型名。回归 `test_unit_sla_import.sla`。
- [ ] **观察**:`lib/commands_dynamic.sla` 曾报瞬时 codegen error,重跑即过 — 疑似 `.test.sa` 缓存陈旧。若再现,先 `rm *.test.sa` 再跑。
- [ ] 发现编译器层 bug 请记录在此,由编译器线程统一修,勿在 ECS 代码里绕过埋坑。

## C. 架构忠实度建议(对照 bevy_ecs)

- [ ] **【最大缺口】无真正 Archetype/Table 概念**:当前 `DynamicWorld<A,B,R,M>` 把实体平铺在并行 Vec 列里,没有"同组件集实体归入同一原型"的分组。bevy 核心就是 archetype。建议下一阶段引入 `ArchetypeId` + 原型签名(组件位掩码 u32)+ 实体按原型分组。
- [ ] **【硬编码组件数】`DynamicWorld<A,B,R,M>` 只支持 2 组件 1 资源 1 消息**。bevy 支持任意多组件。Sla 无类型擦除,短期难做任意多;建议路线:用 ComponentRegistry + 每组件类型一个 Vec 列 + 位掩码原型签名,逐步加到 world_dynamic4/5 或改成注册式。
- [ ] **已有好基础**:`ComponentRegistry` + `ComponentStorageKind(Table/SparseSet)` 已对齐 bevy 的 StorageType 语义;`dyn_store`(Vec 列式)+ `sparse_store`(稀疏集)双存储已具雏形。下一步是让 World 真正用 registry 驱动列,而非硬编码 A/B。
- [ ] **EntityLocation 缺失**:bevy 的 Entity 通过 `{archetype_id, archetype_row, table_id, table_row}` 间接定位。当前 entity 直接线性查找。引入 archetype 后应补 location 表。
- [ ] **change detection 已有 tick**:保持;对齐 bevy 的 added/changed ComponentTicks 即可。
- [ ] **Commands 延迟队列设计不错**:并行 typed Vec 列 + 命令元数据流,apply 时按序执行 —— 这是绕过"无类型擦除队列"的合理忠实适配,保留。

## D. 测试基线(最近巡检)

- [x] 06:32 全绿:lib/ 全模块 + 全 examples 通过。commands_dynamic 20 tests,query_dynamic 22,schedule_dynamic 24,world_dynamic 18,dynamic_commands_demo 21。
