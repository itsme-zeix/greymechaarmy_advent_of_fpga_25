/*
@timeit
def part1(grid: list[str]) -> int:
    rows = len(grid)
    cols = len(grid[0])

    accessible = 0

    # Parallelize across (row, col)
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] != "@":
                continue

            # count adjacent
            count = 0
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    if (
                        not (di == 0 and dj == 0)
                        and 0 <= i + di < rows
                        and 0 <= j + dj < cols
                        and grid[i + di][j + dj] == "@"
                    ):
                        count += 1

            if count < 4:
                accessible += 1

    return accessible
*/

module part1 
    #(
        parameter grid_width = 137
    )(
        input wire clk,
        input wire rst,
        input wire data_in,
        output reg[31:0] total
    );

    reg a,b,c, d,e,f, g,h,i; // 3x3 grid to process
    reg[31:0] row;
    reg[31:0] col;
    // store prev rows for comparison/lookup later
    reg prev_row [0: grid_width - 1];
    reg prev_prev_row [0: grid_width - 1];

    // This is so we skip any additions at the start (before 3x3 grid fills up w data)
    wire is_valid = (row >= 2) && (col >= 2);

    // Excludes e as it is the center of the 3x3 grid, sums to max of 8.
    wire [3:0] neighbour_count = a + b + c + d + f + g + h + i;

    // e == @ and <4 neighbours
    wire is_accessible = (e == 1'b1) && (neighbour_count < 4);

    always @(posedge clk) begin
        if (rst) begin
            {a,b,c,d,e,f,g,h,i} <= 0;
            row <= 0;
            col <= 0;
            total <= 0;
        end else begin
            // Update da grid
            a <= b; b <= c; c <= prev_prev_row[col];
            d <= e; e <= f; f <= prev_row[col];
            g <= h; h <= i; i <= data_in;

            // We advance col by col first, then once we reach the limit, we advance the row
            if (col == grid_width - 1) begin
              col <= 0;
              row <= row + 1;
            end else begin
              col <= col + 1;
            end

            if (is_valid && is_accessible) begin
              total <= total + 1;
            end
        end
    end
endmodule;

/*
@timeit
def part2(grid: list[str]) -> int:
    # Use set instead for speed
    occupied = set()
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "@":
                occupied.add((i, j))
    initial_size = len(occupied)

    needs_rescan = True
    while needs_rescan:
        needs_rescan = False
        for i, j in occupied.copy():
            count = 0
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    if not (di == 0 and dj == 0) and (i + di, j + dj) in occupied:
                        count += 1
            if count < 4:
                occupied.remove((i, j))
                needs_rescan = True

    return initial_size - len(occupied)
*/


