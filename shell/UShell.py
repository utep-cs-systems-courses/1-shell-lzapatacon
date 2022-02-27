import os,sys,time,re


def ecex_pipe(exec_args, bg_enabled):
    inFD,outFd = os.pipe()
    for fd in (infd, outFd):
        os.set_inheritable(fd, True)

    rc = os.fork()

    if rc < 0:
        os.write(1, "fork unstable".encode())
        sys.exit(1)

    elif rc == 0:
        os.close(1)
        os.dup(outFd)
        os.set_inheritable(1,True)

        #Close all pipes
    for fd in (inFd, outFd):
        od.close(fd)
        exec_program(exec_args(:exec_args.index('|')])
        sys.exit(1)
    else:
        if bg_enabled:
            os.wait()
    
