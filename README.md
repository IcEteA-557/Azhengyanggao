# J8 Lab 3 — 简易 3 位 ALU

Hong Kong QS No.2 University · J8 Department  
J8 Course · 2026/27 Semester A

IcEteA So Handsome · 91786767 · 2026-11-16

这个仓库是 Lab 3 的全套文件：一份可直接照着做的中文检查点指南、中英文报告草稿、中文实验手册，以及今晚在 Vivado 里要用的 VHDL、测试平台、引脚约束和一键建工程脚本。

## 今晚先看什么

| 文件 | 用途 |
| --- | --- |
| [EE2000_Lab3_检查点达成指南.pdf](./EE2000_Lab3_检查点达成指南.pdf) | **先看这个**。CP1–CP4 的步骤、演示话术、故障排查、进实验室前自查 |
| [EE2000_Lab3_中文版.pdf](./EE2000_Lab3_中文版.pdf) | 中文实验手册，相当于把英文 manual 重新排了一遍 |
| [EE2000_Lab3_Report.pdf](./EE2000_Lab3_Report.pdf) | 英文报告完整草稿，含图表和代码清单 |
| [EE2000_Lab3_Report_中文版.pdf](./EE2000_Lab3_Report_中文版.pdf) | 中文报告完整草稿 |

报告里的板级结果和逻辑分析仪波形是按设计推算的**预期值**。今晚实测后，把对应表格、照片和截图换成你实际看到的，再提交。

## 仓库结构

```text
lab3/
├── EE2000_Lab3_检查点达成指南.pdf
├── EE2000_Lab3_中文版.pdf
├── EE2000_Lab3_Report.pdf
├── EE2000_Lab3_Report_中文版.pdf
├── README.md
├── .gitignore
├── src/
│   ├── alu.vhd              # 3 位 ALU（CP1、CP2）
│   ├── alu_tb.vhd           # 四段激励测试平台（CP1）
│   ├── alu.xdc              # Basys 3 引脚约束
│   ├── create_project.tcl   # 一键创建 Vivado 工程
│   ├── alu_7ops.vhd         # 七种运算扩展（CP3）
│   ├── alu_7ops_tb.vhd      # 七运算测试平台（CP3 可选）
│   └── alu_expected.csv     # 256 组输入/输出预期值
└── _src/                    # 生成 PDF 用的 HTML/CSS/SVG 和校验脚本，可忽略
```

## 5 分钟建好 Vivado 工程

**方式 A：Tcl（推荐）**

打开 Vivado，在 Tcl Console 里：

```tcl
cd <这个文件夹>/src
source create_project.tcl
```

脚本会创建 `src/lab3_alu/lab3_alu.xpr`，器件设为 `xc7a35tcpg236-1`，并加入 `alu.vhd`、`alu_tb.vhd`、`alu.xdc`，顶层设为 `ALU`。

**方式 B：手动**

1. Create Project，器件选 `xc7a35tcpg236-1`（Basys 3）。
2. Add Sources，加入 `src/alu.vhd`、`src/alu_tb.vhd`、`src/alu.xdc`。
3. 把 `ALU` 设为 top。
4. 检查 `alu.xdc` 在 Constraints 里，没有被 disable。

> 手册里可能写成 `xc7a35ticpg236-1L`；以 Vivado 器件列表里的 `xc7a35tcpg236-1` 为准。

## 引脚

| 信号 | 引脚 | 板上元件 |
| --- | --- | --- |
| `A[2:0]` | V17, V16, W16 | SW0, SW1, SW2 |
| `B[2:0]` | W17, W15, V15 | SW3, SW4, SW5 |
| `op[1:0]` | W14, W13 | SW6, SW7 |
| `result[2:0]` | U16, E19, U19 | LD0, LD1, LD2 |
| `carry` | V19 | LD3 |
| `dup_result[2:0]` | J1, L2, J2 | JA1, JA2, JA3 |
| `dup_carry` | G2 | JA4 |

开关按板上印的标签拨，不要从左往右数。`A[0]` 是 SW0，`op[1]` 是 SW7。

## 四个检查点

