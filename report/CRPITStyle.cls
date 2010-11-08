% CRPITStyle DOCUMENT CLASS
%    adapted from ACM Style by John Roddick

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{CRPITStyle}

%
% Define the conditionals and command for the options.
%
\newif\if@CRPITStyle\@CRPITStyletrue
\long\def\ifCRPITStyle#1#2{\if@CRPITStyle#1\else#2\fi}
\newif\ifpreprint

%
% Declare and process the options
%
\DeclareOption{draft}{\PassOptionsToClass{draft}{article}}
\DeclareOption{fleqn}{\PassOptionsToClass{fleqn}{article}}
\DeclareOption{final}{\PassOptionsToClass{final}{article}}
\DeclareOption{twocolumn}{\PassOptionsToClass{twocolumn}{article}}
\DeclareOption{twoside}{\PassOptionsToClass{twoside}{article}}
\DeclareOption{preprint}{\preprinttrue}
\DeclareOption{a4paper}{\PassOptionsToClass{a4paper}{article}}
%
% Let them off with just a warning for any other option
%
\DeclareOption*{\ClassWarningNoLine{CRPITStyle}{Unknown option `\CurrentOption'}}
%\DeclareOption*{\ClassError{CRPITStyle}
%   {The `\CurrentOption' option is not supported}
%   {Remove the `\CurrentOption' option from the
%    \protect\documentclass\space line.}}

\ExecuteOptions{twocolumn,a4paper}
\ProcessOptions

%
% This class simply modifies a few behaviors of the article class,
% so load it now
%
\LoadClass{article}

%
\renewcommand\baselinestretch{1}

\renewcommand\normalsize{%
   \@setfontsize\normalsize\@xpt\@xpt 
   \abovedisplayskip 10\p@ \@plus2\p@ \@minus4.5\p@%
   \abovedisplayshortskip  \z@ \@plus3\p@%
   \belowdisplayshortskip  5.4\p@ \@plus3\p@ \@minus3\p@%
   \belowdisplayskip \abovedisplayskip
   \let\@listi\@listI}
\normalsize
\renewcommand\small{%
   \@setfontsize\small\@viiipt{9}%
   \abovedisplayskip 7.6\p@ \@plus 3\p@ \@minus 4\p@%
   \abovedisplayshortskip \z@ \@plus2\p@%
   \belowdisplayshortskip 3.6\p@ \@plus2\p@ \@minus 2\p@
   \def\@listi{\leftmargin\leftmargini
                \topsep 4\p@ \@plus 2\p@ \@minus 2\p@
                \parsep 2\p@ \@plus 1\p@ \@minus 1\p@
                \itemsep \parsep}
   \belowdisplayskip \abovedisplayskip
}
\renewcommand\footnotesize{%
   \@setfontsize\footnotesize\@viipt{8}
   \abovedisplayskip 6.4\p@ \@plus 2\p@ \@minus 4\p@%
   \abovedisplayshortskip \z@ \@plus 1\p@%
   \belowdisplayshortskip 2.7\p@ \@plus 1\p@ \@minus 2\p@
   \def\@listi{\leftmargin\leftmargini
               \topsep 3\p@ \@plus 1\p@ \@minus 1\p@
               \parsep 2\p@ \@plus 1\p@ \@minus 1\p@
               \itemsep \parsep}%
   \belowdisplayskip \abovedisplayskip
}
\renewcommand\scriptsize{\@setfontsize\scriptsize\@viipt{8pt}}
\renewcommand\tiny{\@setfontsize\tiny\@vpt{6pt}}
\renewcommand\large{\@setfontsize\large\@xipt{13.6\p@}}
\renewcommand\Large{\@setfontsize\Large\@xiipt{14\p@}}
\renewcommand\LARGE{\@setfontsize\LARGE\@xivpt{18\p@}}
\renewcommand\huge{\@setfontsize\huge\@xviipt{22\p@}}
\renewcommand\Huge{\@setfontsize\Huge\@xxpt{25\p@}}

\setlength\parindent{13.5\p@}    % This is what normally used for one
                                 % column.  Should it be 1em for us?
\setlength\headheight{0\p@}
\setlength\headsep{0\p@}
\setlength\headheight{0\p@}
\setlength\headsep{0\p@}
\setlength\footskip{30\p@}
%
% We inherit 
%\topskip 10pt 
%\maxdepth .5\topskip
% from size10.clo loaded via article.cls
%
\setlength\textwidth{40pc}
\setlength\textheight{730\p@}
\setlength\oddsidemargin{4.5pc}
\addtolength\oddsidemargin{-0.9in}    % Correct for LaTeX gratuittousness
\setlength\evensidemargin{4.5pc}
\addtolength\evensidemargin{-0.9in}   % Correct for LaTeX gratuittousness
\setlength\marginparwidth{0\p@}     % Margin pars are not allowed.
\setlength\marginparsep{11\p@}
\setlength\marginparpush{5\p@}
\setlength\topmargin{4.5pc}
\addtolength\topmargin{-1.2in}         % Correct for LaTeX gratuitousness
%
\addtolength\topmargin{-37\p@} % Leave 37pt above text for headers
\setlength\headheight{12\p@}
\setlength\headsep{25\p@}

\setlength\footnotesep{5.6\p@}
\setlength{\skip\footins}{8.1\p@ \@plus 4\p@ \@minus 2\p@}
\setlength\floatsep{11\p@ \@plus 2\p@ \@minus 2\p@}
\setlength\textfloatsep{18\p@ \@plus 2\p@ \@minus 4\p@}
\setlength\intextsep{11\p@ \@plus 2\p@ \@minus 2\p@}
\setlength\dblfloatsep{11\p@ \@plus 2\p@ \@minus 2\p@}
\setlength\dbltextfloatsep{18\p@ \@plus 2\p@ \@minus 4\p@}
%
% These values will be inherited from the default size10.clo file
% included when we load the base article class.  I include them
% here for completeness in case we split out the size9.clo file someday.
%   --DAB
\setlength\@fptop{0\p@ \@plus 1fil}
\setlength\@fpsep{8\p@ \@plus 2fil}
\setlength\@fpbot{0\p@ \@plus 1fil}
\setlength\@dblfptop{0\p@ \@plus 1fil}
\setlength\@dblfpsep{8\p@ \@plus 2fil}
\setlength\@dblfpbot{0\p@ \@plus 1fil}
\setlength\partopsep{2\p@ \@plus 1\p@ \@minus 1\p@}
%
% I think that all of these should be renewcommands.  I also think
% that \setlength should be used.  But, they are not in the size10.clo
% file that I am following.   --DAB
%
\renewcommand\@listI{\leftmargin\leftmargini 
                     \parsep 3.6\p@ \@plus 2\p@ \@minus 1\p@%
                     \topsep 7.2\p@ \@plus 2\p@ \@minus 4\p@%
                     \itemsep 3.6\p@ \@plus 2\p@ \@minus 1\p@}
\let\@listi\@listI
\@listi
\def\@listii {\leftmargin\leftmarginii
              \labelwidth\leftmarginii
              \advance\labelwidth-\labelsep
              \topsep 3.6\p@ \@plus 2\p@ \@minus 1\p@
              \parsep 1.8\p@ \@plus 0.9\p@ \@minus 0.9\p@
              \itemsep \parsep}
\def\@listiii{\leftmargin\leftmarginiii
              \labelwidth\leftmarginiii
              \advance\labelwidth-\labelsep
              \topsep 1.8\p@ plus 0.9\p@ minus 0.9\p@
              \parsep \z@
              \partopsep 1\p@ plus 0\p@ minus 1\p@
              \itemsep \topsep}
\def\@listiv {\leftmargin\leftmarginiv
              \labelwidth\leftmarginiv
              \advance\labelwidth-\labelsep}
\def\@listv  {\leftmargin\leftmarginv
              \labelwidth\leftmarginv
              \advance\labelwidth-\labelsep}
\def\@listvi {\leftmargin\leftmarginvi
              \labelwidth\leftmarginvi
              \advance\labelwidth-\labelsep}
%
% End of the "size9.clo" commands
%**********************************************************************

%
% here's a few things that I didn't find in either article.cls or
% size10.clo, so I left them here.  --DAB
%
\setlength\columnsep{1.5pc}          %    Space between columns
\setlength\columnseprule{0\p@}     %    Width of rule between columns.
\hfuzz 1pt               % Allow some variation in column width, otherwise it's
                         % too hard to typeset in narrow columns.


%**********************************************************************
%
% Now we get on with overriding things found in article.cls
%
\setlength\parindent{13.5\p@}

%
% This command is used to format section headings.  The format is the only
% thing that differs between these section commands and the ones in
% article.cls.
%
% Although the original documentation says that sans-serif is supposed to be
% used for section titles, the file as I received uses roman.  The
% commented out line implements sans-serif.  Be sure to comment out the
% \bfseries line if you switch.
%   --DAB
%
\newcommand\@acmtitlestyle{\normalsize\bfseries}
%\newcommand\@acmtitlestyle{\normalsize\sffamily}

\renewcommand\section{\@startsection {section}{1}{\z@}%
                                     {-3.5ex \@plus -1ex \@minus -.2ex}%
                                     {2.3ex \@plus .2ex}%
                                     {\@acmtitlestyle}}
\renewcommand\subsection{\@startsection{subsection}{2}{\z@}%
                                       {-3.25ex \@plus -1ex \@minus -.2ex}%
                                       {1.5ex \@plus .2ex}%
                                       {\@acmtitlestyle}}
\renewcommand\subsubsection{\@startsection{subsubsection}{3}{\z@}%
                                          {-3.25ex \@plus -1ex \@minus -.2ex}%
                                          {1.5ex \@plus .2ex}%
                                          {\@acmtitlestyle}}
\renewcommand\paragraph{\@startsection{paragraph}{4}{\z@}%
                                      {3.25ex \@plus 1ex \@minus .2ex}%
                                      {-1em}%
                                      {\@acmtitlestyle}}
\renewcommand\subparagraph{\@startsection{subparagraph}{4}{\parindent}%
                                         {3.25ex \@plus 1ex \@minus .2ex}%
                                         {-1em}%
                                         {\@acmtitlestyle}}

\setcounter{secnumdepth}{3}

\setlength\arraycolsep{4.5\p@}
\setlength\tabcolsep{5.4\p@}
\setlength\doublerulesep{1.8\p@}

\setlength\fboxsep{2.7\p@}
\setlength\fboxrule{.4\p@}

\def\tableofcontents{\ClassError{CRPITStyle}%
  {\protect\tableofcontents: Tables of contents are not allowed in the `CRPITStyle' document class}%
  {Remove the \protect\tableofcontents\space command from the file}}

\def\listoffigures{\ClassError{CRPITStyle}%
  {\protect\listoffigures: Lists of figures are not allowed in the `CRPITStyle' document class}%
  {Remove the \protect\listoffigures\space command from the file}}

\def\listoftables{\ClassError{CRPITStyle}%
   {\protect\listoftables: Lists of tables are not allowed in the `CRPITStyle' document class}%
   {Remove the \protect\listoftables\space command from the file}}
\let\l@table\l@figure

%
% Added \@makefntext definition so that the mark would not over print
% the beginning of the \thanks text.  --DAB
%
\def\maketitle{\par
 \begingroup
   \def\thefootnote{\fnsymbol{footnote}}%
   \def\@makefnmark{\hbox to 0pt{$\m@th^{\@thefnmark}$\hss}}%
   \long\def\@makefntext##1{\parindent 1em\noindent
               \hbox to1.8em{\hss$\m@th^{\@thefnmark}$}##1}%
   \if@twocolumn
     \twocolumn[\@maketitle]
     \else 
     \global\@topnum\z@        % Prevents figures from going at top of page.
     \@maketitle \fi
   \thispagestyle{empty}\@thanks  % UE: Changed {empty} to {plain}
 \endgroup
 \setcounter{footnote}{0}
 \let\maketitle\relax
 \let\@maketitle\relax
 \gdef\@thanks{}\gdef\@author{}\gdef\@title{}\gdef\@affili{}\let\thanks\relax}

%
% extra declarations needed for our version of @maketitle
%
\newbox\@acmtitlebox
\gdef\affili{}
\def\affiliation#1{\gdef\affili{#1}}

%
% The modified @maketitle
%
\def\@maketitle{
\setbox\@acmtitlebox\vbox{%
   \vskip 2em                 % Vertical space above title.
   \begin{center}
    {\LARGE \bf \@title \par}     % Title set in \LARGE size.
    \vskip 1.5em                % Vertical space after title.
    {\large \bf                 % each author set in \large, in a
     \lineskip .5em             % tabular environment
     \begin{tabular}[t]{c} \@author
     \end{tabular}\par}
     \vskip 1em
     \begin{center}
        \affili
     \end{center}
     \vskip 1.5em              % Vertical space after author.
   \end{center}}
 \dimen0=\ht\@acmtitlebox
 \advance\dimen0 by -13.5pc\relax
 \unvbox\@acmtitlebox
 \ifdim\dimen0<0.0pt\relax\vskip-\dimen0\fi}

\long\def\unmarkedfootnote#1{{\long\def\@makefntext##1{##1}\footnotetext{#1}}}

\def\copyrightspace{\unmarkedfootnote{\vrule height 4.5pc
                                             width  0in depth 0in}}

\def\toappear#1%
    {\unmarkedfootnote{\vrule height 2.25pc%
                                          depth  2.5pc width 0in%
                                   \parbox{3.2in}{\small #1}}\pagestyle{empty}
    }

\def\toappearstandard%
    {\unmarkedfootnote{\vrule height 2.25pc%
                                          depth  2.5pc width 0in%
                                   \parbox{3.2in}{\small 
Copyright \copyright\conferenceyear, Australian Computer Society, Inc.  This paper appeared at the \conferencenameandplace.  Conferences in Research and Practice in Information Technology (CRPIT), Vol.\ \volumenumber, \editorname, Ed. Reproduction for academic, not-for-profit purposes permitted provided this text is included.}} \pagestyle{empty}
    }

\def\archivestandard%
    {\unmarkedfootnote{\vrule height 2.25pc%
                                          depth  2.5pc width 0in%
                                   \parbox{3.2in}{\small 
Copyright \copyright\conferenceyear, retained by author(s).  This paper appeared at the \conferencenameandplace, \editorname, Ed. The paper is reprinted by permission in Conferences in Research and Practice in Information Technology (CRPIT), Vol.\ \volumenumber. Reproduction for academic, not-for profit purposes permitted.  Format may differ from original.}} \pagestyle{empty}
    }
    
\def \toappeargovwork%
    {\unmarkedfootnote{\vrule height 2.25pc%
                                          depth  2.5pc width 0in%
                                   \parbox{3.2in}{\small 
Copyright \copyright\conferenceyear, \copyrightholder. This paper appeared at the \conferencenameandplace. Conferences in Research and Practice in Information Technology (CRPIT), Vol.\ \volumenumber, \editorname, Ed. Reproduction for academic, not-for-profit purposes permitted provided this text is included.}} \pagestyle{empty}
    }

\def\submitted#1%
    {\unmarkedfootnote{\vrule height 2.25pc%
                                          depth  2.5pc width 0in%
                                   \parbox{3.2in}{\small #1}}\pagestyle{empty}
    }

\def\submittedstandard%
    {\unmarkedfootnote{\vrule height 2.25pc%
                                          depth  2.5pc width 0in%
                                   \parbox{3.2in}{\small 
This paper has been submitted to the \conferencenameandplace.  Conferences in Research and Practice in Information Technology (CRPIT), Vol.\ \volumenumber, \editorname, Ed. Copyright \copyright\conferenceyear\ currently remains with the author(s) but will be transferred to the Australian Computer Society, Inc.\ if the paper appears in the proceedings.}} \pagestyle{empty}
    }

\def \submittedgovwork%
    {\unmarkedfootnote{\vrule height 2.25pc%
                                          depth  2.5pc width 0in%
                                   \parbox{3.2in}{\small 
Copyright \copyright\conferenceyear, \copyrightholder. This paper has been submitted to the \conferencenameandplace.  Conferences in Research and Practice in Information Technology (CRPIT), Vol.\ \volumenumber. \editorname, Ed.  Reproduction for academic, not-for-profit purposes permitted provided this text is included.}} \pagestyle{empty}
    }

\def\marginpar{\ClassError{CRPITStyle}%
   {The \protect\marginpar command is not allowed in the `CRPITStyle' document class}%
   {Remove the \protect\marginpar\space command from the file}}

\mark{{}{}}   % Initializes TeX's marks

%% Headings are ignored unless the [preprint] option is in force.
\ifpreprint\else % preprint off -- all \pagestyle commands ==> \pagestyle{empty}.
%  \let\ps@plain\ps@empty  % UE: Commented this line out
  \let\ps@headings\ps@empty
  \let\ps@myheadings\ps@empty
\fi

\raggedbottom               % Ragged bottom

\endinput
%%
%% End of file `CRPITStyle.cls'.
