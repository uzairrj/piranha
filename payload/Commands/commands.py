import enum


import subprocess

class Commands:
    async def __shell(self, cmd):
        process = subprocess.Popen(cmd,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE)
        output = process.stdout.read().decode('utf-8')
        errcode = process.returncode

        if errcode is not None:
            raise Exception('cmd %s failed, see above for details', cmd)
        return output


    async def run(self, command, arg = None):
        command = command.lower()
        if  command == "shell":
            try:
                return await self.__shell(arg)
            except Exception as ex:
                return ex
