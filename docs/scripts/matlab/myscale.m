function [out] = myscale(xx, ubound, lbound)
%UNTITLED2 scale xx to within [ubound, lbound] assuming xx is from [0, 1]

s = ubound - lbound;
out = xx .* s;
out = out + lbound;

end

