import patch_autogen  # 👈 run the patch before importing Autogen or Spectre
from spectre import Spectre

if __name__ == "__main__":
    app = Spectre()
    app.run()
