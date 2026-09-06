module cordic16 (
    input  wire                  clk,
    input  wire                  rst_n,
    input  wire                  start,
    input  wire signed [15:0]    angle_in,
    output reg  signed [15:0]    cos_out,
    output reg  signed [15:0]    sin_out,
    output reg                   done
);
    function signed [15:0] atan_lut(input integer idx);
        case (idx)
            0: atan_lut = 12867;
            1: atan_lut = 7596;
            2: atan_lut = 4014;
            3: atan_lut = 2037;
            4: atan_lut = 1023;
            5: atan_lut = 512;
            6: atan_lut = 256;
            7: atan_lut = 128;
            default: atan_lut = 0;
        endcase
    endfunction

    reg signed [15:0] x, y, z;
    reg [3:0] iter_cnt;
    reg busy;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            x <= 0; y <= 0; z <= 0;
            iter_cnt <= 0; busy <= 0; done <= 0;
            cos_out <= 0; sin_out <= 0;
        end else begin
            if (start && !busy) begin
                x <= 9951; y <= 0; z <= angle_in;
                iter_cnt <= 0; busy <= 1; done <= 0;
            end else if (busy) begin
                if (iter_cnt < 8) begin
                    if (z[15] == 1'b0) begin
                        x <= x - (y >>> iter_cnt);
                        y <= y + (x >>> iter_cnt);
                        z <= z - atan_lut(iter_cnt);
                    end else begin
                        x <= x + (y >>> iter_cnt);
                        y <= y - (x >>> iter_cnt);
                        z <= z + atan_lut(iter_cnt);
                    end
                    iter_cnt <= iter_cnt + 1;
                end else begin
                    cos_out <= x; sin_out <= y; done <= 1; busy <= 0;
                end
            end else begin
                done <= 0;
            end
        end
    end
endmodule