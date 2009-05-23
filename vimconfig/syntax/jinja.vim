" Vim syntax file
" Language:	Jinja template
" Maintainer:	Armin Ronacher <armin.ronacher@active-4.com>
" Last Change:	2007 Apr 8
"
" Known Bugs:
"   because of odd limitations dicts and the modulo operator
"   appear wrong in the template.
"

" For version 5.x: Clear all syntax items
" For version 6.x: Quit when a syntax file was already loaded
if version < 600
  syntax clear
elseif exists("b:current_syntax")
  finish
endif

syntax case match

" Jinja template built-in tags and parameters
syn keyword jinjaStatement containedin=jinjaVarBlock,jinjaTagBlock contained and block cycle elif else endblock endfilter endfor endif endmacro endtrans extends filter for if in include is macro not or pluralize recursive set trans

" Variable Names
syn match jinjaVariable containedin=jinjaVarBlock,jinjaTagBlock contained skipwhite /[a-zA-Z_][a-zA-Z0-9_]*/
syn keyword jinjaSpecial containedin=jinjaVarBlock,jinjaTagBlock contained _ false true undefined none loop super

" Filter
syn match jinjaOperator "|" containedin=jinjaVarBlock,jinjaTagBlock contained nextgroup=jinjaFilter
syn match jinjaFilter contained skipwhite /[a-zA-Z_][a-zA-Z0-9_]*/

" Jinja template constants
syn region jinjaString containedin=jinjaVarBlock,jinjaTagBlock contained start=/"/ skip=/\\"/ end=/"/
syn region jinjaString containedin=jinjaVarBlock,jinjaTagBlock contained start=/'/ skip=/\\'/ end=/'/
syn match jinjaNumber containedin=jinjaVarBlock,jinjaTagBlock contained /[0-9]\+\(\.[0-9]\+\)\?/

" Operators
syn match jinjaOperator containedin=jinjaVarBlock,jinjaTagBlock contained /[+\-*\/<>=!,:]/
syn match jinjaPunctuation containedin=jinjaVarBlock,jinjaTagBlock contained /[()\[\]]/
syn match jinjaOperator containedin=jinjaVarBlock,jinjaTagBlock contained /\./ nextgroup=jinjaAttribute
syn match jinjaAttribute contained /[a-zA-Z_][a-zA-Z0-9_]*/

" Jinja template tag and variable blocks
syn region jinjaTagBlock start=/{%-\?/ end=/-\?%}/ containedin=ALLBUT,jinjaTagBlock,jinjaVarBlock,jinjaRaw
syn region jinjaVarBlock start=/{{-\?/ end=/-\?}}/ containedin=ALLBUT,jinjaTagBlock,jinjaVarBlock,jinjaRaw

" Jinja template 'raw' tag
syn region jinjaRaw start="{%\s*raw\s*%}" end="{%\s*endraw\s*%}" containedin=ALLBUT,jinjaTagBlock,jinjaVarBlock

" Jinja comments
syn region jinjaComment start="{#" end="#}" containedin=ALL

" Define the default highlighting.
" For version 5.7 and earlier: only when not done already
" For version 5.8 and later: only when an item doesn't have highlighting yet
if version >= 508 || !exists("did_jinja_syn_inits")
  if version < 508
    let did_jinja_syn_inits = 1
    command -nargs=+ HiLink hi link <args>
  else
    command -nargs=+ HiLink hi def link <args>
  endif

  HiLink jinjaPunctuation jinjaOperator
  HiLink jinjaAttribute jinjaVariable

  HiLink jinjaSpecial Special
  HiLink jinjaOperator Normal
  HiLink jinjaRaw Normal
  HiLink jinjaTagBlock PreProc
  HiLink jinjaVarBlock PreProc
  HiLink jinjaStatement Statement
  HiLink jinjaFilter Function
  HiLink jinjaVariable Identifier
  HiLink jinjaString Constant
  HiLink jinjaNumber Constant
  HiLink jinjaComment Comment

  delcommand HiLink
endif

let b:current_syntax = "jinja"
