# sarcasmNLP
Using sentiment analysis and Emojis to enhance sarcasm detection in tweets

## Setting up python virtualenv
```
sudo yum install --user python3-pip
pip3 install virtualenv
python3 -m virtualenv env
source env/bin/activate
```

## Useful command-line commands
Set up AWS CLI.

SSH into EC2 instance:
```
ssh -i /path/my-key-pair.pem user_name@public_dns_name
ssh -i nlp_tweet_stream.pem ec2-user@ec2-18-208-250-4.compute-1.amazonaws.com
```
`Ctrl + d` to exit from ssh connection

Copy files from local computer to EC2 instance:
```
scp -i /path/my-key-pair.pem /path/SampleFile.txt ec2-user@ec2-18-208-250-4.compute-1.amazonaws.com:~/path/to/folder/
```
