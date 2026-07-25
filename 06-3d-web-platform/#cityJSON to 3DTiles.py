#cityJSON to 3DTiles
import subprocess
from pathlib import Path
import os

scr_path = os.path.dirname(__file__)
data_path = os.path.join(scr_path,'..',"05-ifc2cityjson", "output.city.json")

output = os.path.join(scr_path,"tiles")

Path(output).mkdir(exist_ok=True)

subprocess.run(["cj23dtiles", "convert",data_path, "-o", output], capture_output=True)