# Instructions for Offline Vim Setup from amix/vimrc

This guide explains how to use the `generate_offline_vim_setup.py` script to create a portable, offline-ready Vim configuration based on the amix/vimrc project.

## Goal

The script will:
1.  Consolidate the multiple `.vim` configuration files from the `vimrcs/` directory into a single `generated_vimrc` file.
2.  Transform the plugin management from Pathogen (as used in the original project) to use `vim-plug`.
3.  Attempt to download all identified plugins into a `plugged/` directory, typically within your `~/.vim/` folder (or Neovim equivalent like `~/.config/nvim/`).
4.  The `generated_vimrc` will be configured to use these downloaded plugins via `vim-plug`.

This setup is designed to be usable on a machine without internet access after the initial script run and plugin download.

## Prerequisites

Before running the script, ensure you have the following installed on your system:

1.  **Python 3.x:** The script is written in Python 3.
2.  **Git:** `git` is required to clone the Vim plugins.
3.  **Curl (Optional but Recommended):** `curl` is used by the `vim-plug` auto-install snippet in the generated `vimrc`. The Python script also attempts to download `plug.vim` using Python's `urllib`, but `curl` is a common fallback.

## How to Use

1.  **Download or Clone this Project:**
    If you haven't already, get the entire `amix/vimrc` project (which now includes `generate_offline_vim_setup.py` and this `INSTRUCTIONS.md` file) onto the machine where you want to generate the offline setup.

2.  **Navigate to the Project Root:**
    Open your terminal or command prompt and change to the root directory of the `amix/vimrc` project (the directory containing `generate_offline_vim_setup.py`).

3.  **Review Plugin URLs (Optional but Recommended):**
    The script uses a predefined list (`KNOWN_PLUGIN_URLS` in the script) to find Git repositories for plugins.
    *   If the script encounters plugins not in its known list or forked plugins where the URL is ambiguous, it will mark them as `COULD_NOT_GUESS_URL/...` or `UNKNOWN_URL/...` in its output and in the generated `vimrc` (as commented-out `Plug` lines).
    *   You might want to open `generate_offline_vim_setup.py` and review/update the `KNOWN_PLUGIN_URLS` dictionary if you know specific URLs for plugins, especially those in the `sources_forked` directory or any marked as unknown.

4.  **Run the Python Script:**
    Execute the script from the project root:
    ```bash
    python generate_offline_vim_setup.py
    ```

5.  **Script Actions & Output:**
    *   The script will print its progress as it consolidates configurations and identifies plugins.
    *   It will generate a new Vim configuration file named `generated_vimrc` in the current directory. This file is configured to use `vim-plug`.
    *   **User Consent for Downloads:** After generating `generated_vimrc`, the script will ask for your consent before creating directories (like `~/.vim/plugged`, `~/.vim/autoload`, or their Neovim equivalents) and attempting to download `plug.vim` and the listed plugins.
        ```
        Do you want this script to attempt to create directories (e.g., ~/.vim/plugged, ~/.vim/autoload) and clone plugins? [y/N]:
        ```
        Enter `y` to proceed, or `N` to skip this step and handle plugin setup manually.

6.  **If You Consent to Downloads (Script-Assisted Setup):**
    *   The script will create the necessary plugin and autoload directories under your Vim configuration path (e.g., `~/.vim/` or `~/.config/nvim/`).
    *   It will attempt to download `plug.vim` (the `vim-plug` manager itself) into the autoload directory.
    *   It will then try to `git clone` each plugin with a known URL into the `plugged/` directory.
    *   Pay attention to any error messages during the cloning process.

