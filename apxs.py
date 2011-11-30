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

def get_install_dir(cfg):
    p = subprocess.Popen([cfg.env.APXS, '-q', 'LIBEXECDIR'],
                           stdout=subprocess.PIPE,
                           close_fds=False)
    stdout = p.communicate()[0]

    if p.returncode == 0:
        return stdout.strip()

    return ''

def get_include_flags(cfg):
    p = subprocess.Popen([cfg.env.APXS, '-q', 'INCLUDEDIR'],
                           stdout=subprocess.PIPE,
                           close_fds=False)
    stdout = p.communicate()[0]

    if p.returncode == 0:
        return '-I' + stdout.strip()

    return ''

def get_include_dir(cfg):
    p = subprocess.Popen([cfg.env.APXS, '-q', 'INCLUDEDIR'],
                           stdout=subprocess.PIPE,
                           close_fds=False)
    stdout = p.communicate()[0]

    if p.returncode == 0:
        return stdout.strip()

    return ''

@conf
def check_apxs(self):
    self.start_msg("Checking for apxs")

    self.find_program('apxs', var='APXS')

    includes = get_include_flags(self)
    include_dir = get_include_dir(self)
    install_dir = get_install_dir(self)

    self.env.append_unique("CFLAGS_APXS", includes)
    self.env.append_unique("APXS_INCLUDE_DIR", include_dir)
    self.env.append_unique("INSTALL_DIR", install_dir)

    self.end_msg("ok")

    return True

def configure(conf):
    conf.check_apxs()
