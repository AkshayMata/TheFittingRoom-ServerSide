# TheFittingRoom-ServerSide

Configuring the Server
1.	Set up account with AWS and follow the default instructions for launching instance, which includes the Amazon Machine Image (based on RedHat).   When setting up the security group, enable inbound traffic for HTTP and SSH on port range 80 and 22, respectively.  The source can be defined by the user’s requirements. 

2.	Next, SSH into your amazon instance. Make sure that you are SSHing from the same directory as your key-pair file, as it will be the first argument in SSH command. The command that we used was  ssh -i ./admin-key-pair-useast.pem ec2-user@ec2-54-210-37-207.compute-1.amazonaws.com, however the second argument will be depend on the public DNS of your instance. 

3.	Once you have successfully connected to your instance, install MongoDB. The command that we used to install MongoDB was sudo yum install –y mongodb-org. The install guide can be seen in MongoDB documentation.  

4.	Then install Apache using the sudo yum install httpd command followed by the sudo service httpd start. Refer to step one in the Digital Ocean installation guide for LAMP on RedHat. 

5.	Next, follow the digital installation guide for how to deploy a flask application on an Ubuntu VPS . Keep in mind that the sudo apt-get commands will not work on Amazon Linux as it is based on RedHat. The sudo apt-get install libapache2-mod-wsgi python-dev will need to be replaced with sudo yum install mod_wsgi pythonXX-devel, where XX is your python version number. The sudo apt-get install python-pip command will be replaced with sudo yum install python-pip. 


6.	Install Pymongo using sudo pip install pymongo. 

7.	Install the Nose module using sudo pip install nose. 

8.	Modify the __init__.py file created in step 5, to include the web service API that will used by the client applications.  

Useful Links
  http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html

  http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/authorizing-access-to-an-instance.html
  
  https://docs.mongodb.org/manual/tutorial/install-mongodb-on-amazon/
  
  https://www.digitalocean.com/community/tutorials/how-to-install-linux-apache-mysql-php-lamp-stack-on-centos-6
  
  https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps




