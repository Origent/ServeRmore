
import sys, builder

#1 - R package with methods
#2 - R model in storage

#3 - create
builder_instance = builder.Builder()
#builder_instance.setup()
builder_instance.create("adc_test")
#builder_instance.ssh()
#builder_instance.terminate()

#4 - update
#builder_instance.update()

#5 - package
#builder_instance.package()

#6 - deploy
#builder_instance.deploy()

#7 - test
#builder_instance.test()

#8 - terminate
