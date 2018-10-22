function [output] = rosenbrock(x)
%ROSENBROCK Rosenbrock Function

output = 100 * (x(2) - x(1).^2).^2 + (x(1) - 1).^2;
end

