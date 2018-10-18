c1=2;%ѧϰ����
c2=2;%ѧϰ����
Dimension=20;
Size=30;
Tmax=500;
Velocity_max=1200;%��������ٶ�
 
F_n=2;%���Ժ�����
 
Fun_Ub=600;%�������½�
Fun_Lb=-600;
Position=zeros(Dimension,Size);%����λ��
Velocity=zeros(Dimension,Size);%�����ٶ�
Vmax(1:Dimension)=Velocity_max;%�����ٶ����½�
Vmin(1:Dimension)=-Velocity_max;
Xmax(1:Dimension)=Fun_Ub;%����λ�����½磬�������Ա��������½�
Xmin(1:Dimension)=Fun_Lb;
[Position,Velocity]=Initial_position_velocity(Dimension,Size,Xmax,Xmin,Vmax,Vmin);
 
Pbest_position=Position;%���ӵ���ʷ����λ�ã���ʼֵΪ���ӵ���ʼλ�ã��洢ÿ�����ӵ���ʷ����λ��
Gbest_position=zeros(Dimension,1);%ȫ�����ŵ��Ǹ���������λ�ã���ʼֵ��Ϊ�ǵ�1������
 
for j=1:Size
    Pos=Position(:,j);%ȡ��j�У�����j�����ӵ�λ��
    fz(j)=Fitness_Function(Pos,F_n,Dimension);%�����j�����ӵ���Ӧֵ
end
[Gbest_Fitness,I]=min(fz);%���������Ӧֵ����С���Ǹ���Ӧֵ������ø����ӵ�λ��
Gbest_position=Position(:,I);%ȡ��С��Ӧֵ���Ǹ����ӵ�λ�ã���I��
 
for itrtn=1:Tmax
time(itrtn)=itrtn;
 
Weight=1;
r1=rand(1);
r2=rand(1);
for i=1:Size
   Velocity(:,i)=Weight*Velocity(:,i)+c1*r1*(Pbest_position(:,i)-Position(:,i))+c2*r2*(Gbest_position-Position(:,i));
end
%�����ٶȱ߽�
for i=1:Size
    for row=1:Dimension
        if Velocity(row,i)>Vmax(row)
            Veloctity(row,i)=Vmax(row);
        elseif Velocity(row,i)<Vmin(row)
            Veloctity(row,i)=Vmin(row);
        else
        end
    end
end
 
Position=Position+Velocity;
 
%����λ�ñ߽�
for i=1:Size
    for row=1:Dimension
        if Position(row,i)>Xmax(row)
            Position(row,i)=Xmax(row);
        elseif Position(row,i)<Xmin(row)
            Position(row,i)=Xmin(row);
        else
        end
    end
end
 
  for j=1:Size
     P_position=Position(:,j)';%ȡһ�����ӵ�λ��
     fitness_p(j)=Fitness_Function(P_position,F_n,Dimension);
     if fitness_p(j)< fz(j) %���ӵ���Ӧֵ���˶�֮ǰ����ӦֵҪ�ã�����ԭ������Ӧֵ
         Pbest_position(:,j)=Position(:,j);
         fz(j)=fitness_p(j);
     end
     if fitness_p(j)<Gbest_Fitness
         Gbest_Fitness=fitness_p(j);
     end
  end
  [Gbest_Fitness_new,I]=min(fz);%���º���������ӵ���Ӧֵ��ȡ��С���Ǹ������������
   Best_fitness(itrtn)=Gbest_Fitness_new; %��¼ÿһ���������Ӧֵ
   Gbest_position=Pbest_position(:,I);%�����Ӧֵ��Ӧ�ĸ�������λ��
end
plot(time,Best_fitness);
xlabel('�����Ĵ���');ylabel('��Ӧ��ֵP_g');
