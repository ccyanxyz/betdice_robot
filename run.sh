# cleanup
pkill keosd
pkill Python
pkill python3
keosd > keosd.log 2>&1 &

while true
do
	python3 turbo_boost.py 300 > turbo.log 2>&1 &
	sleep 500
	pkill Python
	pkill python3
	echo kill and restart...
done

