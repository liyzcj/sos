clc
clear
%% initial parameters
% parameters to input
c1 = 2;
c2 = 2; % learning factor
w = 1; % weight
dimension = 2;
size = 10;
iters = 100;
result = zeros(iters,1);
% funtion f
func = @griewank;
% initial vector of velocity max and min
vmax = 10;
vmin = -10;
% initial vector of position max and min
xmax = 600;
xmin = -600;

% Initial position and velocity accroding to limitation.
position = rand(size, dimension) * (xmax - xmin) + xmin;
velocity = rand(size, dimension) * (vmax - vmin) + vmin;

% Initial pbest and gbest
pbest = position;
f = zeros(size,1);
fbest = zeros(size,1);
%% Iterations
for it = 1:iters
    %% set Pbest and Gbest
    % compute fitness and compare with pbest( function f)
    for i = 1:size
        f(i) = func(position(i,:));
        fbest(i) = func(pbest(i,:));
        if f(i) < fbest(i)
            pbest(i,:) = position(i,:);
        end
    end
    % set gbest
    [result(it), pos] = min(fbest);
    gbest = pbest(pos,:);
    
    %% calculate new velocity
    for i = 1:size
        % velocity
        velocity(i,:) = w * velocity(i,:) + c1 * rand * (pbest(i,:) - position(i,:)) + c2 * rand * (gbest - position(i,:));
    end
    
    %% Limitations
    % velocity limitation
    velocity(velocity > vmax) = vmax;
    velocity(velocity < vmin) = vmin;
    % compute new position
    position = position + velocity;
    % position limitation
    position(position > xmax) = xmax;
    position(position < xmin) = xmin;
end
    

plot(result)
xlabel('iterations');
ylabel('fitness');