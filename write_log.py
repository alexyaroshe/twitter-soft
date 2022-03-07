from time import localtime, strftime


def write_log(lines):
    logtime= strftime("%Y-%m-%d %H:%M:%S", localtime())
    with open("_logs.txt", "a") as logs_file:
        logs_file.writelines([f"{logtime} {line}\n" for line in lines.splitlines()])