7.  **Manual Steps (If Downloads Skipped, Failed, or for Special Plugins):**
    *   **Locate `generated_vimrc`:** This file is created in the directory where you ran the script.
    *   **Vim Configuration Path:**
        *   For traditional Vim: `~/.vimrc` (file) and `~/.vim/` (directory).
        *   For Neovim: `~/.config/nvim/init.vim` (file) and `~/.config/nvim/` (directory).
    *   **Backup:** Backup your existing Vim configuration if you have one.
    *   **Copy `generated_vimrc`:** Copy `generated_vimrc` to your Vim configuration path (e.g., `cp generated_vimrc ~/.vimrc` or `cp generated_vimrc ~/.config/nvim/init.vim`).
    *   **Create Directories:** Manually create the plugin directories if the script didn't:
        *   Vim: `mkdir -p ~/.vim/plugged ~/.vim/autoload`
        *   Neovim: `mkdir -p ~/.config/nvim/plugged ~/.config/nvim/autoload`
    *   **Install `plug.vim`:** Download `plug.vim` from [https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim](https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim).
        *   Vim: Place it in `~/.vim/autoload/plug.vim`.
        *   Neovim: Place it in `~/.config/nvim/autoload/plug.vim`.
    *   **Handle Plugins from `generated_vimrc`:**
        *   Open your new Vim configuration file (`~/.vimrc` or `~/.config/nvim/init.vim`).
        *   Look for lines starting with `Plug ...` or `\" Plug ... TODO: ...`.
        *   For each valid `Plug 'user/repo'` line, manually clone the plugin into your `plugged` directory:
            ```bash
            git clone https://github.com/user/repo.git ~/.vim/plugged/repo
            # (Adjust path for Neovim if necessary)
            ```
        *   For plugins with `COULD_NOT_GUESS_URL` or `LOCAL_CONFIG_DIR` comments:
            *   **`COULD_NOT_GUESS_URL`**: You need to find the correct Git URL for these plugins. Once found, uncomment the `Plug` line, replace the placeholder URL, and clone it as above.
            *   **`LOCAL_CONFIG_DIR`**: These are typically local customizations or simple `.vim` files from the original `amix/vimrc` structure (e.g., `peaksea`, `set_tabline`). Their original paths are noted by the script during its identification phase (check script output). You need to:
                1.  Create a subdirectory for them within your `plugged` directory (e.g., `~/.vim/plugged/peaksea`).
                2.  Copy the relevant files from their `original_path` (e.g., from `sources_forked/peaksea/`) into the new subdirectory, maintaining their structure (e.g., `colors/peaksea.vim` should go into `~/.vim/plugged/peaksea/colors/peaksea.vim`).
                3.  Then, ensure the `Plug` line in your `vimrc` for this local plugin correctly refers to the directory name (e.g., `Plug 'peaksea'`). The script attempts to generate this `Plug` line for you.

8.  **Install Plugins with vim-plug (Final Step):**
    *   Open Vim (it should now be using your new configuration).
    *   Run the command:
        ```vim
        :PlugInstall
        ```
    *   This command will process all the `Plug` commands. For plugins already cloned into the `plugged` directory, `vim-plug` will recognize them. If any were missed or if the `vimrc`'s auto-install snippet for `plug.vim` needs to run `curl`, this command ensures everything is set up.
    *   You might see messages about plugins already being installed; this is normal.

9.  **Restart Vim:**
    After `:PlugInstall` completes and reports no errors, restart Vim. Your offline Vim setup should now be ready!

## Troubleshooting

*   **`git not found` / `curl not found`:** Ensure these command-line tools are installed and accessible in your system's PATH.
*   **Plugin clone failures (if script attempted downloads):** Double-check the Git URL for the failed plugin. The script's `KNOWN_PLUGIN_URLS` might have an outdated or incorrect URL. You might need to find the correct one manually and clone it as described in step 7.
*   **Errors in Vim on startup:** Review your new Vim configuration file (`~/.vimrc` or `init.vim`) for syntax issues, especially around the plugin-specific configurations section or any manual edits you made to `Plug` lines.
*   **Permissions:** Ensure you have write permissions for your `~/.vim/` (or `~/.config/nvim/`) directory.

This process gives you a self-contained Vim setup that relies on `vim-plug` and the plugins downloaded into your local `plugged` directory.
