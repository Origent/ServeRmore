
import sys, config, builder

#1 - R package with methods
#2 - R model in storage
builder_instance = builder.Builder()

#3 - create VM
builder_instance.create()

#4 - push
builder_instance.push_handler()

#5 - package
builder_instance.package_to_s3()

#6 - deploy
builder_instance.update_lambda()

#7 - test
#builder_instance.status()
