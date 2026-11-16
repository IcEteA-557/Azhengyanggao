#!/usr/bin/env python3
"""Build the Chinese manual, report and checkpoint guide."""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from build_docs import LAB3, excerpt, figure, listing_text, page, table  # noqa: E402


def zh_title(kind: str, title: str, subtitle: str, report: bool = False) -> str:
    meta = "2026/27 学年 A 学期<br>课程主任：Prof. IcEteA<br><br>"
    if report:
        meta += "姓名：<b>IcEteA So Handsome</b><br>学号：<b>91786767</b><br>日期：<b>2026 年 11 月 16 日</b>"
    else:
        meta += "姓名：<b>IcEteA So Handsome</b>　学号：<b>91786767</b><br>日期：<b>2026 年 11 月 16 日</b>"
    return f"""
<div class="title-page">
  <div class="univ">香港QS No.2大学</div>
  <div class="dept">J8学系</div>
  <div class="rule"></div>
  <div class="course">J8课程</div>
  <div class="kind">{kind}</div>
  <div class="labno">{title}</div>
  <div class="labtitle">{subtitle}</div>
  <div class="meta">{meta}</div>
</div>
"""


# ---------------------------------------------------------------------------
def report_zh() -> str:
    body = zh_title("实验报告三", "简易 3 位 ALU", "设计、仿真与逻辑分析仪验证", report=True)
    body += """
<h1>1. 实验目的</h1>
<p>本次实验的目的，是不再把加法器当成一个大的布尔表达式，而是做一个由两位操作码选择运算的小型算术逻辑单元（ALU）。ALU 有两个三位操作数 <i>A</i> 和 <i>B</i>、一个操作码 <i>op</i>[1:0]，输出三位结果和一位进位。四种运算分别是加法、按位与、按位异或，以及把 <i>A</i> 逻辑右移一位。</p>
<p>除了做出能工作的电路，这次实验还有四个目的。第一，复习前两次实验的组合逻辑流程：写 VHDL、仿真、约束引脚、综合、实现、下载。第二，有意识地使用 VHDL 的类型转换。手册提示 <font face="Menlo, monospace">srl</font> 只适用于 <font face="Menlo, monospace">BIT_VECTOR</font>，不适用于 <font face="Menlo, monospace">STD_LOGIC_VECTOR</font>，这是课程中第一次“不转换就编译不过”的地方。第三，练习位切片与拼接：四位和由 <font face="Menlo, monospace">('0' &amp; A) + ('0' &amp; B)</font> 得到，移位结果由 <font face="Menlo, monospace">'0' &amp; A(2 downto 1)</font> 得到。第四，通过 PMOD 接口用逻辑分析仪观察同样的信号，而不是只相信 LED。</p>
<p>最终完成的是一个纯组合逻辑设计。测试平台给出四段激励，每段对应一种运算，波形上四段结果互不相同。板级实现把操作数接到 SW0–SW5，把操作码接到 SW6–SW7，把结果接到 LD0–LD2，把进位接到 LD3。复制输出 <font face="Menlo, monospace">dup_result</font> 和 <font face="Menlo, monospace">dup_carry</font> 接到 JA1–JA4，供逻辑分析仪使用。报告同时回答检查点 3：如果要实现七种运算，VHDL 需要怎样修改。</p>

<h1>2. 设计</h1>
<h2>2.1 运算表</h2>
<p>在写任何 VHDL 之前，先用表 1 把行为固定下来。最关键的一列是“进位”：只有加法可能从第 2 位产生进位，因此与、异或和移位都把进位强制为 0。先固定这一列，可以避免“逻辑运算时进位没有赋值”这种常见错误。</p>
"""
    body += table(
        "表 1. 3 位 ALU 的运算表。",
        ["op[1:0]", "运算", "result[2:0]", "carry"],
        [
            ["00", "ADD", "(A + B) mod 8", "A + B ≥ 8 时为 1，否则为 0"],
            ["01", "AND", "A 与 B 按位与", "0"],
            ["10", "XOR", "A 与 B 按位异或", "0"],
            ["11", "SHR", "A 逻辑右移一位", "0"],
        ],
    )
    body += """
<p>加法在四位上进行。在每个操作数前面拼接一个 <font face="Menlo, monospace">'0'</font>，就把操作数扩展成四位；和的第四位正好是第 2 位的进位：</p>
<div class="eq">tmp &lt;= ('0' &amp; A) + ('0' &amp; B);&nbsp;&nbsp;&nbsp; result = tmp(2 downto 0),&nbsp; carry = tmp(3)</div>
<p>用算术语言说，结果是 <i>(A + B)</i> 对 8 取模，进位在 <i>A + B</i> 不小于 8 时恰为 1。与和异或按位进行，进位没有意义，所以接 0。移位时结果最高位为 0，<i>A</i> 的低两位下移：<i>result</i> = <font face="Menlo, monospace">'0' &amp; A(2 downto 1)</font>。这是逻辑移位，不是算术移位，旧符号位不会复制。三位操作数下，<i>A</i> = 101 右移一位是 010，不是 110。</p>
<p>手册里有一个容易看漏的细节：<font face="Menlo, monospace">sll</font> 和 <font face="Menlo, monospace">srl</font> 是为 <font face="Menlo, monospace">BIT_VECTOR</font> 定义的，不是为 <font face="Menlo, monospace">STD_LOGIC_VECTOR</font> 定义的。如果 <i>A</i> 声明为 <font face="Menlo, monospace">STD_LOGIC_VECTOR</font>，直接写 <font face="Menlo, monospace">A srl 1</font> 在 VHDL-93 下编译不过。因此设计先转换成 <font face="Menlo, monospace">BIT_VECTOR</font>，移位，再转换回来：</p>
<div class="eq">result &lt;= to_stdlogicvector(to_bitvector(A) srl 1);</div>
<p>这个转换是显式的，而且把移位放在“运算符确实存在”的类型域里。另一个不太显眼的细节是选择语句的默认分支。手册的译码器例子在 <font face="Menlo, monospace">when others</font> 里写了 <font face="Menlo, monospace">"ZZZZ"</font>；那是共享总线用的三态值，不适合作为内部多路选择器的默认值。本设计改用具体的默认值，并把移位放在最后一个具名分支，这样 <font face="Menlo, monospace">when others</font> 覆盖移位以及仿真时刻可能出现的 <font face="Menlo, monospace">"UU"</font> 等值。</p>

<h2>2.2 VHDL 描述</h2>
<p>代码清单 1 是完整的实体和结构体。实体名是 <font face="Menlo, monospace">ALU</font>，与文件名 <font face="Menlo, monospace">alu.vhd</font> 一致，因为 Vivado 添加源文件时使用文件名，名字不一致会让顶层更难找。所有端口名都与手册和 XDC 完全一致。</p>
<p>与模板相比，第一处改动是库子句。模板只用了 <font face="Menlo, monospace">IEEE.STD_LOGIC_1164.ALL</font>。这个包定义了类型和逻辑运算符，但没有在 <font face="Menlo, monospace">STD_LOGIC_VECTOR</font> 上定义算术 <font face="Menlo, monospace">+</font>。加入 <font face="Menlo, monospace">IEEE.STD_LOGIC_UNSIGNED.ALL</font> 后，四位向量的 <font face="Menlo, monospace">+</font> 才是我想要的无符号加法。另一种写法是用 <font face="Menlo, monospace">NUMERIC_STD</font> 加 <font face="Menlo, monospace">unsigned(...)</font> 转换；用 unsigned 包可以让代码更接近手册的提示，也避免在加法器周围写四次转换。</p>
<p>和在并发赋值中只算一次，随后两个选择信号赋值根据 <i>op</i> 选出结果和进位。<font face="Menlo, monospace">with op select</font> 是并发语句，等价于一个多路选择器加无寄存器输出；没有进程，没有敏感列表，也不会产生锁存器。每个分支都赋了值，最后一个分支是 <font face="Menlo, monospace">when others</font>，所以四种编码以及仿真时刻的元值都有定义。</p>
<p>复制输出只是 <font face="Menlo, monospace">result_t</font> 和 <font face="Menlo, monospace">carry_t</font> 的并发副本。它们不是第二个 ALU，也不改变逻辑；它们存在是因为 LED 引脚和 PMOD 排针是不同引脚，逻辑分析仪需要在 JA 上看到副本。综合器会把两份都保留下来，因为两份都驱动输出引脚。</p>
"""
    body += listing_text(excerpt(LAB3 / "src" / "alu.vhd", "library"),
                         "代码清单 1. alu.vhd：四种运算的 ALU（省略注释）。", "long")

    body += """
<h2>2.3 测试平台</h2>
<p>代码清单 2 是测试平台。实体端口列表为空，因为仿真没有引脚。元件声明重复 ALU 的端口，端口映射使用具名关联。我在实验二吃过按位置映射的亏：端口顺序一改，设计仍然能展开，但操作数被接反，波形看起来“合理”却是错的。</p>
<p>四段激励都保持 <i>A</i> = 101、<i>B</i> = 011。这样选是为了让四个结果互不相同：5 + 3 = 8 得 000、进位 1；5 与 3 得 001；5 异或 3 得 110；5 &gt;&gt; 1 得 010。如果两种运算产生相同结果，操作码接错时波形可能看不出来。</p>
"""
    body += table(
        "表 2. 测试平台的激励与预期输出。",
        ["时间 (ns)", "op", "运算", "A", "B", "result", "carry"],
        [
            ["0–10", "00", "ADD", "101", "011", "000", "1"],
            ["10–20", "01", "AND", "101", "011", "001", "0"],
            ["20–30", "10", "XOR", "101", "011", "110", "0"],
            ["30–40", "11", "SHR", "101", "011", "010", "0"],
        ],
    )
    body += """
<p>每次赋值后都有 <font face="Menlo, monospace">wait for 10 ns</font>，最后的 <font face="Menlo, monospace">wait;</font> 让进程停住。如果没有最后的 wait，进程会立刻重复，波形上只剩最后一段，前三段只是一串 delta 周期的模糊。给 <i>A</i>、<i>B</i>、<i>op</i> 的初值让第一个 delta 周期就是确定的，因此第一次赋值之前波形也有定义。</p>
"""
    body += listing_text(excerpt(LAB3 / "src" / "alu_tb.vhd", "begin"),
                         "代码清单 2. alu_tb.vhd：端口映射与激励（省略声明）。", "long")

    body += """
<h2>2.4 引脚约束与复制输出</h2>
<p>表 3 把端口映射到 Basys 3。操作数用 SW0–SW5，操作码用 SW6–SW7，结果用 LD0–LD2，进位用 LD3。四个 JA 引脚复制同样的值，供逻辑分析仪使用。引脚编号来自 Basys 3 主 XDC，不是凭记忆写的。</p>
"""
    body += table(
        "表 3. Basys 3 引脚分配。",
        ["信号", "引脚", "板上元件"],
        [
            ["A[2:0]", "V17, V16, W16", "SW0, SW1, SW2"],
            ["B[2:0]", "W17, W15, V15", "SW3, SW4, SW5"],
            ["op[1:0]", "W14, W13", "SW6, SW7"],
            ["result[2:0]", "U16, E19, U19", "LD0, LD1, LD2"],
            ["carry", "V19", "LD3"],
            ["dup_result[2:0]", "J1, L2, J2", "JA1, JA2, JA3"],
            ["dup_carry", "G2", "JA4"],
        ],
    )
    body += """
<p>XDC 里有两个细节。第一，<font face="Menlo, monospace">get_ports</font> 里的名字必须与 VHDL 完全一致，包括下标：写 <font face="Menlo, monospace">{A[0]}</font>，不是 <font face="Menlo, monospace">{A0}</font>。名字不一致不会阻止综合，但实现时会报告端口未布局，信号永远到不了引脚。第二，每个引脚都要有 <font face="Menlo, monospace">IOSTANDARD LVCMOS33</font>；缺少 IOSTANDARD 会在实现时触发 DRC 错误。CFGBVS 和 CONFIG_VOLTAGE 按主 XDC 的写法在整个设计里设置一次。</p>
<p>复制输出是 <font face="Menlo, monospace">result_t</font> 和 <font face="Menlo, monospace">carry_t</font> 的副本，因此 LED 和逻辑分析仪看到的是同一个信号。没有副本时，分析仪只能去探 LED 引脚，而 LED 引脚并没有引到排针。四个 JA 引脚也是实体比运算表多出两个输出端口的原因。</p>
"""
    body += figure("figs/fig_board.svg", "图 1. 板级映射：开关、LED 与 ALU 使用的 JA 排针。")

    body += """
<h1>3. 结果与讨论</h1>
<h2>3.1 综合后的电路</h2>
<p>图 2 是预期 Vivado 会推断出的数据通路。加法器是四位进位链；与、异或和移位是各自独立的组合逻辑块；输出选择是由 <i>op</i> 控制的四选一多路选择器。手册第 5 页的 RTL 原理图显示了同样的块，Vivado 给它们起名 RTL_ADD、RTL_AND、RTL_XOR、RTL_RSHIFT 和 RTL_MUX。具体门数不重要，重要的是没有锁存器。选择语句的每个分支都赋值，因此设计是纯组合逻辑。</p>
"""
    body += figure("figs/fig_datapath.svg", "图 2. 四种运算 ALU 的数据通路：加法器、逻辑块、移位与输出选择。")

    body += """
<h2>3.2 检查点 1：仿真</h2>
<p>图 3 是四段激励的波形。顶部的阶段标签依次标出 ADD、AND、XOR、SHR。光标在 35 ns，位于 SHR 段，此时 <i>result</i> = 010、<i>carry</i> = 0。表 4 重复了这些值，便于不读波形标签也能核对。</p>
"""
    body += table(
        "表 4. 检查点 1 波形中的预期值。",
        ["阶段", "op", "A", "B", "result", "carry", "dup_result", "dup_carry"],
        [
            ["ADD", "00", "101", "011", "000", "1", "000", "1"],
            ["AND", "01", "101", "011", "001", "0", "001", "0"],
            ["XOR", "10", "101", "011", "110", "0", "110", "0"],
            ["SHR", "11", "101", "011", "010", "0", "010", "0"],
        ],
    )
    body += """
<p>有三处值得核对，而不只是看结果。第一，<i>carry</i> 只在第一段为 1；如果与或异或段出现 1，说明进位的选择赋值写错了。第二，<i>dup_result</i> 和 <i>dup_carry</i> 必须严格跟随 <i>result</i> 和 <i>carry</i>；不一致说明端口映射或副本接错。第三，10 ns 处的跳变是干净的：测试平台每次变化后等满 10 ns，采样点上不会残留 delta 周期的毛刺。</p>
<p>同一组激励可以直接在 XSim 里运行。图 3 是按仿真值重画的矢量图，不是截图，这样打印出来数字仍然清楚；检查点达成指南里列出了需要截图的窗口。</p>
"""
    body += figure("figs/fig_cp1.svg", "图 3. 检查点 1 波形：四种运算各 10 ns，光标在 35 ns。")

    body += """
<h2>3.3 检查点 2：板级结果</h2>
<p>表 5 列出板级测试的十组输入。前四组练习加法与进位，包括两行“结果为 000、进位为 1”的情况；接下来四组练习与和异或；最后两组练习移位。开关模式按 SW7 到 SW0 书写，可以当成一个字节来读；具体哪个物理开关对应哪一位，以板上印的标签为准。</p>
"""
    body += table(
        "表 5. 板级测试用例与预期 LED 模式。",
        ["#", "A", "B", "op", "result", "carry", "LD3..LD0", "SW7..SW0"],
        [
            ["1", "011", "010", "00", "101", "0", "0101", "00 010 011"],
            ["2", "111", "001", "00", "000", "1", "1000", "00 001 111"],
            ["3", "110", "011", "00", "001", "1", "1001", "00 011 110"],
            ["4", "111", "111", "00", "110", "1", "1110", "00 111 111"],
            ["5", "110", "101", "01", "100", "0", "0100", "01 101 110"],
            ["6", "101", "011", "01", "001", "0", "0001", "01 011 101"],
            ["7", "101", "011", "10", "110", "0", "0110", "10 011 101"],
            ["8", "110", "101", "10", "011", "0", "0011", "10 101 110"],
            ["9", "101", "000", "11", "010", "0", "0010", "11 000 101"],
            ["10", "111", "000", "11", "011", "0", "0011", "11 000 111"],
        ],
    )
    body += """
<p>有两行特别容易误判。7 + 1 = 8 时 <i>result</i> = 000、<i>carry</i> = 1，LED 显示 1000 而不是 0000，因为 LD3 是进位。7 + 7 = 14 时结果是 110、进位 1，模式是 1110。若只看 LD2–LD0，这两行都像失败。移位行也要注意：5 &gt;&gt; 1 是 2（010），不是 6（110），因为这是逻辑移位，新的最高位是 0。</p>
<p>开关顺序是另一个实际陷阱。板上 SW0 在拨码开关组的一端，SW7 在另一端；表中按 SW7 到 SW0 书写。设置时按板上印的标签，而不是从左往右数。表 5 的预期值与生成 <font face="Menlo, monospace">alu_expected.csv</font> 的参考模型来自同一份代码，因此表 1、表 5 和 CSV 不会互相矛盾，除非模型本身错了。</p>

<h2>3.4 检查点 3：七种运算</h2>
<p>手册要求讨论：如果要实现七种运算，VHDL 要怎样改。最干净的做法是把 <i>op</i> 扩展到三位：两位只能给出四种编码，再多的译码也变不出另外三种。表 6 列出七种运算和保留编码。</p>
"""
    body += table(
        "表 6. 七种运算 ALU 的运算表。",
        ["op[2:0]", "运算", "result[2:0]", "carry"],
        [
            ["000", "ADD", "(A + B) mod 8", "A + B ≥ 8 时为 1"],
            ["001", "SUB", "(A − B) mod 8", "A ≥ B（无借位）时为 1"],
            ["010", "AND", "A 与 B", "0"],
            ["011", "OR", "A 或 B", "0"],
            ["100", "XOR", "A 异或 B", "0"],
            ["101", "SHR", "A &gt;&gt; 1", "0"],
            ["110", "SHL", "A &lt;&lt; 1（对 8 取模）", "0"],
            ["111", "保留", "000", "0"],
        ],
    )
    body += """
<p>数据通路有三处扩展。输出选择变成八选一多路选择器。加法器由 ADD 和 SUB 共用：减法在二进制补码里是 <i>A</i> + (not <i>B</i>) + 1，所以 <font face="Menlo, monospace">diff &lt;= ('0' &amp; A) + (not ('0' &amp; B)) + "0001"</font>。移位组增加 SHL，即 <font face="Menlo, monospace">A(1 downto 0) &amp; '0'</font>。与、或、异或复用原来的门。</p>
<p>有三个细节容易错。第一，多出的 <i>op</i> 位需要引脚：Basys 3 上 SW8 是 V2，XDC 必须增加 <font face="Menlo, monospace">op[2]</font>。第二，保留编码 111 应输出确定值（000，进位 0），而不是 <font face="Menlo, monospace">'Z'</font>。第三，SUB 的进位不是 <font face="Menlo, monospace">diff(3)</font>，而是它的反，因为 <font face="Menlo, monospace">diff(3) = 1</font> 表示 <i>A</i> &lt; <i>B</i>，也就是有借位；<font face="Menlo, monospace">not diff(3)</font> 才是“无借位”标志。</p>
<p>七运算测试平台每一段用不同的操作数，使七个结果互不相同：001、101、100、111、011、010、110。这样操作码接反时一眼就能看出来。完整设计在 <font face="Menlo, monospace">alu_7ops.vhd</font>，测试平台在 <font face="Menlo, monospace">alu_7ops_tb.vhd</font>；下面的清单只摘出运算选择和进位选择。</p>
"""
    seven_ops = """    signal sum  : STD_LOGIC_VECTOR (3 downto 0);
    signal diff : STD_LOGIC_VECTOR (3 downto 0);
begin
    sum  <= ('0' & A) + ('0' & B);
    diff <= ('0' & A) + (not ('0' & B)) + "0001";

    with op select
        result_t <= sum(2 downto 0)              when "000",
                    diff(2 downto 0)             when "001",
                    A and B                      when "010",
                    A or B                       when "011",
                    A xor B                      when "100",
                    to_stdlogicvector(to_bitvector(A) srl 1) when "101",
                    A(1 downto 0) & '0'          when "110",
                    "000"                        when others;

    with op select
        carry_t <= sum(3)     when "000",
                   not diff(3) when "001",
                   '0'         when others;"""
    body += listing_text(seven_ops, "代码清单 3. 七运算 ALU 中的运算选择与进位选择（摘录）。", "long")
    body += figure("figs/fig_7ops.svg", "图 4. 七运算数据通路：多一位操作码、八选一选择和共用的加减法单元。")

    body += """
<h2>3.5 检查点 4：逻辑分析仪</h2>
<p>实验 2 在 PMOD 排针上观察同样的信号。接线是：黑线接 GND，棕线接 JA1，红线接 JA2，橙线接 JA3，黄线接 JA4。黑线必须接 GND，不能接 VCC；PMOD 引脚图把 5、11 脚标为 GND，把 6、12 脚标为 VCC。接错会得到一条直线，某些分析仪上还可能损坏输入。</p>
<p>PulseView 设为 D0 上升沿触发、5 M 采样点、1 MHz 采样率。触发通道是 JA1 = <font face="Menlo, monospace">dup_result[0]</font>，也就是结果的 LSB。当 <i>B</i> = 000、op = 00 时，结果等于 <i>A</i>，所以 D0 就是 <i>A</i>(0)；每次 <i>A</i> 从偶数变奇数它都会上升，这个边沿启动采集。</p>
"""
    body += table(
        "表 7. 逻辑分析仪通道。",
        ["分析仪通道", "JA 引脚", "ALU 信号", "含义"],
        [
            ["D0", "JA1", "dup_result[0]", "结果 LSB"],
            ["D1", "JA2", "dup_result[1]", "结果第 1 位"],
            ["D2", "JA3", "dup_result[2]", "结果 MSB"],
            ["D3", "JA4", "dup_carry", "进位"],
        ],
    )
    body += """
<p>图 5 是预期采集结果。前八步让 <i>A</i> 从 000 扫到 111，<i>B</i> = 000。D0 每步翻转，D1 每两步翻转，D2 每四步翻转，D3 保持 0。最后两步令 <i>B</i> = 001、<i>A</i> = 111；7 + 1 = 8 得 <i>result</i> = 000、<i>carry</i> = 1，所以 D3 变高，D0–D2 变低。这是整段采集中唯一出现进位的地方。</p>
"""
    body += figure("figs/fig_cp4.svg", "图 5. 预期逻辑分析仪采集：A 从 000 扫到 111、B = 000，然后 B = 001、A = 111。")
    body += """
<p>手册正文写“5 M 采样点、1 MHz”，第 10 页截图却显示 1 M 采样点、20 kHz。两者都有效：5 M @ 1 MHz 给出 5 s 窗口、1 μs 分辨率；1 M @ 20 kHz 给出 50 s 窗口、50 μs 分辨率。手拨开关时慢速设置更从容；如果拨得快，就用快速设置。指南里两种都给出，到实验台再选。</p>
<p>矢量图有一个局限：它是理想采集。真实采集会在每个边沿出现短促的开关抖动，因为分析仪足够快，能记录到抖动。抖动不是 ALU 故障。如果波形像台阶，并在台阶处多出很窄的脉冲，那是开关，不是逻辑。</p>

<h2>3.6 常见问题</h2>
<p>这条流程里有几个错误很容易犯，每一个都指向不同的环节。记下修正方法比只贴最终代码更有用。</p>
<ul>
<li><b>按位置映射端口。</b>实体顺序一改，按位置映射的测试平台仍然能展开，但 <i>result</i> 可能接到 <i>carry</i>。具名关联能让波形可信。</li>
<li><b>缺少最后的 wait。</b>进程末尾没有 <font face="Menlo, monospace">wait;</font> 时会重复执行，波形主要显示最后一段。最后的 wait 让进程在四段之后停住。</li>
<li><b>移位用错类型。</b>对 <font face="Menlo, monospace">STD_LOGIC_VECTOR</font> 写 <font face="Menlo, monospace">A srl 1</font> 编译不过；<font face="Menlo, monospace">to_bitvector</font> / <font face="Menlo, monospace">to_stdlogicvector</font> 成对转换即可。</li>
<li><b>XDC 名字。</b>写 <font face="Menlo, monospace">A0</font>、<font face="Menlo, monospace">A1</font>、<font face="Menlo, monospace">A2</font> 而不是 <font face="Menlo, monospace">A[0]</font>、<font face="Menlo, monospace">A[1]</font>、<font face="Menlo, monospace">A[2]</font>，实现时端口会未布局。</li>
<li><b>三态默认值。</b>照抄手册译码器例子的 <font face="Menlo, monospace">"ZZZZ"</font>，综合会警告三态；换成具体默认值即可消除警告和推断出的三态缓冲。</li>
<li><b>分析仪地线。</b>采集是一条直线，通常是黑线接到了 VCC。改接 GND，并对照 PMOD 引脚图检查。</li>
<li><b>触发边沿。</b>用下降沿触发会在扫描结束时才启动采集；上升沿才对应 JA1 的行为，从第一个偶数到奇数的跳变开始。</li>
</ul>

<h1>4. 结论</h1>
<p>这个 ALU 满足四种运算的要求。设计是纯组合逻辑，加法的进位正确，逻辑运算把进位强制为 0，移位是逻辑移位。复制输出让 JA 上能看到内部值，而不改变逻辑。测试平台给出四个互不相同的结果，板级表覆盖了最容易误读的进位情况。</p>
<p>这次实验最有用的部分不是算术，而是“先用表固定行为，再用测试平台核对表”的纪律。四位和用 <font face="Menlo, monospace">tmp(3)</font> 作进位只是一个小技巧，但它省掉了一条单独的进位等式，并使加法与进位必然一致。移位转换是课程中第一次遇到“信号类型决定可用运算符”的情况，显式转换比在注释里声称“这是逻辑移位”更清楚。</p>
<p>检查点 3 说明，同样的结构可以通过更宽的选择器和共用的加减法单元扩展到七种运算；代价主要是多一个开关和更宽的 XDC。保留编码提醒我们：扩展操作码一定会产生必须定义的编码，而 <font face="Menlo, monospace">when others</font> 就是定义它们的地方。</p>
<p>设计已经可以上板。剩下的工作是在实验台上核对表 5 的十组用例，并采集逻辑分析仪波形；报告中的图是矢量重画，便于保持数字清楚，指南列出了需要补拍的截图。完整源码、约束、工程脚本和预期值 CSV 与报告放在同一个仓库里。</p>
"""
    return page("J8 实验报告三 — 简易 3 位 ALU", body, "zh", "zh")


