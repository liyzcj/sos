function [Position,Velocity] = Initial_position_velocity(Dimension,Size,Xmax,Xmin,Vmax,Vmin)
  for i=1:Dimension
      Position(i,:)=Xmin(i)+(Xmax(i)-Xmin(i))*rand(1,Size); % ��������Χ�ڵ����λ�ã�rand(1,Size)���ڲ���һ��Size�������
      Velocity(i,:)=Vmin(i)+(Vmax(i)-Vmin(i))*rand(1,Size);
  end
end
