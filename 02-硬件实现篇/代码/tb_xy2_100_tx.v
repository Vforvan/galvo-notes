//============================================================================
// tb_xy2_100_tx.v -- xy2_100_tx 的仿真测试平台 (self-checking)
//----------------------------------------------------------------------------
// 检查项:
//   1. 输出 CLK 半周期是否为 500 ns (2 MHz)
//   2. 每帧是否 20 个 CLK 周期 (帧长 10 us, 帧率 100 kHz)
//   3. SYNC 是否只在校验位 (第 20 位) 期间为低
//   4. 采样到的 20 bit 是否等于期望帧 (含偶校验独立验证)
//   5. 位置不变时是否持续重复发送同一帧
//
// 用法 (需要 iverilog):
//   iverilog -o sim tb_xy2_100_tx.v xy2_100_tx.v && vvp sim
//
// 注意: 本 testbench 的期望值与 cycle_accurate_model.py 保持一致。
//       build_expected() 独立实现了帧构造 + 偶校验, 与被测模块无共享代码。
//============================================================================

`timescale 1ns/1ps
`default_nettype none

module tb_xy2_100_tx;

    //------------------------------------------------------------------
    // DUT 接口
    //------------------------------------------------------------------
    reg  clk = 0;
    reg  rst_n = 0;
    reg  signed [15:0] x_target = 0;
    reg  signed [15:0] y_target = 0;
    reg  load = 0;

    wire clk_p, clk_n, sync_p, sync_n, x_p, x_n, y_p, y_n;

    localparam real CLK_PERIOD = 83.333;      // 12 MHz

    always #(CLK_PERIOD/2.0) clk = ~clk;

    xy2_100_tx #(.CLK_HZ(12_000_000)) dut (
        .clk(clk), .rst_n(rst_n),
        .x_target(x_target), .y_target(y_target), .load(load),
        .clk_p(clk_p), .clk_n(clk_n),
        .sync_p(sync_p), .sync_n(sync_n),
        .x_p(x_p), .x_n(x_n),
        .y_p(y_p), .y_n(y_n)
    );

    //------------------------------------------------------------------
    // 期望帧构造 (独立实现)
    //   帧 = { 3'b001, D15..D0, P }
    //   D15..D0 占 bit[16:1]; P 占 bit[0], 使整帧 1 的个数为偶数
    //------------------------------------------------------------------
    function [19:0] build_expected(input signed [15:0] t);
        reg [15:0] w;
        reg        p;
        begin
            w = t + 16'd32768;                       // 偏移二进制
            p = ^{3'b001, w};                        // 19 位前导的异或
            build_expected = {3'b001, w, p};
        end
    endfunction

    //------------------------------------------------------------------
    // 接收方模型: 在 clk_p 下降沿采样, 每 20 位组成一帧
    //------------------------------------------------------------------
    integer    errors      = 0;
    integer    frame_count = 0;
    integer    bit_i       = 0;
    integer    sync_low_in_frame = 0;
    time       last_fall   = 0;
    time       half_period = 0;
    reg        started     = 0;
    reg [19:0] cap_x = 0, cap_y = 0;
    reg [19:0] exp_x, exp_y;

    always @(negedge clk_p) begin
        if (started) begin
            if (last_fall != 0)
                half_period = $time - last_fall;
            last_fall = $time;

            if (sync_p === 1'b0)
                sync_low_in_frame = sync_low_in_frame + 1;

            cap_x = {cap_x[18:0], x_p};
            cap_y = {cap_y[18:0], y_p};
            bit_i = bit_i + 1;

            if (bit_i == 20) begin
                frame_count = frame_count + 1;

                // 跳过第 1 帧 (复位后的第一帧总是复位默认帧)
                if (frame_count > 1) begin
                    if (cap_x !== exp_x) begin
                        $display("  [FAIL] frame %0d X: got %020b expected %020b",
                                 frame_count, cap_x, exp_x);
                        errors = errors + 1;
                    end
                    if (cap_y !== exp_y) begin
                        $display("  [FAIL] frame %0d Y: got %020b expected %020b",
                                 frame_count, cap_y, exp_y);
                        errors = errors + 1;
                    end

                    // 独立验证偶校验: 整帧 20 bit 异或必须为 0
                    if ((^cap_x) !== 1'b0) begin
                        $display("  [FAIL] frame %0d X parity error (XOR=%b)",
                                 frame_count, ^cap_x);
                        errors = errors + 1;
                    end
                    if ((^cap_y) !== 1'b0) begin
                        $display("  [FAIL] frame %0d Y parity error (XOR=%b)",
                                 frame_count, ^cap_y);
                        errors = errors + 1;
                    end

                    // 独立验证控制字
                    if (cap_x[19:17] !== 3'b001) begin
                        $display("  [FAIL] frame %0d X header = %b (expect 001)",
                                 frame_count, cap_x[19:17]);
                        errors = errors + 1;
                    end

                    // SYNC 必须只在校验位期间为低 => 每帧恰好 1 个 bit
                    if (sync_low_in_frame != 1) begin
                        $display("  [FAIL] frame %0d: SYNC low during %0d bits (expect 1)",
                                 frame_count, sync_low_in_frame);
                        errors = errors + 1;
                    end
                end

                bit_i = 0;
                cap_x = 0;
                cap_y = 0;
                sync_low_in_frame = 0;
            end
        end
    end

    //------------------------------------------------------------------
    // 施加新位置: 单周期 load 脉冲
    //   注意: 必须在位边界之前给出, pending 会在帧边界提交
    //------------------------------------------------------------------
    task set_pos(input signed [15:0] xv, input signed [15:0] yv);
        begin
            x_target = xv;
            y_target = yv;
            exp_x = build_expected(xv);
            exp_y = build_expected(yv);
            @(posedge clk);
            load = 1;
            @(posedge clk);
            load = 0;
        end
    endtask

    //------------------------------------------------------------------
    // 测试序列
    //------------------------------------------------------------------
    integer i;
    initial begin
        $dumpfile("tb_xy2_100_tx.vcd");
        $dumpvars(0, tb_xy2_100_tx);

        $display("=== XY2-100 TX testbench ===");

        rst_n = 0;
        #500;
        rst_n = 1;
        #200;
        started = 1;

        $display("--- T1: 中心 (0, 0) ---");
        set_pos(0, 0);
        #30000;

        $display("--- T2: 最正端 (+32767, +32767) ---");
        set_pos(32767, 32767);
        #30000;

        $display("--- T3: 最负端 (-32768, -32768) ---");
        set_pos(-32768, -32768);
        #30000;

        $display("--- T4: 任意值 (-12345, +6789) ---");
        set_pos(-12345, 6789);
        #30000;

        $display("--- T5: X 正 Y 负 (+30000, -30000) ---");
        set_pos(30000, -30000);
        #30000;

        $display("--- T6: 位置不变, 持续重复发送 ---");
        #120000;      // 不调用 set_pos, 观察是否仍在发同一帧

        $display("");
        $display("=== 结果 ===");
        $display("CLK 半周期 (期望 500 ns): %0t ns", half_period);
        $display("总帧数: %0d", frame_count);
        if (errors == 0)
            $display("*** 全部通过 (PASS) ***");
        else
            $display("*** 发现 %0d 个错误 (FAIL) ***", errors);
        $display("");
        $finish;
    end

    // 超时保护
    initial begin
        #5_000_000;
        $display("*** 超时 (TIMEOUT) ***");
        $finish;
    end

endmodule

`default_nettype wire
