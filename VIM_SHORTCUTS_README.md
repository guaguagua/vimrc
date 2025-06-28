# Vim Configuration Shortcuts Guide

This document outlines the custom keyboard shortcuts and mappings defined in this Vim configuration. Understanding these shortcuts can significantly speed up your editing workflow.

## Leader Key

The **Leader key** is a special key that, when pressed before other keys, creates a new namespace for custom shortcuts. In this configuration, the Leader key is set to:

-   **`,` (Comma)**

So, when you see `<leader>` in a shortcut, you should press `,` followed by the specified key(s). For example, `<leader>w` means press `,` then `w`.

---

## Most Frequently Used Shortcuts (Updated)

This section highlights some of the most common and useful shortcuts from this configuration.

| Mode        | Shortcut           | Action                               | Description                                    |
|-------------|--------------------|--------------------------------------|------------------------------------------------|
| Normal      | `<leader>w`        | `:w!<cr>`                            | Save current file.                             |
| Normal      | `<leader><cr>`     | `:noh<cr>`                           | Clear search highlight.                        |
| Normal      | `0`                | `^`                                  | Go to first non-blank character of line.       |
| Normal      | `<leader>tn`       | `:tabnew<cr>`                         | Create a new tab.                              |
| Normal      | `<leader>tc`       | `:tabclose<cr>`                       | Close current tab.                             |
| All         | `<F5>`             | `:call CompileRun()<CR>`             | Compile and run current file.                  |
| Normal      | `<leader>o`        | `:BufExplorer<cr>`                   | Open BufExplorer (manage buffers).             |
| Normal      | `<C-f>`            | (CtrlP main map)                     | Open CtrlP to find files.                      |
| Normal      | `<leader>j`        | `:CtrlP<cr>`                         | (Alternative) Open CtrlP to find files.        |
| Normal      | `<leader>nn`       | `:NERDTreeToggle<cr>`                | Toggle NERDTree file explorer.                 |
| Normal      | `<leader>g`        | `:Ack`                               | Open Ack/ag for project-wide search.           |
| Normal      | `<leader>ss`       | `:setlocal spell!<cr>`               | Toggle spell check for current buffer.         |
| Normal      | `<leader>z`        | `:Goyo<cr>`                          | Toggle Goyo (distraction-free writing mode).   |
| Insert      | `<C-j>`            | (snipMate trigger)                   | Trigger snipMate snippet expansion.            |
| Command     | `:let @+=expand('%:p')` | (Copy file path)                 | Copy full path of current file to clipboard.   |
| Normal      | `<C-o>`            | (Jump list older)                    | Go to older cursor position in jump list.      |
| Normal      | `<C-i>`            | (Jump list newer)                    | Go to newer cursor position in jump list.      |
| Normal      | `gcc`              | (Comment toggle)                     | Toggle comment for the current line.           |
| Normal      | `<C-]>`            | (Go to definition)                   | Jump to definition of tag under cursor (ctags).|

---

## I. Normal Mode Mappings

These shortcuts are available in Normal mode.

### File Operations
| Shortcut        | Action                                           | Description                                 |
|-----------------|--------------------------------------------------|---------------------------------------------|
| `<leader>w`     | `:w!<cr>`                                        | Fast save current file.                     |
| `<leader>e`     | `:e! ~/.vim_runtime/my_configs.vim<cr>`          | Edit the `my_configs.vim` file.             |
| `<leader>q`     | `:e ~/buffer<cr>`                                | Open `~/buffer` for quick notes/scribbling. |
| `<leader>x`     | `:e ~/buffer.md<cr>`                             | Open `~/buffer.md` for markdown notes.      |
| `:W`            | `w !sudo tee % > /dev/null \| edit!`             | Save current file using sudo (for permissions). |

### Navigation & Window Management
| Shortcut        | Action                                           | Description                                 |
|-----------------|--------------------------------------------------|---------------------------------------------|
| `<C-j>`         | `<C-W>j`                                         | Move cursor to the window below.            |
| `<C-k>`         | `<C-W>k`                                         | Move cursor to the window above.            |
| `<C-h>`         | `<C-W>h`                                         | Move cursor to the window to the left.      |
| `<C-l>`         | `<C-W>l`                                         | Move cursor to the window to the right.     |
| `0`             | `^`                                              | Move cursor to the first non-blank character of the line. |
| `<M-j>`         | `mz:m+<cr>\`z`                                   | Move current line down.                     |
| `<M-k>`         | `mz:m-2<cr>\`z`                                  | Move current line up.                       |
| `<D-j>` (Mac)   | `<M-j>`                                          | (Same as Alt+j) Move current line down.     |
| `<D-k>` (Mac)   | `<M-k>`                                          | (Same as Alt+k) Move current line up.       |
| `½`             | `$`                                              | Move cursor to the end of the line.         |
| `<leader>cd`    | `:cd %:p:h<cr>:pwd<cr>`                          | Change Current Working Directory to the directory of the open buffer. |

