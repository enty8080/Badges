"""
MIT License

Copyright (c) 2020-2024 EntySec

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from .__main__ import Badges
from colorscript import ColorScript


class Tables(object):

    def print_table(self, name: str, headers: tuple, *args, **kwargs) -> None:
        """ Print table.

        TODO: This is very very bad and not optimized code.

        Usage example: print_table('Example', ('Col1', 'Col2'), *[(1,2),(3,4)])
        Sample output:

        Example
        =======

          Col1    Col2
          ----    ----
          1       2
          3       4

        :param str name: table name
        :param tuple headers: tuple of headers
        :return None: None
        """

        extra_fill = kwargs.get("extra_fill", 4)

        if not all(map(lambda x: len(x) == len(headers), args)):
            return

        fill = []
        headers_line = ' ' * 4

        def custom_len(x):
            x = str(x)
            try:
                if '\033' in x:
                    return len(x) - 9 * x.count('\033') // 2
                return len(x)
            except TypeError:
                return 0

        for idx, header in enumerate(headers):
            header = str(header)
            header = ColorScript().strip(header)
            column = [custom_len(ColorScript().parse(str(arg[idx]))) for arg in args]
            column.append(len(header))

            current_line_fill = max(column) + extra_fill
            fill.append(current_line_fill)
            headers_line = "".join(
                (
                    headers_line,
                    f"%bold%line{header}%end" + ' ' * (current_line_fill - len(header))
                )
            )

        content = (
            '\n%bold%line' + name[0].upper() + name[1:] + '%end:\n\n' +
            headers_line.rstrip() + '\n'
        )

        for arg in args:
            content_line = "    "
            for idx, element in enumerate(arg):
                element = ColorScript().parse(str(element))
                fill_line = fill[idx]

                if '\033' in element:
                    fill_line = fill[idx] + 9 * element.count('\033') // 2

                content_line = "".join(
                    (content_line, "{:<{}}".format(element, fill_line))
                )
            content += content_line.rstrip() + '\n'

        Badges().print_empty(content.rstrip())
        Badges().print_empty()