| 检查点 | 要做什么 | 算通过的标准 | 谁看 |
| --- | --- | --- | --- |
| CP1 | 仿真 ADD、AND、XOR、SHR 四段 | 结果 `000/001/110/010`；`carry` 只在 ADD 为 1；`dup_*` 与主输出一致 | 演示者 |
| CP2 | 下载后测 10 组输入 | LED 与指南表 4 一致，能解释 `7+1` 的 `1000` 和 `7+7` 的 `1110` | 演示者 |
| CP3 | 报告写 7 种运算的改法 | 三位 `op`、八选一、共享加减法器、`SHL`、`111` 保留、`SUB` 进位取反 | 报告评分 |
| CP4 | 逻辑分析仪抓 D0–D3 | 能指出触发通道、采样率、`D3` 何时为 1 | 演示者 |

CP3 只写报告，不现场演示。详细步骤和“演示时这样说”的话术都在检查点指南里。

## 仿真预期

`alu_tb.vhd` 固定 `A = 101`、`B = 011`，每 10 ns 换一个 `op`：

| 时间段 | op | 运算 | result | carry |
| --- | --- | --- | --- | --- |
| 0–10 ns | 00 | ADD | 000 | 1 |
| 10–20 ns | 01 | AND | 001 | 0 |
| 20–30 ns | 10 | XOR | 110 | 0 |
| 30–40 ns | 11 | SHR | 010 | 0 |

Tcl 跑仿真：

```tcl
set_property top alu_tb [get_filesets sim_1]
launch_simulation
run all
```

波形窗口里加 `A`、`B`、`op`、`result`、`carry`、`dup_result`、`dup_carry`，Radix 设为 Binary，Zoom Fit。

## 逻辑分析仪接线

| 逻辑分析仪线 | 接到 |
| --- | --- |
| 黑 | GND（PMOD 的 5 或 11 脚，**不要接 6/12 的 VCC**） |
| 棕 | JA1（`dup_result[0]`） |
| 红 | JA2（`dup_result[1]`） |
| 橙 | JA3（`dup_result[2]`） |
| 黄 | JA4（`dup_carry`） |

PulseView：触发 `D0` 上升沿，5 M samples、1 MHz；如果下拉菜单没有这两项，用 1 M samples、20 kHz（窗口更长，手拨更从容）。先点 Run，再拨开关。

## GitHub 使用

仓库地址：<https://github.com/IcEteA-557/Azhengyanggao>

第一次推送（仓库根目录就是 `lab3` 的内容）：

```bash
cd lab3
git init
git add .
git commit -m "J8 Lab 3: ALU design, reports and guide"
git branch -M main
git remote add origin https://github.com/IcEteA-557/Azhengyanggao.git
git push -u origin main
```

如果想把整个 `lab`（含 lab1、lab2、lab3）作为一个仓库：

```bash
cd lab
git init
git add lab3
git commit -m "J8 Lab 3"
git branch -M main
git remote add origin https://github.com/IcEteA-557/Azhengyanggao.git
git push -u origin main
```

如果 `origin` 已存在，用 `git remote set-url origin <url>` 改地址；如果 push 被拒绝，先 `git pull --rebase origin main` 再 push。

**公开仓库提醒**：封面有学号 91786767，中文手册里含课程手册的原始截图。不想公开就把仓库改成 private，或删掉中文手册 PDF、把学号改成占位符后再推。`.gitignore` 已排除 Vivado 工程缓存和原始 `EE2000_Lab3.pdf`。

## 文件验证

`_src/verify/check.py` 用 GHDL 对 `alu.vhd` 和 `alu_7ops.vhd` 做过 256 + 448 组穷举（VHDL-93c 和 VHDL-08 两套标准），并检查了 `dup_result`/`dup_carry` 是否跟随主输出。没有装 GHDL 不影响今晚的 Vivado 实验；它只是写报告时的额外证据。

```bash
python3 _src/verify/check.py
```

## 说明

- 报告和指南里的预期值来自 `_src/model.py` 生成的 `src/alu_expected.csv`，与 VHDL 仿真结果一致。
- 中文手册是根据英文原版重新翻译排版的，图中的原始截图来自英文原版；两者冲突时以英文原版为准。
- 原始 `EE2000_Lab3.pdf` 保留在本地，未纳入提交，避免公开课程材料。
