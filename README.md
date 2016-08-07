#serverless-blink1

[![serverless](http://public.serverless.com/badges/v3.svg)](http://www.serverless.com)

A serverless endpoint to push and fetch [blink(1)](http://blink1.thingm.com/) LED color codes.

This project uses:

* python2.7 (because Lambda)
* [Serverless Framework](https://github.com/serverless/serverless)
* [boto3](https://boto3.readthedocs.io/en/latest/)
* [pyresttest](https://github.com/svanoort/pyresttest) for testing


##Install

Make sure you have the [Serverless Framework](http://www.serverless.com) installed and you're using Node.js v4.0+. 
```
npm install serverless -g
```

Install the project using Serverless:
```
serverless project install serverless-blink1
```

Install Python dependencies via pip:
```
pip install -t restApi/vendored/ -r restApi/requirements.txt
```

or via virtualenv:
```
virtualenv myenv
source myenv/bin/activate
pip install -r restApi/requirements.txt
cp -R myenv/lib/python2.7/site-packages/* restApi/vendored/
```



Deploy your functions and endpoints:
```
serverless dash deploy
```

##Usage

###Publish

This is where you get creative. Really, you can hook this up to *anything*, it's just a HTTP PUT. Wrap it in your custom logic.

I often use [httpie](http://radek.io/2015/10/20/httpie/) instead of curl. Try this out:

	#~: http POST https://yourAPIGateway/dev/blink1 endpoint=derp --json
	"derp"

	#~: http PUT https://yourAPIGateway/dev/blink1/derp rgb=#123456 --json
	"#123456"

	#~: http GET https://yourAPIGateway/dev/blink1/derp --json
	"#123456"

The most effective publisher I've used was [Nagios Check_MK Business Intelligence](https://mathias-kettner.de/checkmk_bi.html) because it handled aggregation logic. I'll write a [blog](http://sitereliability.engineer/) post about it sometime soon.

I'm currently experimenting with two publishers: outgoing webhooks from Slack and DataDog.

###Consume

On **Mac** and **Windows**, use [Blink1Control](http://blink1.thingm.com/blink1control/).

1. navigate to the *Tools* tab
2. click *+*
3. enter a *Name*
4. set *Type* as **url**
5. paste your endpoint in *Path*
6. set *Frequency* to **1 min** or **5 min**

I haven't tested this on **linux**, but try using [blink1-tool](http://blink1.thingm.com/blink1-tool/) and setting a cron like so:

	* * * * * /path/to/blink1-tool --rgb `derp=$(http GET https://yourAPIGateway/dev/blink1/derp | grep '#' | awk '{ print substr($1, 3, 6) }') ; echo "0x${derp:0:2},0x${derp:2:2},0x${derp:4:2}"`
