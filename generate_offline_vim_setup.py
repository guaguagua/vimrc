import os
import re
import shlex
import subprocess # For running git commands
import urllib.request # For downloading plug.vim initially if curl is not preferred in vimrc

# --- Configuration ---
VIMRC_SOURCES_DIR = "vimrcs"
BASE_CONFIG_FILES = ["basic.vim", "extended.vim", "filetypes.vim"]
PLUGIN_CONFIG_FILE = "plugins_config.vim"
PLUGIN_SOURCE_DIRS = ["sources_forked", "sources_non_forked"]
GENERATED_VIMRC_NAME = "generated_vimrc" # Output vimrc file name
PLUGGED_DIR = "plugged"  # For vim-plug, relative to where vimrc is placed by user (e.g. ~/.vim/plugged)
VIM_PLUG_URL = "https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim"

KNOWN_PLUGIN_URLS = {
    # sources_non_forked
    "ack.vim": "mileszs/ack.vim", "ale": "dense-analysis/ale", "auto-pairs": "jiangmiao/auto-pairs",
    "bufexplorer": "jlanzarotta/bufexplorer", "copilot.vim": "github/copilot.vim",
    "ctrlp.vim": "ctrlpvim/ctrlp.vim", "dracula": "dracula/vim",
    "editorconfig-vim": "editorconfig/editorconfig-vim", "gist-vim": "mattn/gist-vim",
    "goyo.vim": "junegunn/goyo.vim", "gruvbox": "morhetz/gruvbox",
    "lightline-ale": "maximbaz/lightline-ale", "lightline.vim": "itchyny/lightline.vim",
    "mayansmoke": "vim-scripts/mayansmoke", "mru.vim": "vim-scripts/mru.vim",
    "nerdtree": "preservim/nerdtree", "nginx.vim": "chr4/nginx.vim",
    "open_file_under_cursor.vim": "amix/open_file_under_cursor.vim", "rust.vim": "rust-lang/rust.vim",
    "tabular": "godlygeek/tabular", "tlib": "tomtom/tlib_vim",
    "typescript-vim": "leafgarland/typescript-vim", "vim-abolish": "tpope/vim-abolish",
    "vim-addon-mw-utils": "MarcWeber/vim-addon-mw-utils", "vim-bundle-mako": "sophacles/vim-bundle-mako",
    "vim-coffee-script": "kchmck/vim-coffee-script", "vim-colors-solarized": "altercation/vim-colors-solarized",
    "vim-commentary": "tpope/vim-commentary", "vim-expand-region": "terryma/vim-expand-region",
    "vim-flake8": "nvie/vim-flake8", "vim-fugitive": "tpope/vim-fugitive",
    "vim-gitgutter": "airblade/vim-gitgutter", "vim-indent-guides": "nathanaelkane/vim-indent-guides",
    "vim-indent-object": "michaeljsmith/vim-indent-object", "vim-javascript": "pangloss/vim-javascript",
    "vim-lastplace": "farmergreg/vim-lastplace", "vim-less": "groenewege/vim-less",
    "vim-markdown": "plasticboy/vim-markdown", "vim-multiple-cursors": "terryma/vim-multiple-cursors",
    "vim-pug": "digitaltoad/vim-pug", "vim-pyte": "therubymug/vim-pyte",
    "vim-python-pep8-indent": "hynek/vim-python-pep8-indent", "vim-repeat": "tpope/vim-repeat",
    "vim-rhubarb": "tpope/vim-rhubarb", "vim-ruby": "vim-ruby/vim-ruby",
    "vim-snipmate": "garbas/vim-snipmate", "vim-snippets": "honza/vim-snippets",
    "vim-surround": "tpope/vim-surround", "vim-yankstack": "maxbrunsfeld/vim-yankstack",

    # sources_forked
    "peaksea": "LOCAL_CONFIG_DIR/peaksea",
    "set_tabline": "LOCAL_CONFIG_DIR/set_tabline",
    "vim-irblack-forked": "UNKNOWN_URL/vim-irblack-forked",
    "vim-peepopen": "UNKNOWN_URL/vim-peepopen",
    "vim-irblack": "vim-scripts/vim-irblack",
}

# --- Helper Functions ---
def get_full_path(*args):
    return os.path.join(os.getcwd(), *args)

