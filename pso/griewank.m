function [output] = griewank(x)
%GRIEWANK Griewank Function
d = 2;
part1 = 0;
for i = 1:d
    part1 = part1 + x(i) .^ 2;
end
part2 = 1;
for i = 1:d
    part2 = part2 * cos(x(i) / sqrt(i));
end
output = 1 + part1 / 4000 - part2;
end

