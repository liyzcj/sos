function [output] = rosenbrock(x)
%ROSENBROCK �˴���ʾ�йش˺�����ժҪ
%   �˴���ʾ��ϸ˵��
output = 100 * (x(2) - x(1).^2).^2 + (x(1) - 1).^2;
end

