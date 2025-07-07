import os

def patch_autogen_client():
    path = "/opt/venv/lib/python3.12/site-packages/autogen/oai/client.py"
    if not os.path.exists(path):
        print("⚠️ Autogen client.py not found, skipping patch.")
        return

    with open(path, "r") as f:
        lines = f.readlines()

    modified = False
    with open(path, "w") as f:
        for line in lines:
            if "from openai.lib._parsing._completions" in line:
                f.write("# " + line)  # Comment it out
                modified = True
            else:
                f.write(line)

    if modified:
        print("✅ Patched Autogen: Removed invalid OpenAI import.")
    else:
        print("ℹ️ Patch not needed or already applied.")

patch_autogen_client()