# --- Phase 1 Functions ---
def consolidate_base_config(source_dir_name, files_list):
    print(f"Consolidating base configuration files from '{source_dir_name}'...")
    full_config_str = ""
    # Standard Vim settings that should come very first
    full_config_str += "set nocompatible              \" Be iMproved\n"
    full_config_str += "set encoding=utf-8\n"
    full_config_str += "\" Let Vim itself figure out the runtimepath, vim-plug will add to it.\n\n"

    for fname in files_list:
        fpath = get_full_path(source_dir_name, fname)
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()
                full_config_str += f"\n\" --- Start of content from {fname} ---\n"
                full_config_str += content
                full_config_str += f"\n\" --- End of content from {fname} ---\n"
        except FileNotFoundError:
            print(f"  WARNING: File '{fpath}' not found. Skipping.")
        except Exception as e:
            print(f"  ERROR reading '{fpath}': {e}. Skipping.")
    return full_config_str

def identify_plugins_and_urls(plugin_root_dirs_names, known_urls_map):
    print("Identifying plugins and their source URLs...")
    plugins_found = []
    for source_dirname in plugin_root_dirs_names:
        source_dir_path = get_full_path(source_dirname)
        if not os.path.isdir(source_dir_path):
            print(f"  WARNING: Plugin source directory '{source_dir_path}' not found. Skipping.")
            continue
        for item_name in os.listdir(source_dir_path):
            item_path = os.path.join(source_dir_path, item_name)
            if os.path.isdir(item_path):
                if item_name.lower() in ['.git', '.gitkeep']:
                    continue
                url = known_urls_map.get(item_name)
                plugin_type = 'plugin'
                if not url:
                    if item_name in ["peaksea", "set_tabline"]:
                         url = f"LOCAL_CONFIG_DIR/{item_name}"
                         plugin_type = 'local_config'
                    else:
                        url = f"COULD_NOT_GUESS_URL/{item_name}"
                plugins_found.append({
                    'name': item_name, 'url': url, 'original_path': item_path, 'type': plugin_type,
                })
            # Check for .vim files directly in subdirectories like 'colors' if the parent isn't already a known plugin
            elif item_name.endswith(".vim"):
                parent_dir_name = os.path.basename(os.path.dirname(item_path))
                parent_parent_dir_name = os.path.basename(os.path.dirname(os.path.dirname(item_path)))

                # Handle cases like sources_forked/peaksea/colors/peaksea.vim
                # The plugin name should be 'peaksea'
                plugin_name_candidate = parent_dir_name
                if parent_dir_name.lower() == "colors" and parent_parent_dir_name in PLUGIN_SOURCE_DIRS: # e.g. colors directly under sources_non_forked
                    plugin_name_candidate = item_name[:-4] # Use the .vim file name itself
                elif parent_dir_name.lower() == "colors": # e.g. sources_non_forked/plugin_name/colors/actual_colorscheme.vim
                    plugin_name_candidate = os.path.basename(os.path.dirname(os.path.dirname(item_path)))


                is_already_listed_as_plugin_or_local = any(
                    p['name'] == plugin_name_candidate and (p['type'] == 'plugin' or p['type'] == 'local_config')
                    for p in plugins_found
                )
                if is_already_listed_as_plugin_or_local:
                    continue

                # If the .vim file is in a 'colors' subdirectory of a plugin source dir:
                if os.path.basename(os.path.dirname(item_path).lower()) == "colors":
                    cs_name = item_name[:-4]
                    # Try to get URL by cs_name, then by parent folder name (plugin_name_candidate)
                    cs_url = known_urls_map.get(cs_name, known_urls_map.get(plugin_name_candidate, f"COULD_NOT_GUESS_URL/{plugin_name_candidate}_colorscheme"))

                    # Avoid adding if the parent directory itself is the plugin and will pull in the colorscheme
                    if not any(p['name'] == plugin_name_candidate and p['type'] == 'plugin' for p in plugins_found):
                        # Also avoid adding if this exact colorscheme name is already listed as a plugin
                        if not any(p['name'] == cs_name and p['type'] == 'plugin' for p in plugins_found):
                            plugins_found.append({'name': cs_name, 'url': cs_url, 'original_path': item_path, 'type': 'colorscheme'})


    final_plugins_list = []
    seen_names = set()
    for p in sorted(plugins_found, key=lambda x: ("COULD_NOT_GUESS_URL" in x['url'] or "LOCAL_CONFIG_DIR" in x['url'])):
        if p['name'] not in seen_names:
            final_plugins_list.append(p)
            seen_names.add(p['name'])
        else:
            existing_plugin_idx = next((i for i, item in enumerate(final_plugins_list) if item['name'] == p['name']), -1)
            if existing_plugin_idx != -1:
                existing_plugin = final_plugins_list[existing_plugin_idx]
                is_existing_problematic = "COULD_NOT_GUESS_URL" in existing_plugin['url'] or "LOCAL_CONFIG_DIR" in existing_plugin['url']
                is_current_better = not ("COULD_NOT_GUESS_URL" in p['url'] or "LOCAL_CONFIG_DIR" in p['url'])
                if is_existing_problematic and is_current_better:
                    final_plugins_list[existing_plugin_idx] = p
    print(f"  Identified {len(final_plugins_list)} potential plugins/configs.")
    return final_plugins_list

