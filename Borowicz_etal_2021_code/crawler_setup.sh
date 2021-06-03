#!/bin/bash

## installing geckodriver
if [ ! -d "geckodriver" ]; then
	echo "Installing geckodriver..."
	wget https://github.com/mozilla/geckodriver/releases/download/v0.16.0/geckodriver-v0.16.0-linux64.tar.gz
	mkdir -p geckodriver && tar zxvf geckodriver-v0.16.0-linux64.tar.gz -C geckodriver
	rm geckodriver-v0.16.0-linux64.tar.gz
fi

## installing phantomjs
if [ ! -d "phantomjs-2.1.1-linux-x86_64" ]; then
	echo "Installing phantomjs..."
	wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
	tar xvjf phantomjs-2.1.1-linux-x86_64.tar.bz2
	rm phantomjs-2.1.1-linux-x86_64.tar.bz2
fi

export PATH=${PATH}:${PWD}/geckodriver
export PATH=${PATH}:${PWD}/phantomjs-2.1.1-linux-x86_64/bin


## starting a cluster with iPython Parallel 
ipcluster start -n 8 --engines=MPIEngineSetLauncher &

## loading Jupyter with no browser for SSH-tunneling to port 8900
jupyter notebook --no-browser --port=8900 &