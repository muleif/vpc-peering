#!/bin/bash
yum update -y
yum install httpd -y
chkconfig httpd on
cd /usr/share/httpd/noindex
chmod o+w /usr/share/httpd/noindex
echo "<h1>Hello World from CDK for python &#128578;</h1>" > index.html
systemctl start httpd
systemctl enable httpd