from waflib.Configure import conf
from waflib import Task
from waflib.TaskGen import extension

def options(opt):
    opt.add_option('--libprotobuf-c', action='store', default='/usr',
            dest='protobufc')

@conf
def check_protobuf_c(self):
    self.start_msg("Checking for the variable PROTOBUFC")

    if self.options.protobufc:
        self.env.PROTOBUFC = self.options.protobufc
        self.env.append_unique("CFLAGS_PROTOBUFC", "-I" + self.env.PROTOBUFC + '/include')
        self.env.append_unique("LIBPATH_PROTOBUFC", self.env.PROTOBUFC + '/lib')
        self.env.append_unique("LIB_PROTOBUFC", 'protobuf-c')
        self.end_msg(self.env.PROTOBUFC)
    else:
        self.end_msg("PROTOBUFC is not set")

    return True

class protobuf(Task.Task):
    """Compile protobuf files"""
    color   = 'BLUE'
    run_str = '${PROTOCC} -I${SRC[0].parent.abspath()} ${SRC[0].abspath()} --c_out=.'
    ext_out = ['.c', '.h'] # just to make sure

@extension('.proto')
def big_protobuf(self, node):
        """
        Create a protoc-c task, which must be executed from the directory of the output file.
        """

        outs = []
        outs.append(node.change_ext('.pb-c.c'))
        outs.append(node.change_ext('.pb-c.h'))

        tsk = self.create_task('protobuf', node, outs)
        tsk.cwd = node.parent.get_bld().abspath()

        # and the c file must be compiled too
        self.source.append(outs[0])

def configure(conf):
    conf.find_program('protoc-c', var='PROTOCC')
    conf.check_protobuf_c(mandatory=True)