# --- Phase 2 Functions ---
def extract_plugin_specific_configs(plugin_config_file_path):
    config_lines = []
    try:
        with open(plugin_config_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                stripped_line = line.strip()
                if not stripped_line or stripped_line.startswith('"') or \
                   "pathogen#infect" in stripped_line or \
                   "pathogen#helptags" in stripped_line or \
                   "set packpath+=" in stripped_line or \
                   stripped_line.lower().startswith("call plug#begin") or \
                   stripped_line.lower().startswith("call plug#end") or \
                   stripped_line.lower().startswith("plug "):
                    continue
                config_lines.append(line.rstrip())
        return "\n".join(config_lines)
    except FileNotFoundError:
        print(f"  WARNING: Plugin config file '{plugin_config_file_path}' not found. No specific configs extracted.")
        return ""
    except Exception as e:
        print(f"  ERROR reading plugin config file '{plugin_config_file_path}': {e}")
        return ""

def generate_vimrc_content(base_config_str, plugins_list, plugin_specific_configs_str, vim_plug_url_in_script):
    vimrc_parts = []
    vimrc_parts.append("\" Auto-generated vimrc using vim-plug")
    vimrc_parts.append("\" Original project: https://github.com/amix/vimrc")
    vimrc_parts.append("\" Script to generate this: generate_offline_vim_setup.py\n")

    # Base config (which includes nocompatible, encoding etc.) comes first
    vimrc_parts.append("\n\" --- Base Configuration (from basic.vim, extended.vim, filetypes.vim) ---")
    vimrc_parts.append(base_config_str)

    vimrc_parts.append("\n\" Install vim-plug if not found")
    vim_dir_base = "~/.vim"
    if os.name == 'nt':
        vim_dir_base = "~/vimfiles"

    vimrc_parts.append(f"let data_dir = has('nvim') ? stdpath('data') . '/site' : '{vim_dir_base}'")
    vimrc_parts.append(f"let plug_path = data_dir . '/autoload/plug.vim'")
    vimrc_parts.append(f"if empty(glob(plug_path))")
    vimrc_parts.append(f"  silent execute '!curl -fLo '.shellescape(plug_path).' --create-dirs {vim_plug_url_in_script}'")
    vimrc_parts.append(f"  autocmd VimEnter * PlugInstall --sync | source $MYVIMRC")
    vimrc_parts.append(f"endif\n")

    vimrc_parts.append("\" Initialize vim-plug")
    vimrc_parts.append(f"call plug#begin(data_dir . '/{PLUGGED_DIR}')")

    vimrc_parts.append("\n\" Plugin List - generated from amix/vimrc sources")
    for plugin in plugins_list:
        if plugin['type'] == 'local_config':
            vimrc_parts.append(f"\" For local config/plugin '{plugin['name']}', ensure files from '{plugin['original_path']}'")
            vimrc_parts.append(f"\" are structured correctly for vim-plug within: " + f"data_dir . '/{PLUGGED_DIR}/{plugin['name']}/'")
            vimrc_parts.append(f"Plug '{shlex.quote(plugin['name'])}'  \" Ensure this local plugin is structured correctly (e.g., has plugin/*.vim or autoload/*.vim)")
            continue
        if plugin['type'] == 'colorscheme' and plugin['url'].startswith("COULD_NOT_GUESS_URL"):
             vimrc_parts.append(f"\" Colorscheme: {plugin['name']} from '{plugin['original_path']}'.")
             vimrc_parts.append(f"\" Manually place in '.../{PLUGGED_DIR}/{plugin['name']}/colors/{plugin['name']}.vim' or similar, then add Plug line if it's a full plugin.")
             vimrc_parts.append(f"\" Example: Plug 'USER/REPO_FOR_{plugin['name']}' or Plug '{plugin['name']}' if local and structured for vim-plug.")
        elif plugin['url'].startswith("COULD_NOT_GUESS_URL"):
            vimrc_parts.append(f"\" Plug '{plugin['url']}' \" TODO: Find correct Git URL for {plugin['name']} (original path: {plugin['original_path']})")
        else:
            plug_arg = plugin['url']
            if not (plug_arg.startswith("http") or plug_arg.startswith("git")) and '/' in plug_arg:
                pass
            elif not (plug_arg.startswith("http") or plug_arg.startswith("git")):
                 vimrc_parts.append(f"\" Plug '{shlex.quote(plug_arg)}' \" Ambiguous plugin source for '{plugin['name']}', please verify or provide full URL/path if local.")
                 continue
            vimrc_parts.append(f"Plug '{shlex.quote(plug_arg)}'")

    vimrc_parts.append("\ncall plug#end()")

    vimrc_parts.append("\n\" --- Plugin-Specific Configurations (from plugins_config.vim, filtered) ---")
    vimrc_parts.append(plugin_specific_configs_str)

    vimrc_parts.append("\n\" --- End of auto-generated vimrc ---")
    return "\n".join(vimrc_parts)

# --- Phase 3 Functions ---
def write_file(filepath, content):
    print(f"Writing file to '{filepath}'...")
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Successfully wrote {os.path.basename(filepath)}.")
        return True
    except Exception as e:
        print(f"  ERROR: Could not write to '{filepath}': {e}")
        return False

def setup_plugin_environment(plugins_list, base_plugged_dir_name, vim_plug_download_url):
    print("\n--- Setting up Plugin Environment ---")
    home_dir = os.path.expanduser("~")
    vim_config_dir = os.path.join(home_dir, ".vim")
    if "XDG_CONFIG_HOME" in os.environ:
        nvim_config_dir_xdg = os.path.join(os.environ["XDG_CONFIG_HOME"], "nvim")
        if os.path.isdir(nvim_config_dir_xdg):
            vim_config_dir = nvim_config_dir_xdg
    elif os.path.isdir(os.path.join(home_dir, ".config", "nvim")):
        vim_config_dir = os.path.join(home_dir, ".config", "nvim")
    os.makedirs(vim_config_dir, exist_ok=True)
    final_plugged_dir = os.path.join(vim_config_dir, base_plugged_dir_name)
    final_autoload_dir = os.path.join(vim_config_dir, "autoload")
    os.makedirs(final_plugged_dir, exist_ok=True)
    print(f"  Ensured plugin directory exists: '{final_plugged_dir}'")
    os.makedirs(final_autoload_dir, exist_ok=True)
    print(f"  Ensured autoload directory exists: '{final_autoload_dir}'")
    plug_vim_path = os.path.join(final_autoload_dir, "plug.vim")
    if not os.path.exists(plug_vim_path):
        print(f"  plug.vim not found at '{plug_vim_path}'. Attempting to download...")
        try:
            with urllib.request.urlopen(vim_plug_download_url) as response, open(plug_vim_path, 'wb') as out_file:
                out_file.write(response.read())
            print(f"  Successfully downloaded plug.vim to '{plug_vim_path}'")
        except Exception as e:
            print(f"  ERROR downloading plug.vim: {e}. Please try manually or ensure curl is available for vimrc method.")
    else:
        print(f"  plug.vim already exists at '{plug_vim_path}'.")
    print("\nAttempting to clone plugins...")
    cloned_count = 0
    failed_clones = []
    skipped_clones = []
    for plugin in plugins_list:
        if plugin['type'] == 'local_config' or plugin['url'].startswith("COULD_NOT_GUESS_URL") or \
           (plugin['type'] == 'colorscheme' and plugin['url'].startswith("COULD_NOT_GUESS_URL")):
            skipped_clones.append(plugin['name'])
            continue

        plugin_name_for_dir = plugin['name']
        if '/' in plugin['url']:
            potential_name = plugin['url'].split('/')[-1]
            if potential_name.endswith('.git'):
                potential_name = potential_name[:-4]
            if potential_name:
                plugin_name_for_dir = potential_name

        plugin_repo_url = plugin['url']
        if not (plugin_repo_url.startswith(('http://', 'https://', 'git://')) or os.path.isabs(plugin_repo_url)):
            plugin_repo_url = f"https://github.com/{plugin_repo_url}.git"

        target_path = os.path.join(final_plugged_dir, plugin_name_for_dir)

        if os.path.exists(target_path):
            print(f"  Plugin '{plugin_name_for_dir}' already exists at '{target_path}'. Skipping clone.")
            cloned_count +=1
            continue

        print(f"  Cloning '{plugin_name_for_dir}' from '{plugin_repo_url}' into '{target_path}'...")
        try:
            subprocess.run(['git', 'clone', plugin_repo_url, target_path], check=True, capture_output=True, text=True, errors='ignore')
            print(f"    Successfully cloned '{plugin_name_for_dir}'.")
            cloned_count += 1
        except FileNotFoundError:
            print("  ERROR: git command not found. Please install Git and ensure it's in your PATH.")
            return False
        except subprocess.CalledProcessError as e:
            print(f"    ERROR cloning '{plugin_name_for_dir}': {e.returncode}")
            print(f"    Stdout: {e.stdout.strip()}")
            print(f"    Stderr: {e.stderr.strip()}")
            failed_clones.append(f"{plugin_name_for_dir} (URL: {plugin_repo_url})")
        except Exception as e_gen:
            print(f"    An unexpected ERROR occurred cloning '{plugin_name_for_dir}': {e_gen}")
            failed_clones.append(f"{plugin_name_for_dir} (URL: {plugin_repo_url})")

    print(f"\nPlugin cloning summary:")
    print(f"  Successfully cloned/found: {cloned_count} plugins.")
    if skipped_clones:
        print(f"  Skipped (manual action required): {len(skipped_clones)} plugins: {', '.join(skipped_clones)}")
    if failed_clones:
        print(f"  Failed to clone: {len(failed_clones)} plugins:")
        for p_fail in failed_clones:
            print(f"    - {p_fail}")

    if not failed_clones and not skipped_clones:
        print(f"\nAll specified plugins processed successfully.")
    elif not failed_clones and skipped_clones:
        print(f"\nSome plugins require manual setup. Others processed.")
    else:
        print("\nSome plugins failed to clone or require manual setup. Please review the errors and instructions.")

    print(f"Next, open Vim with the '{GENERATED_VIMRC_NAME}' (e.g., as ~/.vimrc or ~/.config/nvim/init.vim) and run: :PlugInstall")
    return True


if __name__ == '__main__':
    print("--- Vim Configuration Offline Setup Script ---")
    base_config = consolidate_base_config(VIMRC_SOURCES_DIR, BASE_CONFIG_FILES)
    plugins = identify_plugins_and_urls(PLUGIN_SOURCE_DIRS, KNOWN_PLUGIN_URLS)

    print("\n--- Identified Plugins & Configs (for vimrc generation) ---")
    for p in plugins:
        print(f"  Name: {p['name']}, URL: {p['url']}, Type: {p.get('type', 'plugin')}")


    plugin_config_path = get_full_path(VIMRC_SOURCES_DIR, PLUGIN_CONFIG_FILE)
    plugin_settings = extract_plugin_specific_configs(plugin_config_path)

    vimrc_new_content = generate_vimrc_content(base_config, plugins, plugin_settings, VIM_PLUG_URL)

    if write_file(GENERATED_VIMRC_NAME, vimrc_new_content):
        print(f"\nSuccessfully generated '{GENERATED_VIMRC_NAME}'.")
        print("Review it, then you can copy it to your Vim configuration path (e.g., ~/.vimrc or ~/.config/nvim/init.vim).")

        user_consent = input(f"\nDo you want this script to attempt to create directories (e.g., ~/.vim/{PLUGGED_DIR}, ~/.vim/autoload) and clone plugins? [y/N]: ")
        if user_consent.lower() == 'y':
            print("Proceeding with plugin environment setup...")
            setup_plugin_environment(plugins, PLUGGED_DIR, VIM_PLUG_URL)
        else:
            print("\nPlugin download and environment setup skipped by user request.")
            print(f"To complete setup manually: ")
            print(f"  1. Copy '{GENERATED_VIMRC_NAME}' to your Vim configuration path.")
            print(f"  2. Create plugin directories (e.g., `mkdir -p ~/.vim/{PLUGGED_DIR}` and `~/.vim/autoload` or Neovim equivalents).")
            print(f"  3. Download vim-plug: `curl -fLo ~/.vim/autoload/plug.vim --create-dirs {VIM_PLUG_URL}` (adjust path for Neovim).")
            print(f"  4. Review '{GENERATED_VIMRC_NAME}' for `Plug` lines with 'COULD_NOT_GUESS_URL' or 'LOCAL_CONFIG_DIR' and manually clone/copy those plugins/configs into your '{PLUGGED_DIR}' directory, ensuring correct structure for vim-plug.")
            print(f"  5. Open Vim and run: :PlugInstall")

    print("\n--- Script Finished ---")
