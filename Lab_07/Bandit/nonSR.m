function [value, m] = bandit_nonstat(action, m)
v = normrnd(0,0.01, [1, 10]);
m = m + v;
value = m(action)
end
