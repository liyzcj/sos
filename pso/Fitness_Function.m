function Fitness=Fitness_Function(Pos,F_n,Dimension)
 switch F_n
    case 1
        Func_Sphere=Pos(:)'*Pos(:);
        Fitness=Func_Sphere;
    case 2
        res1=Pos(:)'*Pos(:)/4000;
        res2=1;
        for row=1:Dimension
            res2=res2*cos(Pos(row)/sqrt(row));
        end
        Func_Griewank=res1-res2+1;
        Fitness=Func_Griewank;
end

