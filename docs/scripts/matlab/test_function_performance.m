bounds = {
    [1, 1; 0, 0];
    [1, 1, 1, 1; 1e-8, 0, 0, 0];
    [1, 1, 1, 1; 0, 0, 0, 0];
    [0.15,50000,115600,1110,116,820,1680,12045; 0.05,100,63070,990,63.1,700,1120,9855];
};

functions = {
    @curretal88exp, @curretal88explc;
    @park91a, @park91alc;
    @park91b, @park91blc;
    @borehole, @boreholelc;
};
func_names = ["Currin", "Park91A", "Park91B", "Borehole"];

fidelities = ["high", "low"];

ex_start = 0;
num_ex = 7;

num_cases = numel(functions)*num_ex;

Ndim = zeros(num_cases, 1);
Name = strings([num_cases, 1]);
Size = zeros(num_cases, 1);
Fidelity = strings([num_cases, 1]);
Number = zeros(num_cases, 1);
Time_per = zeros(num_cases, 1);
Norm_time_per = zeros(num_cases, 1);

idx = 0;

for i=1:size(functions)
    
    boundaries = bounds{i};
    ubound = boundaries(1,:);
    lbound = boundaries(2,:);
    
    disp(functions{i,1});
    
    for j=1:2
        for ex = ex_start:(ex_start + num_ex - 1)
            idx = idx + 1;
            
            [elapsed, n] = mytiming(functions{i,j}, ubound, lbound, 10^ex);
            time_per = elapsed/n;
            
            fprintf("%7d: %f (%7d)\n", 10^ex, time_per, n);
            
            if ex == ex_start
                base_time = time_per;
            end
            
            Ndim(idx) = numel(ubound);
            Name(idx) = func_names(i);
            Size(idx) = 10^ex;
            Fidelity(idx) = fidelities(j);
            Number(idx) = n;
            Time_per(idx) = time_per;
            Norm_time_per(idx) = time_per / base_time;
            
        end
    end
end

var_names = ["ndim", "name", "size", "fidelity", "number", "time_per", "norm_time_per"];

t = table(Ndim, Name, Size, Fidelity, Number, Time_per, Norm_time_per,'VariableNames',var_names);

disp(t);
writetable(t, 'time_scaling_matlab.csv');