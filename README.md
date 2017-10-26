# aws-boto2-api
This is a super-class of boto2 lib, which integrates the basic features in boto2


# Notice
- All private information is inside the config.py
- You need to built it yourself


## Todo - Inside the service - Initialization

## Inside the service - Supervisor Setting
1. ssh -i "yinhaoti.pem" ec2-user@ec2-18-216-120-1.us-east-2.compute.amazonaws.com
2. cd /etc/supervisor/  
3. supervisord -c ../supervisord.conf 
4. ps ax | grep python
5. kill 17306
6. supervisord -c ../supervisord.conf 

# Todo
1. Build a new key-pair, and replace the new key-pair to the existing instance
