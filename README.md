
# Welcome to my CDK Python project!

In this project, were creating a custom vpc with 4 subnets
2 private subnet and 2 public subnet
We will launch an ec2 instance in of the private subnets of the custom vpc.


Additionally, we will make use of the custome vpc by importing it to out stack
We will launch and ec2 instanece in one of the public subnets.
We will install a webserver in the instance and then open port 22 and 80
 
 
We will establish a peering connection between the two vpc and test if the connection is working.
We will ping the private instance from the publick instance using the private ipv 




The `cdk.json` is where we have stored our parameters

To manually create a virtualenv on MacOS and Linux:

```
$ python -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```
If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
