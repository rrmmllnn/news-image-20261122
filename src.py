import os
import shutil

# The entry image lives beside this program in the repository; the
# grader sets MAKEFUN_OUTPUT_DIR, otherwise the output goes to /output.
here = os.path.dirname(os.path.abspath(__file__))
out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(out_dir, exist_ok=True)
shutil.copyfile(os.path.join(here, "entry.png"),
                os.path.join(out_dir, "entry.png"))
