function [output] = rosenbrock(x)
%ROSENBROCK 此处显示有关此函数的摘要
%   此处显示详细说明
output = 100 * (x(2) - x(1).^2).^2 + (x(1) - 1).^2;
end