# ---------------------------------------------------------------------------
def manual_zh() -> str:
    body = zh_title("实验手册三", "简易 ALU 设计", "组合逻辑、VHDL 类型转换与逻辑分析仪")
    body += """
<h1>实验目的</h1>
<p>本实验的目标是设计一个简单的算术逻辑单元（ALU），用它复习组合逻辑设计，并练习 VHDL 中的类型转换、位切片与拼接。实验分为两部分：实验 1 设计并验证一个 3 位 ALU；实验 2 用逻辑分析仪观察 ALU 的内部信号。</p>
<p>完成本实验后，你应该能够：</p>
<ul>
<li>把运算表转换成 VHDL 的选择赋值；</li>
<li>使用 <font face="Menlo, monospace">STD_LOGIC_VECTOR</font> 的切片与拼接，并在需要时显式转换到 <font face="Menlo, monospace">BIT_VECTOR</font> 做移位；</li>
<li>用测试平台产生多组激励，并在波形窗口中核对结果与进位；</li>
<li>编写 XDC，把信号分配到 Basys 3 的开关、LED 和 JA 排针；</li>
<li>用逻辑分析仪和 PulseView 观察并行信号，并解释触发与采样设置。</li>
</ul>
<p>本实验有 4 个检查点。检查点 1、2、4 需要向演示者展示；检查点 3 写在实验报告中，不需要现场演示。</p>

<h1>实验 1：设计 3 位 ALU</h1>
<p>本实验要设计一个 3 位 ALU。输入是 <i>A</i>[2:0]、<i>B</i>[2:0] 和操作码 <i>op</i>[1:0]；输出是 <i>result</i>[2:0] 和 <i>carry</i>。ALU 根据 <i>op</i> 执行表 1 中的一种运算。</p>
"""
    body += table(
        "表 1. 3 位 ALU 的运算。",
        ["op[1:0]", "运算", "说明", "carry"],
        [
            ["00", "ADD", "A 加 B", "由和决定"],
            ["01", "AND", "A 与 B 按位与", "0"],
            ["10", "XOR", "A 与 B 按位异或", "0"],
            ["11", "SHR", "A 逻辑右移一位", "0"],
        ],
    )
    body += """
<p>除了运算结果，ALU 还要输出两个“复制”信号 <i>dup_result</i>[2:0] 和 <i>dup_carry</i>。它们的值与 <i>result</i>、<i>carry</i> 相同，目的是把这些内部信号送到 JA 排针，方便逻辑分析仪观察；LED 仍然显示原来的结果和进位。</p>

<h2>步骤</h2>
<ol>
<li><b>建立工程。</b>打开 Vivado，新建工程，器件选择 <font face="Menlo, monospace">xc7a35tcpg236-1</font>（Basys 3）。工程名可以用 <font face="Menlo, monospace">lab3_alu</font>。</li>
<li><b>添加源文件。</b>新建 <font face="Menlo, monospace">alu.vhd</font>，把下面的模板抄进去，然后添加到工程。实体名与文件名保持一致。</li>
<li><b>RTL 分析。</b>对源文件执行 RTL Analysis，打开原理图。观察 Vivado 根据你的代码推断出的门电路；它可能与图 1 不同，这是正常的。</li>
<li><b>写 I/O 约束。</b>新建 XDC，按表 2 分配引脚。SW0–SW2 是 <i>A</i>，SW3–SW5 是 <i>B</i>，SW6–SW7 是 <i>op</i>；LD0–LD2 是 <i>result</i>，LD3 是 <i>carry</i>；JA1–JA3 是 <i>dup_result</i>[0]–[2]，JA4 是 <i>dup_carry</i>。</li>
<li><b>仿真。</b>新建 <font face="Menlo, monospace">alu_tb.vhd</font>，用下面的测试平台模板产生激励；运行 XSim，观察波形。</li>
<li><b>综合、实现、生成比特流并下载。</b>流程与实验 1、2 相同。下载后拨动开关，核对 LED。</li>
</ol>
"""
    body += table(
        "表 2. Basys 3 引脚分配。",
        ["信号", "引脚", "板上元件"],
        [
            ["A[2:0]", "V17, V16, W16", "SW0, SW1, SW2"],
            ["B[2:0]", "W17, W15, V15", "SW3, SW4, SW5"],
            ["op[1:0]", "W14, W13", "SW6, SW7"],
            ["result[2:0]", "U16, E19, U19", "LD0, LD1, LD2"],
            ["carry", "V19", "LD3"],
            ["dup_result[2:0]", "J1, L2, J2", "JA1, JA2, JA3"],
            ["dup_carry", "G2", "JA4"],
        ],
    )
    body += """
<h2>ALU 模板</h2>
<p>下面的模板给出实体、信号和输出连接。运算部分需要你自己补全。注意模板只引用了 <font face="Menlo, monospace">STD_LOGIC_1164</font>；如果要直接对 <font face="Menlo, monospace">STD_LOGIC_VECTOR</font> 做加法，需要再引用 <font face="Menlo, monospace">IEEE.STD_LOGIC_UNSIGNED.ALL</font> 或 <font face="Menlo, monospace">IEEE.NUMERIC_STD.ALL</font>。</p>
"""
    template = """library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity ALU is
    Port ( A          : in  STD_LOGIC_VECTOR (2 downto 0);
           B          : in  STD_LOGIC_VECTOR (2 downto 0);
           op         : in  STD_LOGIC_VECTOR (1 downto 0);
           result     : out STD_LOGIC_VECTOR (2 downto 0);
           carry      : out STD_LOGIC;
           dup_result : out STD_LOGIC_VECTOR (2 downto 0);
           dup_carry  : out STD_LOGIC);
end ALU;

architecture Behavioral of ALU is
    signal result_t : STD_LOGIC_VECTOR (2 downto 0);
    signal carry_t  : STD_LOGIC;
begin
    -- 在这里写运算逻辑：根据 op 选择 result_t 和 carry_t。
    -- 例如：
    --   tmp <= ('0' & A) + ('0' & B);
    --   with op select
    --       result_t <= tmp(2 downto 0) when "00",
    --                   A and B        when "01",
    --                   A xor B        when "10",
    --                   to_stdlogicvector(to_bitvector(A) srl 1) when others;

    result     <= result_t;
    carry      <= carry_t;
    dup_result <= result_t;
    dup_carry  <= carry_t;
end Behavioral;"""
    body += listing_text(template, "代码清单 1. ALU 的实体与结构体模板（运算部分待补全）。", "long")

    body += """
<h2>提示</h2>
<ul>
<li><font face="Menlo, monospace">+</font>、<font face="Menlo, monospace">AND</font>、<font face="Menlo, monospace">OR</font>、<font face="Menlo, monospace">XOR</font> 可以直接用于 <font face="Menlo, monospace">STD_LOGIC_VECTOR</font>，但算术 <font face="Menlo, monospace">+</font> 需要相应的无符号包或 <font face="Menlo, monospace">NUMERIC_STD</font>。</li>
<li><font face="Menlo, monospace">sll</font> 和 <font face="Menlo, monospace">srl</font> 是为 <font face="Menlo, monospace">BIT_VECTOR</font> 定义的。对 <font face="Menlo, monospace">STD_LOGIC_VECTOR</font> 要先转换：<font face="Menlo, monospace">to_stdlogicvector(to_bitvector(A) srl 1)</font>。</li>
<li>把操作数前面拼一个 <font face="Menlo, monospace">'0'</font> 再做四位加法：<font face="Menlo, monospace">tmp &lt;= ('0' &amp; A) + ('0' &amp; B);</font>。和的低三位是结果，<font face="Menlo, monospace">tmp(3)</font> 是进位。</li>
<li><font face="Menlo, monospace">with ... select</font> 是并发选择赋值，适合实现运算选择。每个分支都要赋值，最后用 <font face="Menlo, monospace">when others</font> 覆盖剩余编码。</li>
</ul>
"""
    body += figure("figs/manual/rtl_schematic.png", "图 1. Vivado 根据 ALU 代码推断出的 RTL 原理图（原手册第 5 页）。")

    body += """
<h2>测试平台</h2>
<p>测试平台的实体端口列表为空，因为仿真不连接引脚。下面的模板给出元件声明、信号和进程框架；你需要用 <font face="Menlo, monospace">A</font>、<font face="Menlo, monospace">B</font>、<font face="Menlo, monospace">op</font> 的赋值和 <font face="Menlo, monospace">wait for</font> 产生激励。一次只改一组输入时，其他信号会保持上一次的值。</p>
"""
    tb_template = """Library IEEE;
Use IEEE.STD_LOGIC_1164.ALL;

Entity ALU_tb is
end ALU_tb;

Architecture Behavioral of ALU_tb is
    COMPONENT ALU is
        Port ( A          : in  STD_LOGIC_VECTOR (2 DOWNTO 0);
               B          : in  STD_LOGIC_VECTOR (2 DOWNTO 0);
               op         : in  STD_LOGIC_VECTOR (1 DOWNTO 0);
               result     : out STD_LOGIC_VECTOR (2 DOWNTO 0);
               carry      : out STD_LOGIC;
               dup_result : out STD_LOGIC_VECTOR (2 DOWNTO 0);
               dup_carry  : out STD_LOGIC);
    END COMPONENT;

    SIGNAL A          : STD_LOGIC_VECTOR (2 DOWNTO 0);
    SIGNAL B          : STD_LOGIC_VECTOR (2 DOWNTO 0);
    SIGNAL op         : STD_LOGIC_VECTOR (1 DOWNTO 0);
    SIGNAL result     : STD_LOGIC_VECTOR (2 DOWNTO 0);
    SIGNAL carry      : STD_LOGIC;
    SIGNAL dup_result : STD_LOGIC_VECTOR (2 DOWNTO 0);
    SIGNAL dup_carry  : STD_LOGIC;
begin
    uut: ALU PORT MAP (A, B, op, result, carry, dup_result, dup_carry);

    sigen: PROCESS
    begin
        -- 在这里给 A、B、op 赋值，并在每次变化后 wait for 10 ns。
        wait;
    end PROCESS sigen;
end Behavioral;"""
    body += listing_text(tb_template, "代码清单 2. 测试平台模板。", "long")

    body += """
<p>一个最简单的单值测试可以先令 <i>A</i> = "011"、<i>B</i> = "110"、<i>op</i> = "00"，运行后检查 3 + 6 = 9，即 <i>result</i> = 001、<i>carry</i> = 1。确认单值正确后，再在进程里加四段激励，分别覆盖 ADD、AND、XOR 和 SHR。</p>
"""
    body += figure("figs/manual/sim_screenshot.png", "图 2. 单值仿真的波形窗口：A = 3、B = 6、op = 0，result = 1、carry = 1（原手册第 7 页）。")

    body += """
<p>把单值扩展成四段激励后，预期值如表 3。四段结果互不相同，波形一眼就能看出运算有没有接错。</p>
"""
    body += table(
        "表 3. 四段激励的预期输出（A = 101，B = 011）。",
        ["时间段", "op", "运算", "result", "carry"],
        [
            ["0–10 ns", "00", "ADD", "000", "1"],
            ["10–20 ns", "01", "AND", "001", "0"],
            ["20–30 ns", "10", "XOR", "110", "0"],
            ["30–40 ns", "11", "SHR", "010", "0"],
        ],
    )
    body += """
<div class="checkpoint"><b>检查点 1：</b>向演示者展示测试平台，以及显示 ADD、AND、XOR 和移位运算的波形窗口截图。</div>
<div class="checkpoint"><b>检查点 2：</b>向演示者展示开发板和结果，确认设计工作正常。请记得截图并拍照，供实验报告使用。</div>
<div class="checkpoint"><b>检查点 3：</b>在实验报告中讨论：如果要实现 7 种运算，VHDL 源代码需要怎样修改。</div>

<h1>实验 2：使用逻辑分析仪观察信号</h1>
<p>本实验用逻辑分析仪观察 ALU 的 <i>dup_result</i> 和 <i>dup_carry</i>。这样可以直接看到每一位随时间的变化，而不只是看 LED 的最终值。</p>
<ol>
<li>在板子上设置 <i>A</i> = 000、<i>B</i> = 000、<i>op</i> = 00。</li>
<li>把彩虹线接到逻辑分析仪，注意黑线对准逻辑分析仪底部的 GND 引脚。</li>
<li>把另一端接到 Basys 3 的 JA 排针：黑线接 GND，棕线接 JA1，红线接 JA2，橙线接 JA3，黄线接 JA4。黑线必须接 GND。</li>
<li>用 USB Type-C 线把逻辑分析仪接到电脑。</li>
<li>打开 PulseView。</li>
<li>把触发设为 D0 上升沿，采样设为 5 M 采样点、1 MHz。</li>
<li>参数设置好后点击 Run。</li>
<li>逐位改变 <i>A</i>（000 → 111），再逐位改变 <i>B</i>（000 → 111）。</li>
<li>当 JA1 从 0 变 1 时，逻辑分析仪开始记录波形。</li>
</ol>
"""
    body += figure("figs/manual/logic_analyzer.png", "图 3. 把彩虹线接到逻辑分析仪（原手册第 9 页）。")
    body += figure("figs/manual/pmod_pinout.png", "图 4. PMOD 引脚排列：5、11 脚为 GND，6、12 脚为 VCC，其余为信号（原手册第 9 页）。")
    body += figure("figs/manual/basys3_photo.png", "图 5. Basys 3 与 JA 排针的连接（原手册第 9 页）。")
    body += figure("figs/manual/pulseview_settings.png", "图 6. PulseView 的触发与采样设置（原手册第 10 页）。")
    body += figure("figs/manual/pulseview_waveform.png", "图 7. 一次逻辑分析仪采集的波形（原手册第 10 页）。")
    body += """
<p>观察波形时，注意以下几件事：</p>
<ul>
<li>D0 对应 JA1，即 <i>dup_result</i>[0]，是结果的最低位；D1、D2 依次是第 1 位和最高位；D3 对应 JA4，即 <i>dup_carry</i>。</li>
<li>当 <i>B</i> = 000、<i>op</i> = 00 时，结果等于 <i>A</i>，所以 D0 每变一次 <i>A</i> 就翻转一次，D1 每两次翻转一次，D2 每四次翻转一次。</li>
<li>当 <i>A</i> = 111、<i>B</i> = 001 时，7 + 1 = 8，结果为 000、进位为 1，D3 会变高。</li>
<li>采样窗口要足够长，才能覆盖整个手拨开关的过程。5 M @ 1 MHz 是 5 s；如果拨得慢，可以改用 1 M @ 20 kHz（50 s）。</li>
</ul>
<div class="checkpoint"><b>检查点 4：</b>向演示者展示逻辑分析仪的波形，并解释它是怎样产生的（触发、采样率、通道对应关系）。</div>

<h1>报告要求</h1>
<p>报告应包含：</p>
<ol>
<li>实验目的与 ALU 的运算表；</li>
<li>VHDL 设计说明，包括类型转换、位切片、拼接和选择赋值；</li>
<li>测试平台与仿真波形（检查点 1）；</li>
<li>板级测试结果（检查点 2），建议用表格列出输入、结果、进位和 LED 模式；</li>
<li>检查点 3：七种运算的修改方案，包括运算表、代码片段和对进位的讨论；</li>
<li>检查点 4：逻辑分析仪波形与说明（触发、采样率、通道）；</li>
<li>结论与遇到的问题。</li>
</ol>
<p class="small">本中文版根据英文原版手册翻译并重新排版，图中的原始截图来自英文原版；如与英文原版有冲突，以英文原版为准。</p>
"""
    return page("J8 实验手册三 — 简易 ALU 设计", body, "zh", "zh manual")


# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
def guide_zh() -> str:
    body = zh_title("检查点达成指南", "J8 Lab 3", "今晚的实验流程、演示话术与故障排查")
    body += """
<h1>1. 今晚怎么用这份指南</h1>
<p>这份指南按“进实验室之前 → 现场演示 → 交报告之前”的顺序写。Lab 3 有 4 个检查点：<b>检查点 1、2、4 要当场给演示者看</b>，检查点 3 只写在报告里，不需要现场演示。每个检查点下面都写了“做什么、算通过的标准、要留下什么证据”，最后还有演示时可以直接照着说的话。</p>
<p>建议今晚的顺序是：先建工程并跑通仿真（检查点 1），再综合、实现、下载并测板级（检查点 2），然后接逻辑分析仪（检查点 4），最后用剩下的时间补截图和报告（检查点 3）。不要先接逻辑分析仪，因为板级设计没下载成功时，分析仪上什么也看不到。</p>
"""
    body += figure("figs/fig_flow.svg", "图 1. 今晚的流程：写 VHDL → 仿真 → 综合 → 实现 → 下载 → 验证。")

    body += """
<h1>2. 先看这四件事</h1>
"""
    body += table(
        "表 1. 四个检查点：做什么、怎样算通过、谁来看。",
        ["检查点", "要做什么", "算通过的标准", "谁看"],
        [
            ["CP1", "仿真 ADD、AND、XOR、SHR 四段", "四段结果分别为 000/001/110/010；carry 只在 ADD 为 1；dup 与主输出一致", "演示者"],
            ["CP2", "下载后测 10 组输入", "LED 与表 4 一致，能解释 7+1 的 1000 和 7+7 的 1110", "演示者"],
            ["CP3", "报告写 7 种运算的改法", "有运算表、代码片段、进位与保留编码的说明", "报告评分"],
            ["CP4", "逻辑分析仪抓 D0–D3", "能指出触发通道、采样率、D3 何时为 1", "演示者"],
        ],
    )
    body += """
<p>最容易丢分的地方不是代码，而是“做出来了但讲不清”。演示时每个检查点用 30–60 秒说清楚三件事：我做了什么、预期是什么、实际看到什么。下面每一节都给出可以直接使用的说法。</p>

<h1>3. 开工前 10 分钟</h1>
<h2>3.1 把文件放好</h2>
<p>确认 <code>lab3</code> 文件夹里下面这些文件都在：</p>
"""
    body += table(
        "表 2. lab3 里每个文件是干什么的。",
        ["文件", "用途", "今晚什么时候用"],
        [
            ["EE2000_Lab3_中文版.pdf", "中文实验手册", "到场前/现场查要求"],
            ["EE2000_Lab3_Report.pdf", "英文报告（完整草稿）", "写报告、对照表"],
            ["EE2000_Lab3_Report_中文版.pdf", "中文报告（完整草稿）", "写中文报告"],
            ["EE2000_Lab3_检查点达成指南.pdf", "本指南", "现场照着做"],
            ["src/alu.vhd", "3 位 ALU 设计", "CP1、CP2"],
            ["src/alu_tb.vhd", "四段激励的测试平台", "CP1"],
            ["src/alu.xdc", "Basys 3 引脚约束", "CP2"],
            ["src/create_project.tcl", "一键建 Vivado 工程", "开工"],
            ["src/alu_7ops.vhd", "七种运算的扩展设计", "CP3"],
            ["src/alu_7ops_tb.vhd", "七运算测试平台", "CP3（可选）"],
            ["src/alu_expected.csv", "256 组预期值", "核对/写报告"],
        ],
    )
    body += """
<h2>3.2 建工程</h2>
<p>两种方式选一种。第一种最省事：打开 Vivado 的 Tcl Console，<code>cd</code> 到 <code>lab3/src</code>，执行：</p>
<pre class="code">source create_project.tcl</pre>
<p>它会创建 <code>lab3_alu</code> 工程，器件设为 <code>xc7a35tcpg236-1</code>，并加入 <code>alu.vhd</code>、<code>alu_tb.vhd</code>、<code>alu.xdc</code>，顶层设为 <code>ALU</code>。如果 Tcl 脚本因为路径或权限失败，就用手动方式：新建工程 → 选对器件 → Add Sources 加三个文件 → 把 <code>ALU</code> 设为顶层。</p>
<p>检查三件事：</p>
<ol>
<li>器件是 <code>xc7a35tcpg236-1</code>（Basys 3）。手册里可能写成 <code>xc7a35ticpg236-1L</code>，以 Vivado 器件列表里的 <code>xc7a35tcpg236-1</code> 为准。</li>
<li><code>alu.vhd</code> 的实体名是 <code>ALU</code>，与文件名一致。</li>
<li><code>alu.xdc</code> 已经在 Constraints 里，没有被 disable。</li>
</ol>
"""
    body += figure("figs/fig_board.svg", "图 2. Basys 3 的开关、LED 和 JA 排针；A 在 SW0–SW2，B 在 SW3–SW5，op 在 SW6–SW7。")

    body += """
<h1>4. 检查点 1：仿真</h1>
<h2>4.1 跑起来</h2>
<ol>
<li>在 Sources 面板把 <code>alu_tb</code> 设为 Simulation Top（右键 → Set as Top），或在 Tcl Console 执行 <code>set_property top alu_tb [get_filesets sim_1]</code>。</li>
<li>Flow → Run Simulation → Run Behavioral Simulation；或执行 <code>launch_simulation</code>、<code>run all</code>。</li>
<li>在波形窗口把 <code>A</code>、<code>B</code>、<code>op</code>、<code>result</code>、<code>carry</code>、<code>dup_result</code>、<code>dup_carry</code> 都加进来，Radix 设为 Binary。</li>
<li>Zoom Fit，检查 0–10、10–20、20–30、30–40 ns 四段。</li>
</ol>
"""
    body += table(
        "表 3. 检查点 1 的预期值（A=101，B=011）。",
        ["时间段", "op", "运算", "result", "carry", "dup_result", "dup_carry"],
        [
            ["0–10 ns", "00", "ADD", "000", "1", "000", "1"],
            ["10–20 ns", "01", "AND", "001", "0", "001", "0"],
            ["20–30 ns", "10", "XOR", "110", "0", "110", "0"],
            ["30–40 ns", "11", "SHR", "010", "0", "010", "0"],
        ],
    )
    body += """
<h2>4.2 要截什么图</h2>
<p>截两张：一张是 <code>alu_tb.vhd</code> 的代码窗口（能看出四段 <code>wait for 10 ns</code>），一张是完整波形窗口（能看出四段结果和 carry）。文件名建议 <code>cp1_tb.png</code>、<code>cp1_waveform.png</code>。如果演示者只看一张，就给波形，但要能指着说“这一段是 ADD，carry 在这里为 1”。</p>
<div class="say"><b>演示时这样说：</b>“这是测试平台，四段激励分别是 ADD、AND、XOR、SHR。A 固定为 101、B 固定为 011，所以结果依次是 000 带进位 1、001、110、010。carry 只在加法段为 1；dup_result 和 dup_carry 是给 JA 的副本，和主输出完全一致。”</div>
<p>如果被问“为什么不用随机激励”：四段定值是为了让四个结果互不相同，操作码接反时一眼能看出来；随机激励适合跑覆盖率，不适合 30 秒演示。</p>

<h1>5. 检查点 2：上板</h1>
<h2>5.1 生成并下载</h2>
<ol>
<li>Flow → Run Synthesis；完成后 Run Implementation；再 Generate Bitstream。</li>
<li>Open Hardware Manager → Open Target → Auto Connect。</li>
<li>Program Device，选择 <code>lab3_alu.bit</code>，点 Program。</li>
<li>如果 Auto Connect 找不到板子：确认板子电源开关、USB 线是数据线而不是仅充电线、Vivado 的 cable driver 已安装；Windows 下可能需要装 Digilent 的 cable driver。</li>
</ol>
<h2>5.2 测这 10 组</h2>
<p>按表 4 拨开关。开关模式按 SW7 到 SW0 写，具体哪个物理开关对应哪一位，以板上印的标签为准；不要从左往右数。每测完一组，在“实测”一栏打勾，并在报告里把“预期”改成你实际看到的模式。</p>
"""
    body += table(
        "表 4. 板级 10 组用例（A、B、op → result、carry、LED）。",
        ["#", "A", "B", "op", "result", "carry", "LD3..LD0", "SW7..SW0"],
        [
            ["1", "011", "010", "00", "101", "0", "0101", "00 010 011"],
            ["2", "111", "001", "00", "000", "1", "1000", "00 001 111"],
            ["3", "110", "011", "00", "001", "1", "1001", "00 011 110"],
            ["4", "111", "111", "00", "110", "1", "1110", "00 111 111"],
            ["5", "110", "101", "01", "100", "0", "0100", "01 101 110"],
            ["6", "101", "011", "01", "001", "0", "0001", "01 011 101"],
            ["7", "101", "011", "10", "110", "0", "0110", "10 011 101"],
            ["8", "110", "101", "10", "011", "0", "0011", "10 101 110"],
            ["9", "101", "000", "11", "010", "0", "0010", "11 000 101"],
            ["10", "111", "000", "11", "011", "0", "0011", "11 000 111"],
        ],
    )
    body += """
<p>两组最容易误判：</p>
<ul>
<li>7 + 1 = 8：result = 000，carry = 1，LED 是 <b>1000</b>，不是 0000。LD3 是进位。</li>
<li>7 + 7 = 14：result = 110，carry = 1，LED 是 <b>1110</b>。</li>
</ul>
<p>拍一张照片：开关位置 + LED 同时入镜，最好能看出你正在测哪一组。文件名 <code>cp2_board.jpg</code>。</p>
<div class="say"><b>演示时这样说：</b>“这是下载后的板子。A 在 SW0–SW2，B 在 SW3–SW5，op 在 SW6–SW7；LD0–LD2 是结果，LD3 是进位。这一组是 7+1，结果是 000、进位 1，所以 LED 显示 1000。这一组是 7+7，结果是 110、进位 1，显示 1110。”</div>
<p>如果被问“为什么 7+1 的 LED 不是 0000”：因为 LD3 接的是 carry，不是 result 的第四位；result 只有三位。</p>

<h1>6. 检查点 3：报告里的七种运算</h1>
<p>这一项不现场演示，但要写在报告里。最简单的答法是：把 <code>op</code> 从 2 位扩到 3 位，输出选择从四选一变成八选一，加法器由 ADD 和 SUB 共用，移位组增加 SHL，保留编码 111 输出 000。</p>
"""
    body += table(
        "表 5. 七种运算的编码。",
        ["op[2:0]", "运算", "result", "carry"],
        [
            ["000", "ADD", "(A+B) mod 8", "A+B ≥ 8"],
            ["001", "SUB", "(A−B) mod 8", "A ≥ B（无借位）"],
            ["010", "AND", "A and B", "0"],
            ["011", "OR", "A or B", "0"],
            ["100", "XOR", "A xor B", "0"],
            ["101", "SHR", "A >> 1", "0"],
            ["110", "SHL", "A << 1", "0"],
            ["111", "保留", "000", "0"],
        ],
    )
    body += """
<p>报告里至少写清三点：</p>
<ol>
<li><b>为什么要多一位：</b>2 位只有 4 个编码，7 种运算必须用 3 位；多出的 op[2] 接 SW8（V2），XDC 要加一行。</li>
<li><b>SUB 的进位为什么取反：</b>减法用补码 <i>A</i> + (not <i>B</i>) + 1；<code>diff(3)=1</code> 表示 <i>A</i> &lt; <i>B</i>（有借位），所以 carry = <code>not diff(3)</code> 才是“无借位”。</li>
<li><b>保留编码：</b>111 要给确定值 000、carry 0，不能写 <code>'Z'</code>；三态会推断出总线缓冲，不是内部多路选择器。</li>
</ol>
<p>代码用 <code>src/alu_7ops.vhd</code>，报告里贴 <code>result_t</code> 和 <code>carry_t</code> 两个选择赋值即可，不需要贴整个文件。图 3 可以用来解释数据通路。</p>
"""
    body += figure("figs/fig_7ops.svg", "图 3. 七运算数据通路：多一位 op、八选一、共用加减法单元。")

    body += """
<h1>7. 检查点 4：逻辑分析仪</h1>
<h2>7.1 接线</h2>
<p>先把板子设成 <i>A</i> = 000、<i>B</i> = 000、<i>op</i> = 00，再接线。接线顺序：</p>
<ol>
<li>黑线 → GND（PMOD 的 5 或 11 脚；不要接 6/12 脚的 VCC）。</li>
<li>棕线 → JA1；红线 → JA2；橙线 → JA3；黄线 → JA4。</li>
<li>逻辑分析仪 USB-C → 电脑。</li>
</ol>
<p>接好后先看一眼：黑线是否在 GND 那一列，而不是 VCC。接错会得到一条直线，甚至损坏输入。</p>
"""
    body += figure("figs/manual/pmod_pinout.png", "图 4. PMOD 引脚：5/11 是 GND，6/12 是 VCC，中间 8 个是信号。")
    body += """
<h2>7.2 PulseView 设置</h2>
<ol>
<li>打开 PulseView，选择设备（常见的是 <code>fx2lafw</code> 兼容的逻辑分析仪）。</li>
<li>通道只开 D0–D3，分别对应 JA1–JA4。</li>
<li>采样：5 M samples、1 MHz；如果下拉菜单没有这两个值，用 1 M samples、20 kHz（窗口更长，手拨更从容）。</li>
<li>Trigger：D0，Rising edge。</li>
<li>点 Run，然后从 <i>A</i> = 000 开始逐位拨到 111；再拨 <i>B</i> 到 001，让 <i>A</i> = 111，观察最后一次加法。</li>
<li>点 Stop，Zoom Fit，截图。</li>
</ol>
"""
    body += figure("figs/manual/pulseview_settings.png", "图 5. PulseView 的触发和采样设置。")
    body += table(
        "表 6. 通道对应关系。",
        ["通道", "JA", "信号", "含义"],
        [
            ["D0", "JA1", "dup_result[0]", "结果最低位"],
            ["D1", "JA2", "dup_result[1]", "结果第 1 位"],
            ["D2", "JA3", "dup_result[2]", "结果最高位"],
            ["D3", "JA4", "dup_carry", "进位"],
        ],
    )
    body += """
<h2>7.3 波形应该是什么样</h2>
<p>前八步 <i>B</i> = 000，结果等于 <i>A</i>：D0 每步翻转，D1 每两步翻转，D2 每四步翻转，D3 一直是 0。最后一步 <i>A</i> = 111、<i>B</i> = 001，7 + 1 = 8，结果 000、进位 1，所以 D3 变高、D0–D2 变低。</p>
"""
    body += figure("figs/fig_cp4.svg", "图 6. 预期采集：A 从 000 到 111（B=000），然后 B=001、A=111。")
    body += """
<div class="say"><b>演示时这样说：</b>“黑线接 GND，棕红橙黄分别接 JA1–JA4。PulseView 用 D0 上升沿触发、1 MHz 采样、5 M 点。D0 是结果最低位，所以 A 每加一它就翻转；D1 每两步、D2 每四步翻转。最后 7+1=8 时，D3 进位变高，D0–D2 变低。”</div>
<p>如果被问“为什么要触发”：手拨开关的时刻不确定，触发让采集从 JA1 的上升沿开始，波形才有稳定的起点；预触发样本还能看到触发前的一小段。</p>

<h1>8. 故障排查</h1>
"""
    body += table(
        "表 7. 常见现象与处理。",
        ["现象", "可能原因", "处理"],
        [
            ["综合报 srl/sll 未定义", "对 STD_LOGIC_VECTOR 直接移位", "用 to_bitvector / to_stdlogicvector 转换"],
            ["仿真只有最后一段", "进程末尾没有 wait，或没有 wait for", "每段后 wait for 10 ns，末尾 wait;"],
            ["波形全是 X/U", "信号没有初值，或端口映射错", "给初值，改用具名关联"],
            ["实现报 unplaced ports", "XDC 名字与 VHDL 不一致", "改成 {A[0]} 这种带下标的名字"],
            ["DRC 报 IOSTANDARD", "引脚缺电平标准", "每个引脚加 IOSTANDARD LVCMOS33"],
            ["Hardware Manager 找不到板子", "电源/线/驱动", "开电源，换数据线，装 cable driver"],
            ["LED 全灭", "没下载成功，或结果就是 000", "看 LD3 进位；重新 Program"],
            ["LED 与开关不对应", "开关组顺序记反", "按板上标签，A0 是 SW0"],
            ["JA 没有信号", "XDC 缺 JA，或没下载", "检查 dup_result/dup_carry 约束"],
            ["PulseView 找不到设备", "USB/驱动/设备选错", "换线，重插，选 fx2lafw"],
            ["采集是直线", "黑线接 VCC，或通道接错", "黑线接 GND，核对 JA1–JA4"],
            ["触发不启动", "边沿/通道设错", "D0、Rising edge，先 Run 再拨开关"],
            ["窗口太短", "采样率太高/点数太少", "改 1 M @ 20 kHz"],
            ["台阶处有窄脉冲", "开关抖动", "正常现象，不是 ALU 故障"],
        ],
    )

    body += """
<h1>9. 进实验室前自查</h1>
<ul class="checklist">
<li>☐ 中文手册和本指南已下载到本机，能离线打开。</li>
<li>☐ Vivado 工程能打开，器件是 xc7a35tcpg236-1，alu.vhd / alu_tb.vhd / alu.xdc 都在。</li>
<li>☐ 仿真能跑出四段，知道 CP1 要截哪两张图。</li>
<li>☐ 板子、USB 数据线、彩虹线、逻辑分析仪、PulseView 都准备好了。</li>
<li>☐ 手机或截图工具可用。</li>
<li>☐ 知道 CP1/CP2/CP4 要演示，CP3 只写报告。</li>
<li>☐ 记得带学生证；报告封面要填姓名、学号、日期。</li>
</ul>

<h1>10. 交报告前检查</h1>
<ul class="checklist">
<li>☐ 封面：IcEteA So Handsome、91786767、2026 年 11 月 16 日（或实际提交日期）。</li>
<li>☐ 表 1、2、4、5、6、7 都在，编号连续。</li>
<li>☐ 图 1–5 都在，图注完整。</li>
<li>☐ CP1 有波形截图或矢量图；CP2 有实测表和照片；CP4 有分析仪截图。</li>
<li>☐ CP3 有七运算表、代码片段、SUB 进位和保留编码的解释。</li>
<li>☐ 结论里写了遇到的问题和修正方法，不是只抄步骤。</li>
<li>☐ 文件名与 lab2 风格一致：<code>EE2000_Lab3_Report.pdf</code> / <code>EE2000_Lab3_Report_中文版.pdf</code>。</li>
</ul>
<p class="small">本指南中的板级结果和逻辑分析仪波形是按设计推算的预期值；做完实验后，请用你实际看到的 LED 模式、照片和波形替换报告中的对应内容，再提交。</p>
"""
    return page("J8 Lab 3 检查点达成指南", body, "zh", "zh guide")


# ---------------------------------------------------------------------------
def main() -> None:
    for name, fn in [
        ("report_zh.html", report_zh),
        ("manual_zh.html", manual_zh),
        ("guide_zh.html", guide_zh),
    ]:
        out = HERE / name
        out.write_text(fn(), encoding="utf-8")
        print(f"wrote {out}")


if __name__ == "__main__":
    main()
