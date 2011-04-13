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

def get_install_dir():
    p = subprocess.Popen(['apxs', '-q', 'LIBEXECDIR'],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, close_fds=False)
    stdout = p.communicate()[0]

    if p.returncode == 0:
        return stdout.strip()

    return ''

def get_include_flags():
    p = subprocess.Popen(['apxs', '-q', 'INCLUDEDIR'],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, close_fds=False)
    stdout = p.communicate()[0]

    if p.returncode == 0:
        return '-I' + stdout.strip()

    return ''

@conf
def check_apxs(self):
    self.start_msg("Checking for apxs")

    if not which('apxs'):
        self.end_msg("no")
	self.fatal("apxs could not be found")
        return False

    includes = get_include_flags()
    install_dir = get_install_dir()

    self.env.append_unique("CFLAGS_APXS", includes)
    self.env.append_unique("INSTALL_DIR", install_dir)

    self.end_msg("ok")

    return True

def configure(conf):
    conf.check_apxs()
