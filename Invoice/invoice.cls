%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  Copyright (c) 2011 Trey Hunner                                          %
%                                                                          %
%  Permission is hereby granted, free of charge, to any person obtaining   %
%  a copy of this software and associated documentation files (the         %
%  "Software"), to deal in the Software without restriction, including     %
%  without limitation the rights to use, copy, modify, merge, publish,     %
%  distribute, sublicense, and/or sell copies of the Software, and to      %
%  permit persons to whom the Software is furnished to do so, subject to   %
%  the following conditions:                                               %
%                                                                          %
%  The above copyright notice and this permission notice shall be          %
%  included in all copies or substantial portions of the Software.         %
%                                                                          %
%  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,         %
%  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF      %
%  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND                   %
%  NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE  %
%  LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION  %
%  OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION   %
%  WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.         %
%                                                                          %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\ProvidesClass{invoice}

\LoadClass[10pt]{article}

\usepackage[letterpaper,hmargin=0.79in,vmargin=0.79in]{geometry}
\usepackage[parfill]{parskip} % Do not indent paragraphs
\usepackage{fp} % Fixed-point arithmetic
\usepackage{calc} % Counters for totaling hours and cost
\usepackage{longtable}
\usepackage{eurosym}
\usepackage[dutch]{babel}

\usepackage[scaled]{helvet}
\renewcommand\familydefault{\sfdefault}
\usepackage[T1]{fontenc}

\pagestyle{empty} % No page numbers
\linespread{1.5} % Line spacing

\setlength{\doublerulesep}{\arrayrulewidth} % Double rules look like one thick one

% Command for setting a default hourly rate
\newcommand{\feetype}[1]{
    \textbf{#1}
    \\
}

% Counters for totaling up hours and dollars
\newcounter{hours} \newcounter{subhours} \newcounter{cost} \newcounter{subcost} \newcounter{uitbtwhoog} \newcounter{btwhoog} \newcounter{uitbtwgeen} \newcounter{btwgeen}
\setcounter{hours}{0} \setcounter{subhours}{0} \setcounter{cost}{0} \setcounter{subcost}{0} \setcounter{uitbtwhoog}{0} \setcounter{btwhoog}{0} \setcounter{uitbtwgeen}{0} \setcounter{btwgeen}{0}
% Formats inputed number with 2 digits after the decimal place
\newcommand*{\formatNumber}[1]{\FPround{\cost}{#1}{2}\cost} %

% Returns the total of counter
\newcommand*{\total}[1]{\FPdiv{\t}{\arabic{#1}}{1000}\formatNumber{\t}}
%\newcommand*{\totalbtw}
% Create an invoice table
\newenvironment{invoiceTable}{
    % Create a new row from title, unit quantity, unit rate, and unit name
    \newcommand*{\unitrow}[4]{%
         \addtocounter{cost}{1000 * \real{##2} * \real{##3}}%  \formatNumber{##2}
         \addtocounter{subcost}{1000 * \real{##2} * \real{##3}}%
         ##1 & ##2 ##4 & \EUR{\formatNumber{##3}} & \FPmul{\cost}{##2}{##3}\EUR{\formatNumber{\cost}}%
         \\
    }
    % Create a new row from title and expense amount
    \newcommand*{\feerow}[2]{%
         \addtocounter{cost}{1000 * \real{##2}}%
         \addtocounter{subcost}{1000 * \real{##2}}%
         ##1 & & \EUR{\formatNumber{##2}} & \FPmul{\cost}{##2}{1}\EUR{\formatNumber{\cost}}%
         \\
    }

    \newcommand{\subtotalNoStar}{
        {\bf Subtotaal} & {\bf \total{subhours} Uur} &  & {\bf \EUR{\total{subcost}}}
        \setcounter{subcost}{0}
        \setcounter{subhours}{0}
        \\*[1.5ex]
    }
    \newcommand{\subtotalStar}{
        {\bf Subtotaal} & & & {\bf \EUR{\total{subcost}}}
        \setcounter{subcost}{0}
        \\*[1.5ex]
    }
    \newcommand{\subtotal}{
         \hline
         \@ifstar
         \subtotalStar%
         \subtotalNoStar%
    }
    \newcommand*{\setendtotal}[4]{%
        \addtocounter{uitbtwhoog}{1000 * \real{##1}}%
        \addtocounter{btwhoog}{1000 * \real{##2}}
        \addtocounter{uitbtwgeen}{1000 * \real{##3}}%
        \addtocounter{btwgeen}{1000 * \real{##4}}%
    }
    % Create a new row from date and hours worked (use stored fee type and hourly rate)
    \newcommand*{\hourrow}[3]{%
        \addtocounter{hours}{1000 * \real{##2}}%
        \addtocounter{subhours}{1000 * \real{##2}}%
        \unitrow{##1}{##2}{##3}{Uur}%
    }
    \renewcommand{\tabcolsep}{0.8ex}
    \setlength\LTleft{0pt}
    \setlength\LTright{0pt}
    \begin{longtable}{@{\extracolsep{\fill}\hspace{\tabcolsep}} p{10cm} r r r}%l r r r }
    \hline
    {\bf Omschrijving} & \multicolumn{1}{c}{\bf Aantal} & \multicolumn{1}{c}{\bf Stukprijs} & \multicolumn{1}{c}{\bf Totaal Incl. btw} \\*
    \hline\hline
    \endhead
}{
    \hline\hline%\hline
    {\bf Totaal incl. BTW} & & & {\bf \EUR{\total{cost}}} \\
    %{\bf Btw-vrij} & & & {\bf \EUR{\total{btwgeen}}} \\
    {\bf BTW 21\% uit \EUR{\total{uitbtwhoog}}} & & & {\bf \EUR{\total{btwhoog}}} \\
    {\bf BTW margeregeling uit \EUR{\total{uitbtwgeen}}} & & & {\bf \EUR{\total{btwgeen}}} \\
    %\hline
    \\*[1ex]
    {\bf Totaal te betalen bedrag:} & & & {\bf \EUR{\total{cost}}}
    \end{longtable}
}
