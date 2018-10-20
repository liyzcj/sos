clc
clear
%% initial parameters
% parameters to input
c1 = 2;
c2 = 2; % learning factor
w = 1; % weight
dimension = 1;
size = 5;
iters = 100;
% funtion f

% initial vector of velocity max and min
vmax = 300;
vmin = -300;
% initial vector of position max and min
xmax = 300;
xmin = -300;

% Initial position and velocity accroding to limitation.
position = rand(size, dimension) * (xmax - xmin) + xmin;
velocity = rand(size, dimension) * (vmax - vmin) + vmin;

% Initial pbest and gbest
pbest = position;
f = zeros(size,1);

for it = 1:iters
   
    %% compute fitness and compare with pbest( function f)
    for i = 1:size
        f(i) = func(position(i,:));
        if f(i) < func(pbest(i,:))
            pbest(i,:) = position(i,:);
        end
    end
    %% set gbest
    [~, pos] = min(f);
    gbest = position(pos,:);
    
    %% calculate new velocity
    for i = 1:size
        % velocity
        velocity(i,:) = w * velocity(i,:) + c1 * rand * (pbest(i,:) - position(i,:)) + c2 * rand * (gbest - position(i,:));
    end
    
    %% velocity limitation
    velocity(velocity > vmax) = vmax;
    velocity(velocity < vmin) = vmin;
    %% compute new position
    position = position + velocity;
    %% position limitation
    position(position > xmax) = xmax;
    position(position < xmin) = xmin;
end
    