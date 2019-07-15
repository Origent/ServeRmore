# Laptop Manual Configuration

## Assumption

  * You have an AWS IAM or Master account with Command Line access key and secret key.
  * You have a Windows or MacBook.

## Standard Technical Configuration

  * For: MacOS or Windows 10
  * 1: Package Manager Setup
  * 2: Cloud Hosting Setup
  * 3: Source Code Repository Setup

## For Windows 10

1. We want to configure Windows Subsystem for Linux in order to gain the tools we need for our optimal analysis environment. ([Install Guide](https://msdn.microsoft.com/en-us/commandline/wsl/install_guide)).  
  Steps Include:  
  * Toggle on Windows Subsystem for Linux
  * Install Ubuntu Bash on Windows
  * Setup first user, use 'root' with 'root' password on Windows  
  We now have a default manager called "apt-get", which is part of Ubuntu Linux and available in the Ubuntu Bash shell on Windows.  We can use commands like the following to grab a software package and all dependencies.
  ```
  apt-get update
  apt-get upgrade
  apt-get install <package>
  ```

2. Next, we want to configure our cloud hosting provider, AWS.  Begin by confirming you have the following information and then install the AWS Command Line Interface with the steps provided.  
  Confirm the following:  
  * You have an IAM User account, Public Key, Secret Key, and Region.
  * Guide to install the AWS Command Line Interface ([Help](http://docs.aws.amazon.com/cli/latest/userguide/installing.html))
  * Change your Ubuntu Bash window to allow QuickEdit ([Help](https://stackoverflow.com/questions/38832230/copy-paste-in-bash-on-ubuntu-on-windows))
  ```
  cd ~
  apt-get -y update
  apt-get -y install python3-pip
  apt-get -y install awscli
  pip install --upgrade pip
  pip install awscli --upgrade --user
  aws configure
  ```
  * Complete the questions with our region and your IAM account information.
  * Use 'us-east-1' for region unless otherwise directed.

## For MacOS

1. We begin by installing a commonly used package manager called Homebrew, or brew for short. ([Install Homebrew](https://brew.sh/))
  * Running the following command in your terminal:
  ```
  /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
  ```
  * We can now use our package manager to install a software package and all its dependencies.
  ```
  brew update
  brew upgrade
  brew install <package>
  ```

2. Next, we want to configure our cloud hosting provider, AWS.  Begin by confirming you have the following information and then install the AWS Command Line Interface with the steps provided.  
  Confirm the following:  
  * You have an IAM User account, Public Key, Secret Key, and Region.
  * You have permissions to launch an AWS EC2 instance.
  * Guide to install the AWS Command Line Interface ([Help](http://docs.aws.amazon.com/cli/latest/userguide/installing.html))
  ```
  cd ~
  brew update
  brew install python3
  brew install awscli
  pip3 install --upgrade pip
  pip3 install awscli --upgrade --user
  aws configure
  ```
  * Complete the questions with our region and your IAM account information.
  * Use 'us-east-1' for region unless otherwise directed.

## For All

3. Setup your SSH key for AWS EC2.

  Please follow AWS instructions to setup your private key. Specifically, the section titled "Creating a Key Pair Using Amazon EC2".
  ([Instructions](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html#having-ec2-create-your-key-pair))

  We will assume moving forward that your AWS key will be named "aws.pem".  Place the keys inside of your ~/.ssh folder.  Change the permissions so SSH doesn't complain and prevent action.
  ```
  cd ~/.ssh
  chmod go-rwx ~/.ssh/aws.pem
  ```

  Add a '~/.ssh/config' file if it doesn't already exist, and make sure it references the two keys above.

  '~/.ssh/config':
  ```
  IdentityFile ~/.ssh/aws.pem
  ```

  Change the permissions of config so SSH doesn't complain and prevent action.
  ```
  cd ~/.ssh
  chmod go-rwx ~/.ssh/config
  ```
