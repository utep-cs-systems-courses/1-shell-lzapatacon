import os,sys,time,re


def exec_pipe(exec_args, bg_enabled):
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
            
        exec_args = exec_args[:exec_args.index('|')]
        exec_program(exec_args)
        sys.exit(1)
    else:
        rc_2 = os.fork()

        if rc_2 < 0:
            os.write(1, 'Failed to fork second child.'.encode())
            sys.exit(1)

        elif rc_2 == 0:
            os.close(0)
            os.dup(inFd)
            os.set_inheritable(0,True)

            for fd in (outFd, inFd):
                os.close(fd)
            exec_args = exec_args[exec_args.index('|') + 1:]
            exec_program(exec_args)
            sys.exit(1)
        else:
            if bg_enabled is False:
                    os.wait()
        for fd in (inFd, outFd):
            os.close(fd)
        if bg_enabled is False:
            os.wait()

    
def exec_program(exec_args):
    for directory in re.split(":", os.environ['PATH']):
        program = "%s/%s" % (directory, exec_args[0])
        try:
            os.execve(program, exec_args, os.environ)
        except FileNotFoundError:
            pass
    os.write(1,("%s command not found.\n" % args[0]).encode())


def main():
    try:
        sys.ps1
    except AttributeError:
        sys.ps1 = "$ "

    inFd, outFd = os.pipe()
    for f in (inFd, outFd):
        os.set_inheritable(f,True)

    pid = os.getpid()


    args = ''
    while True:
        os.write(1, f'~{os.getcwd()}: {sys.ps1}'.encode())
        args = os.read(0,1000).decode().split()

        bg_enabled = True if '&' in args else False
        args = args [:-1] if bg_enabled else args

        if len(args) == 0:
            continue
        if args[0] == 'exit':
            sys.exit(1)

        if args[0] == 'cd':
            if len(args) == 1:
                os.chdir('/')
            else:
                try:
                    os.chdir(f'{args[1]}')
                except:
                    os.write(1,('Invalid directory: %s\n' % args[1]).encode())
        elif '|' in args:
            exec_pipe(args, bg_enabled)

        else:

            rc = os.fork()

            if rc < 0:
                sys.exit(1)
            elif rc == 0:
                error_state = False

                if '>' in args:
                    file_index = args.index('>')
                    os.close(1)

                    try:
                        os.open(args[file_index + 1], os.O_CREAT | os.O_WRONLY);
                        os.set_inheritable(1,True)
                        args = args[:file_index]
                    except FileNotFoundError:
                        error_state = False
                        os.write(1, ('bash: %s: No such file or directory' % args[file_index + 1]).encode())
                elif '<' in args:
                    file_index = args.index('<')
                    os.close(0)
                    try:
                        os.open(args[file_index + 1], os.O_RDONLY)
                        os.set_inheritable(0, True)
                        args = args[:file_index]
                    except FileNotFoundError:
                        error_state = True
                        os.write(1, ('bash: %s: No such file or directory \n' % args[file_index + 1]).encode())
                else:
                    if not error_state:
                        exec_program(args)

                    sys.exit(1)
            else:
                if bg_enabled is False:
                    os.wait()


if __name__ == "__main__":
    main()