### Buffer Management
| Shortcut        | Action                                           | Description                                 |
|-----------------|--------------------------------------------------|---------------------------------------------|
| `<leader>bd`    | `:Bclose<cr>:tabclose<cr>gT`                     | Close current buffer (and tab if it's the last buffer in it). |
| `<leader>ba`    | `:bufdo bd<cr>`                                  | Close all buffers.                          |
| `<leader>l`     | `:bnext<cr>`                                     | Go to the next buffer.                      |
| `<leader>h`     | `:bprevious<cr>`                                 | Go to the previous buffer.                  |
| `:Bclose`       | `call <SID>BufcloseCloseIt()`                    | Close current buffer without closing window. |

### Tab Management
| Shortcut        | Action                                           | Description                                 |
|-----------------|--------------------------------------------------|---------------------------------------------|
| `<leader>tn`    | `:tabnew<cr>`                                    | Create a new tab.                           |
| `<leader>to`    | `:tabonly<cr>`                                   | Close all other tabs.                       |
| `<leader>tc`    | `:tabclose<cr>`                                  | Close the current tab.                      |
| `<leader>tm`    | `:tabmove`                                       | Prepare to move the current tab (requires numerical input). |
| `<leader>t<leader>` | `:tabnext<cr>`                               | Go to the next tab (likely `,,`).           |
| `<leader>tl`    | `:exe "tabn ".g:lasttab<CR>`                     | Toggle to the last accessed tab.            |
| `<leader>te`    | `:tabedit <C-r>=escape(expand("%:p:h"), " ")<cr>/` | Open a new tab in the current file's directory. |

### Search & Replace
| Shortcut        | Action                                           | Description                                 |
|-----------------|--------------------------------------------------|---------------------------------------------|
| `<space>`       | `/`                                              | Initiate a search.                          |
| `<C-space>`     | `?`                                              | Initiate a backwards search.                |
| `<leader><cr>`  | `:noh<cr>` (silent)                              | Clear search highlight.                     |

### Editing & Text Manipulation
| Shortcut        | Action                                           | Description                                 |
|-----------------|--------------------------------------------------|---------------------------------------------|
| `<leader>pp`    | `:setlocal paste!<cr>`                           | Toggle paste mode.                          |
| `<Leader>m`     | `mmHmt:%s/<C-V><cr>//ge<cr>'tzt'm`               | Remove Windows `^M` (carriage return) characters. |

### Spell Checking
| Shortcut        | Action                                           | Description                                 |
|-----------------|--------------------------------------------------|---------------------------------------------|
| `<leader>ss`    | `:setlocal spell!<cr>`                           | Toggle spell checking for the current buffer. |
| `<leader>sn`    | `]s`                                             | Move to the next spelling error.            |
| `<leader>sp`    | `[s`                                             | Move to the previous spelling error.        |
| `<leader>sa`    | `zg`                                             | Add word under cursor to spell dictionary.  |
| `<leader>s?`    | `z=`                                             | Suggest corrections for word under cursor.  |

### Code Execution
| Shortcut        | Action                                           | Description                                 |
|-----------------|--------------------------------------------------|---------------------------------------------|
| `<F5>`          | `:call CompileRun()<CR>`                         | Compile and run the current file (language-specific). |

---

## II. Visual Mode Mappings

These shortcuts are available when text is selected in Visual mode.

### Search
| Shortcut        | Action                                           | Description                                 |
|-----------------|--------------------------------------------------|---------------------------------------------|
| `*`             | (VisualSelection call) `/<C-R>=@/<CR><CR>`      | Search for the visually selected text.      |
| `#`             | (VisualSelection call) `?<C-R>=@/<CR><CR>`      | Search backwards for the visually selected text. |

### Editing & Text Manipulation (Movement)
| Shortcut        | Action                                           | Description                                 |
|-----------------|--------------------------------------------------|---------------------------------------------|
| `<M-j>`         | `:m\'>+<cr>\`...`                                 | Move selected lines down.                   |
| `<M-k>`         | `:m\'<-2<cr>\`...`                                | Move selected lines up.                     |
| `<D-j>` (Mac)   | (Same as Alt+j)                                  | Move selected lines down.                   |
| `<D-k>` (Mac)   | (Same as Alt+k)                                  | Move selected lines up.                     |

### Surrounding Text (Parentheses/Brackets/Quotes)
| Shortcut        | Action                                           | Description                                 |
|-----------------|--------------------------------------------------|---------------------------------------------|
| `$1`            | `<esc>\`>a)<esc>\`<i(<esc>`                      | Surround selection with `()`.               |
| `$2`            | `<esc>\`>a]<esc>\`<i[<esc>`                      | Surround selection with `[]`.               |
| `$3`            | `<esc>\`>a}<esc>\`<i{<esc>`                      | Surround selection with `{}`.               |
| `$$`            | `<esc>\`>a"<esc>\`<i"<esc>`                      | Surround selection with `""`.               |
| `$q`            | `<esc>\`>a'<esc>\`<i'<esc>`                      | Surround selection with `''`.               |
| `$e`            | `<esc>\`>a\`<esc>\`<i\`<esc>`                      | Surround selection with \`\` (backticks).   |

### Code Execution
| Shortcut        | Action                                           | Description                                 |
|-----------------|--------------------------------------------------|---------------------------------------------|
| `<F5>`          | `<Esc>:call CompileRun()<CR>`                    | Compile and run file (exits Visual mode).   |

*(Many Normal mode mappings using `map` also apply in Visual mode if not specifically overridden, e.g., `<leader>w`, `<space>`, etc.)*

---

## III. Insert Mode Mappings

These shortcuts are available while in Insert mode.

### Auto-Pairing & Snippets
| Shortcut        | Action                                           | Description                                 |
|-----------------|--------------------------------------------------|---------------------------------------------|
| `$1`            | `()<esc>i`                                       | Insert `()` and place cursor inside.        |
| `$2`            | `[]<esc>i`                                       | Insert `[]` and place cursor inside.        |
| `$3`            | `{}<esc>i`                                       | Insert `{}` and place cursor inside.        |
| `$4`            | `{<esc>o}<esc>O`                                 | Insert `{}` on separate lines, cursor inside. |
| `$q`            | `''<esc>i`                                       | Insert `''` and place cursor inside.        |
| `$e`            | `""<esc>i`                                       | Insert `""` and place cursor inside.        |
| `½`             | `$`                                              | (Unusual) May insert `$` or move to EOL.    |


### Abbreviations
| Abbreviation    | Expands to                                       | Description                                 |
|-----------------|--------------------------------------------------|---------------------------------------------|
| `xdate`         | Current datetime (e.g., `01/01/24 14:30:00`)     | Insert current date and time.               |

### Code Execution
| Shortcut        | Action                                           | Description                                 |
|-----------------|--------------------------------------------------|---------------------------------------------|
| `<F5>`          | `<Esc>:call CompileRun()<CR>`                    | Compile and run file (exits Insert mode).   |

---

## IV. Command-Line Mode Mappings

These shortcuts are available when entering commands with `:` or searching with `/`, `?`.

### Navigation & Editing
| Shortcut        | Action                                           | Description                                 |
|-----------------|--------------------------------------------------|---------------------------------------------|
| `$h`            | `e ~/`                                           | Expands to edit home directory.             |
| `$d`            | `e ~/Desktop/`                                   | Expands to edit Desktop directory.          |
| `$j`            | `e ./`                                           | Expands to edit current directory.          |
| `$c`            | `e <C-\>eCurrentFileDir("e")<cr>`                | Expands to edit in current file's directory. |
| `$q`            | `<C-\>eDeleteTillSlash()<cr>`                    | Delete command line content until last `/` or `\`. |
| `<C-A>`         | `<Home>`                                         | Move to beginning of command line.          |
| `<C-E>`         | `<End>`                                          | Move to end of command line.                |
| `<C-K>`         | `<C-U>`                                          | Delete entire command line.                 |
| `<C-P>`         | `<Up>`                                           | Previous command from history.              |
| `<C-N>`         | `<Down>`                                         | Next command from history.                  |
| `½`             | `$`                                              | Move to end of command line.                |

---

## V. Plugin Specific Shortcuts

### Ack / ag (Code Search)
*Plugin for fast code searching.*
| Mode   | Shortcut        | Action                                           | Description                                 |
|--------|-----------------|--------------------------------------------------|---------------------------------------------|
| Normal | `<leader>g`     | `:Ack`                                           | Open Ack/ag prompt for searching.           |
| Visual | `gv`            | (VisualSelection call for Ack)                   | Search for the selected text using Ack/ag.  |
| Visual | `<leader>r`     | (VisualSelection call for replace)               | Search and replace selected text.           |
| Normal | `<leader>cc`    | `:botright cope<cr>`                             | Open Ack/ag results in `cope` (quickfix) window. |
| Normal | `<leader>co`    | `ggVGy:tabnew<cr>:set syntax=qf<cr>pgg`          | Copy `cope` content to a new tab.           |
| Normal | `<leader>n`     | `:cn<cr>`                                        | Go to the next search result in `cope`.     |
| Normal | `<leader>p`     | `:cp<cr>`                                        | Go to the previous search result in `cope`. |

### BufExplorer
*Plugin for browsing and managing buffers.*
| Mode   | Shortcut        | Action                                           | Description                                 |
|--------|-----------------|--------------------------------------------------|---------------------------------------------|
| Normal | `<leader>o`     | `:BufExplorer<cr>`                               | Open BufExplorer.                           |

### MRU (Most Recently Used files)
*Plugin for quickly accessing recently opened files.*
| Mode   | Shortcut        | Action                                           | Description                                 |
|--------|-----------------|--------------------------------------------------|---------------------------------------------|
| Normal | `<leader>f`     | `:MRU<CR>`                                       | Open MRU file list.                         |

### YankStack
*Plugin for managing a history of yanks (copies/cuts).*
| Mode   | Shortcut        | Action                                           | Description                                 |
|--------|-----------------|--------------------------------------------------|---------------------------------------------|
| Normal | `<C-p>`         | `<Plug>yankstack_substitute_older_paste`         | Paste older item from yank stack. **Note: Potential conflict with vim-multiple-cursors.** |
| Normal | `<C-n>`         | `<Plug>yankstack_substitute_newer_paste`         | Paste newer item from yank stack.           |

### CtrlP (File/Buffer Finder)
*Fuzzy finder for files, buffers, MRU files, etc.*
| Mode   | Shortcut        | Action                                           | Description                                 |
|--------|-----------------|--------------------------------------------------|---------------------------------------------|
| Normal | `<C-f>`         | (CtrlP main map)                                 | Open CtrlP to find files.                   |
| Normal | `<leader>j`     | `:CtrlP<cr>`                                     | Open CtrlP to find files.                   |
| Normal | `<leader>b`     | `:CtrlPBuffer<cr>`                               | Open CtrlP to find buffers.                 |

### snipMate (Snippet Manager)
*Plugin for inserting pre-defined code snippets.*
| Mode   | Shortcut        | Action                                           | Description                                 |
|--------|-----------------|--------------------------------------------------|---------------------------------------------|
| Insert | `<C-j>`         | `<C-r>=snipMate#TriggerSnippet()<cr>`            | Trigger snipMate snippet expansion.         |
| Select | `<C-j>`         | `<esc>i<right><C-r>=snipMate#TriggerSnippet()<cr>`| Trigger snipMate snippet expansion.         |

### NERDTree (File Explorer)
*A tree explorer for navigating the filesystem.*
| Mode   | Shortcut        | Action                                           | Description                                 |
|--------|-----------------|--------------------------------------------------|---------------------------------------------|
| Normal | `<leader>nn`    | `:NERDTreeToggle<cr>`                            | Toggle NERDTree file explorer.              |
| Normal | `<leader>nb`    | `:NERDTreeFromBookmark<Space>`                   | Open NERDTree from a bookmark (prompts for bookmark). |
| Normal | `<leader>nf`    | `:NERDTreeFind<cr>`                              | Find and select current file in NERDTree.   |

### vim-multiple-cursors
*Plugin for using multiple cursors simultaneously.*
| Mode   | Shortcut        | Action Setting                                   | Description                                 |
|--------|-----------------|--------------------------------------------------|---------------------------------------------|
| Normal | `<C-s>`         | `g:multi_cursor_start_word_key` / `g:multi_cursor_next_key` | Start multi-cursor on word under cursor / Add next identical word. **Note: Potential conflict/override.** |
| Normal | `<A-s>`         | `g:multi_cursor_select_all_word_key`             | Select all identical words for multi-cursor. |
| Normal | `g<C-s>`        | `g:multi_cursor_start_key`                       | Start multi-cursor at current position.     |
| Normal | `g<A-s>`        | `g:multi_cursor_select_all_key`                  | Select all matching patterns for multi-cursor. |
| Normal | `<C-p>`         | `g:multi_cursor_prev_key`                        | Add previous identical word. **Note: Conflicts with YankStack `<C-p>`.** |
| Normal | `<C-x>`         | `g:multi_cursor_skip_key`                        | Skip current match and find next for multi-cursor. |
| Normal | `<Esc>`         | `g:multi_cursor_quit_key`                        | Quit multi-cursor mode.                     |

### surround.vim
*Plugin for easily adding/changing/deleting "surroundings" like parentheses, quotes, tags.*
| Mode   | Shortcut        | Action                                           | Description                                 |
|--------|-----------------|--------------------------------------------------|---------------------------------------------|
| Visual | `Si`            | `S(i_<esc>f)`                                    | Surround selection with `_()`. (Often for gettext) |
| Visual (Mako) | `Si`      | `S"i${ _(<esc>2f"a) }<esc>`                      | Surround selection with `${ _("...") }` for Mako templates. |

### Goyo (Distraction-free Writing)
*Plugin for a focused writing environment.*
| Mode   | Shortcut        | Action                                           | Description                                 |
|--------|-----------------|--------------------------------------------------|---------------------------------------------|
| Normal | `<leader>z`     | `:Goyo<cr>`                                      | Toggle Goyo (distraction-free) mode.        |

### ALE (Asynchronous Lint Engine)
*Plugin for linting and fixing code.*
| Mode   | Shortcut        | Action                                           | Description                                 |
|--------|-----------------|--------------------------------------------------|---------------------------------------------|
| Normal | `<leader>a`     | `<Plug>(ale_next_wrap)`                          | Go to the next ALE lint warning/error.      |

### GitGutter
*Plugin to show Git diff information in the sign column.*
| Mode   | Shortcut        | Action                                           | Description                                 |
|--------|-----------------|--------------------------------------------------|---------------------------------------------|
| Normal | `<leader>d`     | `:GitGutterToggle<cr>`                           | Toggle GitGutter display (diff signs).      |

### Fugitive (Git Wrapper)
*A Git wrapper that makes it easy to run Git commands from Vim.*
| Mode   | Shortcut        | Action                                           | Description                                 |
|--------|-----------------|--------------------------------------------------|---------------------------------------------|
| Normal | `<leader>v`     | `:.GBrowse!<CR>`                                 | Open current line in Git repository browser (e.g., GitHub). |
| Visual | `<leader>v`     | `:GBrowse!<CR>`                                  | Open selected lines in Git repository browser. |

---

## VI. Filetype-Specific Mappings

These shortcuts are active only for specific filetypes.

### Python (`.py` files)
| Mode   | Shortcut        | Action                                           | Description                                 |
|--------|-----------------|--------------------------------------------------|---------------------------------------------|
| Normal | `F`             | `:set foldmethod=indent<cr>`                     | Set code folding method to indent.          |
| Normal | `<leader>1`     | `/class `                                        | Search forward for `class `.                |
| Normal | `<leader>2`     | `/def `                                          | Search forward for `def `.                  |
| Normal | `<leader>C`     | `?class `                                        | Search backward for `class `.               |
| Normal | `<leader>D`     | `?def `                                          | Search backward for `def `.                 |
| Insert | `$r`            | `return `                                        | Insert `return `.                          |
| Insert | `$i`            | `import `                                        | Insert `import `.                          |
| Insert | `$p`            | `print `                                         | Insert `print `.                           |
| Insert | `$f`            | `# --- <esc>a`                                   | Insert `# --- ` (comment separator).       |

### JavaScript & TypeScript (`.js`, `.ts` files)
| Mode   | Shortcut        | Action                                           | Description                                 |
|--------|-----------------|--------------------------------------------------|---------------------------------------------|
| Insert | `<C-t>`         | `console.log();<esc>hi`                          | Insert `console.log();`.                    |
| Insert | `<C-a>`         | `alert();<esc>hi`                                | Insert `alert();`.                          |
| Insert | `$r`            | `return `                                        | Insert `return `.                          |
| Insert | `$f`            | `// --- PH<esc>FP2xi`                            | Insert `// --- ` (comment separator).      |

---

This guide should help you leverage the custom mappings in this Vim setup. Remember that Vim is highly extensible, and you can always modify these or add your own in your `my_configs.vim` file.
