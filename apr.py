import subprocess
from waflib.Configure import conf

def which(program):
    import os
    def is_exe(fpath):
        return os.path.exists(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

def get_compile_flags():
    p = subprocess.Popen(['apr-1-config', '--cflags', '--cppflags'],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, close_fds=False)
    stdout = p.communicate()[0]

    if p.returncode == 0:
        return stdout.strip().split()

    return nil

def get_include_flags():
    p = subprocess.Popen(['apr-1-config', '--includes'],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, close_fds=False)
    stdout = p.communicate()[0]

    if p.returncode == 0:
        return stdout.strip().split()

    return nil

def get_ld_flags():
    p = subprocess.Popen(['apr-1-config', '--link-ld', '--libs'],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, close_fds=False)
    stdout = p.communicate()[0]

    if p.returncode == 0:
        return stdout.strip().split()

    return nil

@conf
def check_apr(self):
    self.start_msg("Checking for apr")

    if not which('apr-1-config'):
        self.end_msg("no")
	self.fatal("apr-1-config could not be found")
        return False

    cflags = get_compile_flags()
    includes = get_include_flags()
    ldflags = get_ld_flags()

    self.env.append_unique("CFLAGS_APR", cflags)
    self.env.append_unique("CFLAGS_APR", includes)
    self.env.append_unique("LINKFLAGS_APR", ldflags)

    self.end_msg("ok")

    return True

def configure(conf):
    conf.check_apr()
