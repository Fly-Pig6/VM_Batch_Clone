import subprocess
import yaml
import pathlib


class Batcher():
    def __init__(self, filepath: str, fail_ignore: bool=True):
        self.fail_ignore = fail_ignore

        # 读取 yaml 配置
        with open(filepath, 'r', encoding='utf-8') as f:
            conf = yaml.safe_load(f)

        self.source = conf['source']            
        self.executable = conf['executable']    # vmrun.exe
        self.copies = conf['copies']            

    def run(self):

        for copy in self.copies:
            error_debug = 0                     
            copy_name = copy['name']
            is_linked = copy['linked']
            is_started = copy['started']
            copy_dest = copy['dest']
            dest = pathlib.Path(copy_dest) / copy_name / f"{copy_name}.vmx" 
            print(dest)

            try:
                subprocess.run(
                    [
                        self.executable,
                        "clone",
                        self.source,
                        dest,
                        'linked' if is_linked else 'full',
                        f'-cloneName={copy_name}'
                    ],
                    check=True
                )
            except:
                error_debug = 1
                print(f"\033[31m-> {copy_name} creat failed.\033[0m")
                if not self.fail_ignore: exit(1)

            if not error_debug:
                print(f"\033[32m-> {copy_name} created successfully.\033[0m")

            if is_started:
                print(f"Starting {copy_name}..")
                try:
                    subprocess.run(
                        [
                            self.executable,
                            "start",
                            dest
                        ],
                        check=True
                    )
                except:
                    print(f"\033[31m-> {copy_name} start failed.\033[0m")
                    if not self.fail_ignore: exit(1)


if __name__ == "__main__":
    bat = Batcher('configure.yml', fail_ignore=True)
    bat.run()
