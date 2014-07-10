syntax on
set smartindent
set tabstop=4
set shiftwidth=4
set expandtab

" Show line numbers.
set number
" Show cursor position.
set ruler
" Set the terminal's title
set title
autocmd BufWritePre * :%s/\s\+$//e
