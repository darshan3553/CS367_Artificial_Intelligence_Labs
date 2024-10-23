Q = zeros(1, 10);
N = zeros(1, 10);
R = zeros(1, 10000);
epsilon = 0.1;
m = ones(1, 10);
alpha = 0.7;

for i=1:10000
    if rand > epsilon
        [a, id] = max(Q);
        A = id;
    else 
        temp = randperm(10);
        A = temp(1);
    end
    [RR, m] = nonStatReward(A, m)
    N(A) = N(A)+1;
    Q(A) = Q(A) + (RR-Q(A))*alpha;
    if i==1
        R(i) = RR;
    else
        R(i) = ((i-1)*R(i-1) + RR)/i;
    end
    
end

i = 1:10000;
plot(i, R, 'r');

figure
plot(1:1000,avg,"red")
