%% Ant System for TSP problem

clearvars;
close all;
clc;


%% STEP 1: Initialize
% load map1.txt; % load map
% d = map1;
load map.mat;
d = D;

nc = size(d, 1); % number of cite

K = 50; % number of ant (equal number of cite)
iters = 200; % number of iteration
Q = 100;    % Pheromone increase factor

alpha = 1;  % importance of pheromone
beta = 5;   % importance of heuristics
rho = 0.1;  % Pheromone attenuation factor

eta = 1./d; % heuristic factor = 1 / d
tau = ones(nc,nc); % initial matric of pheromone
iter = 1; % initial iteration

best_path_iter = zeros(iters, nc); % best path for every iter
best_length_iter = inf.*ones(iters, 1);  % best length for every iteration
iter_avg_length = zeros(iters, 1);  % avg lenth for iteration


while iter<=iters
    
    %% STEP 2: Put ants in city randomly
    path = zeros(K, nc); % path of each ant
    L = zeros(K,1); % path length for each ant
    % put ant in city randomly
    for ant = 1:K
        path(ant,1) = unidrnd(nc);
    end
    %% STEP 3: Choose next city for every ant
%%%%%%%%%%%% 找不到最优值，待解决。
%     for ant = 1:K
%         visiting = path(ant,1); % current visiting city
%         allowed = 1:nc; % cites can be reached
%         allowed(allowed == visiting) = []; % remove visiting city
%         for n = 2:nc
%             p_trans = tau ^ alpha .* eta ^ beta;
%             p = p_trans(visiting, allowed);
%             p = p / sum(p);
%             % randomly choose next city accroding to the probabilites
%             pcum = cumsum(p);
%             next = allowed(pcum >= rand);
%             next = next(1);
%             % add next city to path and remove from allowed
%             path(ant,n) = next; 
%             allowed(allowed == next) = [];
%             % add length
%             L(ant) = L(ant) + d(visiting, next);
%             % set new visiting city
%             visiting = next;
%         end
%         % add length last city to the first city
%         L(ant) = L(ant) + d(visiting, path(ant, 1));
%     end
%     if iter >= 2
%         path(1,:) = best_path_iter(iter -1 ,:);
%         L(1) = best_length_iter(iter -1 ,:);
%     end
    
    for step = 2:nc
        for ant = 1:K
            visited = path(ant,1:(step-1)); % visited cites
            allowed=zeros(1,(nc-step+1)); % allowed cites
            P = allowed; % initial probability of tranport
            % initial allowed cites, cites not in visited
            Jc = 1;
            for k = 1:nc
                if isempty(find(visited == k, 1))
                    allowed(Jc) = k;
                    Jc = Jc + 1;
                end
            end
            % compute probability of transport
            for k = 1:length(allowed)
                P(k) = (tau(visited(end),allowed(k)) ^ alpha) * (eta(visited(end), allowed(k)) ^ beta);
            end
            P=P/(sum(P));
            % randomly choose next according probability
            Pcum = cumsum(P);
            next=find(Pcum>=rand);
            to_visit=allowed(next(1));
            % add next visit city to path
            path(ant,step)=to_visit;
        end
    end
    % add best path in last iteration to current one 
    if iter>=2
        path(1,:) = best_path_iter(iter -1 ,:);
    end
    % compute best length
    for ant = 1:K
        p = path(ant,:);
        for step = 1:(nc-1)
            L(ant) = L(ant) + d(p(step),p(step + 1));
        end
        % length for the last step
        L(ant) = L(ant) + d(p(nc),p(1));
    end
    
    %% STEP 4: Save best solution
    %save best length and path for this iteration
    best_ant = find(L == min(L));
    best_length_iter(iter) = L(best_ant(1));
    best_path_iter(iter,:) = path(best_ant(1),:); 
    iter_avg_length(iter) = mean(L);
    best_length_iter(iter)
    %% STEP 5: Update Pheromone
    delta_tau = zeros(nc,nc);
    for ant = 1:K
        for n = 1:(nc-1)
            % pheromone for ant in path n -> n+1
            delta_tau(path(ant,n),path(ant,n+1)) = ...
                delta_tau(path(ant,n),path(ant,n+1)) + Q/L(ant);
        end
        %pheromone from last city to first
        delta_tau(path(ant,n),path(ant,1)) = ...
            delta_tau(path(ant,n),path(ant,1)) + Q/L(ant);
    end
    % Pheromone attenuation 
    tau = (1 - rho) .* tau + delta_tau;
    iter = iter + 1; % update iter
end

%% STEP 6: Computer best solution global

best_iter = find(best_length_iter==min(best_length_iter));
best_length = best_length_iter(best_iter(1));
best_path = best_path_iter(best_iter(1),:);

%% STEP 7: Plot picture

figure(1)
plot(best_length_iter)
hold on
plot(iter_avg_length,'r')
legend('length','avg length')
xlabel('iteration')
ylabel('length')
title('length of iteration')


            
