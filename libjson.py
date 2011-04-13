from waflib.Configure import conf
from waflib import Task
from waflib.TaskGen import extension

def options(opt):
    opt.add_option('--libjson', action='store', default='/usr',
            dest='libjson')

@conf
def check_libjson(self):
    self.start_msg("Checking for the variable LIBJSON")

    if self.options.libjson:
        self.env.LIBJSON = self.options.libjson
        self.env.append_unique("CFLAGS_LIBJSON", "-I" + self.env.LIBJSON)
        self.env.append_unique("LIBPATH_LIBJSON", self.env.LIBJSON)
        self.end_msg(self.env.LIBJSON)
    else:
        self.end_msg("LIBJSON is not set")

    return True

def configure(conf):
    conf.check_libjson(mandatory=True)

