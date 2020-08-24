function [elapsed, n] = mytiming(func, ubound, lbound, N)
    n = 1;
    elapsed = 0;
    
    XX = rand(N, numel(ubound));
    XX = myscale(XX, ubound, lbound);
     
    while elapsed < 0.2
        start = cputime;
        for rep = 1:n
            for i=1:N
                func(XX(i,:));
            end
        end

        elapsed = cputime - start;
        n = n*10;
    end
    n = n/10;
end