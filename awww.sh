for ((users=50; users<301; users+=50))
do
python3 simulator.py ${users}
mv -v devices.json edrsync-${users}.json
done 
mv edrsync-*.json /home/leonisio/Desktop/Todo-JustDone/Thesis/THESIS/src/plotPerDeviceNumber
