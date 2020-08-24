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

output_files = [
    "output_2d_Currin_high.mat", "output_2d_Currin_low.mat";
    "output_4d_Park91A_high.mat", "output_4d_Park91A_low.mat";
    "output_4d_Park91B_high.mat", "output_4d_Park91B_low.mat";
    "output_8d_Borehole_high.mat", "output_8d_Borehole_low.mat";
];

allowed_error = 1e-4;

for i=1:size(functions)
    boundaries = bounds{i};
    ubound = boundaries(1,:);
    lbound = boundaries(2,:);
    
    fname = sprintf("input_%dd.mat", numel(ubound));
    xx = load(fname).array;
    xx = myscale(xx, ubound, lbound);
    
    for j=1:2
        func = functions{i,j};
        disp(func);
        output = load(output_files(i,j)).array;
        for k=1:size(xx)
            if abs(func(xx(k,:)) - output(k)) > allowed_error
                disp("failed");
                disp(func(xx(k,:)));
                disp(output(k));
                break;
            end
        end
        disp("done");
    end
end
