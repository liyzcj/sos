function [output] = rastrigin(x)
%UNTITLED rastrigin function
%   
d = 2;
output = 10 * d;
for i = 1:d
    output = output + x(i) .^ 2 - 10 * cos(2*pi*x(i));
end

end

