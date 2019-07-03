import subprocess
import random
import string
import argparse
from mako.template import Template


def generate_tex(year=2019):

    latex_template = r"""\documentclass[12pt]{article}
\usepackage[landscape, a4paper, margin=1cm]{geometry}
\usepackage{calendar}
\pagestyle{empty}

\setlength{\parindent}{0pt}
\StartingDayNumber=2

<%! import calendar %>

\begin{document}

% for imonth in range(12):

\begin{center}
    \textsc{\LARGE ${calendar.month_name[imonth+1]}\\\

    {\large ${year}}}
\end{center}


<%
    monthcal = calendar.monthcalendar(year, imonth+1)
    blank_days = monthcal[0].count(0)
    days_in_month = max(monthcal[-1])
%>

% if len(monthcal) == 4:
\def\boxheight{0.16\textheight}
% elif len(monthcal) == 5:
\def\boxheight{0.12\textheight}
% elif len(monthcal) ==6:
\def\boxheight{0.10\textheight}
% else:
Unimplemented number of weeks
% endif

\begin{calendar}{\textwidth}

% for j in range(blank_days):
\BlankDay
% endfor

\setcounter{calendardate}{1}

% for j in range(days_in_month):
\day{}{\vspace{\boxheight}}
% endfor

\finishCalendar
\end{calendar}

\pagebreak
% endfor
\end{document}"""

    result = Template(latex_template).render(year=year)

    return result


if __name__ == '__main__':

    # {{{ parse args

    parser = argparse.ArgumentParser(description='Generate PDF for a calendar year')
    parser.add_argument('--year', metavar='Y', type=int, nargs=1,
                    help="Year of the calendar(for ex. '2019')")
    parser.add_argument('--fname', metavar='F', type=str, nargs=1,
                    help="filename of the PDF to generate(for ex. "
                    "'cal-2019.pdf')")

    args = parser.parse_args()
    filename = args.fname[0]
    year = args.year[0]

    if not filename.endswith('.pdf'):
        raise ValueError('Filename must have a .pdf extension')

    # }}}

    generated_tex = generate_tex(year=year)

    # {{{ get the pdf

    tex_filename = ('/tmp/'
            + ''.join(random.choice(string.ascii_letters) for _ in
                range(9)) + '.tex')
    gen_pdf_filename = tex_filename[:-4] + '.pdf'
    with open(tex_filename, 'w') as f:
        f.write(generated_tex)
    subprocess.call(('pdflatex -output-directory=/tmp {0}'.format(
        tex_filename)).split())

    # }}}

    # move the pdf to desired filename
    subprocess.call(('mv {0} {1}'.format(gen_pdf_filename, filename)).split())

# vim:foldmethod=marker
