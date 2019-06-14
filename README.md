## Lunatech News Bot

This slack bot tries to keep the developers up-to-date by providing the top voted contents from specific subreddits and some stackexchange sites.

The aim is providing a couple of links from different verticals every day around 08:30 European time so that our engineers can read about new stuff before work. The bot also tries not making too much noise by keeping the new links not more than five each day.

The exact schedule of the bot is as follows;

```
|                     | schedule              |  time | rate                     |
|---------------------+-----------------------+-------+--------------------------|
| reddit              |                       |       |                          |
|---------------------+-----------------------+-------+--------------------------|
| r/programing        | everyday              | 08:30 | daily best (1 - link)    |
| r/scala             | monday                | 08:30 | weekly best (1 - link)   |
| r/linux             | tuesday               | 08:30 | weekly best (1 - link)   |
| r/devops            | wednesday             | 08:30 | weekly best (1 - link)   |
| r/netsec            | thursday              | 08:30 | weekly best (1 - link)   |
| r/programmerhumor   | friday                | 08:30 | weakly best (3 - links)  |
| r/dataisbeautiful   | saturday              | 08:30 | weekly best (3 - links)  |
|---------------------+-----------------------+-------+--------------------------|
| stack-exchange      |                       |       |                          |
|---------------------+-----------------------+-------+--------------------------|
| stackoverflow       | 1st day of the month  | 08:45 | monthly best (3 - links) |
| superuser           | 6th day of the month  | 08:45 | monthly best (3 - links) |
| serverfault         | 12th day of the month | 08:45 | monthly best (3 - links) |
| unix-linux          | 18th day of the month | 08:45 | monthly best (3 - links) |
| softwareengineering | 24th day of the month | 08:45 | monthly best (3 - links) |
|                     |                       |       |                          |
```

### Architecture

The bot runs on top of AWS Lambda, Cloudwatch Events and API Gateway. All deployed using serverless framework. (https://serverless.com/) Serverless framework also handles setting up required IAM roles and logging to Cloudwatch logs.

There is only 3 lambda function, they all use python-3.6 runtime. The stack looks like below;

![Slackbot Diagram](https://i.imgur.com/n65IrDE.png "Slackbot Diagram")


### Contribution Guide

**Requirements**
- Make sure you have python 3.6 installed in your system. You will also need to install pipenv package to setup a virtual environment and install python dependencies.
- Make sure you have npm installed in your system to download serverless framework and it's plugins.

**Installation**

1) Clone the repository
```
$ git clone git://github.com/lunatech/lunatech-news-bot.git
```

2) Initiallize npm
```
$ cd lunatech-news-bot
$ npm install
```

3) Install python dependencies
```
$ cd lunatech-news-bot
$ pipenv install
$ # you should be able to activate python shell with all the dependencies at this moment
$ pipenv shell
```

**Decrypting Sensitive Data**
There is one file in this repository wihch is encrypted using `git-crypt`. The file is just holding somewhat sensitive key-value pairs.

```
$ cat app/settings.py
SLACK_HOOK_URL = "....."
STACK_EXCHANGE_KEY = "...."
SUMMRY_API_KEY = "...."
```

`git-crypt` looks at the `.gitattributes` file on the root folder and encrypts/decrypts the specified files transparantly. Please see the git-crypt documentation for the details, and ask for the private key that encrypts this repository.

**Testing Locally**

Python modules in lambda functions have a strange behaviour. Thus, you cannot run the scripts directly in the app folder. You have to invoke them from the root folder. Instead, for testing, there is a very simple `run.py` file in the top folder. Running this script with python will import the modules correctly.

Please make sure you don't use the same `settings.py` file while testing, launch your own slack, use your own hook urls, otherwise you will directly send messages to the lunatech's related channel.

**Testing In Cloud**

You can also invoke lambda functions locally that is deployed to AWS. (As long as you have `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` variables are set on your workstation)

To do so, run the below command.
```
$ serverless invoke -f reddit --log
```

**Deployment**
You can deploy this to any AWS account with the below command.

```
$ serverless deploy
```

This will package the python module, create a cloudformation template and deploy it to the AWS.
