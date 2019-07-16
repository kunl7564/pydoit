#echo hi | mail -s "say hi3" -c chao.cao@coollu.com.cn -c zhoulu.luo@coollu.com.cn -c yao.chen@coollu.com.cn lk8823@qq.com

while true; 
do
top -n 2 -b > top.out

idle=`cat top.out | grep Cpu | tail -1 | awk '{print $8}'`;
echo $idle

#echo `top -n 1 -b`  | mail -s "say hi3" lk8823@qq.com;
sleep 5;

done;




