while getopts "kspl:" arg
do
	case $arg in
		k)
			ssh do 'cd ./eos && ./killall.sh > /dev/null 2>&1'
			ssh ny 'cd ./eos && ./killall.sh > /dev/null 2>&1'
			echo 'all robots killed'
			;;
		s)
			ssh do "cd ./eos && ./run.sh > run.log 2>&1 &"
			ssh ny "cd ./eos && ./run.sh > run.log 2>&1 &"
			echo 'all robots started'
			;;
		p)
			echo 'singapore:'
			ssh do ps -ef | grep python3
			ssh do ps -ef | grep run.sh
			echo 'newyork:'
			ssh ny ps -ef | grep python3
			ssh ny ps -ef | grep run.sh
			;;
		l)
			echo 'reset limit'
			ssh do 'cd ./eos && ./killall.sh > /dev/null 2>&1'
			ssh do "cd ./eos && ./run.sh $OPTARG > run.log 2>&1 &"
			echo 'singapore done.'
			ssh ny 'cd ./eos && ./killall.sh > /dev/null 2>&1'
			ssh ny "cd ./eos && ./run.sh $OPTARG > run.log 2>&1 &"
			echo 'newyork done.'
			;;
	esac
done
